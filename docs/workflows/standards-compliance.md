[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Standards Compliance Workflow

**Workflow**: `standards-compliance.yml`  
**Status**: Active | **Last Updated**: 2026-02-21

## Overview

The Standards Compliance workflow is a comprehensive validation system that ensures repositories meet MokoStandards requirements across multiple dimensions including structure, documentation quality, coding standards, security, and maintainability.

## Purpose

- **Enforce Standards**: Automatically validate compliance with MokoStandards policies
- **Quality Assurance**: Ensure consistent quality across all organization repositories
- **Early Detection**: Catch compliance issues before merge
- **Actionable Feedback**: Provide clear remediation steps for any violations
- **Comprehensive Reporting**: Generate detailed compliance reports with scores

## Workflow Triggers

```yaml
on:
  push:
    branches:
      - main
      - dev/**
      - rc/**
  pull_request:
    branches:
      - main
      - dev/**
      - rc/**
  workflow_dispatch:
```

**Runs on**:
- Every push to main, dev/*, or rc/* branches
- Every pull request targeting main, dev/*, or rc/*
- Manual trigger via GitHub Actions UI

## Validation Areas

The workflow performs 10 comprehensive validation checks organized into two categories:

### Critical Checks (Must Pass)

These checks are **blocking** - the workflow will fail if any critical check fails:

| Check | Description | Validator | Priority |
|-------|-------------|-----------|----------|
| 📁 **Repository Structure** | Validates required directories and files exist | Built-in shell | 🔴 Critical |
| 📚 **Documentation Quality** | Analyzes README, checks documentation completeness | Built-in shell | 🔴 Critical |
| 💻 **Coding Standards** | Runs language-specific linters (Python, PHP, YAML) | yamllint, black, pylint, phpcs | 🔴 Critical |
| ⚖️ **License Compliance** | Validates license file and SPDX identifiers | Built-in shell | 🔴 Critical |
| 🧹 **Git Repository Hygiene** | Checks commit messages, branch naming, .gitignore | Built-in shell | 🔴 Critical |
| ⚙️ **Workflow Configuration** | Validates GitHub Actions workflow files | actionlint, custom checks | 🔴 Critical |
| 🔢 **Version Consistency** | Ensures all version numbers match across repository | check_version_consistency.php | 🔴 Critical |
| 🔐 **Script Integrity** | Validates SHA-256 hashes of critical scripts | validate_script_registry.py | 🔴 Critical |

### Informational Checks (Non-Blocking)

These checks provide **recommendations** but don't fail the workflow:

| Check | Description | Validator | Priority |
|-------|-------------|-----------|----------|
| 🏢 **Enterprise Readiness** | Assesses enterprise-grade features and patterns | check_enterprise_readiness.php | ℹ️ Info |
| 🏥 **Repository Health** | Evaluates overall repository quality metrics | check_repo_health.php | ℹ️ Info |

## Detailed Check Descriptions

### 1. Repository Structure Validation

**What it checks**:
- Required directories: `docs/`, `scripts/`, `.github/`
- Required files: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.editorconfig`
- File size and completeness validation

**Compliance Requirements**:
- All required directories must exist
- All required files must be present
- README must be at least 500 bytes
- LICENSE must be at least 100 bytes

**Remediation**:
```bash
# Create missing directories
mkdir -p docs scripts .github/workflows

# Create required files from templates
cp templates/docs/required/README.md ./
cp templates/docs/required/CONTRIBUTING.md ./
cp templates/docs/required/SECURITY.md ./
```

### 2. Documentation Quality Check

**What it checks**:
- README.md metrics (size, lines, words, headings, links, code blocks)
- Documentation completeness
- Content quality indicators

**Compliance Requirements**:
- README minimum 500 bytes, 20 lines, 100 words
- At least 3 headings for structure
- Include links and code examples

**Scoring**:
- Size: 500+ bytes (good), <500 (warning), >50KB (warning - too long)
- Headings: 3+ (good), <3 (warning)
- Links: 1+ (good), 0 (info - consider adding)
- Code blocks: 1+ (good), 0 (info - consider adding)

### 3. Coding Standards Validation

**What it checks**:
- YAML files: Validates syntax and formatting with `yamllint`
- Python files: Code formatting with `black`, linting with `pylint`
- PHP files: Coding standards with `phpcs` (PSR-12)

**Compliance Requirements**:
- All YAML files must be valid and properly formatted
- Python code must follow Black formatting
- PHP code must follow PSR-12 standards

**Remediation**:
```bash
# Fix YAML formatting
yamllint --format auto .github/workflows/*.yml

# Fix Python formatting
black scripts/**/*.py

# Fix PHP code style
phpcs --standard=PSR12 src/
```

### 4. License Compliance

**What it checks**:
- LICENSE file exists
- File headers contain copyright and SPDX identifiers
- Consistent licensing across repository

**Compliance Requirements**:
- LICENSE file present at repository root
- All source files include copyright header
- SPDX-License-Identifier present in headers

**Example Header**:
```php
<?php
// Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
// SPDX-License-Identifier: GPL-3.0-or-later
```

### 5. Git Repository Hygiene

**What it checks**:
- Commit message format
- Branch naming conventions
- .gitignore completeness
- No sensitive files in repository

**Compliance Requirements**:
- Conventional commit messages
- Branch names follow pattern: `feature/*`, `bugfix/*`, `hotfix/*`, `release/*`
- Comprehensive .gitignore file

### 6. Workflow Configuration Validation

**What it checks**:
- Valid YAML syntax in workflow files
- Required workflows present
- CodeQL configuration if applicable
- Action version pinning for security

**Compliance Requirements**:
- All workflows have valid YAML syntax
- Actions pinned to commit hashes for security
- Proper permissions configured

### 7. Version Consistency Check ⭐ NEW

**What it checks**:
- All version references match the canonical version in `composer.json`
- Checks 39+ files including:
  - Documentation (README.md, CHANGELOG.md, CONTRIBUTING.md)
  - Workflows (.github/workflows/*.yml)
  - PHP source files (src/**/*.php)
  - Configuration files

