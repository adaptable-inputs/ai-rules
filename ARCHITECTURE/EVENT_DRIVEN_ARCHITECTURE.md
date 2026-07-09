---
applies_to:
  load: "conditional"
  when: "the project publishes or consumes events"
---
# EVENT_DRIVEN_ARCHITECTURE

Guidance for AI agents implementing and reviewing event-driven systems.

## Scope
- Define event-driven architecture constraints for reliability, consistency, and
  operability.
- Apply this file to producers, consumers, and event contract evolution.

## Semantic Dependencies
- Inherit architecture baseline from `ARCHITECTURE/ARCHITECTURE.md` and
  `ARCHITECTURE/CLEAN_ARCHITECTURE.md`.
- Inherit resilience constraints from `ARCHITECTURE/CIRCUIT_BREAKER.md`.
- Inherit cross-cutting constraints from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

## Event Contract Design
- SHOULD model events as facts about completed domain actions.
- SHOULD use stable, domain-driven event names.
- SHOULD keep payloads explicit and minimal; avoid leaking internal persistence shape.
- SHOULD include metadata for tracing and diagnostics (`eventId`, `occurredAt`, `producer`, `correlationId`, `traceId`).
- SHOULD keep contracts versioned and backward-compatible by default.

## Delivery and Processing Semantics
- SHOULD assume at-least-once delivery unless infrastructure guarantees a stronger delivery model.
- MUST make handlers idempotent.
- SHOULD define deduplication strategy for repeated deliveries.
- SHOULD treat ordering guarantees as explicit contracts, not assumptions.
- SHOULD avoid hard dependency on global ordering unless required and documented.

## Reliability Patterns
- SHOULD use retries for transient failures with backoff/jitter.
- SHOULD route poison messages to dead-letter queues/topics.
- SHOULD keep retry limits bounded and observable.
- SHOULD separate business rejection from technical retryable failure.

## Consistency and Workflow Design
- SHOULD use eventual consistency intentionally for cross-boundary workflows.
- SHOULD document consistency expectations and SLA (propagation delays, compensation).
- SHOULD use sagas/compensations for multi-step distributed workflows.
- SHOULD avoid hidden coupling via undocumented event dependencies.

## Security and Governance
- MUST validate event payloads at producer and consumer boundaries.
- MUST NOT include secrets in event payloads.
- MUST enforce producer/consumer access controls per topic/stream.
- SHOULD keep schema registry or equivalent governance controls where available.

## Observability
- SHOULD correlate event flow with `traceId`/`correlationId`.
- SHOULD monitor throughput, lag, retry count, DLQ volume, and processing latency.
- SHOULD log consumer failures with event identity and attempt metadata.
- SHOULD alert on sustained DLQ growth and lag thresholds.

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

## Override Notes
- Broker-specific library docs MAY change implementation details, but idempotency,
  compatibility, retry safety, and observability constraints here remain
  mandatory.
