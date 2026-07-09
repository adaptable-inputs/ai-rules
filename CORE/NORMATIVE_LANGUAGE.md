---
applies_to:
  load: "always"
---
# NORMATIVE_LANGUAGE

Defines the obligation vocabulary used by every rule in this repository. An
agent reading any rule must be able to tell, without inference, whether
deviating from it is forbidden, discouraged, or permitted.

## Scope
- Applies to every normative statement in the ruleset.
- Does not apply to prose that describes, explains, or gives examples.

## Keywords
Keywords are written in uppercase. Their meaning follows RFC 2119.

| Keyword | Meaning | May an agent deviate? |
| --- | --- | --- |
| `MUST` | Absolute requirement. | No. |
| `MUST NOT` | Absolute prohibition. | No. |
| `SHOULD` | Strong recommendation. | Only with a stated reason. |
| `SHOULD NOT` | Strong recommendation against. | Only with a stated reason. |
| `MAY` | Genuinely optional. | Yes, freely. |

## Default Force
Not every statement in this repository carries a keyword yet. Until conversion
is complete, an agent MUST read them as follows:
- An imperative bullet with no keyword has `MUST` force. "Use dedicated feature
  branches" is a requirement, not a suggestion.
- Non-imperative prose (headings, explanations, examples) is descriptive and
  carries no obligation.
- A nested bullet under a lead-in such as "only when all of the following are
  true:" states a condition, not an obligation, and takes no keyword.

Documents that have completed conversion are listed in `KEYWORD_CONVERTED` in
`scripts/check_structure.py`. CI fails if one of them regains a keyword-less
normative statement. That list only grows; the default above governs everything
not yet on it.

This default is deliberately strict: it preserves the force these rules already
had before keywords were introduced. It is a migration aid, not a licence to
omit keywords.

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

## Do / Don't Examples
### 1. Obligation Level
```text
Don't: Prefer constructor injection.
Do:    SHOULD prefer constructor injection over field injection.
```

### 2. Absolute Prohibition
```text
Don't: Never push directly to protected branches.
Do:    MUST NOT push directly to protected branches.
```

### 3. Genuine Option
```text
Don't: Use a BOM where appropriate.
Do:    MAY centralize versions with a BOM when more than one module depends on
       the same artifact.
```
