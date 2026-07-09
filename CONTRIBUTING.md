---
applies_to:
  load: "never"
  reason: "human-facing contribution guidance"
---
# Contributing

Thank you for improving ai-rules. This repo is the single source of truth for
shared AI guidance, so changes should be deliberate and well-reviewed.

## This is a divergent fork
`adaptable-inputs/ai-rules` is a fork of `fabian-barney/ai-rules` and does not
merge back upstream. Its workflow differs from upstream's, and this section
describes what this repository actually does rather than what upstream does.

- Maintainers MAY commit directly to `main`. `main` is not a protected branch
  here, so the protected-branch rules in `CORE/CODE_REVIEW_PLATFORM.md` do not
  bind maintenance of this repository. Those rules govern the projects ai-rules
  is vendored into.
- Outside contributors SHOULD open a pull request from a branch.
- Every change, however delivered, MUST pass all four `docs-check` jobs:
  `markdownlint`, `linkcheck`, `structure`, and `examples`.

## Workflow
- Group related work into one focused commit or pull request per concern.
- An issue is OPTIONAL. When one exists, link it with a closing keyword
  (for example `Closes #123`).
- Update the relevant directory entry file (e.g., `DESIGN/DESIGN.md`).
- Keep `AI.md` as the single top-level entry point.
- Every new document MUST carry `applies_to` frontmatter. See
  `AI-RULES/STRUCTURE.md` for the contract.
- Every new normative statement MUST carry an obligation keyword. See
  `CORE/NORMATIVE_LANGUAGE.md`.
- SHOULD avoid quoting copyrighted sources; summarize in your own words.

## Review Expectations
- Verify AI-generated content for correctness and alignment with repo goals.
- If a change affects downstream-project policy, update related AI-RULES docs
  and templates in the same change.

## Versioning and Releases
- Tag releases (e.g., `v0.2.0`). Fork tags MUST NOT reuse an upstream version
  number for different content.
- Record every change under `## Unreleased` in `CHANGELOG.md` as it lands, and
  promote that section to a version heading at release.

## Docs Hygiene
- Keep filenames UPPERCASE at the repo root.
- Keep line endings consistent (Windows CRLF is acceptable here).
- Ensure links and markdown pass CI checks.
