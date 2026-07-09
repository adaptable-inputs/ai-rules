---
applies_to:
  load: "conditional"
  when: "the project calls remote dependencies"
  annex: "CIRCUIT_BREAKER.ANNEX.md"
---
# CIRCUIT_BREAKER

Guidance for AI agents implementing and reviewing circuit breaker patterns.

## Scope
- Define when and how to apply circuit breakers to remote dependencies.
- Apply this file to service-to-service calls and external IO boundaries.

## Semantic Dependencies
- Inherit architecture baseline from `ARCHITECTURE/ARCHITECTURE.md`.
- Inherit cross-cutting defaults from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.
- Service communication architecture docs MAY specialize breaker usage for their
  communication patterns.

## Placement Rules
- SHOULD place circuit breakers at every remote dependency boundary: HTTP, gRPC, database, and message broker clients.
- MUST NOT apply circuit breakers to in-memory pure operations.
- SHOULD keep breaker scope aligned with dependency blast radius.

## Configuration Defaults
- SHOULD configure timeout, failure-rate threshold, sliding window size, and half-open probe behavior explicitly.
- SHOULD keep retry policy coordinated with breaker settings to avoid storm loops.
- SHOULD use per-dependency configuration; avoid one global profile for all integrations.
- SHOULD keep defaults conservative and tune from production telemetry.

## Fallback Strategy
- SHOULD use fallback only when correctness is preserved.
- SHOULD prefer explicit degraded mode responses over silent stale/incorrect data.
- SHOULD avoid fallback chains that hide systemic failures.
- SHOULD record fallback activation as observable event.

## State Semantics
- Closed: normal operation.
- Open: short-circuit calls for cooldown period.
- Half-open: allow limited probes to test recovery.
- SHOULD keep transitions observable in logs/metrics/events.

## Observability Requirements
- SHOULD emit metrics for call outcomes, breaker state transitions, and short-circuit counts.
- SHOULD log contextual events on open/close transitions with dependency identity.
- SHOULD alert on sustained open state and high fallback rates.
- SHOULD track user-facing degradation tied to breaker events.

## Override Notes
- Library/framework docs MAY prescribe implementation API (for example
  Resilience4j annotations), but placement, correctness, and observability
  constraints in this file remain mandatory.
