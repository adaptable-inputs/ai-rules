---
applies_to:
  load: "always"
  annex: "EARLY_RETURN.ANNEX.md"
  purpose: "when early return is the preferred control-flow style"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "LANGUAGE/READABILITY.md", "DESIGN/CLEAN_CODE.md", "DESIGN/SOLID.md"]
---
# EARLY_RETURN

Guidance for AI agents to use early return and guard clauses effectively.

## Defaults and Guardrails
- SHOULD prefer early return/guard clauses to keep the happy path linear.
- MUST validate inputs and preconditions early; on invalid or error states, return (or exit) immediately.
- SHOULD reduce nested branching depth before extracting deeper abstractions.
- SHOULD keep guard clauses small and intent-revealing.
- SHOULD keep return points semantically obvious, and SHOULD NOT scatter unrelated exits.
- For simple two-branch value selection with no side effects, SHOULD prefer a single ternary expression for
  return/assignment instead of verbose `if` blocks.
- In ternary guard expressions, SHOULD keep the exceptional case first: `condition ? exceptional : happy`
  (for example `value == null ? null : map(value)`).

Use early return carefully when control-flow exits could bypass critical cleanup/consistency behavior:
- resource lifecycle obligations,
- transactional boundary guarantees,
- required audit/logging side effects.

Modern language/runtime features (for example structured cleanup constructs, GC-managed memory, and scoped APIs) reduce
these risks in many cases. Treat early return as the default, and treat caveats as exceptions to check.
