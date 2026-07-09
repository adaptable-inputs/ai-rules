---
applies_to:
  load: "conditional"
  when: "a Kafka client is a declared dependency"
  libraries: ["kafka"]
  annex: "KAFKA.ANNEX.md"
  purpose: "topic, producer, and consumer design constraints for reliable event streaming"
  inherits: ["ARCHITECTURE/EVENT_DRIVEN_ARCHITECTURE.md", "SECURITY/SECURITY.md", "CORE/LOGGING.md"]
---
# KAFKA

Guidance for AI agents implementing and reviewing Apache Kafka usage.

## Defaults
- SHOULD use clear domain-based topic naming and ownership.
- SHOULD keep schema evolution backward-compatible by default.
- SHOULD design consumers for at-least-once delivery semantics.
- SHOULD keep producer/consumer configs explicit and version-controlled.

## Topic and Schema Rules
- SHOULD keep topic partitioning strategy aligned with throughput/order requirements.
- SHOULD keep retention/compaction policy intentional.
- SHOULD use schema registry/contract governance where available.
- SHOULD avoid leaking internal model churn into public event contracts.

## Producer Rules
- SHOULD keep key strategy intentional for partition affinity/order semantics.
- MUST enable idempotent producer settings (`enable.idempotence` with compatible `acks`/retry configuration) where
  retry-duplicate suppression is required.
- SHOULD treat producer idempotence as a producer-session guarantee only; handle end-to-end deduplication/idempotency at
  consumer/workflow boundaries.
- SHOULD handle send failures with clear retry/error policy.
- SHOULD avoid fire-and-forget publishing without observability.

## Consumer Rules
- MUST keep handlers idempotent and retry-safe.
- SHOULD distinguish transient vs permanent processing failures.
- SHOULD route poison messages to DLQ with context.
- SHOULD keep offset commit strategy aligned with processing semantics.

## Observability and Operations
- SHOULD monitor lag, throughput, retry rates, and DLQ volume.
- SHOULD track rebalance frequency and consumer health.
- SHOULD log processing failures with topic/partition/offset context.
- SHOULD alert on sustained lag and retry storms.
