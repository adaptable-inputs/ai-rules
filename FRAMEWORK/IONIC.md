---
applies_to:
  load: "conditional"
  when: "ionic.config.json is present"
  frameworks: ["ionic"]
  annex: "IONIC.ANNEX.md"
  purpose: "Ionic-specific UI, navigation, native-bridge, and mobile-delivery guardrails"
  inherits: ["FRAMEWORK/FRAMEWORK.md", "LANGUAGE/JAVASCRIPT/JAVASCRIPT.md", "LANGUAGE/TYPESCRIPT/TYPESCRIPT.md", "LANGUAGE/HTML/HTML.md", "LANGUAGE/CSS/CSS.md", "FRAMEWORK/ANGULAR.md", "FRAMEWORK/REACT.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# IONIC

Guidance for AI agents implementing and reviewing Ionic applications.

## Defaults and Guardrails
- SHOULD prefer Ionic with Capacitor for modern mobile and web delivery.
- SHOULD prefer official Ionic UI components before creating custom equivalents.
- SHOULD keep UI concerns in pages/components and platform integration in dedicated services/adapters.
- SHOULD keep native plugin usage behind small abstractions to simplify testing and platform fallbacks.
- SHOULD keep loading, empty, offline, and error states explicit for each critical mobile flow.
- SHOULD keep permission usage minimal and only request permissions when needed by a user-initiated action.

## Navigation and Lifecycle
- SHOULD keep route definitions explicit and feature-oriented.
- SHOULD use Ionic page lifecycle hooks only for page-level side effects that cannot be modeled cleanly with
  framework-native patterns.
- SHOULD ensure navigation-triggered async work is cancelable to avoid stale updates after fast route changes.
- SHOULD keep back-navigation behavior deterministic across iOS, Android, and web.

## Native Bridge and Plugin Policy
- SHOULD prefer official Capacitor plugins before third-party plugins.
- SHOULD validate plugin maintenance, platform support, and permission footprint before adoption.
- SHOULD keep platform checks centralized in service boundaries, not scattered through page components.
- SHOULD provide graceful fallback behavior when a capability is unavailable on web or in restricted device contexts.

## Performance and UX
- SHOULD keep first-screen rendering lightweight and lazy-load deeper route trees.
- SHOULD avoid unnecessary re-renders and large synchronous work on interaction paths.
- SHOULD keep list rendering efficient (`trackBy`/stable keys, incremental loading).
- SHOULD keep touch interactions responsive and avoid blocking animations with heavy synchronous logic.

## Security
- MUST NOT render untrusted HTML in Ionic views.
- MUST NOT persist secrets in plaintext storage.
- MUST keep token/session storage strategy aligned with project security policy.
- MUST validate deep-link and external-intent inputs before navigation or execution.
