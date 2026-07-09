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
  `setup`, `never`, `annex`.
- `purpose` states in one line what the doc governs. It replaces a prose Scope
  section.
- `inherits` lists the doc's semantic parents by path. It replaces a prose
  Semantic Dependencies section, and every target MUST exist.
- `annex` names the sibling `*.ANNEX.md` holding this doc's examples, pitfalls,
  review checklist, and testing guidance. An annex MUST carry `annex_of` and
  `tasks`, and MUST NOT contain an obligation.
- `load: conditional` MUST carry at least one of `languages`, `frameworks`,
  `libraries`, `tools`, or a `when` clause.
- `load: never` MUST carry a `reason`.
- Every scalar and list item MUST be quoted. An unquoted `**/*.java` parses as a
  YAML alias, not a string.

## Override Notes
`## Override Notes` is optional, and holds only an override *this* doc declares:
an exception to an inherited rule, a conditional fallback, or a named
specialization. Three shapes are rejected by `check_override_notes()`:

- "Framework docs MAY narrow this baseline" - `CORE/RULE_DEPENDENCY_TREE.md`
  Core Principles says this once, for every doc.
- "...but these constraints remain mandatory" - a rule's own keyword is
  authoritative. Prose cannot make a `SHOULD` mandatory; change the keyword.
- "This file is the Java baseline" - that is the `purpose` frontmatter field.

Category indexes carry no `## Specialization Contract`; it was the same
boilerplate. A doc-specific precedence rule goes under its own heading.

## Directory Layout
- Keep top-level categories at the repository root and list them in `AI.md`.
- Each category must have an index file named after the directory (e.g., `CORE/CORE.md`).
- Keep an index file index-level and boundary-focused; deep behavior belongs in
  the child docs it lists.
- When adding a doc, list it in its category index and regenerate `MANIFEST.md`.
  Both are enforced; see "Generated Artifacts".
- An index MUST NOT carry a `Role in the Ruleset`, `Scope Boundary`, or
  `Authoring Notes` section. The first two restate
  `CORE/RULE_DEPENDENCY_TREE.md` and the doc's own `purpose`; the third is
  maintainer guidance, and it belongs in this file. All three were loaded on
  every task that opened an index.
- `scripts/` is tooling, not a rule category. It has no index file and is not
  listed in `AI.md`. `scripts/check_structure.py` records the exemption in
  `NON_CATEGORY_DIRS`; add any future non-category directory there too.

## Generated Artifacts
`MANIFEST.md` is generated from every doc's `applies_to` frontmatter and MUST
NOT be hand-edited. It is what an agent reads to decide which docs to load, so a
stale manifest silently hides a rule; CI fails the build when it drifts.

```bash
python3 scripts/gen_manifest.py            # regenerate after any frontmatter change
python3 scripts/gen_manifest.py --check    # what CI runs
python3 scripts/check_indexes_accurate.py  # every doc listed once, every link resolves
```

Enable the pre-commit hook once per clone, so drift is caught before it is
pushed rather than in CI:

```bash
git config core.hooksPath .githooks
```

A `conditional` or `task` doc MUST carry a `purpose`: the manifest selects on
it. Index descriptions stay hand-written, because they say things `purpose` does
not; `check_indexes_accurate.py` verifies the links, not the prose.

## Test Suite
`scripts/test_rules.py` runs in CI and MUST pass before merge. Run it locally
with `python3 scripts/test_rules.py`.

It asserts two different things:
- Properties of the corpus: valid frontmatter, an obligation keyword on every
  normative statement, no self-contradicting statement.
- That the checkers actually fail when they should. Each test in
  `TestRatchetFails` reproduces a defect that shipped at least once, and
  `TestRatchetDoesNotCryWolf` guards against false positives, which are what
  make a checker get ignored.

When you fix a checker bug, add the reproducing test in the same change. A guard
that cannot fail is worse than no guard, because it is trusted.
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
