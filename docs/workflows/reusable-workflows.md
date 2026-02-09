<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Documentation
 INGROUP: MokoStandards.Workflows
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 03.01.02
 PATH: /docs/workflows/reusable-workflows.md
 BRIEF: Documentation for reusable GitHub Actions workflows
 -->

# Reusable Workflows

MokoStandards provides seven reusable GitHub Actions workflows that enable consistent CI/CD across all organization repositories, with automatic project type detection for Joomla extensions, Dolibarr modules, and generic applications.

## Quick Start

```yaml
# Basic quality check
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main

# Type-aware build and release
  build:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main

  release:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-release.yml@main
    with:
      version: '1.0.0'
```

## Workflow Categories

### Quality & Testing Workflows
- **reusable-php-quality.yml** - PHP code quality analysis (PHPCS, PHPStan, Psalm)
- **reusable-joomla-testing.yml** - Joomla extension testing with matrix PHP/Joomla versions
- **reusable-ci-validation.yml** - Repository standards validation

### Repository Maintenance Workflows
- **reusable-branch-cleanup.yml** - Automated cleanup of stale and merged branches

### Type-Aware Orchestration Workflows
- **reusable-project-detector.yml** - Automatic project type detection
- **reusable-build.yml** - Universal build for all project types
- **reusable-release.yml** - Type-aware release creation and packaging
- **reusable-deploy.yml** - Multi-environment deployment

> **Type-Aware Workflows** automatically detect whether your project is a Joomla extension, Dolibarr module, or generic application, and apply appropriate build/release/deploy steps. This enables a single workflow definition to work across all repositories.

---

## Quality & Testing Workflows

### PHP Quality Analysis

Runs comprehensive PHP code quality checks using PHPCS, PHPStan, and Psalm with configurable standards and analysis levels.

**Usage:**
```yaml
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-versions: '["8.1", "8.2"]'
      tools: '["phpcs", "phpstan", "psalm"]'
      phpcs-standard: 'PSR12'
      phpstan-level: '6'
```

**Key Inputs:**
- `php-versions` (string) - JSON array of PHP versions, default: `["7.4", "8.0", "8.1", "8.2"]`
- `tools` (string) - JSON array of tools, default: `["phpcs", "phpstan", "psalm"]`
- `phpcs-standard` (string) - Coding standard, default: `PSR12`
- `phpstan-level` (string) - Analysis level 0-9, default: `5`
- `fail-on-error` (boolean) - Fail on errors, default: `true`

**Outputs:** `quality-score` - Overall quality score percentage (0-100)

### Joomla Testing

Matrix testing for Joomla extensions across PHP and Joomla versions with PHPUnit, MySQL, and code coverage support.

**Usage:**
```yaml
jobs:
  test:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      php-versions: '["8.1", "8.2"]'
      joomla-versions: '["4.4", "5.0", "5.1"]'
      coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

**Key Inputs:**
- `php-versions` (string) - JSON array, default: `["7.4", "8.0", "8.1", "8.2"]`
- `joomla-versions` (string) - JSON array, default: `["4.4", "5.0", "5.1"]`
- `coverage` (boolean) - Enable coverage, default: `false`
- `run-integration-tests` (boolean) - Run integration tests, default: `true`

> Automatically excludes incompatible combinations (e.g., PHP 7.4 + Joomla 5.x)

### CI Validation

Repository standards validation with configurable profiles (basic, full, strict).

**Usage:**
```yaml
jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'full'
      validate-security: true
```

**Validation Profiles:**
- **basic** - Manifest, XML, PHP syntax, security checks
- **full** - Basic + changelog, license headers, language structure, paths, whitespace
- **strict** - Full validation with fail-on-warnings enabled

**Key Inputs:**
- `profile` (string) - Validation profile, default: `basic`
- `validate-manifests` (boolean) - Validate XML manifests, default: `true`
- `validate-changelogs` (boolean) - Validate CHANGELOG.md, default: `true`
- `validate-licenses` (boolean) - Validate license headers, default: `true`
- `validate-security` (boolean) - Security checks, default: `true`
- `fail-on-warnings` (boolean) - Fail on warnings, default: `false`

---

## Repository Maintenance Workflows

### Branch Cleanup

Automatically cleans up stale and merged branches with configurable exclusion patterns and dry-run support.

**Usage:**
```yaml
jobs:
  cleanup:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-branch-cleanup.yml@main
    with:
      stale-days: 90
      delete-merged: true
      delete-stale: true
      dry-run: false
    permissions:
      contents: write
