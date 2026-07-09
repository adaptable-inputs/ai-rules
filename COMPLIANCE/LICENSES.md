---
applies_to:
  load: "always"
  annex: "LICENSES.ANNEX.md"
  purpose: "dependency-license acceptance and release-compliance workflow"
  inherits: ["COMPLIANCE/COMPLIANCE.md"]
---
# LICENSES

Guidance for AI agents on software-license decisions in commercial closed-source contexts.

This is engineering policy guidance, not legal advice. Consult legal counsel for final legal decisions.

## Decision Framework
For each dependency (direct and significant transitive):
1. Identify authoritative license (SPDX + source repository/license file).
2. Classify risk (permissive / conditional / restricted).
3. Confirm obligations (notice, attribution, source disclosure, copyleft scope).
4. Verify compatibility with closed-source distribution model.
5. Record decision in dependency inventory/ADR when material.

## Generally Compatible (Permissive)
Typically acceptable for commercial closed-source use:
- Apache-2.0
- MIT
- BSD-2-Clause / BSD-3-Clause
- ISC
- Zlib
- BSL-1.0
- CC0-1.0
- Unlicense

## Conditional Licenses (Review Required)
Potentially acceptable with constraints and legal review:
- MPL-2.0
- LGPL-2.1-only / LGPL-2.1-or-later
- LGPL-3.0-only / LGPL-3.0-or-later
- EPL-2.0
- CDDL-1.0

## Generally Not Compatible for Closed-Source Distribution
Avoid unless legal explicitly approves alternative model:
- GPL-2.0-only / GPL-2.0-or-later
- GPL-3.0-only / GPL-3.0-or-later
- AGPL-3.0-only / AGPL-3.0-or-later
- SSPL-1.0
- Commons Clause / non-commercial-restricted licenses

## Attribution and Notice Workflow
- MUST preserve required copyright/license notices.
- For distributed artifacts, MUST maintain `THIRD_PARTY_NOTICES.md` in the project root
  (or an explicitly documented equivalent path).
- MUST include NOTICE file obligations (for example Apache-2.0) in release outputs.
- MUST keep attribution metadata updated on dependency upgrades/removals.

## Transitive Dependency Governance
- MUST evaluate transitive licenses, not only direct dependencies.
- MUST flag unknown/custom licenses for manual review.
- MUST block merges/releases with unresolved license status.

## Testing and Validation Guidance
- MUST run automated license scan in CI for every dependency change.
- MUST run full license + notice validation before release creation.
- SHOULD diff dependency tree on upgrades to detect new license obligations.
- SHOULD keep manual review log for exceptions and legal decisions.

## Override Notes
- Downstream framework/library/build-tool docs MUST comply with this policy.
