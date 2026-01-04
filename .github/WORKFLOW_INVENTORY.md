<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
PATH: /.github/WORKFLOW_INVENTORY.md
VERSION: 01.00.00
BRIEF: Complete inventory of GitHub Actions workflows for migration planning
-->

# GitHub Actions Workflow Inventory

## Overview

This document provides a complete inventory of all GitHub Actions workflows in the MokoStandards repository, prepared for migration to `.github-private` repository.

## Workflow Summary

| # | Workflow | LOC | Complexity | Secrets Used | Migration Priority |
|---|----------|-----|------------|--------------|-------------------|
| 1 | ci.yml | 98 | Low | None | Standard |
| 2 | repo_health.yml | 651 | High | GH_PAT | High |
| 3 | codeql-analysis.yml | 93 | Low | None | Standard |
| 4 | changelog_update.yml | 76 | Medium | GH_PAT | Standard |
| 5 | version_release.yml | 169 | High | GH_PAT | High |
| 6 | rebuild_docs_indexes.yml | 92 | Medium | GH_PAT | Standard |
| 7 | setup_project_v2.yml | 72 | Medium | GH_PAT | High |
| 8 | setup_project_7.yml | 92 | Medium | GH_PAT | High |
| 9 | sync_docs_to_project.yml | 225 | High | GH_PAT | High |

**Total:** 9 workflows, ~1,568 lines of YAML

## Detailed Workflow Analysis

### 1. ci.yml - Continuous Integration

**Purpose:** Validate repository standards and run compliance checks

