---
applies_to:
  load: "conditional"
  when: "lombok is a declared dependency"
  libraries: ["lombok"]
  annex: "LOMBOK.ANNEX.md"
---
# LOMBOK

Guidance for AI agents implementing and reviewing Lombok usage.

## Scope
- Define when Lombok improves clarity and when explicit code is safer.
- Apply this file to Java classes using Lombok annotations.

## Semantic Dependencies
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md` and
  `LANGUAGE/JAVA/EFFECTIVE_JAVA.md`.
- Inherit design/readability constraints from `DESIGN/CLEAN_CODE.md`.

## Defaults
- SHOULD use Lombok to remove low-value boilerplate while preserving clarity.
- If Lombok is available, SHOULD implement simple constructors with Lombok annotations (`@NoArgsConstructor`,
  `@AllArgsConstructor`, `@RequiredArgsConstructor`).
- For dependency injection, SHOULD prefer `@RequiredArgsConstructor` as the default constructor strategy.
- If Lombok is available, SHOULD implement ordinary getters/setters with `@Getter`/`@Setter`.
- If Lombok is available, SHOULD declare loggers with the Lombok annotation matching the project's logging backend
  (`@Slf4j` for SLF4J).
- SHOULD prefer `@Builder` for complex immutable object construction.
- SHOULD prefer explicit annotations over broad convenience annotations when behavior
  matters.

## Annotation Selection Policy
- `@Getter`/`@Setter`: required for ordinary accessor boilerplate; write manual
  methods only when logic/validation is needed.
- Constructor annotations: use Lombok constructor annotations for simple
  constructor shapes instead of handwritten constructor boilerplate.
- For dependency injection use cases, SHOULD prefer `@RequiredArgsConstructor`; use
  `@NoArgsConstructor`/`@AllArgsConstructor` only when framework or boundary requirements demand those shapes.
- Logging annotations (`@Slf4j`, `@Log4j2`, etc.): required for logger fields
  instead of manual logger instance declarations.
- `@Value` (`lombok.Value`): prefer for immutable DTO/value objects.
- `@Data`: avoid by default on domain entities and types with nuanced identity.
- `@EqualsAndHashCode`: configure intentionally for inheritance/identity.
- `@ToString`: avoid exposing large graphs or sensitive fields.

## Null Handling
- JSpecify nullness annotations take precedence whenever JSpecify is available.
- Lombok/Jakarta nullness annotations are fallback only:
  use `@lombok.NonNull` and `@jakarta.annotation.Nullable` only when JSpecify
  is not available.
- SHOULD keep null contracts explicit on fields, parameters, and return types under the active nullness annotation
  strategy.
- MUST NOT choose Lombok nullness annotations when JSpecify is present.

## Risky Annotations and Guardrails
- `@SneakyThrows`: use only with explicit rationale and bounded scope.
- `@Builder.Default`: verify semantics for null/optional behavior.
- `@SuperBuilder`: use cautiously; avoid deep inheritance complexity.
- SHOULD keep generated behavior understandable to reviewers.

## Tooling and Build Consistency
- SHOULD ensure annotation processing is enabled in build and IDE.
- SHOULD keep `lombok.config` committed and consistent.
- SHOULD configure `lombok.copyableAnnotations` for framework-required constructor annotations where needed.
- SHOULD avoid IDE/build mismatch where generated code differs.

## Override Notes
- If project policy prefers explicit boilerplate in critical modules, follow
  stricter module policy. Baseline rule: favor clarity over annotation density.
- Explicit specialization in this doc: when Lombok is available, constructor,
  ordinary accessor, and logger boilerplate SHOULD be Lombok-generated.
- Nullness specialization: JSpecify always takes precedence; Lombok/Jakarta
  nullness annotations are fallback only when JSpecify is unavailable.
