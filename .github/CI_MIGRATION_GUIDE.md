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

This guide documents the process for migrating GitHub Actions CI workflows from the public MokoStandards repository to a private `.github-private` repository.

### Repository Architecture

Moko Consulting uses a dual-repository strategy for centralized standards and workflows:

- **`MokoStandards`** (Public Central Repository)
  - Public standards, templates, and documentation
  - Workflow templates for community use
  - Project configuration templates
  - Public best practices and guides
  - Product documentation (MokoCRM, MokoWaaS)
  
- **`.github-private`** (Private and Secure Centralization)
  - Proprietary workflow implementations
  - Sensitive automation logic
  - Organization-specific CI/CD pipelines
  - Internal deployment scripts
  - Confidential configurations

### Migration Benefits

This dual-repository approach provides:

- **Security**: Keep sensitive workflow logic and proprietary automation private
- **Centralization**: Single source of truth for organization workflows across all repositories
- **Reusability**: Share private workflows across multiple internal repositories
- **Control**: Manage workflow updates independently from public standards
- **Transparency**: Public templates remain accessible while protecting proprietary implementations

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

### Phase 1: Preparation (Weeks 1-2)

#### Week 1: Infrastructure Setup

**Day 1-2: Repository Setup**
1. **Create `.github-private` repository**
   ```bash
   # Via GitHub CLI
   gh repo create mokoconsulting-tech/.github-private --private --add-readme
   cd .github-private
   git checkout -b main
   ```

2. **Configure repository settings**
   - Visibility: Private (or Internal if available)
   - Branch protection: Required reviews for main branch
   - Access: Organization members with read access
   - Settings: Disable Issues, enable Actions

3. **Setup directory structure**
   ```bash
   mkdir -p .github/workflows/reusable
   mkdir -p .github/workflows/templates
   mkdir -p scripts
   mkdir -p docs
   ```

**Day 3-4: Access Control**
1. **Configure repository permissions**
   - Teams: Engineering (Write), DevOps (Admin)
   - Branch protection: Require 1 approval, require status checks
   - Actions: Allow organization actions only

2. **Setup GitHub Apps/Tokens**
   - Create organization-level GitHub App for workflow access
   - Configure app permissions: Contents (read/write), Actions (read/write)
   - Install app on `.github-private` repository

**Day 5: Organization Secrets**
1. **Configure organization-level secrets**
   ```
   Organization Secrets:
   ├── GH_PAT (GitHub Personal Access Token with full scope)
   ├── STAGING_SSH_KEY (SSH private key for staging servers)
   ├── STAGING_HOST (Staging server hostname)
   ├── STAGING_USER (Staging server username)
   ├── PRODUCTION_SSH_KEY (Production SSH key - for future)
   ├── PRODUCTION_HOST (Production hostname - for future)
   ├── MARKETPLACE_TOKEN (JED/Dolibarr marketplace API token)
   ├── JED_API_KEY (Joomla Extensions Directory API)
   ├── DOLISTORE_API_KEY (Dolibarr store API)
   ├── CODECOV_TOKEN (Code coverage service)
   ├── SONAR_TOKEN (SonarQube/SonarCloud token)
   ├── TEST_DB_PASSWORD (Test database password)
   ├── SLACK_WEBHOOK (Notifications)
   └── RELEASE_SIGNING_KEY (Package signing key)
   ```

2. **Configure secret access**
   - All organization secrets: Available to selected repositories
   - Initially: Enable for `.github-private` repository only
   - As workflows migrate: Enable for calling repositories

#### Week 2: Shared Scripts Migration

**Day 1-2: Script Preparation**
1. **Audit existing scripts**
   - `extension_utils.py`: Review all functions, document parameters
   - `common.py`: Identify dependencies, document API

2. **Create script documentation**
   ```bash
   # In .github-private/scripts/README.md
   ```

3. **Add version metadata**
   - Add `__version__` variable to each script
   - Add function docstrings
   - Add type hints for Python 3.7+

**Day 3-4: Script Migration**
1. **Copy scripts to `.github-private`**
   ```bash
   cd .github-private
   cp /path/to/extension_utils.py scripts/
   cp /path/to/common.py scripts/
   ```

2. **Add unit tests**
   ```bash
   mkdir -p scripts/tests
   # Create test files
   touch scripts/tests/test_extension_utils.py
   touch scripts/tests/test_common.py
   ```

