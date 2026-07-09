---
applies_to:
  load: "conditional"
  when: "pyproject.toml, setup.py, or requirements.txt is present"
  languages: ["python"]
  globs: ["**/*.py"]
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
- Raise specific exceptions with actionable context.
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

## High-Risk Pitfalls
1. Untyped public APIs that hide contract drift.
2. Catch-all exception handlers that mask production failures.
3. Hidden side effects during import/module initialization.
4. Shared mutable globals causing concurrency bugs.
5. Mixing blocking calls into async request paths.
6. Implicit `None` handling that creates runtime failures.
7. Unpinned dependencies causing non-deterministic behavior.

## Do / Don't Examples
### 1. Exception Handling
```python
# Don't: swallow broad exceptions.
try:
    persist_order(order)
except Exception:
    pass

# Do: catch specific exceptions and preserve context.
try:
    persist_order(order)
except DatabaseError as exc:
    raise OrderPersistenceError(order.id) from exc
```

### 2. Typing
```python
# Don't: untyped public API contract.
def fetch_user(user_id):
    ...

# Do: typed API contract.
def fetch_user(user_id: str) -> User:
    ...
```

### 3. Async Safety
```python
# Don't: run blocking work directly in async path.
async def load_payload(path: str) -> bytes:
    with open(path, "rb") as file_handle:
        return file_handle.read()

# Do: isolate blocking work off the event loop.
async def load_payload(path: str) -> bytes:
    return await asyncio.to_thread(Path(path).read_bytes)
```

## Code Review Checklist for Python
- Are public APIs typed and contracts explicit?
- Is exception handling specific and non-silent?
- Are resource lifecycles managed safely (context managers/timeouts)?
- Are concurrency/async assumptions explicit and safe?
- Are module boundaries cohesive with minimal side effects?
- Are dependency additions justified and pinned?

## Testing Guidance
- Test typed API contracts and boundary validation behavior.
- Test exception mapping and error-path outcomes.
- Test concurrency/async paths for timeout/cancellation/race conditions.
- Test configuration parsing and environment-boundary logic.
- Add regression tests for previously observed bug classes.

## Override Notes
- Project-specific Python conventions MAY add stricter patterns, but explicit
  typing, boundary validation, safe error handling, and deterministic dependency
  behavior remain mandatory.
