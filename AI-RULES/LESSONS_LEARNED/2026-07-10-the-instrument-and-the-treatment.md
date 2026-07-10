---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# The instrument and the treatment

Halfway through a study, the measuring apparatus was found to be broken and the thing being measured was found to be
mis-specified. One of those may be corrected mid-study. The other may not, and the argument for correcting it is always
available. The rules extracted from this are in `TEST/WITHHELD_SUITES.md`, "The Instrument and the Treatment".

## What happened

Seven runs of a benchmark were planned against a fixed ruleset. During them:

- The isolation audit, the grader, the ledger, and the baseline were each found defective and corrected. Every one of
  those is **instrument**: no subject of the experiment reads them. Correcting them changed how the runs were measured,
  not what the runs were asked to do. Runs already taken were re-taken where the correction invalidated their
  measurement, and the reason was written down.
- The prompt was found defective too. `NFR2` in the specification states an observable and explicitly refuses to name a
  fix -- *"the requirement is the bound, not the fix."* The prompt put the fix back: *"(fetch join or entity graph)."*
  That is **treatment**: it is the one artefact every subject reads. Correcting it between run 3 and run 4 would have
  made those two runs different experiments.

The excuse for correcting it was ready and reasonable: *this change is an improvement*. It is the same sentence that had
already voided three earlier runs, when a rule file the arms read gained a section between run 7 and run 8.

The study was closed early instead, at n=4, and the correction recorded for the next one.

A related near-miss: the arms read the ruleset from a live working copy on disk. Editing that repository to record these
very lessons would have changed run 4's treatment while run 4 was reading it. The work was done in a separate clone.

## What generalises

- Separate the **instrument** from the **treatment** before the experiment starts, and write down which is which. The
  instrument may be repaired at any time. The treatment may not be touched while a run is in flight.
- The test for which one a thing is: *does the subject read it?* If yes, it is treatment.
- A correction to the treatment does not become admissible because it is correct. It opens a new study.
- Stopping a study early because the treatment is known to be flawed is legitimate, and is not the same as stopping
  early because the results are. Record the decision, its reason, and its timing, before the remaining runs are drawn.
- **The artefact under test MUST NOT be the artefact you are editing.** Take a copy, or wait.
- A freeze enforced by memory is not a freeze. The prompt was pinned by a SHA-256 that lived in an untracked scratch
  file and was checked when somebody remembered to check it. The documentation said "the template's hash is checked
  before every run"; it was a habit, described as a mechanism. The hash is now tracked, and the prompt is emitted by a
  command that refuses a drifted template, an unfrozen one, and one that substitutes nothing.
- A reference value MUST come from an artefact that meets the standard the reference will be used to enforce. A baseline
  pinned from a failing run is a floor that descends to meet it, and every later regression compares favourably against
  the thing that went wrong.

## Cost of not doing this

Three runs of an earlier study were voided after a rule file they read changed underneath them. A fourth was discarded
because it had been graded by an instrument that could not disagree with it. Roughly 700k tokens, spent to learn that
the distinction between instrument and treatment is not obvious in the moment and must be decided in advance.
