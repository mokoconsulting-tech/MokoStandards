# MokoStandards Enforcement Levels Guide

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Document Metadata

| Field | Value |
|-------|-------|
| **VERSION** | 04.00.03 |
| **LAST UPDATED** | 2026-02-21 |
| **STATUS** | Active |
| **APPLIES TO** | All MokoStandards repositories and bulk sync operations |
| **DOCUMENT TYPE** | Policy & Reference Guide |

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Overview](#overview)
3. [The Six Enforcement Levels](#the-six-enforcement-levels)
4. [Enforcement Priority Order](#enforcement-priority-order)
5. [Comparison Matrix](#comparison-matrix)
6. [Decision Tree](#decision-tree)
7. [Practical Examples](#practical-examples)
8. [Best Practices](#best-practices)
9. [Implementation Details](#implementation-details)
10. [Troubleshooting](#troubleshooting)
11. [Related Documentation](#related-documentation)

---

## Quick Reference

### Badge Legend

| Level | Badge | Name | Behavior | Can Override? |
|-------|-------|------|----------|---------------|
| 1 | ![Level 1](https://img.shields.io/badge/Level_1-OPTIONAL-blue?style=flat-square) | OPTIONAL | Opt-in only | ✅ Yes |
| 2 | ![Level 2](https://img.shields.io/badge/Level_2-SUGGESTED-yellow?style=flat-square) | SUGGESTED | Default, warnings if excluded | ✅ Yes |
| 3 | ![Level 3](https://img.shields.io/badge/Level_3-REQUIRED-orange?style=flat-square) | REQUIRED | Mandatory, errors if excluded | ❌ No |
| 4 | ![Level 4](https://img.shields.io/badge/Level_4-FORCED-red?style=flat-square) | FORCED | Always synced (critical) | ❌ No |
| 5 | ![Level 5](https://img.shields.io/badge/Level_5-NOT__SUGGESTED-yellow?style=flat-square) | NOT_SUGGESTED | Discouraged, warnings if present | ✅ Yes (with warning) |
| 6 | ![Level 6](https://img.shields.io/badge/Level_6-NOT__ALLOWED-critical?style=flat-square) | NOT_ALLOWED | Prohibited, errors if present | ❌ **NEVER** |

### Processing Order

```
1. Level 6: NOT_ALLOWED     ← Checked FIRST (absolute priority)
2. Level 4: FORCED           ← Critical compliance
3. Level 3: REQUIRED         ← Mandatory files
4. Level 2: SUGGESTED        ← Recommended files
5. Level 5: NOT_SUGGESTED    ← Discouraged files
6. Level 1: OPTIONAL         ← Opt-in files
```

### One-Minute Summary

- **OPTIONAL**: Must explicitly opt-in to include
- **SUGGESTED**: Recommended, can be excluded with warnings
- **REQUIRED**: Mandatory for all repositories
- **FORCED**: Critical files, always synced, cannot override
- **NOT_SUGGESTED**: Discouraged, warns if present, can override
- **NOT_ALLOWED**: Absolutely prohibited, checked first, cannot override

---

## Overview

### Purpose

The MokoStandards enforcement level system provides graduated control over file synchronization across repositories. It balances:

- **Organizational Standards**: Ensuring consistency and compliance
- **Repository Autonomy**: Allowing repository-specific needs
- **Security Requirements**: Preventing prohibited content
- **Best Practices**: Encouraging recommended patterns

### Why Six Levels?

Each level serves a specific purpose:

1. **OPTIONAL**: Flexibility for special cases
2. **SUGGESTED**: Guidance without mandates
3. **REQUIRED**: Core organizational requirements
4. **FORCED**: Critical security/compliance files
5. **NOT_SUGGESTED**: Deprecation and discouragement
6. **NOT_ALLOWED**: Absolute security boundaries

### System Goals

✅ **Clear Communication**: What's required vs optional vs prohibited
✅ **Graduated Control**: From permissive to restrictive
✅ **Security**: Prevent dangerous files absolutely
✅ **Flexibility**: Allow justified deviations where appropriate
✅ **Auditability**: Complete logging of all decisions

---

## The Six Enforcement Levels

### ![Level 1 - OPTIONAL](https://img.shields.io/badge/Level_1-OPTIONAL-blue?style=flat-square) Level 1: OPTIONAL

#### Definition

Files that **MAY** be included if repository explicitly opts in.

#### Characteristics

- ⭕ Not synced by default
- ⭕ No warnings if excluded
- ✅ Can opt-in per repository
- ✅ No compliance impact
- 💙 Color: Blue (informational)

#### When to Use

Use OPTIONAL for:
- Environment-specific features (staging, production variants)
- Experimental workflows
- Optional tooling
- Advanced features not needed by all repositories
- Repository-type-specific configurations

#### When NOT to Use

Avoid OPTIONAL for:
- Core security requirements
- Organization-wide mandates
- Files needed for basic functionality
- Compliance-required items

#### Configuration Example

```terraform
enforcement_levels = {
  optional_files = [
    {
      path    = ".github/workflows/deploy-to-staging.yml"
      reason  = "Only repositories with staging environment"
      include = true  # Explicit opt-in required
    },
    {
      path    = ".github/workflows/performance-testing.yml"
      reason  = "Optional performance testing"
      include = false  # Not included by default
    },
    {
      path    = "docker-compose.dev.yml"
      reason  = "Local development docker setup"
      include = true
    }
  ]
}
```

#### Sync Behavior

```bash
# Included file (opted in)
✅ SYNC: deploy-to-staging.yml (OPTIONAL - Level 1 - explicitly included)

# Excluded file (not opted in)
⭕ SKIP: performance-testing.yml (OPTIONAL - Level 1 - not included)
```

#### Real-World Examples

**Example 1: Deployment Workflows**
```terraform
{
  path    = ".github/workflows/deploy-production.yml"
  reason  = "Only for repositories that deploy to production"
  include = true  # This repo deploys to production
}
```

**Example 2: Development Tools**
```terraform
{
  path    = ".devcontainer/devcontainer.json"
  reason  = "VS Code dev container configuration"
  include = false  # Team doesn't use dev containers
}
```

#### Override Behavior

- ✅ Can be included or excluded freely
- ✅ No warnings or errors
- ✅ Repository has complete control
- ✅ Can change at any time

---

### ![Level 2 - SUGGESTED](https://img.shields.io/badge/Level_2-SUGGESTED-yellow?style=flat-square) Level 2: SUGGESTED

#### Definition

Files that **SHOULD** be synced (recommended best practices).

#### Characteristics

- ✅ Synced by default
- ⚠️ Warnings if excluded
- ✅ Can be overridden with justification
- ⚠️ May impact compliance scoring
- 💛 Color: Yellow (warning/caution)

#### When to Use

Use SUGGESTED for:
- Best practice configurations
- Recommended workflows
- Standard tooling
- Non-critical but beneficial files
- Quality improvement tools

#### When NOT to Use

Avoid SUGGESTED for:
- Mandatory requirements (use REQUIRED)
- Critical security files (use FORCED)
- Optional features (use OPTIONAL)
- Prohibited content (use NOT_ALLOWED)

#### Configuration Example

```terraform
enforcement_levels = {
  suggested_files = [
    {
      path   = ".editorconfig"
      reason = "Consistent code formatting across editors"
    },
    {
      path   = ".github/workflows/dependency-review.yml"
      reason = "Security best practice for dependency scanning"
    },
    {
      path   = ".github/CODEOWNERS"
      reason = "Recommended for code review automation"
    }
  ]
}
```

#### Sync Behavior

```bash
# Default: Suggested files are synced
✅ SYNC: .editorconfig (SUGGESTED - Level 2 - recommended)

# If excluded in config.tf
⚠️ WARNING: .editorconfig excluded but SUGGESTED (not recommended)
⭕ SKIP: .editorconfig (SUGGESTED but excluded in config.tf)
```

#### Real-World Examples

**Example 1: Code Quality**
```terraform
{
  path   = ".github/workflows/linting.yml"
  reason = "Code quality checks recommended for all projects"
}
```

**Example 2: Documentation**
```terraform
{
  path   = "docs/CONTRIBUTING.md"
  reason = "Contributing guidelines recommended for open source"
}
```

#### Override Behavior

- ✅ Can be excluded via `exclude_files`
- ⚠️ Generates warning when excluded
- ✅ Can be protected via `protected_files`
- ⚠️ Logged in audit trail
- 📊 May affect compliance score

#### Excluding a SUGGESTED File

```terraform
# In repository's .github/config.tf
exclude_files = [
  {
    path   = ".editorconfig"
    reason = "Team uses different formatting standard"
  }
]
```

**Result**: File excluded, warning generated, logged in sync log.

---

### ![Level 3 - REQUIRED](https://img.shields.io/badge/Level_3-REQUIRED-orange?style=flat-square) Level 3: REQUIRED

#### Definition

Files that **MUST** be synced (mandatory for all repositories).

#### Characteristics

- ✅ Always synced
- ❌ Cannot be excluded
- ❌ Cannot be protected
- ❌ Errors if attempted to override
- 🧡 Color: Orange (important/mandatory)

#### When to Use

Use REQUIRED for:
- Core organizational policies
- Legal requirements (LICENSE, NOTICE)
- Mandatory workflows (CI, compliance checks)
- Essential documentation
- Organization-wide standards

#### When NOT to Use

Avoid REQUIRED for:
- Optional features (use OPTIONAL or SUGGESTED)
- Best practices that can vary (use SUGGESTED)
- Critical security files (use FORCED for highest priority)
- Deprecated files (use NOT_SUGGESTED)

#### Configuration Example

```terraform
enforcement_levels = {
  required_files = [
    {
      path   = "LICENSE"
      reason = "GPL-3.0-or-later license required for all repositories"
    },
    {
      path   = ".github/workflows/ci.yml"
      reason = "Continuous integration mandatory for all projects"
    },
    {
      path   = "CONTRIBUTING.md"
      reason = "Contributing guidelines mandatory"
    },
    {
      path   = "CODE_OF_CONDUCT.md"
      reason = "Code of conduct mandatory for all repositories"
    }
  ]
}
```

#### Sync Behavior

```bash
# Always synced
✅ SYNC: LICENSE (REQUIRED - Level 3 - mandatory file - must be synced)

# If attempted to exclude
❌ ERROR: LICENSE is REQUIRED (Level 3) - cannot be excluded
⚠️ WARNING: Required file exclusion violates compliance
✅ SYNC: LICENSE (REQUIRED - Level 3 - mandatory despite exclusion attempt)
```

#### Real-World Examples

**Example 1: Legal Compliance**
```terraform
{
  path   = "LICENSE"
  reason = "Legal requirement - all code must be licensed"
}
```

**Example 2: Security Standards**
```terraform
{
  path   = ".github/workflows/security-scan.yml"
  reason = "Security scanning mandatory for all repositories"
}
```

**Example 3: Documentation Standards**
```terraform
{
  path   = "README.md"
  reason = "README required for all repositories"
}
```

#### Override Behavior

- ❌ **CANNOT** be excluded via `exclude_files`
- ❌ **CANNOT** be protected via `protected_files`
- ❌ Attempts to override generate errors
- ✅ Always synced regardless of configuration
- 📊 Critical for compliance scoring

#### Attempting to Override (FAILS)

```terraform
# In repository's .github/config.tf
exclude_files = [
  {
    path   = "LICENSE"
    reason = "Want to use different license"  # ❌ THIS WILL NOT WORK
  }
]

protected_files = [
  {
    path   = "LICENSE"
    reason = "Customized license text"  # ❌ THIS WILL NOT WORK
  }
]
```

**Result**: 
- ❌ Errors generated
- ✅ File synced anyway
- ⚠️ Compliance violation logged
- 📧 Notification sent to maintainers

---

### ![Level 4 - FORCED](https://img.shields.io/badge/Level_4-FORCED-red?style=flat-square) Level 4: FORCED

#### Definition

Files that are **ALWAYS** synced (critical compliance and security).

#### Characteristics

- ✅ Always synced, highest priority (after NOT_ALLOWED)
- ❌ Cannot be excluded
- ❌ Cannot be protected
- ❌ Overrides ALL configuration settings
- 🔴 Color: Red (critical)
- 🔒 6 predefined critical files

#### When to Use

Use FORCED for:
- Critical security files
- Core compliance workflows
- Essential validation scripts
- Files that MUST stay current for security
- Organization-wide enforcement mechanisms

#### When NOT to Use

Avoid FORCED for:
- Normal organizational requirements (use REQUIRED)
- Best practices (use SUGGESTED)
- Optional features (use OPTIONAL)
- Most files (overuse weakens the system)

#### The 6 FORCED Files

These files are hardcoded in the system:

1. `.github/workflows/standards-compliance.yml` - Core compliance checking
2. `scripts/validate/check_version_consistency.php` - Version validation
3. `scripts/validate/check_enterprise_readiness.php` - Enterprise standards
4. `scripts/validate/check_repo_health.php` - Repository health
5. `scripts/maintenance/validate_script_registry.py` - Script integrity
6. `scripts/.script-registry.json` - Script registry database

#### Why These 6 Files?

**Security**: These files enforce security and compliance across all repositories.
**Currency**: They must always be up-to-date with latest security checks.
**Integrity**: They validate other files and must be trustworthy.
**Non-Negotiable**: Organization security depends on these being current.

#### Configuration Example

```terraform
# FORCED files are hardcoded, not configured
# They are defined in bulk_update_repos.php:

private const ALWAYS_FORCE_OVERRIDE_FILES = [
    '.github/workflows/standards-compliance.yml',
    'scripts/validate/check_version_consistency.php',
    'scripts/validate/check_enterprise_readiness.php',
    'scripts/validate/check_repo_health.php',
    'scripts/maintenance/validate_script_registry.py',
    'scripts/.script-registry.json',
];
```

#### Sync Behavior

```bash
# Always synced, checked after NOT_ALLOWED
✅ SYNC: standards-compliance.yml (FORCED - Level 4 - critical compliance file)

# Even if protected in config.tf
⚠️ WARNING: standards-compliance.yml is protected in config.tf but FORCE_OVERRIDE takes precedence
✅ SYNC: standards-compliance.yml (FORCED - Level 4 - critical compliance - always updated)
```

#### Real-World Scenario

```terraform
# Repository tries to protect a FORCED file
# In .github/config.tf:

protected_files = [
  {
    path   = ".github/workflows/standards-compliance.yml"
    reason = "Customized compliance checks"  # ❌ WILL BE OVERRIDDEN
  }
]
```

**What Happens**:
1. ⚠️ WARNING logged: "Protected file is FORCED - will be overridden"
2. ✅ File is synced anyway (FORCED priority)
3. 📝 Logged in sync audit trail
4. 🔔 Team notified of force-override
5. 🔒 Repository stays compliant

#### Override Behavior

- ❌ **CANNOT** be excluded
- ❌ **CANNOT** be protected
- ❌ Attempts to override generate warnings
- ✅ **ALWAYS** synced (absolute requirement)
- 🔐 Critical for organizational security

#### Why FORCED Can't Be Overridden

**Security**: These files contain security checks. Allowing overrides creates vulnerabilities.
**Compliance**: Organization-wide compliance depends on uniform enforcement.
**Trust**: These files validate other files. They must be trustworthy.
**Currency**: Security threats evolve. These files must stay current.

---

### ![Level 5 - NOT SUGGESTED](https://img.shields.io/badge/Level_5-NOT__SUGGESTED-yellow?style=flat-square) Level 5: NOT_SUGGESTED

#### Definition

Files that are **DISCOURAGED** but not prohibited.

#### Characteristics

- ⚠️ Warns if present in repository
- ✅ Can be overridden with justification
- ⚠️ Generates warnings, not errors
- 💛 Color: Yellow (caution/warning)
- 🗑️ Recommended for removal

#### When to Use

Use NOT_SUGGESTED for:
- Deprecated configurations
- Legacy tools being phased out
- Superseded files
- Non-recommended practices
- Files that should be migrated away from

#### When NOT to Use

Avoid NOT_SUGGESTED for:
- Prohibited content (use NOT_ALLOWED)
- Acceptable alternatives (use OPTIONAL)
- Still-recommended practices (use SUGGESTED)

#### Configuration Example

```terraform
enforcement_levels = {
  not_suggested_files = [
    {
      path   = ".travis.yml"
      reason = "Travis CI deprecated - migrate to GitHub Actions"
    },
    {
      path   = "circle.yml"
      reason = "CircleCI deprecated - migrate to GitHub Actions"
    },
    {
      path   = "Jenkinsfile"
      reason = "Jenkins not recommended - use GitHub Actions"
    },
    {
      path   = "legacy_config.ini"
      reason = "Superseded by modern YAML configuration"
    }
  ]
}
```

#### Sync Behavior

```bash
# If file is present in repository
⚠️ WARNING: .travis.yml found - NOT_SUGGESTED (Level 5 - discouraged)
⚠️ RECOMMENDATION: Remove .travis.yml and migrate to GitHub Actions
⭕ SKIP: .travis.yml (NOT_SUGGESTED - discouraged file)

# If file is protected
⚠️ WARNING: .travis.yml is NOT_SUGGESTED but protected in config.tf
✅ ALLOWED: Protected override, but not recommended
⭕ SKIP: .travis.yml (NOT_SUGGESTED but protected)
```

#### Real-World Examples

**Example 1: Deprecated CI Systems**
```terraform
{
  path   = ".travis.yml"
  reason = "Travis CI deprecated in 2024 - migrate to GitHub Actions"
}
```

**Example 2: Legacy Configuration**
```terraform
{
  path   = "config.xml"
  reason = "XML configuration superseded by YAML in v04.00.00"
}
```

**Example 3: Old Dependencies**
```terraform
{
  path   = "bower.json"
  reason = "Bower deprecated - migrate to npm/yarn"
}
```

#### Override Behavior

- ✅ Can be protected via `protected_files`
- ⚠️ Generates warning when protected
- ✅ Allowed with strong justification
- 📝 Logged in audit trail
- 📊 May impact repository health score

#### Protecting a NOT_SUGGESTED File

```terraform
# In repository's .github/config.tf
protected_files = [
  {
    path   = ".travis.yml"
    reason = "Still used for legacy integration testing - migration planned Q2 2026"
  }
]
```

**Result**:
- ⚠️ Warning generated
- ✅ File allowed (protected)
- 📝 Justification logged
- 📅 Recommendation to migrate

#### Migration Path

1. **Identify**: NOT_SUGGESTED files detected
2. **Plan**: Create migration strategy
3. **Execute**: Migrate to recommended alternative
4. **Remove**: Delete NOT_SUGGESTED file
5. **Verify**: Confirm replacement works

---

### ![Level 6 - NOT ALLOWED](https://img.shields.io/badge/Level_6-NOT__ALLOWED-critical?style=flat-square) Level 6: NOT_ALLOWED

#### Definition

Files that are **ABSOLUTELY PROHIBITED** (highest priority enforcement).

#### Characteristics

- ❌ Errors if present
- ❌ **CANNOT** be overridden (EVER)
- ❌ Checked **FIRST** (before all other levels)
- ❌ Blocks merge if detected
- 🔴 Color: Critical Red (danger/prohibited)
- 🚨 Security-critical enforcement

#### When to Use

Use NOT_ALLOWED for:
- Files containing secrets
- Credential files
- Private keys
- Proprietary code
- Legally prohibited content
- Security vulnerabilities
- Compliance violations

#### When NOT to Use

Avoid NOT_ALLOWED for:
- Discouraged but acceptable files (use NOT_SUGGESTED)
- Configurable requirements (use REQUIRED)
- Optional items (use OPTIONAL)
- Non-security issues

#### Configuration Example

```terraform
enforcement_levels = {
  not_allowed_files = [
    {
      path   = ".env"
      reason = "Contains secrets - NEVER commit to repository"
    },
    {
      path   = ".env.local"
      reason = "Contains secrets - NEVER commit to repository"
    },
    {
      path   = "secrets.json"
      reason = "Contains secrets - NEVER commit to repository"
    },
    {
      path   = "credentials.json"
      reason = "Contains credentials - NEVER commit to repository"
    },
    {
      path   = "private_key.pem"
      reason = "Private key - NEVER commit to repository"
    },
    {
      path   = "id_rsa"
      reason = "SSH private key - NEVER commit to repository"
    },
    {
      path   = "*.p12"
      reason = "Certificate private key - NEVER commit"
    },
    {
      path   = "*.pfx"
      reason = "Certificate private key - NEVER commit"
    }
  ]
}
```

#### Sync Behavior

```bash
# If file is detected (checked FIRST, before anything else)
❌ ERROR: .env file detected - NOT_ALLOWED (Level 6 - prohibited file)
❌ SECURITY: File contains secrets - NEVER commit to repository
❌ BLOCK: Merge blocked until file is removed
🚨 CRITICAL: Immediate action required

# Even if protected (IGNORED)
❌ ERROR: .env is NOT_ALLOWED (Level 6) - cannot be overridden
⚠️ WARNING: protected_files setting IGNORED for NOT_ALLOWED files
❌ BLOCK: File must be removed immediately
```

#### Real-World Examples

**Example 1: Environment Files**
```terraform
{
  path   = ".env"
  reason = "Environment files contain API keys, passwords, tokens"
}
```

**Example 2: Private Keys**
```terraform
{
  path   = "*.pem"
  reason = "PEM files contain private keys - never commit"
}
```

**Example 3: Credentials**
```terraform
{
  path   = "aws-credentials.json"
  reason = "AWS credentials - security risk"
}
```

#### Override Behavior

- ❌ **CANNOT** be protected via `protected_files` (IGNORED)
- ❌ **CANNOT** be excluded (doesn't apply)
- ❌ **ABSOLUTE PRIORITY** - checked first
- ❌ Blocks merge/deployment
- 🚨 Immediate security alert
- 📧 Security team notified

#### Attempting to Override (COMPLETELY FAILS)

```terraform
# In repository's .github/config.tf
protected_files = [
  {
    path   = ".env"
    reason = "Need environment variables"  # ❌ COMPLETELY IGNORED
  }
]
```

**What Happens**:
1. ❌ ERROR: NOT_ALLOWED file detected
2. ❌ protected_files setting COMPLETELY IGNORED
3. ❌ Merge blocked
4. 🚨 Security alert triggered
5. 📧 Security team notified
6. ⛔ Repository flagged as non-compliant
7. 🔒 CI/CD pipeline blocked

#### Why NOT_ALLOWED Has Absolute Priority

**Security First**: Checked BEFORE any other level to prevent security leaks.

**Code Implementation**: In `shouldSkipFile()` method:

```php
// Level 6: NOT_ALLOWED - HIGHEST PRIORITY - Absolutely prohibited
// This check happens FIRST to ensure no override can allow prohibited files
if ($enforcementLevel === self::ENFORCEMENT_LEVELS['NOT_ALLOWED']) {
    // Override configurations (protected_files, exclude_files) are IGNORED
    return [
        'skip' => true,
        'reason' => "NOT_ALLOWED (Level 6 - prohibited file - CANNOT BE OVERRIDDEN)",
        'level' => 'NOT_ALLOWED',
        'enforcement' => 6,
        'error' => true,  // Mark as error for compliance reporting
    ];
}
```

**No Exceptions**: Security cannot be compromised. No overrides allowed.

**Compliance**: Legal and regulatory requirements demand absolute enforcement.

#### Common NOT_ALLOWED Patterns

**Secrets**:
- `.env`, `.env.*`
- `secrets.json`, `credentials.json`
- `config.prod.json` (if contains secrets)

**Keys**:
- `*.pem`, `*.key`, `*.crt` (private keys)
- `id_rsa`, `id_dsa`, `id_ecdsa`
- `*.p12`, `*.pfx`

**Credentials**:
- `aws-credentials.json`
- `gcp-service-account.json`
- `database-password.txt`

**Proprietary**:
- `proprietary-code.js`
- `licensed-library.jar`
- `copyrighted-asset.svg`

---

## Enforcement Priority Order

### Processing Sequence

Files are evaluated in this order:

```
┌─────────────────────────────────────────┐
│ 1. Level 6: NOT_ALLOWED                 │  ← FIRST (absolute priority)
│    ❌ Prohibited, errors, blocks merge  │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. Level 4: FORCED                      │  ← Critical compliance
│    🔒 Always synced, cannot override    │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. Level 3: REQUIRED                    │  ← Mandatory
│    ⛔ Must be synced, errors if not     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 4. Level 2: SUGGESTED                   │  ← Recommended
│    ⚠️ Warnings if excluded              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5. Level 5: NOT_SUGGESTED               │  ← Discouraged
│    ⚠️ Warnings if present               │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 6. Level 1: OPTIONAL                    │  ← Opt-in
│    ⭕ Only if explicitly included       │
└─────────────────────────────────────────┘
```

### Why This Order?

1. **NOT_ALLOWED First**: Security violations must be caught immediately, before anything else.

2. **FORCED Second**: Critical files must always sync, even if others are skipped.

3. **REQUIRED Third**: Mandatory files, but checked after critical security.

4. **SUGGESTED Fourth**: Recommendations, evaluated after requirements.

5. **NOT_SUGGESTED Fifth**: Discouraged files, checked after positive enforcement.

6. **OPTIONAL Last**: Opt-in features, lowest priority.

### Priority Examples

**Example 1**: File is both REQUIRED and NOT_ALLOWED
```
Result: NOT_ALLOWED wins (checked first)
Action: Error, block merge
Reason: Security always takes precedence
```

**Example 2**: File is both FORCED and protected
```
Result: FORCED wins (override ignored)
Action: File synced
Reason: Critical compliance cannot be blocked
```

**Example 3**: File is both SUGGESTED and excluded
```
Result: Exclusion honored with warning
Action: File not synced, warning generated
Reason: SUGGESTED can be overridden
```

---

## Comparison Matrix

### Comprehensive Comparison Table

| Feature | OPTIONAL | SUGGESTED | REQUIRED | FORCED | NOT_SUGGESTED | NOT_ALLOWED |
|---------|----------|-----------|----------|--------|---------------|-------------|
| **Level** | 1 | 2 | 3 | 4 | 5 | 6 |
| **Badge** | ![](https://img.shields.io/badge/Level_1-OPTIONAL-blue?style=flat-square) | ![](https://img.shields.io/badge/Level_2-SUGGESTED-yellow?style=flat-square) | ![](https://img.shields.io/badge/Level_3-REQUIRED-orange?style=flat-square) | ![](https://img.shields.io/badge/Level_4-FORCED-red?style=flat-square) | ![](https://img.shields.io/badge/Level_5-NOT__SUGGESTED-yellow?style=flat-square) | ![](https://img.shields.io/badge/Level_6-NOT__ALLOWED-critical?style=flat-square) |
| **Synced by default** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | N/A | N/A |
| **Can exclude** | ✅ Yes | ✅ Yes (warns) | ❌ No | ❌ No | N/A | N/A |
| **Can protect** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes (warns) | ❌ **NEVER** |
| **Override allowed** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ **NEVER** |
| **Generates warnings** | ❌ No | ⚠️ If excluded | ❌ No | ⚠️ If protected | ⚠️ If present | ❌ No (errors) |
| **Generates errors** | ❌ No | ❌ No | ⚠️ If excluded | ❌ No | ❌ No | ✅ Yes (always) |
| **Blocks merge** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Compliance impact** | None | Warning | Error | Critical | Warning | Critical Error |
| **Processing priority** | 6 (last) | 4 | 3 | 2 | 5 | 1 (first) |
| **Typical use** | Features | Best practices | Mandates | Security | Deprecated | Prohibited |
| **Examples** | Staging deploy | .editorconfig | LICENSE | compliance.yml | .travis.yml | .env |

### Behavior Matrix

| Scenario | OPTIONAL | SUGGESTED | REQUIRED | FORCED | NOT_SUGGESTED | NOT_ALLOWED |
|----------|----------|-----------|----------|--------|---------------|-------------|
| **File present, not configured** | ⭕ Skip | ✅ Sync | ✅ Sync | ✅ Sync | ⚠️ Warn + Skip | ❌ Error + Block |
| **File present, excluded in config** | ⭕ Skip | ⚠️ Warn + Skip | ❌ Error + Sync | ✅ Sync anyway | ⚠️ Warn + Skip | ❌ Error + Block |
| **File present, protected in config** | ⭕ Skip | ⭕ Skip | ❌ Error + Sync | ⚠️ Warn + Sync | ⚠️ Warn + Skip | ❌ Error + Block |
| **File missing, include=true** | ✅ Sync | ✅ Sync | ✅ Sync | ✅ Sync | N/A | N/A |
| **File missing, include=false** | ⭕ Skip | ⚠️ Warn + Skip | ❌ Error + Sync | ✅ Sync anyway | N/A | N/A |

---

## Decision Tree

### How to Choose the Right Level

```
START: Need to classify a file
     ↓
┌────┴────┐
│ Is this │
│ file    │
│ security│
│ risk?   │
└────┬────┘
     │
     ├─ YES ─→ Is it absolutely prohibited?
     │         ├─ YES → Level 6: NOT_ALLOWED ❌
     │         └─ NO  → Is it critical for compliance?
     │                  ├─ YES → Level 4: FORCED 🔒
     │                  └─ NO  → Level 3: REQUIRED ⛔
     │
     └─ NO ──→ Is it being phased out?
               ├─ YES → Level 5: NOT_SUGGESTED ⚠️🚫
               └─ NO  → Is it mandatory for all repos?
                        ├─ YES → Level 3: REQUIRED ⛔
                        └─ NO  → Is it recommended?
                                 ├─ YES → Level 2: SUGGESTED ⚠️
                                 └─ NO  → Level 1: OPTIONAL ⭕
```

### Quick Decision Guide

**Start with these questions:**

1. **Would this file create a security risk if present?**
   - Yes → NOT_ALLOWED (Level 6)

2. **Is this file critical for organizational compliance?**
   - Yes → FORCED (Level 4)

3. **Is this file required by policy for all repositories?**
   - Yes → REQUIRED (Level 3)

4. **Is this file a deprecated/legacy item to be phased out?**
   - Yes → NOT_SUGGESTED (Level 5)

5. **Is this file a recommended best practice?**
   - Yes → SUGGESTED (Level 2)

6. **Is this file optional, needed only for specific use cases?**
   - Yes → OPTIONAL (Level 1)

### Common Scenarios

**Scenario 1: LICENSE file**
- Question: Required by policy?
- Answer: Yes
- **Level**: REQUIRED (3) ⛔

**Scenario 2: .env file**
- Question: Security risk?
- Answer: Yes (contains secrets)
- **Level**: NOT_ALLOWED (6) ❌

**Scenario 3: standards-compliance.yml**
- Question: Critical for compliance?
- Answer: Yes (must always be current)
- **Level**: FORCED (4) 🔒

**Scenario 4: .editorconfig**
- Question: Recommended best practice?
- Answer: Yes (but can be customized)
- **Level**: SUGGESTED (2) ⚠️

**Scenario 5: deploy-to-staging.yml**
- Question: Optional, specific use case?
- Answer: Yes (only repos with staging)
- **Level**: OPTIONAL (1) ⭕

**Scenario 6: .travis.yml**
- Question: Deprecated/legacy?
- Answer: Yes (superseded by GitHub Actions)
- **Level**: NOT_SUGGESTED (5) ⚠️🚫

---

## Practical Examples

### Example 1: Web Application Project

#### Scenario
A web application with:
- Frontend (React)
- Backend (Node.js)
- Database (PostgreSQL)
- Deployment to staging and production
- Using GitHub Actions for CI/CD

#### Classification

```terraform
enforcement_levels = {
  # Files that must opt-in
  optional_files = [
    {
      path    = ".github/workflows/deploy-to-staging.yml"
      include = true  # This project has staging
      reason  = "Staging environment deployment"
    },
    {
      path    = "docker-compose.dev.yml"
      include = true  # Developers use Docker
      reason  = "Local development environment"
    }
  ]
  
  # Recommended files
  suggested_files = [
    {
      path   = ".github/workflows/dependency-review.yml"
      reason = "Security best practice"
    },
    {
      path   = ".editorconfig"
      reason = "Code formatting consistency"
    },
    {
      path   = ".github/CODEOWNERS"
      reason = "Code review automation"
    }
  ]
  
  # Mandatory files
  required_files = [
    {
      path   = "LICENSE"
      reason = "GPL-3.0-or-later required"
    },
    {
      path   = ".github/workflows/ci.yml"
      reason = "CI mandatory for all projects"
    },
    {
      path   = "README.md"
      reason = "Documentation required"
    }
  ]
  
  # Deprecated files to phase out
  not_suggested_files = [
    {
      path   = ".travis.yml"
      reason = "Migrated to GitHub Actions"
    }
  ]
  
  # Prohibited files
  not_allowed_files = [
    {
      path   = ".env"
      reason = "Contains database credentials"
    },
    {
      path   = "database-config.json"
      reason = "Contains connection strings"
    }
  ]
}

# FORCED files (6) are automatic, not configured here
```

#### Sync Results

```bash
Processing repository: mycompany/web-application

✅ SYNC: deploy-to-staging.yml (OPTIONAL - Level 1 - opted in)
✅ SYNC: docker-compose.dev.yml (OPTIONAL - Level 1 - opted in)
✅ SYNC: dependency-review.yml (SUGGESTED - Level 2)
✅ SYNC: .editorconfig (SUGGESTED - Level 2)
✅ SYNC: LICENSE (REQUIRED - Level 3)
✅ SYNC: ci.yml (REQUIRED - Level 3)
✅ SYNC: standards-compliance.yml (FORCED - Level 4)
⚠️ WARNING: .travis.yml found (NOT_SUGGESTED - Level 5)
❌ ERROR: .env found (NOT_ALLOWED - Level 6)

Summary:
- Files synced: 7
- Warnings: 1 (NOT_SUGGESTED file)
- Errors: 1 (NOT_ALLOWED file)
- Action required: Remove .env file immediately
```

---

### Example 2: API Service Project

#### Scenario
A microservice API with:
- RESTful API (Go)
- No frontend
- No staging environment (deploy straight to production)
- Kubernetes deployment
- Using GitHub Actions

#### Classification

```terraform
enforcement_levels = {
  optional_files = [
    {
      path    = ".github/workflows/deploy-to-staging.yml"
      include = false  # No staging environment
      reason  = "Project deploys directly to production"
    },
    {
      path    = ".github/workflows/frontend-tests.yml"
      include = false  # No frontend
      reason  = "Backend-only service"
    },
    {
      path    = "Dockerfile.dev"
      include = true  # Developers use Docker
      reason  = "Local development container"
    }
  ]
  
  suggested_files = [
    {
      path   = ".github/workflows/go-lint.yml"
      reason = "Go code quality checks"
    }
  ]
  
  required_files = [
    {
      path   = "go.mod"
      reason = "Go module definition required"
    },
    {
      path   = "LICENSE"
      reason = "All services must be licensed"
    }
  ]
  
  not_allowed_files = [
    {
      path   = "kubernetes/secrets.yaml"
      reason = "Kubernetes secrets - use sealed secrets"
    },
    {
      path   = "api-keys.json"
      reason = "API keys - use environment variables"
    }
  ]
}
```

---

### Example 3: Library Project

#### Scenario
A reusable library with:
- Pure library (no deployment)
- Published to package registry
- Used by other projects
- High code quality standards

#### Classification

```terraform
enforcement_levels = {
  optional_files = [
    {
      path    = ".github/workflows/deploy-*"
      include = false  # No deployment for library
      reason  = "Library is published, not deployed"
    },
    {
      path    = ".github/workflows/publish-package.yml"
      include = true  # Publish to npm/PyPI
      reason  = "Package publishing workflow"
    }
  ]
  
  suggested_files = [
    {
      path   = ".github/workflows/code-coverage.yml"
      reason = "High test coverage important for libraries"
    },
    {
      path   = "docs/API.md"
      reason = "API documentation critical for library users"
    }
  ]
  
  required_files = [
    {
      path   = "LICENSE"
      reason = "License critical for library distribution"
    },
    {
      path   = "README.md"
      reason = "Usage instructions required"
    },
    {
      path   = "CHANGELOG.md"
      reason = "Version history required for library"
    }
  ]
  
  not_suggested_files = [
    {
      path   = "docker-compose.yml"
      reason = "Not applicable for libraries"
    }
  ]
}
```

---

## Best Practices

### Classification Guidelines

#### DO

✅ **Start Conservative**: Begin with SUGGESTED, move to REQUIRED only if necessary
✅ **Document Reasons**: Always provide clear `reason` fields
✅ **Review Regularly**: Re-evaluate classifications quarterly
✅ **Consider Impact**: Think about all repository types
✅ **Use NOT_ALLOWED Sparingly**: Only for genuine security risks
✅ **Provide Migration Paths**: For NOT_SUGGESTED files

#### DON'T

❌ **Overuse FORCED**: Reserve for truly critical files
❌ **Skip Justifications**: Always document why
❌ **Make Everything REQUIRED**: Reduces flexibility
❌ **Ignore Warnings**: Warnings indicate potential issues
❌ **Allow NOT_ALLOWED Overrides**: Never compromise security

### Common Patterns

#### Security Files

```terraform
# Always NOT_ALLOWED
not_allowed_files = [
  { path = ".env", reason = "Environment secrets" },
  { path = "*.pem", reason = "Private keys" },
  { path = "credentials.*", reason = "Credentials" }
]
```

#### License Files

```terraform
# Always REQUIRED
required_files = [
  { path = "LICENSE", reason = "Legal requirement" },
  { path = "NOTICE", reason = "Attribution requirement" }
]
```

#### CI/CD Workflows

```terraform
# Deployment: OPTIONAL (environment-specific)
optional_files = [
  { 
    path = ".github/workflows/deploy-*.yml",
    include = true,  # If this repo deploys
    reason = "Deployment workflows"
  }
]

# Testing: REQUIRED
required_files = [
  { path = ".github/workflows/ci.yml", reason = "CI mandatory" }
]

# Compliance: FORCED
# (automatically handled, can't be configured)
```

#### Documentation

```terraform
# Core docs: REQUIRED
required_files = [
  { path = "README.md", reason = "Essential documentation" },
  { path = "CONTRIBUTING.md", reason = "Contribution guide" }
]

# API docs: SUGGESTED
suggested_files = [
  { path = "docs/API.md", reason = "API documentation recommended" }
]
```

### Migration Strategies

#### Phasing Out a File

**Step 1**: Add as NOT_SUGGESTED
```terraform
not_suggested_files = [
  {
    path   = ".travis.yml"
    reason = "Travis CI deprecated - migrate to GitHub Actions by Q2 2026"
  }
]
```

**Step 2**: Monitor usage (via sync logs)

**Step 3**: After migration period, upgrade to NOT_ALLOWED if necessary

#### Introducing a New Requirement

**Phase 1**: SUGGESTED (with grace period)
```terraform
suggested_files = [
  {
    path   = "SECURITY.md"
    reason = "Security policy recommended - will be required Q3 2026"
  }
]
```

**Phase 2**: After grace period, upgrade to REQUIRED
```terraform
required_files = [
  {
    path   = "SECURITY.md"
    reason = "Security policy required (as of Q3 2026)"
  }
]
```

### Troubleshooting Common Issues

#### Issue: File keeps getting synced despite exclusion

**Diagnosis**: File might be REQUIRED or FORCED

**Solution**:
```bash
# Check enforcement level
grep -r "filename" .github/config.tf docs/terraform/
# If REQUIRED or FORCED, cannot be excluded
```

#### Issue: Warning about protected file being FORCED

**Diagnosis**: File is in FORCED list

**Solution**: Remove from protected_files (it will be synced anyway)

#### Issue: NOT_ALLOWED file present but no error

**Diagnosis**: File might not be in not_allowed_files list

**Solution**: Add to NOT_ALLOWED list in config.tf

---

## Implementation Details

### Code Location

**Primary Implementation**: `scripts/automation/bulk_update_repos.php`

**Key Methods**:
- `shouldSkipFile()` - Determines if file should be skipped
- `getFileEnforcementLevel()` - Gets enforcement level for file
- `ENFORCEMENT_LEVELS` - Constant defining all 6 levels
- `ALWAYS_FORCE_OVERRIDE_FILES` - Array of FORCED files

### Configuration Format

**Location**: `.github/config.tf` in each repository

**Structure**:
```terraform
locals {
  enforcement_levels = {
    optional_files      = [...]  # Level 1
    suggested_files     = [...]  # Level 2
    required_files      = [...]  # Level 3
    # Level 4 (FORCED) is hardcoded
    not_suggested_files = [...]  # Level 5
    not_allowed_files   = [...]  # Level 6
  }
}
```

### Validation

**Standards-Compliance Check #28**: Terraform Validation
- Validates config.tf syntax
- Checks for required metadata
- Verifies enforcement level configuration
- Warns about conflicts

### Logging

**Remote Sync Logs**: `logs/MokoStandards/sync/`
- `sync-YYYYMMDD-HHMMSS.log` - Session log
- `sync-latest.log` - Most recent sync
- `sync-summary.json` - Machine-readable summary

**Log Contents**:
- Enforcement level for each file
- Skip/sync decisions
- Warnings and errors
- Override attempts
- Compliance violations

---

## Troubleshooting

### Common Scenarios

#### Scenario 1: File Won't Sync

**Symptoms**: File is not being synced to repository

**Possible Causes**:
1. File is OPTIONAL and not opted in
2. File is excluded in config.tf
3. File is NOT_SUGGESTED
4. File path is wrong

**Diagnosis**:
```bash
# Check sync logs
cat logs/MokoStandards/sync/sync-latest.log | grep filename

# Check config.tf
cat .github/config.tf | grep filename

# Verify file exists in MokoStandards
ls -la path/to/file
```

**Solutions**:
- If OPTIONAL: Add `include = true`
- If excluded: Remove from `exclude_files`
- If NOT_SUGGESTED: Remove from `not_suggested_files`
- If path wrong: Correct path in configuration

#### Scenario 2: Cannot Exclude Required File

**Symptoms**: File syncs even though excluded in config.tf

**Cause**: File is REQUIRED or FORCED

**Diagnosis**:
```bash
# Check if file is in REQUIRED list
grep -A 5 "required_files" .github/config.tf

# Check if file is in FORCED list (hardcoded)
# Look for file in ALWAYS_FORCE_OVERRIDE_FILES
```

**Solution**: 
- REQUIRED files cannot be excluded (by design)
- FORCED files cannot be excluded (security requirement)
- If file shouldn't be REQUIRED, request policy change

#### Scenario 3: NOT_ALLOWED File Present

**Symptoms**: Build fails with "NOT_ALLOWED file detected"

**Cause**: Prohibited file is in repository

**Diagnosis**:
```bash
# Find the file
find . -name ".env" -o -name "secrets.json" -o -name "*.pem"

# Check what's in the file (carefully!)
head -5 .env  # View first 5 lines
```

**Solution**:
1. **Immediate**: Remove file from repository
   ```bash
   git rm .env
   git commit -m "Remove prohibited file"
   git push
   ```

2. **If file is needed**:
   - Move secrets to environment variables
   - Use secret management system
   - Add .env to .gitignore
   - Use .env.example template instead

3. **Verify removal**:
   ```bash
   # Check git history
   git log --all --full-history -- .env
   
   # If file is in history, may need to remove from history
   # (consult security team before doing this)
   ```

#### Scenario 4: Too Many Warnings

**Symptoms**: Sync logs full of warnings

**Causes**:
1. Many SUGGESTED files excluded
2. Many NOT_SUGGESTED files present
3. Configuration conflicts

**Diagnosis**:
```bash
# Count warnings
cat logs/MokoStandards/sync/sync-latest.log | grep WARNING | wc -l

# List warnings
cat logs/MokoStandards/sync/sync-latest.log | grep WARNING
```

**Solutions**:
- Review excluded SUGGESTED files - do you really need to exclude them?
- Migrate away from NOT_SUGGESTED files
- Align configuration with organizational standards
- If justified, document reasons clearly

### Debug Commands

```bash
# View enforcement levels for a file
grep -A 3 "filename" .github/config.tf

# Check recent sync log
tail -100 logs/MokoStandards/sync/sync-latest.log

# Count files by enforcement level
cat logs/MokoStandards/sync/sync-summary.json | jq '.files_by_level'

# Find all NOT_ALLOWED files
cat logs/MokoStandards/sync/sync-latest.log | grep "NOT_ALLOWED"

# Check if file is FORCED
# (check source code)
grep -n "ALWAYS_FORCE_OVERRIDE_FILES" scripts/automation/bulk_update_repos.php
```

---

## Related Documentation

### Primary References

- **Terraform File Standards**: [docs/policy/terraform-file-standards.md](../policy/terraform-file-standards.md)
- **Terraform Enforcement Levels** (terraform-specific): [docs/terraform/enforcement-levels.md](terraform/enforcement-levels.md)
- **Override Configuration**: [docs/terraform/config-override.md](terraform/config-override.md)
- **Bulk Sync Documentation**: [docs/workflows/bulk-repo-sync.md](workflows/bulk-repo-sync.md)

### Training Materials

- **Session 7: Terraform Infrastructure**: [docs/training/session-7-terraform-infrastructure.md](training/session-7-terraform-infrastructure.md)
  - Part 2: Six-Tier Enforcement System
  - Part 2.5: How Terraform Enforces Standards
  - Hands-on exercises

### Technical References

- **Standards-Compliance Workflow**: [.github/workflows/standards-compliance.yml](../.github/workflows/standards-compliance.yml)
  - Check #28: Terraform Validation
- **Bulk Update Script**: [scripts/automation/bulk_update_repos.php](../scripts/automation/bulk_update_repos.php)
  - Implementation of enforcement logic

### Quick References

- **Terraform README**: [docs/terraform/README.md](terraform/README.md)
- **Config Template**: [.github/config.tf](../.github/config.tf)

---

## Appendix

### Glossary

**Enforcement Level**: Category that determines how a file is handled during sync

**Sync**: Process of copying files from MokoStandards to target repositories

**Override**: Repository-specific configuration that changes default behavior

**Protected File**: File that repository wants to keep unchanged

**Excluded File**: File that repository doesn't want to include

**Force-Override**: Mechanism that syncs file regardless of configuration

**Compliance**: Adherence to organizational standards and requirements

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Added comprehensive enforcement levels documentation |
| 04.00.02 | 2026-02-21 | Implemented six-tier system with NOT_SUGGESTED and NOT_ALLOWED |
| 04.00.01 | 2026-02-21 | Four-tier system (OPTIONAL, SUGGESTED, REQUIRED, FORCED) |

### Contributing

To suggest changes to enforcement levels:

1. Open an issue describing the change
2. Provide justification (security, compliance, best practice)
3. Include example use cases
4. Consider impact on existing repositories
5. Update this documentation

---

## Summary

The six-tier enforcement level system provides:

✅ **Clear Structure**: Six well-defined levels from OPTIONAL to NOT_ALLOWED
✅ **Graduated Control**: From permissive to restrictive
✅ **Security First**: NOT_ALLOWED checked before anything else
✅ **Flexibility**: Appropriate override capabilities per level
✅ **Compliance**: Clear requirements and audit trail
✅ **Documentation**: Comprehensive guidance for all scenarios

**Remember**:
- NOT_ALLOWED (Level 6): Absolute prohibition, checked first
- FORCED (Level 4): Critical files, always synced
- REQUIRED (Level 3): Mandatory for all
- SUGGESTED (Level 2): Recommended, can override
- NOT_SUGGESTED (Level 5): Discouraged, can override
- OPTIONAL (Level 1): Opt-in only

For questions or clarifications, consult the training materials or reach out to the MokoStandards team.

---

**Document End**