**Compliance Requirements**:
- Single source of truth: version in `composer.json`
- All references must match exactly
- No version drift across repository

**Validator**: `scripts/validate/check_version_consistency.php`

**Remediation**:
```bash
# Check current status
php scripts/validate/check_version_consistency.php --verbose

# Update all version references (if mismatches found)
# Manually update files or use bulk search/replace
```

### 8. Script Integrity Validation ⭐ NEW

**What it checks**:
- SHA-256 hashes of critical scripts match registry
- No unauthorized modifications to security-critical scripts
- Registry file (scripts/.script-registry.json) is up-to-date

**Compliance Requirements**:
- All scripts in registry must have valid SHA-256 hashes
- Critical priority scripts cannot have mismatches
- Changes to scripts must update registry

**Validator**: `scripts/maintenance/validate_script_registry.py`

**Remediation**:
```bash
# Validate current hashes
python3 scripts/maintenance/validate_script_registry.py --priority critical

# Update registry after legitimate changes
python3 scripts/maintenance/generate_script_registry.py --update

# Or use auto-update workflow
# .github/workflows/auto-update-sha.yml
```

### 9. Enterprise Readiness Check ⭐ NEW (Informational)

**What it checks**:
- Enterprise-grade features implementation
- Security best practices
- Scalability patterns
- Error handling and logging
- Transaction management
- API design patterns

**Assessment Areas**:
- Architecture patterns
- Error recovery mechanisms
- Monitoring and observability
- Documentation completeness
- Test coverage
- Security controls

**Validator**: `scripts/validate/check_enterprise_readiness.php`

**Note**: This check is **informational only** and does not block merges. It provides recommendations for improving enterprise readiness.

### 10. Repository Health Check ⭐ NEW (Informational)

**What it checks**:
- Code quality metrics
- Technical debt indicators
- Dependency health
- Documentation coverage
- Test coverage
- Issue/PR activity

**Health Metrics**:
- File structure organization
- Code duplication
- Dependency freshness
- Security vulnerabilities
- Community engagement

**Validator**: `scripts/validate/check_repo_health.php`

**Note**: This check is **informational only** and does not block merges. It provides insights for continuous improvement.

## Compliance Scoring

The workflow calculates a compliance percentage based on critical checks:

```
Compliance % = (Critical Checks Passed / Total Critical Checks) × 100
```

### Score Interpretation

