---
applies_to:
  load: "index"
---
# ARCHITECTURE

Architecture-layer contract for system design, boundaries, and interaction
patterns.

## Role in the Ruleset
- ARCHITECTURE docs define structural constraints that guide implementation in
  frameworks and libraries.
- Architecture guidance inherits cross-cutting and language baselines and then
  adds system-level design rules.
- Global precedence and override behavior are defined in
  `CORE/RULE_DEPENDENCY_TREE.md`.

## Scope Boundary
ARCHITECTURE includes:
- Service/system boundaries and dependency direction.
- API style and integration pattern constraints.
- Architecture-level performance/resilience and consistency guardrails.

ARCHITECTURE does not include:
- Framework lifecycle/state/rendering details.
- Library API-level coding guidance.
- Build/deploy/runtime infrastructure procedures.

Those belong in `FRAMEWORK/**`, `LIBRARY/**`, `BUILD_TOOLS/**`,
`INFRASTRUCTURE/**`, and `CI-CD/**`.

## Files
- [CLEAN_ARCHITECTURE.md](CLEAN_ARCHITECTURE.md) - Layering and dependency direction guidance.
- [CIRCUIT_BREAKER.md](CIRCUIT_BREAKER.md) - Circuit breaker usage and monitoring.
- [CQRS.md](CQRS.md) - Command/query model separation guidance.
- [EVENT_DRIVEN_ARCHITECTURE.md](EVENT_DRIVEN_ARCHITECTURE.md) - Event-driven systems guidance.
- [GRAPHQL.md](GRAPHQL.md) - GraphQL API design rules.
- [MICROSERVICE.md](MICROSERVICE.md) - Microservice architecture practices.
- [N_PLUS_1.md](N_PLUS_1.md) - Prevent N+1 query patterns.
- [REST.md](REST.md) - REST API design rules.

## Authoring Notes
- Keep this file index-level and boundary-focused.
- Put deep pattern behavior in child architecture docs.
- When adding a new architecture doc, update this index and align semantic
  dependencies in `CORE/RULE_DEPENDENCY_TREE.md`.
