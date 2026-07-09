---
applies_to:
  load: "annex"
  annex_of: "EARLY_RETURN.md"
  tasks: ["review", "test"]
---
# EARLY_RETURN - Annex

## High-Risk Pitfalls
1. Deeply nested condition trees when guard clauses would make intent obvious.
2. Early exits with vague predicates that hide why execution stops.
3. Multiple exits that duplicate side effects in inconsistent ways.
4. Adding guard clauses without tests for changed control-flow paths.
5. Avoiding early return dogmatically and keeping unnecessary nesting.
6. Keeping trivial guard-return/guard-assignment logic as multi-line branching when a single ternary expression is
   clearer.
7. Reversing ternary guard order (`happy` first) and hiding the exceptional path.

## Do / Don't Examples
### 1. Guard Clauses over Nested Blocks
```text
Don't:
// Happy path is buried inside multiple nested checks.
if (isValid(request)) {
  if (hasActiveSession(user)) {
    if (!isTokenExpired(token)) {
      process(request);
    }
  }
}

Do:
// Fail fast on invalid or unauthorized states; keep happy path linear.
if (!isValid(request)) return;
if (!hasActiveSession(user)) return;
if (isTokenExpired(token)) return;
process(request);
```

### 2. Keep Shared Side Effects Explicit
```text
Don't: duplicate audit/log side effects in each return branch.
Do:    keep mandatory side effects in one explicit place before return,
       or enforce them with structured constructs.
```

### 3. Predicate Clarity
```text
Don't: if (x) return;
Do:    if (isRateLimitExceeded(user)) return;
```

### 4. Ternary Return for Guard Mapping
```text
Don't:
if (value == null) return null;
return map(value);

Don't:
return value != null ? map(value) : null;

Do:
return value == null ? null : map(value);
```

### 5. Ternary Assignment for Guard Mapping
```text
Don't:
if (value == null) {
  target = null;
  return;
}
target = map(value);

Do:
target = value == null ? null : map(value);
```

## Code Review Checklist for Early Return
- Does early return reduce nesting and improve linear readability?
- Are guard predicates explicit and semantically named?
- Are mandatory cleanup/transaction/audit effects still guaranteed?
- Is the happy path easier to understand in one pass?
- For simple guard mappings, is ternary used for return/assignment with exceptional case first
  (`condition ? exceptional : happy`)?
- Were tests updated for changed control-flow branches?

## Testing Guidance
- Add tests for each guard-clause exit path introduced or changed.
- Keep at least one explicit happy-path test per refactored method.
- For cleanup-sensitive code, add tests that prove required effects still run.
- For transactional code, test rollback/commit semantics after refactoring.
- When refactoring guard `if` blocks into ternary return/assignment, test both exceptional and happy outcomes.