3. **Setup testing workflow**
   - Create `.github/workflows/test-scripts.yml`
   - Run tests on script changes
   - Report coverage

**Day 5: Script Integration Testing**
1. **Test script checkout in workflows**
   ```yaml
   - name: Checkout shared scripts
     uses: actions/checkout@v4
     with:
       repository: mokoconsulting-tech/.github-private
       path: .github-private
       token: ${{ secrets.GH_PAT }}
   
   - name: Test script import
     run: |
       python -c "import sys; sys.path.append('.github-private/scripts'); import extension_utils; print(extension_utils.__version__)"
   ```

2. **Document import patterns**
3. **Create example workflows**

### Phase 2: Workflow Migration (Weeks 3-4)

#### Week 3: High-Priority Workflows

**Day 1-2: php_quality.yml Migration**

1. **Create reusable workflow**
   ```bash
   # In .github-private/.github/workflows/reusable/php-quality.yml
   ```

2. **Design workflow interface**
   ```yaml
   on:
     workflow_call:
       inputs:
         php-versions:
           description: 'JSON array of PHP versions'
           required: false
           type: string
           default: '["7.4", "8.0", "8.1", "8.2"]'
         tools:
           description: 'Quality tools to run'
           required: false
           type: string
           default: '["phpcs", "phpstan", "psalm"]'
         working-directory:
           description: 'Working directory'
           required: false
           type: string
           default: '.'
       outputs:
         quality-score:
           description: 'Overall quality score'
           value: ${{ jobs.quality.outputs.score }}
   ```

3. **Implement workflow**
   - Setup PHP matrix
   - Install quality tools
   - Run checks
   - Report results

4. **Test in isolation**
   ```bash
   # Create test repository
   gh repo create mokoconsulting-tech/test-php-quality --private
   ```

5. **Update caller workflow**
   ```yaml
   # In MokoStandards/.github/workflows/php_quality.yml
   jobs:
     quality:
       uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main
       with:
         php-versions: '["7.4", "8.0", "8.1", "8.2"]'
         tools: '["phpcs", "phpstan", "psalm"]'
       secrets: inherit
   ```

6. **Test end-to-end**
7. **Monitor first 10 runs**
8. **Document in migration log**

**Day 3-4: release_pipeline.yml Migration**

1. **Create reusable workflow with complex interface**
   ```yaml
   on:
     workflow_call:
       inputs:
         version:
           description: 'Release version (semver)'
           required: true
           type: string
         platform:
           description: 'Target platform (joomla, dolibarr, generic)'
           required: true
           type: string
         publish-to-marketplace:
           description: 'Publish to marketplace'
           required: false
           type: boolean
           default: false
         create-github-release:
           description: 'Create GitHub release'
           required: false
           type: boolean
           default: true
         pre-release:
           description: 'Mark as pre-release'
           required: false
           type: boolean
           default: false
   ```

2. **Implement release stages**
   - Validation: Verify version format, check for existing release
   - Build: Create ZIP/TAR packages with `extension_utils.py`
   - Checksums: Generate SHA256 checksums
   - GitHub Release: Create release with assets
   - Marketplace: Publish to JED or Dolistore
   - Notifications: Send success/failure notifications

3. **Add rollback capability**
   ```yaml
   - name: Rollback on failure
     if: failure()
     run: |
       gh release delete ${{ inputs.version }} --yes || true
       git push --delete origin ${{ inputs.version }} || true
   ```

4. **Test with dry-run mode**
5. **Migrate and monitor**

**Day 5: deploy_staging.yml Migration**

1. **Create secure deployment workflow**
2. **Implement health checks and rollback**
3. **Add deployment notifications**
4. **Test in sandbox environment**
5. **Migrate production deployments**

#### Week 4: Testing & Finalization

**Day 1-2: joomla_testing.yml Migration**

1. **Create comprehensive testing workflow**
2. **Setup test matrix (PHP × Joomla versions)**
3. **Integrate code coverage**
4. **Test with multiple repositories**
5. **Fine-tune performance**

**Day 3: Integration Testing**

1. **Test all workflows together**
   - Create test PR in repository
   - Trigger all workflows
   - Verify results
   - Check logs for errors

2. **Load testing**
   - Trigger multiple concurrent runs
   - Monitor GitHub Actions quota
   - Check for race conditions

