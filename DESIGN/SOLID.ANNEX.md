---
applies_to:
  load: "annex"
  annex_of: "SOLID.md"
  tasks: ["review", "test"]
---
# SOLID - Annex

## High-Risk Pitfalls
1. Over-abstraction from dogmatic SOLID application.
2. Huge interface hierarchies with little value.
3. Inheritance hierarchies violating substitutability.
4. Dependency inversion applied superficially while leaking concrete types.
5. SRP ignored in service/controller "god objects".

## Do / Don't Examples
### 1. SRP
```text
Don't: one class validates input, persists data, and sends notifications.
Do:    separate responsibilities into focused collaborators.
```

### 2. OCP
```text
Don't: giant if/else for every new payment type.
Do:    strategy interface with pluggable implementations.
```

### 3. ISP
```text
Don't: Repository interface with unrelated read/write/admin methods.
Do:    split read and write interfaces by client need.
```

## Code Review Checklist for SOLID
- Does each module have a clear reason to change?
- Are extension points aligned with actual change vectors?
- Are subtype contracts behaviorally compatible?
- Are interfaces client-focused and minimal?
- Are high-level modules isolated from low-level details?
- Is abstraction level proportional to complexity?

## Testing Guidance
- Add contract tests for polymorphic interfaces/subtypes.
- Add focused unit tests for strategy implementations.
- Add architecture tests to enforce dependency direction.
- Add regression tests when refactoring responsibilities/interfaces.