```

**Key Inputs:**
- `stale-days` (number) - Days before branch is stale, default: `90`
- `delete-merged` (boolean) - Delete merged branches, default: `true`
- `delete-stale` (boolean) - Delete stale branches, default: `true`
- `dry-run` (boolean) - Preview without deleting, default: `false`
- `exclude-patterns` (string) - JSON array of regex patterns to exclude, default: `["main", "master", "develop", "dev", "dev/.*", "rc/.*", "release/.*", "staging", "production"]`
- `exclude-prefix` (string) - Comma-separated prefixes to exclude, default: `"dependabot/,renovate/"`

**Features:**
- Detects and deletes branches merged into default branch
- Identifies stale branches based on last commit date
- Configurable exclusion patterns (regex and prefix-based)
- Dry-run mode for previewing changes
- Detailed summary of deleted and failed branches

**Example with custom exclusions:**
```yaml
jobs:
  cleanup:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-branch-cleanup.yml@main
    with:
      stale-days: 60
      delete-merged: true
      delete-stale: true
      dry-run: false
      exclude-patterns: '["main", "master", "develop", "hotfix/.*"]'
      exclude-prefix: 'dependabot/,renovate/,feature/'
```

---

## Type-Aware Orchestration Workflows

### Project Type Detection

Automatically detects project type and provides outputs for downstream workflows.

**Usage:**
```yaml
jobs:
  detect:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-project-detector.yml@main
```

**Outputs:**
- `project-type` - Detected type: `joomla`, `dolibarr`, or `generic`
- `extension-type` - Extension type: `component`, `module`, `plugin`, `template`, `package`, or `application`
- `has-php` - Whether project contains PHP files (true/false)
- `has-node` - Whether project contains package.json (true/false)

### Type-Aware Build

Universal build workflow that adapts to project type with automatic dependency management.

**Usage:**
```yaml
jobs:
  build:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main
    with:
      php-version: '8.1'
      node-version: '20.x'
      upload-artifacts: true
```

**Key Inputs:**
- `php-version` (string) - PHP version, default: `8.1`
- `node-version` (string) - Node.js version, default: `20.x`
- `upload-artifacts` (boolean) - Upload build artifacts, default: `true`
- `artifact-name` (string) - Artifact name, default: `build-artifacts`

**Build Logic:**
- **Joomla:** Installs dependencies, runs npm build if available, prepares extension
- **Dolibarr:** Installs production dependencies, runs build scripts
- **Generic:** Runs npm build, checks for Makefile, executes build commands

### Type-Aware Release

Creates releases with type-specific packaging and marketplace support.

**Usage:**
```yaml
jobs:
  release:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-release.yml@main
    with:
      version: '1.0.0'
      prerelease: false
      create-github-release: true
    permissions:
      contents: write
```

**Key Inputs:**
- `version` (string, **required**) - Release version in semver format
- `prerelease` (boolean) - Mark as pre-release, default: `false`
- `draft` (boolean) - Create as draft, default: `false`
- `create-github-release` (boolean) - Create GitHub release, default: `true`
- `publish-to-marketplace` (boolean) - Publish to marketplace, default: `false`

**Package Creation:**
- **Joomla/Dolibarr:** ZIP package with manifest version updates
- **Generic:** TAR.GZ package with build artifacts
- All packages include SHA256 and MD5 checksums

### Type-Aware Deployment

Multi-environment deployment with type-specific logic and health checks.

**Usage:**
```yaml
jobs:
  deploy:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: staging
      deployment-method: rsync
      health-check-url: https://staging.example.com/health
    secrets:
      DEPLOY_HOST: ${{ secrets.STAGING_HOST }}
      DEPLOY_USER: ${{ secrets.STAGING_USER }}
      DEPLOY_KEY: ${{ secrets.STAGING_SSH_KEY }}
      DEPLOY_PATH: ${{ secrets.STAGING_PATH }}
    permissions:
      contents: read
      deployments: write
