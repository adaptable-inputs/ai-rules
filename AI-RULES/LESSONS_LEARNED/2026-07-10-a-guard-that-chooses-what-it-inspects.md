---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# A guard that chooses what it inspects

Six guards in one day reported success while inspecting nothing, or inspecting the wrong thing. Every one of them had
been written deliberately, reviewed, and covered by a passing test. The rules extracted from this are in
`TEST/GUARDS.md`, "A Guard Does Not Choose What It Inspects" and "An Omitted Check Must Be Declared, Not Assumed".

## What happened

1. **An audit resolved its own subjects, from names that had gone stale.** `audit_isolation.py` scanned each benchmark
   arm's sources for traces of the test suite it was graded by. It found the arms itself:

   ```python
   BENCH = Path(__file__).resolve().parent
   for arm_name in ("arm-fork", "arm-upstream"):
       problems += scan_sources(BENCH / arm_name)
   ```

   Those were the arm names of an earlier study. The current arms were called `arm-fork-v3-r01` and so on, and
   `BENCH` resolved to the directory holding the script, which contained no arms at all. `scan_sources` returned `[]`
   for a directory that did not exist, and `[]` is what a clean arm returns. A source file naming three suite classes
   was planted in a real arm; the audit printed `isolation audit passed: no arm referenced the test suite` and exited 0.

2. **An empty scan and a clean scan were the same value.** The same function returned `[]` when the source tree was
   missing, when it was empty, and when it was clean. Three states, one answer, and the answer was innocence.

3. **A second copy carried the same defect for a different reason.** A byte-identical copy of the script sat beside the
   arms, where `BENCH` resolved correctly -- and still scanned nothing, because the hardcoded names were a study out of
   date. Two copies, two independent reasons, one silence.

4. **A check that did not exist read as a check that passed.** The suite was sealed, but a *graded* arm's implementation
   was not. The moment run 1 finished, a complete, conforming, fully covered program sat on disk beside six empty
   workspaces. Each later arm was told not to read it by the prompt, and by nothing else. A transcript whose only action
   was opening the previous arm's `OwnerService.java` passed the audit.

5. **The fix for that was nearly an opt-in flag.** Adding `--peer` to name the workspaces an arm must not read would
   have restored the hole the first time somebody forgot it. Absence of the flag now has to be asserted: `--no-peers`.
   Passing neither is a failure; passing both is a contradiction the audit refuses.

## What generalises

- A guard MUST be told what to inspect. A guard that discovers its own subjects will one day discover none, and nothing
  in its output distinguishes that from finding nothing wrong.
- "Nothing to inspect" is a failure, not a pass. A missing directory, an empty set, an unreadable input, and a clean
  result MUST NOT share a return value.
- A guard MUST report how much it inspected, not only what it found. `isolation audit passed` was true and useless;
  `passed over 1 arm and 1 transcript` would have made the zero visible the first time.
- Duplicating a guard duplicates its blast radius and not its review. The two copies were byte-identical, so the second
  bought nothing and hid the same defect twice.
- A safety check that can be omitted MUST require its omission to be declared. An optional guard is a guard that is off
  in exactly the situation nobody thought about.
- Seal the answer key, and seal the answers already given. The suite was withheld from every arm; the previous arm's
  finished solution was not, and it was a better cheat sheet than the tests.

## Cost of not doing this

Two studies -- twelve runs, roughly 2.1M tokens -- were audited on one channel out of two. Nothing suggests any arm was
contaminated; the transcript channel worked, and it is the channel through which an arm would have had to read the
suite. But "we did not detect contamination" and "we checked for contamination" are different claims, and only the first
was true. The ledger was reset and the runs re-taken.
