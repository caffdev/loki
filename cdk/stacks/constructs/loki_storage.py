# ABOUTME: CDK construct for the Loki S3 storage bucket.
# ABOUTME: Creates a versioned, encrypted bucket with lifecycle rules and access logging.
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class LokiStorage(Construct):
    """S3 bucket for Loki chunk and index storage."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
    ) -> None:
        super().__init__(scope, construct_id)

        is_prod = env_name == "prod"

        self.bucket = s3.Bucket(
            self,
            "LokiChunksBucket",
            bucket_name=f"loki-chunks-{env_name}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN if is_prod else RemovalPolicy.DESTROY,
            auto_delete_objects=not is_prod,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="expire-old-chunks",
                    expiration=Duration.days(90 if is_prod else 30),
                    noncurrent_version_expiration=Duration.days(7),
                ),
                s3.LifecycleRule(
                    id="abort-incomplete-uploads",
                    abort_incomplete_multipart_upload_after=Duration.days(1),
                ),
            ],
            intelligent_tiering_configurations=[
                s3.IntelligentTieringConfiguration(
                    name="loki-tiering",
                    archive_access_tier_time=Duration.days(90) if is_prod else None,
                ),
            ]
            if is_prod
            else None,
        )
