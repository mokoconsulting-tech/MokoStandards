# MokoStandards Override Configuration

## Overview

The `MokoStandards.override.tf` file controls how the bulk repository sync process handles files in the MokoStandards repository. Since MokoStandards serves as a template repository, it needs special handling to prevent circular overwrites.

## Summary

**Excluded Files (10):** Template workflows that should NOT exist in MokoStandards
**Protected Files (35):** MokoStandards-specific files that must be preserved

## Key Points

- `exclude_files`: Prevents template workflows from being created in MokoStandards
- `protected_files`: Preserves MokoStandards-specific workflows and configurations
- Version: 2.1.0 (updated 2026-01-30)

## Workflow Categories

### Excluded (Templates - should not exist in MokoStandards)
1. build.yml
2. ci.yml
3. code-quality.yml
4. codeql-analysis.yml
5. dependency-review.yml
6. deploy-to-dev.yml
7. release-cycle.yml
8. terraform-ci.yml
9. terraform-deploy.yml
10. terraform-drift.yml

### Protected (MokoStandards-specific - must be preserved)

#### Repository Automation (14)
- auto-create-dev-branch.yml
- auto-create-org-projects.yml
- auto-release-on-version-bump.yml
- auto-release.yml
- auto-update-changelog.yml
- bulk-label-deployment.yml
- bulk-repo-sync.yml (CRITICAL)
- confidentiality-scan.yml
- enterprise-firewall-setup.yml
- enterprise-issue-manager.yml
- flush-actions-cache.yml
- repo-health.yml
- standards-compliance.yml
- sync-changelogs.yml

#### Reusable Workflows (8)
- reusable-build.yml
- reusable-ci-validation.yml
- reusable-deploy.yml
- reusable-php-quality.yml
- reusable-platform-testing.yml
- reusable-project-detector.yml
- reusable-release.yml
- reusable-script-executor.yml

#### Configuration Files (8)
- .gitignore
- .editorconfig
- MokoStandards.override.tf
- README.md
- CONTRIBUTING.md
- .github/copilot.yml
- .github/org-settings.yml
- .github/issue-management-config.yml

#### Directories (5)
- templates/
- scripts/
- docs/
- terraform/
- scripts/automation/bulk_update_repos.py

## Maintenance

When adding a new template workflow:
1. Add to `exclude_files` in MokoStandards.override.tf
2. Update version and timestamp

When adding a MokoStandards-specific workflow:
1. Add to `protected_files` in MokoStandards.override.tf
2. Update version and timestamp

## Validation

```bash
python3 << 'EOF'
with open('MokoStandards.override.tf', 'r') as f:
    content = f.read()
print(f"Braces: {content.count('{')} open, {content.count('}')} close")
print(f"Brackets: {content.count('[')} open, {content.count(']')} close")
EOF
```

---
**Version:** 2.1.0 | **Updated:** 2026-01-30 | **Maintainer:** MokoStandards Team
