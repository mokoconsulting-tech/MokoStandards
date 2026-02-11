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
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/terraform-override-files.md
VERSION: 03.02.00
BRIEF: Guide for using MokoStandards.override.tf files to control bulk sync behavior
-->

# Terraform Override Files - Complete Guide

**Version**: 2.0.0  
**Status**: Active  
**Last Updated**: 2026-02-11

## Table of Contents

- [Overview](#overview)
- [What is MokoStandards.override.tf?](#what-is-mokostandardsoverridetf)
- [Why Use Override Files?](#why-use-override-files)
- [Enterprise Library Integration](#enterprise-library-integration)
- [File Structure](#file-structure)
- [Key Features](#key-features)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The `MokoStandards.override.tf` file is a **Terraform-based configuration file** that controls how the bulk repository sync tool synchronizes standards, workflows, and scripts from MokoStandards to your repository.

**New in Version 2.0**: Support for enterprise library integration and new monitoring workflows (audit-log-archival, metrics-collection, health-check, security-scan, integration-tests).

### Key Benefits

✅ **Explicit Platform Control** - Specify your repository type to skip auto-detection  
✅ **File Exclusion** - Prevent specific files from being synced  
✅ **File Protection** - Protect files from being overwritten  
✅ **Cleanup Configuration** - Control how obsolete files are handled  
✅ **Enterprise Library Support** - Control sync of enterprise audit, metrics, and monitoring features  
✅ **Self-Documenting** - Terraform format is readable and version-controlled

---

## What is MokoStandards.override.tf?

The override file is placed in the **root directory** of your repository and uses Terraform's HCL (HashiCorp Configuration Language) syntax to define sync behavior.

### Location

```
your-repository/
├── .github/
├── src/
├── MokoStandards.override.tf  ← Place file here
└── README.md
```

### How It Works

1. **Bulk sync script runs** (monthly or manually)
2. **Script checks for override file** in your repository
3. **Override settings are applied** BEFORE platform detection
4. **Only allowed files are synced** based on your configuration

---

## Why Use Override Files?

### Problem Without Override File

Without an override file, the bulk sync tool will:
- Auto-detect your platform type (may be incorrect)
- Sync ALL standard files (may conflict with your needs)
- Overwrite files you've customized
- Use default cleanup behavior

### Solution With Override File

With an override file, you can:
- **Explicitly specify platform type** (terraform, dolibarr, joomla, generic)
- **Exclude unwanted workflows** or scripts
- **Protect custom files** from being overwritten
- **Control cleanup behavior** (conservative, aggressive, none)
- **Enable/disable enterprise features** (audit logging, metrics collection, monitoring)

---

## Enterprise Library Integration

**New in Version 03.02.00**: MokoStandards now includes enterprise-grade libraries and monitoring workflows.

### Available Enterprise Features

#### 1. Enterprise Libraries (scripts/lib/)
- **enterprise_audit.py** - Transaction tracking and security event logging
- **api_client.py** - Rate limiting, circuit breaker, and response caching
- **error_recovery.py** - Automatic retry, checkpointing, and state recovery
- **metrics_collector.py** - Prometheus-compatible metrics collection
- **transaction_manager.py** - Atomic operations with rollback support
- **cli_framework.py** - Standardized CLI with common arguments

#### 2. Monitoring Workflows
- **audit-log-archival.yml** - Weekly audit log archival and compliance reports
- **metrics-collection.yml** - Daily metrics collection and trend analysis
- **health-check.yml** - Hourly health monitoring and circuit breaker testing
- **security-scan.yml** - Daily enhanced security scanning
- **integration-tests.yml** - Enterprise library integration testing

### Controlling Enterprise Features

Use the override file to protect or exclude enterprise workflows:

```hcl
# Exclude enterprise workflows if not needed
exclude_files = [
  {
    path   = ".github/workflows/audit-log-archival.yml"
    reason = "Custom audit solution in place"
  },
  {
    path   = ".github/workflows/metrics-collection.yml"
    reason = "Using external monitoring service"
  },
]

# Protect enterprise workflows from updates
protected_files = [
  {
    path   = ".github/workflows/health-check.yml"
    reason = "Customized health check configuration"
  },
]
```

### Integration Status

The following critical scripts have been enhanced with enterprise libraries:
- ✅ `scripts/automation/bulk_update_repos.py` - Audit, API client, error recovery, metrics
- ✅ `scripts/automation/auto_create_org_projects.py` - Audit, API client, metrics
- ✅ `scripts/maintenance/clean_old_branches.py` - Audit, metrics
- ✅ `scripts/release/unified_release.py` - Transaction management, audit, error recovery

See [docs/planning/README.md](../planning/README.md) for the complete enterprise transformation roadmap.

---

## File Structure

### Minimal Example

```hcl
# MokoStandards.override.tf
locals {
  # Metadata
  override_metadata = {
    name            = "My Repository Override"
    description     = "Custom sync configuration for my-repo"
    version         = "1.0.0"
    last_updated    = "2026-02-08T00:00:00Z"
    maintainer      = "Your Team"
    schema_version  = "2.0"
    repository_url  = "https://github.com/mokoconsulting-tech/my-repo"
    
    # Platform Type (IMPORTANT!)
    repository_type  = "terraform"  # or "dolibarr", "joomla", "generic"
    compliance_level = "standard"
    format           = "terraform"
  }

  # Sync Configuration
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"  # "none", "conservative", or "aggressive"
  }

  # Files to Exclude (optional)
  exclude_files = []

  # Files to Protect (optional)
  protected_files = []
}
```

### Complete Example

See [Complete Override Example](#complete-override-example) below for a full-featured configuration.

---

## Key Features

### 1. Platform Type Specification

**Most Important Feature**: Specify your repository type to skip auto-detection.

```hcl
override_metadata = {
  repository_type = "terraform"  # Options: terraform, dolibarr, joomla, generic, standards
}
```

**Platform Types:**
- `terraform` - Infrastructure/Terraform projects
- `dolibarr` - Dolibarr CRM modules
- `joomla` - Joomla extensions
- `generic` - General-purpose projects
- `standards` - Template repositories (like MokoStandards itself)

**Benefits:**
- ✅ Faster sync (no platform detection needed)
- ✅ More accurate (no detection errors)
- ✅ Explicit control over workflows synced

### 2. File Exclusion

Prevent specific files from being synced to your repository.

```hcl
exclude_files = [
  {
    path   = ".github/workflows/build.yml"
    reason = "Using custom build workflow"
  },
  {
    path   = ".github/workflows/release.yml"
    reason = "Manual release process"
  }
]
```

**Use Cases:**
- Custom workflows you want to maintain independently
- Files that conflict with your project structure
- Deprecated workflows you don't use

### 3. File Protection

Protect files from being overwritten during sync.

```hcl
protected_files = [
  {
    path   = ".gitignore"
    reason = "Repository-specific ignore patterns"
  },
  {
    path   = ".editorconfig"
    reason = "Custom editor configuration"
  },
  {
    path   = "scripts/custom_deploy.py"
    reason = "Custom deployment script"
  }
]
```

**Use Cases:**
- Files you've customized for your repository
- Configuration files with project-specific settings
- Scripts with custom logic

### 4. Cleanup Mode

Control how the sync tool handles obsolete files.

```hcl
sync_config = {
  enabled = true
  cleanup_mode = "conservative"  # Options: none, conservative, aggressive
}
```

**Cleanup Modes:**

| Mode | Behavior | When to Use |
|------|----------|-------------|
| `none` | No cleanup, only add/update files | Initial sync, testing |
| `conservative` | Remove obsolete `.yml` and `.py` files | **Recommended** - Safe cleanup |
| `aggressive` | Remove all non-synced files in managed dirs | Advanced users only |

---

## Usage Examples

### Example 1: Terraform Project

```hcl
# MokoStandards.override.tf for Terraform infrastructure repo
locals {
  override_metadata = {
    name             = "Infrastructure Repository Override"
    description      = "Terraform infrastructure project"
    version          = "1.0.0"
    last_updated     = "2026-02-08T00:00:00Z"
    maintainer       = "DevOps Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/infra"
    repository_type  = "terraform"
    compliance_level = "strict"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # Exclude generic workflows, we only want terraform-specific ones
  exclude_files = [
    {
      path   = ".github/workflows/code-quality.yml"
      reason = "Using terraform-specific linting"
    }
  ]

  # Protect our custom terraform configuration
  protected_files = [
    {
      path   = "terraform.tfvars"
      reason = "Environment-specific variables"
    }
  ]
}
```

### Example 2: Dolibarr Module

```hcl
# MokoStandards.override.tf for Dolibarr module
locals {
  override_metadata = {
    name             = "Dolibarr Module Override"
    description      = "Custom CRM module for Dolibarr"
    version          = "1.0.0"
    last_updated     = "2026-02-08T00:00:00Z"
    maintainer       = "CRM Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/dolibarr-mymodule"
    repository_type  = "dolibarr"
    compliance_level = "standard"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  exclude_files = []
  protected_files = []
}
```

### Example 3: Generic Application

```hcl
# MokoStandards.override.tf for generic application
locals {
  override_metadata = {
    name             = "Application Repository Override"
    description      = "Custom application project"
    version          = "1.0.0"
    last_updated     = "2026-02-08T00:00:00Z"
    maintainer       = "Application Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/my-app"
    repository_type  = "generic"
    compliance_level = "standard"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # We have custom CI/CD
  exclude_files = [
    {
      path   = ".github/workflows/ci.yml"
      reason = "Custom CI pipeline with specialized steps"
    },
    {
      path   = ".github/workflows/build.yml"
      reason = "Custom build process"
    }
  ]

  # Protect our custom configurations
  protected_files = [
    {
      path   = ".editorconfig"
      reason = "Team-specific editor settings"
    },
    {
      path   = ".gitignore"
      reason = "Project-specific ignore patterns"
    }
  ]
}
```

---

## Best Practices

### 1. Always Specify Repository Type

**DO:**
```hcl
repository_type = "terraform"  # Explicit
```

**DON'T:**
```hcl
# Omitting repository_type forces auto-detection
```

### 2. Document Your Exclusions

**DO:**
```hcl
exclude_files = [
  {
    path   = ".github/workflows/deploy.yml"
    reason = "Using custom deployment with Ansible integration"
  }
]
```

**DON'T:**
```hcl
exclude_files = [
  {
    path   = ".github/workflows/deploy.yml"
    reason = "custom"  # Too vague
  }
]
```

### 3. Start Conservative

**DO:**
```hcl
cleanup_mode = "conservative"  # Safe default
```

**DON'T:**
```hcl
cleanup_mode = "aggressive"  # Use only when you know what you're doing
```

### 4. Version Your Override File

**DO:**
```hcl
version      = "1.0.0"
last_updated = "2026-02-08T00:00:00Z"
```

Update these fields when you modify the override configuration.

### 5. Keep Metadata Current

**DO:**
```hcl
maintainer     = "Current Team Name"
repository_url = "https://github.com/mokoconsulting-tech/actual-repo"
```

**DON'T:**
```hcl
maintainer     = "Unknown"
repository_url = "https://example.com"
```

---

## Advanced Configuration

### Complete Override Example

```hcl
# MokoStandards.override.tf - Complete Example
locals {
  # Metadata about this override configuration
  override_metadata = {
    name           = "Advanced Repository Override Configuration"
    description    = "Comprehensive sync control with exclusions and protections"
    version        = "2.0.0"
    last_updated   = "2026-02-08T10:00:00Z"
    maintainer     = "DevOps Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/advanced-repo"
    
    # Platform specification
    repository_type  = "terraform"
    compliance_level = "strict"
    format           = "terraform"
  }

  # Sync configuration
  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # Files to exclude from sync
  exclude_files = [
    # Custom workflows
    {
      path   = ".github/workflows/custom-ci.yml"
      reason = "Custom CI with integration tests"
    },
    {
      path   = ".github/workflows/deploy-production.yml"
      reason = "Production deployment with manual approval"
    },
    # Custom scripts
    {
      path   = "scripts/deploy.sh"
      reason = "Custom deployment script with environment-specific logic"
    },
    # Platform-specific exclusions
    {
      path   = ".github/workflows/code-quality.yml"
      reason = "Using terraform-specific linting instead"
    }
  ]

  # Files to protect from overwrite
  protected_files = [
    # Configuration files
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    },
    {
      path   = ".editorconfig"
      reason = "Team-specific editor configuration"
    },
    # Documentation
    {
      path   = "README.md"
      reason = "Custom project documentation"
    },
    # Custom GitHub configurations
    {
      path   = ".github/CODEOWNERS"
      reason = "Team-specific code ownership"
    },
    # Custom scripts
    {
      path   = "scripts/bootstrap.sh"
      reason = "Custom initialization script"
    }
  ]

  # Optional: Mark files as obsolete for removal
  obsolete_files = [
    {
      path   = "scripts/old_deploy.sh"
      reason = "Replaced by new deployment system"
    }
  ]
}
```

### Testing Your Override Configuration

Before committing your override file:

1. **Validate Terraform syntax:**
   ```bash
   terraform fmt -check MokoStandards.override.tf
   ```

2. **Test with dry run:**
   Trigger the bulk sync workflow with dry-run mode enabled to preview changes.

3. **Review sync logs:**
   Check that excluded files are not synced and protected files are not overwritten.

---

## Troubleshooting

### Problem: Files Still Being Synced Despite Exclusion

**Symptom:** Files listed in `exclude_files` are still being synced.

**Solutions:**
1. Check the exact file path in `exclude_files` matches the sync target path
2. Verify Terraform syntax is valid (`terraform fmt -check`)
3. Check sync logs to confirm override file was loaded
4. Ensure `sync_config.enabled = true`

### Problem: Platform Detection Still Running

**Symptom:** Logs show "Detecting platform type..." even with override.

**Solutions:**
1. Verify `repository_type` is set in `override_metadata`
2. Check that `repository_type` is not "standards" (which is ignored)
3. Ensure override file is in repository root
4. Validate file syntax

### Problem: Cleanup Removing Too Many Files

**Symptom:** Important files are being deleted during sync.

**Solutions:**
1. Change `cleanup_mode` from "aggressive" to "conservative"
2. Add files to `protected_files` list
3. Use `cleanup_mode = "none"` temporarily to diagnose
4. Review deleted files in sync logs

### Problem: Override File Not Being Read

**Symptom:** Default behavior is used despite override file existing.

**Solutions:**
1. Verify file is named exactly `MokoStandards.override.tf`
2. Check file is in repository root (not subdirectory)
3. Validate Terraform syntax
4. Check file permissions (must be readable)

---

## Related Documentation

- [Bulk Repository Sync Workflow](../workflows/bulk-repo-sync.md)
- [Terraform Metadata Standards](../policy/terraform-metadata-standards.md)
- [Terraform Schemas Reference](../reference/terraform-schemas.md)
- [Platform Detection Guide](../guide/platform-detection.md)

---

## Support

For questions or issues with override files:

1. Review this documentation
2. Check [bulk_update_repos.py](../../scripts/automation/bulk_update_repos.py) source code
3. Open an issue in [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards/issues)
4. Contact the MokoStandards team

---

**Last Updated**: 2026-02-08  
**Maintainer**: MokoStandards Team  
**License**: GPL-3.0-or-later
