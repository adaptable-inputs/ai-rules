---
applies_to:
  load: "always"
---
# CORE

Core, non-negotiable baseline rules for all technology stacks in this
repository.

## Application Contract for AI Agents
- MUST interpret every rule using the obligation vocabulary in [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md).
- MUST apply CORE guidance by default before any domain-specific specialization.
- MUST NOT weaken CORE constraints in downstream docs unless an explicit override
  is documented and justified in the specialized doc.
- MUST resolve rule conflicts using the Conflict Resolution Rules in [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md).
  That procedure is authoritative; do not apply a different order here.
- MUST NOT block a task on an unresolved conflict. Apply the resolution the
  procedure yields, complete the task, and report the conflict in your final
  summary so a human can file the follow-up.

## Files
- [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md) - Obligation vocabulary
  (MUST/SHOULD/MAY) used by every rule in this repository.
- [VERSION_CONTROL_SYSTEM.md](VERSION_CONTROL_SYSTEM.md) - Commit/branch/PR workflow, issue linkage, and VCS hygiene.
- [DEPENDENCY_SELECTION.md](DEPENDENCY_SELECTION.md) - Criteria for choosing a
  framework, library, or build-tool dependency.
- [CONFLUENCE.md](CONFLUENCE.md) - Confluence wiki read-only and non-overridable no-delete safety rules.
- [CODE_REVIEW_PLATFORM.md](CODE_REVIEW_PLATFORM.md) - Platform-neutral
  protected-branch, merge-authority, and review-thread contract.
- [GITHUB.md](GITHUB.md) - GitHub specializations and the review-thread
  ownership override.
- [GITLAB.md](GITLAB.md) - GitLab specializations; no override.
- [JIRA.md](JIRA.md) - Jira ticket authoring, edit policy, and summary templates.
- [LOGGING.md](LOGGING.md) - Logging purpose, safety, and reliability guardrails.
- [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md) - Semantic inheritance, precedence, and override contract.
