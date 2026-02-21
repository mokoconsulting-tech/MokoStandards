<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Workflows
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/workflows/workflow-inventory.md
VERSION: 04.00.03
BRIEF: Complete inventory of GitHub Actions workflows for migration planning
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# GitHub Actions Workflow Inventory

## Overview

This document provides a complete inventory of all GitHub Actions workflows in the MokoStandards repository, prepared for migration to `.github-private` repository.

### Repository Architecture

Moko Consulting maintains a dual-repository strategy:

- **`MokoStandards`** - **Public Central Repository**
  - Public standards, templates, and documentation
  - Community-accessible workflow templates
  - Open-source best practices

- **`.github-private`** - **Private and Secure Centralization**
  - Proprietary workflow implementations
  - Organization-specific CI/CD pipelines
  - Sensitive automation and deployment logic

This inventory identifies which workflows stay in the public `MokoStandards` repository and which migrate to the private `.github-private` repository for secure centralization.

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
| 13 | sync_docs_to_project.yml | 225 | High | GH_PAT | Evaluate |

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

**Purpose:** Automated PHP code quality checks including linting, static analysis, and coding standards validation

**Current Status:** To be migrated to `.github-private`

**Triggers:**
- `push` to main and development branches (`dev/**`, `rc/**`)
- `pull_request` to main branch
- `workflow_dispatch` for manual execution

**Jobs:**

1. **syntax-check**
   - Validates PHP syntax across all PHP files
   - Runs `php -l` (lint) on changed files
   - Fails fast if syntax errors found

2. **phpcs** (PHP_CodeSniffer)
   - Checks coding standards compliance
   - Standard: PSR-12 (configurable)
   - Reports: Summary with error count, detailed report artifact
   - Error threshold: 0 errors, 10 warnings maximum

3. **phpstan** (Static Analysis)
   - Type checking and bug detection
   - Level: 6 (out of 9)
   - Memory limit: 1GB
   - Cache enabled for faster subsequent runs

4. **psalm** (Static Analysis)
   - Additional type checking with different heuristics
   - Error level: 3
   - Shows info about inferred types
   - Integrates with PHPUnit for test assertions

5. **phpmd** (Mess Detector)
   - Code complexity and design analysis
   - Rules: codesize, controversial, design, naming, unusedcode
   - Cyclomatic complexity threshold: 10
   - NPath complexity threshold: 200

**Matrix Strategy:**
```yaml
strategy:
  matrix:
    php: ['7.4', '8.0', '8.1', '8.2']
    tools: ['phpcs', 'phpstan', 'psalm', 'phpmd']
  fail-fast: false
```

**Dependencies:**
- PHP 7.4-8.2 (multi-version testing)
- Composer for dependency management
- Quality tools installed via composer:
  - `squizlabs/php_codesniffer:^3.7`
  - `phpstan/phpstan:^1.10`
  - `vimeo/psalm:^5.0`
  - `phpmd/phpmd:^2.13`
- `extension_utils.py` for Joomla-specific validation
- `common.py` for reporting utilities

**Environment Variables:**
```yaml
env:
  COMPOSER_AUTH: ${{ secrets.COMPOSER_AUTH }}  # For private packages
  PHPSTAN_MEMORY_LIMIT: 1G
  PHPCS_COLORS: 1
```

**Outputs:**
- Quality scores (per tool, aggregated)
- Error/warning counts
- Detailed reports as artifacts
- PR comments with summary

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/php-quality.yml`

**Migration Complexity:** ⭐⭐⭐ Medium
- Requires PHP tool setup and configuration
- Matrix testing adds complexity
- Integration with `extension_utils.py` needs testing
- Multiple output formats to support

**Estimated LOC:** ~250 lines (including all jobs and steps)

**Secrets Required:**
```yaml
secrets:
  COMPOSER_AUTH:        # Organization-level, for private Packagist/Composer repos
  CODECOV_TOKEN:        # Organization-level, optional for coverage upload
  SONAR_TOKEN:          # Organization-level, optional for SonarQube integration
