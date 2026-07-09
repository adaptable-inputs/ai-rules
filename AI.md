---
applies_to:
  load: "entry"
---
# AI Rules Index

This index is the single entry point for the baseline rules. Each level links only one level deeper to keep navigation
predictable.

## Loading Protocol
An agent MUST NOT read this ruleset exhaustively. Load in this order:

1. **Always load.** `CORE/NORMATIVE_LANGUAGE.md`, `CORE/CORE.md`, and `CORE/RULE_DEPENDENCY_TREE.md`. Without these an
   agent cannot interpret the obligation level or precedence of any other rule.
2. **Detect the stack.** Inspect the project for languages, frameworks, libraries, build tools, and infrastructure
   actually in use. Also read the project's declared `compliance_scope`, if it has one; see "Compliance Scope" below.
3. **Load only what matches.** Read [MANIFEST.md](MANIFEST.md) - one generated table of every loadable doc, its load
   class, and the condition under which it applies - then load only the rows matching the detected stack. A Java project
   MUST NOT load `LANGUAGE/PYTHON/`. An agent MUST NOT open a category index to make this decision; the manifest is
   authoritative and CI verifies it against each doc's frontmatter. A doc's `purpose` says what it governs and its
   `inherits` names its semantic parents; both live in frontmatter, so neither costs a section.
4. **Load task overlays by task type**, not by stack: `PROGRAMMING/`, `PLAN/`, `REVIEW/`.
5. **Load annexes only for the tasks they name.** A doc with an `annex:` field has a sibling `*.ANNEX.md` holding its
   examples, pitfalls, review checklist, and testing guidance. Those sections contain no obligations. An agent MUST NOT
   load an annex while implementing a change; it MUST load one whose `tasks` include the task at hand
   (`review`, `test`). This removes about 32% of the context an implementation task would otherwise carry.

### Compliance Scope
`COMPLIANCE/LICENSES.md` binds every project and always loads. The five jurisdiction-specific regimes - `gdpr`,
`eprivacy`, `eu-ai-act`, `dora`, `nis2` - load only when the project's entry point (`AGENTS.md`, `CLAUDE.md`) declares
them:

```md
compliance_scope: ["gdpr", "eprivacy"]
```

An undeclared project loads **all five**, because an agent that misjudges a project's jurisdiction MUST fail toward
loading a regulation rather than skipping one. Declaring the scope is what makes skipping safe. To assert that none
apply, declare it empty: `compliance_scope: []`.

### Never Load
These MUST NOT be read as project rules. They are repository history and maintainer meta-guidance, and consume context
without governing any downstream project:

- `AI-RULES/**` - guidance for maintaining *this* repository. Load only when the task is to modify ai-rules itself.
  `AI-RULES/UPDATE.md` is the exception; see below.
- `CONTRIBUTING.md`, `README.md` - human-facing repository docs.

### Load During Setup Only
These carry `load: setup`. They are not project rules, but the target-version preflight in `AGENTS_TEMPLATE.md` requires
reading them before any `git subtree add` or `git subtree pull`. An agent MUST read them when setting up or updating
ai-rules, and MUST NOT read them during ordinary project work:

- `CHANGELOG.md` - release history; the preflight reads it to learn what the target version changed.
- `AI-RULES/UPDATE.md` - the update procedure itself.
- `AGENTS_TEMPLATE.md` - the bootstrap template.

## CORE
- [CORE/CORE.md](CORE/CORE.md) - Core, non-negotiable rules.

## AI-RULES
- [AI-RULES/AI-RULES.md](AI-RULES/AI-RULES.md) - Meta-guidance for maintaining this repository. Not a project rule; see
  "Never Load" above.

## PROGRAMMING
- [PROGRAMMING/PROGRAMMING.md](PROGRAMMING/PROGRAMMING.md) - Programming task guidance.

## PLAN
- [PLAN/PLAN.md](PLAN/PLAN.md) - Planning guidance for execution tasks.

## REVIEW
- [REVIEW/REVIEW.md](REVIEW/REVIEW.md) - Code review guidance.

## SECURITY
- [SECURITY/SECURITY.md](SECURITY/SECURITY.md) - Security guidance.

## TEST
- [TEST/TEST.md](TEST/TEST.md) - Testing guidance.

## LANGUAGE
- [LANGUAGE/LANGUAGE.md](LANGUAGE/LANGUAGE.md) - Language and coding guidance.

## DESIGN
- [DESIGN/DESIGN.md](DESIGN/DESIGN.md) - Design and code-quality guidance.

## ARCHITECTURE
- [ARCHITECTURE/ARCHITECTURE.md](ARCHITECTURE/ARCHITECTURE.md) - Architecture patterns and guidance.

## FRAMEWORK
- [FRAMEWORK/FRAMEWORK.md](FRAMEWORK/FRAMEWORK.md) - Framework-specific rules.

## BUILD_TOOLS
- [BUILD_TOOLS/BUILD_TOOLS.md](BUILD_TOOLS/BUILD_TOOLS.md) - Build and dependency tools.

## LIBRARY
- [LIBRARY/LIBRARY.md](LIBRARY/LIBRARY.md) - Library-specific guidance.

## COMPLIANCE
- [COMPLIANCE/COMPLIANCE.md](COMPLIANCE/COMPLIANCE.md) - Compliance and license rules.

## CI-CD
- [CI-CD/CI-CD.md](CI-CD/CI-CD.md) - CI/CD guidance.

## INFRASTRUCTURE
- [INFRASTRUCTURE/INFRASTRUCTURE.md](INFRASTRUCTURE/INFRASTRUCTURE.md) - Infrastructure guidance.
