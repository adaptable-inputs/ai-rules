---
applies_to:
  load: "conditional"
  when: "the project ships shell scripts"
  languages: ["shell"]
  globs: ["**/*.sh", "**/*.bash"]
  annex: "SHELL.ANNEX.md"
  purpose: "safe and maintainable shell scripting defaults"
  inherits: ["SECURITY/SECURITY.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# SHELL

Guidance for AI agents implementing and reviewing shell scripts.

## Defaults
- SHOULD prefer Bash for non-trivial scripts and declare interpreter explicitly (`#!/usr/bin/env bash`).
- SHOULD enable strict mode for Bash scripts: `set -euo pipefail` and safe `IFS` handling when needed.
- Quote variable expansions by default (`"$var"`).
- SHOULD use functions to structure scripts; keep `main` flow explicit.
- SHOULD keep scripts idempotent where practical.

## Error Handling and Exit Behavior
- MUST fail fast on command failures unless explicitly handling error cases.
- SHOULD use explicit error messages for failure paths (`echo ... >&2`).
- SHOULD check required commands and inputs early.
- For cleanup logic, SHOULD use `trap` handlers.
- SHOULD keep exit codes meaningful and consistent.

## Security Guardrails
- MUST NOT build shell commands by concatenating untrusted input.
- SHOULD avoid `eval` unless there is no alternative and input is tightly controlled.
- MUST NOT print secrets/tokens to logs.
- MUST use least-privilege execution; avoid unnecessary `sudo`.
- MUST validate file paths and arguments before destructive operations.

## Portability and Environment
- SHOULD be explicit about shell features requiring Bash vs POSIX sh.
- SHOULD avoid relying on environment-specific behavior without checks.
- SHOULD use `command -v` for dependency checks.
- SHOULD avoid hidden reliance on interactive shell state.

## Data and Loop Handling
- SHOULD prefer arrays over word-splitting where Bash arrays are available.
- SHOULD use `read -r` to preserve backslashes.
- SHOULD avoid parsing command output with brittle text assumptions when machine- readable alternatives exist.
- SHOULD be careful with globbing and empty-match behavior.
