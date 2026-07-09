---
applies_to:
  load: "conditional"
  when: "Kubernetes manifests are present"
  tools: ["kubernetes"]
  annex: "KUBERNETES.ANNEX.md"
---
# KUBERNETES

Guidance for AI agents implementing and reviewing Kubernetes manifests.

## Scope
- Define Kubernetes workload, deployment, and runtime safety defaults.
- Apply this file to manifests, controllers, and cluster deployment reviews.

## Semantic Dependencies
- Inherit container baseline from `INFRASTRUCTURE/DOCKER.md`.
- Inherit YAML safety rules from `LANGUAGE/YAML/YAML.md`.
- Inherit security constraints from `SECURITY/SECURITY.md`.

## Defaults
- SHOULD define `requests` and `limits` for CPU/memory explicitly.
- SHOULD configure `readinessProbe` and `livenessProbe` meaningfully.
- MUST keep deployments declarative and idempotent.
- SHOULD keep labels/annotations consistent and queryable.
- SHOULD use namespaces and RBAC intentionally.

## Workload and Rollout Rules
- SHOULD prefer rolling updates with controlled surge/unavailable values.
- SHOULD keep replica counts and autoscaling policy explicit.
- SHOULD avoid mutable image tags (`latest`) in production.
- SHOULD use `PodDisruptionBudget` for critical services.
- SHOULD keep rollout/rollback strategy documented for critical apps.

## Security Baseline
- SHOULD run containers as non-root where possible.
- MUST use explicit `securityContext` fields (`runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation`,
  `capabilities`, `seccompProfile`) as applicable.
- MUST set safe values intentionally (for example `allowPrivilegeEscalation: false`, drop unnecessary capabilities).
- MUST apply least privilege RBAC for service accounts.
- MUST keep secrets in dedicated secret resources, not plain config maps.
- SHOULD restrict network reachability with network policies where applicable.

## Configuration and Secrets
- SHOULD separate config by environment with controlled overlays.
- MUST keep config maps/secrets versioned and auditable.
- SHOULD avoid coupling runtime behavior to undocumented env vars.

## Observability and Operations
- SHOULD expose metrics/logging in a platform-compatible way.
- SHOULD track pod restarts, crash loops, and probe failures.
- SHOULD monitor resource saturation and eviction risk.
- SHOULD keep alerting tied to service SLO indicators.

## Override Notes
- Helm/Istio docs MAY define additional layer-specific constraints, but
  Kubernetes runtime safety and security controls here remain mandatory.
