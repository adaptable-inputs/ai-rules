---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# A withheld suite leaked through the compiler

A benchmark graded two implementations against a suite neither was allowed to see. The suite was sealed in an archive
and absent from disk while each implementation was written. It still leaked. The rule extracted from this is in
`TEST/TEST.md`, "Withheld Verification Suites".

## What happened

The harness installed the suite into each arm's own `src/test/`, ran it, and left it there. Later both arms were resumed
to delete unreachable code. The suite was now sitting in their trees. One arm ran `mvn package`, javac compiled the
tests, and the build failed with:

```text
.../src/test/java/com/bench/vetclinic/StructureAndBootTest.java:[83,53] cannot find symbol
  symbol:   method getId()
  location: variable s of type com.bench.vetclinic.domain.Specialty
```

The arm restored the getter it had just deleted, and reported plainly that it had learned this "from the compiler error
only - did not open the test file". That is true, and it is still exposure: the diagnostic disclosed that the suite
calls `Specialty.getId()`.

## What generalises

- Absence from the workspace must hold at **every** moment the author works, not only at first. An artifact left behind
  by one grading run is present for the next task.
- Grade in a copy. The author's tree must never contain the suite, so there is nothing to leave behind.
- A toolchain speaks. A compiler, a linker, or a coverage report that names a withheld test discloses its contract
  without anyone reading a line of it.
- Earlier, before the suite was sealed at all, both arms opened it unprompted. One said "these shared tests define the
  exact contract"; the other, "the shared tests link against my code, so I must read them to get signatures exactly
  right." Both readings were reasonable. The fix was not discipline but the specification: naming every operation the
  suite calls removed the reason to look.

## Cost of not doing this

The leak was bounded here - one method signature, during a cleanup phase, after the implementation was already complete
- because the arm disclosed it. An arm that did not volunteer it would have been indistinguishable from an honest one,
and the benchmark would have reported a number it had not earned.
