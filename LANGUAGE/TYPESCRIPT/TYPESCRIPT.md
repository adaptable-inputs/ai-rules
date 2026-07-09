---
applies_to:
  load: "conditional"
  when: "tsconfig.json is present"
  languages: ["typescript"]
  globs: ["**/*.ts", "**/*.tsx"]
---
# TYPESCRIPT

Guidance for AI agents implementing and reviewing TypeScript code.

## Scope
- Define TypeScript-specific rules that specialize JavaScript guidance.
- Apply this file for all `.ts`/`.tsx` implementation and review tasks.

## Semantic Dependencies
- Inherit JavaScript baseline from
  `LANGUAGE/JAVASCRIPT/JAVASCRIPT.md`.
- Inherit cross-cutting constraints from:
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.
- Inherit naming/readability expectations from:
  `LANGUAGE/CONVENTIONS.md`, `LANGUAGE/READABILITY.md`.
- Framework docs MAY further specialize TypeScript usage, but MUST NOT weaken
  type-safety and runtime-safety constraints.

## Compiler and Project Defaults
- Enable and keep strict mode enabled (`"strict": true`).
- SHOULD treat type errors as blocking for merges in CI.
- SHOULD keep `noImplicitOverride`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` enabled unless a
  documented project constraint prevents it.
- SHOULD keep `skipLibCheck` disabled by default for long-term correctness; enable only with explicit rationale.

## Typing Strategy
- SHOULD prefer precise domain types over broad primitives and ad-hoc objects.
- SHOULD prefer `type` aliases for unions/utility composition and `interface` for
  extendable object contracts; use whichever is clearer for the case.
- SHOULD avoid `any`.
  If unavoidable at a boundary, isolate it and narrow immediately.
- SHOULD prefer `unknown` for untrusted inputs and narrow with type guards.
- Model state variants with discriminated unions instead of boolean flags.
- SHOULD use `readonly` for immutable APIs and value objects.

## Domain Types vs Ad-Hoc Objects
- Use this default split:
  domain type for semantic data with meaning and invariants;
  ad-hoc object for local, short-lived, mechanical data.
- SHOULD treat ad-hoc objects as local implementation details. Promote them to named types once they start shaping
  domain contracts.

### Require Named Domain Types When
- Data crosses a boundary:
  exported function signatures, cross-module contracts, package boundaries,
  persistence models, network DTOs, or event payloads.
- The shape is reused or shared:
  used in multiple call sites, stored and passed around, or repeated in tests.
- The data has invariants or behavior:
  needs validation, normalization, derived fields, or domain operations.
- Complexity is no longer trivial:
  nested structures, multiple lifecycle states, or domain unions/workflows.

### Allow Ad-Hoc Objects When Local
- Options/config bags for infrastructure helpers
  (for example retry/cache/http/logging helpers).
- Query/filter/URL parameter objects that remain local to one call flow.
- `Record`/dictionary lookup maps for simple key-to-value translations.
- UI-local view models or style/config objects kept inside one component/module.
- Test fixtures/mocks that stay local to one test;
  promote to builders/factories when shared.

### Promotion Guardrails
- If an ad-hoc object gets reused, exported, or shared across module boundaries,
  replace it with a named type.
- If fields encode domain semantics, promote immediately
  (for example pricing, tax, policy, risk, authorization).
- MUST NOT accept `object`, `Record<string, unknown>`, or `any` for
  domain-shaped data contracts.
- In public APIs, SHOULD prefer named parameter/return types; callers MAY still pass inline literals when structural
  typing permits.

## Runtime Boundary Rules
- TypeScript types do not validate runtime data.
- SHOULD validate untrusted external data at boundaries (HTTP, queue, env, file).
- Convert validated payloads into internal domain types before deeper logic.
- MUST NOT expose transport-layer DTOs as internal domain models by default.

## Nullability and Optionality
- SHOULD keep `null`/`undefined` handling explicit.
- SHOULD avoid non-null assertions (`!`) unless a documented invariant exists.
- SHOULD prefer control-flow narrowing and guard functions over assertions.
- SHOULD use optional properties intentionally; avoid optional fields for required lifecycle states.

## API and Module Design
- SHOULD keep public API signatures stable and explicit.
- SHOULD prefer return types that communicate failure explicitly
  (`Result`-like unions, typed errors) for expected error paths.
- SHOULD avoid large "utility" modules mixing unrelated concerns.
- SHOULD keep module side effects explicit and minimal.

## Naming Conventions
- Variables, parameters, properties, and functions: `camelCase`.
- Types, interfaces, classes, enums, namespaces: `PascalCase`.
- Enum members: `PascalCase` (TypeScript ecosystem convention).
- `const` values:
  use `camelCase` for local/runtime values;
  use `UPPER_SNAKE_CASE` only for shared true constants.
- SHOULD treat abbreviations as one word for casing (`userId`, `httpServer`).

## Enums and Alternatives
- SHOULD prefer union literals (`type Status = "Draft" | "Published"`) when values
  are simple and no runtime enum object is required.
- SHOULD use enums when runtime reflection/iteration or interop requires them.
- SHOULD avoid heterogeneous enums.
- SHOULD prefer explicit string values for externally persisted or serialized enums.

## Error Handling
- SHOULD throw `Error` subclasses with actionable context.
- MUST NOT throw raw strings or untyped objects.
- SHOULD preserve error cause chains when wrapping.
- For async paths, SHOULD ensure rejected promises are observed and handled.

## Decorators and JSDoc Order
- For decorated classes, SHOULD place JSDoc immediately above the top-most decorator.
- SHOULD keep decorators contiguous and directly above the class declaration.
- MUST NOT place JSDoc between a decorator and the class declaration.
- SHOULD use one ordering style consistently across the codebase to avoid formatter and tooling ambiguity.

## Performance and Build Hygiene
- SHOULD avoid unnecessary type-level complexity that harms compile performance.
- SHOULD keep deeply recursive conditional types bounded and documented.
- SHOULD avoid broad barrel exports that cause accidental import bloat.
- SHOULD use `import type` whenever an import is referenced only in type positions.

## High-Risk Pitfalls
1. Using `any` broadly and losing type guarantees.
2. Trusting runtime payload shape from static types alone.
3. Overusing non-null assertions to silence compiler checks.
4. Non-exhaustive union handling with silent default branches.
5. Enum/string mismatch at API boundaries.
6. Type-safe signatures with unsafe internal casts.
7. Leaking framework/transport DTOs into domain core.
8. Letting ad-hoc objects become shared domain contracts without promotion.

## Do / Don't Examples
### 1. `any` vs `unknown` Narrowing
```ts
// Don't: any bypasses type safety.
function parsePayloadBad(payload: any): User {
  return { id: payload.id, name: payload.name };
}

