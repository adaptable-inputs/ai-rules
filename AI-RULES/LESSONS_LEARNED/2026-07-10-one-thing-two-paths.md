---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# One thing, two paths

A producer wrote to one location and a consumer read from another. Nothing failed. Both locations held plausible
content, and the disagreement was invisible for as long as the two happened to agree. The rule extracted from this is in
`CORE/CORE.md`, "One Thing Has One Path".

## What happened

1. **Two sealed archives.** `seal.py` produced `build/suite-sealed.tgz`, and CI verified it. `study.py` graded against
   `harness-sealed.tgz`, which nothing regenerated. The guard watched an archive the runner never opened. On the day it
   was found, the two held byte-identical test sources and differed only in gzip timestamps, so no run had been graded
   against the wrong suite. A single edit to the suite would have ended that, silently, with CI green.

2. **Three ledgers.** `study.py` appended graded rows to `bench/study-runs.jsonl`. `study_report.py` read
   `results/fork-runs.jsonl`. `record_run.py` used `build/runs.jsonl`. The rows reached the report because a human
   copied them across, and three voided runs existed only in the destination, added by hand. Every published figure had
   passed through a transcription step that nothing verified.

3. **A script that kept its coordinate system.** `study.py` and `audit_isolation.py` were extracted from the scratch
   directory where they ran into a version-controlled repository. Their paths came with them: five constants resolved
   against the script's own directory -- the arms, the ledger, the toolchain, the sealed archive -- and not one of them
   existed beside the new location. The tracked copy could not run at all. The only working copy was untracked, in a
   directory whose git repository held zero commits. What was versioned could not run; what ran was not versioned.

   `study.py` failed **closed** and exited 1, so nobody noticed. `audit_isolation.py` failed **open** and reported every
   arm clean. Same defect, and only the harmless one was loud.

## What generalises

- One artefact has one path. Where a producer and a consumer name the same thing, a test MUST assert they resolve to the
  same location, in code, and not by inspection.
- A manual step between a measurement and its report is a place where they can differ. Give the tool a command for it.
  Three runs were once appended to a ledger by hand *because nothing offered to do it*.
- Moving code does not move its assumptions. After relocating a script, every path it resolves relative to itself is
  wrong until proven otherwise. Resolve from an explicit argument, or from the repository root, and require the
  argument.
- Failing closed hides a defect as effectively as failing open, for as long as nobody runs the code. The difference is
  only in what happens on the day they do.
- Two copies of a guard do not double its review. They double the number of places its defect can live.

## Cost of not doing this

The document written specifically to survive a context compaction -- the protocol every later run was to follow -- named
commands that exited 1. It had never been executed as written.
