<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
PATH: /.github/CI_MIGRATION_GUIDE.md
VERSION: 01.00.00
BRIEF: Guide for migrating CI workflows to .github-private repository
-->

# CI Migration Guide: Moving to .github-private

## Overview

This guide documents the process for migrating GitHub Actions CI workflows from the public MokoStandards repository to a private `.github-private` repository. This approach allows for:

- **Security**: Keep sensitive workflow logic private
- **Centralization**: Single source of truth for organization workflows
- **Reusability**: Share workflows across multiple repositories
- **Control**: Manage workflow updates independently

## Current CI Workflows

### Workflows to Centralize to .github-private

| Workflow | Purpose | Migration Priority |
|----------|---------|-------------------|
| `php_quality.yml` | PHP code quality analysis (PHPCS, PHPStan, Psalm) | **High** |
| `release_pipeline.yml` | Automated release with marketplace publishing | **High** |
| `deploy_staging.yml` | Staging environment deployment | **High** |
| `joomla_testing.yml` | Comprehensive Joomla testing matrix | **High** |

### Workflows to Keep Local

| Workflow | Purpose | Rationale |
|----------|---------|-----------|
| `ci.yml` | Continuous integration validation | Repository-specific validation |
| `repo_health.yml` | Repository health and governance checks | Repo-specific governance rules |
| `version_branch.yml` | Version branch management | Repository-specific branching |
| `codeql-analysis.yml` | Security code scanning | Security best practice (public) |

### Shared Resources

| Resource | Purpose | Location |
|----------|---------|----------|
| `extension_utils.py` | Joomla extension operations | `.github-private/scripts/` |
| `common.py` | Common utility functions | `.github-private/scripts/` |
| Organization secrets | All credentials | Organization level with `secrets: inherit` |

## Migration Strategy

### Phase 1: Preparation (Current)

1. **Document existing workflows** - Catalog all workflows, their triggers, and dependencies
2. **Identify sensitive workflows** - Mark workflows containing proprietary logic
3. **Create migration checklist** - Define steps for each workflow type
4. **Setup `.github-private` repository** - Create and configure the private repo

### Phase 2: Migration

1. **Move reusable workflows** to `.github-private`
2. **Update workflow calls** in public repositories
3. **Test migrated workflows** in development branches
4. **Document new workflow structure**

### Phase 3: Cleanup

1. **Archive old workflows** in public repository
2. **Update documentation** to reference new locations
3. **Verify all repositories** are using migrated workflows

## .github-private Repository Structure

```
.github-private/
├── .github/workflows/
│   ├── reusable/
│   │   ├── php-quality.yml          (from php_quality.yml)
│   │   ├── release-pipeline.yml     (from release_pipeline.yml)
│   │   ├── deploy-staging.yml       (from deploy_staging.yml)
│   │   └── joomla-testing.yml       (from joomla_testing.yml)
│   └── templates/
│       ├── php-quality-template.yml
│       ├── release-template.yml
│       ├── deploy-template.yml
│       └── testing-template.yml
├── scripts/
│   ├── extension_utils.py           (shared Joomla utilities)
│   ├── common.py                    (shared common functions)
│   └── README.md                    (script API documentation)
├── docs/
│   ├── README.md
│   ├── workflow-usage.md
│   └── script-api.md
└── README.md
```

## Reusable Workflow Pattern

### In .github-private Repository

Create reusable workflows with clear inputs:

```yaml
# .github-private/.github/workflows/reusable/ci-validation.yml
name: Reusable CI Validation

on:
  workflow_call:
    inputs:
      profile:
        description: 'Validation profile (basic, full, strict)'
        required: false
        type: string
        default: 'basic'
      node-version:
        description: 'Node.js version'
        required: false
        type: string
        default: '20.x'
    secrets:
      CUSTOM_TOKEN:
        required: false

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run validation
        run: |
          echo "Running ${{ inputs.profile }} validation"
          # Validation logic here
```

### In Public Repository

Call the reusable workflow:

```yaml
# MokoStandards/.github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main, dev/**]

jobs:
  ci:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/ci-validation.yml@main
    with:
      profile: full
      node-version: '20.x'
    secrets: inherit
```

