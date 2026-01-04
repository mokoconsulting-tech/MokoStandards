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

The following workflows are currently in `.github/workflows/`:

| Workflow | Purpose | Sensitivity | Migration Priority |
|----------|---------|-------------|-------------------|
| `ci.yml` | Continuous integration validation | Low | Standard |
| `repo_health.yml` | Repository health and governance checks | Medium | High |
| `codeql-analysis.yml` | Security code scanning | Low | Standard |
| `changelog_update.yml` | Automated changelog management | Low | Standard |
| `version_release.yml` | Version bumping and releases | Medium | High |
| `rebuild_docs_indexes.yml` | Documentation index generation | Low | Standard |
| `setup_project_v2.yml` | GitHub Projects v2 setup automation | Medium | High |
| `setup_project_7.yml` | Project #7 specific setup | Medium | High |
| `sync_docs_to_project.yml` | Sync documentation to project board | Medium | High |

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
│   │   ├── ci-validation.yml
│   │   ├── repo-health-check.yml
│   │   ├── version-management.yml
│   │   ├── project-automation.yml
│   │   ├── docs-automation.yml
│   │   └── security-scanning.yml
│   └── templates/
│       ├── standard-ci.yml
│       ├── standard-release.yml
│       └── standard-health.yml
├── docs/
│   ├── README.md
│   ├── workflow-catalog.md
│   └── migration-guide.md
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

### 1. CI Validation (ci.yml)

**Current Location:** `.github/workflows/ci.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/ci-validation.yml`

**Migration Steps:**
1. Extract validation logic into reusable workflow
2. Add parameters for validation profiles
3. Maintain compatibility with existing scripts
4. Update public repo to call reusable workflow

**Caller Example:**
```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/ci-validation.yml@main
    with:
      profile: strict
```

### 2. Repository Health (repo_health.yml)

**Current Location:** `.github/workflows/repo_health.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/repo-health-check.yml`

**Migration Steps:**
1. Preserve all health check logic
2. Make profile selection configurable
3. Add repository-specific customization options
4. Maintain admin-only execution gate

**Caller Example:**
```yaml
jobs:
  health:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/repo-health-check.yml@main
    with:
      profile: all
      strict-mode: true
```

### 3. Version Release (version_release.yml)

**Current Location:** `.github/workflows/version_release.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/version-management.yml`

**Migration Steps:**
1. Extract version bumping logic
2. Support multiple version schemes
3. Add release note generation
4. Maintain changelog integration

**Caller Example:**
```yaml
jobs:
  release:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/version-management.yml@main
    with:
      new-version: '1.2.3'
      version-text: 'LTS'
    secrets: inherit
```

### 4. Project Automation (setup_project_*.yml)

**Current Location:** `.github/workflows/setup_project_v2.yml`, `setup_project_7.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/project-automation.yml`

**Migration Steps:**
1. Consolidate project setup workflows
2. Add template selection parameters
3. Support both org and repo projects
4. Maintain field configuration logic

**Caller Example:**
```yaml
jobs:
  setup:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/project-automation.yml@main
    with:
      project-type: joomla
      project-name: 'MyProject'
    secrets: inherit
```

### 5. Documentation Automation (rebuild_docs_indexes.yml, sync_docs_to_project.yml)

**Current Location:** `.github/workflows/rebuild_docs_indexes.yml`, `sync_docs_to_project.yml`  
**Target Location:** `.github-private/.github/workflows/reusable/docs-automation.yml`

**Migration Steps:**
1. Combine documentation workflows
2. Add selective update capabilities
3. Support multiple documentation formats
4. Maintain project sync logic

**Caller Example:**
```yaml
jobs:
  docs:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/docs-automation.yml@main
    with:
      rebuild-indexes: true
      sync-to-project: true
```

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
- ⬜ Setup `.github-private` repository
- ⬜ Configure access permissions

### Week 2: Initial Migration
- ⬜ Migrate non-sensitive workflows (CI, CodeQL)
- ⬜ Test migrated workflows
- ⬜ Update documentation

### Week 3: Sensitive Workflows
- ⬜ Migrate repository health workflow
- ⬜ Migrate version release workflow
- ⬜ Migrate project automation workflows

### Week 4: Final Migration
- ⬜ Migrate documentation workflows
- ⬜ Complete testing across all repositories
- ⬜ Archive old workflows
- ⬜ Final documentation updates

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
