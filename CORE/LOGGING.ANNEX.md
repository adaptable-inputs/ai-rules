---
applies_to:
  load: "annex"
  annex_of: "LOGGING.md"
  tasks: ["review", "test"]
---
# LOGGING - Annex

## High-Risk Pitfalls
1. Logging secrets or raw personal payloads.
2. Logging the same failure repeatedly at multiple layers.
3. High-cardinality fields causing indexing/storage cost spikes.
4. Missing correlation IDs across service boundaries.
5. Logging side effects that alter business logic timing/outcomes.
6. Silent logger initialization failure with no fallback behavior.
7. Catch-and-log-without-rethrow where callers need failure semantics.

## Do / Don't Examples
```text
# Don't: duplicate exception logging across layers.
controller: ERROR "save failed" ex=...
service:    ERROR "save failed" ex=...
repository: ERROR "save failed" ex=...

# Do: log once at the handling boundary with context.
controller: ERROR "invoice save failed" invoiceId=... traceId=... ex=...
```

```jsonc
// Don't: free-form string with sensitive payload.
{"level":"ERROR","message":"login failed for user=alice password=secret"}

// Do: structured, redacted, machine-readable fields.
{"level":"WARN","event":"auth.login.failed","userIdHash":"...",
 "reason":"invalid_credentials","traceId":"..."}
```

## Code Review Checklist for Logging
- Is structured logging used consistently with stable keys?
- Are `ERROR` logs reserved for real failures, not expected user behavior?
- Are secrets/PII excluded or redacted in all success and error paths?
- Is correlation context (`traceId`/`requestId`) present at boundaries?
- Are duplicate logs for the same exception path avoided?
- Are high-cardinality fields avoided in indexed labels/tags?
- Are retry loops and hot paths protected from log storms?
- Does logging remain non-blocking and failure-tolerant?
- Are event names/messages actionable for operators?

## Testing Guidance for Logging Behavior
- Test sensitive-data redaction paths explicitly.
- Test representative error paths to ensure one boundary log, not many.
- Test correlation propagation across async/reactive/message boundaries.
- Test sampling/rate-limit behavior for repeated failures.
- Test malformed payload handling in log formatting.
- If alerting depends on fields, test field presence and schema stability.