```

**Shared Scripts Used:**
- `extension_utils.py` - Joomla manifest validation, custom rule checks
- `common.py` - Report formatting, PR comment generation

**Reusable Workflow Interface:**
```yaml
on:
  workflow_call:
    inputs:
      php-versions:
        description: 'JSON array of PHP versions to test'
        required: false
        type: string
        default: '["7.4", "8.0", "8.1", "8.2"]'
      tools:
        description: 'Quality tools to run'
        required: false
        type: string
        default: '["phpcs", "phpstan", "psalm", "phpmd"]'
      phpcs-standard:
        description: 'PHP_CodeSniffer standard'
        required: false
        type: string
        default: 'PSR12'
      phpstan-level:
        description: 'PHPStan analysis level (0-9)'
        required: false
        type: string
        default: '6'
      working-directory:
        description: 'Working directory for checks'
        required: false
        type: string
        default: '.'
      fail-on-error:
        description: 'Fail workflow if errors found'
        required: false
        type: boolean
        default: true
      upload-artifacts:
        description: 'Upload detailed reports as artifacts'
        required: false
        type: boolean
        default: true
    outputs:
      quality-score:
        description: 'Overall quality score (0-100)'
        value: ${{ jobs.aggregate.outputs.score }}
      error-count:
        description: 'Total number of errors found'
        value: ${{ jobs.aggregate.outputs.errors }}
    secrets:
      COMPOSER_AUTH:
        required: false
      CODECOV_TOKEN:
        required: false
      SONAR_TOKEN:
        required: false
```

**Success Criteria:**
- All syntax checks pass
- PHPCS: 0 errors, ≤10 warnings
- PHPStan: Level 6 with 0 errors
- Psalm: Error level 3 with 0 errors
- PHPMD: No violations of critical rules

**Performance Optimizations:**
- Cache Composer dependencies (saves ~30 seconds)
- Cache PHPStan result cache (saves ~15 seconds)
- Parallel tool execution where possible
- Skip tools for unchanged file types

**Known Issues:**
- PHPStan can be memory-intensive on large codebases (1GB limit set)
- PHPCS can be slow on monorepos (use path filters)
- Psalm may have false positives with complex types (configure baseline)

**Example Usage After Migration:**
```yaml
name: PHP Quality

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

jobs:
  quality:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/php-quality.yml@main
    with:
      php-versions: '["7.4", "8.0", "8.1", "8.2"]'
      tools: '["phpcs", "phpstan", "psalm"]'
      phpcs-standard: 'PSR12'
      phpstan-level: '6'
    secrets: inherit
```

---

### 2. release_pipeline.yml - Automated Release Management

**Purpose:** Complete release automation including building, testing, packaging, and publishing to GitHub Releases and external marketplaces

**Current Status:** To be migrated to `.github-private`

**Triggers:**
- `workflow_dispatch` with manual inputs:
  - `version` (required): Semver version string (e.g., "1.2.3")
  - `platform` (required): Target platform (joomla, dolibarr, generic)
  - `publish-to-marketplace` (optional): Whether to publish to JED/Dolistore
  - `pre-release` (optional): Mark as pre-release
- `push` with tag matching pattern `v*.*.*`

**Jobs:**

1. **validate-version**
   - Validates semver format (X.Y.Z)
   - Checks version doesn't already exist
   - Verifies version is newer than latest release
   - Validates CHANGELOG.md has entry for version
   - Duration: ~30 seconds

2. **build-joomla** (conditional: platform == 'joomla')
   - Builds Joomla extension package
   - Steps:
     - Install PHP dependencies (Composer)
     - Install JS dependencies (npm/yarn)
     - Compile SCSS to CSS
     - Minify JavaScript
     - Run webpack/build scripts
     - Copy files to staging directory
     - Update manifest XML with version
     - Create ZIP package
   - Uses: `extension_utils.py` for manifest updates
   - Artifacts: `{extension-name}-{version}.zip`
   - Duration: ~2-3 minutes

3. **build-dolibarr** (conditional: platform == 'dolibarr')
   - Builds Dolibarr module package
   - Similar to Joomla but different structure
   - Updates module descriptor
   - Creates module archive
   - Duration: ~2 minutes

4. **build-generic** (conditional: platform == 'generic')
   - Generic build process
   - Configurable build command
   - Creates distributable artifacts
   - Duration: varies

5. **generate-checksums**
   - Generates SHA256 checksums for all artifacts
   - Creates CHECKSUMS.txt file
   - Signs checksums with GPG (optional)
   - Duration: ~10 seconds

6. **run-tests**
   - Runs test suite on built packages
   - Installs package in test environment
   - Runs smoke tests
   - Validates package integrity
   - Duration: ~5 minutes

7. **create-github-release**
   - Creates GitHub Release via API
   - Release notes from CHANGELOG.md
   - Uploads all artifacts
   - Tags commit with version
   - Duration: ~30 seconds

8. **publish-to-jed** (conditional: platform == 'joomla' && publish-to-marketplace)
   - Publishes to Joomla Extensions Directory
   - Uses JED API
   - Updates extension listing
   - Duration: ~1 minute

9. **publish-to-dolistore** (conditional: platform == 'dolibarr' && publish-to-marketplace)
   - Publishes to Dolibarr Store
   - Uses Dolistore API
   - Updates module listing
   - Duration: ~1 minute

10. **notify**
    - Sends notifications (Slack, email)
    - Updates project management tools
    - Triggers documentation rebuild
    - Duration: ~20 seconds

**Workflow Orchestration:**
```yaml
jobs:
  validate-version:
    runs-on: ubuntu-latest

  build:
    needs: validate-version
    strategy:
      matrix:
        include:
          - platform: joomla
            artifact: extension
          - platform: dolibarr
            artifact: module

  checksums:
    needs: build

  test:
    needs: checksums

  release:
    needs: test
    if: success()

  publish:
    needs: release
    if: inputs.publish-to-marketplace

  notify:
    needs: [release, publish]
    if: always()
