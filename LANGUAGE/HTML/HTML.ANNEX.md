---
applies_to:
  load: "annex"
  annex_of: "HTML.md"
  tasks: ["review", "test"]
---
# HTML - Annex

## High-Risk Pitfalls
1. Generic `<div>` usage where semantic elements exist.
2. Click handlers on non-interactive elements without keyboard support.
3. Missing labels/alt text causing accessibility failures.
4. Duplicate IDs breaking selectors and accessibility references.
5. Unescaped dynamic HTML introducing XSS risk.
6. Incorrect heading structure harming navigation and SEO.

## Do / Don't Examples
### 1. Semantic Controls
```html
<!-- Don't: clickable div -->
<div onclick="submitOrder()">Submit</div>

<!-- Do: semantic button -->
<button type="button">Submit</button>
```

### 2. Image Accessibility
```html
<!-- Don't: missing alt -->
<img src="/avatar.png">

<!-- Do: informative alt text -->
<img src="/avatar.png" alt="Customer profile picture">
```

### 3. Label Association
```html
<!-- Don't: unlabeled input -->
<input id="email" type="email">

<!-- Do: explicit label -->
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email">
```

## Code Review Checklist for HTML
- Is every `div`/`span` that conveys structure replaced by a semantic element?
- Is keyboard accessibility preserved for all interactions?
- Do controls have accessible names and clear labels?
- Is heading/landmark structure valid and navigable?
- Is every interpolated value escaped, and every HTML string sanitized before
  insertion?
- Are duplicate IDs and invalid nesting avoided?
- Are form validation/error semantics accessible?

## Testing Guidance for HTML
- Add accessibility checks (automated and spot manual keyboard testing).
- Test form controls with screen-reader-friendly labels and errors.
- Test dynamic rendering paths for escaping/sanitization behavior.
- Validate document structure with HTML linting/validation tools.
