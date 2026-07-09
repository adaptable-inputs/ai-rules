---
applies_to:
  load: "conditional"
  when: "the project layers domain against infrastructure"
  annex: "CLEAN_ARCHITECTURE.ANNEX.md"
---
# CLEAN_ARCHITECTURE

Guidance for AI agents implementing and reviewing Clean Architecture patterns.

## Scope
- Define dependency-direction and boundary rules for layered architecture.
- Apply this file when designing modules/services and reviewing architectural
  changes.

## Semantic Dependencies
- Inherit core constraints from `ARCHITECTURE/ARCHITECTURE.md`.
- Inherit design principles from `DESIGN/SOLID.md` and
  `DESIGN/CLEAN_CODE.md`.
- Inherit security/testing/logging baselines from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

## Core Rules
- Dependencies point inward toward domain policy.
- Domain and use-case layers MUST NOT depend on frameworks, DB clients, or web
  adapters.
- Outer layers implement interfaces defined by inner layers.
- SHOULD keep business policy independent from delivery and persistence details.

## Layer Responsibilities
- Domain:
  entities, value objects, invariants, and core policy.
- Application/use-case:
  orchestration, transaction boundaries, policy composition.
- Interface adapters:
  controllers, presenters, gateways, mappers.
- Infrastructure:
  DB, message bus, network clients, framework integration.

## Boundary Contracts
- SHOULD define ports/interfaces at policy boundaries.
- SHOULD keep boundary DTOs stable and explicit.
- SHOULD avoid leaking framework-specific annotations/types into domain core.
- SHOULD keep mapping between boundary DTOs and domain models explicit.

## Dependency Injection and Composition
- SHOULD compose concrete dependencies at outermost composition root.
- SHOULD inject abstractions into use cases.
- SHOULD avoid service locators and hidden global singletons in core policy.

## Transaction and Side-Effect Placement
- SHOULD keep side effects in outer layers/gateways.
- SHOULD keep use-case logic deterministic where possible.
- SHOULD keep transaction scope aligned with use-case boundary.
- SHOULD avoid domain-layer calls directly to infrastructure.

## Override Notes
- Framework docs MAY prescribe wiring patterns, but dependency direction and
  boundary-isolation rules in this file remain mandatory.
