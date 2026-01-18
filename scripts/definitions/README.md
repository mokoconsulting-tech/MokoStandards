# Repository Structure Definitions

## Overview

This directory contains repository structure definition files that define the expected file and directory structure for different types of repositories in the MokoStandards ecosystem.

## Definition Files

| File | Type | Description |
|------|------|-------------|
| **default-repository.xml** | Generic | Standard structure for generic repositories |
| **default-repository.json** | Generic | JSON format of default repository structure |
| **waas-component.xml** | Joomla | Structure for Joomla/WaaS components, modules, plugins |
| **crm-module.xml** | Dolibarr | Structure for Dolibarr/CRM modules |
| **generic-repository.xml** | Generic | Alternative generic repository structure |

## Schema Format

Definition files can be in either XML or JSON format:

### XML Format
- Extension: `.xml`
- Schema: `schemas/repository-structure.xsd`
- Namespace: `http://mokoconsulting.com/schemas/repository-structure`

### JSON Format
- Extension: `.json`
- Schema: `schemas/repository-structure.schema.json`
- More lightweight and easier to parse programmatically

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
python3 scripts/validate/validate_structure_v2.py \
  --schema scripts/definitions/default-repository.xml \
  --repo /path/to/repository
```

### With Auto-Detection Script

```bash
# Auto-detect platform and validate
python3 scripts/validate/auto_detect_platform.py \
  --repo-path /path/to/repository
```

The auto-detection script will:
1. Detect the repository type (Joomla, Dolibarr, or Generic)
2. Load the appropriate definition from `scripts/definitions/`
3. Validate the repository structure
4. Generate validation reports

### With Stub Generation Script

```bash
# Generate missing files based on definition
python3 scripts/validate/generate_stubs.py \
  scripts/definitions/default-repository.xml \
  /path/to/repository
```

## Creating Custom Definitions

To create a custom repository structure definition:

1. **Copy Template**:
   ```bash
   cp templates/schemas/template-repository-structure.xml \
      scripts/definitions/my-custom-structure.xml
   ```

2. **Edit Definition**:
   - Update metadata (name, description, type)
   - Define root files with source/destination
   - Define directory structure
   - Add validation rules
   - Specify repository requirements

3. **Validate Definition**:
   ```bash
   xmllint --schema schemas/repository-structure.xsd \
           scripts/definitions/my-custom-structure.xml
   ```

4. **Test Definition**:
   ```bash
   python3 scripts/validate/validate_structure_v2.py \
     --schema scripts/definitions/my-custom-structure.xml \
     --repo /test/repository
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

**Location**: `scripts/definitions/`  
**Last Updated**: 2026-01-18  
**Maintained By**: MokoStandards Team

## Changelog

### 2026-01-18
- **Security Enhancement**: Added `scripts/requirements.txt` to all repository structure definitions
- Added defusedxml>=0.7.1 requirement for safe XML parsing (prevents XXE attacks)
- Updated all schema definition timestamps
- Enhanced security documentation for Python script dependencies
- All definitions now include stub content for requirements.txt with security notes