```

**Dependencies:**
- PHP 7.4+ for Joomla/Dolibarr
- Node.js 18+ for frontend builds
- zip/tar utilities
- GitHub CLI (`gh`)
- `extension_utils.py` for package creation
- `common.py` for notification utilities

**Environment Variables:**
```yaml
env:
  VERSION: ${{ inputs.version }}
  PLATFORM: ${{ inputs.platform }}
  BUILD_DIR: build/
  DIST_DIR: dist/
```

**Secrets Required:**
```yaml
secrets:
  GH_PAT:                    # GitHub Personal Access Token for release creation
  MARKETPLACE_TOKEN:         # JED API token
  JED_API_KEY:              # Joomla Extensions Directory API key
  DOLISTORE_API_KEY:        # Dolibarr Store API key
  RELEASE_SIGNING_KEY:      # GPG key for signing (optional)
  SLACK_WEBHOOK:            # Notification webhook
  COMPOSER_AUTH:            # For private dependencies (optional)
```

**Outputs:**
```yaml
outputs:
  release-url:
    description: 'URL of created GitHub Release'
  artifact-urls:
    description: 'JSON array of artifact download URLs'
  marketplace-url:
    description: 'URL of marketplace listing'
```

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/release-pipeline.yml`

**Migration Complexity:** ⭐⭐⭐⭐⭐ Very High
- Complex multi-stage process
- Multiple platform support
- External API integrations
- Rollback complexity
- Error handling critical

**Estimated LOC:** ~450 lines (all jobs, error handling, rollback)

**Shared Scripts Used:**
- `extension_utils.py` - Package creation, manifest updates, ZIP generation
- `common.py` - API client utilities, notification sending, error handling

**Reusable Workflow Interface:**
```yaml
on:
  workflow_call:
    inputs:
      version:
        description: 'Release version (semver format)'
        required: true
        type: string
      platform:
        description: 'Target platform'
        required: true
        type: string  # enum: joomla, dolibarr, generic
      publish-to-marketplace:
        description: 'Publish to external marketplace'
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
      draft:
        description: 'Create as draft release'
        required: false
        type: boolean
        default: false
      run-tests:
        description: 'Run tests before release'
        required: false
        type: boolean
        default: true
    outputs:
      release-url:
        description: 'GitHub Release URL'
        value: ${{ jobs.release.outputs.url }}
      artifact-urls:
        description: 'Artifact download URLs (JSON array)'
        value: ${{ jobs.release.outputs.artifacts }}
```

**Rollback Strategy:**
```yaml
- name: Rollback on failure
  if: failure()
  run: |
    # Delete GitHub release if created
    gh release delete ${{ inputs.version }} --yes || true

    # Delete Git tag
    git push --delete origin v${{ inputs.version }} || true

    # Unpublish from marketplace (if published)
    if [ "${{ inputs.publish-to-marketplace }}" = "true" ]; then
      curl -X DELETE "$JED_API_URL/extensions/$EXTENSION_ID/versions/$VERSION" \
        -H "Authorization: Bearer ${{ secrets.JED_API_KEY }}"
    fi

    # Notify team of rollback
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"Release ${{ inputs.version }} rolled back due to failure"}'
```

