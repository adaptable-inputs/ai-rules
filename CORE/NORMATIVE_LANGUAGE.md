---
applies_to:
  load: "always"
  annex: "NORMATIVE_LANGUAGE.ANNEX.md"
---
# NORMATIVE_LANGUAGE

Defines the obligation vocabulary used by every rule in this repository. An
agent reading any rule MUST be able to tell, without inference, whether
deviating from it is forbidden, discouraged, or permitted.

## Keywords
Keywords are written in uppercase. Their meaning follows RFC 2119.

| Keyword | Meaning | May an agent deviate? |
| --- | --- | --- |
| `MUST` | Absolute requirement. | No. |
| `MUST NOT` | Absolute prohibition. | No. |
| `SHOULD` | Strong recommendation. | Only with a stated reason. |
| `SHOULD NOT` | Strong recommendation against. | Only with a stated reason. |
| `MAY` | Genuinely optional. | Yes, freely. |

## Reading Statements Without a Keyword
Conversion is complete: every document an agent can load carries explicit
keywords, and `KEYWORD_CONVERTED` in `scripts/check_structure.py` lists them all.
CI fails if any of them regains a keyword-less normative statement.

An agent MUST read the remaining keyword-less text as follows:
- Non-imperative prose (headings, explanations, examples) is descriptive and
  carries no obligation.
- A nested bullet under a lead-in such as "only when all of the following are
  true:" states a condition, not an obligation, and takes no keyword.
- A "Label: value" bullet introduces a list and takes no keyword.
- A bullet in a Scope, Semantic Dependencies, Code Review Checklist, Testing
  Guidance, or High-Risk Pitfalls section states a fact or asks a question. It
  carries no obligation.

Should a document ever be added without keywords, an imperative bullet in it has
`MUST` force. This fallback is deliberately strict: it preserves the force a
rule already carries rather than silently demoting it. It is a safety net, not a
licence to omit keywords.

## Authoring Rules
- Every new or edited normative statement MUST contain exactly one keyword.
- Authors MUST NOT open a normative statement with a bare "prefer", "avoid",
  "always", "never", "do not", "consider", or "where appropriate". Each hides
  the obligation level.
- "prefer" and "avoid" MAY follow a keyword, where they carry meaning a bare
  keyword cannot: `SHOULD prefer X over Y` expresses a ranked choice, and
  `SHOULD avoid X` expresses a discouraged-but-legal practice. Neither is a
  synonym for `MUST NOT`.
- `SHOULD` and `SHOULD NOT` MUST be deviable in principle. If deviation is never
  acceptable, use `MUST` or `MUST NOT`.
- A `SHOULD` deviation MUST be reported in the agent's final summary.

## Applying Keywords
- Safety, security, and compliance constraints MUST use `MUST` or `MUST NOT`.
- Style and structure guidance SHOULD use `SHOULD` or `SHOULD NOT`.
- Genuine either/or choices SHOULD use `MAY`.

## Conflicts
Conflicts between rules are resolved by
[RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md). A `MUST` in a broader scope
MUST NOT be weakened to `SHOULD` in a narrower scope without an explicit,
documented override.
