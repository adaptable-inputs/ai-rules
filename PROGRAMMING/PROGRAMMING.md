---
applies_to:
  load: "task"
  tasks: ["programming"]
  annex: "PROGRAMMING.ANNEX.md"
  purpose: "end-to-end implementation workflow expectations for coding tasks"
  inherits: ["CORE/VERSION_CONTROL_SYSTEM.md", "TEST/TEST.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CORE/RULE_DEPENDENCY_TREE.md", "LANGUAGE/LANGUAGE.md", "DESIGN/DESIGN.md", "ARCHITECTURE/ARCHITECTURE.md", "FRAMEWORK/FRAMEWORK.md", "LIBRARY/LIBRARY.md", "BUILD_TOOLS/BUILD_TOOLS.md", "INFRASTRUCTURE/INFRASTRUCTURE.md", "CI-CD/CI-CD.md", "LANGUAGE/**", "DESIGN/**", "ARCHITECTURE/**", "FRAMEWORK/**", "LIBRARY/**", "BUILD_TOOLS/**", "INFRASTRUCTURE/**", "CI-CD/**"]
---
# PROGRAMMING

Guidance for AI agents executing implementation tasks.

## Default Execution Workflow
1. Verify hard preconditions before implementation:
   - The ruleset read gate in this file has been completed.
   - A plan exists (see `PLAN/PLAN.md`).
   - The work is mapped to an issue/ticket.
   - Work is on a dedicated non-default branch for that issue/ticket.
   - If any precondition is missing, stop implementation and either establish
     the missing precondition first or, if impossible due to
     permissions/tooling/VCS policy, stop and report `BLOCKED` as defined in
     `CORE/VERSION_CONTROL_SYSTEM.md`.
2. Confirm behavior goals, acceptance criteria, and scope boundaries.
3. Locate semantic parent docs using `CORE/RULE_DEPENDENCY_TREE.md` and the
   relevant index docs (`LANGUAGE/LANGUAGE.md`, `DESIGN/DESIGN.md`,
   `ARCHITECTURE/ARCHITECTURE.md`, `FRAMEWORK/FRAMEWORK.md`,
   `LIBRARY/LIBRARY.md`, `BUILD_TOOLS/BUILD_TOOLS.md`,
   `INFRASTRUCTURE/INFRASTRUCTURE.md`, `CI-CD/CI-CD.md`).
4. Design minimal-change implementation path.
5. Implement with explicit error handling and observability where relevant.
6. Add/update tests and run verification.
7. Summarize changes, risks, and validation evidence.

## Implementation Quality Rules
- SHOULD keep changes scoped; avoid unrelated refactors.
- SHOULD prefer explicit, readable logic over compact clever solutions.
- SHOULD keep boundaries clear (domain vs transport vs infrastructure).
- SHOULD keep side effects explicit and controlled.
- SHOULD preserve backward compatibility unless change explicitly requires breakage.

## Dependency and Tooling Decisions
- SHOULD avoid new dependencies unless necessary and justified.
- SHOULD evaluate new dependencies using `FRAMEWORK/FRAMEWORK.md`, `LIBRARY/LIBRARY.md`, and `COMPLIANCE/LICENSES.md`.
- SHOULD keep runtime/build impact of dependency additions explicit.

## Verification Requirements
- SHOULD add tests for new behavior and bug fixes.
- SHOULD add regression tests before risky refactors where behavior is ambiguous.
- SHOULD run relevant checks locally/CI and report outcomes.
- If checks were not run, state why and expected risk.

## Delivery and Documentation
- SHOULD update user/developer docs when behavior or usage changes.
- SHOULD keep commit/PR summaries explicit about what changed and why.
- SHOULD document notable tradeoffs and deferred follow-ups.
- SHOULD include the completion status contract defined in `CORE/VERSION_CONTROL_SYSTEM.md`.
