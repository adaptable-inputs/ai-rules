---
applies_to:
  load: "annex"
  annex_of: "ISTIO.md"
  tasks: ["review", "test"]
---
# ISTIO - Annex

## High-Risk Pitfalls
1. Overlapping route rules creating nondeterministic behavior.
2. Retry/timeouts misconfiguration causing cascading load.
3. Permissive security policies left in place.
4. Mesh policy drift across namespaces/environments.
5. Canary rollout without objective success/failure gates.
6. Blindly applying global policies to heterogeneous workloads.

## Do / Don't Examples
### 1. Traffic Safety
```text
Don't: global retry policy with high retries and long timeout everywhere.
Do:    per-service tuned retry/timeout aligned with dependency behavior.
```

### 2. Security Policy
```text
Don't: broad allow-all AuthorizationPolicy in production.
Do:    explicit principal/path/method-scoped allow rules.
```

### 3. Rollout Control
```text
Don't: immediate 100% route switch for major backend change.
Do:    weighted canary progression with observability gates.
```

## Code Review Checklist for Istio
- Are traffic rules explicit, non-overlapping, and deterministic?
- Are timeout/retry/circuit policies aligned and bounded?
- Is mTLS/authz policy least-privilege and intentional?
- Is rollout strategy safe and reversible?
- Are telemetry and alerting implications considered?
- Is policy scope targeted to intended workloads only?

## Testing Guidance
- Validate manifest syntax/schema and policy lint in CI.
- Run staged canary tests with rollback drills.
- Test authz and mTLS enforcement paths.
- Test resilience behavior under dependency failure/latency injection.
- Monitor mesh metrics during rollout validation.
