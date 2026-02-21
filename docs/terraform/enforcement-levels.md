# File Enforcement Levels in Terraform Configuration

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **VERSION** | 04.00.03 |
| **LAST UPDATED** | 2026-02-21 |
| **STATUS** | Active |
| **APPLIES TO** | All terraform configurations and bulk sync operations |

## Overview

The MokoStandards terraform configuration system uses a **six-tier enforcement level system** to control file synchronization across repositories. This system balances organizational standards with repository-specific needs.

## The Six Enforcement Levels

### Level 1: OPTIONAL ⭕

**Definition**: Files that **MAY** be synced if repository explicitly opts in.

**Behavior**:
- ❌ Not created by default
- ✅ Repository must explicitly include
- ✅ Can be excluded without warnings
- ✅ No compliance impact if missing

**Use Cases**:
- Optional features (e.g., performance testing workflows)
- Environment-specific configurations (e.g., staging deployment)
- Advanced tooling (e.g., specialized CI/CD pipelines)
- Experimental features

**Configuration Example**:
```terraform
enforcement_levels = {
  optional_files = [
    {
      path    = ".github/workflows/deploy-to-staging.yml"
      reason  = "Only needed for repositories with staging environment"
      include = true  # Opt-in: Set to true to include this file
    },
    {
      path    = ".github/workflows/performance-testing.yml"
      reason  = "Optional performance testing workflow"
      include = false  # Opt-out: File will not be synced
    }
  ]
}
```

**Sync Behavior**:
```
Processing optional file: .github/workflows/deploy-to-staging.yml
✓ OPTIONAL (Level 1 - explicitly included) - will sync
```

---

### Level 2: SUGGESTED ⚠️

**Definition**: Files that **SHOULD** be synced (recommended best practices).

**Behavior**:
- ✅ Created by default
- ⚠️ Generates warnings if excluded
- ✅ Can be overridden with justification
- ⚠️ May impact compliance scoring
- ✅ Respects protected_files configuration

**Use Cases**:
- Security best practices (e.g., CodeQL scanning)
- Recommended workflows (e.g., dependency review)
- Standard configurations (e.g., .editorconfig)
- Quality assurance tools

**Configuration Example**:
```terraform
enforcement_levels = {
  suggested_files = [
    {
      path   = ".github/workflows/dependency-review.yml"
      reason = "Recommended security practice for dependency scanning"
    },
    {
      path   = ".github/workflows/codeql-analysis.yml"
      reason = "Recommended for code security scanning"
    },
    {
      path   = ".editorconfig"
      reason = "Recommended for consistent code formatting"
    }
  ]
}

# Can be excluded, but generates warning
exclude_files = [
  {
    path   = ".github/workflows/codeql-analysis.yml"
    reason = "Using external security scanning service"
  }
]
```

**Sync Behavior**:
```
Processing suggested file: .github/workflows/dependency-review.yml
✓ SUGGESTED (Level 2 - recommended file) - will sync

Processing suggested file: .github/workflows/codeql-analysis.yml
⚠ WARNING: Suggested file excluded (not recommended)
✗ Skip: SUGGESTED but excluded in config.tf
```

---

### Level 3: REQUIRED ⛔

**Definition**: Files that **MUST** be synced (mandatory for compliance).

**Behavior**:
- ✅ Always created
- ❌ Cannot be excluded via config.tf
- ⚠️ Generates errors if missing or excluded
- ❌ Ignores protected_files setting
- ❌ Compliance failure if not present

**Use Cases**:
- License files (e.g., LICENSE)
- Contributing guidelines (e.g., CONTRIBUTING.md)
- Required workflows (e.g., CI/CD)
- Mandatory documentation (e.g., README.md structure)

**Configuration Example**:
```terraform
enforcement_levels = {
  required_files = [
    {
      path   = ".github/workflows/ci.yml"
      reason = "Continuous integration is mandatory"
    },
    {
      path   = "LICENSE"
      reason = "License file required for all repositories"
    },
    {
      path   = "CONTRIBUTING.md"
      reason = "Contributing guidelines required"
    }
  ]
}

# Attempting to exclude generates ERROR
exclude_files = [
  {
    path   = "LICENSE"  # This will be IGNORED
    reason = "Custom license"  # ERROR: Cannot exclude required file
  }
]
```

