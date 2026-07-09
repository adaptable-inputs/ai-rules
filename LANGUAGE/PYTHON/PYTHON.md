---
applies_to:
  load: "conditional"
  when: "pyproject.toml, setup.py, or requirements.txt is present"
  languages: ["python"]
  globs: ["**/*.py"]
  annex: "PYTHON.ANNEX.md"
---
# PYTHON

Guidance for AI agents implementing and reviewing Python code.

## Scope
- Define baseline Python rules for correctness, maintainability, and production
  safety.
- Apply this file for Python code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific Python docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD prefer explicit, readable code over clever one-liners.
- SHOULD use type hints for public APIs and complex internal boundaries.
- SHOULD keep module boundaries cohesive and side effects explicit.
- SHOULD use virtual environments and pinned dependencies for reproducibility.
- SHOULD validate external input at boundaries and fail fast with clear errors.

## Typing and API Design
- Type public function/method signatures and return values.
- SHOULD use domain-specific types/dataclasses for structured business data.
- SHOULD avoid broad `Any` usage unless explicitly justified.
- SHOULD keep `Optional`/`None` handling explicit at call boundaries.

## Error Handling and Resource Safety
- SHOULD raise specific exceptions with actionable context.
- MUST NOT swallow exceptions silently.
- MUST use context managers for files/sockets/transactions/locks.
- SHOULD preserve root cause context when mapping exceptions at boundaries.

## State, Concurrency, and Async Rules
- SHOULD avoid shared mutable global state by default.
- SHOULD keep thread/process safety explicit when concurrency is used.
- SHOULD use `async`/`await` for IO-bound concurrency, not CPU-bound work.
- SHOULD keep async cancellation and timeout behavior explicit for external calls.

## Packaging and Imports
- SHOULD keep import paths stable and avoid circular dependencies.
- SHOULD keep configuration separate from runtime/business logic.
- SHOULD keep dependency surface minimal and justified.
- SHOULD keep scripts/entrypoints thin and delegate behavior to testable modules.

## Override Notes
- Project-specific Python conventions MAY add stricter patterns, but explicit
  typing, boundary validation, safe error handling, and deterministic dependency
  behavior remain mandatory.