**Success Criteria:**
- Version validation passes
- All builds succeed
- Tests pass on built artifacts
- GitHub Release created
- Marketplace publishing succeeds (if enabled)
- Notifications sent

**Performance Optimizations:**
- Cache build dependencies (Composer, npm)
- Parallel builds for multiple platforms
- Reuse test environments between runs

**Known Issues:**
- JED API can be rate-limited (implement retry with exponential backoff)
- Large extension ZIPs can timeout on upload (increase timeout to 30 min)
- Dolistore API occasionally returns 500 (implement retry logic)

**Example Usage After Migration:**
```yaml
name: Release

on:
  workflow_dispatch:
    inputs:
      version:
        required: true
      publish:
        type: boolean
        default: false

jobs:
  release:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/release-pipeline.yml@main
    with:
      version: ${{ inputs.version }}
      platform: 'joomla'
      publish-to-marketplace: ${{ inputs.publish }}
      pre-release: false
    secrets: inherit
```

**Additional Notes:**
- Integrates with version_release.yml for version bumping
- Can trigger deploy workflows after successful release
- Supports multi-package releases (component + modules + plugins)
- Maintains release history in RELEASES.md

---

### 3. deploy_staging.yml - Staging Environment Deployment

**Purpose:** Automated deployment to staging environments for testing before production release

**Current Status:** To be migrated to `.github-private`

**Triggers:**
- `push` to develop branch
- `workflow_dispatch` for manual deployment with inputs:
  - `environment` (default: 'staging'): Target environment
  - `version` (optional): Specific version to deploy
  - `skip-tests` (optional): Skip smoke tests
- Successful completion of `php_quality.yml` workflow

**Jobs:**

1. **pre-deploy-checks**
   - Validates deployment configuration
   - Checks target environment health
   - Verifies required secrets are available
   - Confirms no ongoing deployments
   - Duration: ~30 seconds

2. **build-deployment-package**
   - Creates deployment artifact
   - Includes only necessary files
   - Excludes development files (.git, tests, etc.)
   - Compresses package
   - Duration: ~1-2 minutes

3. **backup-current**
   - Creates backup of current staging environment
   - Backs up database
   - Backs up files
   - Stores backup with timestamp
   - Duration: ~2-3 minutes

4. **deploy-to-staging**
   - SSHs to staging server
   - Uploads deployment package
   - Extracts files to correct location
   - Sets proper permissions
   - Runs database migrations
   - Clears caches
   - Duration: ~3-5 minutes

5. **smoke-tests**
   - Waits for application to stabilize (30 seconds)
   - Runs HTTP health checks
   - Validates critical endpoints
   - Checks database connectivity
   - Verifies file permissions
   - Duration: ~2 minutes

6. **integration-tests** (optional)
   - Runs Selenium/Playwright tests
   - Tests critical user flows
   - Validates API endpoints
   - Duration: ~5-10 minutes

7. **notify-success**
   - Sends deployment success notification
   - Updates deployment tracking system
   - Posts to Slack/Teams
   - Duration: ~10 seconds

8. **rollback** (on failure)
   - Automatically triggered if any step fails
   - Restores from backup
   - Rolls back database
   - Restores files
   - Clears caches
   - Notifies team of rollback
   - Duration: ~3-5 minutes

**Workflow Orchestration:**
```yaml
jobs:
  pre-deploy-checks:
    runs-on: ubuntu-latest

  backup:
    needs: pre-deploy-checks
    runs-on: ubuntu-latest

  deploy:
    needs: backup
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

  smoke-tests:
    needs: deploy
    runs-on: ubuntu-latest

  integration-tests:
    needs: smoke-tests
    if: inputs.skip-tests == false
    runs-on: ubuntu-latest

  notify:
    needs: [deploy, smoke-tests, integration-tests]
    if: always()
    runs-on: ubuntu-latest
```

**Dependencies:**
- SSH client
- rsync for file transfer
- MySQL client for database operations
- curl for HTTP checks
- `common.py` for deployment utilities

