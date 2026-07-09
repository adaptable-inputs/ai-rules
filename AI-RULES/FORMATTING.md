---
applies_to:
  load: "never"
  reason: "maintainer meta-guidance for the ai-rules repository itself"
---
# FORMATTING

Formatting rules for the ai-rules repository itself (not downstream-projects).

## Markdown
- Use UTF-8 without BOM.
- End each Markdown file with a single trailing newline.
- Keep lines at or under 120 characters; wrap long list items.
- Use "## Files" as the link section heading in index files.

## Code Examples
`scripts/check_examples.py` parses every fenced block in CI. It checks syntax only, never types: paired Do/Don't
snippets reference types they never declare.

- Tag every fenced block with a known language, or leave it untagged. An unrecognised tag MUST fail the build.
- A block containing `//` comments MUST be tagged `jsonc`, not `json`.
- In paired Do/Don't snippets, each declaration MUST have a unique name (`*Bad` / `*Good`) so each half is independently
  compilable. See `LESSONS_LEARNED/2026-02-08-react-example-robustness.md`.
- A snippet showing a class body MUST wrap it in a class. Bare method bodies do not parse.
- To exempt a block, put `<!-- no-verify: reason -->` on the line directly above its opening fence.
