# Validation Guide

## Overview

This directory contains guides for validating repository structure and compliance with MokoStandards.

## Available Guides

- [**Auto-Detection**](auto-detection.md) - Automatically detect platform type (Joomla/Dolibarr/Generic) and validate structure

## Validation Tools

### Auto-Detection Script

**Location**: `scripts/validate/auto_detect_platform.py`

Automatically detects repository platform type and validates against the appropriate schema:
- Detects Joomla/WaaS components by manifest files
- Detects Dolibarr/CRM modules by module descriptors
- Falls back to generic repository validation
- Generates comprehensive documentation reports

**Quick Start**:
```bash
python3 scripts/validate/auto_detect_platform.py --verbose
```

### Manual Validation Script

**Location**: `scripts/validate/validate_structure_v2.py`

Validates repository against a specific schema (XML or JSON format):

```bash
# XML schema
python3 scripts/validate/validate_structure_v2.py --schema scripts/definitions/default-repository.xml

# JSON schema
python3 scripts/validate/validate_structure_v2.py --schema scripts/definitions/default-repository.json
```

## Related Documentation

- [Repository Structure Schema](../repository-structure-schema.md)
- [Layered Documentation Guide](../layered-documentation.md)
- [Repository Startup Guide](../../quickstart/repository-startup-guide.md)
