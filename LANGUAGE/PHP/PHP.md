---
applies_to:
  load: "conditional"
  when: "composer.json is present"
  languages: ["php"]
  globs: ["**/*.php"]
  annex: "PHP.ANNEX.md"
---
# PHP

Guidance for AI agents implementing and reviewing PHP code.

## Scope
- Define baseline PHP rules for correctness, maintainability, and production
  safety.
- Apply this file for PHP code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific PHP docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD enable strict typing mode (`declare(strict_types=1)`) for application code.
- SHOULD keep function and public API type declarations explicit.
- SHOULD keep business logic separated from transport/framework glue code.
- MUST keep configuration and secrets outside source code.
- SHOULD keep dependency surface minimal and justified.

## Typing and API Contracts
- Type parameters, return values, and properties where supported.
- SHOULD avoid mixed/dynamic shapes for core domain contracts.
- SHOULD use value objects/DTOs for structured domain data.
- SHOULD validate external input at boundaries before domain processing.

## Error and Resource Handling
- SHOULD throw/map specific exception types with actionable context.
- MUST NOT suppress errors silently.
- SHOULD use deterministic cleanup for external resources (files/sockets/locks).
- SHOULD keep error-to-response mapping explicit at API boundaries.

## State and Side-Effect Control
- SHOULD avoid hidden mutable globals and implicit state.
- SHOULD keep side effects explicit in service boundaries.
- SHOULD keep static state and singleton usage minimal and intentional.
- SHOULD keep IO interactions isolated for testability.

## Override Notes
- Project-specific PHP conventions MAY add stricter patterns, but strict type
  discipline, explicit boundary validation, safe error handling, and clear
  side-effect boundaries remain mandatory.
