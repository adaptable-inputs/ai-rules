---
applies_to:
  load: "annex"
  annex_of: "JAVASCRIPT.md"
  tasks: ["review", "test"]
---
# JAVASCRIPT - Annex

## High-Risk Pitfalls
1. Unhandled promise rejections causing hidden failures.
2. Trusting external payload shape without validation.
3. Mutating shared objects across module boundaries.
4. Using `==`/`!=` and relying on coercion side effects.
5. Silent catch blocks that drop operational failures.
6. Fire-and-forget async tasks without cancellation/logging.
7. Mixing CommonJS and ESM inconsistently in one package.

## Do / Don't Examples
### 1. Promise Rejection Handling
```js
// Don't: unhandled rejection.
function saveUserBad(user) {
  db.write(user);
}

// Do: await and handle failure with context.
async function saveUserGood(user) {
  try {
    await db.write(user);
  } catch (error) {
    logger.error("user.save.failed", { userId: user.id, error });
    const wrappedError = new Error(`Failed to save user ${user.id}`, {
      cause: error,
    });
    if (wrappedError.cause === undefined) {
      wrappedError.cause = error;
    }
    throw wrappedError;
  }
}
```

### 2. Boundary Validation
```js
// Don't: trust request body shape.
function createInvoiceBad(req) {
  return invoiceService.create(req.body.amount, req.body.currency);
}

// Do: validate and normalize at boundary.
function createInvoiceGood(req) {
  const payload = validateInvoiceRequest(req.body);
  return invoiceService.create(payload.amount, payload.currency);
}
```

### 3. Shared Mutation
```js
// Don't: mutate imported/shared state.
settings.timeoutMs = 5000;

// Do: create explicit derived config.
const runtimeSettings = { ...settings, timeoutMs: 5000 };
```

## Code Review Checklist for JavaScript
- Are all external inputs validated at boundaries?
- Are promise rejections handled for all async operations?
- Is error handling explicit, contextual, and non-silent?
- Is module state mutation controlled and intentional?
- Are `===`/`!==` used consistently?
- Are side effects isolated from pure domain logic?
- Are there event-loop blocking operations on hot paths?
- Are security-sensitive APIs (`eval`, shell exec, dynamic code paths) avoided or tightly controlled?

## Testing Guidance for JavaScript
- Test boundary validators with valid, invalid, and malicious payloads.
- Test async failure paths, including timeout/cancellation behavior.
- Test concurrency behavior for multi-promise flows.
- Test mutation-sensitive logic for unintended shared-state side effects.
- Add regression tests for previously observed runtime edge cases.
