---
applies_to:
  load: "always"
  annex: "LOGGING.ANNEX.md"
  purpose: "logging rules that maximize debuggability without leaking sensitive data or creating observability cost explosions"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# LOGGING

Guidance for AI agents implementing and reviewing logging behavior.

## Defaults
- MUST use structured logs (JSON or stable key-value pairs), not free-form strings.
- SHOULD emit one log entry per meaningful event; avoid duplicate logs for the same failure path.
- MUST include stable context keys:
  `timestamp`, `level`, `service`, `component`, `operation`, `traceId`
  (or equivalent correlation key).
- SHOULD keep message text concise and action-oriented; put variable context in fields.
- MUST keep logging side-effect free: logging MUST NOT change business behavior.

## Log Level Policy
- `TRACE`: high-frequency diagnostic details only for short-lived debugging.
- `DEBUG`: developer diagnostics that are safe but too noisy for production
  defaults.
- `INFO`: meaningful state transitions and successful business-relevant events.
- `WARN`: degraded or unexpected states where execution can continue.
- `ERROR`: failed operations requiring investigation or user-visible fallback.
- `FATAL` (if supported): unrecoverable startup/runtime failure before process
  termination.

Level selection rules:
- MUST NOT log expected domain outcomes as `ERROR` (for example validation
  failures caused by user input).
- MUST NOT log the same exception at multiple layers unless each layer adds
  distinct value.
- If an exception is rethrown unchanged, MUST log it at one boundary only.

## Event Design Rules
- SHOULD prefer event names that describe domain intent (`invoice.paid`,
  `auth.login.failed`) over technical noise.
- MUST keep key names stable over time; treat field renames as compatibility changes for dashboards/alerts.
- MUST include explicit outcome fields (`status`, `result`, `errorCode`) to support machine-readable alerting.
- For high-volume events, SHOULD include sampling metadata (`sampleRate`, `sampled=true/false`).

## Sensitive Data and Privacy Guardrails
- MUST NOT log secrets: passwords, API keys, tokens, private keys, session
  secrets, connection strings with credentials.
- MUST NOT log full personal data payloads; log minimal identifiers only when
  needed for supportability and allowed by policy.
- MUST redact or hash sensitive identifiers before emission.
- If uncertain whether data is sensitive, MUST treat it as sensitive and redact.
- MUST review logging in error handlers carefully; stack traces often contain sensitive request payload fragments.

## Cardinality and Volume Control
- SHOULD avoid unbounded/high-cardinality fields in indexed logs:
  raw user input, full URLs with query strings, full stack traces as labels,
  random IDs as metric labels.
- SHOULD put high-cardinality details in non-indexed payload fields when required.
- SHOULD apply rate limiting or sampling for repetitive failures and noisy warnings.
- MUST NOT log inside tight loops at `INFO`/`WARN`/`ERROR` without throttling.
- MUST ensure retries do not multiply identical log storms.

## Error Logging and Exception Boundaries
- MUST log enough context to reproduce failure: operation name, stable identifiers, dependency target, timeout/retry
  status.
- MUST preserve original exception cause chains when wrapping exceptions.
- SHOULD distinguish transient from permanent failures in fields (`retryable=true/false`).
- For async/background processing, SHOULD include job/task identifiers and attempt numbers.

## Correlation and Distributed Tracing
- MUST propagate and log correlation IDs across sync and async boundaries.
- SHOULD align logging context with tracing context (`traceId`, `spanId`) where available.
- For message-driven systems, SHOULD include message key/id and consumer group context.
- MUST ensure correlation context survives thread switching/reactive pipelines.

## Operational Reliability
- Logging failures MUST NOT crash core request handling.
- SHOULD use async/non-blocking appenders carefully; define backpressure/drop policy.
- SHOULD prefer bounded queues over unbounded memory growth in logging pipelines.
- MUST validate log formatter behavior under malformed payloads.

## Override Notes
- Framework/library docs MAY require additional fields or stricter logging
  behavior (for example HTTP-specific request IDs, Kafka offsets).
- Such specializations MAY narrow this baseline but MUST NOT weaken
  confidentiality or reliability constraints defined here.
