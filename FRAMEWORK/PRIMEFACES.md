---
applies_to:
  load: "conditional"
  when: "primefaces is a declared dependency"
  frameworks: ["primefaces"]
  annex: "PRIMEFACES.ANNEX.md"
  purpose: "PrimeFaces-specific rules for JSF lifecycle, state handling, and UI behavior"
  inherits: ["LANGUAGE/JAVA/JAVA.md", "LANGUAGE/HTML/HTML.md", "LANGUAGE/CSS/CSS.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# PRIMEFACES

Guidance for AI agents implementing and reviewing PrimeFaces/JSF projects.

## Defaults
- SHOULD keep JSF views presentation-focused.
- SHOULD keep business logic in services/use-cases, not backing beans.
- SHOULD use explicit bean scopes (`@RequestScoped`, `@ViewScoped`, `@SessionScoped`) based on lifecycle need.
- SHOULD prefer reusable composites/components for repeated UI patterns.

## State and Scope Rules
- SHOULD keep view/session state minimal.
- SHOULD avoid storing large mutable graphs in session scope.
- SHOULD keep conversation state explicit; clear state on flow completion.
- MUST NOT use broader scope than needed.

## Component and Ajax Usage
- SHOULD keep partial updates targeted (`update`/`process` scopes explicit).
- SHOULD avoid broad page re-renders for small interactions.
- SHOULD keep component IDs stable and predictable.
- SHOULD prefer declarative component configuration over heavy imperative JS hacks.

## Validation and Error Handling
- SHOULD use Bean Validation for model constraints.
- SHOULD keep validation messages user-actionable.
- SHOULD handle conversion/validation failures consistently.
- SHOULD avoid swallowing backend exceptions in UI layer.

## Performance Baseline
- SHOULD minimize component tree complexity in heavy pages.
- SHOULD avoid unnecessary nested forms/components.
- SHOULD lazy-load large datasets where possible.
- SHOULD profile expensive render phases and optimize high-cost components.

## Security Baseline
- MUST enforce authorization on backend operations, not only UI rendering.
- MUST protect against CSRF/XSS with framework and platform controls.
- SHOULD avoid exposing sensitive data in hidden fields/view state.
- MUST keep file upload and input handling strictly validated.
