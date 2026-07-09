---
applies_to:
  load: "always"
  annex: "SOLID.ANNEX.md"
  purpose: "practical SOLID usage for maintainable, extensible software design"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "DESIGN/CLEAN_CODE.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md"]
---
# SOLID

Guidance for AI agents applying SOLID principles pragmatically.

## SRP: Single Responsibility Principle
- SHOULD keep modules with one primary reason to change.
- SHOULD separate orchestration, policy, and IO responsibilities.
- SHOULD avoid classes that mix domain logic, persistence, and transport concerns.

## OCP: Open/Closed Principle
- SHOULD design extension seams where change vectors are expected.
- SHOULD prefer composition/polymorphism over branching explosion for variants.
- SHOULD avoid speculative abstractions without credible extension need.

## LSP: Liskov Substitution Principle
- Subtypes MUST honor base type contracts.
- MUST NOT strengthen preconditions or weaken postconditions.
- SHOULD keep behavioral compatibility explicit in inheritance hierarchies.

## ISP: Interface Segregation Principle
- SHOULD prefer narrow interfaces focused on client needs.
- SHOULD avoid large kitchen-sink interfaces.
- SHOULD keep interface methods cohesive and role-specific.

## DIP: Dependency Inversion Principle
- SHOULD depend on abstractions across boundary seams.
- SHOULD keep high-level policy independent from low-level framework details.
- SHOULD compose implementations at outer boundaries.

## Tradeoff Guidance
- SOLID is a decision aid, not a hard quota.
- SHOULD prefer simple direct code when extension pressure is low.
- SHOULD introduce abstraction when it reduces expected change cost.
- MUST document deliberate deviations when pragmatic constraints apply.

## Override Notes
- Framework constraints MAY require pragmatic compromises, but contract
  compatibility and boundary isolation principles remain mandatory.