3. **Security audit**
   - Review secret access
   - Check for leaked credentials
   - Verify access controls

**Day 4: Documentation**

1. **Complete workflow documentation**
   - Usage examples for each workflow
   - Troubleshooting guides
   - API reference for inputs/outputs

2. **Update team documentation**
   - Migration checklist completed
   - New workflow patterns documented
   - Runbook for common issues

3. **Create training materials**
   - Video tutorials
   - Quick reference guides
   - FAQ document

**Day 5: Team Training & Handoff**

1. **Conduct training session**
   - Demo new workflows
   - Show troubleshooting process
   - Q&A session

2. **Gradual rollout**
   - Enable for pilot repositories
   - Monitor for 1 week
   - Gather feedback
   - Adjust based on feedback

3. **Full deployment**
   - Enable for all repositories
   - Announce to team
   - Monitor closely for 2 weeks

### Phase 3: Cleanup & Optimization (Week 5+)

#### Week 5: Cleanup

**Day 1-2: Archive Old Workflows**

1. **Create archived/ directory**
   ```bash
   mkdir -p .github/workflows/archived
   ```

2. **Move old workflows with deprecation notice**
   ```yaml
   # .github/workflows/archived/php_quality.yml
   name: PHP Quality (DEPRECATED)
   
   on:
     push:
       branches-ignore:
         - '**'  # Never run
   
   jobs:
     deprecated:
       runs-on: ubuntu-latest
       steps:
         - name: Deprecation Notice
           run: |
             echo "⚠️ This workflow has been deprecated"
             echo "Use the reusable workflow instead:"
             echo "uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main"
             exit 1
   ```

3. **Update workflow references**
   - Find all references in documentation
   - Update links to new workflows
   - Add migration notes

**Day 3-4: Documentation Updates**

1. **Update README files**
2. **Update workflow templates**
3. **Update onboarding docs**
4. **Create migration changelog**

**Day 5: Verification**

1. **Audit all repositories**
   ```bash
   # Script to check all repos for old workflow calls
   ```

2. **Verify secret access**
3. **Check workflow run history**
4. **Confirm no broken integrations**

#### Ongoing: Optimization

**Performance Monitoring**

1. **Track workflow metrics**
   - Average execution time
   - Success rate
   - Queue time
   - Resource usage

2. **Optimize slow workflows**
   - Cache dependencies
   - Parallelize jobs
   - Reduce checkout depth

3. **Cost management**
   - Monitor GitHub Actions minutes
   - Optimize matrix size
   - Use self-hosted runners if needed

**Continuous Improvement**

1. **Monthly reviews**
   - Workflow performance
   - User feedback
   - New requirements

2. **Quarterly updates**
   - Update dependencies
   - Security patches
   - Feature additions

3. **Annual audit**
   - Full security review
   - Architecture assessment
   - Roadmap planning

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
   
   **Recommended Settings:**
   ```
   Repository: .github-private
   ├── Visibility: Private (or Internal if available on GitHub Enterprise)
   ├── Teams Access:
   │   ├── DevOps: Admin (can manage workflows and secrets)
   │   ├── Engineering: Write (can update workflows)
   │   └── QA: Read (can view but not modify)
   ├── Branch Protection (main):
   │   ├── Require pull request: Yes
   │   ├── Required approvals: 2 (for critical workflows)
   │   ├── Dismiss stale reviews: Yes
   │   ├── Require status checks: Yes
   │   ├── Require linear history: Yes
   │   └── Include administrators: Yes
   └── Actions:
       ├── Allow: Organization actions only
       ├── Runner group: Default
       └── Workflow permissions: Read repository contents
   ```

2. **Workflow Permissions:**
   - Use `secrets: inherit` carefully - only when all org secrets are safe to expose
   - Explicitly define required secrets for sensitive workflows
   - Limit token permissions with `permissions:` key
   
   **Example: Restricted Permissions**
   ```yaml
   jobs:
     quality:
       uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main
       with:
         php-versions: '["8.0", "8.1"]'
       secrets:
         # Explicitly pass only needed secrets instead of inherit
         CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
         SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
       permissions:
         contents: read
         pull-requests: write  # For PR comments
         checks: write  # For check runs
   ```
   
   **Example: Token Scoping**
   ```yaml
   jobs:
     deploy:
       runs-on: ubuntu-latest
       permissions:
         contents: write  # For creating releases
         packages: write  # For publishing packages
         # Minimal permissions - no id-token, no actions, etc.
       steps:
         - uses: actions/checkout@v4
         - name: Deploy
           run: ./deploy.sh
   ```

