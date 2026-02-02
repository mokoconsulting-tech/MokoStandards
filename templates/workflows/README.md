<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: GitHub.WorkflowTemplates
INGROUP: MokoStandards.Templates
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/workflows/README.md
VERSION: 01.00.00
BRIEF: Documentation for consolidated GitHub workflow templates
-->

# GitHub Workflow Templates

## Purpose

This directory contains consolidated GitHub Actions workflow templates for use across MokoStandards-governed repositories. These templates provide standardized CI/CD configurations for different project types.

All workflow templates are documented in the unified repository schema at `schemas/unified-repository-schema.json`. The schema defines:
- Platform compatibility (generic, joomla, dolibarr, shared)
- Category (ci, build, test, release, deploy, quality, security, etc.)
- Required secrets and variables
- Permissions needed
- Requirement level (required, recommended, optional)

## Live Workflows vs Templates

**Live Workflows** (.github/workflows/) - Always active for MokoStandards repo:
- `standards-compliance.yml` - Repository standards validation
- `confidentiality-scan.yml` - Security and confidentiality checks
- `changelog_update.yml` - CHANGELOG management
- `bulk-repo-sync.yml` - Bulk repository synchronization
- `auto-create-org-projects.yml` - Organization project automation

**Templates** (templates/workflows/) - For use in governed repositories:
- All workflow templates organized by platform and purpose
- 43 workflow templates available

## Structure

The workflows are organized by platform and purpose:

### Platform-Specific Templates