**Sync Behavior**:
```
Processing required file: LICENSE
⚠ WARNING: Required file 'LICENSE' is excluded - this violates compliance
✓ REQUIRED (Level 3 - mandatory file - must be synced) - will sync anyway

Processing required file: CONTRIBUTING.md
⚠ WARNING: Required file is protected - will be overridden
✓ REQUIRED (Level 3 - mandatory file - must be synced) - will sync
```

---

### Level 4: FORCED 🔒

**Definition**: Files that are **ALWAYS** synced regardless of any configuration.

**Behavior**:
- ✅ Always created and updated
- ❌ Cannot be excluded
- ❌ Cannot be protected
- ❌ Overrides ALL config.tf settings
- ✅ Ensures critical compliance infrastructure

**Use Cases**:
- Critical security files
- Organization-wide compliance checks
- Essential validation scripts
- Core infrastructure requirements

**Forced Files** (Defined in Code):
```php
// In bulk_update_repos.php
private const ALWAYS_FORCE_OVERRIDE_FILES = [
    '.github/workflows/standards-compliance.yml',
    'scripts/validate/check_version_consistency.php',
    'scripts/validate/check_enterprise_readiness.php',
    'scripts/validate/check_repo_health.php',
    'scripts/maintenance/validate_script_registry.py',
    'scripts/.script-registry.json',
];
```

**Configuration Example**:
```terraform
# These are documented for clarity but CANNOT be overridden
enforcement_levels = {
  forced_files = [
    {
      path   = ".github/workflows/standards-compliance.yml"
      reason = "Critical: Organization-wide compliance checks"
      # NOTE: This documentation is informational only
      # These files ALWAYS sync regardless of config
    },
    {
      path   = "scripts/validate/check_version_consistency.php"
      reason = "Critical: Version consistency validation"
    }
  ]
}

# Attempting to protect or exclude is IGNORED
protected_files = [
  {
    path   = ".github/workflows/standards-compliance.yml"
    reason = "Custom compliance checks"  # IGNORED: File still synced
  }
]
```

**Sync Behavior**:
```
Processing forced file: .github/workflows/standards-compliance.yml
✓ FORCED (Level 4 - critical compliance file - always updated regardless of config.tf)
  Note: This file is protected in config.tf but FORCE_OVERRIDE takes precedence
```

---

## Enforcement Level Comparison

| Feature | OPTIONAL (1) | SUGGESTED (2) | REQUIRED (3) | FORCED (4) |
|---------|--------------|---------------|--------------|------------|
| **Synced by default** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Can be excluded** | ✅ Yes | ✅ Yes (warning) | ❌ No (error) | ❌ No |
| **Can be protected** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Requires opt-in** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Compliance impact** | ✅ None | ⚠️ Warning | ❌ Error | ❌ Critical |
| **Override allowed** | ✅ Yes | ⚠️ Discouraged | ❌ No | ❌ Never |

## Enforcement Level Decision Tree

```
┌─────────────────────────────────────┐
│ Is this file critical for security  │
│ or organization-wide compliance?    │
└─────────────┬───────────────────────┘
              │
              ├─ YES ─→ Level 4: FORCED
              │
              └─ NO
                 │
                 ┌────────────────────────────────┐
                 │ Is this file mandatory for all │
                 │ repositories to function?      │
                 └──────────┬─────────────────────┘
                            │
                            ├─ YES ─→ Level 3: REQUIRED
                            │
                            └─ NO
                               │
                               ┌──────────────────────────────┐
                               │ Is this file a recommended   │
                               │ best practice?               │
                               └──────────┬───────────────────┘
                                          │
                                          ├─ YES ─→ Level 2: SUGGESTED
                                          │
                                          └─ NO ─→ Level 1: OPTIONAL
```

## Configuration Examples

### Example 1: Web Application Repository

```terraform
locals {
  enforcement_levels = {
    optional_files = [
      {
        path    = ".github/workflows/deploy-to-staging.yml"
        reason  = "Has staging environment"
        include = true  # Opt in
      },
      {
        path    = ".github/workflows/performance-testing.yml"
        reason  = "Performance not critical for this app"
        include = false  # Opt out
      }
    ]
    
    suggested_files = [
      {
        path   = ".github/workflows/dependency-review.yml"
        reason = "Security scanning recommended"
      },
      {
        path   = ".editorconfig"
        reason = "Code formatting standards"
      }
    ]
    
    required_files = [
      {
        path   = ".github/workflows/ci.yml"
        reason = "Continuous integration mandatory"
      },
      {
        path   = "LICENSE"
        reason = "Open source project"
      }
    ]
    
    # forced_files documented for reference
    # (cannot be overridden)
  }
}
```