| Score | Status | Description |
|-------|--------|-------------|
| 100% | ✅ **COMPLIANT** | All critical checks passed - repository fully compliant |
| 80-99% | ⚠️ **MOSTLY COMPLIANT** | Most checks passed - minor issues to address |
| 50-79% | ⚠️ **PARTIALLY COMPLIANT** | Significant issues - requires attention |
| 0-49% | ❌ **NON-COMPLIANT** | Major compliance violations - immediate action required |

### Example Output

```
## ✅ Overall Status: COMPLIANT (100%)

**Critical Checks:** 8/8 passed
**Total Checks:** 10/10 passed
**Informational:** 0 warning(s)

████████████████████ 100%

## Validation Results

| Area                        | Status  | Result     | Priority    |
|-----------------------------|---------|------------|-------------|
| 📁 Repository Structure     | ✅ Pass | Compliant  | -           |
| 📚 Documentation Quality    | ✅ Pass | Compliant  | -           |
| 💻 Coding Standards         | ✅ Pass | Compliant  | -           |
| ⚖️ License Compliance       | ✅ Pass | Compliant  | -           |
| 🧹 Git Repository Hygiene   | ✅ Pass | Compliant  | -           |
| ⚙️ Workflow Configuration   | ✅ Pass | Compliant  | -           |
| 🔢 Version Consistency      | ✅ Pass | All versions match | -    |
| 🔐 Script Integrity         | ✅ Pass | SHA hashes validated | -  |
| 🏢 Enterprise Readiness     | ✅ Pass | Ready for enterprise | ℹ️ Info |
| 🏥 Repository Health        | ✅ Pass | Health check passed  | ℹ️ Info |
```

## Usage Examples

### Running Manually

```bash
# Trigger workflow manually via GitHub Actions UI
# Go to: Actions → Standards Compliance → Run workflow

# Or use GitHub CLI
gh workflow run standards-compliance.yml
```

### Local Validation

Run individual validators locally before pushing:

```bash
# Check version consistency
php scripts/validate/check_version_consistency.php --verbose

# Validate script integrity
python3 scripts/maintenance/validate_script_registry.py --priority critical --verbose

# Check enterprise readiness
php scripts/validate/check_enterprise_readiness.php --verbose

# Check repository health
php scripts/validate/check_repo_health.php --verbose

# Lint YAML files
yamllint .github/workflows/*.yml

# Format Python code
black --check scripts/**/*.py

# Check PHP code style
phpcs --standard=PSR12 src/
```

### Fixing Common Issues

#### Version Mismatches

```bash
# 1. Identify current version
grep '"version"' composer.json

# 2. Find mismatches
php scripts/validate/check_version_consistency.php

# 3. Update all references to match
# Use sed or manually update files listed in output
```

#### Script Integrity Violations

```bash
# If changes are legitimate:
python3 scripts/maintenance/generate_script_registry.py --update

# If changes are NOT authorized:
git checkout HEAD -- scripts/
```

#### Coding Standard Violations

```bash
# Auto-fix Python formatting
black scripts/**/*.py

# Auto-fix PHP code style
phpcbf --standard=PSR12 src/

# Fix YAML issues
# Manual fixes required based on yamllint output
```

## Integration with Pull Requests

The workflow automatically:

