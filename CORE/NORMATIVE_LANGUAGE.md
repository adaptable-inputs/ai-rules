---
applies_to:
  load: "always"
  annex: "NORMATIVE_LANGUAGE.ANNEX.md"
---
# NORMATIVE_LANGUAGE

Defines the obligation vocabulary used by every rule in this repository. An agent reading any rule MUST be able to tell,
without inference, whether deviating from it is forbidden, discouraged, or permitted.

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
Conversion is complete: every document an agent can load carries explicit keywords, and `KEYWORD_CONVERTED` in
`scripts/check_structure.py` lists them all. CI fails if any of them regains a keyword-less normative statement.

An agent MUST read the remaining keyword-less text as follows:
- Non-imperative prose (headings, explanations, examples) is descriptive and carries no obligation.
- A nested bullet under a lead-in such as "only when all of the following are true:" states a condition, not an
  obligation, and takes no keyword.
- A "Label: value" bullet introduces a list and takes no keyword.
- A bullet in a Scope, Semantic Dependencies, Code Review Checklist, Testing Guidance, or High-Risk Pitfalls section
  states a fact or asks a question. It carries no obligation.

Should a document ever be added without keywords, an imperative bullet in it has `MUST` force. This fallback is
deliberately strict: it preserves the force a rule already carries rather than silently demoting it. It is a safety net,
not a licence to omit keywords.

## Authoring Rules
- Every new or edited normative statement MUST contain exactly one keyword.
- Authors MUST NOT open a normative statement with a bare "prefer", "avoid", "always", "never", "do not", "consider", or
  "where appropriate". Each hides the obligation level.
- "prefer" and "avoid" MAY follow a keyword, where they carry meaning a bare keyword cannot: `SHOULD prefer X over Y`
  expresses a ranked choice, and `SHOULD avoid X` expresses a discouraged-but-legal practice. Neither is a synonym for
  `MUST NOT`.
- `SHOULD` and `SHOULD NOT` MUST be deviable in principle. If deviation is never acceptable, use `MUST` or `MUST NOT`.
- A `SHOULD` deviation MUST be reported in the agent's final summary.

## State the Observable, Not the Mechanism
A requirement names a property that can be observed. Naming a way to achieve it replaces the question "did the property
hold?" with "did you apply the named technique?", and those two answers diverge exactly where the interesting defects
live. A suggested mechanism points at the cases its author thought of, and away from every other.

- A normative statement MUST state the observable property. It MUST NOT name an implementation technique as the
  obligation.
- A mechanism MAY be offered as a non-normative illustration, and MUST then be marked as one. An example inside a `MUST`
  is read as the definition of compliance.
- Where a property is measurable, a requirement SHOULD oblige the measurement rather than a claim about it. "Bounded by
  a constant; measure it at one item and at four, and report both" is verifiable. "Uses a bounded number of queries" is
  a self-assessment.
- An actor's account of its own behaviour MUST NOT be accepted as verification of that behaviour, including when the
  actor is diligent and the account is true.

## Preconditions
A `MUST` binds only where its subject exists. An obligation written as though its subject always exists becomes
unsatisfiable the first time it does not, and an agent then either violates it or quietly ignores it. Both outcomes are
worse than the rule not applying.

- A normative statement whose subject is not universal MUST state the condition under which it binds. "MUST enforce
  authentication at resource boundaries" binds a service that has resource boundaries and non-public data; it says
  nothing useful to one that has neither.
- A `MUST` whose stated precondition does not hold does not apply, and its non-application is not a deviation. Nothing
  is reported, because nothing was skipped.
- An agent that cannot satisfy an applicable `MUST` MUST NOT proceed silently. It MUST report the obligation, the reason
  it cannot be met, and what it did instead, in its final summary.
- A task instruction MUST NOT be read as waiving an applicable `MUST`. If a task and an applicable `MUST` genuinely
  conflict, the rule is defective: resolve by `CORE/RULE_DEPENDENCY_TREE.md` Conflict Resolution Rules, complete the
  task, and report the conflict so the rule can be fixed.
- Authors MUST NOT weaken a `MUST` to a `SHOULD` to escape an unsatisfiable case. State the precondition instead. A
  security control that is mandatory where it applies stays `MUST`.

## Applying Keywords
- Safety, security, and compliance constraints MUST use `MUST` or `MUST NOT`.
- Style and structure guidance SHOULD use `SHOULD` or `SHOULD NOT`.
- Genuine either/or choices SHOULD use `MAY`.

## Conflicts
Conflicts between rules are resolved by [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md). A `MUST` in a broader scope
MUST NOT be weakened to `SHOULD` in a narrower scope without an explicit, documented override.
