---
applies_to:
  load: "conditional"
  when: "a suite certifies work whose author must not see it: a benchmark arm, an evaluation, or an acceptance suite written by another party"
  purpose: "isolation rules for a verification suite the author of the work is forbidden to read"
  inherits: ["TEST/TEST.md"]
---
# WITHHELD_SUITES

## Defaults
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

## Run Conditions
A measured run states what it measured. A run assembled by patching a previous one measures the patching, and a run
whose subject ignored the instruction under test measures the disobedience.

- Each run MUST begin from a reset state: the subject's workspace deleted and recreated, its build output gone, and no
  artefact of a previous run reachable. Reuse of a warm toolchain cache is permitted and MUST be stated, because
  clearing it would put network variance into the measurement.
- Each run MUST use a fresh agent with an empty transcript. A resumed agent carries prior context, so its cost is not
  comparable, and its cumulative transcript carries any earlier isolation leak into the new result.
- Every arm of a comparison MUST receive the same task text, differing only in which ruleset and workspace it names. A
  requirement added mid-study MUST be given to every arm, and the affected runs MUST be repeated, not amended.
- A run whose subject was patched after grading MUST NOT be reported as a run. Archive it as evidence and repeat it.
- MUST record, per run: the tokens consumed, whether each gate passed, and how much of the ruleset the subject actually
  read. Compliance with the instruction under test is a variable, not an assumption.
- MUST report a failed or voided run rather than dropping it. Dropping failures turns a distribution of runs into a
  distribution of successes.
- Where the subject's compliance varies between runs, the measurement MUST report that variance before any ratio drawn
  from it. A ratio computed across runs that differ in compliance measures the subject, not the ruleset.
- MUST state the sample size beside every derived figure. A single run yields an observation, never an effect size.

## The Harness
A withheld suite needs machinery: sealing, grading in a copy, auditing the author's transcript. Re-implementing that
machinery per project reproduces its defects per project. `adaptable-inputs/ai-test-harness` implements it, and its
guards are each covered by a test that fails when the guard is weakened.

The reference is a plain name, not a link: the repository is private, and a link checker MUST NOT be made to reach for
what it cannot fetch.

- MUST use a sealed harness rather than hand-rolled grading. Grading in the author's own tree leaves the suite behind,
  and the next task compiles against it.
- MUST run the isolation audit over every author's full transcript and produced sources before accepting any result
  measured against a withheld suite. An audit over zero transcripts, or over a stub, MUST fail.
- MUST seal the suite before an author begins, and MUST verify no test source is readable in the author's workspace.
- MUST NOT accept a token or performance number from an author whose audit found the suite. The number is void.
- A harness MUST report what it inspected and how much: a count of transcripts scanned, tests run, methods covered.
  "Nothing found" and "nothing checked" MUST be distinguishable in its output.
