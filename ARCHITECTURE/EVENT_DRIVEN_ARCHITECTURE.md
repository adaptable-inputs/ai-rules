---
applies_to:
  load: "conditional"
  when: "the project publishes or consumes events"
  annex: "EVENT_DRIVEN_ARCHITECTURE.ANNEX.md"
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

## Override Notes
- Broker-specific library docs MAY change implementation details, but idempotency,
  compatibility, retry safety, and observability constraints here remain
  mandatory.
