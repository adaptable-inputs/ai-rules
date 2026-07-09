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
