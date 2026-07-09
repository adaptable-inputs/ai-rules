---
applies_to:
  load: "annex"
  annex_of: "TAILWIND_CSS.md"
  tasks: ["review", "test"]
---
# TAILWIND_CSS - Annex

## High-Risk Pitfalls
1. Utility sprawl making components unreadable.
2. Arbitrary value overuse bypassing design system.
3. Dynamic class name generation breaking purge/content extraction.
4. Missing focus/contrast accessibility states.
5. Excessive responsive/state variants causing style bloat.
6. Duplicated style patterns across components with no abstraction.

## Do / Don't Examples
### 1. Reuse
```text
Don't: copy/paste same 20 utility classes in many files.
Do:    extract shared component or utility composition.
```

### 2. Arbitrary Values
```text
Don't: w-[317px] text-[#4a6dff] everywhere.
Do:    use theme tokens and approved spacing/size scales.
```

### 3. Dynamic Classes
```text
Don't: className={`text-${color}-600`}
Do:    map known variants to explicit class strings.
```

## Code Review Checklist for Tailwind
- Are class lists readable and grouped by concern?
- Are design tokens used instead of arbitrary values?
- Is every utility pattern repeated three or more times extracted into a
  component or an `@apply` rule?
- Are dynamic classes purge-safe and explicit?
- Are accessibility states (focus/contrast/disabled/error) present?
- Is generated CSS size and variant usage controlled?

## Testing Guidance
- Add visual regression tests for shared components.
- Add accessibility checks for color contrast and focus states.
- Test responsive variants at key breakpoints.
- Validate production build output to ensure unused class purge works.
