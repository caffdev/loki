# ABOUTME: Phase 3 plan — deploy the monitoring stack to eks-staging and run smoke tests.
# ABOUTME: Covers first real cluster deployment, validation, and iteration.

# Phase 3 — Staging Deployment & Smoke Tests

## Goal

Deploy the full observability stack to `eks-staging`, verify all components are healthy, confirm log and metric flows end-to-end.

## Tasks

- [ ] Deploy CDK resources to staging account
- [ ] Apply `make apply ENV=staging`
- [ ] Verify Prometheus is scraping kube-state-metrics and node-exporter
- [ ] Verify Alertmanager is reachable and has loaded rules
- [ ] Verify Grafana is accessible and datasources connect
- [ ] Verify Fluent Bit pods are running on all nodes
- [ ] Verify Loki is receiving logs (query via Grafana Explore)
- [ ] Run a test alert and confirm routing
- [ ] Document any values tuning needed

## Acceptance criteria

- All pods in `monitoring` and `logging` namespaces are Running/Ready.
- Grafana shows data from both Prometheus and Loki datasources.
- At least one alert fires and routes correctly.

## Dependencies

- Phase 1 (manifests) and Phase 2 (cloud resources) complete.
- `kubectl` access to `eks-staging`.
