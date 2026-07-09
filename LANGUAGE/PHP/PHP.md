---
applies_to:
  load: "conditional"
  when: "composer.json is present"
  languages: ["php"]
  globs: ["**/*.php"]
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
- Enable strict typing mode (`declare(strict_types=1)`) for application code.
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

## High-Risk Pitfalls
1. Running with loose typing and implicit coercion in domain logic.
2. Mixed-array contracts with unclear schema/ownership.
3. Silent error suppression and missing boundary mappings.
4. Hidden globals/static state creating non-deterministic behavior.
5. Framework-coupled business logic reducing testability.
6. Unvalidated external input reaching domain/database layers.
7. Dependency growth without maintenance/compliance review.

## Do / Don't Examples
### 1. Type Safety
```text
Don't: rely on implicit type coercion in core business paths.
Do:    use strict types and explicit type contracts.
```

### 2. Error Handling
```text
Don't: suppress exceptions and continue with undefined state.
Do:    map exceptions explicitly at API/service boundaries.
```

### 3. Input Validation
```text
Don't: pass raw request payloads directly into domain logic.
Do:    validate and normalize boundary input first.
```

## Code Review Checklist for PHP
- Is strict typing enabled and used consistently?
- Are API contracts typed and explicit?
- Are exceptions mapped specifically and non-silently?
- Are side effects/global state minimized and clear?
- Are boundaries between framework and domain logic well defined?
- Are dependencies justified, maintained, and compliant?

## Testing Guidance
- Test boundary validation and normalization behavior.
- Test exception mapping and error-path outputs.
- Test type-contract-sensitive paths for coercion regressions.
- Test side-effect boundaries with focused integration tests.
- Add regression tests for previously observed bug classes.

## Override Notes
- Project-specific PHP conventions MAY add stricter patterns, but strict type
  discipline, explicit boundary validation, safe error handling, and clear
  side-effect boundaries remain mandatory.
