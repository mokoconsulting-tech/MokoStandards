# Repository Structure Definitions

## Overview

This directory contains repository structure definition files that define the expected file and directory structure for different types of repositories in the MokoStandards ecosystem.

## Definition Files

| File | Type | Description |
|------|------|-------------|
| **default-repository.tf** | Generic | Standard structure for generic repositories |
| **default-repository.json** | Generic | JSON format of default repository structure |
| **waas-component.tf** | Joomla | Structure for Joomla/WaaS components, modules, plugins |
| **crm-module.tf** | Dolibarr | Structure for Dolibarr/CRM modules |
| **generic-repository.tf** | Generic | Alternative generic repository structure |

## Schema Format

Definition files use Terraform HCL (HashiCorp Configuration Language) format with `.tf` extension:

### Terraform HCL Format (Standard)
- Extension: `.tf`
- Syntax: HashiCorp Configuration Language (HCL)
- Structure: Uses `locals` blocks with nested maps and lists
- Consistent with `.github/config.tf` and other infrastructure-as-code files
- Native to Terraform ecosystem

**Example Structure:**
```hcl
locals {
  repository_structure = {
    metadata = {
      name             = "Repository Name"
      description      = "Description"
      repository_type  = "type"
      platform         = "platform"
      last_updated     = "2026-01-01T00:00:00Z"
      maintainer       = "Maintainer"
    }
    root_files = [
      {
        name        = "README.md"
        extension   = "md"
        description = "Project documentation"
        required    = true
        audience    = "general"
      }
    ]
    directories = [
      {
        name       = "src"
        path       = "src"
        required   = true
        purpose    = "Source code"
      }
    ]
  }
}
```

### JSON Format (Alternative)
- Extension: `.json`
- Schema: `schemas/repository-structure.schema.json`
- Lightweight alternative for programmatic parsing
- Example: `default-repository.json`

## Structure

Each definition file includes:

1. **Metadata**: Name, description, repository type, platform, maintainer
2. **Root Files**: Files expected at repository root
3. **Directories**: Directory structure with nested files and subdirectories
4. **Requirements**: Requirement status (required, suggested, optional, not-allowed)
5. **Templates**: Source and destination paths for file generation
6. **Validation Rules**: Custom validation rules for files and directories
7. **Repository Requirements**: Variables, secrets, branch protections, etc.

## Usage

### With Validation Script

```bash
# Validate repository against definition
php api/validate/auto_detect_platform.php \
  --repo-path /path/to/repository \
  --schema-dir api/definitions
```

### Programmatic Access

The definition files can be parsed using Terraform or HCL parsing libraries:

**Terraform:**
```bash
terraform console < api/definitions/default-repository.tf
```

**Python (using python-hcl2):**
```python
import hcl2
with open('api/definitions/default-repository.tf', 'r') as f:
    data = hcl2.load(f)
    metadata = data['locals'][0]['repository_structure']['metadata']
```

**JavaScript/Node.js (using hcl-parser):**
```javascript
const hcl = require('hcl-parser');
const fs = require('fs');
const content = fs.readFileSync('api/definitions/default-repository.tf', 'utf-8');
const parsed = hcl.parse(content);
const metadata = parsed.locals.repository_structure.metadata;
```

### With Auto-Detection Script

```bash
# Auto-detect platform and validate
php api/validate/auto_detect_platform.php \
  --repo-path /path/to/repository
```

The auto-detection script will:
1. Detect the repository type (Joomla, Dolibarr, or Generic)
2. Load the appropriate definition from `api/definitions/`
3. Validate the repository structure
4. Generate validation reports

## Creating Custom Definitions

To create a custom repository structure definition:

1. **Copy Template**:
   ```bash
   cp api/definitions/generic-repository.tf \
      api/definitions/my-custom-structure.tf
   ```

2. **Edit Definition**:
   - Update metadata (name, description, type, platform)
   - Define root_files array with required files
   - Define directories array with nested structure
   - Add validation rules and repository requirements as needed
   - Use proper HCL syntax with snake_case naming

3. **Validate Syntax**:
   ```bash
   # Using Terraform (if installed)
   terraform fmt -check api/definitions/my-custom-structure.tf
   
   # Or use an HCL linter
   hclfmt api/definitions/my-custom-structure.tf
   ```

4. **Test Definition**:
   ```bash
   php api/validate/auto_detect_platform.php \
     --repo-path /test/repository \
     --schema-dir api/definitions \
     --platform my-custom-type
   ```

## Schema Structure

Each definition file uses a consistent HCL structure:

