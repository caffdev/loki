# ABOUTME: CDK construct for ECR repositories used by the monitoring stack.
# ABOUTME: Creates repos for custom/mirrored images with lifecycle cleanup rules.
from aws_cdk import (
    aws_ecr as ecr,
    RemovalPolicy,
)
from constructs import Construct


class EcrRepos(Construct):
    """ECR repositories for the monitoring stack container images."""

    REPO_NAMES = [
        "monitoring/fluent-bit-custom",
        "monitoring/grafana-custom",
    ]

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
    ) -> None:
        super().__init__(scope, construct_id)

        is_prod = env_name == "prod"

        self.repositories: dict[str, ecr.Repository] = {}

        for repo_name in self.REPO_NAMES:
            repo = ecr.Repository(
                self,
                repo_name.replace("/", "-"),
                repository_name=f"{repo_name}-{env_name}",
                removal_policy=RemovalPolicy.RETAIN if is_prod else RemovalPolicy.DESTROY,
                empty_on_delete=not is_prod,
                image_scan_on_push=True,
                lifecycle_rules=[
                    ecr.LifecycleRule(
                        description="Keep last 20 tagged images",
                        max_image_count=20,
                        rule_priority=1,
                        tag_status=ecr.TagStatus.ANY,
                    ),
                ],
            )
            self.repositories[repo_name] = repo
