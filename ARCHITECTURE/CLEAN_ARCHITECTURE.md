---
applies_to:
  load: "conditional"
  when: "the project layers domain against infrastructure"
  annex: "CLEAN_ARCHITECTURE.ANNEX.md"
  purpose: "dependency-direction and boundary rules for layered architecture"
  inherits: ["ARCHITECTURE/ARCHITECTURE.md", "DESIGN/SOLID.md", "DESIGN/CLEAN_CODE.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# CLEAN_ARCHITECTURE

Guidance for AI agents implementing and reviewing Clean Architecture patterns.

## Core Rules
- Dependencies point inward toward domain policy.
- Domain and use-case layers MUST NOT depend on frameworks, DB clients, or web adapters.
- Outer layers implement interfaces defined by inner layers.
- SHOULD keep business policy independent from delivery and persistence details.

## Layer Responsibilities
- Domain: entities, value objects, invariants, and core policy.
- Application/use-case: orchestration, transaction boundaries, policy composition.
- Interface adapters: controllers, presenters, gateways, mappers.
- Infrastructure: DB, message bus, network clients, framework integration.

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
