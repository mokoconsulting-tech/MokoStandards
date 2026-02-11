[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Public Architecture Guide

This document describes the public-facing architecture patterns and best practices used in MokoStandards for building maintainable, scalable open-source projects.

## Overview

MokoStandards provides a flexible, reusable framework for implementing consistent CI/CD pipelines, coding standards, and project structures across multiple repositories and project types.

## Architecture Principles

### 1. Separation of Concerns

- **Reusable Workflows**: Generic, configurable workflows that can be called from any repository
- **Project-Specific Configuration**: Project-level settings and overrides
- **Centralized Standards**: Common rules maintained in one place

### 2. Template Inheritance

Projects can inherit and customize standards at multiple levels:

```
MokoStandards (Base)
    ↓
Project Type Templates (Joomla, Dolibarr, Generic)
    ↓
Organization Standards
    ↓
Individual Project Configuration
```

### 3. Configuration Management

Configuration is managed through a hierarchy:

1. **Default values** in reusable workflows
2. **Template defaults** in template files
3. **Project overrides** in individual repositories
4. **Runtime parameters** passed to workflows

## Architecture Components

### Reusable Workflows

Reusable workflows are the core of the MokoStandards architecture:

```yaml
# In your project's .github/workflows/ci.yml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
    secrets: inherit
```

**Key Reusable Workflows:**

- `reusable-ci-validation.yml` - Main CI validation pipeline
- `reusable-project-detector.yml` - Project type detection
- `repo-health.yml` - Repository health checks
- `reusable-build.yml` - Build automation
- `reusable-deploy.yml` - Deployment automation
- `reusable-php-quality.yml` - PHP quality checks
- `reusable-joomla-testing.yml` - Joomla-specific testing

### Project Type Detection

Automatic detection of project types enables appropriate validation:

```
[Repository] → [Detector] → [Project Type] → [Appropriate Validation]
                                ↓
                          joomla/dolibarr/generic
```

See [PROJECT_TYPE_DETECTION.md](PROJECT_TYPE_DETECTION.md) for details.

### Validation Profiles

Three validation profiles provide flexibility:

| Profile | Use Case | Speed | Thoroughness |
|---------|----------|-------|--------------|
| **basic** | Quick feedback during development | Fast | Essential checks only |
| **full** | Standard PR validation | Medium | Comprehensive validation |
| **strict** | Release validation | Slow | Maximum validation |

## CI/CD Patterns

### Pattern 1: Simple CI

For basic projects needing only validation:

```yaml
name: CI
on: [push, pull_request]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
    secrets: inherit
```

### Pattern 2: CI with Build

For projects that need to build artifacts:

```yaml
name: CI
on: [push, pull_request]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
    secrets: inherit

  build:
    needs: validate
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main
    with:
      build-command: npm run build
    secrets: inherit
```

### Pattern 3: Full CI/CD Pipeline

For projects with deployment:

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: ${{ github.event_name == 'push' && 'strict' || 'full' }}
    secrets: inherit

  build:
    needs: validate
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main
    secrets: inherit

  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: production
    secrets: inherit
```

### Pattern 4: Multi-Environment

For projects deploying to multiple environments:

```yaml
jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: strict
    secrets: inherit

  deploy-staging:
    needs: validate
    if: github.ref == 'refs/heads/develop'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: staging
    secrets: inherit

  deploy-production:
    needs: validate
    if: github.ref == 'refs/heads/main'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: production
    secrets: inherit
```

## Configuration Strategies

### Strategy 1: Minimal Configuration

Use workflow defaults for quick setup:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    secrets: inherit
```

### Strategy 2: Project-Specific Configuration

Override defaults for your project:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      php-version: '8.2'
      node-version: '20.x'
      validate-manifests: true
      validate-changelogs: true
      validate-licenses: true
      validate-security: true
    secrets: inherit
```

### Strategy 3: Environment-Based Configuration

Different configurations per environment:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: ${{ github.ref == 'refs/heads/main' && 'strict' || 'full' }}
      fail-on-warnings: ${{ github.ref == 'refs/heads/main' }}
    secrets: inherit
```

## Standards Enforcement

### Automated Enforcement

Standards are enforced automatically through:

1. **Pre-commit hooks** - Local validation before commit
2. **Pull request checks** - Required status checks
3. **Branch protection rules** - Prevent merging non-compliant code
4. **Automated fixes** - Auto-format and fix simple issues

### Progressive Enhancement

Adopt standards incrementally:

```yaml
# Phase 1: Start with basic validation
with:
  profile: basic
  validate-security: true

# Phase 2: Add more validations
with:
  profile: full
  validate-security: true
  validate-licenses: true

# Phase 3: Full compliance
with:
  profile: strict
  validate-manifests: true
  validate-changelogs: true
  validate-licenses: true
  validate-security: true
  fail-on-warnings: true
```

## Security Practices

### Secret Scanning

Automated secret scanning prevents accidental credential exposure:

- Scan all files for common secret patterns
- Exclude documentation and test fixtures
- Fail builds if secrets are detected
- Provide remediation guidance

### Dependency Scanning

Monitor dependencies for vulnerabilities:

- Automated dependency updates (Dependabot)
- Security advisories monitoring
- License compliance checking

### Access Control

Proper permissions for workflows:

```yaml
permissions:
  contents: read          # Read repository code
  pull-requests: write    # Comment on PRs
  checks: write          # Create check runs
  issues: write          # Create issues (for health checks)
```

## Testing Strategies

### Test Pyramid

```
           E2E Tests
        ↗            ↖
   Integration Tests
  ↗                    ↖
Unit Tests
```

### Test Organization

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests
└── e2e/           # End-to-end tests
```

### Continuous Testing

Tests run automatically on:

- Every commit (unit tests)
- Pull requests (unit + integration)
- Pre-release (full test suite)

## Documentation Patterns

### Essential Documentation

Every project should include:

```
/
├── README.md              # Project overview and quick start
├── CONTRIBUTING.md        # How to contribute
├── CODE_OF_CONDUCT.md    # Community guidelines
├── SECURITY.md           # Security policy
├── CHANGELOG.md          # Version history
├── LICENSE               # License file
└── docs/
    ├── architecture.md   # Architecture decisions
    ├── api.md           # API documentation
    └── development.md   # Development guide
```

### Documentation as Code

- Store docs with code
- Version docs with code
- Review docs in PRs
- Generate docs from code (JSDoc, PHPDoc, etc.)

## Extensibility

### Custom Validations

Add project-specific validations:

```yaml
jobs:
  standard-validation:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    secrets: inherit

  custom-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Custom validation
        run: ./scripts/custom-validate.sh
```

### Plugin Architecture

Extend functionality through:

- Custom validation scripts
- Additional workflow jobs
- Webhook integrations
- GitHub Apps

## Best Practices

### 1. Keep Workflows DRY

Don't repeat yourself - use reusable workflows:

```yaml
# ❌ Don't repeat workflow logic
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]
  test:
    runs-on: ubuntu-latest
    steps: [...]

