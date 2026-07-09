---
applies_to:
  load: "annex"
  annex_of: "TYPESCRIPT.md"
  tasks: ["review", "test"]
---
# TYPESCRIPT - Annex

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
