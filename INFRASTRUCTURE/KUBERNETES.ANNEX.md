---
applies_to:
  load: "annex"
  annex_of: "KUBERNETES.md"
  tasks: ["review", "test"]
---
# KUBERNETES - Annex

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
