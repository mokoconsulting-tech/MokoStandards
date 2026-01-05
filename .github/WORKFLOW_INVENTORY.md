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

| # | Workflow | LOC | Complexity | Secrets Used | Migration Decision |
|---|----------|-----|------------|--------------|-------------------|
| 1 | php_quality.yml | TBD | Medium | Org Secrets | **Centralize to .github-private** |
| 2 | release_pipeline.yml | TBD | High | Org Secrets | **Centralize to .github-private** |
| 3 | deploy_staging.yml | TBD | High | Org Secrets | **Centralize to .github-private** |
| 4 | joomla_testing.yml | TBD | Medium | Org Secrets | **Centralize to .github-private** |
| 5 | ci.yml | 98 | Low | None | **Keep Local** |
| 6 | repo_health.yml | 651 | High | GH_PAT | **Keep Local** |
| 7 | version_branch.yml | TBD | Medium | GH_PAT | **Keep Local** |
| 8 | codeql-analysis.yml | 93 | Low | None | Keep Local (security) |
| 9 | changelog_update.yml | 76 | Medium | GH_PAT | Evaluate |
| 10 | version_release.yml | 169 | High | GH_PAT | Evaluate |
| 11 | rebuild_docs_indexes.yml | 92 | Medium | GH_PAT | Evaluate |
| 12 | setup_project_v2.yml | 72 | Medium | GH_PAT | Evaluate |
| 13 | setup_project_7.yml | 92 | Medium | GH_PAT | Evaluate |
| 14 | sync_docs_to_project.yml | 225 | High | GH_PAT | Evaluate |

**Decision Summary:**
- **Centralize (4):** php_quality.yml, release_pipeline.yml, deploy_staging.yml, joomla_testing.yml
- **Keep Local (3):** ci.yml, repo_health.yml, version_branch.yml
- **Other (7):** Existing workflows to evaluate separately

## Shared Scripts

The following Python scripts will be shared across repositories via `.github-private`:

| Script | Purpose | Current Location | Target Location |
|--------|---------|------------------|-----------------|
| `extension_utils.py` | Joomla extension utilities | Repository-specific | `.github-private/scripts/` |
| `common.py` | Common helper functions | Repository-specific | `.github-private/scripts/` |

These scripts will be:
- Versioned and maintained centrally
- Imported via GitHub Actions checkout from `.github-private`
- Available to all workflows with organization access
- Documented with clear API contracts

## Secret Configuration

All secrets are configured at **organization level** with inheritance:

| Secret Type | Scope | Usage |
|-------------|-------|-------|
| Deployment Keys | Organization | All deployment workflows |
| API Tokens | Organization | Release and quality workflows |
| Registry Credentials | Organization | Docker/package publishing |
| Service Accounts | Organization | External integrations |

**Inheritance Pattern:**
```yaml
jobs:
  deploy:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/deploy-staging.yml@main
    secrets: inherit  # All org secrets automatically available
```

## Detailed Workflow Analysis

### Workflows to Centralize to .github-private

### 1. php_quality.yml - PHP Code Quality Analysis

**Purpose:** Automated PHP code quality checks including linting, static analysis, and coding standards

**Triggers:**
- Push to main and development branches
- Pull requests to main

**Jobs:**
- PHP syntax validation
- PHP_CodeSniffer (PHPCS) compliance
- PHPStan static analysis
- Psalm type checking
- Mess Detector checks

**Dependencies:**
- PHP 7.4-8.2
- Composer
- Quality tools (phpcs, phpstan, psalm)
- `extension_utils.py` for Joomla-specific checks

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/php-quality.yml`

**Migration Complexity:** Medium - Requires PHP tool setup and shared script integration

**Secrets Required:**
- Organization-level secrets for package registries (if using private dependencies)

**Shared Scripts:** `extension_utils.py`, `common.py`

---

### 2. release_pipeline.yml - Automated Release Management

**Purpose:** Complete release automation including building, testing, packaging, and publishing

**Triggers:**
- Manual workflow_dispatch with version input
- Tag creation matching release pattern

**Jobs:**
- Version validation
- Build artifacts (ZIP packages for Joomla/Dolibarr)
- Generate checksums (SHA256)
- Create GitHub Release
- Publish to marketplaces
- Update documentation
- Notify stakeholders

**Dependencies:**
- Build tools (zip, tar)
- Checksum utilities
- GitHub CLI
- Marketplace APIs
- `extension_utils.py` for package creation

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/release-pipeline.yml`

