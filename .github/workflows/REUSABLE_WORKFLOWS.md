<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 01.00.00
 PATH: ./.github/workflows/REUSABLE_WORKFLOWS.md
 BRIEF: Documentation for reusable GitHub Actions workflows
 -->

# Reusable Workflows

This document describes the reusable GitHub Actions workflows available in MokoStandards for use across organization repositories.

## Overview

MokoStandards provides three reusable workflows that can be called from any repository in the organization:

1. **reusable-php-quality.yml** - PHP code quality analysis
2. **reusable-joomla-testing.yml** - Joomla extension testing
3. **reusable-ci-validation.yml** - Repository standards validation

These workflows follow the [GitHub Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) pattern and can be called from other workflows using the `workflow_call` trigger.

## Workflows

### 1. PHP Quality Analysis (reusable-php-quality.yml)

Runs comprehensive PHP code quality checks using PHPCS, PHPStan, and Psalm.

#### Features
- Configurable PHP versions (default: 7.4, 8.0, 8.1, 8.2)
- Configurable quality tools (PHPCS, PHPStan, Psalm)
- Customizable coding standards and analysis levels
- Quality score output
- Parallel execution with matrix strategy
- Composer dependency caching

#### Usage Example

```yaml
name: Quality Checks

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

jobs:
  php-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-versions: '["8.0", "8.1", "8.2"]'
      tools: '["phpcs", "phpstan", "psalm"]'
      phpcs-standard: 'PSR12'
      phpstan-level: '6'
      fail-on-error: true
```

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `php-versions` | string | No | `["7.4", "8.0", "8.1", "8.2"]` | JSON array of PHP versions |
| `tools` | string | No | `["phpcs", "phpstan", "psalm"]` | JSON array of tools to run |
| `working-directory` | string | No | `.` | Working directory |
| `phpcs-standard` | string | No | `PSR12` | PHPCS coding standard |
| `phpstan-level` | string | No | `5` | PHPStan analysis level (0-9) |
| `psalm-level` | string | No | `4` | Psalm error level (1-8) |
| `fail-on-error` | boolean | No | `true` | Fail workflow on errors |

#### Outputs

| Output | Description |
|--------|-------------|
| `quality-score` | Overall quality score percentage (0-100) |

### 2. Joomla Testing (reusable-joomla-testing.yml)

Comprehensive testing workflow for Joomla extensions with matrix testing across PHP and Joomla versions.

#### Features
- Matrix testing (PHP × Joomla versions)
- Unit tests with PHPUnit
- Integration tests with Joomla installation
- MySQL database service
- Code coverage with Codecov
- Automatic incompatibility exclusions (e.g., PHP 7.4 + Joomla 5.x)

#### Usage Example

```yaml
name: Test Suite

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  joomla-tests:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      php-versions: '["7.4", "8.0", "8.1", "8.2"]'
      joomla-versions: '["4.4", "5.0", "5.1"]'
      coverage: true
      coverage-php-version: '8.1'
      coverage-joomla-version: '5.0'
      run-integration-tests: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `php-versions` | string | No | `["7.4", "8.0", "8.1", "8.2"]` | JSON array of PHP versions |
| `joomla-versions` | string | No | `["4.4", "5.0", "5.1"]` | JSON array of Joomla versions |
| `coverage` | boolean | No | `false` | Enable code coverage |
| `coverage-php-version` | string | No | `8.1` | PHP version for coverage |
| `coverage-joomla-version` | string | No | `5.0` | Joomla version for coverage |
| `working-directory` | string | No | `.` | Working directory |
| `run-integration-tests` | boolean | No | `true` | Run integration tests |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `CODECOV_TOKEN` | No | Codecov token for coverage uploads |

### 3. CI Validation (reusable-ci-validation.yml)

Repository standards validation workflow with configurable profiles and checks.

#### Features
- Three validation profiles: basic, full, strict
- Automatic project detection (PHP, Node.js)
- Manifest validation (XML)
- Changelog format validation
- License header checks
- Security checks (secret detection)
- Modular validation stages

#### Usage Example

```yaml
name: CI

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'full'
      php-version: '8.1'
      node-version: '20.x'
      validate-manifests: true
      validate-changelogs: true
      validate-licenses: true
      validate-security: true
      fail-on-warnings: false
