---
applies_to:
  load: "conditional"
  when: "the change adds or modifies a checker, linter, CI gate, pre-commit hook, or any test that certifies other work"
  purpose: "rules a guard must obey, because a guard is trusted more than the code it inspects"
  inherits: ["TEST/TEST.md"]
---
# GUARDS

Rules for code that certifies other code.

## Defaults
A guard is a checker, a linter, a CI gate, a pre-commit hook, or a test that certifies other work. Guards are trusted
more than the code they inspect and reviewed less, so they MUST meet every standard they impose.

- A guard MUST be covered by a test that fails when the guard is removed or weakened. An uncovered guard is an assertion
  that it works.
- A guard MUST NOT exempt itself from the project's coding standard, review, or coverage requirements. If a standard
  does not fit the guard, MUST change the standard or the guard, and MUST NOT silently exclude it.
- A guard's own failure MUST be loud. It MUST exit non-zero, MUST name what it inspected, and MUST report how many items
  it inspected, so that "checked nothing" and "found nothing" are distinguishable in its output.
- A guard MUST refuse to run rather than report success, when its inputs are missing, empty, or unreadable.
- A guard MUST fail on a stale exemption. An allowlist entry whose target no longer exists, or no longer violates, is
  cover for the next one.
- Every exemption a guard grants MUST name what it exempts and state why the check cannot apply. An exemption without a
  justification is an unchecked case with a nicer name.

## Recursion Terminates at Depth Two
"A guard MUST be covered by a test" invites an infinite regress: who guards the guard's test? The regress MUST be cut,
and cut deliberately, because each level costs real effort and returns less than the one below it.

The three levels, and no more:

1. **Code.** Tested by a suite.
2. **A guard** (checker, linter, CI gate, hook, or a test that certifies other work). Covered by a test that fails when
   the guard is removed or weakened.
3. **A guard's test.** Terminates the recursion. It MUST be mutation-verified once, by hand: inject the defect, watch
   the test fail, restore, watch it pass. That observation is the evidence.

- MUST NOT write a test whose only subject is another guard's test. Depth three adds no information: a meta-test that a
  meta-test exists is satisfied by a file that asserts `True`.
- A guard's test MUST be mutation-verified before it is relied on, and the mutation MUST be recorded in the test's name
  or docstring, so the evidence survives the person who produced it.
- Where the terminating observation cannot be automated, MUST record it in the commit that introduces the guard, naming
  the defect injected and the failure observed.
- MUST NOT treat depth as a substitute for evidence. One guard's test, seen to fail, is worth more than three layers
  none of which has ever been red.
