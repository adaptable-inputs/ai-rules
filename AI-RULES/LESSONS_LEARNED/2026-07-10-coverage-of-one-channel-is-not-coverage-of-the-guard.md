---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# Coverage of one channel is not coverage of the guard

A guard with two inputs was covered by three tests, all of which exercised the input that worked. It was green for the
entire life of the defect. The rules extracted from this are in `TEST/GUARDS.md`, "Every Channel Carries Its Own Defect
Case" and "A Guard's Test Asserts the Reason, Not the Exit Code".

## What happened

1. **Three tests, one channel.** `audit_isolation.py` scanned two things: the arm's produced sources, and the agent's
   transcript. Its three unit tests -- `test_no_transcript_fails`, `test_stub_transcript_fails`,
   `test_planted_leak_is_caught` -- each planted their leak in the **transcript**. The transcript channel worked. The
   source channel scanned zero files. Nothing failed, because nothing asked it to.

2. **A verification channel confounded by its own input.** `study.py` documented `files_actually_read()` as the
   independent record against which an agent's claim is checked: *"an agent's account of what it read is a claim; the
   transcript is the record; where they disagree, the record governs."* It counted a rule file as read when its path
   appeared **anywhere in the transcript text**. The agent's first act is to read `RULES.txt`, whose entire content is
   the list of those thirty paths. A transcript in which the agent opened the manifest and nothing else scored 30 of 30.
   It could not disagree with a claim of 30. Seven unanimous "30/30" rows were never evidence.

3. **A test that agreed with the world instead of testing it.** `TestBaselinePinning` asserted that a conforming run can
   be pinned as a baseline. It passed only because the repository's baseline happened to be unpinned. The moment a run
   pinned it, two tests errored -- on the first real state they had ever met.

4. **A validation case that died before reaching the guard.** A harness was written to plant a synthetic defect for each
   guard and require the guard to reject it. One case invoked `record_run.py add --status void --files-read 1`.
   `--files-read` is not an argument that command accepts, so it exited 2 on an argument error, never running the
   void-reason check at all. Under a returncode-only assertion the case read green. It was caught only because each case
   also asserts the *reason* it expects to see in the output.

## What generalises

- A guard with N inputs needs N defect cases. Coverage of one channel reads as coverage of the guard, and the untested
  channel is the one that rots, because nothing is watching it.
- A verification channel MUST be independent of the artifact it verifies. If the thing being checked can put the
  evidence into the record, the check agrees with it by construction. Match against what a tool *did* -- the argument of
  a read call -- not against what the text *contains*.
- Prefer the failure mode that is loud. After the fix, an agent reading a rule by some other means is *under*counted,
  and the grader prints the disagreement. Silent agreement was the bug; noisy disagreement is a bug report.
- A guard's test MUST assert why the guard failed, not merely that it exited non-zero. A guard that dies on a typo, a
  missing file, or a bad argument exits non-zero too, and proves nothing.
- A guard's test MUST build the state it needs. A test that passes because of ambient repository state is a test of the
  repository, and it will fail on the first day the repository is right.
- Unanimity across runs is a signal to check the instrument, not a result. Seven identical readings from a gauge that
  can only read one number is what a broken gauge looks like.

## Cost of not doing this

The defect survived a 26-test suite, six CI gates, and two full studies. It was found by asking a question no test
asked: *what does this return when there is nothing to see?*
