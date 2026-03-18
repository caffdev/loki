# ABOUTME: Phase 4 plan — build out production-quality dashboards and alerting rules.
# ABOUTME: Covers dashboard JSON authoring, PrometheusRule CRs, and Alertmanager routing.

# Phase 4 — Dashboards & Alerting Rules

## Goal

Create a curated set of Grafana dashboards and Prometheus alerting rules covering cluster health, workload metrics, and log-based alerts.

## Tasks

- [x] Create cluster-overview dashboard (CPU, memory, pod count, node health)
- [x] Create namespace-level dashboard (per-namespace resource usage)
- [x] Create Loki log-explorer dashboard (log volume, error rates by namespace)
- [x] Create alerting-overview dashboard (active alerts, silences)
- [x] Define alerting rules: node health (NotReady, disk pressure, memory pressure)
- [x] Define alerting rules: pod health (CrashLoopBackOff, OOMKilled, high restart count)
- [x] Define alerting rules: Prometheus self-health (scrape failures, WAL corruption)
- [x] Define alerting rules: Loki health (ingestion errors, S3 write failures)
- [x] Configure Alertmanager receivers (Slack — placeholder webhook)
- [ ] Test all alerts in staging with synthetic failures (deferred to Phase 3)

## Acceptance criteria

- All dashboards load without error in Grafana.
- All PrometheusRule CRs are accepted by the Prometheus Operator.
- Alertmanager correctly routes test alerts to configured receivers.

## Dependencies

- Phase 1 complete (repo structure exists).
- Staging testing deferred to Phase 3.
