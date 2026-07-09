---
applies_to:
  load: "annex"
  annex_of: "CQRS.md"
  tasks: ["review", "test"]
---
# CQRS - Annex

## High-Risk Pitfalls
1. Adopting CQRS without concrete scaling/complexity need.
2. Command handlers bypassing invariants for convenience.
3. Query handlers mutating state or triggering hidden side effects.
4. Undocumented eventual consistency leading to UX/data confusion.
5. Non-idempotent projection handlers causing duplicate read-state effects.
6. Missing replay/rebuild plan for corrupted read models.
7. No observability for lag and projection failure modes.

## Do / Don't Examples
### 1. Read/Write Separation
```text
Don't: one handler both updates payment status and returns dashboard data.
Do:    command handler updates state; separate query endpoint serves dashboard.
```

### 2. Consistency Contract
```text
Don't: claim immediate consistency when read model is async projected.
Do:    document eventual consistency and expose "lastUpdatedAt"/lag indicators.
```

### 3. Projection Idempotency
```text
Don't: increment counters on every duplicate event delivery.
Do:    dedupe by eventId/version and apply projection updates once.
```

## Code Review Checklist for CQRS
- Is CQRS justified with concrete domain/scaling reasons?
- Are command and query responsibilities strictly separated?
- Do command handlers enforce invariants and idempotency?
- Are query models optimized for reads without write-model leakage?
- Is consistency model explicit and user-visible where needed?
- Are projection/replay failure modes handled and observable?
- Are security constraints enforced on both command and query boundaries?

## Testing Guidance
- Add command-side tests for invariants, authorization, and idempotency.
- Add query-side tests for read-model shape and staleness behavior.
- Add projection tests for duplicate events and replay/rebuild flows.
- Add integration tests for command-to-read propagation paths.
- Add operational tests/alerts for lag thresholds and failure recovery.
