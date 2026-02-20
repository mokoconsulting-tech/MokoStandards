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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Guide
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/bulk-repo-sync-override-files.md
VERSION: 04.00.01
BRIEF: Complete guide to terraform override files for bulk repository synchronization
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Terraform Override Files for Bulk Repository Sync

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2026-02-16

## Table of Contents

- [Overview](#overview)
- [What is a Terraform Override File?](#what-is-a-terraform-override-file)
- [File Location and Structure](#file-location-and-structure)
- [How Bulk Sync Uses Override Files](#how-bulk-sync-uses-override-files)
- [Configuration Options](#configuration-options)
- [Force Override Mode](#force-override-mode)
- [Common Use Cases](#common-use-cases)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

The **MokoStandards.override.tf** file is a Terraform-based configuration file that controls how the bulk repository sync workflow synchronizes standards, workflows, scripts, and configurations from MokoStandards to your repository.

### Purpose

When the bulk repository sync workflow runs (monthly or manually), it:
1. Checks for a `MokoStandards.override.tf` file in your repository root
2. Reads the configuration to determine sync behavior
3. Applies your custom exclusions and protections
4. Syncs only the files you've allowed

### Key Benefits

✅ **Control What Gets Synced** - Exclude specific workflows or scripts you don't need  
✅ **Protect Custom Files** - Prevent important custom files from being overwritten  
✅ **Skip Platform Detection** - Explicitly specify your repository type  
✅ **Cleanup Control** - Choose how obsolete files are handled  
✅ **Force Override Support** - Override protected files when necessary  
✅ **Self-Documenting** - Configuration is version-controlled and readable

---

## What is a Terraform Override File?

The override file uses **Terraform's HCL (HashiCorp Configuration Language)** syntax, making it:
- **Human-readable** - Easy to understand and edit
- **Version-controlled** - Tracked in git like any other file
- **Validated** - Can be checked with `terraform fmt` and `terraform validate`
- **Consistent** - Same format across all repositories

### File Name

The file **must** be named exactly:
```
MokoStandards.override.tf
```

Case-sensitive, no variations allowed.

---

## File Location and Structure

### Location

The override file must be placed in the **root directory** of your repository:

```
your-repository/
├── .github/
│   └── workflows/
├── src/
├── MokoStandards.override.tf  ← Place file here
└── README.md
```

### Basic Structure

```hcl
# MokoStandards.override.tf
locals {
  # Metadata about this configuration
  override_metadata = {
    name             = "My Repository Override"
    description      = "Custom sync configuration"
    version          = "1.0.0"
    last_updated     = "2026-02-16T00:00:00Z"
    maintainer       = "DevOps Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/my-repo"
    repository_type  = "terraform"  # or "dolibarr", "joomla", "generic"
    compliance_level = "standard"
    format           = "terraform"
  }

  # Sync configuration
  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"  # "none", "conservative", or "aggressive"
  }

  # Files to exclude from sync (optional)
  exclude_files = []

  # Files to protect from overwrite (optional)
  protected_files = []

  # Files explicitly marked for removal (optional)
  obsolete_files = []
}
```

---

## How Bulk Sync Uses Override Files

### Sync Process Flow

1. **Clone Repository**: Bulk sync clones your repository to a temporary directory
2. **Check for Override**: Looks for `MokoStandards.override.tf` in repository root
3. **Parse Configuration**: If found, reads and validates the configuration
4. **Apply Settings**: Uses your settings to control sync behavior
5. **Sync Files**: Only syncs files that aren't excluded or protected
6. **Create PR**: Creates pull request with changes for review

### Priority Order

The bulk sync tool uses this priority order:

1. **Force Override Mode** (if enabled) - Overrides everything, including protected files
2. **Protected Files** - Never overwritten (unless force override)
3. **Excluded Files** - Never synced
4. **Repository Type** - Uses override type or auto-detects
5. **Cleanup Mode** - Controls obsolete file removal
6. **Default Behavior** - Standard sync behavior

---

## Configuration Options

### 1. Repository Metadata

Describes your repository and override configuration:

```hcl
override_metadata = {
  name             = "Infrastructure Repository Override"
  description      = "Terraform infrastructure project with custom CI"
  version          = "1.2.0"
  last_updated     = "2026-02-16T10:30:00Z"
  maintainer       = "DevOps Team"
  schema_version   = "2.0"
  repository_url   = "https://github.com/mokoconsulting-tech/infra"
  
  # Platform type (REQUIRED)
  repository_type  = "terraform"  # Options: terraform, dolibarr, joomla, generic, standards
  
  compliance_level = "strict"     # Options: minimal, standard, strict
  format           = "terraform"  # Always "terraform"
}
```

**Repository Types:**
- `terraform` - Infrastructure/Terraform projects
- `dolibarr` - Dolibarr CRM modules
- `joomla` - Joomla extensions
- `generic` - General-purpose projects
- `standards` - Template repositories (like MokoStandards)

### 2. Sync Configuration

Controls how sync behaves:

```hcl
sync_config = {
  enabled      = true              # Enable/disable sync
  cleanup_mode = "conservative"    # Cleanup behavior
}
```

**Cleanup Modes:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| `none` | No cleanup, only add/update files | Testing, initial sync |
| `conservative` | Remove obsolete `.yml` and `.py` files only | **Recommended** - Safe default |
| `aggressive` | Remove all non-synced files in managed dirs | Advanced users, strict compliance |

### 3. Exclude Files

Prevent specific files from being synced to your repository:

```hcl
exclude_files = [
  {
    path   = ".github/workflows/custom-ci.yml"
    reason = "Custom CI workflow with integration tests"
  },
  {
    path   = "scripts/deploy.sh"
    reason = "Custom deployment script with environment-specific logic"
  }
]
```

**Use Cases:**
- Custom workflows you maintain independently
- Files that conflict with your project structure
- Deprecated workflows you don't use
- Platform-specific files not needed

### 4. Protected Files

Protect files from being overwritten during sync:

```hcl
protected_files = [
  {
    path   = ".gitignore"
    reason = "Repository-specific ignore patterns"
  },
  {
    path   = ".editorconfig"
    reason = "Team-specific editor configuration"
  },
  {
    path   = "scripts/custom_deploy.py"
    reason = "Custom deployment script with sensitive credentials"
  }
]
```

**Use Cases:**
- Files you've customized for your repository
- Configuration files with project-specific settings
- Scripts with custom logic or credentials
- Documentation with repository-specific content

**Important:** Protected files can be overridden with `--force-override` flag (see below).

### 5. Obsolete Files

Explicitly mark files for removal:

```hcl
obsolete_files = [
  {
    path   = "scripts/old_deploy.sh"
    reason = "Replaced by new deployment system in v2.0"
  },
  {
    path   = ".github/workflows/deprecated-ci.yml"
    reason = "Replaced by unified-ci.yml"
  }
]
```

---

## Force Override Mode

### Overview

**Force override mode** allows the bulk sync workflow to override **all** protections, including protected files. This is useful for emergency updates or enforcing critical standards.

### When to Use Force Override

✅ **DO use for:**
- Emergency security fixes that must be deployed immediately
- Critical workflow updates required across all repositories
- Standardizing configuration after organizational policy changes
- Fixing broken workflows that are protected

❌ **DON'T use for:**
- Regular monthly syncs
- Testing new workflows
- Updates that can wait for review
- Non-critical changes

### How to Enable Force Override

#### Method 1: Workflow Dispatch (Recommended)

When manually triggering the bulk sync workflow:

1. Go to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. Check the **force_override** checkbox
4. Specify repositories and run

#### Method 2: Command Line

When running the script directly:

```bash
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --repos target-repo
```

### Force Override Behavior

When force override is enabled:

1. **Protected files** - WILL be overwritten
2. **Excluded files** - Still NOT synced (exclusions still respected)
3. **Custom files** - May be overwritten if they match sync targets
4. **Cleanup mode** - Still applies (conservative/aggressive/none)

### Safety Considerations

⚠️ **Important Warnings:**

- Force override bypasses repository-level protections
- Custom changes in protected files will be lost
- Always create a backup before using force override
- Review the PR carefully before merging
- Consider communicating with repository owners first

**Best Practice:** Always use `--dry-run` first to preview what will be overwritten:

```bash
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --dry-run \
  --repos target-repo
```

---

## Common Use Cases

### Use Case 1: Terraform Project with Custom CI

**Scenario:** Infrastructure repository needs terraform workflows but has custom CI.

```hcl
locals {
  override_metadata = {
    name             = "Infrastructure Repository"
    repository_type  = "terraform"
    version          = "1.0.0"
    last_updated     = "2026-02-16T00:00:00Z"
    maintainer       = "DevOps Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/infra"
    compliance_level = "strict"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # Exclude generic CI, we have custom terraform CI
  exclude_files = [
    {
      path   = ".github/workflows/code-quality.yml"
      reason = "Using terraform-specific linting and validation"
    }
  ]

  # Protect our terraform configuration
  protected_files = [
    {
      path   = "terraform.tfvars"
      reason = "Environment-specific variables and secrets"
    }
  ]
}
```

### Use Case 2: Dolibarr Module with Custom Release

**Scenario:** Dolibarr module needs standard workflows but custom release process.

```hcl
locals {
  override_metadata = {
    name             = "Dolibarr Custom Module"
    repository_type  = "dolibarr"
    version          = "1.0.0"
    last_updated     = "2026-02-16T00:00:00Z"
    maintainer       = "CRM Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/dolibarr-mymodule"
    compliance_level = "standard"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # We have custom release workflow
  exclude_files = [
    {
      path   = ".github/workflows/release.yml"
      reason = "Custom release process with manual testing steps"
    }
  ]

  protected_files = []
}
```

### Use Case 3: Generic Project with Many Customizations

**Scenario:** Application with custom workflows, scripts, and configuration.

```hcl
locals {
  override_metadata = {
    name             = "Web Application Project"
    repository_type  = "generic"
    version          = "1.0.0"
    last_updated     = "2026-02-16T00:00:00Z"
    maintainer       = "Application Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/webapp"
    compliance_level = "standard"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  # Extensive customizations
  exclude_files = [
    {
      path   = ".github/workflows/ci.yml"
      reason = "Custom CI with database integration tests"
    },
    {
      path   = ".github/workflows/deploy.yml"
      reason = "Multi-stage deployment with manual approvals"
    },
    {
      path   = "scripts/validate/custom_checks.py"
      reason = "Application-specific validation logic"
    }
  ]

  protected_files = [
    {
      path   = ".gitignore"
      reason = "Project-specific ignore patterns for node_modules, vendor, etc"
    },
    {
      path   = ".editorconfig"
      reason = "Team coding standards different from MokoStandards"
    },
    {
      path   = "README.md"
      reason = "Project-specific documentation with architecture diagrams"
    }
  ]
}
```

### Use Case 4: Emergency Security Update (Force Override)

**Scenario:** Critical security fix needed in all repositories immediately.

**Step 1:** Update the workflow in MokoStandards

**Step 2:** Run force override sync:

1. Navigate to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. **Configuration:**
   - `repos`: (leave empty for all repositories)
   - `exclude`: (only truly incompatible repos)
   - `dry_run`: `false`
   - `force_override`: `true` ✓ (checked)
4. Click **Run workflow**

**Step 3:** Monitor and merge PRs quickly

**Result:** Security fix deployed to all repositories, even those with protected workflows.

---

## Examples

### Minimal Override (Platform Only)

```hcl
# MokoStandards.override.tf - Minimal configuration
locals {
  override_metadata = {
    name             = "Simple Override"
    description      = "Just specify platform type"
    version          = "1.0.0"
    last_updated     = "2026-02-16T00:00:00Z"
    maintainer       = "DevOps"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/simple-repo"
    repository_type  = "terraform"
    compliance_level = "standard"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  exclude_files   = []
  protected_files = []
}
```

### Complete Override (All Options)

```hcl
# MokoStandards.override.tf - Complete configuration
locals {
  override_metadata = {
    name             = "Advanced Repository Override"
    description      = "Comprehensive configuration with all options"
    version          = "2.0.0"
    last_updated     = "2026-02-16T10:00:00Z"
    maintainer       = "DevOps Team"
    schema_version   = "2.0"
    repository_url   = "https://github.com/mokoconsulting-tech/advanced-repo"
    repository_type  = "terraform"
    compliance_level = "strict"
    format           = "terraform"
  }

  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }

  exclude_files = [
    {
      path   = ".github/workflows/custom-ci.yml"
      reason = "Custom CI with integration tests and database setup"
    },
    {
      path   = ".github/workflows/deploy-production.yml"
      reason = "Production deployment requires manual approval process"
    },
    {
      path   = "scripts/deploy.sh"
      reason = "Custom deployment script with environment-specific logic"
    }
  ]

  protected_files = [
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns for build artifacts"
    },
    {
      path   = ".editorconfig"
      reason = "Team-specific editor configuration agreed upon in team meeting"
    },
    {
      path   = "README.md"
      reason = "Custom project documentation with architecture diagrams"
    },
    {
      path   = ".github/CODEOWNERS"
      reason = "Team-specific code ownership and review requirements"
    },
    {
      path   = "scripts/bootstrap.sh"
      reason = "Custom initialization script with environment setup"
    }
  ]

  obsolete_files = [
    {
      path   = "scripts/old_deploy.sh"
      reason = "Replaced by new deployment system in version 2.0"
    },
    {
      path   = ".github/workflows/legacy-ci.yml"
      reason = "Replaced by unified-ci.yml workflow"
    }
  ]
}
```

---

## Best Practices

### 1. Always Specify Repository Type

**DO:**
```hcl
repository_type = "terraform"  # Explicit and fast
```

**DON'T:**
```hcl
# Omitting forces slower auto-detection
```

**Why:** Explicit type is 2-3 seconds faster per sync and more accurate.

### 2. Document All Exclusions and Protections

**DO:**
```hcl
exclude_files = [
  {
    path   = ".github/workflows/deploy.yml"
    reason = "Custom deployment process with manual approval gates and rollback procedures"
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

**Why:** Future maintainers need to understand why files are excluded.

### 3. Start with Conservative Cleanup

**DO:**
```hcl
cleanup_mode = "conservative"  # Safe default
```

**DON'T:**
```hcl
cleanup_mode = "aggressive"  # Risk of deleting custom files
```

**Why:** Conservative mode rarely causes problems; aggressive mode requires expertise.

### 4. Version Your Override File

**DO:**
```hcl
version      = "1.2.0"          # Semantic versioning
last_updated = "2026-02-16T10:30:00Z"  # ISO 8601 format
```

**Update these fields** whenever you modify the configuration.

### 5. Keep Metadata Current

**DO:**
```hcl
maintainer     = "Current DevOps Team"
repository_url = "https://github.com/mokoconsulting-tech/actual-repo-name"
```

**DON'T:**
```hcl
maintainer     = "Unknown"
repository_url = "https://example.com"
```

### 6. Test Changes with Dry Run

Before committing changes to your override file:

```bash
# Test locally with bulk sync script
php scripts/automation/bulk_update_repos.php \
  --dry-run \
  --repos your-repo-name
```

Or trigger workflow with `dry_run: true` in GitHub Actions.

### 7. Use Force Override Sparingly

**DO use for:**
- Emergency security updates
- Critical bug fixes
- Organization-wide policy enforcement

**DON'T use for:**
- Regular monthly syncs
- Testing new features
- Convenience

---

## Troubleshooting

### Problem 1: Override File Not Being Read

**Symptoms:**
- Default sync behavior used
- Platform auto-detection runs despite override
- Excluded files still being synced

**Solutions:**
1. Verify file name is exactly `MokoStandards.override.tf` (case-sensitive)
2. Confirm file is in repository root directory (not subdirectory)
3. Check Terraform syntax: `terraform fmt -check MokoStandards.override.tf`
4. Ensure file has proper read permissions
5. Review bulk sync workflow logs for parse errors

### Problem 2: Files Still Being Overwritten Despite Protection

**Symptoms:**
- Protected files are being modified in sync PR
- Custom changes being lost

**Solutions:**
1. Verify `path` in `protected_files` exactly matches file path from repo root
2. Check if sync was run with `--force-override` flag (overrides protection)
3. Ensure `sync_config.enabled = true`
4. Review sync logs to confirm override was loaded
5. Validate Terraform syntax has no errors

### Problem 3: Platform Detection Still Running

**Symptoms:**
- Logs show "Detecting platform type..." message
- Wrong workflows being synced

**Solutions:**
1. Confirm `repository_type` is set in `override_metadata`
2. Verify `repository_type` is valid value (terraform/dolibarr/joomla/generic)
3. Check that `repository_type` is not set to "standards" (which is ignored for target repos)
4. Ensure override file syntax is correct

### Problem 4: Too Many Files Being Deleted

**Symptoms:**
- Important files removed during sync
- Custom scripts deleted

**Solutions:**
1. Change `cleanup_mode` from "aggressive" to "conservative"
2. Add custom files to `protected_files` list
3. Temporarily set `cleanup_mode = "none"` to diagnose
4. Review deleted files list in sync PR before merging

### Problem 5: Force Override Not Working

**Symptoms:**
- Protected files still not overridden with `--force-override`
- Changes not applied despite force flag

**Solutions:**
1. Verify `--force-override` flag was actually used
2. Check workflow input `force_override` is checked/true
3. Note: Excluded files (`exclude_files`) still won't sync (by design)
4. Review workflow logs to confirm force override mode activated

### Validation Checklist

Before committing your override file:

- [ ] File named exactly `MokoStandards.override.tf`
- [ ] Located in repository root directory
- [ ] Terraform syntax valid (`terraform fmt -check`)
- [ ] `repository_type` specified and valid
- [ ] All `exclude_files` paths correct (from repo root)
- [ ] All `protected_files` paths correct (from repo root)
- [ ] Each exclusion/protection has clear `reason`
- [ ] `version` and `last_updated` fields current
- [ ] Tested with dry-run before committing

---

## Related Documentation

### Essential Reading

- **[Terraform Override Files Guide](guide/terraform-override-files.md)** - Complete reference for override configuration
- **[Bulk Repository Updates](guide/bulk-repository-updates.md)** - Bulk sync script documentation
- **[Bulk Repository Sync Workflow](workflows/bulk-repo-sync.md)** - Workflow architecture and usage

### Related Topics

- **[Platform Detection](guide/platform-detection.md)** - How auto-detection works
- **[Workflow Architecture](workflows/workflow-architecture.md)** - Understanding workflow hierarchy
- **[Standards Compliance](workflows/standards-compliance.md)** - Validation and compliance

### Support Resources

- **[MokoStandards Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)** - Report bugs or request features
- **[Bulk Sync Script Source](../scripts/automation/bulk_update_repos.php)** - Review implementation
- **[Workflow Source](.github/workflows/bulk-repo-sync.yml)** - Review workflow code

---

## Summary

### Key Takeaways

1. **Override files control sync behavior** - Use `MokoStandards.override.tf` to customize
2. **Always specify repository type** - Faster and more accurate than auto-detection
3. **Protect your custom files** - Add to `protected_files` list
4. **Document your choices** - Include clear reasons for exclusions and protections
5. **Use force override carefully** - Only for emergencies and critical updates
6. **Test with dry-run first** - Preview changes before applying
7. **Keep configuration current** - Update version and last_updated fields

### Quick Reference

```hcl
# MokoStandards.override.tf - Template
locals {
  override_metadata = {
    repository_type = "terraform"  # REQUIRED: terraform|dolibarr|joomla|generic
    version = "1.0.0"               # Update when you change config
    last_updated = "2026-02-16"     # Update when you change config
    # ... other metadata ...
  }
  
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"   # none|conservative|aggressive
  }
  
  exclude_files = [/* files NOT to sync */]
  protected_files = [/* files NOT to overwrite */]
  obsolete_files = [/* files TO remove */]
}
```

---

**Last Updated**: 2026-02-16  
**Maintainer**: MokoStandards Team  
**License**: GPL-3.0-or-later

**Next Steps:**
1. Review complete examples above
2. Create override file for your repository
3. Test with dry-run mode
4. Monitor sync PRs and adjust as needed
