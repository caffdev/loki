# ABOUTME: CDK app entry point for the EKS monitoring stack cloud resources.
# ABOUTME: Instantiates S3, IAM, and ECR constructs for staging and production.
import aws_cdk as cdk

from stacks.monitoring_stack import MonitoringStack

app = cdk.App()

MonitoringStack(
    app,
    "monitoring-staging",
    env_name="staging",
    eks_cluster_name="eks-staging",
    env=cdk.Environment(
        account=app.node.try_get_context("staging_account"),
        region="us-east-1",
    ),
)

MonitoringStack(
    app,
    "monitoring-prod",
    env_name="prod",
    eks_cluster_name="eks-prod",
    env=cdk.Environment(
        account=app.node.try_get_context("prod_account"),
        region="us-east-1",
    ),
)

app.synth()
