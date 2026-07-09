---
applies_to:
  load: "annex"
  annex_of: "REST.md"
  tasks: ["review", "test"]
---
# REST - Annex

## High-Risk Pitfalls
1. Endpoint behavior inconsistent with HTTP method semantics.
2. Silent breaking changes in response schemas.
3. Non-deterministic pagination order causing duplicate/missing items.
4. Leaking sensitive internal errors in API responses.
5. Missing idempotency strategy causing duplicate writes on retries.
6. Inconsistent error shapes across endpoints.
7. Over-nested URI structures tightly coupled to database shape.

## Do / Don't Examples
### 1. Method Semantics
```text
Don't: GET /orders/123/cancel
Do:    POST /orders/123/cancellations
```

### 2. Error Shape
```jsonc
// Don't
{"error":"bad request"}

// Do
{"code":"VALIDATION_ERROR","message":"email is invalid",
 "details":{"field":"email"},"traceId":"..."}
```

### 3. Pagination
```text
Don't: GET /orders?page=2  (no stable sort)
Do:    GET /orders?cursor=...&limit=50 with deterministic ordering
```

## Code Review Checklist for REST APIs
- Do URI and method semantics match REST expectations?
- Are status codes and error shapes consistent and actionable?
- Are compatibility and versioning concerns addressed?
- Are pagination/filter/sort semantics deterministic and validated?
- Are idempotency and retry behavior safe for writes?
- Are auth/authz and input validation consistently enforced?
- Are observability fields (`traceId`, error codes) present?

## Testing Guidance for REST APIs
- Add contract tests for request/response schemas.
- Test validation and authorization failure paths.
- Test pagination/filter/sort determinism.
- Test idempotency/retry behavior for create/update operations.
- Test backward compatibility for non-breaking API evolution.
