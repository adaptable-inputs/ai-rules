---
applies_to:
  load: "never"
  reason: "maintainer meta-guidance for the ai-rules repository itself"
---
# STRUCTURE

Rules for organizing the ai-rules repository itself (not downstream-projects).

## Frontmatter Contract
Every Markdown file MUST begin with an `applies_to` YAML frontmatter block. It
tells an agent whether to load the file at all. See `AI.md` Loading Protocol.

```yaml
---
applies_to:
  load: "conditional"
  when: "pom.xml or build.gradle is present"
  languages: ["java"]
  globs: ["**/*.java"]
---
```

- `load` MUST be one of: `always`, `entry`, `index`, `conditional`, `task`,
  `setup`, `never`.
- `load: conditional` MUST carry at least one of `languages`, `frameworks`,
  `libraries`, `tools`, or a `when` clause.
- `load: never` MUST carry a `reason`.
- Every scalar and list item MUST be quoted. An unquoted `**/*.java` parses as a
  YAML alias, not a string.

## Directory Layout
- Keep top-level categories at the repository root and list them in `AI.md`.
- Each category must have an index file named after the directory (e.g., `CORE/CORE.md`).
- `scripts/` is tooling, not a rule category. It has no index file and is not
  listed in `AI.md`. `scripts/check_structure.py` records the exemption in
  `NON_CATEGORY_DIRS`; add any future non-category directory there too.
- Category index files should only link one level down.
- In index files, every "## Files" entry includes a one-line description.
- MUST NOT add headings that only link to another file; use the "## Files" list instead.
- In `AI.md`, add a one-line description for every link to help navigation.

## AI-RULES Area
- Meta-guidance lives under `AI-RULES/`.
- Link AI-RULES files from `AI-RULES/AI-RULES.md`.
- Keep bootstrap definitions in `AGENTS_TEMPLATE.md` in sync with terminology
  in `AI-RULES/AI-RULES.md`.
- Keep repository-standard governance files (for example `CONTRIBUTING.md` and
  `CHANGELOG.md`) scoped to this repository only.
- `README.md` may include user-facing guidance on how to use ai-rules in
  downstream-projects.
- Put detailed downstream-project operational guidance in
  `AI-RULES/DOWNSTREAM-PROJECT.md`, `AI-RULES/UPDATE.md`, and
  `AGENTS_TEMPLATE.md`.

## Dependency Inversion Principle (DIP)
- Apply the Dependency Inversion Principle (DIP) to ruleset structure.
- More general rule docs must not reference child/specialization docs in
  normative rule content.
- Child/specialization docs may reference parent/general docs.
- Exception: pure index docs may link to child docs for navigation.
