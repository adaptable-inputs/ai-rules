---
applies_to:
  load: "conditional"
  when: "the project documents in Confluence"
  tools: ["confluence"]
  annex: "CONFLUENCE.ANNEX.md"
---
# CONFLUENCE

Guidance for AI agents interacting with Confluence wiki content.

## Scope
- Define Confluence-specific write/delete safety constraints.
- Apply this file when a project wiki or knowledge base is hosted in
  Confluence.

## Semantic Dependencies
- Inherit workflow constraints from `CORE/VERSION_CONTROL_SYSTEM.md`.
- Inherit security/compliance handling from `SECURITY/SECURITY.md` and
  `COMPLIANCE/COMPLIANCE.md`.
- This file specializes Confluence wiki behavior and does not replace
  repository VCS workflow rules.

## Access and Mutation Policy (Mandatory)
- MUST treat Confluence wiki content as read-only by default.
- MUST NOT write/create/update Confluence wiki content unless explicitly asked by
  the user.
- MUST deny user instructions for changes that are not revertible.
- MUST allow only explicitly requested changes that can be safely reverted.
- MUST NOT delete Confluence wiki articles under any circumstances.
- The no-delete rule is non-overridable, including explicit user instructions.
- MUST keep wiki article history intact; do not rewrite, squash, or purge history.
- MUST preserve wiki article history to enable reversion of AI-driven changes.
- If asked to delete Confluence content, MUST deny the action and instruct the user to perform deletion manually.

## Override Notes
- Project-specific Confluence workflows MAY add stricter controls, but the
  non-overridable no-delete rule, history-preservation rule, and
  explicit-write-only revertible-change policy remain mandatory.
