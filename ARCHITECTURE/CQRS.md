---
applies_to:
  load: "conditional"
  when: "the project separates command and query models"
  annex: "CQRS.ANNEX.md"
---
# CQRS

Guidance for AI agents implementing and reviewing Command Query
Responsibility Segregation (CQRS) architectures.

## Scope
- Define rules for separating write behavior (commands) and read behavior
  (queries) when domain complexity or scale justifies it.
- Apply this file when introducing or reviewing CQRS-style service/module
  boundaries.

## Semantic Dependencies
- Inherit architecture baseline from `ARCHITECTURE/ARCHITECTURE.md` and
  `ARCHITECTURE/CLEAN_ARCHITECTURE.md`.
- Inherit event integration constraints from
  `ARCHITECTURE/EVENT_DRIVEN_ARCHITECTURE.md` when projections are event-fed.
- Inherit cross-cutting constraints from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

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

## Override Notes
- Framework/library docs MAY define CQRS implementation mechanics, but command/
  query separation, consistency contracts, and operability constraints in this
  file remain mandatory.