## Workflow Migration Checklist

### For Each Workflow:

- [ ] **Analyze workflow** - Understand triggers, inputs, secrets, and dependencies
- [ ] **Identify sensitive data** - Mark any proprietary logic or credentials
- [ ] **Create reusable version** - Convert to reusable workflow in `.github-private`
- [ ] **Add input parameters** - Define all necessary inputs and secrets
- [ ] **Test in isolation** - Verify workflow works independently
- [ ] **Update caller workflows** - Modify public repos to call reusable workflow
- [ ] **Test integration** - Run end-to-end tests
- [ ] **Document changes** - Update workflow documentation
- [ ] **Archive old workflow** - Move to `archived/` directory with deprecation notice

## Specific Workflow Migrations

### 1. PHP Quality (php_quality.yml) → .github-private

**Current Location:** `.github/workflows/php_quality.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/php-quality.yml`

**Migration Steps:**
1. Extract PHP quality checks into reusable workflow
2. Add parameters for PHP version matrix and tools selection
3. Integrate `extension_utils.py` from shared scripts
4. Configure organization-level secrets for private packages

**Caller Example:**
```yaml
jobs:
  quality:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main
    with:
      php-versions: '["7.4", "8.0", "8.1", "8.2"]'
      tools: '["phpcs", "phpstan", "psalm"]'
    secrets: inherit
```

**Shared Scripts Used:** `extension_utils.py`, `common.py`

---

### 2. Release Pipeline (release_pipeline.yml) → .github-private

**Current Location:** `.github/workflows/release_pipeline.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/release-pipeline.yml`

**Migration Steps:**
1. Consolidate build, package, and publish steps
2. Add support for multiple marketplaces (JED, Dolibarr)
3. Integrate `extension_utils.py` for package creation
4. Configure marketplace API tokens at org level

**Caller Example:**
```yaml
jobs:
  release:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/release-pipeline.yml@main
    with:
      version: '1.2.3'
      publish-to-marketplace: true
      platform: 'joomla'
    secrets: inherit
```

**Shared Scripts Used:** `extension_utils.py`, `common.py`

---

### 3. Deploy Staging (deploy_staging.yml) → .github-private

**Current Location:** `.github/workflows/deploy_staging.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/deploy-staging.yml`

**Migration Steps:**
1. Extract deployment logic with rollback capabilities
2. Add environment-specific configuration
3. Integrate `common.py` for deployment utilities
4. Use org-level secrets for staging credentials

**Caller Example:**
```yaml
jobs:
  deploy:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/deploy-staging.yml@main
    with:
      environment: staging
      health-check-url: 'https://staging.example.com/health'
    secrets: inherit
```

**Shared Scripts Used:** `common.py`

---

### 4. Joomla Testing (joomla_testing.yml) → .github-private

**Current Location:** `.github/workflows/joomla_testing.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/joomla-testing.yml`

**Migration Steps:**
1. Create matrix testing for PHP and Joomla versions
2. Setup Joomla test instances with MySQL
3. Integrate `extension_utils.py` for installation tests
4. Configure code coverage tokens at org level

**Caller Example:**
```yaml
jobs:
  test:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/joomla-testing.yml@main
    with:
      php-versions: '["7.4", "8.0", "8.1", "8.2"]'
      joomla-versions: '["4.4", "5.0", "5.1"]'
      coverage: true
    secrets: inherit
```

**Shared Scripts Used:** `extension_utils.py`, `common.py`

---

### Workflows Kept Local

### 5. CI Validation (ci.yml) - KEEP LOCAL

**Decision:** Keep in local repository

**Rationale:**
- Repository-specific validation rules
- No sensitive logic
- Fast iteration without cross-repo dependencies

---

### 6. Repository Health (repo_health.yml) - KEEP LOCAL

**Decision:** Keep in local repository

**Rationale:**
- Proprietary governance but repo-specific
- Complex repo-specific rules
- Frequent customization needed

---

### 7. Version Branch (version_branch.yml) - KEEP LOCAL

**Decision:** Keep in local repository

**Rationale:**
- Repository-specific branching strategies
- No sensitive credentials
- Different per repository

## Security Considerations

### Access Control

