---
applies_to:
  load: "annex"
  annex_of: "PRIMEFACES.md"
  tasks: ["review", "test"]
---
# PRIMEFACES - Annex

## High-Risk Pitfalls
1. Business logic embedded in backing beans/view code.
2. Overly broad session scope causing memory bloat/stale state.
3. Unbounded ajax updates degrading performance.
4. Component tree complexity causing render latency.
5. UI-only authorization checks without backend enforcement.
6. Hidden state carrying sensitive information.

## Do / Don't Examples
### 1. Scope Selection
```text
Don't: store per-request form state in session scope.
Do:    use view/request scope according to interaction lifetime.
```

### 2. Ajax Update Targeting
```text
Don't: update="@all" for simple field interaction.
Do:    update only impacted region/component IDs.
```

### 3. Layering
```text
Don't: perform repository operations directly in backing bean action methods.
Do:    delegate to service/use-case layer.
```

## Code Review Checklist for PrimeFaces
- Are view/backing-bean responsibilities cleanly separated from business logic?
- Is bean scope minimal and intentional?
- Are Ajax process/update targets narrow and explicit?
- Are validation and conversion paths consistent and user-actionable?
- Is component tree complexity controlled?
- Are security checks enforced on backend boundaries?

## Testing Guidance
- Add integration/UI tests for critical user workflows.
- Test validation and conversion failure behavior.
- Test scope/lifecycle-sensitive behavior (view refresh/navigation/session).
- Test Ajax partial updates for correct UI state transitions.
- Add performance checks for heavy pages/components where needed.
