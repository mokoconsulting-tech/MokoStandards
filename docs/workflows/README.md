# GitHub Workflow Templates Documentation

**Status**: Active | **Version**: 03.00.00 | **Effective**: 2026-01-07

## Overview

This document provides comprehensive documentation for MokoStandards workflow templates. These templates provide standardized CI/CD configurations that ensure consistency, security, and compliance across all Moko Consulting repositories.

### Workflow Documentation

- [Workflow Architecture](./workflow-architecture.md) - Workflow hierarchy and design patterns
- [Workflow Inventory](./workflow-inventory.md) - Complete inventory of workflows
- [Reusable Workflows](./reusable-workflows.md) - Documentation for reusable GitHub Actions workflows
- [Release System](./release-system.md) - Unified release system documentation
- [Changelog Management](./changelog-management.md) - Changelog management workflows and scripts
- [Dev Branch Tracking and Issue Coordination](./dev-branch-tracking.md) - Automated dev branch and PR tracking system
- [Dev Deployment](./dev-deployment.md) - Development deployment workflows

### Workflow Template Locations

MokoStandards provides workflow templates in two locations:

1. **`templates/workflows/`** - **Public workflow templates** for community adoption
   - `build-universal.yml.template` - Universal build workflow with automatic project detection
   - `release-cycle-simple.yml.template` - Automated release management workflow
   - `generic/codeql-analysis.yml` - Security scanning with CodeQL
   - `generic/dependency-review.yml.template` - Dependency vulnerability scanning
   - `standards-compliance.yml.template` - MokoStandards compliance validation
   - `flush-actions-cache.yml.template` - GitHub Actions cache management workflow

2. **`templates/workflows/`** - Platform-specific workflow examples
   - `joomla/` - Joomla extension workflows
   - `dolibarr/` - Dolibarr module workflows
   - `generic/` - Generic project workflows

### Quick Start

To adopt MokoStandards workflows in your repository:

```bash
# Copy universal build workflow
cp templates/workflows/build-universal.yml.template .github/workflows/build.yml

# Copy release management workflow
cp templates/workflows/release-cycle-simple.yml.template .github/workflows/release.yml

# Copy security scanning workflows
cp templates/workflows/generic/codeql-analysis.yml .github/workflows/
cp templates/workflows/generic/dependency-review.yml.template .github/workflows/dependency-review.yml

# Copy standards compliance workflow
cp templates/workflows/standards-compliance.yml.template .github/workflows/standards-compliance.yml

# Optional: Copy cache management workflow
cp templates/workflows/flush-actions-cache.yml.template .github/workflows/flush-actions-cache.yml
```

Then customize the workflows for your project as needed.

## Public Workflow Templates (`templates/workflows/`)

### 1. Build Universal (`build-universal.yml.template`)

**Location**: `templates/workflows/build-universal.yml.template`

Universal build workflow with automatic project type detection and Makefile precedence system.

**Features**:
- **Automatic project detection** - Detects Joomla, Dolibarr, or Generic projects
- **Makefile precedence system** - Repository Makefile → MokoStandards Makefile → Default builds
- **Multi-language support** - PHP, Node.js, and mixed projects
- **Build artifacts** - Automatic artifact upload
- **Customizable** - Extensive inline documentation for customization

**Trigger Patterns**:
```yaml
on:
  push:
    branches: [main, dev/**, rc/**, version/**]
  pull_request:
    branches: [main, dev/**, rc/**]
  workflow_dispatch:
```

**Usage**: Copy to `.github/workflows/build.yml` and customize as needed.

See [Build System Documentation](../build-system/README.md) for details on the Makefile precedence system.

### 2. Release Cycle (`release-cycle-simple.yml.template`)

**Location**: `templates/workflows/release-cycle-simple.yml.template`

Automated release management workflow implementing the MokoStandards release cycle: main → dev → rc → version → main.

