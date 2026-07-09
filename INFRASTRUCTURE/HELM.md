---
applies_to:
  load: "conditional"
  when: "Chart.yaml is present"
  tools: ["helm"]
  annex: "HELM.ANNEX.md"
  purpose: "Helm chart authoring, templating, and release management rules"
  inherits: ["INFRASTRUCTURE/KUBERNETES.md", "LANGUAGE/YAML/YAML.md", "SECURITY/SECURITY.md"]
---
# HELM

Guidance for AI agents implementing and reviewing Helm charts.

## Defaults
- SHOULD keep charts small, purpose-focused, and versioned.
- SHOULD keep values explicit and documented.
- SHOULD keep templates readable; avoid over-abstracted logic.
- SHOULD keep environment overrides controlled and minimal.

## Chart Structure and Values Governance
- SHOULD keep default `values.yaml` safe and production-aware.
- SHOULD group values by domain concern (image, resources, probes, ingress, etc.).
- SHOULD avoid hidden behavior behind implicit defaults.
- SHOULD prefer explicit booleans/enums over magic strings.
- SHOULD keep backward compatibility for chart consumers when evolving values.

## Templating Rules
- SHOULD prefer simple, readable template expressions.
- SHOULD avoid deep nested conditionals in templates.
- SHOULD use helper templates for repeated fragments.
- SHOULD validate required values explicitly (fail early with clear messages).
- SHOULD avoid business logic in chart templates.

## Release and Upgrade Strategy
- SHOULD use semantic versioning for charts.
- SHOULD document breaking value/schema changes clearly.
- SHOULD prefer additive changes and deprecation windows.
- SHOULD keep rollback strategy tested for critical services.

## Security and Secret Handling
- MUST NOT commit plaintext secrets in chart values.
- MUST integrate secret management mechanisms (sealed/external secrets) as policy requires.
- MUST keep service account and security context defaults least-privilege.