// Do: unknown + explicit narrowing.
function parsePayloadGood(payload: unknown): User {
  if (!isUserPayload(payload)) {
    throw new Error("Invalid user payload");
  }
  return { id: payload.id, name: payload.name };
}
```

### 2. Exhaustive Union Handling
```ts
// Don't: silent default can hide new states.
function renderStatusBad(status: Status): string {
  switch (status.kind) {
    case "loading": return "Loading";
    case "ready": return "Ready";
    default: return "Unknown";
  }
}

// Do: enforce exhaustiveness.
function renderStatusGood(status: Status): string {
  switch (status.kind) {
    case "loading": return "Loading";
    case "ready": return "Ready";
  }
  const _exhaustive: never = status;
  return _exhaustive;
}
```

### 3. Enum Naming Convention
```ts
// Don't: Java-style enum member casing.
enum RetryPolicy {
  NO_RETRY,
  EXPONENTIAL_BACKOFF,
}

// Do: TypeScript-standard PascalCase members.
enum RetryPolicy {
  NoRetry,
  ExponentialBackoff,
}
```

### 4. JSDoc and Decorator Order
```ts
// Don't: mixed ordering around decorated class declarations.
@Injectable()
/** Handles invoice orchestration. */
export class InvoiceServiceBad {}

// Do: put JSDoc above the top-most decorator.
/** Handles invoice orchestration. */
@Injectable()
export class InvoiceServiceGood {}
```

## Code Review Checklist for TypeScript
- Is strict typing preserved without `any` leakage?
- Are untrusted inputs validated at runtime boundaries?
- Are union types handled exhaustively?
- Are null/undefined paths explicit and safe?
- Are casts/assertions minimal and justified?
- Are ad-hoc objects kept local and promoted to named types when they become
  shared or domain-relevant?
- Are naming conventions consistent with TypeScript standards?
- Is JSDoc/decorator ordering for decorated classes consistent with this file?
- Are public types cohesive, stable, and domain-focused?
- Are async error paths typed and handled intentionally?

## Testing Guidance for TypeScript
- Test boundary validators and type guards with invalid inputs.
- Test all union variants and exhaustiveness-sensitive branches.
- Add regression tests for null/undefined edge cases.
- Test serialization/deserialization for enum and literal union values.
- Keep type-checking in CI (`tsc --noEmit` or equivalent) as required quality
  gate.

## VCS Ignore Additions
Add these when using TypeScript (if not already covered by baseline ignore
list):
- `*.tsbuildinfo`
- `dist/`, `out/` when build outputs are generated locally

## Override Notes
- This file narrows JavaScript baseline by enforcing static typing discipline.
- Framework docs MAY add TS framework idioms (for example React props typing),
  but MUST keep strict boundary validation and safe narrowing rules.
