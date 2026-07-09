---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# Verifications that cannot fail

Four checks in one week reported success over a real defect. Each was trusted because it was green, and none had ever
been observed failing. The rule extracted from them is in `TEST/TEST.md`, "Verifying the Tests Themselves".

## What happened

1. **A crashed parser read as "no findings".** `scripts/check_examples.py` shelled out to a Node parser that died with
   `ERR_MODULE_NOT_FOUND`. Its exit code 1 was interpreted as "ran fine, nothing to report". The checker announced 304
   verified code blocks while verifying none. Fixed by requiring the parser to print an `OK <n>` sentinel; a run without
   it is a failure.

2. **A quiet flag hid the test summary.** The benchmark harness ran `mvn -q test` and scraped the console for "Tests
   run:". `-q` suppresses that line, so the scraper found nothing and reported "no test summary found" while the build
   was green - indistinguishable from a suite that never ran. Fixed by reading `surefire-reports/TEST-*.xml`; zero
   report files is now a failure.

3. **A severity threshold no finding could reach.** Checkstyle's `google_checks.xml` emits almost every rule at
   `warning`, and `maven-checkstyle-plugin` fails only at `error`. The obvious wiring reports BUILD SUCCESS on code full
   of violations. Fixed with `-Dcheckstyle.violationSeverity=warning`, then verified against a deliberately misformatted
   file and a conforming one.

4. **A test that could not fail.** A shared suite located an error handler reflectively - "a public method taking one
   `Exception`" - and asserted the handler was non-null when it found none. It passed on an implementation that declared
   no such handler at all. Fixed by naming the operation in the specification, which turned its absence into a compile
   error.

## What generalises

- The failure mode of all four is silence. A check that reports nothing when it cannot run looks exactly like a check
  that reports nothing because there is nothing wrong.
- Two further defects came from tests asserting an implementation rather than a contract: one demanded a handler return
  `ResponseEntity` when `@ResponseStatus` on the returned body is equally correct, and one asserted on a record's
  `toString`, so a null field Jackson never serialises looked like a field present on the wire. Both failed a conforming
  implementation.
- The cure for an uncertain test is not more reasoning about the test. Build a minimal reference that conforms and one
  that violates, and require the test to pass the first and fail the second. That is how the handler test above was
  finally settled: three variants, two conforming shapes and one that leaked the exception message, and the test
  accepted both conforming shapes and rejected the leak.

## Cost of not doing this

`check_examples.py` sat green in CI while verifying nothing. The reflective handler test would have certified an arm
with no error handling. Neither would have been caught by a reviewer reading the code, because both looked correct.
