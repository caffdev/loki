# ABOUTME: Master book-of-work index for the EKS monitoring stack project.
# ABOUTME: Links to phase plans and tracks overall progress.

# Book of Work — EKS Monitoring Stack

## Phases

| Phase | Name                        | Status    | Plan file                          |
|-------|-----------------------------|-----------|------------------------------------|
| 1     | Repo scaffold & foundations | Complete  | [phase-1-scaffold.md](phase-1-scaffold.md) |
| 2     | Cloud resources (CDK)       | Complete  | [phase-2-cdk.md](phase-2-cdk.md)           |
| 3     | Staging deployment & smoke  | Blocked   | [phase-3-staging.md](phase-3-staging.md)   |
| 4     | Dashboards & alerting rules | Complete  | [phase-4-dashboards.md](phase-4-dashboards.md) |
| 5     | Production rollout          | Not started | [phase-5-prod.md](phase-5-prod.md)         |

## Principles

- Each phase is independently shippable.
- Phase N+1 does not start until Phase N is validated.
- Every component gets a kustomize build + kubeconform check before merge.
