---
applies_to:
  load: "annex"
  annex_of: "SPRING_BOOT.md"
  tasks: ["review", "test"]
---
# SPRING_BOOT - Annex

## High-Risk Pitfalls
1. Business logic in controllers.
2. Field injection and hidden dependencies.
3. Configuration sprawl via many ad-hoc `@Value` strings.
4. Leaky exceptions returning stack traces to clients.
5. Open-ended transactions across remote calls.
6. Silent async failures in scheduled/background jobs.
7. Overuse of global state/static caches without lifecycle control.

## Do / Don't Examples
### 1. Injection Style
```text
Don't: @Autowired field injection.
Do:    constructor injection with final dependencies.
```

### 2. Layering
```text
Don't: controller directly manipulates EntityManager.
Do:    controller -> service/use-case -> repository adapter.
```

### 3. Config Management
```text
Don't: scattered @Value("${x.y}") across many classes.
Do:    typed @ConfigurationProperties with validation.
```

## Code Review Checklist for Spring Boot
- Are dependencies injected via constructors?
- Are controller/service/repository boundaries respected?
- Are validation and error mapping consistent and centralized?
- Are transactions scoped and safe?
- Is configuration typed, validated, and environment-safe?
- Are observability and correlation patterns applied?
- Are security boundaries enforced and secrets handled correctly?

## Testing Guidance
- Add unit tests for service/use-case logic.
- Add slice tests for web/persistence layers where useful.
- Add integration tests for transaction and persistence behavior.
- Add security tests for auth/authz and error exposure.
- Add tests for configuration binding/validation of critical properties.
