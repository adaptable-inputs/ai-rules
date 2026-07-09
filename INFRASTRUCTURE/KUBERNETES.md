---
applies_to:
  load: "conditional"
  when: "Kubernetes manifests are present"
  tools: ["kubernetes"]
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

## High-Risk Pitfalls
1. Missing resource requests causing noisy-neighbor instability.
2. Misconfigured probes causing restart loops.
3. Over-privileged service accounts and broad RBAC roles.
4. Mutable image tags causing unpredictable deployments.
5. Secret leakage via plain env/config or logs.
6. Rollout strategy that can drop all replicas.

## Do / Don't Examples
### 1. Resource Governance
```text
Don't: omit resources section.
Do:    define cpu/memory requests and limits per workload.
```

### 2. Image Pinning
```text
Don't: image: my-service:latest
Do:    image: my-service:v1.4.2 (or digest pin)
```

### 3. Probe Semantics
```text
Don't: liveness probe that fails during normal warm-up.
Do:    tune startup/readiness/liveness thresholds to app behavior.
```

## Code Review Checklist for Kubernetes
- Are resources/replicas/probes explicitly configured and sane?
- Is rollout strategy safe for availability goals?
- Are security contexts and RBAC least-privilege?
- Are images pinned and pull policy intentional?
- Are secrets/config separated and safely handled?
- Are observability and failure signals sufficient for operations?

## Testing Guidance
- Validate manifests with schema/policy checks in CI.
- Run server-side dry-run and diff checks before deployment
  (for example `kubectl apply --dry-run=server`, `kubectl diff`).
- Test rollout and rollback behavior in staging.
- Test probe behavior under startup/slow dependency conditions.
- Test autoscaling/resource behavior under representative load.

## Override Notes
- Helm/Istio docs MAY define additional layer-specific constraints, but
  Kubernetes runtime safety and security controls here remain mandatory.
