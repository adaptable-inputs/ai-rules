---
applies_to:
  load: "conditional"
  when: "resilience4j is a declared dependency"
  libraries: ["resilience4j"]
  annex: "RESILIENCE4J.ANNEX.md"
  purpose: "safe usage of resilience primitives for remote dependency protection"
  inherits: ["ARCHITECTURE/CIRCUIT_BREAKER.md", "ARCHITECTURE/MICROSERVICE.md", "CORE/LOGGING.md"]
---
# RESILIENCE4J

Guidance for AI agents implementing and reviewing Resilience4j policies.

## Defaults
- SHOULD keep resilience policy per dependency/use case, not one global profile.
- SHOULD keep policies explicit and externally configurable where practical.
- SHOULD start conservative and tune using production telemetry.
- SHOULD keep fallback behavior correctness-preserving.

## Policy Composition Rules
- SHOULD retry only transient failures.
- Circuit breaker for failing/slow remote dependencies.
- Time limiter for bounded response latency.
- Bulkhead for resource isolation.
- SHOULD rate limiter for downstream protection and fair usage.
- SHOULD coordinate policies to avoid amplification loops.

## Configuration Guardrails
- SHOULD keep retry attempts bounded with backoff + jitter.
- SHOULD avoid retrying non-retryable business exceptions.
- SHOULD keep circuit-breaker thresholds/window sizes aligned with traffic profile.
- SHOULD keep bulkhead pool/queue settings aligned with capacity planning.
- SHOULD keep rate-limit and timeout values documented per dependency SLA.

## Observability and Operations
- SHOULD export metrics for policy activations and outcomes.
- SHOULD log state transitions and fallback activations with dependency context.
- SHOULD alert on sustained breaker open states, retry storms, and bulkhead rejection spikes.
