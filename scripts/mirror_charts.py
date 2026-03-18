#!/usr/bin/env python3
"""ABOUTME: Mirror Helm charts from upstream Helm repos into AWS ECR as OCI artifacts.
ABOUTME: Downloads chart tarballs from Helm chart repositories, then uses the
`helm` CLI to save and push charts as OCI artifacts into ECR. Creates ECR
repositories if they don't exist.

Requirements:
  - helm >= 3.11 (for `helm chart save` / `helm chart push` / `helm registry login`)
  - AWS CLI configured OR environment credentials for boto3
  - Python packages: boto3, pyyaml

Usage:
  python3 scripts/mirror_charts.py --charts charts-to-mirror.yaml --region us-east-1

The input YAML lists charts to mirror, e.g.:

charts:
  - name: kube-prometheus-stack
    repo: https://prometheus-community.github.io/helm-charts
    chart: kube-prometheus-stack
    version: "67.9.0"
    dest_repo: monitoring/kube-prometheus-stack

See scripts/charts-to-mirror.yaml for an example shipped with the repo.
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

import boto3
import yaml


def run(cmd, capture=False, input_data=None, check=True, env=None):
    print("$", " ".join(cmd))
    if capture:
        return subprocess.check_output(cmd, input=input_data, env=env)
    else:
        subprocess.check_call(cmd, env=env)


def ensure_helm():
    try:
        run(["helm", "version"], capture=True)
    except Exception as e:
        print("helm CLI not found or not working. Install helm >= 3.11.")
        raise


def ensure_aws_cli():
    try:
        run(["aws", "--version"], capture=True)
    except Exception:
        print("aws CLI not found. Install and configure AWS CLI or provide AWS creds for boto3.")
        # Not fatal; boto3 can use env creds. But we need AWS CLI for login password piping.


def ecr_repo_exists(ecr, repository_name):
    try:
        ecr.describe_repositories(repositoryNames=[repository_name])
        return True
    except ecr.exceptions.RepositoryNotFoundException:
        return False


def create_ecr_repo(ecr, repository_name):
    print(f"Creating ECR repository: {repository_name}")
    ecr.create_repository(repositoryName=repository_name)


def aws_account_id():
    sts = boto3.client("sts")
    return sts.get_caller_identity()["Account"]


def region_for_client(region_arg):
    if region_arg:
        return region_arg
    session = boto3.session.Session()
    reg = session.region_name
    if not reg:
        raise RuntimeError("AWS region not found; pass --region or configure default region")
    return reg


def helm_repo_add(alias, repo_url):
    try:
        run(["helm", "repo", "add", alias, repo_url])
    except subprocess.CalledProcessError:
        # try to update instead
        run(["helm", "repo", "update"])


def helm_pull_chart(alias, chart_name, version, dest):
    # Use helm to pull chart tgz into dest
    run(["helm", "repo", "update"])
    run(["helm", "pull", f"{alias}/{chart_name}", "--version", version, "--destination", str(dest)])
    # find tgz
    for f in Path(dest).glob(f"{chart_name}-*.tgz"):
        return str(f)
    raise FileNotFoundError("chart tgz not found after helm pull")


def helm_registry_login(registry, region):
    # aws ecr get-login-password | helm registry login --username AWS --password-stdin <registry>
    print("Logging into ECR registry for Helm OCI push")
    pw = subprocess.check_output(["aws", "ecr", "get-login-password", "--region", region])
    p = subprocess.Popen(["helm", "registry", "login", registry, "--username", "AWS", "--password-stdin"], stdin=subprocess.PIPE)
    p.communicate(pw)
    if p.returncode != 0:
        raise RuntimeError("helm registry login failed")


def helm_save_and_push(chart_tgz, oci_ref):
    # helm chart save <tgz> oci://registry/repo:tag
    # helm chart push oci://registry/repo:tag
    run(["helm", "chart", "save", chart_tgz, oci_ref])
    run(["helm", "chart", "push", oci_ref])


def mirror(charts_yaml, region_arg=None, profile=None):
    ensure_helm()
    ensure_aws_cli()

    region = region_for_client(region_arg)
    account = aws_account_id()
    registry = f"{account}.dkr.ecr.{region}.amazonaws.com"

    ecr = boto3.client("ecr", region_name=region)

    tmpdir = Path(tempfile.mkdtemp(prefix="helm-mirror-"))
    print("using tempdir", tmpdir)

    try:
        with open(charts_yaml) as fh:
            cfg = yaml.safe_load(fh)
    except Exception as e:
        print("Failed to read charts YAML:", e)
        raise

    charts = cfg.get("charts", [])
    if not charts:
        print("No charts defined in", charts_yaml)
        return

    # Add repos map to alias names
    alias_map = {}

    for idx, ch in enumerate(charts):
        repo_url = ch["repo"]
        chart = ch["chart"]
        version = str(ch.get("version", ""))
        dest_repo = ch.get("dest_repo")
        alias = f"repo{idx}"
        alias_map[repo_url] = alias
        try:
            helm_repo_add(alias, repo_url)
        except Exception:
            print(f"Failed to add repo {repo_url} as {alias}")

        # Pull chart
        try:
            chart_tgz = helm_pull_chart(alias, chart, version, tmpdir)
            print("Downloaded chart to", chart_tgz)
        except Exception as e:
            print(f"Failed to pull chart {chart}@{version} from {repo_url}: {e}")
            continue

        # Ensure ECR repo exists
        if "/" in dest_repo:
            repo_name = dest_repo
        else:
            repo_name = dest_repo
        if not ecr_repo_exists(ecr, repo_name):
            create_ecr_repo(ecr, repo_name)

        # Login
        helm_registry_login(registry, region)

        # Prepare OCI reference
        tag = version if version else "latest"
        oci_ref = f"oci://{registry}/{repo_name}:{tag}"

        # Save & push
        try:
            helm_save_and_push(chart_tgz, oci_ref)
            print(f"Pushed {chart}@{version} -> {oci_ref}")
        except Exception as e:
            print(f"Failed to push chart to {oci_ref}: {e}")
            continue

    shutil.rmtree(tmpdir)
    print("done")


def main():
    parser = argparse.ArgumentParser(description="Mirror Helm charts into ECR as OCI artifacts")
    parser.add_argument("--charts", required=True, help="YAML file listing charts to mirror")
    parser.add_argument("--region", required=False, help="AWS region to use (overrides boto3) )")
    parser.add_argument("--profile", required=False, help="AWS profile name (optional)")

    args = parser.parse_args()

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile

    mirror(args.charts, region_arg=args.region, profile=args.profile)


if __name__ == "__main__":
    main()
