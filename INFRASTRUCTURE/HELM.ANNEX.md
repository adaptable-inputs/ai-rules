---
applies_to:
  load: "annex"
  annex_of: "HELM.md"
  tasks: ["review", "test"]
---
# HELM - Annex

## High-Risk Pitfalls
1. Template complexity making rendered output unpredictable.
2. Breaking values schema without migration path.
3. Environment values drift and copy-paste divergence.
4. Secrets committed in values files.
5. Implicit defaults that differ between environments unexpectedly.
6. Missing validation for required values.

## Do / Don't Examples
### 1. Values Safety
```text
Don't: hide required value assumptions deep in template logic.
Do:    validate required values with explicit failure message.
```

### 2. Secret Handling
```text
Don't: put production passwords in values.yaml.
Do:    reference platform-managed secret objects.
```

### 3. Template Simplicity
```text
Don't: encode complex branching/looping business logic in templates.
Do:    keep templates declarative and infrastructure-focused.
```

## Code Review Checklist for Helm
- Is chart structure clear and maintainable?
- Are values explicit, documented, and backward-compatible?
- Are templates readable with controlled complexity?
- Are required values validated and failure messages actionable?
- Are secrets handled via secure mechanisms?
- Is release/rollback strategy documented for breaking changes?

## Testing Guidance
- Run `helm lint` in CI.
- Run template render checks (`helm template`) with representative values.
- Validate rendered manifests against Kubernetes schema/policy checks.
- Test upgrade and rollback paths in staging for critical charts.