3. **Secret Management:**
   - Store sensitive values in organization secrets
   - Use environment-specific secrets when needed
   - Rotate secrets regularly (quarterly minimum)
   - Audit secret usage monthly
   
   **Secret Rotation Schedule:**
   ```
   Monthly:
   └── Review secret access logs
   
   Quarterly:
   ├── Rotate API tokens (MARKETPLACE_TOKEN, CODECOV_TOKEN, etc.)
   ├── Rotate service account passwords
   └── Audit organization secret usage
   
   Annually:
   ├── Rotate SSH keys (STAGING_SSH_KEY, PRODUCTION_SSH_KEY)
   ├── Rotate signing keys (RELEASE_SIGNING_KEY)
   ├── Review and revoke unused GitHub Apps/PATs
   └── Comprehensive security audit
   ```
   
   **Secret Naming Convention:**
   ```
   Pattern: {ENVIRONMENT}_{SERVICE}_{TYPE}
   
   Examples:
   - STAGING_DATABASE_PASSWORD
   - PRODUCTION_API_TOKEN
   - DEV_SLACK_WEBHOOK
   - GLOBAL_GH_PAT (cross-environment)
   ```

4. **Audit Logging:**
   - Enable audit log streaming (GitHub Enterprise)
   - Monitor workflow runs for unusual patterns
   - Set up alerts for failed authentication
   
   **Monitoring Checklist:**
   - [ ] Failed workflow runs with authentication errors
   - [ ] Unexpected secret access patterns
   - [ ] Workflows running at unusual times
   - [ ] High resource usage (potential crypto mining)
   - [ ] New repositories calling workflows
   - [ ] Changes to reusable workflows without review

### Code Review

1. **All workflow changes** in `.github-private` require review
   - Minimum 2 approvals for production workflows
   - DevOps team member must approve infrastructure changes
   - Security team review for new secret usage
   
2. **Breaking changes** must be communicated to all teams
   - Announce in #devops Slack channel 1 week before
   - Update documentation with migration guides
   - Provide deprecation timeline (minimum 2 sprints)
   - Create compatibility layer when possible
   
3. **Version tagging** for stable workflow releases
   ```bash
   # Tag workflow releases for stability
   git tag -a php-quality-v1.0.0 -m "PHP Quality Workflow v1.0.0"
   git push origin php-quality-v1.0.0
   
   # Caller can pin to specific version
   uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@php-quality-v1.0.0
   ```
   
   **Versioning Strategy:**
   - `@main` - Latest stable (recommended for most use cases)
   - `@v1` - Major version branch (gets patches and minor updates)
   - `@v1.2` - Minor version branch (gets patches only)
   - `@v1.2.3` - Exact version tag (no automatic updates)
   - `@sha` - Commit SHA (maximum stability, no updates)
   
4. **Changelog** maintained for workflow updates
   ```markdown
   # CHANGELOG.md
   
   ## [1.2.0] - 2026-01-15
   ### Added
   - PHP 8.3 support in quality checks
   - New `strict-mode` input parameter
   
   ### Changed
   - Default PHPStan level from 5 to 6
   - Improved error reporting format
   
   ### Fixed
   - Race condition in parallel quality checks
   - Memory limit issues with large codebases
   
   ### Deprecated
   - `legacy-mode` parameter (will be removed in v2.0.0)
   
   ## [1.1.0] - 2026-01-01
   ...
   ```

### Security Best Practices

1. **Least Privilege Principle**
   - Grant minimum necessary permissions
   - Use fine-grained PATs instead of classic tokens
   - Scope tokens to specific repositories when possible
   
2. **Secrets Hygiene**
   - Never log secrets or echo them to console
   - Use secret masking: `echo "::add-mask::$SECRET"`
   - Validate secret format before use
   - Never store secrets in code or environment files
   
   **Example: Safe Secret Usage**
   ```yaml
   - name: Use secret safely
     env:
       API_TOKEN: ${{ secrets.API_TOKEN }}
     run: |
       # Mask secret in logs
       echo "::add-mask::$API_TOKEN"
       
       # Validate secret exists and has correct format
       if [ -z "$API_TOKEN" ] || [ ${#API_TOKEN} -lt 20 ]; then
         echo "Error: Invalid API_TOKEN"
         exit 1
       fi
       
       # Use secret (will be masked in logs)
       curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com
   ```

