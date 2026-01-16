# Repository Structure Schemas

This directory contains template schema files for defining custom repository structures.

## Overview

Schema files define the expected structure, files, and directories for different types of repositories in the Moko Consulting ecosystem.

## Available Schemas

### template-repository-structure.xml

A base template schema that can be customized for new repository types. This template includes:

- Required root-level files (README, LICENSE, CHANGELOG, etc.)
- Core directory structure (docs, scripts, .github)
- Basic GitHub Actions workflow requirements
- Documentation standards

## Usage

To create a custom schema:

1. Copy `template-repository-structure.xml` to your desired location
2. Update the `<metadata>` section with your repository type details
3. Customize the `<root-files>` and `<directories>` sections
4. Reference appropriate templates from the `/templates/` directory
5. Save with a descriptive name (e.g., `my-project-type.xml`)

## Schema Structure

Each schema file contains:

- **Metadata**: Repository type, platform, maintainer information
- **Root Files**: Required files in the repository root
- **Directories**: Required and optional directory structure
- **Files within Directories**: Specific files expected in each directory

## Requirement Status Values

- `required`: Must be present
- `suggested`: Recommended but optional
- `optional`: Nice to have
- `not-allowed`: Should not be present

## Template References

Use the `<template>` element to reference template files:

```xml
<file extension="md">
  <name>README.md</name>
  <template>templates/docs/required/template-README.md</template>
</file>
```

## Always Overwrite Flag

Use `<always-overwrite>false</always-overwrite>` to protect files from being overwritten during sync:

```xml
<file extension="gitignore">
  <name>.gitignore</name>
  <always-overwrite>false</always-overwrite>
</file>
```

## Related Documentation

- Schema validation: `/scripts/validate/validate_structure_v2.py`
- Auto-detection: `/scripts/validate/auto_detect_platform.py`
- Main schemas: `/schemas/structures/`
