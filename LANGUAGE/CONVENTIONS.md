---
applies_to:
  load: "always"
  annex: "CONVENTIONS.ANNEX.md"
  purpose: "repository-wide conventions that apply before language/framework specializations"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "LANGUAGE/READABILITY.md"]
---
# CONVENTIONS

Guidance for AI agents on cross-language naming and formatting conventions.

## Precedence Model
Formatting and naming decisions MUST follow this order:
1. Language/ecosystem standards and official style rules.
2. Repository conventions in this file.
3. Project-local conventions that do not conflict with 1 or 2.

Rules:
- MUST NOT override established language standards with team preference.
- If multiple style tools exist, MUST choose one canonical formatter/linter path.
- MUST resolve ambiguity by favoring consistency with existing code in the module.

## Formatting Baseline
- MUST use auto-formatters where available; MUST NOT hand-format against tooling.
- SHOULD keep multiline parameter/argument lists when item count is high (typically more than three) or readability
  improves.
- In multiline comma-separated lists, MUST keep one item per line.
- SHOULD use trailing delimiters in multiline lists when language/tooling supports it.
- MUST keep import/group ordering deterministic.
- SHOULD avoid alignment formatting that is fragile under edits.

## Naming Baseline
- SHOULD use English names by default.
- Domain-native non-English terms MAY be used when they are canonical,
  precise, and consistently used.
- SHOULD prefer descriptive names over compressed/cryptic names.
- Names SHOULD express intent and role, not implementation mechanics.
- MUST keep naming consistent within module boundaries.

## Casing Rules (General)
Apply language-standard casing as default:
- Types/class-like constructs: `PascalCase`.
- Variables/functions/methods: follow language/ecosystem standard
  (`camelCase` in Java/JS/TS, `snake_case` in Python/Ruby, etc.).
- True constants: language-standard constant style
  (commonly `UPPER_SNAKE_CASE`, but follow language conventions).
- File/directory casing SHOULD follow ecosystem conventions and existing module
  pattern.

## Abbreviation Policy
- SHOULD avoid abbreviations unless broadly recognized.
- Initialism casing MUST follow the target language/ecosystem style guide.
- When the language style does not mandate all-caps initialisms, MUST treat abbreviations as one word for casing
  (`userId`, `httpClient`, `xmlParser`).
- MUST NOT mix styles for the same identifier family in one codebase.
- SHOULD prefer expanding obscure domain shorthand in public APIs.

## Identifier Quality Rules
- SHOULD prefer semantic/domain types over raw basic types (`String`, numeric types)
  when language/runtime/library support makes that practical.
- Boolean names SHOULD read as predicates (`isActive`, `hasAccess`).
- Collections SHOULD use plural names.
- Temporal values SHOULD prefer temporal types (for example Java `Duration`)
  over primitive numerics when feasible.
- If basic numeric/string fields are still required, MUST keep unit/domain semantics explicit in naming (`timeoutMs`,
  `expiresAt`, `orderId`).
- SHOULD avoid misleading names that imply stronger guarantees than implementation.
- SHOULD avoid generic names (`data`, `result`, `temp`) unless scope is tiny and clear.

Pragmatic exceptions where basic types MAY be required:
- External API/serialization contracts that mandate primitive/string shapes.
- Performance-critical hot paths where domain-wrapper overhead is material.
- Interop boundaries where richer types would add unsafe conversion churn.

## Comment and Documentation Naming
- MUST keep comment terminology aligned with code identifiers.
- MUST rename related comments/docs when renaming key identifiers.
- SHOULD avoid stale terminology drift between code and documentation.

## Testing and Validation Guidance
- MUST keep formatter/linter checks mandatory in CI.
- SHOULD use naming-convention lint rules where ecosystem support exists.
- SHOULD add static checks for import ordering and formatting drift.
- MUST treat style lint failures as quality-gate failures, not optional warnings.
