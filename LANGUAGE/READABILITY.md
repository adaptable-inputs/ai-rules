---
applies_to:
  load: "always"
---
# READABILITY

Guidance for AI agents on writing code with low cognitive load.

## Scope
- Define readability constraints that apply across languages and frameworks.
- Use this file during implementation and review to reduce defect-prone
  complexity.

## Semantic Dependencies
- Inherit design constraints from `DESIGN/CLEAN_CODE.md` and `DESIGN/SOLID.md`.
- `LANGUAGE/CONVENTIONS.md` is a companion baseline that applies alongside this
  file.
- Language/framework docs MAY specialize patterns but MUST preserve readability
  and explainability constraints.

## Core Principles
- SHOULD optimize for future readers first, then for terse implementation.
- SHOULD prefer explicitness over cleverness.
- SHOULD keep one level of abstraction per function where practical.
- SHOULD make control flow and error flow immediately visible.

## Cognitive Complexity Rules
- SHOULD keep functions focused on one responsibility.
- SHOULD avoid deep nesting; prefer guard clauses and early returns.
- SHOULD split large conditional trees into named predicates or strategy objects.
- SHOULD avoid mixing orchestration, transformation, and IO concerns in one function.
- SHOULD prefer clear linear flow over intertwined branching.
- MUST use `DESIGN/EARLY_RETURN.md` for focused early-return defaults and guardrails.

## Expression and Statement Clarity
- SHOULD avoid cascading ternary expressions.
- For simple two-branch guard mappings, SHOULD prefer a single ternary return or assignment over verbose `if` blocks.
- In ternary guard mappings, SHOULD keep exceptional case first: `condition ? exceptional : happy`.
- SHOULD avoid deeply nested function calls in a single line when intent is unclear.
- SHOULD introduce intermediate variables for non-trivial expressions.
- SHOULD name intermediate values semantically, not mechanically.
- SHOULD keep boolean logic readable; extract complex predicates into named helpers.

## Function and Module Shape
- SHOULD keep function length proportionate to complexity.
- SHOULD keep parameter lists small and coherent; use value objects for grouped concepts.
- SHOULD keep related logic close; avoid jumping across distant utility modules for core business flow.
- SHOULD prefer small cohesive modules over large mixed-responsibility files.

## Comments and Documentation
- SHOULD prefer self-explanatory code over explanatory comments.
- SHOULD use comments for intent, invariants, and non-obvious tradeoffs.
- MUST remove or update comments when code changes.
- SHOULD avoid narrative comments that duplicate code step-by-step.

## Error Path Readability
- SHOULD keep happy path and failure path clearly separated.
- SHOULD use explicit error types/messages that communicate cause and recovery context.
- SHOULD avoid broad error-handling blocks that hide control flow outcomes.

## High-Risk Pitfalls
1. Deeply nested conditionals obscuring business intent.
2. Functions performing multiple unrelated responsibilities.
3. Dense one-liners hiding side effects and null/error handling.
4. Placeholder naming (`data`, `obj`, `tmp`) masking domain meaning.
5. Comments that drift from behavior and become misleading.
6. Boolean flags controlling unrelated behavior branches.
7. Refactors that shrink lines but increase cognitive load.
8. Ternary guard expressions that place happy-path first and hide exceptional
   behavior.

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
- Does each function do exactly one thing, and fit on one screen without
  scrolling?
- Are nested branches and boolean expressions easy to follow?
- For simple guard mappings, does ternary keep exceptional case first
  (`condition ? exceptional : happy`)?
- Are names meaningful and domain-specific?
- Are comments useful, current, and non-redundant?
- Are error paths explicit and readable?
- Were abstractions introduced to reduce, not increase, cognitive load?

## Testing Guidance for Readability-Driven Changes
- Add focused regression tests before readability refactors that alter control
  flow.
- Ensure tests cover both happy path and failure path behavior.
- Keep test names behavior-oriented to mirror readability expectations.
- Validate that extraction/refactor steps did not alter side effects.

## Override Notes
- Language/framework docs MAY define local idioms (for example React hooks,
  Java stream style) but SHOULD still satisfy these readability constraints.
