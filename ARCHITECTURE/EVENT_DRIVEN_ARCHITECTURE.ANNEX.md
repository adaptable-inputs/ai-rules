---
applies_to:
  load: "annex"
  annex_of: "EVENT_DRIVEN_ARCHITECTURE.md"
  tasks: ["review", "test"]
---
# EVENT_DRIVEN_ARCHITECTURE - Annex

## High-Risk Pitfalls
1. Non-idempotent consumers producing duplicate side effects.
2. Breaking payload changes without compatibility strategy.
3. Infinite retry loops with no DLQ escape.
4. Assuming ordering guarantees not provided by broker topology.
5. Hidden synchronous dependencies in supposedly async flow.
6. Missing lag/DLQ monitoring until production incidents occur.
7. Sensitive data leakage in event payloads.

## Do / Don't Examples
### 1. Idempotency
```text
Don't: apply payment on every delivery without dedupe check.
Do:    track processed eventId and short-circuit duplicates.
```

### 2. Version Evolution
```text
Don't: remove payload field consumed by old consumers immediately.
Do:    introduce additive field, deprecate old field, migrate consumers.
```

### 3. Retry/DLQ
```text
Don't: retry forever on non-recoverable validation failure.
Do:    send invalid message to DLQ with failure reason metadata.
```

## Code Review Checklist for Event-Driven Systems
- Are event contracts domain-oriented, explicit, and version-safe?
- Are handlers idempotent under duplicate delivery?
- Are retry and DLQ policies explicit and bounded?
- Are ordering assumptions documented and valid?
- Is consistency model explicit (eventual vs immediate guarantees)?
- Are payload validation and access controls enforced?
- Are observability signals sufficient for operations?

## Testing Guidance
- Add contract tests for event schema compatibility.
- Add idempotency tests with duplicate deliveries.
- Add retry/DLQ behavior tests for transient and permanent failures.
- Add integration tests for end-to-end event flow and eventual consistency.
- Add load/lag tests for throughput-sensitive consumers.
