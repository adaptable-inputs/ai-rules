---
applies_to:
  load: "conditional"
  when: "Gemfile is present"
  languages: ["ruby"]
  globs: ["**/*.rb"]
  annex: "RUBY.ANNEX.md"
---
# RUBY

Guidance for AI agents implementing and reviewing Ruby code.

## Scope
- Define baseline Ruby rules for correctness, maintainability, and production
  safety.
- Apply this file for Ruby code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific Ruby docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD prefer explicit object contracts over ad-hoc dynamic behavior.
- SHOULD keep domain logic separate from framework/transport concerns.
- SHOULD keep side effects explicit and isolated to boundary layers.
- SHOULD keep dependency usage minimal and maintainable.
- SHOULD validate external input at boundaries before domain operations.

## API and Object Design
- SHOULD keep class/module responsibilities cohesive.
- SHOULD use explicit method arguments and return expectations for critical paths.
- SHOULD avoid metaprogramming for core business logic when plain Ruby is clearer.
- SHOULD keep mutation boundaries intentional and documented.

## Error Handling and Reliability
- SHOULD raise/map specific exceptions with contextual information.
- MUST NOT rescue broad exceptions without bounded rationale.
- SHOULD keep retries/timeouts explicit for external dependencies.
- SHOULD preserve root cause context when mapping errors at boundaries.

## State and Side-Effect Control
- SHOULD avoid hidden global state and implicit mutable singletons.
- SHOULD keep transactional boundaries explicit for stateful operations.
- SHOULD keep IO operations at service/adapter boundaries for testability.
- MUST keep logging redacted and purpose-minimal for sensitive fields.

## Override Notes
- Project-specific Ruby conventions MAY add stricter patterns, but explicit
  contracts, bounded error handling, clear side-effect boundaries, and boundary
  validation remain mandatory.
