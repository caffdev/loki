# ABOUTME: Phase 5 plan — production rollout of the monitoring stack to eks-prod.
# ABOUTME: Covers pre-flight checks, deployment, validation, and handoff.

# Phase 5 — Production Rollout

## Goal

Deploy the validated observability stack to `eks-prod` with production-grade resource sizing, retention policies, and alerting routes.

## Tasks

- [ ] Deploy CDK resources to prod account
- [ ] Review and finalize prod overlay values (replicas, retention, resource limits)
- [ ] Apply `make apply ENV=prod`
- [ ] Verify all components healthy (same checks as Phase 3)
- [ ] Verify Alertmanager production receivers are connected
- [ ] Verify Grafana SSO/OIDC authentication works
- [ ] Run capacity estimation (Prometheus TSDB size, Loki ingest rate)
- [ ] Set up Prometheus remote_write or Thanos for long-term retention (if needed)
- [ ] Document runbook for common operational tasks
- [ ] Hand off to on-call team

## Acceptance criteria

- All pods healthy in production.
- Dashboards display real production data.
- Alerts fire and reach production on-call channel.
- Runbook published and reviewed by team.

## Dependencies

- Phases 1–4 complete.
- Production cluster access and change-management approval.
