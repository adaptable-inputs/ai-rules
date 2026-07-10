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
- MUST confirm the guard reports what it claims. A quiet flag that suppresses the test summary, a severity threshold no
  emitted finding reaches, and a crashed sub-process whose exit code reads as "no findings" each report success over a
  real defect.
- When a guard is fixed, MUST add the reproducing test in the same change, named after the defect that shipped.

## A Guard Does Not Choose What It Inspects
A guard that discovers its own subjects will one day discover none, and its output will not say so. Discovery is where a
guard goes quietly blind: the names it searches for go stale, the directory it looks in moves, and an empty result is
indistinguishable from a clean one.

- A guard MUST take the set it inspects as an input. It MUST NOT infer that set from its own location, from hardcoded
  names, or from a search of the filesystem.
- A guard MUST fail when the set it was given is empty, and MUST NOT treat an empty set as a clean one.
- A guard MUST distinguish "the subject is missing", "the subject is empty", and "the subject is clean". These MUST NOT
  share a return value.
- A guard MUST report the size of what it inspected alongside its verdict. "Passed" is true of an audit that scanned
  nothing; "passed over 3 files" is not.
- MUST NOT keep a second copy of a guard. Two copies double the places its defect can live and do not double its review.

## Every Channel Carries Its Own Defect Case
A guard with more than one input needs a defect case for each. Coverage of one channel reads as coverage of the guard,
and the channel nobody tests is the one that rots, because nothing is watching it.

- For each distinct input a guard inspects, MUST write a test that plants a defect in *that* input and observe the guard
  reject it. A guard with two channels and three tests against one channel is untested on the other.
- A verification channel MUST be independent of the artefact it verifies. Where the subject can place the evidence into
  the record the guard reads, the guard agrees with the subject by construction. Match against what a tool *did*, not
  against what its output *contains*.
- Where a channel cannot be exact, it MUST err toward a false alarm rather than a false clearance. An undercount
  surfaces as a disagreement someone investigates; a silent agreement surfaces as nothing.
- Unanimity across independent runs MUST be treated as a reason to check the instrument, not as a result. Repeated
  identical readings are what a gauge stuck on one value produces.

## A Guard's Test Asserts the Reason, Not the Exit Code
A guard that dies on a typo, a missing file, or an unrecognised argument exits non-zero, exactly as a guard that caught
the defect does. A test that asserts only the exit code cannot tell them apart, and will certify a guard that never ran.

- A test of a guard MUST assert the reason the guard gives, not merely that it failed. Match the message, the finding,
  or the named subject.
- A test of a guard MUST build the state it needs. A test that passes because of ambient repository, environment, or
  filesystem state is a test of that state, and it fails on the first day the repository is correct.
- A guard MUST be exercised on clean input as well as on a defect. A guard that cannot say yes will be switched off, and
  a guard never seen to say yes has never shown that it can.

## An Omitted Check Must Be Declared, Not Assumed
A safety check that can be left off is off in exactly the situation nobody considered. The omission MUST be an
assertion, not a default.

- Where a guard accepts an optional subject, omitting it MUST be a failure unless its absence is asserted explicitly.
  Supplying neither the subject nor the assertion MUST NOT read as "there was none".
- Supplying both the subject and the assertion of its absence MUST be refused as a contradiction.
- MUST NOT add a safety check as an opt-in flag to spare existing callers. Update the callers.

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
