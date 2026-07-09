---
applies_to:
  load: "task"
  tasks: ["plan"]
  annex: "PLAN.ANNEX.md"
  purpose: "planning standards for implementation tasks"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "LANGUAGE/LANGUAGE.md", "DESIGN/DESIGN.md", "ARCHITECTURE/ARCHITECTURE.md", "FRAMEWORK/FRAMEWORK.md", "LIBRARY/LIBRARY.md", "BUILD_TOOLS/BUILD_TOOLS.md", "INFRASTRUCTURE/INFRASTRUCTURE.md", "CI-CD/CI-CD.md", "LANGUAGE/**", "DESIGN/**", "ARCHITECTURE/**", "FRAMEWORK/**", "LIBRARY/**", "BUILD_TOOLS/**", "INFRASTRUCTURE/**", "CI-CD/**", "TEST/TEST.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# PLAN

Guidance for AI agents creating implementation plans.

## Ruleset Read Gate (Mandatory)
- SHOULD start every planning task by reading the complete ai-rules ruleset.
- "Complete ai-rules ruleset" means every Markdown file transitively reachable
  from the baseline entry point `AI.md`.
- In downstream-projects, also read every Markdown file transitively reachable
  from the downstream extension entry point described in
  `AI-RULES/DOWNSTREAM-PROJECT.md`.
- MUST NOT skip reachable Markdown files and do not pick files ad-hoc.
- After the full read is complete, irrelevant rules MAY be removed from active
  context.

## Planning Requirement (Mandatory)
- SHOULD create a plan before starting implementation for every implementation task.
- The plan MAY be lightweight for low-risk, trivial changes, but it MUST still
  be decision-complete for its scope and risk while stating required elements
  tersely.
- MUST NOT start implementation when no plan exists.

## Plan Step Ordering Gates (Mandatory)
- Every plan MUST include a ruleset-read step as the very first task.
- The first task MUST require reading the complete ai-rules ruleset as defined
  in `Ruleset Read Gate (Mandatory)`.
- No other planning or implementation task MAY appear before that first step.
- Every plan MUST include a final task that re-reads the complete ai-rules
  ruleset and verifies the current planned/implemented changes still conform.
- If non-conformance is found during that final task, corrective updates are
  mandatory before the plan can be marked complete.
- This end-of-plan conformance check is a hard quality gate.

## Decision-Complete Plan Requirements
A plan MUST specify every item below. Expand each item in proportion to its
risk; never omit one:
- Goal and success criteria.
- In-scope and out-of-scope items.
- Semantic dependency order and target files.
- Key design decisions with rationale and chosen defaults.
- Edge cases/failure modes and mitigation strategy.
- Verification strategy (tests/checks) and acceptance criteria.
- Rollout/rollback or migration steps where relevant.

## Plan Quality Rules
- SHOULD keep steps concrete and implementable.
- SHOULD avoid ambiguous TODO-style phrasing.
- SHOULD keep assumptions explicit; avoid hidden decisions.
- SHOULD mark where follow-up issues are needed.
- SHOULD keep plan aligned with one-issue/one-branch/one-PR workflow when required.
- SHOULD prioritize system-level architecture and design decisions in planning.
- MUST NOT over-index on fine-grained implementation details that are better
  handled during execution unless they materially change risk/scope.

## Risk and Dependency Handling
- SHOULD identify external dependencies and blockers early.
- SHOULD call out coupling across layers and documents.
- SHOULD prefer dependency-first ordering (parent constraints before child
  specialization).
- SHOULD include rollback options for high-impact changes.

## Research Requirements
- SHOULD perform intensive research before finalizing a plan.
- Research MUST cover:
  - semantic parent and sibling docs that influence scope and decisions,
  - architecture and design constraints,
  - relevant codebase context and issue/PR history,
  - external authoritative sources when domain or risk requires it.
- SHOULD record the key options considered and why the chosen plan is preferred.

## Testing and Validation Planning
- SHOULD define required tests before implementation starts.
- SHOULD include regression strategy for changed behavior.
- MUST specify mandatory CI checks and quality gates.
- SHOULD define observable acceptance signals for rollout.

## Plan Review Checklist
- Is the plan decision-complete and implementation-ready?
- Does the plan start with the mandatory complete-ruleset-read task?
- Does the plan end with the mandatory complete-ruleset-read conformance gate?
- Are scope and success criteria explicit?
- Are semantic dependencies and ordering correct?
- Are risks, mitigations, and rollback steps captured?
- Are testing and acceptance criteria concrete?
- Are assumptions and follow-ups explicit?

## Override Notes
- Plans MUST stay decision-complete and dependency-aware.
