---
applies_to:
  load: "annex"
  annex_of: "LOMBOK.md"
  tasks: ["review", "test"]
---
# LOMBOK - Annex

## High-Risk Pitfalls
1. `@Data` on entities with incorrect equals/hashCode semantics.
2. Hidden behavior from broad annotations reducing readability.
3. `@ToString` leaking sensitive or massive object graphs.
4. `@SneakyThrows` masking API exception contracts.
5. Annotation processing misconfiguration causing compile/runtime drift.
6. Handwritten no-arg/all-arg/required-arg constructors despite Lombok
   availability.
7. Handwritten ordinary getters/setters despite Lombok availability.
8. Manual logger field declarations instead of Lombok logging annotations.
9. Implicit nullability contracts or use of Lombok/Jakarta nullness annotations
   when JSpecify is available.

## Do / Don't Examples
### 1. Entity Identity
```text
Don't: @Data on JPA entity with mutable identity semantics.
Do:    selective Lombok annotations + deliberate equals/hashCode strategy.
```

### 2. Exception Transparency
```text
Don't: use @SneakyThrows to bypass checked exception design.
Do:    model exception flow explicitly unless justified otherwise.
```

### 3. Constructor Injection
```text
Don't: field injection with mutable dependencies.
Do:    @RequiredArgsConstructor + final dependencies.
```

### 4. Ordinary Accessors
```text
Don't: hand-write trivial getters/setters when Lombok is available.
Do:    use @Getter/@Setter and keep custom methods only for business logic.
```

### 5. Logger Wiring
```text
Don't: declare manual static logger fields in Lombok-enabled classes.
Do:    declare the logger with @Slf4j.
```

### 6. Nullness Strategy Precedence
```text
Don't: use Lombok/Jakarta nullness annotations when JSpecify is available.
Do:    use JSpecify when available; otherwise use @lombok.NonNull and
       @jakarta.annotation.Nullable as fallback.
```

## Code Review Checklist for Lombok
- Is Lombok reducing boilerplate without hiding critical behavior?
- Are simple constructors (`@NoArgsConstructor`, `@AllArgsConstructor`,
  `@RequiredArgsConstructor`) Lombok-generated when Lombok is available?
- For DI classes, is `@RequiredArgsConstructor` used by default?
- Are ordinary getters/setters Lombok-generated when Lombok is available?
- Are logger instances provided via Lombok log annotations (for example
  `@Slf4j`)?
- Is nullness annotation precedence correct (JSpecify first; Lombok/Jakarta
  fallback only when JSpecify is unavailable)?
- Under the chosen strategy, are fields/parameters/return types explicitly
  annotated for null contracts?
- Are risky annotations (`@Data`, `@SneakyThrows`) justified?
- Are equality/toString semantics safe and intentional?
- Is sensitive data excluded from generated toString output?
- Is lombok config/tooling consistency ensured?
- Are generated constructors aligned with DI framework needs?

## Testing Guidance
- Test equality/hashCode behavior for classes using generated methods.
- Test serialization/mapping behavior for Lombok-built DTOs.
- Validate build + IDE annotation processing consistency in CI.
- Add null-contract tests matching the active strategy (JSpecify if available;
  otherwise Lombok/Jakarta fallback annotations).
- Add regression tests when Lombok annotation strategy changes.