**Features**:
- **Semantic versioning** - Automatic validation of version format
- **Branch management** - Automated branch creation and merging
- **Release actions** - start-release, create-rc, finalize-release, hotfix
- **Release notes** - Automated generation from commits
- **GitHub releases** - Automatic creation with artifacts

**Actions**:
- `start-release` - Create development branch and update version
- `create-rc` - Create release candidate from dev branch
- `finalize-release` - Create version branch, merge to main, create release
- `hotfix` - Create hotfix branch for emergency fixes

**Trigger Pattern**:
```yaml
on:
  workflow_dispatch:
    inputs:
      action:
        type: choice
        options: [start-release, create-rc, finalize-release, hotfix]
      version:
        type: string
        required: true
```

**Usage**: Copy to `.github/workflows/release.yml` for automated release management.

See [Release Management Documentation](../release-management/README.md) for complete release procedures.

### 3. Dependency Review (`dependency-review.yml.template`)

**Location**: `templates/workflows/generic/dependency-review.yml.template`

Comprehensive dependency vulnerability scanning for pull requests.

**Features**:
- **GitHub Dependency Review** - Scans dependencies in PRs
- **npm audit** - Node.js dependency security checks
- **Composer audit** - PHP dependency security checks
- **Python Safety** - Python dependency vulnerability scanning
- **License compliance** - Validates dependency licenses

**Trigger Pattern**:
```yaml
on:
  pull_request:
    branches: [main, dev/**, rc/**]
```

**Usage**: Copy to `.github/workflows/dependency-review.yml` to enable dependency scanning on PRs.

### 4. Standards Compliance (`standards-compliance.yml.template`)

**Location**: `templates/workflows/standards-compliance.yml.template`

MokoStandards compliance validation workflow.

**Features**:
- **Repository structure** - Validates required directories and files
- **Documentation quality** - Checks README, CHANGELOG, and other docs
- **Coding standards** - Tab detection, encoding, line endings
- **License compliance** - SPDX header validation
- **Git hygiene** - .gitignore, large files, etc.
- **Workflow validation** - YAML syntax and required workflows

**Trigger Pattern**:
```yaml
on:
  push:
    branches: [main, dev/**, rc/**]
  pull_request:
    branches: [main, dev/**, rc/**]
  workflow_dispatch:
```

**Usage**: Copy to `.github/workflows/standards-compliance.yml` to enable compliance checks.

### 5. Flush Actions Cache (`flush-actions-cache.yml.template`)

**Location**: `templates/workflows/flush-actions-cache.yml.template`

Cache management workflow for flushing GitHub Actions caches on demand.

**Features**:
- **Manual trigger** - Run from Actions tab when needed
- **Filter by branch** - Target specific branch caches
- **Filter by key pattern** - Target specific dependency caches (composer, node)
- **Dry-run mode** - Preview deletions before executing
- **Comprehensive reporting** - Shows cache details before deletion
- **Automatic script download** - Downloads latest flush script from MokoStandards

**Trigger Pattern**:
```yaml
on:
  workflow_dispatch:
    inputs:
      branch:
        description: 'Branch to filter caches (leave empty for all branches)'
      key-pattern:
        description: 'Key pattern to filter caches (e.g., composer, node)'
      dry-run:
        description: 'Dry run mode (show what would be deleted without deleting)'
        type: boolean
```

**Common Use Cases**:
- Clear all caches when corrupted
- Clear branch-specific caches after branch deletion
- Clear dependency caches after major updates (Composer, npm)
- Preview cache usage with dry-run mode

**Usage**: Copy to `.github/workflows/flush-actions-cache.yml` to enable cache management.

See [flush_actions_cache.py documentation](/docs/scripts/maintenance/flush-actions-cache-py.md) for detailed script usage.

### 6. CodeQL Analysis (`codeql-analysis.yml`)

**Location**: `templates/workflows/generic/codeql-analysis.yml`

Security scanning with GitHub's CodeQL engine (also available in `.github/workflows/`).

See section below for complete details.

## Platform-Specific Workflow Templates (`templates/workflows/`)