3. **Third-Party Actions**
   - Only use verified actions from GitHub Marketplace
   - Pin actions to specific commit SHA, not tags
   - Review action source code before use
   - Audit action permissions regularly
   
   **Example: Pinned Actions**
   ```yaml
   # ✅ GOOD: Pinned to commit SHA
   - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
   
   # ❌ BAD: Using mutable tag
   - uses: actions/checkout@v4
   
   # ⚠️ ACCEPTABLE: For first-party GitHub actions with @main
   - uses: actions/checkout@main
   ```

4. **Code Injection Prevention**
   - Never use untrusted input in `run:` directly
   - Use intermediate environment variables
   - Validate and sanitize all inputs
   
   **Example: Preventing Injection**
   ```yaml
   # ❌ VULNERABLE to code injection
   - name: Process PR title
     run: echo "PR title is: ${{ github.event.pull_request.title }}"
   
   # ✅ SAFE with environment variable
   - name: Process PR title
     env:
       PR_TITLE: ${{ github.event.pull_request.title }}
     run: echo "PR title is: $PR_TITLE"
   
   # ✅ EVEN SAFER with validation
   - name: Process PR title
     env:
       PR_TITLE: ${{ github.event.pull_request.title }}
     run: |
       # Validate title doesn't contain dangerous characters
       if echo "$PR_TITLE" | grep -qE '[;&|`$]'; then
         echo "Error: PR title contains invalid characters"
         exit 1
       fi
       echo "PR title is: $PR_TITLE"
   ```

5. **Workflow Triggers**
   - Avoid `pull_request_target` unless absolutely necessary
   - Use `pull_request` for untrusted PRs
   - Require approval for first-time contributors
   
   **Trigger Security Matrix:**
   ```
   pull_request: ✅ Safe for external PRs (uses PR branch)
   pull_request_target: ⚠️  Dangerous (uses base branch, has secrets access)
   workflow_dispatch: ✅ Safe (manual trigger, requires permissions)
   push: ✅ Safe (only trusted users can push)
   issue_comment: ⚠️  Moderate risk (validate comment author)
   ```

### Incident Response

**If Security Issue Detected:**

1. **Immediate Response (0-15 minutes)**
   - Disable affected workflow immediately
   - Revoke compromised secrets
   - Lock down `.github-private` repository
   - Notify security team

2. **Investigation (15-60 minutes)**
   - Review audit logs
   - Identify scope of compromise
   - Document timeline of events
   - Preserve evidence

3. **Remediation (1-4 hours)**
   - Rotate all potentially exposed secrets
   - Fix security vulnerability
   - Test fixes in sandbox
   - Re-enable workflows with monitoring

4. **Post-Incident (1-2 days)**
   - Conduct post-mortem
   - Update security documentation
   - Implement preventive controls
   - Train team on lessons learned

**Emergency Contacts:**
- Security Team Lead: security@mokoconsulting.tech
- On-Call DevOps: devops-oncall@mokoconsulting.tech
- Emergency Hotline: +1-XXX-XXX-XXXX

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

## Troubleshooting

### Common Issues and Solutions

#### 1. "Resource not accessible by integration" Error

**Symptom:**
```
Error: Resource not accessible by integration
```

**Causes:**
- Insufficient workflow permissions
- Missing organization secrets
- Repository not allowed to access `.github-private`

**Solutions:**

A. **Check workflow permissions:**
```yaml
permissions:
  contents: read
  pull-requests: write  # Add if workflow needs PR access
  checks: write  # Add if workflow creates check runs
```

B. **Verify organization secret access:**
- Go to Organization Settings → Secrets and variables → Actions
- Check that secrets are available to the calling repository
- Ensure "Selected repositories" includes your repo

C. **Verify repository access to `.github-private`:**
- `.github-private` repository settings → Actions → General
- Under "Access", ensure calling repository is allowed

#### 2. "Workflow file not found" Error

**Symptom:**
```
Error: Unable to resolve action `mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main`
```

**Causes:**
- Incorrect workflow path
- Missing GH_PAT or insufficient permissions
- Repository is private but no access granted

**Solutions:**

A. **Verify workflow path:**
```yaml
# ✅ CORRECT
uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main