**Sync Output**:
```
✓ Sync .github/workflows/deploy-to-staging.yml: OPTIONAL (Level 1 - explicitly included)
✗ Skip .github/workflows/performance-testing.yml: OPTIONAL (Level 1 - not opted in)
✓ Sync .github/workflows/dependency-review.yml: SUGGESTED (Level 2 - recommended file)
✓ Sync .github/workflows/ci.yml: REQUIRED (Level 3 - mandatory file)
✓ Sync .github/workflows/standards-compliance.yml: FORCED (Level 4 - critical compliance)
```

### Example 2: Library Project

```terraform
locals {
  enforcement_levels = {
    optional_files = [
      {
        path    = ".github/workflows/deploy.yml"
        reason  = "Library doesn't deploy"
        include = false
      }
    ]
    
    suggested_files = [
      {
        path   = ".github/workflows/publish-package.yml"
        reason = "Package publishing workflow"
      }
    ]
  }
  
  # Exclude deployment workflows (not applicable)
  exclude_files = [
    {
      path   = ".github/workflows/deploy-production.yml"
      reason = "Library project - no deployment"
    }
  ]
  
  # Protect package-specific configuration
  protected_files = [
    {
      path   = "package.json"
      reason = "Library-specific dependencies"
    }
  ]
}
```

## Best Practices

### 1. Use Appropriate Levels

```terraform
# ✅ GOOD: Optional feature
optional_files = [{
  path = ".github/workflows/mobile-ci.yml"
  reason = "Only for mobile projects"
}]

# ❌ BAD: Using OPTIONAL for security
optional_files = [{
  path = ".github/workflows/security-scan.yml"  # Should be SUGGESTED
  reason = "Security scanning"
}]
```

### 2. Provide Clear Justifications

```terraform
# ✅ GOOD: Clear reason
exclude_files = [{
  path = ".github/workflows/deploy.yml"
  reason = "Uses external deployment system (Jenkins)"
}]

# ❌ BAD: Vague reason
exclude_files = [{
  path = ".github/workflows/deploy.yml"
  reason = "Not needed"  # Why not needed?
}]
```

### 3. Respect Enforcement Levels

```terraform
# ❌ DON'T: Try to exclude FORCED files
protected_files = [{
  path = ".github/workflows/standards-compliance.yml"  # Will be ignored
  reason = "Custom implementation"
}]

# ✅ DO: Understand FORCED files cannot be overridden
# Document your understanding instead
```

## Migration Guide

### Upgrading from Legacy Override System

**Old System** (Before 04.00.03):
```terraform
# Only had exclude and protected
exclude_files = [...]
protected_files = [...]
```

**New System** (04.00.03+):
```terraform
enforcement_levels = {
  optional_files = [...]    # Level 1
  suggested_files = [...]   # Level 2
  required_files = [...]    # Level 3
  forced_files = [...]      # Level 4 (documented)
}

# Legacy sections still supported for compatibility
exclude_files = [...]
protected_files = [...]
```

## Troubleshooting

### Issue: FORCED file marked as protected but still syncing

**Reason**: This is expected behavior. Level 4 (FORCED) overrides ALL config settings.

**Solution**: Remove from protected_files and document understanding in comments.

### Issue: REQUIRED file excluded but generating error

**Reason**: Level 3 (REQUIRED) files cannot be excluded.

**Solution**: Remove from exclude_files or contact organization admin if file truly not needed.

### Issue: SUGGESTED file warning

**Reason**: Level 2 (SUGGESTED) files generate warnings when excluded.

**Solution**: Either include the file or document why it's not needed in the reason field.

## Related Documentation

- [Override Configuration](config-override.md) - Complete override system documentation
- [Bulk Repository Sync](../workflows/bulk-repo-sync.md) - Sync process details
- [Terraform File Standards](../policy/terraform-file-standards.md) - Structure requirements

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Four-tier enforcement level system introduced |
| 04.00.02 | 2026-02-20 | Force-override system added |
| 04.00.01 | 2026-02-19 | Basic override system |

## Support

Questions about enforcement levels? Contact: MokoStandards Team