The following templates are organized by platform in `templates/workflows/`.

### 1. CI Template (`ci.yml`)

**Location**: `.github/workflows/ci.yml` (MokoStandards root)

Continuous Integration workflow that enforces repository standards through automated validation.

**Features**:
- **Manifest validation** - Validates project manifests (Joomla XML, Dolibarr descriptors)
- **XML well-formedness** - Ensures all XML files are properly formatted
- **PHP syntax validation** - Checks PHP code across multiple versions
- **CHANGELOG structure** - Validates changelog formatting and completeness
- **License headers** - Verifies SPDX headers in all source files
- **Version alignment** - Ensures version numbers are consistent across files
- **Path separator checks** - Validates file paths
- **Tab detection** - Enforces space-over-tabs policy
- **Secret scanning** - Prevents accidental secret commits

**Trigger Patterns**:
```yaml
on:
  push:
    branches: [main, dev/**, rc/**, version/**]
  pull_request:
    branches: [main, dev/**, rc/**, version/**]
```

**Usage**: Copy from MokoStandards `.github/workflows/ci.yml` to your repository.

### 2. CodeQL Analysis Template (`codeql-analysis.yml`)

**Location**: `.github/workflows/codeql-analysis.yml` (MokoStandards root)

Security scanning workflow using GitHub's CodeQL engine for vulnerability detection.

**Features**:
- **Multi-language support** - Analyzes Python, JavaScript, PHP, Go, etc.
- **Security-extended queries** - Uses comprehensive security query packs
- **Quality analysis** - Includes code quality checks
- **Scheduled scans** - Weekly automated security scans (Monday 6:00 AM UTC)
- **PR integration** - Scans all pull requests automatically

**Trigger Patterns**:
```yaml
on:
  push:
    branches: [main, dev/**, rc/**]
  pull_request:
    branches: [main, dev/**, rc/**]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6:00 AM UTC
  workflow_dispatch:
```

**Usage**: Copy from MokoStandards `.github/workflows/codeql-analysis.yml` to your repository.

### 3. Dependency Review

**Purpose**: Automated dependency vulnerability scanning

Dependency scanning in MokoStandards repositories is handled through:
- **Dependabot configuration** - `.github/dependabot.yml` (configure for your project)
- **CodeQL analysis** - Includes dependency checks
- **Generic code quality workflow** - `templates/workflows/generic/code-quality.yml`

**Recommended Approach**:
1. Enable Dependabot in repository settings
2. Create `.github/dependabot.yml` configuration
3. Use CodeQL for comprehensive security analysis

### 4. Standards Compliance Template (`repo_health.yml`)

**Location**: `templates/workflows/generic/repo_health.yml`

Repository health and governance validation workflow that enforces MokoStandards compliance.

**Features**:
- **Admin-only execution** - Requires admin permissions
- **Release configuration checks** - Validates SFTP deployment variables
- **SFTP connectivity testing** - Tests remote server access
- **Scripts governance** - Validates script directory structure
- **Repository artifacts** - Checks required files (README, LICENSE, CONTRIBUTING, etc.)
- **Content heuristics** - Validates document content and structure
- **Extended checks** (optional):
  - CODEOWNERS presence
  - Workflow action version pinning
  - Documentation link integrity
  - ShellCheck validation
  - SPDX header compliance
  - Git hygiene (stale branches)

**Profiles**:
- `all` - Run all checks (default)
- `release` - Release configuration only
- `scripts` - Scripts governance only
- `repo` - Repository health only

**Trigger Pattern**:
```yaml
on:
  workflow_dispatch:
    inputs:
      profile:
        type: choice
        options: [all, release, scripts, repo]
```

**Usage**: Copy from `templates/workflows/generic/repo_health.yml` and customize for your project.

### 5. Platform-Specific Workflows

#### Joomla Workflows (`templates/workflows/joomla/`)

**ci.yml** - Joomla extension CI workflow:
- Joomla manifest validation
- Extension structure checks
- PHP 7.4-8.2 compatibility
- XML schema validation