# ❌ WRONG: Missing .github/workflows/
uses: mokoconsulting-tech/.github-private/reusable/php-quality.yml@main

# ❌ WRONG: Using .yml instead of path
uses: mokoconsulting-tech/.github-private@main
  with:
    workflow: php-quality.yml
```

B. **Check GH_PAT permissions:**
```bash
# Test PAT has access to .github-private
curl -H "Authorization: token $GH_PAT" \
  https://api.github.com/repos/mokoconsulting-tech/.github-private
```

C. **Ensure repository access:**
- User must have read access to `.github-private`
- For organization apps: Install app on `.github-private`

#### 3. Secrets Not Available in Reusable Workflow

**Symptom:**
```
Environment variable 'STAGING_SSH_KEY' is not set
```

**Causes:**
- Forgot `secrets: inherit`
- Secret not configured at organization level
- Secret name mismatch

**Solutions:**

A. **Add secrets inheritance:**
```yaml
jobs:
  deploy:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/deploy-staging.yml@main
    secrets: inherit  # ⬅️ Add this line
```

B. **Explicitly pass secrets:**
```yaml
jobs:
  deploy:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/deploy-staging.yml@main
    secrets:
      STAGING_SSH_KEY: ${{ secrets.STAGING_SSH_KEY }}
      STAGING_HOST: ${{ secrets.STAGING_HOST }}
```

C. **Verify secret exists:**
- Organization Settings → Secrets → Actions
- Check secret name matches exactly (case-sensitive)
- Verify secret is not empty

#### 4. Shared Scripts Import Fails

**Symptom:**
```python
ModuleNotFoundError: No module named 'extension_utils'
```

**Causes:**
- Scripts not checked out
- Incorrect Python path
- Missing GH_PAT for private repository

**Solutions:**

A. **Checkout shared scripts first:**
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
  
  - name: Checkout shared scripts
    uses: actions/checkout@v4
    with:
      repository: mokoconsulting-tech/.github-private
      path: .github-private
      token: ${{ secrets.GH_PAT }}
  
  - name: Use shared scripts
    run: |
      python -c "import sys; sys.path.append('.github-private/scripts'); import extension_utils"
```

B. **Add to PYTHONPATH:**
```yaml
- name: Setup Python path
  run: echo "PYTHONPATH=$PYTHONPATH:$GITHUB_WORKSPACE/.github-private/scripts" >> $GITHUB_ENV

- name: Use shared scripts
  run: python -c "import extension_utils; print(extension_utils.__version__)"
```

C. **Install as package:**
```yaml
- name: Install shared scripts as package
  run: |
    cd .github-private/scripts
    pip install -e .
```

#### 5. Workflow Runs on Wrong Branch

**Symptom:**
Workflow runs on pull request, but should only run on main

**Solution:**

```yaml
on:
  workflow_call:
    # Reusable workflow accepts all triggers from caller
    
# In caller workflow:
on:
  push:
    branches:
      - main  # Only trigger on main
  pull_request:
    branches:
      - main
```

#### 6. Matrix Jobs Fail Randomly

**Symptom:**
Some matrix jobs succeed, others fail with no clear pattern

**Causes:**
- Rate limiting
- Resource contention
- Flaky tests

**Solutions:**

A. **Add retries:**
```yaml
- name: Run tests with retry
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test
```

B. **Reduce concurrency:**
```yaml
strategy:
  matrix:
    php: ['7.4', '8.0', '8.1', '8.2']
  max-parallel: 2  # Limit concurrent jobs
```

C. **Add delays:**
```yaml
- name: Wait before starting (prevent rate limits)
  run: sleep $((RANDOM % 30))
```

#### 7. Workflow Timeout

**Symptom:**
```
The job running on runner GitHub Actions XXX has exceeded the maximum execution time of 360 minutes.
```

**Solutions:**

A. **Increase timeout (if justified):**
```yaml
jobs:
  long-running:
    timeout-minutes: 480  # 8 hours
```

B. **Optimize workflow:**
- Cache dependencies
- Parallelize independent steps
- Skip unnecessary steps

C. **Split into multiple workflows:**
```yaml
# Workflow 1: Fast checks
jobs:
  quick-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Lint
      - name: Unit tests

# Workflow 2: Slow checks (only if fast checks pass)
jobs:
  slow-checks:
    needs: quick-checks
    steps:
      - name: Integration tests
```