**Migration Complexity:** High - Complex multi-step process with external integrations

**Secrets Required:**
- Marketplace API tokens (organization-level)
- Signing keys for packages
- Release notification webhooks

**Shared Scripts:** `extension_utils.py`, `common.py`

---

### 3. deploy_staging.yml - Staging Environment Deployment

**Purpose:** Automated deployment to staging environments for testing before production

**Triggers:**
- Push to develop branch
- Manual workflow_dispatch
- Successful completion of quality checks

**Jobs:**
- Build deployment package
- Deploy to staging server
- Run smoke tests
- Health check validation
- Rollback on failure

**Dependencies:**
- SSH/SFTP access to staging
- Deployment scripts
- Health check endpoints
- `common.py` for deployment utilities

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/deploy-staging.yml`

**Migration Complexity:** High - Requires secure credential handling and deployment logic

**Secrets Required:**
- Staging server credentials (organization-level)
- Deployment keys
- Notification webhooks

**Shared Scripts:** `common.py`

---

### 4. joomla_testing.yml - Joomla Extension Testing

**Purpose:** Comprehensive testing for Joomla extensions across multiple PHP and Joomla versions

**Triggers:**
- Push to main and development branches
- Pull requests
- Schedule: Nightly

**Jobs:**
- Unit tests with PHPUnit
- Integration tests with Joomla instances
- Matrix testing (PHP 7.4-8.2 × Joomla 4.4-5.1)
- Code coverage reporting
- Extension installation tests

**Dependencies:**
- PHP 7.4-8.2
- MySQL/MariaDB
- Joomla CMS installations
- PHPUnit
- `extension_utils.py` for installation testing

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/joomla-testing.yml`

**Migration Complexity:** High - Complex test matrix and Joomla setup

**Secrets Required:**
- Code coverage service tokens (organization-level)
- Test environment credentials

**Shared Scripts:** `extension_utils.py`, `common.py`

---

### Workflows to Keep Local

### 5. ci.yml - Continuous Integration

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

**Decision:** **Keep Local**

**Rationale:** 
- Repository-specific validation rules
- No sensitive proprietary logic in this workflow
- Fast iteration without cross-repo dependencies
- Public transparency for CI process

---

### 6. repo_health.yml - Repository Health & Governance

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

**Decision:** **Keep Local**

**Rationale:**
- Repository governance is repo-specific
- Complex proprietary validation logic best maintained locally
- Frequent updates needed for repository-specific rules
- Admin-only execution gate works better locally

**Note:** While this contains proprietary governance logic, keeping it local allows for repository-specific customization and faster iteration.

---

### 7. version_branch.yml - Version Branch Management

**Purpose:** Automated creation and management of version-specific branches

**Triggers:**
- Manual workflow_dispatch with version parameters
- Release creation events

**Jobs:**
- Version branch creation
- Branch protection setup
- Documentation updates
- Changelog initialization

**Dependencies:**
- Git operations
- Branch protection API
- Documentation generator

**Decision:** **Keep Local**

**Rationale:**
- Repository-specific branching strategies
- Different versioning schemes per repository
- Fast iteration on branching logic
- No sensitive deployment credentials

---

### 8. codeql-analysis.yml - Security Code Scanning

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

**Decision:** **Keep Local** (security best practice)

**Rationale:**
- Standard GitHub security feature
- Public transparency for security scanning
- Best practice to keep in public repositories
- No customization needed

---

### Other Existing Workflows (To Evaluate Separately)

### 9. changelog_update.yml - Changelog Management

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

**Decision:** Evaluate - May keep local or integrate with release_pipeline.yml

---

### 10. version_release.yml - Version Management

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

**Decision:** Evaluate - May integrate with release_pipeline.yml or keep local

---

### 11. rebuild_docs_indexes.yml - Documentation Index Generation

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

**Decision:** Evaluate - Repository-specific documentation may warrant keeping local

---

### 12. setup_project_v2.yml - GitHub Projects v2 Setup

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

**Decision:** Evaluate - Project automation may benefit from centralization

---

### 13. setup_project_7.yml - Project #7 Specific Setup

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

**Decision:** Evaluate - May merge with setup_project_v2.yml

---

### 14. sync_docs_to_project.yml - Documentation Project Sync

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

