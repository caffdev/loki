ABOUTME: Project-level instructions for AI assistants working on this EKS monitoring stack.
ABOUTME: Covers conventions, stack decisions, repo layout, and tooling for Prometheus/Loki/Grafana on EKS.

# EKS Monitoring Stack — Project Instructions

## Stack decisions (locked)

| Concern           | Choice                                      |
|-------------------|---------------------------------------------|
| Metrics           | kube-prometheus-stack Helm chart             |
| Logs              | Loki (distributed / microservices mode)     |
| Log collector     | Promtail DaemonSet                          |
| Visualization     | Grafana Operator + GrafanaDashboard CRs     |
| Alerts            | AWS Alertmanager   |
| Packaging         | Kustomize wrapping Helm charts              |
| Cloud access      | EKS Pod Identity (not IRSA)                 |
| Cloud resources   | CDK constructs (Python)                     |
| Secrets           | AWS Secret nabager                          |
| Container images  | ECR                                         |
| Node scheduling   | Karpenter node-group selectors              |

## Namespaces

- `monitoring` — Prometheus, Alertmanager, Grafana
- `logging` — Loki, Promtail

## Clusters

Two target clusters: `eks-staging`, `eks-prod`.

## Repo layout

```
apps/
  monitoring/prometheus/     # kube-prometheus-stack kustomize wrapper
  monitoring/alertmanager/   # Alertmanager CR + receivers
  grafana/operator/          # Grafana Operator + dashboard CRs
  logging/loki/              # Loki distributed (microservices)
  logging/collector/         # Promtail DaemonSet
  observability/common/      # namespaces, RBAC, network policies
clusters/
  eks-staging/               # staging overlay
  eks-prod/                  # production overlay
cdk/                         # Python CDK constructs (S3, IAM, ECR)
dashboards/                  # Grafana dashboard JSON sources
docs/                        # arch.md, book-of-work/
```

## Conventions

- Every kustomization.yaml uses `helmCharts` to render upstream charts with a thin values overlay.
- Alerting rules live under `apps/monitoring/alertmanager/rules/` as PrometheusRule CRs.
- Dashboards are stored as JSON in `dashboards/` and referenced by GrafanaDashboard CRs.
- All pods must define resource requests and limits.
- All pods must include Karpenter-compatible `nodeSelector` labels.
- Cluster overlays patch environment-specific values (retention, replicas, ingress hosts).

## Working in this repo

- Architecture detail is in `docs/arch.md`. Update it when design changes.
- Planning and task tracking lives in `docs/book-of-work/`.
- Run `make build` to render all kustomize manifests; `make validate` to lint them.
- Run `make diff ENV=staging` to preview changes against a live cluster.

