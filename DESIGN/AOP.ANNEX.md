---
applies_to:
  load: "annex"
  annex_of: "AOP.md"
  tasks: ["review", "test"]
---
# AOP - Annex

## High-Risk Pitfalls
1. Business logic hidden in aspects.
2. Broad pointcuts unintentionally capturing unrelated methods.
3. Undocumented aspect ordering conflicts.
4. Aspects swallowing exceptions and hiding failures.
5. Performance overhead from heavy around-advice on hot paths.
6. Mixed-responsibility methods where desired cross-cutting boundary exists
   only inside method internals (not at method contracts).

## Do / Don't Examples
### 1. Cross-Cutting Classification
```text
Don't: implement domain discount rules in aspect advice.
Do:    keep domain rules in services/use cases; use AOP for cross-cutting policy.
```

### 2. Pointcut Scope
```text
Don't: pointcut matching "all public methods" globally.
Do:    target specific package/annotation boundary.
```

### 3. Error Transparency
```text
Don't: catch and ignore exceptions in advice.
Do:    log/annotate and rethrow or map intentionally.
```

### 4. Clean-Code Boundary Readiness
```text
Don't: keep validation, domain mutation, and notification side effects in one
       method, then expect AOP to target only one inner block.
Do:    split responsibilities into focused methods so pointcuts can bind at
       clear method contracts.
```

## Code Review Checklist for AOP
- Is concern truly cross-cutting and reusable?
- Are pointcuts narrow and intentional?
- Is aspect ordering defined and safe?
- Are side effects/exception semantics explicit?
- Is aspect behavior observable through logs/metrics/tests?
- Is base code organized with cohesive methods so pointcuts can target
  contract-level boundaries cleanly?
- Would explicit composition be clearer than AOP for this case?

## Testing Guidance
- Add focused tests for advice trigger boundaries.
- Add integration tests validating composed aspect behavior/order.
- Test exception paths and ensure failures are not masked.
- Measure performance impact on affected hot paths.
