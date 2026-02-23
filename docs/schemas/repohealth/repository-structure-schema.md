# Repository Structure Schema System

## Overview

The Repository Structure Schema System provides a standardized way to define, validate, and generate repository structures across Moko Consulting projects. It uses XML schemas to define the expected file and folder hierarchy, along with validation rules and stub generation capabilities.

## Table of Contents

1. [Components](#components)
2. [XML Schema Definition](#xml-schema-definition)
3. [Structure Definitions](#structure-definitions)
4. [Validation Tool](#validation-tool)
5. [Stub Generation Tool](#stub-generation-tool)
6. [Usage Examples](#usage-examples)
7. [Best Practices](#best-practices)
8. [Creating Custom Structures](#creating-custom-structures)

## Components

The system consists of the following components:

### 1. XML Schema (XSD)
- **File**: `schemas/repository-structure.xsd`
- **Purpose**: Defines the structure and validation rules for repository structure XML files
- **Namespace**: `http://mokoconsulting.com/schemas/repository-structure`

### 2. Structure Definitions (XML)
- **Location**: `scripts/definitions/`
- **Purpose**: Define specific repository structures (e.g., CRM modules, WaaS components)
- **Examples**:
  - `crm-module.xml` - MokoCRM (Dolibarr) module structure
  - `waas-component.xml` - MokoWaaS (Joomla) component structure

### 3. Validation Tool

Repository structure validation is handled through:
1. **Web Interface**: Material Design 3 dashboard at `public/index.php`
2. **Manual Validation**: Using the XML/JSON schema definitions as reference
3. **CI/CD Integration**: GitHub Actions workflows for automated checks

### 4. Stub Generation Tool

**Current Approach**:
- Use XML/JSON schema as structural reference
- Manual file creation following schema guidelines
- Web-based repository management tools

## XML Schema Definition

### Root Element

```xml
<repository-structure version="1.0" schema-version="1.0">
  <metadata>...</metadata>
  <structure>...</structure>
</repository-structure>
```

### Metadata Section

Describes the repository structure:

```xml
<metadata>
  <name>MokoCRM Module</name>
  <description>Standard repository structure for MokoCRM modules</description>
  <repository-type>crm-module</repository-type>
  <platform>mokokrm</platform>
  <last-updated>2026-01-07T00:00:00Z</last-updated>
  <maintainer>Moko Consulting</maintainer>
</metadata>
```

#### Repository Types
- `standards` - MokoStandards repository
- `waas-component` - Joomla component
- `waas-module` - Joomla module
- `waas-plugin` - Joomla plugin
- `waas-template` - Joomla site template
- `waas-library` - Joomla library
- `waas-package` - Joomla package
- `crm-module` - Dolibarr module
- `crm-plugin` - Dolibarr plugin
- `application` - Standalone application
- `library` - Standalone library

#### Platforms
- `mokowaas` - MokoWaaS (Joomla-based)
- `mokokrm` - MokoCRM (Dolibarr-based)
- `standards` - MokoStandards repository
- `multi-platform` - Cross-platform

### Structure Section

Defines the actual file and folder hierarchy:

```xml
<structure>
  <root-files>
    <file>...</file>
  </root-files>
  <directories>
    <directory>...</directory>
  </directories>
</structure>
```

### File Definition

```xml
<file extension="md">
  <name>README.md</name>
  <description>Developer-focused documentation</description>
  <required>true</required>
  <audience>developer</audience>
  <stub-content><![CDATA[
    # Content here
  ]]></stub-content>
  <validation-rules>
    <rule>...</rule>
  </validation-rules>
</file>
```

#### File Attributes
- `extension` - File extension (optional)

#### File Elements
- `name` - File name (required)
- `description` - Human-readable description
- `required` - Boolean, whether file must exist
- `audience` - Target audience (developer, end-user, administrator, contributor, general)
- `template` - Path to template file
- `stub-content` - Content to use when generating stub (use CDATA for multiline)
- `validation-rules` - Validation rules to apply

### Directory Definition

```xml
<directory path="src">
  <name>src</name>
  <description>Source code directory</description>
  <required>true</required>
  <purpose>Contains deployable module code</purpose>
  <files>
    <file>...</file>
  </files>
  <subdirectories>
    <directory>...</directory>
  </subdirectories>
  <validation-rules>
    <rule>...</rule>
  </validation-rules>
</directory>
```

#### Directory Attributes
- `path` - Path relative to parent (defaults to name if not specified)

#### Directory Elements
- `name` - Directory name (required)
- `description` - Human-readable description
- `required` - Boolean, whether directory must exist
- `purpose` - Explanation of directory's role
- `files` - Files contained in this directory
- `subdirectories` - Subdirectories
- `validation-rules` - Validation rules to apply

### Validation Rules

```xml
<validation-rules>
  <rule>
    <type>naming-convention</type>
    <description>Must follow PascalCase naming</description>
    <pattern>^[A-Z][a-zA-Z0-9]*$</pattern>
    <severity>error</severity>
  </rule>
</validation-rules>
```

#### Rule Types
- `naming-convention` - Validate name against regex pattern
- `content-pattern` - Validate file content against regex pattern
- `file-exists` - Check if file exists
- `directory-exists` - Check if directory exists
- `min-size` - Minimum file size in bytes
- `max-size` - Maximum file size in bytes
- `header-required` - Require file header comment
- `license-required` - Require license header
- `custom` - Custom validation logic

#### Severity Levels
- `error` - Must be fixed
- `warning` - Should be fixed
- `info` - Informational only

## Structure Definitions

### MokoCRM Module Structure

**File**: `scripts/definitions/crm-module.xml`

Defines the standard structure for MokoCRM (Dolibarr) modules with special emphasis on the dual-README requirement:

- **Root README.md**: For developers (setup, building, testing, contributing)
- **src/README.md**: For end users (installation, configuration, usage)

Key directories:
- `src/` - Deployable module code
- `docs/` - Developer documentation
- `scripts/` - Build and maintenance scripts
- `tests/` - Test files
- `templates/` - Code generation templates
- `.github/` - GitHub configuration

### MokoWaaS Component Structure

**File**: `scripts/definitions/waas-component.xml` (to be created)

Defines the standard structure for MokoWaaS (Joomla) components.

## Validation Tool

**Note**: Validation scripts are deprecated as of v04.00.01. This section is maintained for historical reference.

### Historical Usage (v03.xx.xx and earlier)

```bash
# These commands are no longer supported in v04.00.01+
# Validate current directory
# python scripts/validate/validate_structure.py scripts/definitions/crm-module.xml

# Validate specific directory
# python scripts/validate/validate_structure.py scripts/definitions/crm-module.xml /path/to/repo

# Use with make (from project root)
# make validate-structure
```

### Current Approach (v04.00.01+)

Repository structure validation is now performed through:
1. **Manual Review**: Compare your repository against XML schema definitions in `schemas/`
2. **Web Interface**: Use Material Design 3 dashboard at `public/index.php` for repository management
3. **CI/CD**: Implement custom validation in GitHub Actions workflows

### Output

**Historical Reference**: The deprecated validation tool (v03.xx.xx) provided:

1. **Metadata Display**: Shows structure being validated against
2. **Validation Results**: Categorized by severity
   - ❌ Errors: Must be fixed
   - ⚠️ Warnings: Should be fixed
   - ℹ️ Info: Optional items
3. **Summary**: Count of issues by type
4. **Exit Code**: 0 if passed, 1 if errors found

### Example Output

```
Validating repository: /path/to/repo
Against structure: scripts/definitions/crm-module.xml
--------------------------------------------------------------------------------
Structure: MokoCRM Module
Description: Standard repository structure for MokoCRM (Dolibarr) modules
Type: crm-module
Platform: mokokrm
--------------------------------------------------------------------------------

================================================================================
VALIDATION RESULTS
================================================================================

❌ ERRORS (2):
--------------------------------------------------------------------------------
  README.md
    Required file missing: README.md
    Rule: file-exists

  src/README.md
    Required file missing: README.md
    Rule: file-exists

⚠️  WARNINGS (1):
--------------------------------------------------------------------------------
  CONTRIBUTING.md
    Content pattern not found: Must include contribution guidelines
    Rule: content-pattern

ℹ️  INFO (3):
--------------------------------------------------------------------------------
  templates
    Optional directory missing: templates

================================================================================
SUMMARY
================================================================================
Total issues: 6
  Errors:   2
  Warnings: 1
  Info:     3

❌ Validation FAILED - please fix errors
```

## Stub Generation Tool

**Note**: Stub generation scripts are deprecated as of v04.00.01. This section is maintained for historical reference.

### Historical Usage (v03.xx.xx and earlier)

```bash
# These commands are no longer supported in v04.00.01+
# Dry run (preview)
# python scripts/validate/generate_stubs.py scripts/definitions/crm-module.xml --dry-run

# Generate stubs in current directory
# python scripts/validate/generate_stubs.py scripts/definitions/crm-module.xml

# Generate stubs in specific directory
# python scripts/validate/generate_stubs.py scripts/definitions/crm-module.xml /path/to/repo

# Force overwrite existing files
# python scripts/validate/generate_stubs.py scripts/definitions/crm-module.xml --force

# Use with make (from project root)
# make generate-stubs STRUCTURE=crm-module
```

### Current Approach (v04.00.01+)

Repository structure setup is now performed through:
1. **Manual Creation**: Create files/directories based on XML schema definitions
2. **Template Copying**: Copy template files from `templates/` directory manually
3. **Web Interface**: Use Material Design 3 dashboard for repository initialization

### Features (Historical - v03.xx.xx)

The deprecated stub generation tool offered:

1. **Dry Run Mode**: Preview what would be created
2. **Force Mode**: Overwrite existing files
3. **Template Substitution**: Replace placeholders in stub content
4. **Smart Defaults**: Generate sensible default content for files without stub-content
5. **Directory Creation**: Automatically create parent directories

### Template Placeholders

Available placeholders for use in `stub-content`:

- `{MODULE_NAME}` - Name from metadata
- `{MODULE_DESCRIPTION}` - Description from metadata
- `{REPOSITORY_TYPE}` - Repository type from metadata
- `{PLATFORM}` - Platform from metadata
- `{VERSION}` - Default: "1.0.0"
- `{SUPPORT_EMAIL}` - Default: "support@mokoconsulting.com"
- `{USAGE_INSTRUCTIONS}` - Default instruction text

### Example Output

```
=== STUB GENERATION ===
Repository: /path/to/repo
Structure: scripts/definitions/crm-module.xml
Force overwrite: False
--------------------------------------------------------------------------------

Structure Metadata:
  name: MokoCRM Module
  description: Standard repository structure for MokoCRM modules
  repository-type: crm-module
  platform: mokokrm
--------------------------------------------------------------------------------

✓ Created file: README.md
✓ Created directory: src
✓ Created file: src/README.md
✓ Created directory: docs
✓ Created file: docs/index.md
✓ Created directory: scripts
✓ Created directory: tests
✓ Created directory: tests/unit

================================================================================
SUMMARY
================================================================================
Total actions: 12
  Directories created: 5
  Files created: 7
  Skipped (already exists): 0

✅ Stub generation complete!

Next steps:
  1. Review generated files and update TODO sections
  2. Run validation: Manual review against XML schema (v04.00.01+)
  3. Commit changes to version control
```

## Usage Examples

**Note**: Examples below reference deprecated Python scripts (v03.xx.xx). As of v04.00.01, use manual file creation or web interface.

### Example 1: Create a New MokoCRM Module (Historical)

```bash
# Historical commands (v03.xx.xx) - No longer supported in v04.00.01+
# 1. Create new directory
# mkdir my-new-module
# cd my-new-module

# 2. Generate structure stubs
# python ../MokoStandards/scripts/validate/generate_stubs.py \
#     ../MokoStandards/scripts/definitions/crm-module.xml

# 3. Review generated files
# ls -la

# 4. Update TODOs in generated files
# Edit README.md, src/README.md, etc.

# 5. Validate structure
# python ../MokoStandards/scripts/validate/validate_structure.py \
#     ../MokoStandards/scripts/definitions/crm-module.xml

# 6. Initialize git and commit
# git init
# git add .
# git commit -m "Initial commit with standard structure"
```

**Current Approach (v04.00.01+)**:
1. Create directory structure manually based on XML schema
2. Copy template files from `templates/` directory
3. Initialize Git repository
4. Use web interface for additional setup

### Example 2: Validate Existing Repository (Historical)

```bash
# Historical validation (v03.xx.xx) - No longer supported
# Validate against CRM module structure
# cd existing-module
# python ../MokoStandards/scripts/validate/validate_structure.py \
#     ../MokoStandards/scripts/definitions/crm-module.xml

# Fix any errors reported

# Validate again
# python ../MokoStandards/scripts/validate/validate_structure.py \
#     ../MokoStandards/scripts/definitions/crm-module.xml
```

**Current Approach (v04.00.01+)**:
1. Manually compare repository against XML schema in `schemas/`
2. Use web interface for health checks
3. Implement custom validation in CI/CD if needed

### Example 3: Generate Missing Files Only (Historical)

```bash
# Historical approach (v03.xx.xx) - No longer supported
# Generate stubs without overwriting existing files
# cd partially-complete-module
# python ../MokoStandards/scripts/validate/generate_stubs.py \
#     ../MokoStandards/scripts/definitions/crm-module.xml

# This will create only missing files
# Existing files will be skipped
```

**Current Approach (v04.00.01+)**:
1. Manually identify missing files from XML schema
2. Create files using templates from `templates/` directory
3. Follow structure guidelines from schema documentation

### Example 4: CI/CD Integration (Updated for v04.00.01)

```yaml
# .github/workflows/validate-structure.yml
name: Validate Repository Structure

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Checkout MokoStandards
        uses: actions/checkout@v3
        with:
          repository: mokoconsulting-tech/MokoStandards
          path: MokoStandards

      # Note: Python validation scripts no longer available in v04.00.01+
      # Implement custom validation logic here or use web interface
      
      - name: Check Required Files
        run: |
          # Custom validation logic
          if [ ! -f "README.md" ]; then
            echo "ERROR: README.md is required"
            exit 1
          fi
          if [ ! -f "LICENSE" ]; then
            echo "ERROR: LICENSE is required"
            exit 1
          fi
          echo "Basic structure validation passed"
```

## Best Practices

### 1. Use Dual READMEs for MokoCRM Modules

- **Root README.md**: Developer audience
  - Setup instructions
  - Build commands
  - Testing procedures
  - Contribution guidelines

- **src/README.md**: End-user audience
  - Installation steps
  - Configuration options
  - Usage instructions
  - Support contact

### 2. Keep Structure Definitions Updated

- Update XML when project structure changes
- Version control structure XMLs
- Document changes in CHANGELOG

### 3. Run Validation in CI/CD

- Add structure validation to PR checks
- Fail builds on validation errors
- Report warnings for review

### 4. Use Stub Generation for New Projects

- Start with stubs for consistency
- Customize generated content
- Keep placeholders for team reference

### 5. Define Clear Validation Rules

- Use appropriate severity levels
- Provide helpful error messages
- Document custom validation logic

### 6. Organize Structure Files

```
schemas/
├── repository-structure.xsd    # XSD schema
└── structures/
    ├── crm-module.xml          # CRM module structure
    ├── waas-component.xml      # WaaS component structure
    ├── waas-module.xml         # WaaS module structure
    └── standards.xml           # Standards repository structure
```

## Creating Custom Structures

### Step 1: Create XML Definition

Create a new XML file in `scripts/definitions/`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository-structure xmlns="http://mokoconsulting.com/schemas/repository-structure"
                      version="1.0"
                      schema-version="1.0">
  <metadata>
    <name>My Custom Structure</name>
    <description>Description of this structure</description>
    <repository-type>custom-type</repository-type>
    <platform>mokowaas</platform>
    <last-updated>2026-01-07T00:00:00Z</last-updated>
    <maintainer>Your Name</maintainer>
  </metadata>

  <structure>
    <!-- Define your structure here -->
[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

  </structure>
</repository-structure>
```

### Step 2: Define Root Files

```xml
<root-files>
  <file extension="md">
    <name>README.md</name>
    <description>Project documentation</description>
    <required>true</required>
    <audience>developer</audience>
    <stub-content><![CDATA[
# {MODULE_NAME}

{MODULE_DESCRIPTION}

## Getting Started

TODO: Add getting started instructions
    ]]></stub-content>
  </file>
</root-files>
```

### Step 3: Define Directory Structure

```xml
<directories>
  <directory path="src">
    <name>src</name>
    <description>Source code</description>
    <required>true</required>
    <purpose>Contains all source code files</purpose>

    <files>
      <file extension="php">
        <name>index.php</name>
        <description>Entry point</description>
        <required>true</required>
      </file>
    </files>
  </directory>
</directories>
```

### Step 4: Add Validation Rules

```xml
<validation-rules>
  <rule>
    <type>naming-convention</type>
    <description>Files must use lowercase with hyphens</description>
    <pattern>^[a-z][a-z0-9-]*\.(php|js|css)$</pattern>
    <severity>warning</severity>
  </rule>
</validation-rules>
```

### Step 5: Test Your Structure

```bash
# Validate the XML against the XSD schema
xmllint --noout --schema schemas/repository-structure.xsd \
    scripts/definitions/your-structure.xml

# Note: Stub generation and validation scripts deprecated in v04.00.01+
# Test stub generation (Historical - v03.xx.xx)
# python scripts/validate/generate_stubs.py \
#     scripts/definitions/your-structure.xml \
#     /tmp/test-repo --dry-run

# Test validation (Historical - v03.xx.xx)
# python scripts/validate/validate_structure.py \
#     scripts/definitions/your-structure.xml \
#     /tmp/test-repo
```

**Current Approach (v04.00.01+)**:
1. Validate XML syntax with xmllint
2. Manually test structure creation
3. Use web interface for validation

### Step 6: Document Your Structure

Add documentation to `docs/policy/` or `docs/guide/` explaining:
- Purpose of the structure
- When to use it
- Special considerations
- Examples

## Integration with MokoStandards

### Makefile Integration (Historical - v03.xx.xx)

**Note**: These commands referenced deprecated Python scripts. Shown for historical reference only.

```makefile
# Historical Makefile targets (v03.xx.xx) - No longer functional in v04.00.01+
# MOKOSTANDARDS_ROOT ?= ../MokoStandards
# STRUCTURE_TYPE ?= crm-module

# .PHONY: validate-structure
# validate-structure:
# 	python $(MOKOSTANDARDS_ROOT)/scripts/validate/validate_structure.py \
# 		$(MOKOSTANDARDS_ROOT)/scripts/definitions/$(STRUCTURE_TYPE).xml .

# .PHONY: generate-stubs
# generate-stubs:
# 	python $(MOKOSTANDARDS_ROOT)/scripts/validate/generate_stubs.py \
# 		$(MOKOSTANDARDS_ROOT)/scripts/definitions/$(STRUCTURE_TYPE).xml .

# .PHONY: validate-structure-dry
# validate-structure-dry:
# 	python $(MOKOSTANDARDS_ROOT)/scripts/validate/generate_stubs.py \
# 		$(MOKOSTANDARDS_ROOT)/scripts/definitions/$(STRUCTURE_TYPE).xml . --dry-run
```

**Current Approach (v04.00.01+)**:
Create custom Makefile targets for your specific validation needs or use web interface.

### GitHub Actions Workflow (Updated for v04.00.01)

`.github/workflows/validate.yml`:

```yaml
name: Validate Structure

on:
  pull_request:
    branches: [main, dev]
  push:
    branches: [main, dev]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Checkout MokoStandards
        uses: actions/checkout@v3
        with:
          repository: mokoconsulting-tech/MokoStandards
          path: .mokostandards
          token: ${{ secrets.GITHUB_TOKEN }}

      # Note: Python validation scripts removed in v04.00.01+
      # Implement custom validation or use web interface
      
      - name: Basic Structure Validation
        run: |
          # Custom validation logic
          echo "Checking required files..."
          test -f README.md || (echo "ERROR: README.md missing" && exit 1)
          test -f LICENSE || (echo "ERROR: LICENSE missing" && exit 1)
          echo "Structure validation passed"
```

## Troubleshooting

### Common Issues

**Issue**: XML parsing error
```
Error parsing XML structure: mismatched tag
```
**Solution**: Check XML syntax, ensure all tags are properly closed, use CDATA for content with special characters

**Issue**: Namespace errors
```
Error: Element not found in namespace
```
**Solution**: Ensure XML file includes correct namespace declaration

**Issue**: Validation always passes even with missing files
```
✅ Validation PASSED
```
**Solution**: Check that `<required>true</required>` is set for mandatory files

**Issue**: Stub generation creates empty files
```
Created file but it's empty
```
**Solution**: Add `<stub-content>` with CDATA section or let tool generate defaults

### Debug Mode (Historical - v03.xx.xx)

**Note**: This section refers to deprecated Python scripts.

For historical reference, debugging was done by modifying the Python scripts:

```python
# Historical debugging approach (v03.xx.xx)
# Add to validator script
# print(f"DEBUG: Checking file: {file_path}")
# print(f"DEBUG: Required: {is_required}")
# print(f"DEBUG: Exists: {file_path.exists()}")
```

**Current Approach (v04.00.01+)**:
- Use browser developer tools with web interface
- Implement custom debugging in CI/CD scripts

## Appendix

### Complete XSD Schema

See `schemas/repository-structure.xsd` for the complete XML Schema Definition.

### Example Structures

See `scripts/definitions/` directory for example structure definitions.

### Related Documentation

- [MokoCRM Development Standards](../docs/policy/crm/development-standards.md)
- [MokoWaaS Development Standards](../docs/policy/waas/development-standards.md)
- [Branching Strategy](../docs/policy/branching-strategy.md)
- [Coding Style Guide](../docs/policy/coding-style-guide.md)

## Support

For issues or questions:
- Open an issue in the MokoStandards repository
- Contact: support@mokoconsulting.com
- See [SUPPORT.md](SUPPORT.md)

---

**Version**: 1.0.0
**Last Updated**: 2026-01-07
**Maintained By**: Moko Consulting

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Documentation                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/schemas/repohealth/repository-structure-schema.md                                      |
| Version        | 04.00.03                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-02-14 | Moko Consulting | Updated for PHP-only architecture | Deprecated Python scripts, updated to v04.00.01 |
