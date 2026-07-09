---
applies_to:
  load: "annex"
  annex_of: "LICENSES.md"
  tasks: ["review", "test"]
---
# LICENSES - Annex

## High-Risk Pitfalls
1. Approving dependency based only on package registry metadata.
2. Ignoring transitive copyleft obligations.
3. Missing NOTICE/attribution files in release artifacts.
4. License changes on dependency upgrade unnoticed.
5. Assuming "internal use" exception when software is distributed.

## Do / Don't Examples
### 1. License Verification
```text
Don't: trust single registry field blindly.
Do:    verify SPDX + upstream LICENSE file + release notes.
```

### 2. Upgrade Governance
```text
Don't: auto-merge major dependency upgrades without license recheck.
Do:    run license scan and review before merge/release.
```

### 3. Release Compliance
```text
Don't: ship binaries without third-party notices.
Do:    include required notices/licenses with release artifacts.
```

## Code Review Checklist for License Compliance
- Is license classification verified for new/updated dependencies?
- Are transitive licenses scanned and acceptable?
- Are attribution/notice obligations captured and implemented?
- Are restricted/conditional licenses escalated for legal review?
- Are license checks integrated into CI/release gating?
