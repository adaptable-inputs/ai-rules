---
applies_to:
  load: "annex"
  annex_of: "RULE_DEPENDENCY_TREE.md"
  tasks: ["review", "test"]
---
# RULE_DEPENDENCY_TREE - Annex

## Code Review Checklist (Dependency Integrity)
- Does the PR preserve precedence order and semantic inheritance?
- Does the change preserve DIP direction (no parent-to-child references outside
  pure index linking)?
- Are new rules placed at the correct abstraction layer?
- Do specialized docs avoid weakening cross-cutting baseline constraints?
- Are required companion index updates included when adding new docs?
- Does the change introduce new semantic parents that require follow-up issues?
