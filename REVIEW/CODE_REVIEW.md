---
applies_to:
  load: "task"
  tasks: ["review"]
  annex: "CODE_REVIEW.ANNEX.md"
  purpose: "review workflow, prioritization, and output expectations"
  inherits: ["REVIEW/REVIEW.md", "CORE/RULE_DEPENDENCY_TREE.md", "LANGUAGE/LANGUAGE.md", "DESIGN/DESIGN.md", "ARCHITECTURE/ARCHITECTURE.md", "FRAMEWORK/FRAMEWORK.md", "LIBRARY/LIBRARY.md", "BUILD_TOOLS/BUILD_TOOLS.md", "INFRASTRUCTURE/INFRASTRUCTURE.md", "CI-CD/CI-CD.md", "LANGUAGE/**", "DESIGN/**", "ARCHITECTURE/**", "FRAMEWORK/**", "LIBRARY/**", "BUILD_TOOLS/**", "INFRASTRUCTURE/**", "CI-CD/**", "SECURITY/SECURITY.md", "TEST/TEST.md", "COMPLIANCE/COMPLIANCE.md"]
---
# CODE_REVIEW

Guidance for AI agents performing code and rules-document reviews.

## Review Priority Order
1. Correctness and regression risk.
2. Security, privacy, and compliance.
3. Data integrity and error handling.
4. Architecture and boundary violations.
5. Performance and scalability risks.
6. Observability and operational readiness.
7. Maintainability/readability/test adequacy.

## Finding Severity Model
- `Critical`: exploitable security/data-loss/system outage risk.
- `High`: likely production failure or major correctness bug.
- `Medium`: maintainability/performance/reliability risk with non-trivial
  impact.
- `Low`: minor quality issue or consistency gap.

## Finding Format Requirements
Each finding SHOULD include:
- severity,
- impacted file/path reference,
- concrete issue description,
- why it matters (risk),
- actionable remediation guidance.

## Review Coverage Expectations
- SHOULD validate behavior changes against tests.
- SHOULD validate boundary adherence to semantic parent docs.
- SHOULD validate dependency additions for maturity/license/security fit.
- SHOULD validate error-handling and observability for failure paths.
- SHOULD validate migration/compatibility implications where relevant.

## Dependency Review Rules
- New dependencies require explicit justification.
- MUST reject niche/unmaintained dependencies unless strong rationale exists.
- SHOULD verify license compatibility with `COMPLIANCE/LICENSES.md`.
- SHOULD check overlap/redundancy with existing dependencies.

## Output Quality Rules
- SHOULD prioritize concrete findings over summaries.
- SHOULD avoid vague comments; anchor findings to code locations.
- SHOULD distinguish confirmed issues from assumptions/questions.
- State verification gaps explicitly (what was not tested/checked).

## Review Checklist
- Are top-risk categories (correctness/security/compliance) covered first?
- Are findings severity-ranked and actionable?
- Are semantic parent-rule violations identified?
- Are dependency/tooling additions evaluated rigorously?
- Are test/verification gaps clearly documented?
- Is final output concise, concrete, and decision-useful?
