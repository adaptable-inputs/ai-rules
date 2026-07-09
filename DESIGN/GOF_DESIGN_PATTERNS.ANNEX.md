---
applies_to:
  load: "annex"
  annex_of: "GOF_DESIGN_PATTERNS.md"
  tasks: ["review", "test"]
---
# GOF_DESIGN_PATTERNS - Annex

## High-Risk Pitfalls
1. Pattern inflation for simple code paths.
2. Abstract factories with only one implementation forever.
3. Strategy/state abstractions that obscure trivial logic.
4. Observer chains with implicit side effects and poor tracing.
5. Decorator stacks with unclear execution order.

## Do / Don't Examples
### 1. Variation Pressure
```text
Don't: introduce Strategy with one static algorithm and no expected variation.
Do:    keep direct implementation until variation emerges.
```

### 2. Singleton Misuse
```text
Don't: use Singleton for mutable global cache state.
Do:    inject scoped cache service via DI container.
```

### 3. Adapter Boundary
```text
Don't: scatter external API shape conversions across business logic.
Do:    isolate conversion in dedicated Adapter.
```

## Code Review Checklist for GoF Pattern Use
- Is there a clear change vector justifying this pattern?
- Does pattern use reduce complexity or increase it?
- Are responsibilities and boundaries clearer after applying the pattern?
- Are side effects and execution order observable/testable?
- Are simpler alternatives inferior for this context?

## Testing Guidance
- Add contract tests for pattern interfaces/strategies.
- Add behavioral tests for state transitions and decorator/proxy composition.
- Add integration tests around adapter/facade boundary assumptions.
- Add regression tests when refactoring branch logic into patterns.
