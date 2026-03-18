# ABOUTME: Phase 1 plan — repo scaffold, kustomize bases, cluster overlays, Makefile.
# ABOUTME: Covers everything needed before any cluster deployment.

# Phase 1 — Repo Scaffold & Foundations

## Goal

Produce a fully-rendered, lint-clean set of Kustomize manifests for all stack components, with staging and prod overlays, a Makefile, and CI-ready validation.

## Tasks

- [x] Initialize git repo, branch, hooks
- [x] Audit and rewrite CLAUDE.md
- [x] Create docs/arch.md
- [x] Create readme.md
- [x] Create book-of-work structure
- [x] Scaffold directory layout
- [x] Implement apps/observability/common (namespaces, RBAC, network policies)
- [x] Implement apps/monitoring/prometheus (kube-prometheus-stack kustomize wrapper)
- [x] Implement apps/monitoring/alertmanager (rules directory, example rule)
- [x] Implement apps/logging/loki (Loki simple-scalable kustomize wrapper)
- [x] Implement apps/logging/collector (Fluent Bit DaemonSet kustomize wrapper)
- [x] Implement apps/grafana/operator (Grafana Operator + datasource CRs)
- [x] Create clusters/eks-staging overlay
- [x] Create clusters/eks-prod overlay
- [x] Create Makefile (build, validate, diff, apply, start, stop)
- [x] Create placeholder dashboard JSON

## Acceptance criteria

- `make build ENV=staging` renders all manifests without error.
- `make build ENV=prod` renders all manifests without error.
- All rendered YAML passes kubeconform (when available).
- Each kustomize base builds independently.

## Dependencies

None — this is the first phase.
