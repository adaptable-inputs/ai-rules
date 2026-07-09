---
applies_to:
  load: "annex"
  annex_of: "KAFKA.md"
  tasks: ["review", "test"]
---
# KAFKA - Annex

## High-Risk Pitfalls
1. Non-idempotent consumers producing duplicate side effects.
2. Incompatible schema changes breaking downstream consumers.
3. Missing key strategy causing hot partitions/order issues.
4. Infinite retries with no DLQ path.
5. Silent producer send failure handling.
6. Weak observability of lag and failure metrics.

## Do / Don't Examples
### 1. Idempotency
```text
Don't: process event twice with duplicate side effects.
Do:    detect duplicate eventId and short-circuit safely.
```

### 2. Schema Evolution
```text
Don't: remove field consumers still use.
Do:    additive changes + deprecation window.
```

### 3. Failure Handling
```text
Don't: retry forever on non-recoverable payload.
Do:    send to DLQ with reason metadata.
```

## Code Review Checklist for Kafka
- Is topic/schema ownership and versioning clear?
- Are producer settings aligned with durability/idempotency needs?
- Are consumers idempotent with safe commit/retry strategy?
- Is DLQ/error handling explicit and bounded?
- Are observability metrics/logs sufficient for operations?
- Are partition/key choices aligned with ordering and scale goals?

## Testing Guidance
- Add integration tests with test Kafka for producer/consumer paths.
- Add schema compatibility tests.
- Add duplicate/retry/DLQ behavior tests.
- Add load/lag tests for throughput-sensitive consumers.
