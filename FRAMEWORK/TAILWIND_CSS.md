---
applies_to:
  load: "conditional"
  when: "a tailwind.config file is present"
  frameworks: ["tailwind"]
  annex: "TAILWIND_CSS.ANNEX.md"
  purpose: "Tailwind-specific rules for scalable, readable, and accessible styling"
  inherits: ["LANGUAGE/CSS/CSS.md", "LANGUAGE/HTML/HTML.md"]
---
# TAILWIND_CSS

Guidance for AI agents implementing and reviewing Tailwind CSS code.

## Defaults
- SHOULD prefer utility-first styling with clear class grouping by concern (layout, spacing, typography, color, state).
- SHOULD keep class lists readable and intentional.
- SHOULD use design tokens via Tailwind theme configuration instead of ad-hoc values.
- SHOULD prefer component extraction when class lists become repetitive or complex.

## Utility and Composition Rules
- SHOULD keep utilities local to component intent.
- SHOULD avoid giant one-off class strings with many conditionals.
- SHOULD prefer reusable abstractions for repeated UI patterns.
- SHOULD use `@apply` sparingly and only when it improves maintainability.
- SHOULD keep variant usage (`sm:`, `md:`, `hover:`, `focus:`) predictable and minimal.

## Design System Alignment
- SHOULD centralize colors, spacing, typography scales in config.
- SHOULD avoid arbitrary values unless genuinely required.
- SHOULD keep naming aligned with design language, not implementation details.
- SHOULD review custom plugins/utilities for long-term maintainability.

## Accessibility and UX
- SHOULD preserve focus-visible states.
- SHOULD ensure color contrast compliance.
- SHOULD ensure disabled/loading/error states are visually and semantically clear.
- SHOULD avoid motion-heavy transitions without reduced-motion consideration.

## Performance Baseline
- SHOULD ensure content paths are configured so unused classes are purged.
- SHOULD avoid dynamically constructed class names that evade static extraction.
- SHOULD keep generated CSS size bounded and monitored through the project's build and delivery standards.
- SHOULD prefer stable class composition over runtime string-generation complexity.
