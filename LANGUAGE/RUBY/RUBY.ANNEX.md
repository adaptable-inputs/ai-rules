---
applies_to:
  load: "annex"
  annex_of: "RUBY.md"
  tasks: ["review", "test"]
---
# RUBY - Annex

## High-Risk Pitfalls
1. Overuse of metaprogramming that obscures behavior contracts.
2. Broad `rescue` blocks that hide production failures.
3. Implicit mutable global/singleton state causing order-dependent bugs.
4. Framework-coupled domain logic reducing testability.
5. Missing timeout/retry boundaries for external dependencies.
6. Unvalidated input reaching domain/persistence layers.
7. Excessive gem additions with weak maintenance posture.

## Do / Don't Examples
### 1. Exception Scope
```text
Don't: rescue StandardError broadly and continue silently.
Do:    rescue specific exceptions and preserve context.
```

### 2. Metaprogramming
```text
Don't: use dynamic magic for core business rules by default.
Do:    prefer explicit methods when behavior clarity matters.
```

### 3. Side Effects
```text
Don't: scatter external IO side effects through domain objects.
Do:    isolate IO at clear service/adapter boundaries.
```

## Code Review Checklist for Ruby
- Are object/module responsibilities cohesive and clear?
- Are exception boundaries specific and non-silent?
- Are side effects and mutable state explicit and bounded?
- Are external dependency calls bounded by timeout/retry strategy?
- Are boundary validations present for external inputs?
- Are new gems justified, maintained, and compliant?

## Testing Guidance
- Test boundary validation and normalization behavior.
- Test exception mapping and failure-path outcomes.
- Test timeout/retry behavior for external dependencies.
- Test state/transaction boundaries for consistency guarantees.
- Add regression tests for previously observed bug classes.
