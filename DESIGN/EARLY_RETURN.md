---
applies_to:
  load: "always"
  annex: "EARLY_RETURN.ANNEX.md"
---
# EARLY_RETURN

Guidance for AI agents to use early return and guard clauses effectively.

## Scope
- Define when early return is the preferred control-flow style.
- Apply during implementation, refactoring, and review across languages.
- Use this file with readability and clean-code guidance, not as isolated style
  dogma.

## Semantic Dependencies
- Inherit baseline precedence rules from `CORE/RULE_DEPENDENCY_TREE.md`.
- Inherit naming/readability constraints from `LANGUAGE/READABILITY.md`.
- Inherit function cohesion constraints from `DESIGN/CLEAN_CODE.md` and
  `DESIGN/SOLID.md`.

## Defaults and Guardrails
- SHOULD prefer early return/guard clauses to keep the happy path linear.
- MUST validate inputs and preconditions early; on invalid or error states, return (or exit) immediately.
- SHOULD reduce nested branching depth before extracting deeper abstractions.
- SHOULD keep guard clauses small and intent-revealing.
- SHOULD keep return points semantically obvious, and SHOULD NOT scatter
  unrelated exits.
- For simple two-branch value selection with no side effects, SHOULD prefer a single ternary expression for
  return/assignment instead of verbose `if` blocks.
- In ternary guard expressions, SHOULD keep the exceptional case first: `condition ? exceptional : happy` (for example
  `value == null ? null : map(value)`).

Use early return carefully when control-flow exits could bypass critical
cleanup/consistency behavior:
- resource lifecycle obligations,
- transactional boundary guarantees,
- required audit/logging side effects.

Modern language/runtime features (for example structured cleanup constructs,
GC-managed memory, and scoped APIs) reduce these risks in many cases. Treat
early return as the default, and treat caveats as exceptions to check.

## Override Notes
- Language/framework docs MAY narrow early-return style for specific paradigms,
  but SHOULD keep the default preference for reduced nesting and explicit flow.
