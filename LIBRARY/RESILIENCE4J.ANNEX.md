---
applies_to:
  load: "annex"
  annex_of: "RESILIENCE4J.md"
  tasks: ["review", "test"]
---
# RESILIENCE4J - Annex

## High-Risk Pitfalls
1. Retrying non-idempotent operations.
2. Retry + short timeout causing request storms.
3. Fallbacks returning incorrect business outcomes.
4. One shared policy for heterogeneous dependencies.
5. Missing metrics/alerts for policy behavior.
6. Swallowing failures behind broad fallback defaults.

## Do / Don't Examples
### 1. Retry Scope
```text
Don't: retry validation errors or permanent 4xx responses.
Do:    retry transient network/timeouts with bounded attempts.
```

### 2. Fallback Correctness
```text
Don't: return synthetic success on payment failure.
Do:    return explicit degraded/unavailable outcome.
```

### 3. Policy Tuning
```text
Don't: copy same thresholds to every dependency.
Do:    tune per dependency latency/error profile.
```

## Code Review Checklist for Resilience4j
- Does each failure mode map to a named primitive: retry for transient faults, circuit breaker for sustained faults,
  bulkhead for saturation, timeout for latency?
- Are retry policies bounded and idempotency-safe?
- Are fallback paths correctness-preserving?
- Are timeout/circuit/bulkhead/rate policies coordinated?
- Are metrics/logging/alerts sufficient for operation?
- Is policy scope dependency-specific and documented?

## Testing Guidance
- Add failure-injection tests for downstream outages and latency spikes.
- Test retry idempotency safety.
- Test circuit-breaker state transitions.
- Test bulkhead saturation/rejection behavior.
- Test fallback outcomes for correctness.
