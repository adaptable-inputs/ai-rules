---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# The experimenter was the variable

A benchmark compared two rulesets by the tokens an agent spent producing the same program under each. The headline was
that the fork cost 2.6x less. The headline was an artefact of how the arms were prompted. The rule extracted from this
is in `TEST/WITHHELD_SUITES.md`, "Run Conditions".

## What happened

Upstream's `PROGRAMMING.md` orders an exhaustive read of every file reachable from `AI.md`. Three clean runs, same
ruleset, same task, same model:

| prompt instruction | files read | tokens |
|---|---:|---:|
| "Obey it. Read them all, as your ruleset requires" | 124 / 124 | 444,627 |
| "Obey your ruleset" | 24 / 124 | 194,654 |
| "Obey your ruleset" | 24 / 124 | 171,236 |

The first prompt told the agent to read everything. The other two did not, and both agents hand-picked about 24
documents, judging the rest irrelevant to a Java service. The 2.6x gap was not the ruleset. It was the sentence the
experimenter added to one arm's task and not to the others.

## What generalises

- Compliance with the instruction under test is a variable to measure, not an assumption to build on. Record how much of
  the ruleset each subject actually read, and report that variance before any ratio drawn from it.
- Every arm of a comparison gets the same task text, differing only in which ruleset and workspace it names. A
  difference in the prompt is a difference in the treatment.
- A ruleset's *instruction* and an agent's *behaviour* are separate measurements. Upstream instructs a 110,442-token
  read; agents left to themselves pay about a quarter of that. Both facts are true and neither substitutes for the
  other.
- The deterministic measurement -- what each ruleset makes an agent read, computed from its own loading protocol -- has
  no such confound, and is the number that survives.

## Cost of not doing this

The benchmark ran to completion, passed every gate, and produced a number that would have been quoted. It measured a
sentence in the experimenter's prompt.
