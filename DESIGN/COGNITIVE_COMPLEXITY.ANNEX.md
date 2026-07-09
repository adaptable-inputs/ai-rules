---
applies_to:
  load: "annex"
  annex_of: "COGNITIVE_COMPLEXITY.md"
  tasks: ["review", "test"]
---
# COGNITIVE_COMPLEXITY - Annex

## High-Risk Pitfalls
1. Treating metric thresholds as optional suggestions for new code.
2. Splitting methods mechanically without improving cohesion or naming.
3. Hiding complexity in boolean flags and multi-branch parameter behavior.
4. Ignoring legacy hot spots with complexity > 20 and no follow-up plan.
5. Claiming "tool unavailable" without providing a reasoned estimate.

## Do / Don't Examples
### 1. New Method Gate
```text
Don't: introduce a new method with cognitive complexity 24 and merge "as is".
Do:    refactor before merge until the method is <= 15.
```

### 2. Legacy Touch Rule
```text
Don't: modify a legacy method from 19 to 27 without mitigation.
Do:    reduce complexity during the change, or file a follow-up issue if > 20 remains.
```

### 3. Measurement Transparency
```text
Don't: state "complexity looks fine" without evidence.
Do:    attach Sonar/plugin metric or a documented estimate rationale.
```

## Code Review Checklist for Cognitive Complexity
- Do new methods stay at or below complexity 15?
- For altered existing methods, was complexity reduced or kept within target?
- If any altered method remains above 20, is there a linked follow-up issue?
- Is complexity evidence included (Sonar/plugin/estimate)?
- Were nested branches flattened with early returns where it improves clarity?
- Did refactoring improve readability/cohesion instead of only moving branches?

## Testing Guidance
- Add or update regression tests before major method decomposition.
- Validate behavior equivalence after complexity-reduction refactors.
- Add focused tests for extracted branches/decision paths.
- For deferred complexity reductions, capture risk and test focus in the follow-up issue/PR notes.