#### 8. Cache Not Restoring

**Symptom:**
Dependencies reinstalled every run, ignoring cache

**Solutions:**

A. **Check cache key:**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.composer/cache
    key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
    restore-keys: |
      ${{ runner.os }}-composer-
```

B. **Verify cache path exists:**
```yaml
- name: Debug cache
  run: |
    echo "Cache path: ~/.composer/cache"
    ls -la ~/.composer/cache || echo "Cache directory not found"
```

C. **Check GitHub cache limits:**
- Maximum cache size: 10 GB per repository
- Least recently used caches deleted first
- Cache expires after 7 days if not used

### Performance Optimization

#### Caching Strategies

**PHP Dependencies:**
```yaml
- name: Get Composer cache directory
  id: composer-cache
  run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

- name: Cache Composer dependencies
  uses: actions/cache@v3
  with:
    path: ${{ steps.composer-cache.outputs.dir }}
    key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
    restore-keys: ${{ runner.os }}-composer-
```

**Node.js Dependencies:**
```yaml
- name: Cache Node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-node-
```

**Docker Layers:**
```yaml
- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: ${{ runner.os }}-buildx-
```

#### Parallelization

**Parallel Jobs:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        php: ['7.4', '8.0', '8.1', '8.2']
        dependency: ['lowest', 'highest']
      fail-fast: false  # Continue even if one fails
    runs-on: ubuntu-latest
```

**Parallel Steps (with composite action):**
```yaml
- name: Run parallel checks
  run: |
    ./phpcs.sh &
    PID1=$!
    ./phpstan.sh &
    PID2=$!
    ./psalm.sh &
    PID3=$!
    
    wait $PID1 && wait $PID2 && wait $PID3
```

#### Resource Management

**Self-Hosted Runners for Heavy Workloads:**
```yaml
jobs:
  heavy-build:
    runs-on: [self-hosted, linux, x64, high-memory]
    steps:
      - name: Build large project
        run: ./build.sh
```

**Conditional Jobs to Save Resources:**
```yaml
jobs:
  check-changes:
    runs-on: ubuntu-latest
    outputs:
      should-test: ${{ steps.filter.outputs.src }}
    steps:
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            src:
              - 'src/**'
              - 'tests/**'
  
  test:
    needs: check-changes
    if: needs.check-changes.outputs.should-test == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
```

### Debugging Workflows

#### Enable Debug Logging

**For a single run:**
- Re-run workflow with "Enable debug logging" checkbox

**Permanently in workflow:**
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

#### SSH into Runner (for debugging)

```yaml
- name: Setup tmate session
  if: failure()  # Only on failure
  uses: mxschmitt/action-tmate@v3
  timeout-minutes: 30
```

#### Artifact Debugging

```yaml
- name: Upload logs on failure
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: debug-logs
    path: |
      ~/.composer/cache/
      vendor/
      *.log
```

### Migration-Specific Issues

#### Workflow Call Depth Limit

**Symptom:**
```
Error: Reusable workflow depth exceeds limit of 4
```

**Solution:**
Flatten workflow hierarchy - don't nest reusable workflows more than 3 levels deep

#### Changed Workflow Interface

**Symptom:**
Old callers break after reusable workflow input changes

**Solution:**

```yaml
# In reusable workflow: Support both old and new inputs
on:
  workflow_call:
    inputs:
      php-version:  # DEPRECATED
        required: false
        type: string
      php-versions:  # NEW
        required: false
        type: string
        default: '["8.0"]'

jobs:
  test:
    strategy:
      matrix:
        # Support both old and new
        php: ${{ fromJSON(inputs.php-versions || format('["{0}"]', inputs.php-version)) }}
```

#### Different Default Behavior

**Symptom:**
Migrated workflow behaves differently than local version

**Solution:**
Document all default values and breaking changes in CHANGELOG

```markdown
## Migration from Local Workflows

### Breaking Changes
- Default PHP version changed from 7.4 to 8.0
- PHPCS standard changed from PSR2 to PSR12
- Tests now run with strict mode by default

### Migration Guide
To maintain old behavior, explicitly set:
```yaml
with:
  php-versions: '["7.4"]'
  phpcs-standard: 'PSR2'
  strict-mode: false
```
```

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
