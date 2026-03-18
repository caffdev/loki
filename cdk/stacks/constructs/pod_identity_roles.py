# ABOUTME: CDK construct for EKS Pod Identity IAM roles.
# ABOUTME: Creates least-privilege roles for Loki (S3 access) and Prometheus (future remote-write).
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_eks as eks,
)
from constructs import Construct


class PodIdentityRoles(Construct):
    """IAM roles for EKS Pod Identity associations."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        eks_cluster_name: str,
        loki_bucket: s3.IBucket,
    ) -> None:
        super().__init__(scope, construct_id)

        # Pod Identity trust policy — pods.eks.amazonaws.com
        pod_identity_principal = iam.ServicePrincipal("pods.eks.amazonaws.com")

        # --- Loki role: read/write to S3 for chunks + index ---
        self.loki_role = iam.Role(
            self,
            "LokiRole",
            role_name=f"loki-pod-identity-{env_name}",
            assumed_by=pod_identity_principal,
            description=f"Pod Identity role granting Loki S3 access in {env_name}",
        )

        loki_bucket.grant_read_write(self.loki_role)

        # Loki also needs s3:ListBucket for existence checks
        loki_bucket.grant_read(self.loki_role)

        # --- Pod Identity association for Loki ---
        eks.CfnPodIdentityAssociation(
            self,
            "LokiPodIdentityAssociation",
            cluster_name=eks_cluster_name,
            namespace="logging",
            service_account="loki",
            role_arn=self.loki_role.role_arn,
        )

        # --- Prometheus role: placeholder for remote-write targets ---
        self.prometheus_role = iam.Role(
            self,
            "PrometheusRole",
            role_name=f"prometheus-pod-identity-{env_name}",
            assumed_by=pod_identity_principal,
            description=f"Pod Identity role for Prometheus in {env_name}",
        )

        # Prometheus may need AMP remote-write permissions in the future.
        # Add grants here when configuring remote_write.

        eks.CfnPodIdentityAssociation(
            self,
            "PrometheusPodIdentityAssociation",
            cluster_name=eks_cluster_name,
            namespace="monitoring",
            service_account="kube-prometheus-stack-prometheus",
            role_arn=self.prometheus_role.role_arn,
        )