**test.yml** - Comprehensive Joomla testing:
- PHPUnit tests with Joomla framework
- Code quality (PHPCS, PHPStan, Psalm)
- Matrix testing: PHP 7.4-8.2, Joomla 4.4-5.0
- Code coverage with Codecov

**release.yml** - Automated Joomla package creation:
- Version bumping in manifests
- ZIP package creation with proper structure
- Checksum generation (SHA256, MD5)
- GitHub release creation with changelog
- Release artifact upload

#### Dolibarr Workflows (`templates/workflows/dolibarr/`)

**ci.yml** - Dolibarr module CI workflow:
- Module structure validation
- PHP syntax checking (7.4-8.2)
- Dolibarr API usage validation (16.0-18.0)
- Database schema validation
- Security scanning (SQL injection, XSS, credentials)

**test.yml** - Dolibarr module testing:
- PHPUnit tests with Dolibarr environment
- Automatic Dolibarr installation
- MySQL database integration
- Module linking and installation
- Code coverage reporting

#### Generic Workflows (`templates/workflows/generic/`)

**ci.yml** - Multi-language CI with auto-detection:
- Supports: Node.js, Python, PHP, Go, Ruby, Rust
- Automatic language detection
- Parallel testing across language matrices
- Language-specific linting
- Security scanning with Trivy

**test.yml** - Comprehensive testing framework:
- Unit tests with coverage
- Integration tests (PostgreSQL, Redis)
- End-to-end tests with Playwright
- Codecov integration
- Test result summaries

**deploy.yml** - Multi-environment deployment:
- Automatic environment detection
- Multi-language build support
- Staging and production deployment jobs
- Smoke tests after deployment
- Automatic rollback on failure
- Deployment notifications

**code-quality.yml** - Advanced code analysis:
- Multi-language linting (ESLint, Flake8, PHPCS, golangci-lint, clippy)
- Code formatting validation
- Static analysis (CodeQL, PHPStan, Pylint)
- Dependency security (Snyk, npm audit, pip safety)
- Code complexity analysis

## Platform Detection

Workflows use automatic project type detection based on file presence. See [Project Type Detection](../reference/project-types.md) for complete details.

### Quick Reference

- **Joomla**: Detected by `joomla.xml` manifest file
- **Dolibarr**: Detected by `htdocs/` directory or `core/modules/` structure
- **Generic**: Fallback for all other projects

## Usage Instructions

### For New Projects

1. **Choose appropriate templates**:
   - Joomla → `templates/workflows/joomla/`
   - Dolibarr → `templates/workflows/dolibarr/`
   - Other → `templates/workflows/generic/`

2. **Copy workflow files**:
   ```bash
   mkdir -p .github/workflows
   cp /path/to/MokoStandards/templates/workflows/joomla/ci.yml .github/workflows/
   ```

3. **Customize for your project**:
   - Update FILE INFORMATION headers with correct paths
   - Adjust branch patterns if needed
   - Configure environment-specific settings
   - Add/remove validation scripts as appropriate

4. **Commit and enable**:
   ```bash
   git add .github/workflows/
   git commit -m "Add MokoStandards workflows"
   git push
   ```

### For Existing Projects

1. Review current workflows against templates
2. Identify gaps or outdated patterns
3. Update workflows incrementally
4. Test on feature branch before merging to main

## Required Workflows

All MokoStandards-governed repositories **MUST** implement:

1. **CI workflow** - For build validation and testing
2. **Security scanning** - CodeQL or equivalent

Recommended workflows:
- Repository health workflow
- Platform-specific test workflows
- Automated release workflows (for libraries/extensions)
- Deployment workflows (for applications)
- Code quality workflows

## Workflow Dependencies

### Common Requirements (All Workflows)

- Git repository with proper branching structure
- Python 3.x for validation scripts
- Proper permissions configured in repository settings

### CI Workflows Require

