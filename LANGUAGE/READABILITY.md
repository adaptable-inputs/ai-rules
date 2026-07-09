---
applies_to:
  load: "always"
  annex: "READABILITY.ANNEX.md"
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

## Override Notes
- Language/framework docs MAY define local idioms (for example React hooks,
  Java stream style) but SHOULD still satisfy these readability constraints.
