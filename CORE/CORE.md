---
applies_to:
  load: "always"
---
# CORE

Core, non-negotiable baseline rules for all technology stacks in this repository.

## Application Contract for AI Agents
- MUST interpret every rule using the obligation vocabulary in [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md).
- MUST apply CORE guidance by default before any domain-specific specialization.
- MUST NOT weaken CORE constraints in downstream docs unless an explicit override is documented and justified in the
  specialized doc.
- MUST resolve rule conflicts using the Conflict Resolution Rules in [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md).
  That procedure is authoritative; do not apply a different order here.
- MUST NOT block a task on an unresolved conflict. Apply the resolution the procedure yields, complete the task, and
  report the conflict in your final summary so a human can file the follow-up.

## Authorization Before Touching What You Do Not Own
An agent MAY manage what it created: processes it started, files it wrote, directories it made. Everything else belongs
to someone, and an agent that cannot name the owner MUST NOT act on it.

- MUST NOT signal, kill, delete, move, or modify any process or file the agent did not create in the current session,
  without explicit authorization. Ask, and wait for an answer.
- Ownership descends the process tree. An agent that started a process owns that process and every descendant it
  spawned, and MAY signal any of them. Ownership does not ascend: a child the agent did not start confers no claim on
  its parent, and no claim on that parent's other children.
- MUST scope a destructive command by something that identifies the agent's own work: a process identifier captured when
  it was started, its descendants, a directory the agent created, a path it wrote. MUST NOT scope by a behavioural
  pattern such as "matches this name" or "is the parent of a sleeping process", which selects by what a process does
  rather than by who started it, and so sweeps in what belongs to others.
- MUST check ownership before signalling a process. Where the owner is not the agent's own user, MUST stop and ask.
- MUST NOT escalate to an uncatchable signal without having observed a catchable one fail for a reason the agent
  understands.
- A glob that can match outside a directory the agent created MUST NOT be passed to a destructive command.
- Being unable to do damage is not the same as not attempting it. An attempted action on something the agent does not
  own MUST be reported, whether or not it succeeded.

## Context Economy Never Buys Correctness
The loading protocol exists so an agent reads what governs its task and nothing else. It exists to remove waste, not to
ration correctness. A smaller context that omits a rule the task is subject to is not an optimization; it is a missed
rule.

- MUST NOT skip a document whose loading condition holds, in order to reduce context. If the condition holds, the
  document governs the task.
- MUST NOT weaken, shorten, or delete a rule, a check, or a test to reduce context. Remove redundancy instead:
  restatements, prose an agent cannot act on, and rules that bind few tasks but load on all of them.
- A rule that governs a narrow situation MUST be made conditional rather than made brief. Scope is the lever, not
  brevity.
- When correctness work grows the context an agent loads, MUST report the cost plainly. An unreported cost cannot be
  weighed.
- A large context is evidence of a structural defect worth finding, and MUST NOT be treated as licence to omit a
  governing rule. An exhaustive read of an entire ruleset on every task is such a defect; so is a rule that loads always
  and binds almost nothing.

## Files
- [NORMATIVE_LANGUAGE.md](NORMATIVE_LANGUAGE.md) - Obligation vocabulary (MUST/SHOULD/MAY) used by every rule in this
  repository.
- [VERSION_CONTROL_SYSTEM.md](VERSION_CONTROL_SYSTEM.md) - Commit/branch/PR workflow, issue linkage, and VCS hygiene.
- [DEPENDENCY_SELECTION.md](DEPENDENCY_SELECTION.md) - Criteria for choosing a framework, library, or build-tool
  dependency.
- [CONFLUENCE.md](CONFLUENCE.md) - Confluence wiki read-only and non-overridable no-delete safety rules.
- [CODE_REVIEW_PLATFORM.md](CODE_REVIEW_PLATFORM.md) - Platform-neutral protected-branch, merge-authority, and
  review-thread contract.
- [GITHUB.md](GITHUB.md) - GitHub specializations and the review-thread ownership override.
- [GITLAB.md](GITLAB.md) - GitLab specializations; no override.
- [JIRA.md](JIRA.md) - Jira ticket authoring, edit policy, and summary templates.
- [LOGGING.md](LOGGING.md) - Logging purpose, safety, and reliability guardrails.
- [RULE_DEPENDENCY_TREE.md](RULE_DEPENDENCY_TREE.md) - Semantic inheritance, precedence, and override contract.
