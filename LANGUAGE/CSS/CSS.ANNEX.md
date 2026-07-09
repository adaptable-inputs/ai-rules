---
applies_to:
  load: "annex"
  annex_of: "CSS.md"
  tasks: ["review", "test"]
---
# CSS - Annex

## High-Risk Pitfalls
1. Specificity wars requiring escalating selectors or `!important`.
2. Hard-coded colors/sizes bypassing design token system.
3. Global selectors unintentionally overriding unrelated components.
4. Removing focus outlines without accessible replacement.
5. Deep nested selectors tightly coupled to DOM structure.
6. Animations causing motion/accessibility issues.

## Do / Don't Examples
### 1. Specificity
```css
/* Don't: deep chained selector */
.page .content .card .header .title { font-size: 1.2rem; }

/* Do: component class selector */
.card-title { font-size: 1.2rem; }
```

### 2. Token Usage
```css
/* Don't: hard-coded palette */
.button-primary { background: #3a62ff; color: #ffffff; }

/* Do: design token usage */
.button-primary {
  background: var(--color-primary);
  color: var(--color-on-primary);
}
```

### 3. Focus Handling
```css
/* Don't: remove focus indicator */
button:focus { outline: none; }

/* Do: provide accessible focus style */
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

## Code Review Checklist for CSS
- Are selectors low-specificity and maintainable?
- Are design tokens used consistently?
- Are focus, contrast, and motion accessibility requirements preserved?
- Is responsive behavior intentional and testable?
- Are global side effects/leaks minimized?
- Is `!important` avoided or justified?
- Are performance-heavy patterns avoided on hot interaction paths?

## Testing Guidance for CSS
- Add visual regression tests for critical components/pages.
- Validate responsive behavior at key breakpoints.
- Run accessibility checks for contrast and focus visibility.
- Test interactive states (hover/focus/active/disabled/error).
- Verify style isolation to avoid unintended cross-component regressions.
