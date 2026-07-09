---
applies_to:
  load: "conditional"
  when: "composer.json is present"
  languages: ["php"]
  globs: ["**/*.php"]
  annex: "PHP.ANNEX.md"
  purpose: "baseline PHP rules for correctness, maintainability, and production safety"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# PHP

Guidance for AI agents implementing and reviewing PHP code.

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
