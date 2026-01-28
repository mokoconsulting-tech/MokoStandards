# Repository Structure Schema Guide

## Overview

The Repository Structure Schema system provides a comprehensive framework for defining, validating, and managing repository structures across all MokoStandards-governed repositories. This guide covers the complete schema specification including the new source/destination system and stub generation capabilities.

## Table of Contents

1. [Introduction](#introduction)
2. [Schema Architecture](#schema-architecture)
3. [File Definition with Source and Destination](#file-definition-with-source-and-destination)
4. [Stub Generation](#stub-generation)
5. [Directory Structure](#directory-structure)
6. [Requirement Status Levels](#requirement-status-levels)
7. [XML Schema Format](#xml-schema-format)
8. [JSON Schema Format](#json-schema-format)
9. [Template System](#template-system)
10. [Validation Rules](#validation-rules)
11. [Usage Examples](#usage-examples)
12. [Best Practices](#best-practices)

---

## Introduction

### Purpose

The Repository Structure Schema system enables:
- **Standardization**: Consistent repository structures across the organization
- **Automation**: Automatic file generation from templates or stubs
- **Validation**: Compliance checking against organizational standards
- **Documentation**: Self-documenting repository requirements

### Key Features (NEW in v2.0)

- **Source/Destination Mapping**: Explicit paths for template sources and file destinations
- **Automatic Extension Conversion**: Templates with `.template` extensions are automatically converted to working extensions (e.g., `.yml.template` → `.yml`)
- **Stub Generation**: Automatic creation of placeholder files when no template source is defined
- **Type-Safe Operations**: Explicit source types (template, stub, copy)
- **Path Auto-Creation**: Automatic directory creation for destination paths

---

## Schema Architecture

### Components

```
schemas/
├── repository-structure.xsd          # XML Schema Definition (XSD)
├── repository-structure.schema.json  # JSON Schema Definition
└── structures/                       # Repository structure definitions
    ├── default-repository.xml        # Generic repository structure
    ├── waas-component.xml            # Joomla component structure
    ├── crm-module.xml                # Dolibarr module structure
    └── ...
```

### Schema Hierarchy

```
Repository Structure
├── Metadata (name, description, type, platform)
└── Structure
    ├── Root Files (files at repository root)
    └── Directories (recursive directory structure)
        ├── Files (files within directory)
        └── Subdirectories (nested directories)
```

---

## File Definition with Source and Destination

### New Schema Structure (v2.0)

Every file entry can now include explicit source and destination information:

```xml
<file extension="yml">
  <name>ci.yml</name>
  <description>Continuous integration workflow</description>
  <requirement-status>suggested</requirement-status>

  <!-- SOURCE: Where to get the file -->
  <source>
    <path>templates/workflows/generic</path>
    <filename>ci.yml.template</filename>
    <type>template</type>
  </source>

  <!-- DESTINATION: Where to place the file -->
  <destination>
    <path>.github/workflows</path>
    <filename>ci.yml</filename>
    <create-path>true</create-path>
  </destination>

  <!-- Legacy template field (maintained for backward compatibility) -->
  <template>templates/workflows/generic/ci.yml.template</template>
</file>
```

### Source Element

**Purpose**: Defines where to get the file content

**Fields**:
- `<path>` (string, required): Directory path relative to MokoStandards root
- `<filename>` (string, required): Source filename (e.g., `ci.yml.template`)
- `<type>` (enum, required): Source type - one of:
  - `template`: Copy from template file (default)
  - `stub`: Generate stub file if no source defined
  - `copy`: Direct copy from source location

**Example - Template Source**:
```xml
<source>
  <path>templates/workflows/generic</path>
  <filename>ci.yml.template</filename>
  <type>template</type>
</source>
```

**Example - Copy Source**:
```xml
<source>
  <path>.github/workflows</path>
  <filename>standards-compliance.yml</filename>
  <type>copy</type>
</source>
```

### Destination Element

**Purpose**: Defines where to place the file in target repository

**Fields**:
- `<path>` (string, required): Destination directory path relative to repository root
- `<filename>` (string, required): Destination filename (e.g., `ci.yml` - note: no `.template`)
- `<create-path>` (boolean, optional, default: true): Auto-create destination directory if missing

**Key Feature**: **Automatic Extension Conversion**
- Template files with `.template` extension are automatically converted to working extensions
- Example: `ci.yml.template` → `ci.yml`
- Example: `template-README.md` → `README.md`

**Example - Workflow Destination**:
```xml
<destination>
  <path>.github/workflows</path>
  <filename>ci.yml</filename>
  <create-path>true</create-path>
</destination>
```

**Example - Root File Destination**:
```xml
<destination>
  <path>.</path>
  <filename>LICENSE</filename>
  <create-path>false</create-path>
</destination>
```

### Complete Example - Workflow File

```xml
<file extension="yml">
  <name>codeql-analysis.yml</name>
  <description>CodeQL security analysis workflow</description>
  <requirement-status>suggested</requirement-status>

  <source>
    <path>templates/workflows/generic</path>
    <filename>codeql-analysis.yml.template</filename>
    <type>template</type>
  </source>

  <destination>
    <path>.github/workflows</path>
    <filename>codeql-analysis.yml</filename>
    <create-path>true</create-path>
  </destination>

  <always-overwrite>false</always-overwrite>
  <audience>developer</audience>
  <template>templates/workflows/generic/codeql-analysis.yml.template</template>
</file>
```

### Complete Example - Documentation File

```xml
<file extension="md">
  <name>README.md</name>
  <description>Project overview and documentation</description>
  <requirement-status>required</requirement-status>

  <source>
    <path>templates/docs/required</path>
    <filename>template-README.md</filename>
    <type>template</type>
  </source>

  <destination>
    <path>.</path>
    <filename>README.md</filename>
    <create-path>false</create-path>
  </destination>

  <audience>general</audience>
  <template>templates/docs/required/template-README.md</template>
</file>
```

---

## Stub Generation

### What is a Stub?

A **stub** is a minimal placeholder file automatically generated when:
1. No template source is defined (`<source>` element missing or type is "stub")
2. The file is required or suggested but doesn't exist
3. No `<stub-content>` is provided

### Stub Generation Rules

**Rule 1**: If `<source>` is missing → Generate stub
**Rule 2**: If `<source type="stub">` → Generate stub
**Rule 3**: If `<stub-content>` is provided → Use that content
**Rule 4**: Otherwise → Generate default stub based on file type

### Stub Content Element

```xml
<file extension="md">
  <name>ARCHITECTURE.md</name>
  <description>Architecture documentation</description>
  <requirement-status>optional</requirement-status>

  <!-- No source defined, will generate stub -->

  <destination>
    <path>docs</path>
    <filename>ARCHITECTURE.md</filename>
    <create-path>true</create-path>
  </destination>

  <stub-content><![CDATA[
# Architecture

## Overview

TODO: Describe the system architecture

## Components

TODO: List and describe major components

## Data Flow

TODO: Explain data flow through the system
]]></stub-content>
</file>
```

### Default Stub Templates by File Type

When no `<stub-content>` is provided:

**Markdown (.md)**:
```markdown
# [Filename]

TODO: Add content for [filename]
```

**YAML (.yml)**:
```yaml
# [Filename]
# TODO: Configure workflow
```

**Shell Script (.sh)**:
```bash
#!/bin/bash
# [Filename]
# TODO: Implement script

set -e

echo "TODO: Implement [filename]"
```

**Python (.py)**:
```python
#!/usr/bin/env python3
"""[Filename]

TODO: Add module documentation
"""

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
```

### Stub Example - Config File

```xml
<file extension="yml">
  <name>config.yml</name>
  <description>Application configuration</description>
  <requirement-status>required</requirement-status>

  <source>
    <type>stub</type>
  </source>

  <destination>
    <path>config</path>
    <filename>config.yml</filename>
    <create-path>true</create-path>
  </destination>

  <stub-content><![CDATA[
# Application Configuration

app:
  name: "TODO: Application Name"
  version: "0.1.0"
  environment: "development"

database:
  # TODO: Configure database connection
  host: "localhost"
  port: 5432

logging:
  level: "INFO"
]]></stub-content>
</file>
```

---

## Directory Structure

### Directory Definition

```xml
<directory path="src">
  <name>src</name>
  <description>Source code directory</description>
  <requirement-status>required</requirement-status>
  <purpose>Contains application source code</purpose>

  <files>
    <!-- Files in this directory -->
  </files>

  <subdirectories>
    <!-- Nested directories -->
  </subdirectories>
</directory>
```

### Directory Fields

- `<name>` (string, required): Directory name
- `<description>` (string, optional): Human-readable description
- `<requirement-status>` (enum, required): required | suggested | optional | not-allowed
- `<purpose>` (string, optional): Detailed purpose explanation
- `<files>` (collection, optional): Files within the directory
- `<subdirectories>` (collection, optional): Nested subdirectories
- `path` (attribute, required): Full path from repository root

### Example - Complete Directory

```xml
<directory path=".github/workflows">
  <name>workflows</name>
  <description>GitHub Actions workflows</description>
  <requirement-status>required</requirement-status>
  <purpose>Contains CI/CD workflow definitions</purpose>

  <files>
    <file extension="yml">
      <name>ci.yml</name>
      <description>Continuous integration</description>
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
  </files>
</directory>
```

---

## Requirement Status Levels

### Four Requirement Levels

| Status | Meaning | Validation | Impact |
|--------|---------|------------|--------|
| **required** | MUST be present | Error if missing | Blocks deployment |
| **suggested** | SHOULD be present | Warning if missing | Reduces health score |
| **optional** | MAY be present | No validation | No impact |
| **not-allowed** | MUST NOT be present | Error if present | Compliance violation |

### Examples

**Required File**:
```xml
<file extension="">
  <name>LICENSE</name>
  <description>License file</description>
  <requirement-status>required</requirement-status>
  <!-- Missing file = Deployment blocked -->
</file>
```

**Suggested File**:
```xml
<file extension="md">
  <name>CODE_OF_CONDUCT.md</name>
  <description>Community code of conduct</description>
  <requirement-status>suggested</requirement-status>
  <!-- Missing file = Warning only -->
</file>
```

**Not-Allowed Directory**:
```xml
<directory path="node_modules">
  <name>node_modules</name>
  <description>Node.js dependencies (generated)</description>
  <requirement-status>not-allowed</requirement-status>
  <!-- Present directory = Compliance violation -->
</directory>
```

---

## XML Schema Format

### Complete XML Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository-structure version="1.0"
                       schema-version="1.0"
                       xmlns="http://mokoconsulting.com/schemas/repository-structure">

  <!-- Metadata -->
  <metadata>
    <name>Generic Repository</name>
    <description>Standard structure for generic repositories</description>
    <repository-type>application</repository-type>
    <platform>multi-platform</platform>
    <last-updated>2026-01-16T00:00:00Z</last-updated>
    <maintainer>MokoStandards Team</maintainer>
  </metadata>

  <!-- Structure -->
  <structure>
    <!-- Root Files -->
    <root-files>
      <file extension="md">
        <name>README.md</name>
        <description>Project documentation</description>
        <requirement-status>required</requirement-status>

        <source>
          <path>templates/docs/required</path>
          <filename>template-README.md</filename>
          <type>template</type>
        </source>

        <destination>
          <path>.</path>
          <filename>README.md</filename>
          <create-path>false</create-path>
        </destination>

        <audience>general</audience>
        <always-overwrite>false</always-overwrite>
      </file>
    </root-files>

    <!-- Directories -->
    <directories>
      <directory path="src">
        <name>src</name>
        <description>Source code</description>
        <requirement-status>required</requirement-status>
        <purpose>Application source code</purpose>
      </directory>

      <directory path="docs">
        <name>docs</name>
        <description>Documentation</description>
        <requirement-status>required</requirement-status>
        <purpose>Project documentation</purpose>
      </directory>
    </directories>
  </structure>
</repository-structure>
```

---

## JSON Schema Format

### Complete JSON Example

```json
{
  "schemaVersion": "1.0",
  "metadata": {
    "name": "Generic Repository",
    "description": "Standard structure for generic repositories",
    "repositoryType": "application",
    "platform": "multi-platform",
    "lastUpdated": "2026-01-16T00:00:00Z",
    "maintainer": "MokoStandards Team"
  },
  "structure": {
    "rootFiles": [
      {
        "name": "README.md",
        "extension": "md",
        "description": "Project documentation",
        "requirementStatus": "required",
        "source": {
          "path": "templates/docs/required",
          "filename": "template-README.md",
          "type": "template"
        },
        "destination": {
          "path": ".",
          "filename": "README.md",
          "createPath": false
        },
        "audience": "general",
        "alwaysOverwrite": false
      }
    ],
    "directories": [
      {
        "name": "src",
        "path": "src",
        "description": "Source code",
        "requirementStatus": "required",
        "purpose": "Application source code"
      },
      {
        "name": "docs",
        "path": "docs",
        "description": "Documentation",
        "requirementStatus": "required",
        "purpose": "Project documentation"
      }
    ]
  }
}
```

---

## Template System

### Template Naming Convention

**Source (in templates/)**: Files with `.template` extension or `template-` prefix
**Destination (in repository)**: Working extension without template markers

| Source Template | Destination File |
|----------------|------------------|
| `ci.yml.template` | `ci.yml` |
| `template-README.md` | `README.md` |
| `codeql-analysis.yml.template` | `codeql-analysis.yml` |
| `template-CONTRIBUTING.md` | `CONTRIBUTING.md` |

### Template Processing

1. **Locate Source**: Find template file at `<source><path>/<filename>`
2. **Process Content**: Apply variable substitutions (if any)
3. **Convert Name**: Remove `.template` or `template-` from filename
4. **Create Path**: Ensure `<destination><path>` exists
5. **Write File**: Save to `<destination><path>/<filename>`

### Template Variables (Future Enhancement)

Templates may support variable substitution:

```yaml
name: {{PROJECT_NAME}}
version: {{PROJECT_VERSION}}
```

---

## Validation Rules

### File Validation

```xml
<file>
  <!-- ... -->
  <validation-rules>
    <rule type="file-exists" severity="error">
      <message>File must exist</message>
    </rule>
    <rule type="not-empty" severity="warning">
      <message>File should not be empty</message>
    </rule>
  </validation-rules>
</file>
```

### Directory Validation

```xml
<directory>
  <!-- ... -->
  <validation-rules>
    <rule type="dir-exists" severity="error">
      <message>Directory must exist</message>
    </rule>
    <rule type="contains-files" severity="warning">
      <message>Directory should contain files</message>
    </rule>
  </validation-rules>
</directory>
```

---

## Usage Examples

### Example 1: Adding Workflow Template

```xml
<file extension="yml">
  <name>deploy.yml</name>
  <description>Deployment workflow</description>
  <requirement-status>optional</requirement-status>

  <source>
    <path>templates/workflows/generic</path>
    <filename>deploy.yml.template</filename>
    <type>template</type>
  </source>

  <destination>
    <path>.github/workflows</path>
    <filename>deploy.yml</filename>
    <create-path>true</create-path>
  </destination>
</file>
```

**Result**:
- Copies `templates/workflows/generic/deploy.yml.template`
- Renames to `deploy.yml` (removes `.template`)
- Places in `.github/workflows/deploy.yml`
- Creates `.github/workflows/` if missing

### Example 2: Adding Required Documentation with Stub

```xml
<file extension="md">
  <name>SECURITY.md</name>
  <description>Security policy</description>
  <requirement-status>required</requirement-status>

  <!-- No source - will generate stub -->

  <destination>
    <path>.</path>
    <filename>SECURITY.md</filename>
    <create-path>false</create-path>
  </destination>

  <stub-content><![CDATA[
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com
]]></stub-content>
</file>
```

**Result**:
- Generates `SECURITY.md` with stub content
- Places in repository root
- File is required for compliance

### Example 3: Platform-Specific Workflow

```xml
<file extension="yml">
  <name>ci.yml</name>
  <description>Joomla CI workflow</description>
  <requirement-status>required</requirement-status>

  <source>
    <path>templates/workflows/joomla</path>
    <filename>ci-joomla.yml.template</filename>
    <type>template</type>
  </source>

  <destination>
    <path>.github/workflows</path>
    <filename>ci.yml</filename>
    <create-path>true</create-path>
  </destination>
</file>
```

**Result**:
- Uses Joomla-specific CI template
- Converts to working `ci.yml` file
- Validates Joomla manifest on CI

---

## Best Practices

### 1. Source/Destination Always Defined

**Good**:
```xml
<file>
  <source>...</source>
  <destination>...</destination>
</file>
```

**Avoid** (unless intentionally generating stub):
```xml
<file>
  <!-- No source or destination -->
</file>
```

### 2. Consistent Path Separators

Use forward slashes (`/`) for all paths:
```xml
<path>templates/workflows/generic</path>  <!-- Good -->
<path>templates\workflows\generic</path>  <!-- Bad -->
```

### 3. Create-Path Default

Set `<create-path>` explicitly:
```xml
<destination>
  <path>.github/workflows</path>
  <filename>ci.yml</filename>
  <create-path>true</create-path>  <!-- Explicit -->
</destination>
```

### 4. Stub Content for Complex Files

Provide comprehensive stub content for files requiring structure:
```xml
<stub-content><![CDATA[
# Well-structured stub
## With sections
### And examples
]]></stub-content>
```

### 6. Requirement Status Guidelines

- **required**: Core functionality files
- **suggested**: Quality/documentation files
- **optional**: Nice-to-have files
- **not-allowed**: Generated artifacts

### 7. Extension Consistency

Source and destination extensions should match intent:
```xml
<!-- Template with .template extension -->
<source>
  <filename>ci.yml.template</filename>
</source>
<destination>
  <filename>ci.yml</filename>  <!-- Removes .template -->
</destination>
```

---

## Migration from v1.0 to v2.0

### Changes

1. Added `<source>` element
2. Added `<destination>` element
3. Retained `<template>` for backward compatibility
4. Added `<stub-content>` for custom stubs

### Migration Steps

1. **Keep existing `<template>` field**
2. **Add `<source>` element** with template path
3. **Add `<destination>` element** with target path
4. **Test validation** with new fields

### Example Migration

**v1.0**:
```xml
<file extension="yml">
  <name>ci.yml</name>
  <template>templates/workflows/generic/ci.yml.template</template>
</file>
```

**v2.0**:
```xml
<file extension="yml">
  <name>ci.yml</name>

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

  <template>templates/workflows/generic/ci.yml.template</template>
</file>
```

---

## Additional Resources

- [Repository Structure Schema XSD](../../../schemas/repository-structure.xsd)
- [Repository Structure JSON Schema](../../../schemas/repository-structure.schema.json)
- [Default Repository Structure](../../../scripts/definitions/default-repository.xml)
- [Joomla Component Structure](../../../scripts/definitions/waas-component.xml)
- [Dolibarr Module Structure](../../../scripts/definitions/crm-module.xml)
- [Validation Script Documentation](../validation/auto-detection.md)

---

**Last Updated**: 2026-01-16
**Schema Version**: 2.0
**Maintained By**: MokoStandards Team

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Documentation                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/schemas/repohealth/schema-guide.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
