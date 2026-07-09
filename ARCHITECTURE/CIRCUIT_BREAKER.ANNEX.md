---
applies_to:
  load: "annex"
  annex_of: "CIRCUIT_BREAKER.md"
  tasks: ["review", "test"]
---
# CIRCUIT_BREAKER - Annex

## High-Risk Pitfalls
1. Circuit breaker applied too broadly, masking healthy dependencies.
2. Misaligned retry + breaker causing traffic amplification.
3. Fallbacks returning incorrect business data.
4. Missing timeout configuration rendering breaker ineffective.
5. No monitoring for open-state duration.
6. Shared breaker instance for unrelated dependencies.

## Do / Don't Examples
### 1. Boundary Placement
```text
Don't: wrap internal pure function with circuit breaker.
Do:    wrap external payment API client boundary.
```

### 2. Fallback Correctness
```text
Don't: on failure, return fabricated "success" response.
Do:    return explicit degraded/unavailable outcome with traceable code.
```

### 3. Retry Coordination
```text
Don't: high retry count + short timeout + tight loop.
Do:    bounded retries with jitter and breaker-aware policy.
```

## Code Review Checklist for Circuit Breakers
- Is breaker applied only to true remote dependency boundaries?
- Are timeout/threshold/window settings explicit and justified?
- Are retries coordinated to avoid amplification?
- Are fallback behaviors correctness-preserving and explicit?
- Are state transitions observable via logs/metrics/alerts?
- Is breaker scope isolated per dependency/domain risk?

## Testing Guidance
- Add tests for open/half-open/closed transitions.
- Add chaos/failure-injection tests for downstream outage behavior.
- Test fallback correctness and user-visible degradation semantics.
- Test retry-breaker interaction under sustained failure.
- Test recovery behavior after dependency returns healthy.
