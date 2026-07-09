---
applies_to:
  load: "conditional"
  when: "the project ships stylesheets"
  languages: ["css"]
  globs: ["**/*.css", "**/*.scss"]
  annex: "CSS.ANNEX.md"
  purpose: "CSS baseline rules for predictable, maintainable, and accessible UI styling"
  inherits: ["LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md", "SECURITY/SECURITY.md"]
---
# CSS

Guidance for AI agents implementing and reviewing CSS.

## Defaults
- SHOULD prefer low-specificity, composable selectors.
- SHOULD use design tokens/variables for colors, spacing, typography, and sizing.
- SHOULD keep style concerns separate from markup structure where practical.
- SHOULD prefer modern layout systems (`flex`, `grid`) over float/position hacks.
- SHOULD keep responsive behavior mobile-first unless project constraints differ.

## Selector and Specificity Rules
- SHOULD avoid IDs in selectors for styling.
- SHOULD keep selector depth shallow.
- SHOULD avoid `!important` except for controlled utility/override cases with
  documented rationale.
- SHOULD prefer class-based selectors over element and descendant-heavy chains.
- SHOULD keep state styles explicit (`is-active`, `has-error` patterns).

## Architecture and Reuse
- SHOULD use consistent naming strategy (BEM/utility/component-based) per project.
- SHOULD co-locate component styles with component ownership boundaries.
- SHOULD avoid global leakage; scope styles where tooling supports it.
- SHOULD remove dead styles during refactors.

## Accessibility and UX Baseline
- SHOULD preserve visible focus indicators for keyboard navigation.
- SHOULD ensure color contrast meets accessibility requirements.
- MUST NOT communicate state by color alone.
- SHOULD respect user preferences (`prefers-reduced-motion`, dark mode policy where applicable).

## Performance Baseline
- SHOULD avoid expensive selectors and overly broad wildcard patterns.
- SHOULD avoid unnecessary layout thrash via frequent class/style mutations.
- SHOULD keep animation properties to performant transforms/opacity when possible.
- SHOULD limit large paint-heavy effects on scrolling/high-frequency interactions.
