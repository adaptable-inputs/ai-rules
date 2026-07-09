# CORE

Core, non-negotiable baseline rules for all technology stacks in this
repository.

## Role in the Ruleset
- CORE is part of the first-applied cross-cutting baseline layer.
- CORE rules are inherited by all downstream docs, including language,
  framework, library, build-tool, infrastructure, CI/CD, and task-overlay docs.
- Precedence and override behavior are defined in
  [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md).

## Scope Boundary
CORE includes only stack-agnostic guidance such as:
- VCS workflow and delivery hygiene.
- Logging safety and reliability practices.
- Semantic dependency and override contract for the full ruleset.

CORE does not include:
- Language-specific coding rules.
- Framework-specific implementation details.
- Library/tool/runtime-specific usage patterns.

Those belong in their respective domains (`LANGUAGE/**`, `FRAMEWORK/**`,
`LIBRARY/**`, `BUILD_TOOLS/**`, `INFRASTRUCTURE/**`, `CI-CD/**`).

## Application Contract for AI Agents
- Interpret every rule using the obligation vocabulary in
  [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md).
- Apply CORE guidance by default before any domain-specific specialization.
- MUST NOT weaken CORE constraints in downstream docs unless an explicit override
  is documented and justified in the specialized doc.
- Resolve rule conflicts using the Conflict Resolution Rules in
  [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md). That procedure is
  authoritative; do not apply a different order here.
- MUST NOT block a task on an unresolved conflict. Apply the resolution the
  procedure yields, complete the task, and report the conflict in your final
  summary so a human can file the follow-up.

## Files
- [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md) - Obligation vocabulary
  (MUST/SHOULD/MAY) used by every rule in this repository.
- [VERSION_CONTROL_SYSTEM.md](VERSION_CONTROL_SYSTEM.md) - Commit/branch/PR workflow, issue linkage, and VCS hygiene.
- [CONFLUENCE.md](CONFLUENCE.md) - Confluence wiki read-only and non-overridable no-delete safety rules.
- [CODE_REVIEW_PLATFORM.md](CODE_REVIEW_PLATFORM.md) - Platform-neutral
  protected-branch, merge-authority, and review-thread contract.
- [GITHUB.md](GITHUB.md) - GitHub specializations and the review-thread
  ownership override.
- [GITLAB.md](GITLAB.md) - GitLab specializations; no override.
- [JIRA.md](JIRA.md) - Jira ticket authoring, edit policy, and summary templates.
- [LOGGING.md](LOGGING.md) - Logging purpose, safety, and reliability guardrails.
- [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md) - Semantic inheritance, precedence, and override contract.

## Authoring Notes
- Keep this file index-level and boundary-focused.
- Add new core documents only when guidance is truly cross-cutting.
- Any dependency-precedence change must be reflected in
  `RULE_DEPENDENCY_TREE.md`.
