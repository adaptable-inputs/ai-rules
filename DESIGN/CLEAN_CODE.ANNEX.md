---
applies_to:
  load: "annex"
  annex_of: "CLEAN_CODE.md"
  tasks: ["review", "test"]
---
# CLEAN_CODE - Annex

## High-Risk Pitfalls
1. Clever compact code that hides intent.
2. God classes/functions with mixed responsibilities.
3. Catch-all exception handling with no context.
4. Premature abstraction increasing complexity.
5. Naming drift across module boundaries.
6. Refactors without regression safety tests.

## Do / Don't Examples
### 1. Function Cohesion
```text
Don't: one function validates, persists, sends email, and logs analytics.
Do:    separate orchestration from focused operations.
```

### 2. Error Context
```text
Don't: throw a generic error with no context ("failed").
Do:    throw domain-specific error with contextual identifiers.
```

### 3. Duplication Strategy
```text
Don't: abstract two near-identical lines into complex helper prematurely.
Do:    wait for stable repeated pattern, then extract meaningfully.
```

## Code Review Checklist for Clean Code
- Is intent clear without decoding implementation details?
- Are responsibilities cohesive at function/class/module levels?
- Are names domain-meaningful and consistent?
- Are error paths explicit and actionable?
- Is abstraction level justified by real reuse/change patterns?
- Are side effects and dependencies explicit?

## Testing Guidance
- Add regression tests before significant refactors.
- Keep tests aligned to behavior contracts, not incidental structure.
- Add tests for error/edge paths introduced by cleanup changes.
- Ensure refactors keep existing behavior stable unless intentionally changed.