**Triggers:**
- Push to main, dev/**, rc/**, version/** branches
- Pull requests to main, dev/**, rc/**, version/** branches

**Jobs:**
- Repository validation pipeline
- Script executability verification
- Required and optional validations

**Dependencies:**
- Scripts in `scripts/validate/`
- Python 3.x
- ShellCheck

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/ci-validation.yml`

**Migration Complexity:** Low - No sensitive logic, straightforward conversion

---

### 2. repo_health.yml - Repository Health & Governance

**Purpose:** Comprehensive repository health checks and governance validation

**Triggers:**
- Manual workflow_dispatch with profile selection
- Push to main (workflows, scripts, docs paths)
- Pull requests to main

**Jobs:**
- Admin-only execution gate
- Scripts governance validation
- Repository artifact validation
- Content heuristics
- Extended health checks
- Audit trail generation

**Dependencies:**
- Python 3.x for JSON processing
- ShellCheck
- Various governance artifacts

**Migration Type:** Convert to reusable workflow with profile parameter

**Proposed Location:** `.github-private/.github/workflows/reusable/repo-health-check.yml`

**Migration Complexity:** High - Complex logic, multiple execution paths

**Sensitive Content:** 
- Proprietary governance rules
- Organization-specific validation logic

---

### 3. codeql-analysis.yml - Security Code Scanning

**Purpose:** Automated security vulnerability detection using CodeQL

**Triggers:**
- Push to main
- Pull requests to main
- Schedule: Weekly on Mondays

**Jobs:**
- CodeQL analysis for multiple languages
- Security alert generation

**Dependencies:**
- GitHub CodeQL action
- Language detection

**Migration Type:** Keep local (standard GitHub security feature)

**Proposed Location:** Stay in `.github/workflows/` (public best practice)

**Migration Complexity:** N/A - Should remain local

**Note:** CodeQL workflows typically stay in public repositories for transparency

---

### 4. changelog_update.yml - Changelog Management

**Purpose:** Automated CHANGELOG.md updates and validation

**Triggers:**
- Push to main
- Manual workflow_dispatch

**Jobs:**
- Changelog validation
- Automatic updates
- Commit and push changes

**Dependencies:**
- Python 3.x
- GH_PAT secret

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/changelog-management.yml`

**Migration Complexity:** Medium - Requires GH_PAT handling

---

### 5. version_release.yml - Version Management

**Purpose:** Automated version bumping and release creation

**Triggers:**
- Manual workflow_dispatch with version inputs

**Jobs:**
- Version validation
- File updates
- Branch creation
- Changelog updates
- Governance checks

**Dependencies:**
- Python 3.x
- GH_PAT secret
- Multiple governance artifacts

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/version-management.yml`

**Migration Complexity:** High - Complex version logic, governance checks

**Sensitive Content:**
- Version bumping strategy
- Release process automation

---

### 6. rebuild_docs_indexes.yml - Documentation Index Generation

**Purpose:** Automatically rebuild documentation index files

**Triggers:**
- Push to main (docs/ and templates/ paths)
- Pull requests to main
- Manual workflow_dispatch

**Jobs:**
- Run Python script to generate indexes
- Commit and push changes

**Dependencies:**
- Python 3.x
- `scripts/docs/rebuild_indexes.py`
- GH_PAT secret

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/docs-automation.yml`

**Migration Complexity:** Low - Simple script execution

---

### 7. setup_project_v2.yml - GitHub Projects v2 Setup

**Purpose:** Automated GitHub Projects v2 creation and configuration

**Triggers:**
- Manual workflow_dispatch with project parameters

**Jobs:**
- Project creation
- Field configuration
- Item population

**Dependencies:**
- Python 3.x
- GitHub GraphQL API
- GH_PAT secret
- Project setup scripts

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/project-automation.yml`

**Migration Complexity:** High - API interactions, complex setup logic

**Sensitive Content:**
- Project templates
- Field configurations

---

### 8. setup_project_7.yml - Project #7 Specific Setup

**Purpose:** Specialized setup for Project #7 with version tracking

**Triggers:**
- Manual workflow_dispatch with version parameters

**Jobs:**
- Project #7 creation/update
- Version field configuration
- Documentation tagging

**Dependencies:**
- Python 3.x
- GitHub GraphQL API
- GH_PAT secret
- `scripts/setup_project_7.py`

**Migration Type:** Merge with setup_project_v2.yml into unified workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/project-automation.yml`

**Migration Complexity:** Medium - Can be consolidated

---

### 9. sync_docs_to_project.yml - Documentation Project Sync

**Purpose:** Sync documentation files to GitHub Project items

**Triggers:**
- Push to main (docs/ and templates/ paths)
- Manual workflow_dispatch

**Jobs:**
- Scan documentation files
- Create/update project items
- Set custom fields
- Generate sync report

**Dependencies:**
- Python 3.x
- GitHub GraphQL API
- GH_PAT secret
- `scripts/sync_file_to_project.py`

**Migration Type:** Convert to reusable workflow

**Proposed Location:** `.github-private/.github/workflows/reusable/docs-automation.yml`

**Migration Complexity:** High - Complex GraphQL operations

**Sensitive Content:**
- Project sync logic
- Field mappings

---

## Secret Dependencies

| Secret Name | Used By | Purpose | Migration Impact |
|-------------|---------|---------|------------------|
| GH_PAT | repo_health.yml | Push to repository | Must be org secret |
| GH_PAT | changelog_update.yml | Commit changes | Must be org secret |
| GH_PAT | version_release.yml | Create branches/tags | Must be org secret |
| GH_PAT | rebuild_docs_indexes.yml | Commit indexes | Must be org secret |
| GH_PAT | setup_project_v2.yml | GraphQL API access | Must be org secret |
| GH_PAT | setup_project_7.yml | GraphQL API access | Must be org secret |
| GH_PAT | sync_docs_to_project.yml | GraphQL API access | Must be org secret |

**Note:** All workflows using GH_PAT should migrate to use `secrets: inherit` pattern

## Script Dependencies

| Script | Used By | Migration Action |
|--------|---------|------------------|
| `scripts/validate/*` | ci.yml | Keep in repository |
| `scripts/docs/rebuild_indexes.py` | rebuild_docs_indexes.yml | Keep in repository |
| `scripts/setup_project_v2.py` | setup_project_v2.yml | Consider moving to .github-private |
| `scripts/setup_project_7.py` | setup_project_7.yml | Consider moving to .github-private |
| `scripts/sync_file_to_project.py` | sync_docs_to_project.yml | Consider moving to .github-private |

## Migration Priority Matrix

### High Priority (Week 2-3)
1. **repo_health.yml** - Contains proprietary governance logic
2. **version_release.yml** - Sensitive release automation
3. **setup_project_v2.yml** - Project template exposure
4. **setup_project_7.yml** - Can be consolidated with v2
5. **sync_docs_to_project.yml** - Complex proprietary sync logic

### Standard Priority (Week 3-4)
6. **ci.yml** - Standard validation, can migrate for consistency
7. **changelog_update.yml** - Simple automation
8. **rebuild_docs_indexes.yml** - Simple automation

### Keep Local
9. **codeql-analysis.yml** - Security best practice to keep public

## Reusable Workflow Structure

### Proposed .github-private Layout

```
.github-private/
└── .github/
    └── workflows/
        ├── reusable/
        │   ├── ci-validation.yml          (from ci.yml)
        │   ├── repo-health-check.yml      (from repo_health.yml)
        │   ├── version-management.yml     (from version_release.yml)
        │   ├── project-automation.yml     (from setup_project_*.yml)
        │   ├── docs-automation.yml        (from rebuild + sync)
        │   └── changelog-management.yml   (from changelog_update.yml)
        └── templates/
            ├── standard-ci.yml
            ├── standard-release.yml
            └── standard-health.yml
```

## Migration Checklist

### Pre-Migration
- [ ] Create `.github-private` repository
- [ ] Configure repository access
- [ ] Set up organization secrets
- [ ] Document all workflow dependencies
- [ ] Create backup of current workflows

### Per-Workflow Migration
- [ ] Analyze workflow complexity
- [ ] Identify sensitive content
- [ ] Design reusable workflow interface
- [ ] Create reusable workflow in `.github-private`
- [ ] Test reusable workflow in isolation
- [ ] Update caller workflow in public repo
- [ ] Test integration end-to-end
- [ ] Archive old workflow with deprecation notice
- [ ] Update documentation
- [ ] Notify affected teams

### Post-Migration
- [ ] Monitor workflow runs
- [ ] Verify all repositories using new workflows
- [ ] Clean up archived workflows
- [ ] Update repository documentation
- [ ] Conduct team training session
- [ ] Create runbook for common issues

## Risk Assessment

### High Risk
- **Breaking Changes:** Workflow interface changes could break existing implementations
- **Access Issues:** Repository permission problems could block workflow execution
- **Secret Management:** Incorrect secret configuration could expose sensitive data

### Medium Risk
- **Performance:** Additional indirection could slow workflow execution
- **Debugging:** Harder to troubleshoot issues in private repository
- **Maintenance:** Two repositories to manage instead of one

### Low Risk
- **Documentation:** Migration guide reduces knowledge transfer issues
- **Testing:** Comprehensive testing strategy mitigates most risks
- **Rollback:** Clear rollback plan available

## Success Metrics

### Migration Success
- All workflows migrated within 4-week timeline
- Zero downtime or failed runs during migration
- All secrets properly configured
- Complete documentation updated

### Post-Migration Success
- Workflow run success rate > 95%
- Average workflow execution time maintained or improved
- Zero security incidents related to workflow access
- Team satisfaction rating > 4/5

## Metadata

| Field | Value |
|-------|-------|
| Document | Workflow Inventory |
| Path | /.github/WORKFLOW_INVENTORY.md |
| Status | Active |
| Version | 01.00.00 |
| Date | 2026-01-04 |
| Last Updated | 2026-01-04 |

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-04 | Initial inventory created for migration planning | DevOps Team |
