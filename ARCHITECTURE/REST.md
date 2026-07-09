---
applies_to:
  load: "conditional"
  when: "the project exposes or consumes a REST API"
  annex: "REST.ANNEX.md"
  purpose: "REST API design constraints for correctness, compatibility, and operability"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "ARCHITECTURE/ARCHITECTURE.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md"]
---
# REST

Guidance for AI agents implementing and reviewing REST-style APIs.

## Resource and URI Design
- SHOULD model APIs around resources and domain capabilities, not UI internals.
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
- SHOULD deprecate before removal and document timelines.
- SHOULD version APIs only when compatibility cannot be preserved.
- SHOULD keep response fields stable; avoid semantic field repurposing.

## Pagination, Filtering, and Sorting
- SHOULD paginate list endpoints by default when cardinality can grow.
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
- MUST rate-limit and monitor abusive access patterns.

## Override Notes
- Framework docs MAY define controller/handler idioms, but REST contract,
  compatibility, and security requirements in this file remain authoritative.
