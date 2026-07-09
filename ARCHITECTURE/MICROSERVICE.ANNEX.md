---
applies_to:
  load: "annex"
  annex_of: "MICROSERVICE.md"
  tasks: ["review", "test"]
---
# MICROSERVICE - Annex

## High-Risk Pitfalls
1. Premature microservice adoption without clear boundaries.
2. Shared databases creating hidden coupling.
3. Chatty synchronous chains amplifying latency and failure risk.
4. Breaking API changes without compatibility strategy.
5. Missing observability/correlation across service hops.
6. Centralized "utility service" becoming bottleneck/single point of failure.
7. Over-distributed transactions with fragile consistency guarantees.

## Do / Don't Examples
### 1. Boundary Ownership
```text
Don't: User service and Billing service write same users table.
Do:    each service owns its storage; integrate via API/event contracts.
```

### 2. Communication Pattern
```text
Don't: synchronous fan-out chain for non-critical updates.
Do:    publish domain event for eventual consistency workflows.
```

### 3. Compatibility
```text
Don't: remove response field without migration path.
Do:    add replacement field, deprecate old field, monitor usage before removal.
```

## Code Review Checklist for Microservices
- Is service split justified by capability/ownership requirements?
- Are boundaries and contracts explicit and stable?
- Is data ownership isolated per service?
- Are cross-service calls protected (timeouts/retries/circuit breakers)?
- Is consistency model explicit for multi-service workflows?
- Are observability and correlation built in across boundaries?
- Are auth/authz and least-privilege controls enforced?

## Testing Guidance
- Add contract tests between service providers/consumers.
- Add integration tests for critical cross-service workflows.
- Test retry/timeout/circuit-breaker behavior.
- Test eventual-consistency and compensation flows.
- Run failure-injection scenarios for dependency outages.
