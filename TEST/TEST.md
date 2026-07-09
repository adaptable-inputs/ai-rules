---
applies_to:
  load: "always"
  annex: "TEST.ANNEX.md"
  inherits: ["CORE/CORE.md", "CORE/RULE_DEPENDENCY_TREE.md"]
---
# TEST

Guidance for AI agents implementing, updating, and reviewing tests.

## Testing Defaults
- MUST add or update tests for every behavior change.
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

## Guards Are Code, and Obey These Rules
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

## Withheld Verification Suites
Applies when a suite certifies work whose author MUST NOT see it: a benchmark arm, an evaluation, an acceptance suite
written by another party. An author who sees the suite implements its assertions instead of the specification, and the
suite then certifies nothing.

- A withheld suite MUST be absent from the author's workspace at every moment the author is working, not merely
  unmentioned. Presence is exposure.
- MUST run the suite against a copy of the author's work, never in the author's tree. An artifact left behind after one
  run is still present during the next.
- MUST treat a toolchain diagnostic that names the suite as exposure. A compiler error quoting a test's path and a
  missing symbol discloses the contract as surely as reading the file does.
- The specification MUST name every operation the suite calls. Otherwise the author cannot compile against a suite it is
  forbidden to read, and the pressure to look is structural rather than a lapse of discipline.
- MUST audit each author's full transcript and produced sources for the suite's paths, symbols, and assertions before
  accepting any result measured against it. An audit that scans nothing MUST fail.

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