**Environment Variables:**
```yaml
env:
  STAGING_HOST: ${{ secrets.STAGING_HOST }}
  STAGING_USER: ${{ secrets.STAGING_USER }}
  STAGING_PATH: /var/www/staging
  BACKUP_PATH: /var/backups/staging
  DATABASE_NAME: staging_db
```

**Secrets Required:**
```yaml
secrets:
  STAGING_SSH_KEY:           # SSH private key for staging server access
  STAGING_HOST:              # Staging server hostname/IP
  STAGING_USER:              # SSH username
  STAGING_DB_PASSWORD:       # Database password for migrations
  SLACK_WEBHOOK:             # Notification webhook
  HEALTH_CHECK_TOKEN:        # Token for health check endpoints (optional)
```

**Outputs:**
```yaml
outputs:
  deployment-url:
    description: 'URL of deployed application'
  deployment-time:
    description: 'Deployment timestamp'
  backup-id:
    description: 'Backup identifier for rollback'
```

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/deploy-staging.yml`

**Migration Complexity:** ⭐⭐⭐⭐ High
- Requires secure credential handling
- Complex deployment logic with rollback
- Environment-specific configurations
- Critical failure handling needed

**Estimated LOC:** ~350 lines (including rollback logic)

**Shared Scripts Used:**
- `common.py` - SSH utilities, health checks, notification sending

**Reusable Workflow Interface:**
```yaml
on:
  workflow_call:
    inputs:
      environment:
        description: 'Target environment (staging, qa, demo)'
        required: false
        type: string
        default: 'staging'
      version:
        description: 'Version to deploy (default: latest)'
        required: false
        type: string
      skip-tests:
        description: 'Skip smoke and integration tests'
        required: false
        type: boolean
        default: false
      health-check-url:
        description: 'URL for health check'
        required: true
        type: string
      rollback-on-failure:
        description: 'Automatically rollback on failure'
        required: false
        type: boolean
        default: true
    outputs:
      deployment-url:
        description: 'Deployed application URL'
        value: ${{ jobs.deploy.outputs.url }}
      backup-id:
        description: 'Backup ID (for manual rollback)'
        value: ${{ jobs.backup.outputs.backup-id }}
```

**Rollback Strategy:**
```yaml
- name: Automatic Rollback
  if: failure() && inputs.rollback-on-failure
  run: |
    echo "Deployment failed, rolling back to previous version..."

    # Restore files from backup
    ssh $STAGING_USER@$STAGING_HOST "cd $BACKUP_PATH && ./restore.sh $BACKUP_ID"

    # Restore database
    ssh $STAGING_USER@$STAGING_HOST "mysql -u$DB_USER -p$DB_PASS $DATABASE_NAME < $BACKUP_PATH/$BACKUP_ID/database.sql"

    # Clear caches
    ssh $STAGING_USER@$STAGING_HOST "cd $STAGING_PATH && php artisan cache:clear"

    # Verify rollback successful
    curl -f ${{ inputs.health-check-url }} || echo "⚠️ Health check failed after rollback"

    # Notify team
    curl -X POST $SLACK_WEBHOOK \
      -d '{"text":"🔴 Staging deployment failed and was rolled back. Backup ID: '"$BACKUP_ID"'"}'
```

**Health Check Implementation:**
```yaml
- name: Run Health Checks
  run: |
    MAX_RETRIES=10
    RETRY_DELAY=5

    for i in $(seq 1 $MAX_RETRIES); do
      echo "Health check attempt $i/$MAX_RETRIES..."

      # Check HTTP 200 response
      if curl -f -s -o /dev/null -w "%{http_code}" ${{ inputs.health-check-url }} | grep -q "200"; then
        echo "✅ Health check passed"
        exit 0
      fi

      echo "❌ Health check failed, retrying in ${RETRY_DELAY}s..."
      sleep $RETRY_DELAY
    done

    echo "❌ Health check failed after $MAX_RETRIES attempts"
    exit 1
```

**Success Criteria:**
- Pre-deploy checks pass
- Backup created successfully
- Files deployed without errors
- Database migrations succeed
- Health checks return 200 OK
- Smoke tests pass

**Performance Optimizations:**
- Use rsync with compression for faster file transfer
- Parallel backup of files and database
- Skip unchanged files during deployment
- Cache SSH connections

**Known Issues:**
- SSH connection can timeout on slow networks (increase timeout to 600s)
- Large database backups can be slow (implement incremental backups)
- Simultaneous deployments can cause conflicts (use deployment locks)

**Example Usage After Migration:**
```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/deploy-staging.yml@main
    with:
      environment: staging
      health-check-url: 'https://staging.example.com/health'
      skip-tests: false
    secrets: inherit
