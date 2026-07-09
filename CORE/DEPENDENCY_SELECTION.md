---
applies_to:
  load: "conditional"
  when: "the task adds, replaces, or upgrades a framework, library, or build tool"
  purpose: "criteria for choosing a framework, library, or build-tool dependency"
  inherits: ["COMPLIANCE/LICENSES.md"]
---
# DEPENDENCY_SELECTION

Criteria for choosing a new framework, library, or build tool. These rules once
lived in the `FRAMEWORK/`, `LIBRARY/`, and `BUILD_TOOLS/` category indexes, which
an agent no longer reads.

## Defaults
- SHOULD prefer mature, enterprise-ready dependencies with a proven track record.
  Popularity is a strong indicator: a widely adopted dependency is more likely to
  be maintained and supported long term.
- SHOULD prefer trustworthy stewardship (for example the Apache Foundation, the
  Linux Foundation, major vendors, or well-governed communities) over a
  one-person side project.
- SHOULD NOT adopt a very new dependency without evidence of long-term
  sustainability.
- SHOULD prefer clear release cadences, published support windows, and strong
  maintenance.
- SHOULD prefer comprehensive feature sets over hype-driven adoption.
- SHOULD prefer the standard build tool for the language or ecosystem unless a
  strong, explicit reason exists to deviate.
- MUST ensure licenses are compatible with commercial closed-source use and that
  required attribution is provided; see `COMPLIANCE/LICENSES.md`.
