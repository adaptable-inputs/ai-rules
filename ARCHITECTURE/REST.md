---
applies_to:
  load: "conditional"
  when: "the project exposes or consumes a REST API"
---
# REST

Guidance for AI agents implementing and reviewing REST-style APIs.

## Scope
- Define REST API design constraints for correctness, compatibility, and
  operability.
- Apply this file to service interface design and API review.

## Semantic Dependencies
- Inherit the full cross-cutting baseline as defined in
  `CORE/RULE_DEPENDENCY_TREE.md` (including security/testing/logging and other
  mandatory cross-cutting constraints).
- Inherit architecture boundaries from `ARCHITECTURE/ARCHITECTURE.md` and
  `ARCHITECTURE/CLEAN_ARCHITECTURE.md`.
- Specialized framework docs MAY refine implementation details but SHOULD keep
  protocol/contract constraints here.

## Resource and URI Design
- Model APIs around resources and domain capabilities, not UI internals.
- SHOULD keep URIs noun-based and stable.
- SHOULD use plural resource names for collections.
- SHOULD keep hierarchy shallow; avoid deeply nested paths when IDs suffice.
- SHOULD use explicit sub-resources only when ownership relationship is clear.

## HTTP Method Semantics
- `GET`: safe and read-only.
- `POST`: create or non-idempotent action.
- `PUT`: full replacement, idempotent.
- `PATCH`: partial update with explicit patch semantics.
- `DELETE`: remove/deactivate resource with clear idempotency expectations.
- MUST NOT overload methods with mismatched behavior.

## Status Codes and Error Model
- SHOULD use standard status codes consistently.
- SHOULD return machine-readable error payloads with stable fields (`code`, `message`, `details`, `traceId`).
- SHOULD distinguish validation failures (`4xx`) from server/dependency failures (`5xx`).
- SHOULD avoid returning `200` for failed operations.

## Versioning and Compatibility
- SHOULD prefer backward-compatible additive changes.
- Deprecate before removal and document timelines.
- Version APIs only when compatibility cannot be preserved.
- SHOULD keep response fields stable; avoid semantic field repurposing.

## Pagination, Filtering, and Sorting
- Paginate list endpoints by default when cardinality can grow.
- SHOULD keep filtering/sorting parameters explicit and validated.
- SHOULD ensure pagination ordering is deterministic.
- SHOULD return pagination metadata when useful (`total`, `nextCursor`, etc.).

## Concurrency and Idempotency
- SHOULD support idempotency keys for retry-prone create endpoints when needed.
- SHOULD use conditional requests (`ETag`, `If-Match`) for optimistic concurrency where applicable.
- SHOULD document retry-safe operations clearly.

## Caching and Performance
- SHOULD use cache headers intentionally for cacheable responses.
- SHOULD avoid over-fetching payloads; use targeted representations.
- SHOULD keep response times predictable for hot paths and monitor SLA-critical endpoints.

## Security Baseline
- MUST enforce authentication and authorization at resource boundaries.
- MUST validate and sanitize all input parameters/body fields.
- MUST NOT expose internal stack traces or sensitive fields in responses.
- Rate-limit and monitor abusive access patterns.

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

## Override Notes
- Framework docs MAY define controller/handler idioms, but REST contract,
  compatibility, and security requirements in this file remain authoritative.