**Decision:** Evaluate - Project sync may benefit from centralization

---

## Secret Dependencies

### Organization-Level Secrets (Configured)

All secrets are configured at **organization level** with automatic inheritance to workflows:

| Secret Category | Specific Secrets | Used By | Purpose |
|-----------------|------------------|---------|---------|
| **Deployment** | STAGING_SSH_KEY, STAGING_HOST | deploy_staging.yml | Staging deployment |
| **Releases** | MARKETPLACE_TOKEN, JED_API_KEY | release_pipeline.yml | Marketplace publishing |
| **Quality** | CODECOV_TOKEN, SONAR_TOKEN | php_quality.yml, joomla_testing.yml | Code coverage/quality |
| **Testing** | TEST_DB_PASSWORD | joomla_testing.yml | Test database setup |
| **General** | GH_PAT | Various | GitHub API access |

### Inheritance Pattern

Workflows use `secrets: inherit` to access all organization secrets:

```yaml
jobs:
  quality:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main
    secrets: inherit  # Automatically inherits all org secrets
```

**Benefits:**
- Single source of truth for secrets
- No per-repository secret configuration
- Automatic rotation across all repositories
- Centralized access control

## Script Dependencies

### Shared Scripts (Move to .github-private)

| Script | Used By | Purpose | Target Location |
|--------|---------|---------|-----------------|
| **extension_utils.py** | php_quality.yml, joomla_testing.yml, release_pipeline.yml | Joomla extension operations | `.github-private/scripts/` |
| **common.py** | All centralized workflows | Common utilities | `.github-private/scripts/` |

**Usage Pattern in Workflows:**
```yaml
- name: Checkout shared scripts
  uses: actions/checkout@v4
  with:
    repository: mokoconsulting-tech/.github-private
    path: .github-private
    token: ${{ secrets.GH_PAT }}

- name: Use shared scripts
  run: |
    python .github-private/scripts/extension_utils.py
```

### Repository-Specific Scripts (Keep Local)

| Script | Used By | Migration Action |
|--------|---------|------------------|
| `scripts/validate/*` | ci.yml | Keep in repository (repo-specific) |
| `scripts/docs/rebuild_indexes.py` | rebuild_docs_indexes.yml | Keep in repository |
| `scripts/setup_project_v2.py` | setup_project_v2.yml | Evaluate for centralization |
| `scripts/setup_project_7.py` | setup_project_7.yml | Evaluate for centralization |
| `scripts/sync_file_to_project.py` | sync_docs_to_project.yml | Evaluate for centralization |

## Migration Priority Matrix

### Centralize to .github-private (Priority 1)
1. **php_quality.yml** - PHP code quality analysis with shared scripts
2. **release_pipeline.yml** - Release automation with marketplace integration
3. **deploy_staging.yml** - Staging deployment with sensitive credentials
4. **joomla_testing.yml** - Comprehensive Joomla testing matrix

### Keep Local (Decided)
5. **ci.yml** - Repository-specific validation
6. **repo_health.yml** - Repository governance (proprietary but repo-specific)
7. **version_branch.yml** - Repository-specific branching
8. **codeql-analysis.yml** - Security best practice (keep public)

### Evaluate Later
9. **changelog_update.yml** - May integrate with release_pipeline.yml
10. **version_release.yml** - May integrate with release_pipeline.yml  
11. **rebuild_docs_indexes.yml** - Repository-specific documentation
12. **setup_project_v2.yml** - Project automation
13. **setup_project_7.yml** - Project automation
14. **sync_docs_to_project.yml** - Project sync

## Reusable Workflow Structure

### Finalized .github-private Layout

```
.github-private/
├── .github/
│   └── workflows/
│       ├── reusable/
│       │   ├── php-quality.yml           (php_quality.yml)
│       │   ├── release-pipeline.yml      (release_pipeline.yml)
│       │   ├── deploy-staging.yml        (deploy_staging.yml)
│       │   └── joomla-testing.yml        (joomla_testing.yml)
│       └── templates/
│           ├── php-quality-template.yml
│           ├── release-template.yml
│           ├── deploy-template.yml
│           └── testing-template.yml
├── scripts/
│   ├── extension_utils.py                (shared across repos)
│   ├── common.py                         (shared across repos)
│   └── README.md
└── docs/
    ├── README.md
    ├── workflow-usage.md
    └── script-api.md
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
