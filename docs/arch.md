# ABOUTME: Architecture document for the EKS monitoring and logging stack.
# ABOUTME: Covers component design, data flows, security, and operational considerations.

# Architecture — EKS Monitoring Stack

## Overview

This repo provisions a complete observability stack for two EKS clusters (`eks-staging`, `eks-prod`) using Kustomize-wrapped Helm charts, deployed via GitOps.

```
┌─────────────────────────────────────────────────────────────┐
│  EKS Cluster                                                │
│                                                             │
│  ┌──────────── monitoring namespace ──────────────────────┐ │
│  │  Prometheus  ←── ServiceMonitors                       │ │
│  │  Alertmanager ←── PrometheusRules                      │ │
│  │  Grafana (Operator) ←── GrafanaDashboard CRs           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────── logging namespace ─────────────────────────┐ │
│  │  Fluent Bit (DaemonSet) ──→ Loki (simple-scalable)     │ │
│  │                                  │                      │ │
│  │                                  ▼                      │ │
│  │                              S3 (chunks)                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Metrics — kube-prometheus-stack

- Deploys Prometheus Operator, Prometheus, Alertmanager, node-exporter, kube-state-metrics, and default Grafana dashboards.
- Application teams add `ServiceMonitor` CRs to scrape their workloads.
- Alerting rules stored as `PrometheusRule` CRs in `apps/monitoring/alertmanager/rules/`.

### Visualization — Grafana Operator

- Grafana is deployed and managed by the Grafana Operator.
- Dashboards are stored as JSON in `dashboards/` and wrapped as `GrafanaDashboard` CRs.
- Datasources (Prometheus, Loki) are created via `GrafanaDatasource` CRs.

### Logs — Loki (simple-scalable)

- Loki runs in simple-scalable mode (read, write, backend).
- Long-term chunk and index storage in S3.
- Pod Identity grants Loki write/read access to the S3 bucket.

### Log collection — Fluent Bit

- Runs as a DaemonSet on every node.
- Collects container stdout/stderr from `/var/log/containers/`.
- Enriches with Kubernetes metadata (namespace, pod, container, labels).
- Forwards to Loki's HTTP push endpoint.

### Alertmanager

- Bundled with kube-prometheus-stack.
- Routes and receivers (Slack, PagerDuty, etc.) configured via Helm values.
- Silence and inhibition rules for maintenance windows.

## Cloud resources (CDK — Python)

| Resource    | Purpose                                   |
|-------------|-------------------------------------------|
| S3 bucket   | Loki chunk + index storage                |
| IAM roles   | Pod Identity roles for Loki, Prometheus   |
| ECR repos   | Container image mirrors (if needed)       |

## Packaging

Each component is a Kustomize base under `apps/`. The `kustomization.yaml` uses `helmCharts` to inflate the upstream Helm chart with a thin `values.yaml`. Cluster overlays under `clusters/eks-staging/` and `clusters/eks-prod/` patch environment-specific values (replicas, retention, ingress hosts).

## Security considerations

- **Secrets**: Encrypted with SOPS. `.sops.yaml` at repo root configures KMS key.
- **Grafana auth**: OIDC/SSO via Helm values.
- **Network policies**: Restrict inter-namespace and egress traffic.
- **Pod Identity**: No long-lived credentials — IAM roles assumed at pod level.
- **Ingress**: TLS-terminated ingress for Grafana and Alertmanager.

## Operational checklist

- Prometheus local storage is ephemeral — plan Thanos or remote_write for long-term retention.
- Monitor the observability stack itself (operator health, restart counts).
- Define log retention policies and scrape-interval budgets to manage cost.
- Use `make build` / `make validate` in CI to catch misconfigurations before merge.
- VPC endpoints for S3 reduce egress cost and latency.
