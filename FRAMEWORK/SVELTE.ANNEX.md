---
applies_to:
  load: "annex"
  annex_of: "SVELTE.md"
  tasks: ["review", "test"]
---
# SVELTE - Annex

## High-Risk Pitfalls
1. Hidden reactive dependency chains causing update surprises.
2. In-place mutations not triggering expected updates.
3. Missing cleanup for subscriptions/timers.
4. Heavy logic embedded directly in template expressions.
5. Non-keyed list rendering causing DOM/state mismatch.
6. Browser API usage without SSR guards.

## Do / Don't Examples
### 1. Shared State
```text
Don't: duplicate same value in multiple local component states.
Do:    keep shared state in a store and derive local projections.
```

### 2. Cleanup
```text
Don't: create interval in onMount without clearInterval on destroy.
Do:    always pair setup with teardown.
```

### 3. List Rendering
```text
Don't: each block without stable key for dynamic lists.
Do:    keyed list rendering with stable identity.
```

## Code Review Checklist for Svelte
- Are component boundaries focused and cohesive?
- Is state ownership clear (local vs shared store)?
- Are reactive dependencies explicit and loop-safe?
- Are side effects lifecycle-safe with cleanup?
- Are templates semantic, accessible, and readable?
- Are list/render performance considerations handled?
- Are SSR/browser boundaries guarded where needed?

## Testing Guidance
- Add unit tests for state/reactive logic.
- Add component tests for key interaction/accessibility behaviors.
- Test lifecycle cleanup behavior (subscriptions/timers/listeners).
- Add integration tests for critical user flows.
- If SSR is used, test browser-guarded paths and hydration behavior.