**generic/** - Universal workflows for all project types
- `ci.yml` - Generic continuous integration
- `code-quality.yml` - Code quality checks
- `codeql-analysis.yml` - Security analysis
- `dependency-review.yml.template` - Dependency review
- `repo-health.yml` - Repository health checks
- `test.yml.template` - Generic testing workflow

**terraform/** - Terraform infrastructure-as-code workflows
- `ci.yml` - Terraform validation, formatting, and planning
- `deploy.yml.template` - Infrastructure deployment workflow
- `drift-detection.yml.template` - Automated drift detection

**joomla/** - Joomla extension workflows
- `ci-joomla.yml.template` - Joomla-specific CI
- `test.yml.template` - Joomla extension testing
- `release.yml.template` - Joomla package creation
- `repo_health.yml.template` - Joomla repo health
- `version_branch.yml.template` - Version management

**dolibarr/** - Dolibarr module workflows
- `ci-dolibarr.yml.template` - Dolibarr CI
- `test.yml.template` - Dolibarr module testing
- `release.yml.template` - Dolibarr package creation
- `sync-changelogs.yml.template` - Changelog synchronization

### Release & Build Templates

- `release-cycle.yml.template` - Full release cycle (main → dev → rc → version → main)
- `release-pipeline.yml.template` - Automated release pipeline
- `build.yml.template` - Universal build workflow
- `version_branch.yml` - Version branch management
- `branch-cleanup.yml.template` - Branch cleanup automation

### Reusable Workflows

- `reusable-build.yml.template` - Reusable build job
- `reusable-ci-validation.yml` - Reusable CI validation
- `reusable-deploy.yml` - Reusable deployment
- `reusable-joomla-testing.yml` - Reusable Joomla tests
- `reusable-php-quality.yml` - Reusable PHP quality checks
- `reusable-platform-testing.yml` - Reusable platform testing
- `reusable-project-detector.yml` - Project type detection
- `reusable-release.yml.template` - Reusable release job
- `reusable-script-executor.yml` - Reusable script execution

### Shared Utilities

**shared/** - Organization-wide utility workflows
- `enterprise-firewall-setup.yml.template` - Firewall configuration
- `rebuild-docs-indexes.yml.template` - Documentation indexing
- `setup-project-v2.yml.template` - Project setup automation
- `sync-docs-to-project.yml.template` - Documentation sync

### Root Templates

- `ci-joomla.yml.template` - Legacy Joomla CI template
- `repo_health.yml.template` - Legacy repo health template
- `repo_health_xml.yml.template` - XML-based repo health
├── dolibarr/                      # Dolibarr-specific workflow templates
│   ├── ci-dolibarr.yml.template   # Continuous integration for Dolibarr modules
│   ├── test.yml.template          # Testing workflow for Dolibarr modules
│   └── release.yml.template       # Automated release and deployment
└── generic/                       # Generic/platform-agnostic workflow templates
    ├── ci.yml.template            # Multi-language CI (Node.js, Python, PHP, Go, Ruby, Rust)
    ├── test.yml.template          # Comprehensive testing (unit, integration, e2e)
    ├── deploy.yml.template        # Deployment workflow for multiple environments
    ├── code-quality.yml.template  # Code quality, linting, and static analysis
    ├── codeql-analysis.yml.template # CodeQL security analysis
    └── repo_health.yml.template   # Repository health checks for generic projects
```

**Note**: All template workflow files use the `.yml.template` extension to clearly distinguish them from actual workflow files. When copying to your repository, rename them to `.yml` (e.g., `cp ci.yml.template .github/workflows/ci.yml`).

## Template Categories

### Joomla Templates (`joomla/`)

Workflow templates specifically designed for Joomla extensions (components, modules, plugins, libraries, packages, templates):

- **ci-joomla.yml.template** - Continuous integration workflow with PHP validation, XML checking, and manifest verification
- **test.yml.template** - Comprehensive testing with PHPUnit, code quality checks, and integration tests
- **release.yml.template** - Automated release workflow for creating and publishing Joomla extension packages
- **repo_health.yml.template** - Repository health monitoring including documentation checks and standards validation
- **version_branch.yml.template** - Automated version branch management and release preparation

### Dolibarr Templates (`dolibarr/`)

Workflow templates specifically designed for Dolibarr ERP/CRM modules:

- **ci-dolibarr.yml.template** - Continuous integration for Dolibarr modules with structure validation, PHP syntax checking, and security checks
- **test.yml.template** - Automated testing workflow with PHPUnit tests and Dolibarr environment integration
- **release.yml.template** - Automated release workflow for Dolibarr module packaging and deployment

### Generic Templates (`generic/`)

Platform-agnostic workflow templates for multi-language software development:

- **ci.yml.template** - Multi-language continuous integration with automatic language detection (supports Node.js, Python, PHP, Go, Ruby, Rust)
- **test.yml.template** - Comprehensive testing workflow supporting unit tests, integration tests, and end-to-end tests
- **deploy.yml.template** - Deployment workflow for staging and production environments with rollback capabilities
- **code-quality.yml.template** - Code quality analysis with linting, formatting, static analysis, dependency checks, and security scanning
- **codeql-analysis.yml.template** - CodeQL security analysis for vulnerability detection
- **repo_health.yml.template** - Repository health monitoring for generic projects

## Available Templates

### ci-joomla.yml / joomla/ci.yml
Continuous Integration workflow for Joomla component repositories.

**Features:**
- Validates Joomla manifests
- Checks XML well-formedness
- Runs PHP syntax validation
- Validates CHANGELOG structure
- Checks license headers
- Validates version alignment
- Tab and path separator checks
- Secret scanning

**Usage:**
Copy to your repository as `.github/workflows/ci.yml` and customize as needed.

### repo_health.yml / generic/repo_health.yml / joomla/repo_health.yml
Repository health and governance validation workflow.

**Features:**
- Admin-only execution gate
- Scripts governance (directory structure validation)
- Repository artifact validation (required files and directories)
- Content heuristics (CHANGELOG, LICENSE, README validation)
- Extended checks:
  - CODEOWNERS presence
  - Workflow pinning advisory
  - Documentation link integrity
  - ShellCheck validation
  - SPDX header compliance
  - Git hygiene (stale branches)

**Profiles:**
- `all` - Run all checks
- `scripts` - Scripts governance only
- `repo` - Repository health only

**Usage:**
Copy to your repository as `.github/workflows/repo_health.yml`. Requires admin permissions to run.

### version_branch.yml / joomla/version_branch.yml
Automated version branching and version bumping workflow.

**Features:**
- Creates `dev/<version>` branches from base branch
- Updates version numbers across all governed files
- Updates manifest dates
- Updates CHANGELOG with version entry
- Enterprise policy gates:
  - Required governance artifacts check
  - Branch namespace collision defense
  - Control character guard
  - Update feed enforcement

**Inputs:**
- `new_version` (required) - Version in format NN.NN.NN (e.g., 03.01.00)
- `version_text` (optional) - Version label (e.g., LTS, RC1, hotfix)
- `report_only` (optional) - Dry run mode without branch creation
- `commit_changes` (optional) - Whether to commit and push changes

**Usage:**
Copy to your repository as `.github/workflows/version_branch.yml`. Run manually via workflow_dispatch.

### joomla/test.yml
Comprehensive testing workflow for Joomla extensions.

**Features:**
- PHPUnit tests across multiple PHP and Joomla versions
- Code quality checks (PHPCS, PHPStan, Psalm)
- Integration tests with MySQL database
- Code coverage reporting with Codecov integration

**Matrix Testing:**
- PHP versions: 7.4, 8.0, 8.1, 8.2
- Joomla versions: 4.4, 5.0

**Usage:**
Copy to your repository as `.github/workflows/test.yml`.

### joomla/release.yml
Automated release and package creation workflow for Joomla extensions.

**Features:**
- Builds release packages from tags or manual triggers
- Updates version numbers in manifest files
- Creates ZIP packages with proper structure
- Generates checksums (SHA256 and MD5)
- Creates GitHub releases with changelog extraction
- Uploads release artifacts

**Triggers:**
- Push to tags matching `v*.*.*`
- Manual workflow dispatch with version input

**Usage:**
Copy to your repository as `.github/workflows/release.yml`.

### dolibarr/ci.yml
Continuous integration workflow for Dolibarr modules.

**Features:**
- Module structure validation
- PHP syntax checking across PHP 7.4-8.2 and Dolibarr 16.0-18.0
- Dolibarr API usage validation
- Database schema validation
- License header compliance
- Code quality checks (PHPCS, PHPStan)
- Security scanning (hardcoded credentials, SQL injection, XSS)

**Usage:**
Copy to your repository as `.github/workflows/ci.yml`.

### dolibarr/test.yml
Testing workflow for Dolibarr modules with full environment setup.

**Features:**
- PHPUnit tests with Dolibarr environment
- Automatic Dolibarr installation and configuration
- MySQL database integration
- Module linking and installation
- Integration tests support
- Code coverage reporting

**Usage:**
Copy to your repository as `.github/workflows/test.yml`.

### generic/ci.yml
Multi-language continuous integration workflow with automatic language detection.

**Features:**
- Automatic project language detection (Node.js, Python, PHP, Go, Ruby, Rust)
- Parallel testing across language matrices
- Language-specific linting and code quality checks
- Security scanning with Trivy
- Comprehensive test execution

**Supported Languages:**
- Node.js (16.x, 18.x, 20.x)
- Python (3.8, 3.9, 3.10, 3.11)
- PHP (7.4, 8.0, 8.1, 8.2)
- Go (1.20, 1.21, 1.22)
- Ruby (2.7, 3.0, 3.1, 3.2)
- Rust (stable, beta)

**Usage:**
Copy to your repository as `.github/workflows/ci.yml`.

### generic/test.yml
Comprehensive testing workflow supporting unit, integration, and end-to-end tests.

**Features:**
- Automatic project type detection
- Unit tests with coverage reporting
- Integration tests with PostgreSQL and Redis
- End-to-end tests with Playwright
- Codecov integration
- Test result summaries

**Usage:**
Copy to your repository as `.github/workflows/test.yml`.

### generic/deploy.yml
Deployment workflow for multiple environments with rollback capabilities.

**Features:**
- Automatic environment detection (staging, production, development)
- Multi-language build support
- Separate staging and production deployment jobs
- Smoke tests after deployment
- Automatic rollback on failure
- Deployment notifications

**Triggers:**
- Push to main or staging branches
- Release publication
- Manual workflow dispatch

**Usage:**
Copy to your repository as `.github/workflows/deploy.yml`. Configure deployment commands for your infrastructure.

### generic/code-quality.yml
Comprehensive code quality analysis workflow.

**Features:**
- Multi-language linting and formatting
  - JavaScript/TypeScript: ESLint, Prettier
  - Python: Flake8, Black, isort, Pylint, Bandit
  - PHP: PHPCS, PHP-CS-Fixer, PHPStan, Psalm
  - Go: golangci-lint, go fmt
  - Rust: cargo fmt, cargo clippy
- Static analysis with CodeQL
- Dependency security checks (Snyk, npm audit, pip safety)
- Code complexity analysis with radon
- Code coverage analysis

**Usage:**
Copy to your repository as `.github/workflows/code-quality.yml`.

## Usage

### For New Projects

1. Choose the appropriate template directory for your project type:
   - **Joomla extensions** → `joomla/`
   - **Dolibarr modules** → `dolibarr/`
   - **Other projects** → `generic/`
2. Copy the relevant workflow files to your project's `.github/workflows/` directory
3. Customize the workflow parameters as needed for your specific project:
   - Update FILE INFORMATION headers with correct paths
   - Adjust branch patterns to match your branching strategy
   - Configure environment-specific settings (deployment URLs, secrets, etc.)
4. Commit and push to enable the workflows

### For Existing Projects

1. Review your current workflows against the templates
2. Identify gaps or improvements from the standard templates
3. Update your workflows to align with current standards
4. Test changes on a feature branch before merging to main

## Integration with MokoStandards

These workflows are designed to work with:

- **Script templates** in `templates/scripts/`
- **Documentation standards** in `docs/policy/`
- **Repository layout standards** defined in README.md

## Customization Guidelines

When adapting these templates:

- **Preserve core validation steps** - Don't remove required compliance checks
- **Add project-specific steps** - Extend templates with additional validation as needed
- **Maintain naming conventions** - Keep workflow names consistent for cross-repo visibility
- **Document deviations** - If you must deviate from templates, document why in the workflow file

When copying templates to your repository:

1. **Update FILE INFORMATION headers** with correct paths
2. **Adjust branch patterns** to match your branching strategy
3. **Modify validation scripts** based on available scripts in your repository
4. **Customize required artifacts** in repo_health.yml
5. **Update allowed script directories** to match your structure

## Workflow Dependencies

### Joomla Workflows

**ci.yml requires:**
- `scripts/validate/manifest.sh`
- `scripts/validate/xml_wellformed.sh`
- Optional validation scripts in `scripts/validate/`

**test.yml requires:**
- PHPUnit configuration (`phpunit.xml` or `phpunit.xml.dist`)
- Composer for dependency management
- Optional: PHPCS, PHPStan, Psalm configurations

**release.yml requires:**
- Git tags following semver pattern (`v*.*.*`)
- XML manifest files for version updates
- Optional: CHANGELOG.md for release notes

### Dolibarr Workflows

**ci.yml requires:**
- Module descriptor in `core/modules/modMyModule.class.php`
- Proper Dolibarr module directory structure
- Optional: `scripts/validate/` directory for custom validation

**test.yml requires:**
- PHPUnit configuration
- MySQL database (provided by GitHub Actions services)
- Dolibarr installation (automated in workflow)

### Generic Workflows

**ci.yml requires:**
- Language-specific package managers (npm, pip, composer, go, bundler, cargo)
- Test configurations for your language

**test.yml requires:**
- Test framework configuration (Jest, pytest, PHPUnit, etc.)
- Optional: PostgreSQL and Redis (provided by services)
- Optional: Playwright for E2E tests

**deploy.yml requires:**
- Environment secrets configured in GitHub repository settings
- Deployment target configuration (servers, cloud platforms, etc.)

**code-quality.yml requires:**
- Optional: Snyk token for security scanning
- Language-specific linter configurations

### repo_health.yml requires:
- Python 3.x (for JSON processing)
- ShellCheck (installed automatically if needed)

### version_branch.yml requires:
- Python 3.x (for version bumping logic)
- Governance artifacts: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, etc.

## Required Workflows

All MokoStandards-governed repositories MUST implement:

1. **CI workflow** - For build validation and testing
   - Use `joomla/ci.yml` for Joomla extensions
   - Use `dolibarr/ci.yml` for Dolibarr modules
   - Use `generic/ci.yml` for other projects
2. **Repository health workflow** - For ongoing compliance monitoring

Optional but recommended:

3. **Test workflow** - For comprehensive automated testing
4. **Release workflow** - For automated release management (Joomla projects)
5. **Deploy workflow** - For automated deployments (web applications)
6. **Code quality workflow** - For advanced code analysis
7. **Version branch workflow** - For repositories using version-based branching
8. **Security scanning** - CodeQL or equivalent (now in main .github/workflows/)
9. **Dependency updates** - Dependabot (configured in .github/dependabot.yml)

## Standards Compliance

All workflows follow MokoStandards requirements:

- SPDX license headers
- GPL-3.0-or-later license
- Proper error handling and reporting
- Step summaries for GitHub Actions UI
- Audit trail generation

## Trigger Patterns

### CI Workflows
- Push to main, dev/**, rc/**, version/** branches
- Pull requests to same branches

### Repo Health
- Manual workflow_dispatch with profile selection
- Push to main (workflows, scripts, docs paths)
- Pull requests (workflows, scripts, docs paths)

### Version Branch
- Manual workflow_dispatch only (admin-level operation)

## Template Maintenance

These templates are maintained as part of MokoStandards and updated periodically:

- **Breaking changes** - Will be announced via changelog and require downstream updates
- **Non-breaking improvements** - Can be adopted at downstream projects' convenience
- **Security updates** - Must be adopted immediately per security policy

## Integration with Repository Scaffolds

These workflow templates are designed to work with project-specific repository scaffolds maintained in individual repositories. The separation allows:
- Workflow templates to be version-controlled and updated independently
- Easy discovery and comparison of workflow configurations
- Central management of CI/CD patterns across the organization

Consult the organization's scaffold repositories for complete repository layouts that integrate these workflows.

## Best Practices

1. **Pin action versions** - Use specific versions (@v4) not @main/@master
2. **Test workflows** in development branches before merging to main
3. **Review step summaries** in GitHub Actions UI after runs
4. **Use workflow concurrency** to prevent simultaneous runs
5. **Set appropriate timeouts** for long-running operations
6. **Configure secrets properly** - Use GitHub repository secrets for sensitive data
7. **Start with basic workflows** - Begin with CI and testing, then add advanced workflows
8. **Monitor workflow costs** - Be aware of GitHub Actions minutes usage
9. **Use matrix strategies** - Test across multiple versions when appropriate
10. **Document customizations** - Add comments explaining any deviations from templates

## Support and Feedback

For issues or questions about these workflows:

1. Review the workflow logs in GitHub Actions UI
2. Check the step summaries for detailed error reports
3. Validate your scripts locally before CI runs
4. Refer to MokoStandards documentation in `docs/`

For questions, issues, or suggestions regarding these workflow templates:

- Open an issue in the MokoStandards repository
- Reference specific template files in your report
- Tag with `workflow-template` label

## Compliance

Use of these templates helps ensure:

- Consistent CI/CD patterns across projects
- Automated enforcement of coding standards
- Security scanning and vulnerability detection
- Documentation and governance compliance

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | GitHub Workflow Templates README                                                                             |
| Path       | /templates/workflows/README.md                                                                               |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Workflow template documentation                                                                              |
| Status     | Active                                                                                                       |
| Effective  | 2026-01-04                                                                                                   |

## Version History

| Version  | Date       | Changes                                          |
| -------- | ---------- | ------------------------------------------------ |
| 01.01.00 | 2026-01-04 | Added comprehensive development workflow templates |
| 01.00.01 | 2026-01-04 | Consolidated templates to /templates/workflows/  |
| 01.00.00 | 2026-01-04 | Initial workflow templates for MokoStandards     |

## Revision History

| Date       | Change Description                                  | Author          |
| ---------- | --------------------------------------------------- | --------------- |
| 2026-01-04 | Added Joomla test.yml, release.yml; Dolibarr ci.yml, test.yml; Generic ci.yml, test.yml, deploy.yml, code-quality.yml | Moko Consulting |
| 2026-01-04 | Moved to /templates/workflows/ directory            | Moko Consulting |
| 2026-01-04 | Initial creation with consolidated workflow templates | Moko Consulting |
