---
applies_to:
  load: "always"
  annex: "CLEAN_CODE.ANNEX.md"
  purpose: "practical code-quality rules for maintainability and clarity"
  inherits: ["LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md", "DESIGN/SOLID.md"]
---
# CLEAN_CODE

Guidance for AI agents applying clean-code principles in implementation and
review.

## Core Principles
- SHOULD prioritize clarity over cleverness.
- SHOULD keep code intent obvious for future maintainers.
- SHOULD keep responsibilities cohesive and boundaries explicit.
- SHOULD prefer incremental improvement over large speculative rewrites.

## Naming and Intent
- SHOULD use precise, domain-driven names.
- SHOULD avoid ambiguous abbreviations.
- MUST keep naming consistent across module boundaries.
- MUST rename related symbols/comments when intent changes.

## Function and Method Design
- SHOULD keep functions focused on one responsibility.
- SHOULD avoid long parameter lists; group related data into value objects.
- SHOULD prefer guard clauses over deep nested conditionals.
- MUST keep side effects explicit.

## Error Handling
- MUST fail fast on invalid input/invariants.
- SHOULD use meaningful exception/error types.
- MUST NOT swallow errors silently.
- SHOULD keep error paths observable and actionable.

## Duplication and Abstraction
- SHOULD remove duplication that increases maintenance risk.
- SHOULD avoid premature abstraction with unclear reuse value.
- SHOULD extract shared behavior when duplication is stable and semantic.
- SHOULD keep abstractions aligned to domain concepts, not accidental code shape.

## Module and Dependency Hygiene
- SHOULD keep modules cohesive and dependency direction clear.
- SHOULD avoid cyclic dependencies.
- SHOULD keep public APIs minimal and stable.
- SHOULD avoid hidden coupling through globals/static mutable state.

## Override Notes
- Specialized docs MAY add stricter/idiomatic constraints; explicit overrides
  MUST be documented and justified.
- Framework/language docs MAY prescribe idiomatic structures, but clean-code
  clarity and cohesion constraints remain mandatory.
