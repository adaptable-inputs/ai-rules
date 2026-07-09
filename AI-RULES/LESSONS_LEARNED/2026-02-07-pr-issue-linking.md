---
applies_to:
  load: "never"
  reason: "maintainer meta-guidance for the ai-rules repository itself"
---
# 2026-02-07-pr-issue-linking

## Issue
Several PRs were merged without being linked to their corresponding GitHub
issues, so the issues stayed open and project tracking became inconsistent.

## Prevention
- Link each PR to its main issue before merge (for example with `Closes #<id>`
  in the PR description).
- If a PR is already open, update the PR body to add the issue link instead of
  leaving manual follow-up for later.
- During final PR checks, confirm the issue link is present so merged PRs close
  their issues automatically.
