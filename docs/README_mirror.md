# Mirroring Helm charts into ECR (Airgap pre-staging)

This repository contains `scripts/mirror_charts.py` — a standalone Python script
that downloads Helm chart tarballs from upstream Helm chart repositories and
pushes them to AWS ECR as OCI artifacts.

Prerequisites
- Python 3.9+
- `helm` CLI >= 3.11
- `aws` CLI configured or environment credentials for boto3
- Install Python deps for the script:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Usage

```bash
# Mirror charts listed in the default YAML
python3 scripts/mirror_charts.py --charts scripts/charts-to-mirror.yaml --region us-east-1

# Use a specific AWS profile
python3 scripts/mirror_charts.py --charts scripts/charts-to-mirror.yaml --region us-east-1 --profile myprofile
```

Notes
- The script shells out to `helm` for pulling charts and pushing OCI artifacts.
- It will create ECR repositories if they do not exist.
- After the artifacts are in ECR they can be pulled from the air-gapped environment
  (if ECR images are exported or mirrored) or copied to a private registry accessible
  to the airgapped cluster.

Security
- The Slack webhook placeholder in `apps/monitoring/alertmanager/alertmanager-config.yaml`
  must be replaced and encrypted with SOPS before committing production secrets.