```

#### Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `profile` | string | No | `basic` | Validation profile (basic, full, strict) |
| `node-version` | string | No | `20.x` | Node.js version |
| `php-version` | string | No | `8.1` | PHP version |
| `working-directory` | string | No | `.` | Working directory |
| `validate-manifests` | boolean | No | `true` | Validate XML manifests |
| `validate-changelogs` | boolean | No | `true` | Validate CHANGELOG.md |
| `validate-licenses` | boolean | No | `true` | Validate license headers |
| `validate-security` | boolean | No | `true` | Security checks |
| `fail-on-warnings` | boolean | No | `false` | Fail on warnings |

#### Validation Profiles

**Basic Profile**
- Required validations only
- Manifest validation
- XML well-formedness
- PHP syntax checks
- Security checks

**Full Profile**
- All basic validations
- Changelog validation
- License header checks
- Language structure checks
- Path validation
- Whitespace/tabs checks
- Version alignment

**Strict Profile**
- All full validations
- Fails on any warnings
- Strictest enforcement

## Best Practices

### 1. Version Pinning

Pin workflows to specific versions for stability:

```yaml
# Pin to main branch (latest)
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main

# Pin to specific tag
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@v1.0.0

# Pin to commit SHA (most stable)
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@abc1234
```

### 2. Secret Management

Use `secrets: inherit` to pass all organization secrets:

```yaml
jobs:
  test:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    secrets: inherit
```

Or pass specific secrets:

```yaml
jobs:
  test:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### 3. Matrix Customization

Customize the test matrix for your project:

```yaml
jobs:
  test:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      # Test only recent versions
      php-versions: '["8.1", "8.2"]'
      joomla-versions: '["5.0", "5.1"]'
```

### 4. Progressive Adoption

Start with basic validation and gradually increase strictness:

```yaml
# Development branches - basic validation
jobs:
  validate-dev:
    if: startsWith(github.ref, 'refs/heads/dev/')
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'basic'
      fail-on-warnings: false

# Main branch - strict validation
  validate-main:
    if: github.ref == 'refs/heads/main'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'strict'
      fail-on-warnings: true
```

## Complete Example

Here's a complete workflow using all three reusable workflows:

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  # Stage 1: Validation
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: 'full'
      php-version: '8.1'
      validate-security: true

  # Stage 2: Quality Checks
  quality:
    needs: validate
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-versions: '["8.0", "8.1", "8.2"]'
      tools: '["phpcs", "phpstan", "psalm"]'
      phpstan-level: '6'

  # Stage 3: Testing
  test:
    needs: quality
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      php-versions: '["8.0", "8.1", "8.2"]'
      joomla-versions: '["4.4", "5.0"]'
      coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

## Troubleshooting

### Workflow Not Found Error

**Error**: `Unable to resolve action mokoconsulting-tech/MokoStandards/.github/workflows/...`

**Solution**: Ensure the calling repository has access to MokoStandards repository. For public repositories, this should work automatically. For private repositories, ensure proper access permissions are configured.

### Missing Secrets

**Error**: `Secret CODECOV_TOKEN is not available`

**Solution**: Add the secret at the organization level or repository level, or pass it explicitly in the workflow call.

### Matrix Exclusions

Some PHP/Joomla version combinations are automatically excluded:
- PHP 7.4 + Joomla 5.x (incompatible)

If you need custom exclusions, fork the workflow or create a custom matrix.

### Cache Issues

If you experience cache-related issues:

```yaml
# Clear cache by changing the cache key
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    # Cache is automatically managed by the reusable workflow
```

## Migration Guide

### From Local Workflows

If you have local workflows that you want to migrate to these reusable workflows:

1. **Identify the workflow type** (quality, testing, validation)
2. **Map your inputs** to the reusable workflow parameters
3. **Update the workflow file** to call the reusable workflow
4. **Test the migration** on a development branch
5. **Archive the old workflow** once migration is complete

Example migration:

```yaml
# Old local workflow
jobs:
  phpcs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
      - run: phpcs --standard=PSR12 src/

# New reusable workflow
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      phpcs-standard: 'PSR12'
      tools: '["phpcs"]'
```

## Support

For questions or issues with reusable workflows:
- **Documentation**: [CI Migration Guide](../CI_MIGRATION_GUIDE.md)
- **Issues**: Open an issue in the MokoStandards repository
- **Slack**: #devops-support channel

## Related Documentation

- [CI Migration Guide](../CI_MIGRATION_GUIDE.md) - Detailed migration strategy
- [GitHub Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Workflow Templates](../../templates/workflows/) - Additional workflow templates

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 01.00.00 | 2026-01-09 | Initial release of reusable workflows |
