---
applies_to:
  load: "conditional"
  when: "the system is decomposed into services"
  annex: "MICROSERVICE.ANNEX.md"
  purpose: "when and how to use microservices safely"
  inherits: ["ARCHITECTURE/ARCHITECTURE.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md", "ARCHITECTURE/CIRCUIT_BREAKER.md", "ARCHITECTURE/EVENT_DRIVEN_ARCHITECTURE.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# MICROSERVICE

Guidance for AI agents implementing and reviewing microservice architecture.

## Adoption Criteria
- SHOULD prefer modular monolith first unless there is a clear need for independent
  scaling, deployment cadence, ownership, or isolation.
- SHOULD define measurable reasons for each service split.
- SHOULD avoid splitting by technical layers; split by business capability.

## Service Boundary Rules
- Each service owns a clear domain capability and bounded context.
- SHOULD keep APIs small, stable, and domain-oriented.
- SHOULD avoid shared domain model libraries that force lockstep releases.
- SHOULD keep ownership explicit (team/service accountability).

## Data Ownership and Consistency
- Each service owns its data store/schema.
- SHOULD avoid shared database writes across services.
- SHOULD use explicit integration patterns for cross-service consistency (events, sagas, compensating actions).
- MUST NOT assume distributed transactions by default.

## Communication Strategy
- SHOULD prefer asynchronous messaging for decoupled workflows.
- SHOULD use synchronous calls only when immediate response is required.
- SHOULD timebox and protect remote calls with timeout/retry/circuit-breaker patterns.
- SHOULD keep contracts versioned and backward-compatible.

## Reliability and Operability
- SHOULD design for partial failures and graceful degradation.
- SHOULD include correlation IDs across service boundaries.
- SHOULD keep health/readiness checks meaningful.
- SHOULD instrument latency, error rate, saturation, and queue lag.
- SHOULD keep service startup/shutdown behavior predictable.

## Security Baseline
- MUST enforce service-to-service authentication and authorization.
- MUST apply least privilege for data and network access.
- MUST validate all incoming payloads at service boundaries.
- SHOULD avoid exposing internal topology details via public errors.