```

**Additional Notes:**
- Integrates with monitoring tools (Datadog, New Relic)
- Supports blue-green deployments (future enhancement)
- Can trigger load testing after deployment
- Maintains deployment history and audit logs

---

### 4. joomla_testing.yml - Joomla Extension Testing

**Purpose:** Comprehensive testing for Joomla extensions across multiple PHP and Joomla versions with integration tests

**Current Status:** To be migrated to `.github-private`

**Triggers:**
- `push` to main and development branches
- `pull_request` to main
- `schedule`: Nightly at 2:00 AM UTC
- `workflow_dispatch` with manual inputs:
  - `php-versions` (optional): PHP versions to test
  - `joomla-versions` (optional): Joomla versions to test
  - `coverage` (optional): Enable code coverage

**Jobs:**

1. **unit-tests**
   - Runs PHPUnit tests without Joomla
   - Fast feedback on core logic
   - No database required
   - Duration: ~1-2 minutes per PHP version

2. **integration-tests**
   - Sets up full Joomla installation
   - Installs extension
   - Runs integration tests
   - Tests database interactions
   - Duration: ~5-10 minutes per matrix combination

3. **code-coverage**
   - Collects coverage from all test runs
   - Generates HTML/XML reports
   - Uploads to Codecov/Coveralls
   - Enforces minimum coverage threshold (80%)
   - Duration: ~2 minutes

4. **compatibility-check**
   - Validates extension compatibility
   - Checks manifest requirements
   - Verifies update server
   - Tests installation/uninstallation
   - Duration: ~3 minutes

5. **browser-tests** (optional)
   - Selenium/Playwright E2E tests
   - Tests admin interface
   - Tests frontend functionality
   - Screenshots on failure
   - Duration: ~10-15 minutes

**Matrix Strategy:**
```yaml
strategy:
  matrix:
    php: ['7.4', '8.0', '8.1', '8.2']
    joomla: ['4.4', '5.0', '5.1']
    include:
      # Test PHP 8.3 with latest Joomla only
      - php: '8.3'
        joomla: '5.1'
    exclude:
      # Joomla 4.4 doesn't support PHP 8.2+
      - php: '8.2'
        joomla: '4.4'
      - php: '8.3'
        joomla: '4.4'
  fail-fast: false  # Continue testing other combinations
  max-parallel: 4   # Limit concurrent jobs
```

**Dependencies:**
- PHP 7.4-8.3 with extensions: `mysqli`, `gd`, `zip`, `xml`, `mbstring`
- MySQL/MariaDB 5.7+
- Joomla CMS 4.4-5.1
- PHPUnit 9.5+
- Composer
- Node.js (for frontend builds)
- `extension_utils.py` for installation testing

**Environment Variables:**
```yaml
env:
  JOOMLA_DB_HOST: 127.0.0.1
  JOOMLA_DB_USER: root
  JOOMLA_DB_PASS: root
  JOOMLA_DB_NAME: joomla_test
  JOOMLA_ADMIN_USER: admin
  JOOMLA_ADMIN_PASS: admin123!
  COVERAGE_THRESHOLD: 80
```

**Services:**
```yaml
services:
  mysql:
    image: mysql:8.0
    env:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: joomla_test
    ports:
      - 3306:3306
    options: >-
      --health-cmd="mysqladmin ping"
      --health-interval=10s
      --health-timeout=5s
      --health-retries=3
```

**Secrets Required:**
```yaml
secrets:
  CODECOV_TOKEN:             # Code coverage service token
  TEST_DB_PASSWORD:          # Test database password (if different from env)
  BROWSERSTACK_KEY:          # BrowserStack for cross-browser testing (optional)
```

**Outputs:**
```yaml
outputs:
  coverage-percentage:
    description: 'Code coverage percentage'
  test-results:
    description: 'Summary of test results (JSON)'
  compatibility-matrix:
    description: 'Compatibility matrix results (JSON)'