1. **Repository Permissions:**
   - `.github-private` must be accessible to organization members
   - Configure repository visibility as Internal or Private
   - Set up branch protection rules

2. **Workflow Permissions:**
   - Use `secrets: inherit` carefully
   - Explicitly define required secrets
   - Limit token permissions with `permissions:` key

3. **Secret Management:**
   - Store sensitive values in organization secrets
   - Use environment-specific secrets when needed
   - Rotate secrets regularly

### Code Review

1. **All workflow changes** in `.github-private` require review
2. **Breaking changes** must be communicated to all teams
3. **Version tagging** for stable workflow releases
4. **Changelog** maintained for workflow updates

## Testing Strategy

### Unit Testing

1. Test individual workflow steps locally where possible
2. Use `act` tool for local GitHub Actions testing
3. Validate input parameter handling

### Integration Testing

1. Create test repositories to validate workflows
2. Run workflows against development branches
3. Verify cross-repository workflow calls

### Regression Testing

1. Maintain test suite for workflow changes
2. Run tests before merging workflow updates
3. Monitor workflow failures across repositories

## Rollback Plan

### If Migration Issues Occur:

1. **Immediate:** Revert public repository to use local workflows
2. **Short-term:** Fix issues in `.github-private`
3. **Communication:** Notify affected teams
4. **Long-term:** Update migration guide with lessons learned

### Rollback Steps:

```bash
# In public repository
git revert <migration-commit>
git push origin main

# Or restore from backup
cp .github/workflows/archived/workflow.yml .github/workflows/
git commit -m "Rollback: Restore local workflow"
git push
```

## Migration Timeline

### Week 1: Preparation
- ✅ Document existing workflows
- ✅ Create migration guide
- ✅ Identify workflows to centralize vs keep local
- ⬜ Setup `.github-private` repository
- ⬜ Configure access permissions
- ⬜ Setup organization-level secrets

### Week 2: Shared Scripts
- ⬜ Create `scripts/` directory in `.github-private`
- ⬜ Move `extension_utils.py` to shared location
- ⬜ Move `common.py` to shared location
- ⬜ Document script APIs
- ⬜ Test script access from workflows

### Week 3: Workflow Migration
- ⬜ Migrate **php_quality.yml** to reusable workflow
- ⬜ Migrate **release_pipeline.yml** to reusable workflow
- ⬜ Migrate **deploy_staging.yml** to reusable workflow
- ⬜ Migrate **joomla_testing.yml** to reusable workflow
- ⬜ Update caller workflows in repositories

### Week 4: Testing & Documentation
- ⬜ Test all migrated workflows end-to-end
- ⬜ Verify secret inheritance works correctly
- ⬜ Verify shared script access works
- ⬜ Document usage patterns
- ⬜ Train team on new workflow structure
- ⬜ Archive migration guide as reference

## Post-Migration Maintenance

### Ongoing Tasks:

1. **Monitor workflow runs** across all repositories
2. **Update workflows** as needs evolve
3. **Version control** workflow releases
4. **Document changes** in changelog
5. **Communicate updates** to development teams

### Quarterly Reviews:

1. Review workflow usage and performance
2. Identify optimization opportunities
3. Update documentation
4. Solicit feedback from teams

## Resources

### Internal Documentation
- [GitHub Actions Best Practices](../docs/standards/github-actions.md)
- [Workflow Templates](../../templates/workflows/)
- [Project Standards](../../templates/projects/)

### External Resources
- [GitHub: Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub: Sharing Workflows](https://docs.github.com/en/actions/using-workflows/sharing-workflows-secrets-and-runners-with-your-organization)
- [GitHub: Internal Repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories#about-internal-repositories)

## Support

For questions or issues with CI migration:
- **Email:** devops@mokoconsulting.tech
- **Slack:** #devops-support
- **GitHub Issues:** Open issue in `.github-private` repository

## Metadata

| Field | Value |
|-------|-------|
| Document | CI Migration Guide |
| Path | /.github/CI_MIGRATION_GUIDE.md |
| Status | Active |
| Version | 01.00.00 |
| Date | 2026-01-04 |
| Author | Moko Consulting DevOps Team |

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-04 | Initial migration guide created | DevOps Team |
