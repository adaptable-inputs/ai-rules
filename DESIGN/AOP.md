---
applies_to:
  load: "conditional"
  when: "the project applies aspect-oriented cross-cutting concerns"
  annex: "AOP.ANNEX.md"
  purpose: "when AOP is appropriate for cross-cutting concerns"
  inherits: ["DESIGN/CLEAN_CODE.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md", "SECURITY/SECURITY.md", "CORE/LOGGING.md", "TEST/TEST.md"]
---
# AOP

Guidance for AI agents applying Aspect-Oriented Programming responsibly.

## Appropriate AOP Use Cases
- Logging/tracing instrumentation.
- Metrics/timing instrumentation.
- Security checks and policy enforcement wrappers.
- Transaction boundaries.
- Retry/circuit-breaker wrappers.

## Boundaries and Guardrails
- SHOULD keep domain business rules out of aspects.
- SHOULD keep method responsibilities cohesive ("do one thing") so join points remain explicit at method boundaries.
- SHOULD keep pointcuts narrow, explicit, and auditable.
- SHOULD keep aspect ordering deterministic when multiple aspects apply.
- SHOULD keep side effects observable and documented.
- SHOULD avoid hidden control-flow changes that surprise maintainers.

## Aspect Design Rules
- SHOULD keep advice logic small and focused.
- SHOULD keep cross-cutting seams at clear method contracts; avoid embedding multiple unrelated concerns inside one
  large method body.
- SHOULD avoid mutating method arguments/results unless explicitly intended.
- SHOULD preserve exception semantics unless mapping is deliberate.
- SHOULD keep aspect configuration centralized and discoverable.
