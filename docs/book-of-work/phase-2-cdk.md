# ABOUTME: Phase 2 plan — CDK constructs for S3, IAM, and ECR cloud resources.
# ABOUTME: Covers infrastructure needed before deploying the stack to EKS.

# Phase 2 — Cloud Resources (CDK)

## Goal

Deploy AWS resources (S3 bucket for Loki, IAM roles for Pod Identity, ECR repos) using Python CDK constructs.

## Tasks

- [x] Initialize CDK app (`cdk/`)
- [x] Create S3 bucket construct for Loki storage (per-environment)
- [x] Create IAM role constructs for Pod Identity (Loki read/write, Prometheus remote-write if needed)
- [x] Create ECR repository constructs (optional image mirrors)
- [x] Create `.sops.yaml` with KMS key ARN
- [x] Add `make cdk-synth` and `make cdk-deploy` targets
- [ ] Validate CDK output with `cdk diff` (deferred — no AWS access)

## Acceptance criteria

- `cdk synth` produces valid CloudFormation.
- IAM policies follow least-privilege for Loki S3 access.
- S3 bucket has versioning, encryption, and lifecycle rules.

## Dependencies

- Phase 1 complete (repo structure exists).
- AWS account access and KMS key provisioned.
