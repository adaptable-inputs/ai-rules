---
applies_to:
  load: "conditional"
  when: "the project separates command and query models"
  annex: "CQRS.ANNEX.md"
  purpose: "rules for separating write behavior (commands) and read behavior (queries) when domain complexity or scale justifies it"
  inherits: ["ARCHITECTURE/ARCHITECTURE.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md", "ARCHITECTURE/EVENT_DRIVEN_ARCHITECTURE.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# CQRS

Guidance for AI agents implementing and reviewing Command Query
Responsibility Segregation (CQRS) architectures.

## CQRS Decision Rules
- SHOULD use CQRS only when command and query concerns have materially different scaling, consistency, or model
  complexity.
- MUST NOT apply CQRS by default for simple CRUD domains.
- SHOULD document why separation is needed before introducing additional moving parts.

## Command-Side Rules
- Commands represent intent to change state and enforce domain invariants.
- SHOULD keep command handlers transactional and explicit about side effects.
- MUST validate authorization and invariants before state mutation.
- MUST ensure command handling is idempotent for retry-prone paths.

## Query-Side Rules
- Queries MUST be read-only and MUST NOT mutate domain state.
- SHOULD optimize read models for consumer needs; do not force write-model shape on read use cases.
- SHOULD keep query contracts explicit and stable.
- SHOULD make staleness expectations explicit when using eventually consistent reads.

## Consistency and Projection Rules
- SHOULD treat eventual consistency as an explicit product contract.
- SHOULD define projection update strategy and recovery behavior (replay/rebuild).
- MUST keep projection handlers idempotent and replay-safe.
- SHOULD track projection lag and expose operational signals for stale reads.

## Reliability and Operability
- SHOULD use correlation IDs to trace command-to-projection flow.
- SHOULD bound retries with a maximum attempt count, then route poison events/messages to a dead-letter destination.
- SHOULD emit structured logs for command execution and projection failures.
- SHOULD alert on sustained projection lag, retry storms, and replay failures.
