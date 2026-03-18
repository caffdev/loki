# ABOUTME: Top-level readme for the EKS monitoring and logging stack repository.
# ABOUTME: Provides quickstart, layout overview, and common make targets.

# EKS Monitoring & Logging Stack

Kustomize-packaged observability stack for EKS clusters. Deploys Prometheus, Loki, Grafana, Fluent Bit, and Alertmanager.

## Prerequisites

- `kubectl` configured for target cluster
- `kustomize` >= 5.0 (with Helm chart inflation support)
- `helm` >= 3.12
- `sops` for secrets decryption
- AWS CDK CLI + Python 3.11+ (for cloud resources)

## Quick start

```bash
# Render all manifests for staging
make build ENV=staging

# Validate rendered manifests
make validate

# Preview diff against live cluster
make diff ENV=staging

# Apply to cluster
make apply ENV=staging
```

## Repo layout

```
apps/                        # Kustomize bases (one per component)
  monitoring/prometheus/     # kube-prometheus-stack
  monitoring/alertmanager/   # Alertmanager rules + receivers
  grafana/operator/          # Grafana Operator + dashboards
  logging/loki/              # Loki simple-scalable
  logging/collector/         # Fluent Bit DaemonSet
  observability/common/      # Namespaces, RBAC, network policies
clusters/                    # Per-cluster overlays
  eks-staging/
  eks-prod/
cdk/                         # Python CDK constructs (S3, IAM, ECR)
dashboards/                  # Grafana dashboard JSON files
docs/                        # Architecture + planning docs
```

## Make targets

| Target            | Description                                     |
|-------------------|-------------------------------------------------|
| `make build`      | Render all kustomize manifests (`ENV=` required) |
| `make validate`   | Lint rendered manifests with kubeconform          |
| `make diff`       | Diff rendered manifests against live cluster      |
| `make apply`      | Apply manifests to cluster                        |
| `make start`      | Alias for `make apply ENV=staging`                |
| `make stop`       | Delete the monitoring stack from staging          |

## Documentation

- [Architecture](docs/arch.md)
- [Book of work](docs/book-of-work/)
