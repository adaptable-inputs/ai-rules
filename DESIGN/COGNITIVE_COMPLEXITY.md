---
applies_to:
  load: "always"
  annex: "COGNITIVE_COMPLEXITY.ANNEX.md"
  purpose: "mandatory and target limits for method cognitive complexity"
  inherits: ["CORE/RULE_DEPENDENCY_TREE.md", "DESIGN/CLEAN_CODE.md", "DESIGN/SOLID.md"]
---
# COGNITIVE_COMPLEXITY

Guidance for AI agents to control method-level cognitive complexity.

## Cognitive Complexity Targets
- New methods MUST have cognitive complexity `<= 15`.
- Altered existing methods SHOULD have cognitive complexity `<= 15`.
- Altered legacy methods MAY reach `20` only when behavior risk is high and the PR includes a documented reduction plan.
- If an altered legacy method stays above `20`, MUST create or link a follow-up issue with an explicit reduction plan.

Definition used in this document:
- Legacy method: a method that already existed before the current change and had cognitive complexity above the
  encouraged target (`> 15`) at change start.

These thresholds align with typical static-analysis defaults (for example SonarQube/SonarCloud) and common IDE plugin
conventions.

## Metric Determination and Evidence
An agent MUST use the strongest available source in this order:
1. SonarQube/SonarCloud result for the branch/PR (preferred when available).
2. IDE/static-analysis plugin result (for example SonarLint/IntelliJ plugin).
3. Agent-side estimate when no tool result is available.

When using an estimate, an agent MUST state that it is an estimate and MUST apply the same thresholds conservatively.

## Complexity Reduction Heuristics
- SHOULD extract nested decision logic into named methods with single responsibility.
- SHOULD prefer early return/guard clauses to flatten nested condition pyramids.
- SHOULD separate orchestration from domain decision logic.
- SHOULD replace branch-heavy variant handling with Strategy/Polymorphism where variation is stable.
- SHOULD keep cross-cutting concerns out of core methods
  (use focused wrappers/aspects only for the cross-cutting concerns listed in `DESIGN/AOP.md`).
- MUST use `DESIGN/EARLY_RETURN.md` for guard-clause defaults, guardrails, and caveats.
