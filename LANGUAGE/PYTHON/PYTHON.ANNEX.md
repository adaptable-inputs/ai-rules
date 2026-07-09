---
applies_to:
  load: "annex"
  annex_of: "PYTHON.md"
  tasks: ["review", "test"]
---
# PYTHON - Annex

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