**For Joomla**:
- `scripts/validate/manifest.sh`
- `scripts/validate/xml_wellformed.sh`
- Joomla XML manifest file

**For Dolibarr**:
- Module descriptor (`core/modules/modMyModule.class.php`)
- Proper Dolibarr directory structure

**For Generic**:
- Language-specific package managers (npm, pip, composer, etc.)
- Test configurations

### Test Workflows Require

- Test framework configuration (Jest, pytest, PHPUnit, etc.)
- Optional: Database services (configured in workflow)
- Optional: Browser testing tools (Playwright)

### Deployment Workflows Require

- Environment secrets in GitHub repository settings
- Deployment target configuration
- For SFTP deployments: See [SFTP Deployment Guide](../deployment/sftp.md)

## Standards Compliance

All workflows follow MokoStandards requirements:

- ✅ SPDX license headers (GPL-3.0-or-later)
- ✅ Proper error handling and reporting
- ✅ Step summaries for GitHub Actions UI
- ✅ Audit trail generation
- ✅ Secure secret handling
- ✅ Versioned action dependencies

## Best Practices

1. **Pin action versions** - Use `@v4` not `@main`
2. **Test in feature branches** - Never merge untested workflows
3. **Use workflow concurrency** - Prevent duplicate runs
4. **Set appropriate timeouts** - Avoid hanging workflows
5. **Configure secrets properly** - Use GitHub repository secrets
6. **Monitor costs** - Track GitHub Actions minutes usage
7. **Document customizations** - Add comments for deviations
8. **Review step summaries** - Check GitHub Actions UI after runs
9. **Use matrix strategies** - Test across multiple versions
10. **Keep workflows DRY** - Use reusable workflows when possible

## Integration with Health Scoring

These workflows contribute to the [Health Scoring System](../policy/health-scoring.md):

- **CI/CD Status**: 15 points - CI workflow passing
- **Workflows**: 10 points - Required workflows present
- **Security**: 15 points - CodeQL and dependency scanning enabled

## Support and Troubleshooting

### Common Issues

**Workflow fails to find scripts**:
- Ensure scripts exist in expected locations
- Verify script permissions (`chmod +x`)
- Check FILE INFORMATION paths match actual structure

**SFTP connectivity fails**:
- Verify all required secrets are configured
- Test credentials manually
- Check firewall/network access
- See [SFTP Deployment Guide](../deployment/sftp.md)

**CodeQL fails**:
- Ensure language matrix includes project languages
- Remove languages with no code to analyze
- Review CodeQL queries configuration

### Getting Help

1. Review workflow logs in GitHub Actions UI
2. Check step summaries for detailed errors
3. Validate scripts locally before CI
4. Refer to [Project Types Documentation](../reference/project-types.md)
5. Consult [SFTP Deployment Guide](../deployment/sftp.md)

For issues with templates:
- Open issue in MokoStandards repository
- Tag with `workflow-template` label
- Include workflow name and error details

## Metadata

| Field | Value |
|---|---|
| Document | Workflow Templates Documentation |
| Path | /docs/workflows/README.md |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
| Owner | Moko Consulting |
| Status | Active |
| Version | 03.00.00 |
| Effective | 2026-01-07 |

## Version History

| Version | Date | Changes |
|---|---|---|
| 03.00.00 | 2026-01-07 | Added public workflow templates documentation (build-universal, release-cycle, dependency-review, standards-compliance) |
| 01.00.00 | 2026-01-07 | Initial comprehensive workflow documentation |

## See Also

- [Build System Documentation](../build-system/README.md)
- [Release Management Documentation](../release-management/README.md)
- [Health Scoring System](../policy/health-scoring.md)
- [SFTP Deployment Guide](../deployment/sftp.md)
- [Project Type Detection](../reference/project-types.md)
- [Repository Structure Schema](../guide/repository-structure-schema.md)
- [Workflow Templates (Technical)](../../templates/workflows/README.md)
- [Public Workflow Templates](../../templates/workflows/)
