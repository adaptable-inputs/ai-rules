---
applies_to:
  load: "always"
  annex: "TEST.ANNEX.md"
  inherits: ["CORE/CORE.md", "CORE/RULE_DEPENDENCY_TREE.md"]
---
# TEST

Guidance for AI agents implementing, updating, and reviewing tests.

## Testing Defaults
- MUST add or update tests for every behavior change, unless a withheld suite the author is forbidden to see covers that
  change; see "Withheld Verification Suites". The obligation is that the change is tested, not that its author writes
  the test.
- SHOULD prefer deterministic and isolated tests.
- SHOULD keep test suites fast enough for frequent CI execution.
- MUST use risk-based depth: higher business/security impact requires stronger test coverage across layers.

## Test Strategy by Layer
- Unit tests:
  - SHOULD be the default first choice for business logic.
  - MUST be fast, isolated, and behavior-focused.
- Integration tests:
  - MUST be used for boundaries (DB, queues, file systems, external services).
  - MUST validate wiring, contracts, and transactional behavior.
- End-to-end tests:
  - MUST cover critical user/value flows only.
  - MUST keep suite small, stable, and non-flaky.

## Determinism and Flakiness Control
- SHOULD avoid reliance on wall-clock time, random seeds, network timing, and shared mutable state without explicit
  control.
- MUST use stable fixtures and explicit setup/teardown.
- SHOULD control time/randomness with test doubles where feasible.
- MUST quarantine and fix flaky tests; do not normalize flaky behavior as acceptable.

## Mocks, Stubs, and Fakes
- MUST mock boundaries, not core behavior under test.
- SHOULD avoid over-mocking that hides integration risks.
- SHOULD use fakes/stubs for dependencies that are slow, non-deterministic, or unavailable in the test environment.
- MUST reset shared test doubles between tests to avoid cross-test coupling.

## Data and Fixtures
- MUST keep fixtures in test-only paths.
- MUST NOT ship test fixtures in production artifacts.
- SHOULD prefer minimal fixture data that expresses intent clearly.
- SHOULD use scenario-based datasets for edge and failure-path coverage.

## Coverage and Confidence
- High line coverage alone is insufficient; MUST prioritize meaningful assertions and branch/error-path validation.
- MUST cover happy paths, edge cases, failure modes, and regression paths.
- If coverage targets are not met, MUST document exact gaps and risk rationale.

## Tests Are Derived From Requirements
A test written from the code asserts what the code does. A test written from the requirement asserts what was asked for.
Only the second can fail in a way that matters, and only the second reveals a requirement nobody implemented.

- Every functional test MUST derive from a stated requirement, and MUST name it: the requirement identifier in the test
  name, or in a comment on the test.
- Every stated requirement MUST have at least one test that names it. A requirement with no naming test MUST fail the
  build; it is a requirement nobody implemented, or a test nobody wrote.
- A test MUST NOT assert behaviour the requirements do not state. Asserting more than was asked punishes an
  implementation for a choice it was never given, and the test then measures the test author's taste.
- Before writing tests, MUST read the requirements for gaps: behaviour the specification leaves undefined, an error path
  with no stated status, an ordering with no stated tie-break, a boundary with no stated side.
- On finding a gap, MUST report it and MUST request confirmation before adding a requirement or any test derived from
  one. MUST NOT invent a requirement, and MUST NOT quietly test the behaviour the implementation happens to have.
- Where a gap is left open by decision, MUST record it in the requirements as a known gap, naming what is undefined and
  what the implementations currently do. An undefined behaviour that is written down is a decision; one that is not is a
  trap.

## The Second Verification Pass
One pass tells you a thing agrees with itself. A guard that checks its own output, a formatter that validates its own
rewrite, an agent that reports its own compliance: each is a closed loop, and a closed loop cannot detect the error it
is made of.

- Work MUST be verified twice, and the second pass MUST observe through a different channel from the first. Re-running
  the same command proves determinism, not correctness.
- The second pass MUST NOT share a code path, a parser, or an assumption with the first. Where the first reads a report,
  the second reads the artifact. Where the first calls a method, the second drives the interface. Where the first trusts
  a self-report, the second reads the record.
- The second pass MUST run after the work is declared complete, from a clean state, on what was actually produced rather
  than on what was intended.
- An actor's account of its own behaviour MUST NOT be accepted as a verification of that behaviour. It is a claim, and
  the record is the evidence. Where the two disagree, the record governs.
- MUST record what each pass observed, separately. "Verified" without naming the two observations is one pass wearing a
  second name.
- Where a second channel does not exist, MUST build one, or MUST state plainly that the property is unverified. An
  unverifiable claim MUST NOT be reported as verified.

## Bounded Correction
A failed verification MUST be acted on, and the acting MUST be bounded. An unbounded retry loop mistakes persistence for
progress: it will keep changing code until the check passes, and a check that passes after enough undirected edits has
stopped verifying anything.

- On a failed verification, MUST attempt to correct the defect rather than restate the failure. Reporting a red test
  without acting on it leaves the work unfinished.
- Each attempt MUST begin with a stated hypothesis about the cause, and MUST change what that hypothesis implicates.
  MUST NOT retry the same change, and MUST NOT alter the check to make it pass.
