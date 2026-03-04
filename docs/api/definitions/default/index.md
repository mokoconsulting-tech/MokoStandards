# Default Repository Definitions

## Overview

This directory contains base platform-specific definition files that serve as templates for repository validation and structure. These definitions are used as the foundation for generating repository-specific definitions during bulk sync operations.

## Definition Files

| File | Platform | Description |
|------|----------|-------------|
| **crm-module.tf** | Dolibarr | Structure for Dolibarr/CRM modules with core/modules structure, language files, SQL tables |
| **default-repository.json** | Generic | JSON format of default repository structure (legacy format) |
| **default-repository.tf** | Generic | Standard structure for generic repositories, libraries, and multi-language projects |
| **generic-repository.tf** | Generic | Alternative generic repository structure with minimal requirements |
| **standards-repository.tf** | Standards | Structure for MokoStandards organizational repository with api/, templates/, docs/, logs/ |
| **waas-component.tf** | Joomla | Structure for Joomla/WaaS components, modules, plugins with manifest validation |

## File Format

All definition files use Terraform HCL (HashiCorp Configuration Language) format with `.tf` extension:

```hcl
locals {
  repository_structure = {
    metadata = {
      name             = "Repository Type Name"
      description      = "Detailed description"
      repository_type  = "type-identifier"
      platform         = "platform-name"
      last_updated     = "ISO8601-timestamp"
      maintainer       = "Maintainer Name"
      version          = "1.0"
      schema_version   = "1.0"
    }
    
    root_files = [
      {
        name              = "filename.ext"
        extension         = "ext"
        description       = "File description"
        required          = true
        audience          = "general"
      }
    ]
    
    directories = [
      {
        name        = "dirname"
        path        = "path/to/dir"
        description = "Directory description"
        required    = true
        purpose     = "Purpose description"
        
        files = [ /* nested files */ ]
        subdirectories = [ /* nested directories */ ]
      }
    ]
    
    repository_requirements = {
      secrets = [ /* required secrets */ ]
      variables = [ /* required variables */ ]
      branch_protections = { /* protection rules */ }
      repository_settings = { /* settings */ }
    }
  }
}
```

## Usage

### Platform Detection

These definitions are automatically selected during platform detection:

```bash
# Auto-detect platform and load appropriate definition
php api/validate/auto_detect_platform.php \
  --repo-path /path/to/repository \
  --schema-dir api/definitions/default
```

The detection script will:
1. Analyze repository structure and content
2. Score each platform based on indicators
3. Select the best-matching definition
4. Validate repository against the definition

### Manual Selection

You can manually specify which definition to use:

```bash
# Use specific definition
php api/validate/auto_detect_platform.php \
  --repo-path /path/to/repository \
  --platform dolibarr
```

This will load `api/definitions/default/crm-module.tf`.

### During Bulk Sync

When bulk sync runs, it:
1. Detects the repository platform
2. Loads the corresponding base definition from this directory
3. Customizes it with repository-specific metadata
4. Saves to `api/definitions/sync/{repo}.def.tf`

## Platform Mapping

The auto-detection script maps platforms to definition files:

| Platform | Definition File |
|----------|----------------|
| `joomla` | waas-component.tf |
| `dolibarr` | crm-module.tf |
| `nodejs` | nodejs-repository.tf (future) |
| `python` | python-repository.tf (future) |
| `terraform` | terraform-repository.tf (future) |
| `standards` | standards-repository.tf |
| `generic` | default-repository.tf |

## Creating New Definitions

To create a new platform definition:

1. **Copy an existing definition as template:**
   ```bash
   cp api/definitions/default/default-repository.tf \
      api/definitions/default/myplatform-repository.tf
   ```

2. **Update metadata:**
   - Change `name`, `description`, `repository_type`, `platform`
   - Update `last_updated` timestamp
   - Set appropriate `version` and `schema_version`

3. **Define structure:**
   - Update `root_files` array with platform-specific files
   - Define `directories` with nested structure
   - Add platform-specific validation rules
   - Specify repository requirements (secrets, variables, etc.)

4. **Update platform detection:**
   Add mapping in `api/validate/auto_detect_platform.php`:
   ```php
   'myplatform' => 'myplatform-repository.tf',
   ```

5. **Add detection logic:**
   Update detection scoring to recognize your platform based on:
   - File patterns (e.g., `composer.json`, `package.json`)
   - Directory structure
   - Repository topics
   - Naming conventions

6. **Validate syntax:**
   ```bash
   # Using Terraform (if installed)
   terraform fmt -check api/definitions/default/myplatform-repository.tf
   ```

7. **Test definition:**
   ```bash
   php api/validate/auto_detect_platform.php \
     --repo-path /test/repository \
     --platform myplatform
   ```

## Validation Levels

Definitions support multiple requirement levels:

| Level | Meaning | Impact |
|-------|---------|--------|
| **required** | MUST be present | Blocks deployment if missing |
| **suggested** | SHOULD be present | Warning if missing, reduces health score |
| **optional** | MAY be present | No validation, informational only |
| **not-allowed** | MUST NOT be present | Error if present (e.g., node_modules) |

## Maintenance

### Updating Definitions

1. Edit the definition file
2. Update `last_updated` timestamp
3. Increment `version` if breaking changes
4. Test with validation script
5. Update CHANGELOG.md
6. Commit changes

### Version Control

- Definition files are versioned through git
- Breaking changes require major version bump
- Schema version tracked in definition metadata
- Maintain backward compatibility when possible

## Related Documentation

- [Synced Definitions](../sync/index.md) - Auto-generated repository definitions
- [Schema Guide](../../../docs/schemas/repohealth/schema-guide.md) - Complete schema specification
- [Validation Guide](../../../docs/guide/validation/auto-detection.md) - Platform detection and validation
- [Main Definitions README](../README.md) - Overview of definitions structure

---

**Location**: `api/definitions/default/`  
**Purpose**: Base platform-specific repository definitions  
**Used By**: Auto-detection, validation, bulk sync  
**Last Updated**: 2026-03-03  
**Maintained By**: MokoStandards Team