```hcl
locals {
  repository_structure = {
    # Basic information about the repository type
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
    
    # Files expected at repository root
    root_files = [
      {
        name              = "filename.ext"
        extension         = "ext"
        description       = "File description"
        required          = true|false
        requirement_status = "required|suggested|optional"
        always_overwrite  = true|false
        audience          = "general|developer|contributor"
        template          = "path/to/template"
      }
    ]
    
    # Directory structure with nested files
    directories = [
      {
        name                = "dirname"
        path                = "path/to/dir"
        description         = "Directory description"
        required            = true|false
        requirement_status  = "required|suggested|optional"
        purpose             = "Purpose description"
        
        files = [
          { /* file definition */ }
        ]
        
        subdirectories = [
          { /* nested directory definition */ }
        ]
      }
    ]
    
    # Repository-level requirements (optional)
    repository_requirements = {
      secrets = [
        { name = "SECRET_NAME", description = "Description", required = true }
      ]
      variables = [
        { name = "VAR_NAME", description = "Description", required = true }
      ]
      branch_protections = {
        /* protection rules */
      }
      repository_settings = {
        /* settings */
      }
    }
  }
}
```

## Definition Examples

### Minimal Definition

```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository-structure version="1.0" schema-version="1.0">
  <metadata>
    <name>Minimal Repository</name>
    <description>Minimal repository structure</description>
    <repository-type>library</repository-type>
    <platform>multi-platform</platform>
    <last-updated>2026-01-16T00:00:00Z</last-updated>
    <maintainer>MokoStandards Team</maintainer>
  </metadata>

  <structure>
    <root-files>
      <file extension="md">
        <name>README.md</name>
        <description>Project documentation</description>
        <requirement-status>required</requirement-status>
      </file>
    </root-files>

    <directories>
      <directory path="src">
        <name>src</name>
        <description>Source code</description>
        <requirement-status>required</requirement-status>
      </directory>
    </directories>
  </structure>
</repository-structure>
```

### With Source/Destination

```xml
<file extension="yml">
  <name>ci.yml</name>
  <description>CI workflow</description>
  <requirement-status>suggested</requirement-status>

  <source>
    <path>templates/workflows/generic</path>
    <filename>ci.yml.template</filename>
    <type>template</type>
  </source>

  <destination>
    <path>.github/workflows</path>
    <filename>ci.yml</filename>
    <create-path>true</create-path>
  </destination>
</file>
```

### With Stub Content

```xml
<file extension="md">
  <name>ARCHITECTURE.md</name>
  <description>Architecture documentation</description>
  <requirement-status>optional</requirement-status>

  <destination>
    <path>docs</path>
    <filename>ARCHITECTURE.md</filename>
    <create-path>true</create-path>
  </destination>

  <stub-content><![CDATA[
# Architecture

## Overview

TODO: Describe system architecture

## Components

TODO: List major components
]]></stub-content>
</file>
```

## Platform-Specific Definitions

### Joomla/WaaS (waas-component.xml)

Structure for Joomla extensions:
- Manifest file validation
- Admin and site directories
- Language files structure
- SQL installation scripts
- Joomla-specific workflows

### Dolibarr/CRM (crm-module.xml)

Structure for Dolibarr modules:
- Module descriptor validation
- Core/modules directory structure
- Language files (langs/)
- SQL table definitions
- Dolibarr-specific workflows

### Generic (default-repository.xml)

Standard structure for:
- Multi-language projects
- Libraries and packages
- Applications
- Documentation projects

## Validation Levels

| Level | Meaning | Impact |
|-------|---------|--------|
| **required** | MUST be present | Blocks deployment if missing |
| **suggested** | SHOULD be present | Warning if missing, reduces health score |
| **optional** | MAY be present | No validation, informational only |
| **not-allowed** | MUST NOT be present | Error if present (e.g., node_modules) |

## Repository Requirements (NEW)

Definitions can now include repository-level requirements:

- **Variables**: Required environment variables
- **Secrets**: Required GitHub secrets
- **Branch Protections**: Branch protection rules
- **Settings**: Repository settings (issues enabled, wiki, etc.)
- **Labels**: Required issue/PR labels
- **Webhooks**: Required webhook configurations

See [Schema Guide](../../docs/schemas/repohealth/schema-guide.md) for complete documentation.

## Documentation

- [Schema Guide](../../docs/schemas/repohealth/schema-guide.md) - Complete schema specification
- [Repository Structure Schema](../../docs/schemas/repohealth/repository-structure-schema.md) - Detailed schema documentation
- [Validation Guide](../../docs/guide/validation/auto-detection.md) - Platform detection and validation

## Maintenance

### Updating Definitions

1. Edit definition file
2. Validate against XSD/JSON schema
3. Test with validation script
4. Update CHANGELOG.md
5. Commit changes

### Version Control

- Definition files are versioned through git
- Breaking changes require major version bump
- Schema version tracked in definition metadata

---

**Location**: `api/definitions/`
**Last Updated**: 2026-01-16
**Maintained By**: MokoStandards Team