- After each attempt, MUST re-verify through the independent channel that found the defect, not through the change
  itself. See "The Second Verification Pass".
- MUST make at most three attempts. After the third, MUST stop, MUST report the defect, the three hypotheses, what each
  attempt changed, and what the independent channel observed after each.
- MUST NOT weaken, skip, or delete the failing check to end the loop. A check removed to make a build green is a defect
  promoted to a policy.
- Where an attempt makes the failure worse, or reveals that the specification is silent on the behaviour under test,
  MUST stop before exhausting the three and MUST report that instead. Attempts are a budget, not a quota.

## Coverage Exclusions
Full coverage of production code is the target. Where a unit genuinely cannot be reached, the gap MUST be named and
justified, never absorbed. A threshold that tolerates a percentage of uncovered code stops naming which code that is,
and the exclusion review is the step most easily skipped once the number looks acceptable.

- Every uncovered unit MUST carry an exclusion that names it and states why the check cannot apply. An uncovered unit
  with no exclusion MUST fail the build.
- An exclusion MUST assert one of exactly two things: that no input can reach the unit, or that only a framework reaches
  it reflectively and the system fails without it. Any other reason is an admission the unit is untested.
- A framework-reflective exclusion MUST cite the evidence that produced it. Remove the unit, run the system, record what
  broke. An untested claim that a persistence provider needs an accessor is a guess.
- The exclusion set MUST be validated on every run, before any result derived from coverage is accepted. Validation MUST
  fail closed: a malformed, empty, or unjustified entry stops the run rather than excusing the unit.
- MUST fail on a stale exclusion, one whose unit is now covered or no longer exists. A list that only grows becomes
  where uncovered code hides.
- Exclusions MUST be scoped to the subject they describe. One list shared across several implementations makes a valid
  exclusion look stale and a stale one look valid.
- MUST NOT raise a coverage threshold, widen a pattern, or delete an assertion to make an uncovered unit disappear.
  Cover it, exclude it with a reason, or delete the unit.
- Unreachable production code MUST be deleted rather than excluded. A gap that a deletion would close is not an
  infeasibility.

## Verifying the Tests Themselves
A test that cannot fail is worse than no test, because it is trusted. A green result never seen fail is not evidence.

- MUST observe every new test or checker failing on the defect it exists to catch, before relying on it. Inject the
  defect, watch the guard reject it, then restore.
- A verification MUST fail closed. Absence of a report, a summary, or a finding is a failure, not a pass. MUST require a
  positive success signal, and MUST NOT infer success from the absence of complaints.
- MUST confirm the tool reports what it claims. A quiet flag that suppresses the test summary, a severity threshold no
  emitted finding reaches, and a crashed sub-process whose exit code reads as "no findings" each report success over a
  real defect.
- A test MUST assert the contract, not one way of satisfying it. If two conforming implementations differ, the test MUST
  accept both.
- If the correctness of a test is uncertain, MUST validate it against a purpose-built reference: a minimal
  implementation that conforms, and one that violates the rule under test. The test MUST pass the first and fail the
  second. MUST NOT settle the question by reasoning about the test alone.
- MUST NOT locate the code under test by reflective search over names the contract does not fix. A named surface turns a
  missing operation into a compile error; a reflective lookup turns it into a silent pass.
- When a checker is fixed, MUST add the reproducing test in the same change, named after the defect that shipped.

## Traceability
An untraced test proves nothing about the requirement it was meant to cover, and an untraced requirement is one nobody
noticed was never implemented. The mapping MUST be explicit and MUST be checked, because a mapping held only in a
reviewer's head decays on the first rename.

- Every test MUST name what it verifies: the requirement identifier, the rule, or the guard it exercises. A test whose
  subject is not stated cannot be shown to be missing.
- Every functional requirement MUST be reachable from at least one test that names it. A requirement with no naming test
  MUST fail the build, not wait for a reviewer to notice.
- Every guard MUST be named by a test that exercises it, and MUST be invoked from the entry point that runs the guards.
  A guard that is defined but never called cannot fail.
- The traceability check MUST itself be automated and MUST fail closed. Traceability asserted in a document, and not
  enforced by a check, is a claim about the past.
- When a requirement is removed, its tests MUST be removed in the same change. A test that traces to nothing is either
  dead or evidence the requirement still exists.

## CI and Reporting Expectations
- MUST run relevant tests before opening a PR.
- MUST report what was executed and what was not.
- In CI, MUST fail builds on test failures.
- MUST treat a missing or empty test report as a build failure, never as a passing run with nothing to say.
- SHOULD publish actionable reports/artifacts for failed runs when available.

## Validation Notes for Delivery
When delivering a change, include:
- Tests executed (unit/integration/e2e).
- Key manual checks (if applicable).
- Known test gaps and risk justification.
- Follow-up issue references for deferred test debt.

## Override Notes
- Security-sensitive scenarios MUST also satisfy `SECURITY/SECURITY.md`.

## Files
- [GUARDS.md](GUARDS.md) - Obligations on a checker, linter, or CI gate.
- [WITHHELD_SUITES.md](WITHHELD_SUITES.md) - Isolation of a suite withheld from the author.
