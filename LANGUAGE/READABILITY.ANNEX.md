---
applies_to:
  load: "annex"
  annex_of: "READABILITY.md"
  tasks: ["review", "test"]
---
# READABILITY - Annex

## High-Risk Pitfalls
1. Deeply nested conditionals obscuring business intent.
2. Functions performing multiple unrelated responsibilities.
3. Dense one-liners hiding side effects and null/error handling.
4. Placeholder naming (`data`, `obj`, `tmp`) masking domain meaning.
5. Comments that drift from behavior and become misleading.
6. Boolean flags controlling unrelated behavior branches.
7. Refactors that shrink lines but increase cognitive load.
8. Ternary guard expressions that place happy-path first and hide exceptional behavior.

## Do / Don't Examples
### 1. Guard Clauses over Nested Blocks
```text
Don't:
if (isValid(request)) {
  if (isAuthorized(user)) {
    if (!isExpired(token)) {
      process(request);
    }
  }
}

Do:
if (!isValid(request)) return;
if (!isAuthorized(user)) return;
if (isExpired(token)) return;
process(request);
```

### 2. Named Intermediate Values
```text
Don't: send(a(b(c(input))));
Do:    const normalized = normalize(input);
       const enriched = enrich(normalized);
       send(enriched);
```

### 3. Avoid Cascading Ternary
```text
Don't: status = a ? "A" : b ? "B" : c ? "C" : "D";
Do:    use explicit if/switch with named intent.
```

### 4. Guard Mapping with Ternary
```text
Don't:
if (value == null) return null;
return map(value);

Don't:
result = value != null ? map(value) : null;

Do:
return value == null ? null : map(value);
result = value == null ? null : map(value);
```

## Code Review Checklist for Readability
- Is the main execution flow understandable in one pass?
- Does each function do exactly one thing, and fit on one screen without scrolling?
- Are nested branches and boolean expressions easy to follow?
- For simple guard mappings, does ternary keep exceptional case first (`condition ? exceptional : happy`)?
- Are names meaningful and domain-specific?
- Are comments useful, current, and non-redundant?
- Are error paths explicit and readable?
- Were abstractions introduced to reduce, not increase, cognitive load?

## Testing Guidance for Readability-Driven Changes
- Add focused regression tests before readability refactors that alter control flow.
- Ensure tests cover both happy path and failure path behavior.
- Keep test names behavior-oriented to mirror readability expectations.
- Validate that extraction/refactor steps did not alter side effects.
