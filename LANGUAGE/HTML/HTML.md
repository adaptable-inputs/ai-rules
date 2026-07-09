---
applies_to:
  load: "conditional"
  when: "the project renders HTML"
  languages: ["html"]
  globs: ["**/*.html"]
  annex: "HTML.ANNEX.md"
---
# HTML

Guidance for AI agents implementing and reviewing HTML markup.

## Scope
- Define semantic, accessible, and secure HTML defaults.
- Apply this file for templates, server-rendered pages, component markup, and
  static documents.

## Semantic Dependencies
- Inherit naming/readability constraints from
  `LANGUAGE/CONVENTIONS.md` and `LANGUAGE/READABILITY.md`.
- Inherit security constraints from `SECURITY/SECURITY.md`.
- Inherit testing expectations from `TEST/TEST.md`.
- CSS/framework docs MAY specialize styling patterns, but SHOULD NOT weaken
  semantic and accessibility requirements.

## Defaults
- SHOULD use semantic HTML elements (`main`, `nav`, `section`, `article`, `button`).
- SHOULD prefer native controls over ARIA-heavy custom widgets when possible.
- SHOULD keep document structure valid and predictable: one `<main>` per page, logical heading hierarchy, meaningful
  landmarks.
- SHOULD keep markup declarative and free of presentation-only hacks.

## Accessibility Baseline
- SHOULD set the root document language (`<html lang="...">`) and set `dir` where bidirectional text requirements apply.
- SHOULD ensure interactive elements are keyboard reachable and operable.
- Every form control needs an accessible name (`label`, `aria-label`, etc.).
- SHOULD provide `alt` text for informative images; use empty alt for decorative images.
- SHOULD preserve heading order (`h1` -> `h2` -> `h3`) without skipping levels.
- SHOULD ensure sufficient text alternatives for icon-only controls.

## Forms and Inputs
- SHOULD use correct input types (`email`, `number`, `date`) to improve validation and assistive behavior.
- SHOULD associate labels explicitly with controls.
- SHOULD provide inline error feedback linked via accessibility attributes.
- SHOULD keep required/optional semantics explicit.

## Security and Injection Guardrails
- MUST NOT inject untrusted HTML directly into DOM output without sanitization.
- SHOULD avoid inline event handlers (`onclick`) in generated markup.
- SHOULD prefer escaping by default for dynamic text content.
- MUST treat URL-bearing attributes (`href`, `src`) as untrusted inputs and validate schemes.
- For links opened via `target="_blank"`, MUST include `rel="noopener"` (typically `noopener noreferrer`) to prevent
  reverse-tabnabbing.

## Performance and Maintainability
- SHOULD avoid deeply nested DOM structures without semantic justification.
- SHOULD keep reusable UI structures componentized where framework allows.
- SHOULD prefer lazy-loading for non-critical media where applicable.
- SHOULD avoid duplicated IDs and non-unique `id` attributes.

## Override Notes
- Framework docs MAY define templating syntax, but semantic and accessibility
  obligations in this file remain mandatory.