```

**Migration Type:** Convert to reusable workflow in `.github-private`

**Proposed Location:** `.github-private/.github/workflows/reusable/joomla-testing.yml`

**Migration Complexity:** ⭐⭐⭐⭐ High
- Complex test matrix (PHP × Joomla versions)
- Full Joomla setup required
- Database service coordination
- Coverage collection from multiple jobs

**Estimated LOC:** ~500 lines (including matrix, setup, all test types)

**Shared Scripts Used:**
- `extension_utils.py` - Extension installation, manifest validation, update server checks
- `common.py` - Test result aggregation, coverage reporting

**Reusable Workflow Interface:**
```yaml
on:
  workflow_call:
    inputs:
      php-versions:
        description: 'PHP versions to test (JSON array)'
        required: false
        type: string
        default: '["7.4", "8.0", "8.1", "8.2"]'
      joomla-versions:
        description: 'Joomla versions to test (JSON array)'
        required: false
        type: string
        default: '["4.4", "5.0", "5.1"]'
      coverage:
        description: 'Enable code coverage'
        required: false
        type: boolean
        default: true
      browser-tests:
        description: 'Run browser-based E2E tests'
        required: false
        type: boolean
        default: false
      coverage-threshold:
        description: 'Minimum coverage percentage required'
        required: false
        type: number
        default: 80
    outputs:
      coverage-percentage:
        description: 'Overall code coverage'
        value: ${{ jobs.coverage.outputs.percentage }}
      tests-passed:
        description: 'All tests passed (true/false)'
        value: ${{ jobs.aggregate.outputs.success }}
```

**Test Setup Steps:**
```yaml
- name: Setup Joomla
  run: |
    # Download Joomla
    wget https://downloads.joomla.org/cms/joomla${{ matrix.joomla }}/Joomla_${{ matrix.joomla }}.0-Stable-Full_Package.zip

    # Extract
    unzip -q Joomla_${{ matrix.joomla }}.0-Stable-Full_Package.zip -d /var/www/html

    # Install Joomla via CLI
    php /var/www/html/installation/joomla.php install \
      --site-name="Test Site" \
      --admin-user="$JOOMLA_ADMIN_USER" \
      --admin-password="$JOOMLA_ADMIN_PASS" \
      --admin-email="admin@example.com" \
      --db-type="mysqli" \
      --db-host="$JOOMLA_DB_HOST" \
      --db-user="$JOOMLA_DB_USER" \
      --db-pass="$JOOMLA_DB_PASS" \
      --db-name="$JOOMLA_DB_NAME" \
      --db-prefix="jos_"

    # Remove installation folder
    rm -rf /var/www/html/installation

- name: Install Extension
  run: |
    # Use extension_utils.py to install
    python .github-private/scripts/extension_utils.py install \
      --joomla-path /var/www/html \
      --package dist/*.zip
```

**Success Criteria:**
- All unit tests pass
- All integration tests pass across matrix
- Code coverage ≥ 80%
- Extension installs successfully
- No PHP errors/warnings in logs
- Browser tests pass (if enabled)

**Performance Optimizations:**
- Cache Joomla downloads (saves ~30 seconds)
- Cache Composer/npm dependencies
- Parallel test execution where possible
- Skip browser tests for draft PRs

**Known Issues:**
- Joomla 5.x requires PHP 8.0+ (matrix excludes invalid combinations)
- MySQL 8.0 authentication issues with PHP 7.4 (use legacy auth)
- Browser tests can be flaky (implement retry logic)
- Large test suites can timeout (split into multiple jobs)

**Example Usage After Migration:**
```yaml
name: Test Joomla Extension

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    uses: mokoconsulting-tech/.github-private/.github/workflows/reusable/joomla-testing.yml@main
    with:
      php-versions: '["7.4", "8.0", "8.1", "8.2"]'
      joomla-versions: '["4.4", "5.0", "5.1"]'
      coverage: true
      browser-tests: false
      coverage-threshold: 80
    secrets: inherit
```

**Additional Notes:**
- Supports multiple extension types (component, module, plugin, template)
- Can test against Joomla nightly builds
- Integrates with PHPUnit code coverage
- Generates compatibility badge for README
- Saves test artifacts (logs, screenshots) for debugging

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

### 13. sync_docs_to_project.yml - Documentation Project Sync

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
| `scripts/automation/sync_file_to_project.py` | sync_docs_to_project.yml | Keep in repository |

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
13. **sync_docs_to_project.yml** - Project sync

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