```

**Key Inputs:**
- `environment` (string, **required**) - Target: `staging` or `production`
- `deployment-method` (string) - Method: `rsync`, `ssh`, `ftp`, `kubernetes`, `custom`, default: `custom`
- `health-check-url` (string) - URL for post-deployment health check
- `health-check-timeout` (number) - Timeout in seconds, default: `300`

**Deployment Methods:**
- **rsync:** Direct sync to remote server
- **ssh:** Package transfer and extraction via SSH
- **custom:** Type-specific deployment logic (Joomla extension, Dolibarr module, generic app)

---

## Complete Pipeline Examples

### Example 1: Type-Aware CI/CD Pipeline

Single pipeline that works for Joomla, Dolibarr, and generic projects:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, staging, dev/**]
  pull_request:
    branches: [main]
  release:
    types: [published]

permissions:
  contents: write
  deployments: write
  pull-requests: write
  checks: write

jobs:
  # Auto-detect project type
  detect:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-project-detector.yml@main

  # Validate code
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'full'

  # Check quality (PHP projects only)
  quality:
    needs: detect
    if: needs.detect.outputs.has-php == 'true'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-versions: '["8.1", "8.2"]'

  # Test Joomla extensions
  test:
    needs: [detect, quality]
    if: needs.detect.outputs.project-type == 'joomla'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      php-versions: '["8.1", "8.2"]'
      coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  # Build (works for all types)
  build:
    needs: [detect, validate]
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main

  # Deploy to staging
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/staging'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: staging
      deployment-method: rsync
    secrets: inherit

  # Create release on tag
  release:
    needs: [detect, build]
    if: startsWith(github.ref, 'refs/tags/v')
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-release.yml@main
    with:
      version: ${{ github.ref_name }}

  # Deploy to production
  deploy-production:
    needs: release
    if: github.event_name == 'release'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: production
      version: ${{ github.event.release.tag_name }}
    secrets: inherit
```

### Example 2: Basic Quality and Testing

Simple quality and testing pipeline:

```yaml
name: Quality & Test

on: [push, pull_request]

jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'full'

  quality:
    needs: validate
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-versions: '["8.1", "8.2"]'

  test:
    needs: quality
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

---

## Best Practices

### Version Pinning

**Recommended:** Pin to main branch for automatic updates
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
```

**Stable:** Pin to specific tag
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@v1.0.0
```

**Maximum Stability:** Pin to commit SHA
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@abc1234
```

### Secret Management

**Pass all secrets:**
```yaml
secrets: inherit
```

**Pass specific secrets:**
```yaml
secrets:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
  DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

### Progressive Adoption

Start with basic validation, gradually increase strictness:

```yaml
jobs:
  # Dev branches: basic validation
  validate-dev:
    if: startsWith(github.ref, 'refs/heads/dev/')
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'basic'

  # Main branch: strict validation
  validate-main:
    if: github.ref == 'refs/heads/main'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'strict'
      fail-on-warnings: true
```

---

## Troubleshooting

### Workflow Not Found
**Error:** `Unable to resolve action mokoconsulting-tech/MokoStandards/.github/workflows/...`

**Solution:** Ensure calling repository has access to MokoStandards. For private repositories, configure proper access permissions.

### Missing Secrets
**Error:** `Secret CODECOV_TOKEN is not available`

**Solution:** Add secret at organization or repository level, or pass explicitly:
```yaml
secrets:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### Matrix Job Failures
Random matrix job failures may indicate rate limiting or resource contention.

**Solution:** Reduce concurrency
```yaml
strategy:
  matrix:
    php: ['8.1', '8.2']
  max-parallel: 2  # Limit concurrent jobs
```

### Health Check Timeout
**Solution:** Increase timeout or verify URL accessibility
```yaml
with:
  health-check-timeout: 600  # 10 minutes
```

---

## Migration from Local Workflows

**Steps:**
1. Identify workflow type (quality, testing, validation, build, release, deploy)
2. Map your inputs to reusable workflow parameters
3. Update workflow file to call reusable workflow
4. Test on development branch
5. Archive old workflow once validated

**Example Migration:**

```yaml
# Before: Local workflow
jobs:
  phpcs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
      - run: phpcs --standard=PSR12 src/

# After: Reusable workflow
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      phpcs-standard: 'PSR12'
      tools: '["phpcs"]'
```

---

## Support & Resources

**Support:**
- Documentation: [CI Migration Guide](../CI_MIGRATION_GUIDE.md)
- Issues: Open issue in MokoStandards repository
- Slack: #devops-support channel

**Related Documentation:**
- [CI Migration Guide](../CI_MIGRATION_GUIDE.md) - Detailed migration strategy
- [GitHub Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Workflow Templates](../../templates/workflows/) - Additional templates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 02.01.00 | 2026-01-11 | Added reusable-branch-cleanup workflow, standards-compliance workflow |
| 02.00.00 | 2026-01-09 | Consolidated documentation, added type-aware workflows |
| 01.00.00 | 2026-01-09 | Initial release (php-quality, joomla-testing, ci-validation) |
