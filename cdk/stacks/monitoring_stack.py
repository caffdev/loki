# ABOUTME: CDK stack for monitoring cloud resources (S3, IAM, ECR).
# ABOUTME: Composes per-environment constructs for Loki storage, Pod Identity, and ECR.
import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct

from stacks.constructs.loki_storage import LokiStorage
from stacks.constructs.pod_identity_roles import PodIdentityRoles
from stacks.constructs.ecr_repos import EcrRepos


class MonitoringStack(Stack):
    """Cloud resources for the EKS monitoring and logging stack."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        eks_cluster_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        loki_storage = LokiStorage(self, "LokiStorage", env_name=env_name)

        pod_identity = PodIdentityRoles(
            self,
            "PodIdentityRoles",
            env_name=env_name,
            eks_cluster_name=eks_cluster_name,
            loki_bucket=loki_storage.bucket,
        )

        ecr = EcrRepos(self, "EcrRepos", env_name=env_name)

        # --- Outputs ---
        cdk.CfnOutput(self, "LokiBucketName", value=loki_storage.bucket.bucket_name)
        cdk.CfnOutput(self, "LokiBucketArn", value=loki_storage.bucket.bucket_arn)
        cdk.CfnOutput(self, "LokiRoleArn", value=pod_identity.loki_role.role_arn)
        cdk.CfnOutput(
            self, "PrometheusRoleArn", value=pod_identity.prometheus_role.role_arn
        )