# ✅ Use reusable workflow
jobs:
  ci:
    uses: org/repo/.github/workflows/reusable-ci.yml@main
```

### 2. Version Your Workflows

Pin workflow versions for stability:

```yaml
# ❌ Unstable - uses latest
uses: org/repo/.github/workflows/ci.yml@main

# ✅ Stable - pinned version
uses: org/repo/.github/workflows/ci.yml@v1.2.3

# ✅ Acceptable - pinned major version
uses: org/repo/.github/workflows/ci.yml@v1
```

### 3. Fail Fast

Configure workflows to fail early:

```yaml
with:
  fail-on-warnings: true    # Don't allow warnings
  profile: strict           # Maximum validation
```

### 4. Provide Feedback

Make failures actionable:

- Clear error messages
- Link to documentation
- Suggest fixes
- Show examples

### 5. Monitor and Iterate

Continuously improve your workflows:

- Track workflow success rates
- Monitor execution times
- Gather developer feedback
- Update standards regularly

## Performance Optimization

### Caching

Use caching to speed up workflows:

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.composer/cache
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/composer.lock', '**/package-lock.json') }}
```

### Parallel Execution

Run independent jobs in parallel:

```yaml
jobs:
  lint:     # Runs in parallel with test
    runs-on: ubuntu-latest
    steps: [...]

  test:     # Runs in parallel with lint
    runs-on: ubuntu-latest
    steps: [...]

  build:    # Waits for lint and test
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps: [...]
```

### Matrix Builds

Test across multiple configurations:

```yaml
jobs:
  test:
    strategy:
      matrix:
        php-version: ['8.1', '8.2', '8.3']
        node-version: ['18.x', '20.x']
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
```

## Related Documentation

- [Project Type Detection](PROJECT_TYPE_DETECTION.md)
- [Health Scoring](../policy/health-scoring.md)
- [Reusable Workflows](../.github/workflows/REUSABLE_WORKFLOWS.md)

## Contributing

Improvements to this architecture are welcome! Please:

1. Open an issue to discuss changes
2. Follow existing patterns
3. Document new patterns
4. Provide examples

---

**Version:** 1.0.0
**Last Updated:** 2026-01-13
**License:** GPL-3.0-or-later

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/PUBLIC_ARCHITECTURE.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
