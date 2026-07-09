---
applies_to:
  load: "conditional"
  when: "the task involves selecting a design pattern"
  annex: "GOF_DESIGN_PATTERNS.ANNEX.md"
  purpose: "when GoF patterns are useful and when they are overengineering"
  inherits: ["DESIGN/SOLID.md", "DESIGN/CLEAN_CODE.md", "ARCHITECTURE/**"]
---
# GOF_DESIGN_PATTERNS

Guidance for AI agents applying GoF patterns pragmatically.

## Pattern Selection Principles
- SHOULD use patterns to reduce concrete change cost for known change vectors.
- MUST NOT introduce patterns solely for textbook conformity.
- SHOULD keep pattern intent explicit in naming/docs when it aids maintainability.
- SHOULD prefer simpler direct code when variation pressure is low.

## Creational Pattern Guidance
- Factory Method / Abstract Factory: use when object family/instantiation varies by environment/context.
- Builder: use for complex object construction with optional parameters/invariants.
- Singleton: avoid as global state; prefer DI-managed lifecycle.

## Structural Pattern Guidance
- Adapter: isolate incompatible interfaces.
- Facade: simplify interaction with a complex subsystem.
- Decorator: extend behavior without subclass explosion.
- Proxy: control access, lazy loading, remoting, or policy boundaries.

## Behavioral Pattern Guidance
- Strategy: replace branch-heavy algorithm selection.
- Observer: decouple event publishers and subscribers.
- Command: encapsulate actions for queueing, undo, orchestration.
- State: replace state-driven condition pyramids.

## Anti-Pattern Guardrails
- SHOULD avoid speculative pattern layering without real variability pressure.
- SHOULD avoid pattern names as substitutes for clear domain names.
- SHOULD avoid hidden complexity behind facade/proxy without observability.
- SHOULD avoid singleton-as-global-variable design.
