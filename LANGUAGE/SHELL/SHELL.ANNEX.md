---
applies_to:
  load: "annex"
  annex_of: "SHELL.md"
  tasks: ["review", "test"]
---
# SHELL - Annex

## High-Risk Pitfalls
1. Unquoted expansions causing word splitting and glob injection.
2. Missing strict mode masking failures.
3. Using `eval` with untrusted input.
4. Secret leakage via command echo/logs.
5. Cleanup omission leaving temp files/locks.
6. Destructive commands without path guards.
7. Bash-specific syntax in scripts declared as `/bin/sh`.

## Do / Don't Examples
### 1. Quoting
```bash
# Don't
rm -rf $TARGET_DIR/*

# Do
rm -rf "${TARGET_DIR:?}"/*
```

### 2. Error Handling
```bash
# Don't
cp source.txt "$dest"
echo "done"

# Do
set -euo pipefail
cp source.txt "$dest"
echo "done"
```

### 3. Command Injection Risk
```bash
# Don't
eval "tar -czf backup.tar.gz $INPUT_PATH"

# Do
tar -czf backup.tar.gz -- "$INPUT_PATH"
```

## Code Review Checklist for Shell
- Are the interpreter and strict mode configured correctly?
- Are all variable expansions safely quoted?
- Is untrusted input kept away from command construction/eval?
- Are errors surfaced with meaningful exit behavior?
- Are destructive operations guarded (`${var:?}`, path checks)?
- Are secrets kept out of output/logs?
- Are cleanup handlers present for temp resources?

## Testing Guidance for Shell Scripts
- Run static analysis (`shellcheck`) in CI.
- Test scripts in clean environments (minimal env vars).
- Test failure paths and non-zero exit behavior.
- Test idempotency where scripts MAY run repeatedly.
- Add integration tests for critical automation scripts.
