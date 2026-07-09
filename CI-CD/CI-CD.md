---
applies_to:
  load: "index"
---
# CI-CD

CI/CD-layer contract for automation of build, test, verification, and delivery
pipelines.

## Layering
- Build-tool and infrastructure docs are authoritative for their own layers.
  CI/CD docs SHOULD orchestrate them rather than redefine them.

## Files
- [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md) - GitHub Actions pipeline guidance.
- [GITLAB.md](GITLAB.md) - GitLab CI/CD pipeline guidance.