1. **Runs on every PR** to main, dev/*, or rc/* branches
2. **Posts results** in the PR checks section
3. **Provides detailed summary** in the workflow run
4. **Blocks merge** if critical checks fail
5. **Offers remediation steps** for any violations

### PR Status Checks

| Check Result | PR Status | Merge Allowed |
|--------------|-----------|---------------|
| All critical checks pass | ✅ Success | Yes |
| Any critical check fails | ❌ Failure | No (blocked) |
| Only informational warnings | ✅ Success | Yes |

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              PARALLEL VALIDATION CHECKS                      │
└─────────────────────────────────────────────────────────────┘
     │
     ├─────────────┬──────────────┬──────────────┬────────────┐
     ▼             ▼              ▼              ▼            ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐
│Repository  │File Header  │Code Style│  │  Docs   │  │ License  │
│Structure│  │ Validation│  │  Check   │  │  Check  │  │  Check   │
└─────────┘  └──────────┘  └──────────┘  └─────────┘  └──────────┘
     │             │              │              │            │
     ├─────────────┼──────────────┼──────────────┼────────────┤
     ▼             ▼              ▼              ▼            ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐
│  Git    │  │ Workflow │  │ Version  │  │ Script  │  │Enterprise│
│ Hygiene │  │  Config  │  │Consistency│  │Integrity│  │Readiness │
└─────────┘  └──────────┘  └──────────┘  └─────────┘  └──────────┘
     │             │              │              │            │
     └─────────────┴──────────────┴──────────────┴────────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │  All Checks Pass?│
                           └──────────────────┘
                              │            │
                          YES │            │ NO
                              ▼            ▼
                       ┌──────────┐  ┌──────────────┐
                       │  SUCCESS │  │ CREATE ISSUE │
                       │  Summary │  │ with Failure │
                       └──────────┘  │   Details    │
                                     └──────────────┘
```

## Customization

### Adjusting Severity

To change a critical check to informational (non-blocking):

```yaml
# In the summary job, change from:
[ "$CHECK_STATUS" = "success" ] && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))

# To:
if [ "$CHECK_STATUS" = "success" ]; then
  PASSED=$((PASSED + 1))
else
  WARNINGS=$((WARNINGS + 1))
fi
```

### Adding Custom Checks

Add a new validation job:

```yaml
custom-check:
  name: Custom Validation
  runs-on: ubuntu-latest
  steps:
    - name: Checkout
      uses: actions/checkout@v6
    
    - name: Run Custom Validator
      run: |
        ./scripts/custom-validator.sh
```

Then add it to the summary `needs` array.

### Skipping Checks

To skip a check temporarily, add to job:

```yaml
if: false  # Skip this check
```

Or make conditional:

```yaml
if: ${{ github.event_name != 'pull_request' }}  # Skip on PRs
```

## Troubleshooting

### Workflow Fails Unexpectedly

**Check**:
1. Review workflow run logs in GitHub Actions
2. Look for specific error messages in failed jobs
3. Check if required scripts exist (new checks depend on PHP/Python scripts)

**Common Issues**:
- Missing validator scripts (version/enterprise/health checks)
- PHP/Python not available in runner
- Permissions issues with files

### Version Consistency Always Fails

**Cause**: Multiple version references across repository don't match

**Fix**:
1. Identify canonical version: `grep '"version"' composer.json`
2. Find mismatches: `php scripts/validate/check_version_consistency.php`
3. Update all references to match canonical version

### Script Integrity Violations

**Legitimate Changes**:
```bash
# Update registry after modifying scripts
python3 scripts/maintenance/generate_script_registry.py --update
git add scripts/.script-registry.json
git commit -m "chore: update script registry"
```

**Unauthorized Changes**:
```bash
# Restore original scripts
git checkout HEAD -- scripts/
```

## Related Documentation

- [Workflow Architecture](./workflow-architecture.md)
- [Workflow Inventory](./workflow-inventory.md)
- [Repository Structure Standards](../policy/core-structure.md)
- [Coding Style Guide](../policy/coding-style-guide.md)
- [File Header Standards](../policy/file-header-standards.md)
- [License Compliance Policy](../policy/license-compliance.md)
- [Version Management](../guide/version-badge-guide.md)
- [Script Integrity Guide](../guide/script-integrity-validation.md)

## Changelog

### v04.00.03 (2026-02-21)

**Added**:
- ✨ Version Consistency Check - Validates all version numbers match
- ✨ Script Integrity Validation - Verifies SHA-256 hashes
- ✨ Enterprise Readiness Check - Assesses enterprise patterns (informational)
- ✨ Repository Health Check - Evaluates overall quality (informational)

**Changed**:
- 📊 Enhanced compliance scoring with critical vs informational distinction
- 📊 Improved summary reporting with detailed breakdowns
- 📊 Total validation checks increased from 6 to 10

**Fixed**:
- 🐛 Compliance percentage now correctly calculates based on critical checks only

### v04.00.03 (2026-01-07)

**Added**:
- Initial comprehensive standards compliance workflow
- Repository structure validation
- Documentation quality checks
- Coding standards enforcement
- License compliance validation
- Git hygiene checks
- Workflow configuration validation

---

**Maintained by**: MokoStandards Team  
**Last Review**: 2026-02-21  
**Next Review**: 2026-03-21
