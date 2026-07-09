---
applies_to:
  load: "conditional"
  when: "Istio resources are present"
  tools: ["istio"]
  annex: "ISTIO.ANNEX.md"
---
# ISTIO

Guidance for AI agents implementing and reviewing Istio service mesh policies.

## Scope
- Define Istio traffic, security, and observability policy defaults.
- Apply this file to VirtualService, DestinationRule, Gateway, and security
  policy design.

## Semantic Dependencies
- Inherit Kubernetes baseline from `INFRASTRUCTURE/KUBERNETES.md`.
- Inherit resilience constraints from `ARCHITECTURE/CIRCUIT_BREAKER.md`.
- Inherit security constraints from `SECURITY/SECURITY.md`.

## Defaults
- SHOULD keep traffic policies explicit and versioned.
- SHOULD keep retries/timeouts bounded and aligned with service SLOs.
- SHOULD use progressive rollout patterns for risky changes.
- SHOULD keep policy scope minimal (namespace/service targeted).

## Traffic Management Rules
- SHOULD define clear routing intent in VirtualService rules.
- SHOULD avoid conflicting route matches and overlapping wildcard policies.
- SHOULD coordinate retries, timeouts, and outlier detection to avoid traffic storms.
- SHOULD use canary/weighted rollout for high-risk changes.
- SHOULD keep gateway ingress exposure tightly controlled.

## Security Rules
- MUST enforce mTLS according to environment policy.
- MUST use AuthorizationPolicy with least privilege.
- MUST keep trust-domain and identity assumptions explicit.
- SHOULD avoid permissive policies as long-term defaults.

## Observability and Operations
- SHOULD ensure mesh telemetry is enabled and consumed meaningfully.
- SHOULD track latency, error rate, retry count, and outlier ejection behavior.
- SHOULD alert on policy-induced failures (5xx spikes, route blackholes).
- SHOULD keep config changes auditable and rollback-ready.

## Override Notes
- Platform governance MAY enforce stricter mesh controls, but explicit traffic
  safety, least privilege, and observability constraints here remain mandatory.
