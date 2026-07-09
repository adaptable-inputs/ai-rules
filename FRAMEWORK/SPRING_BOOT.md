---
applies_to:
  load: "conditional"
  when: "spring-boot is a declared dependency"
  frameworks: ["spring-boot"]
  annex: "SPRING_BOOT.ANNEX.md"
---
# SPRING_BOOT

Guidance for AI agents implementing and reviewing Spring Boot applications.

## Scope
- Define Spring Boot-specific defaults for layering, configuration, and runtime
  behavior.
- Apply this file to Spring Boot service/application code and review.

## Semantic Dependencies
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md` and
  `LANGUAGE/JAVA/EFFECTIVE_JAVA.md`.
- Inherit architecture constraints from `ARCHITECTURE/CLEAN_ARCHITECTURE.md`
  and `ARCHITECTURE/REST.md` where relevant.
- Inherit cross-cutting constraints from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

## Defaults
- SHOULD prefer constructor injection (for example with Lombok
  `@RequiredArgsConstructor`), avoid field injection.
- SHOULD keep controllers thin; move orchestration/business rules into services or use-case classes.
- SHOULD keep persistence logic in repositories/adapters, not controllers.
- SHOULD prefer explicit DTOs for API boundaries.
- SHOULD use `@ConfigurationProperties` for structured config over scattered `@Value` usage.

## Configuration and Profiles
- SHOULD keep configuration keys stable and documented.
- SHOULD use profile/environment separation intentionally.
- SHOULD keep defaults safe for local/dev and override via environment for production.
- SHOULD validate critical configuration at startup.

## Web and API Layer
- SHOULD validate request payloads with Bean Validation.
- SHOULD keep exception-to-response mapping centralized (`@ControllerAdvice`).
- SHOULD use consistent API error payload shapes with trace correlation.
- SHOULD avoid exposing internal exception details to clients.

## Transactions and Persistence
- SHOULD keep transaction boundaries explicit and use-case aligned.
- SHOULD avoid long transactions with remote/network calls inside.
- SHOULD choose JPA or jOOQ intentionally per query complexity.
- SHOULD avoid Open Session in View reliance for business-critical flows.

## Asynchrony and Scheduling
- SHOULD use async/scheduling only with explicit thread pool configuration.
- SHOULD keep background job idempotency and retry policy explicit.
- SHOULD propagate correlation context where observability requires it.

## Observability
- SHOULD use structured logging with correlation IDs.
- SHOULD expose health/readiness checks meaningfully.
- SHOULD emit metrics for key business and dependency operations.
- SHOULD keep log/metric cardinality controlled.

## Security Baseline
- MUST enforce authentication/authorization at endpoint and service boundaries.
- MUST keep secrets out of code/config files; use secret management paths.
- MUST validate and sanitize external input.
- MUST apply least privilege for outbound clients and data access.

## Override Notes
- Library docs (JPA, jOOQ, Resilience4j, etc.) MAY add stricter rules for
  specific integrations, but Spring Boot layering, configuration, and boundary
  constraints here remain mandatory.
