[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Automatic Platform Detection and Validation

## Overview

The `auto_detect_platform.py` script automatically detects whether a repository is a Joomla/WaaS component, Dolibarr/CRM module, or generic repository, then validates it against the appropriate schema and generates comprehensive documentation files.

## Features

- **Automatic Platform Detection**: Analyzes repository structure to identify platform
- **Smart Schema Selection**: Automatically loads the correct schema from `scripts/definitions/`
- **Documentation Generation**: Creates detailed validation and detection reports
- **Multiple Platform Support**: Joomla, Dolibarr, and Generic repositories

## Platform Detection Methods

### Joomla/WaaS Component Detection

The script looks for:
- Joomla manifest files (`.xml` files with `<extension>` or `<install>` root elements)
- Component types: `component`, `module`, `plugin`, `library`, `template`
- Directory structure: `site/`, `admin/`, `administrator/`
- Joomla-specific files: `index.html`, language files

**Detection Threshold**: Requires 50%+ confidence score

### Dolibarr/CRM Module Detection

The script looks for:
- Module descriptor files (`mod*.class.php` extending `DolibarrModules`)
- Dolibarr-specific code patterns: `dol_include_once`, `$this->numero`
- Directory structure: `core/modules/`, `sql/`, `class/`, `lib/`, `langs/`
- SQL files in `sql/` directory

**Detection Threshold**: Requires 50%+ confidence score

### Generic Repository (Fallback)

If neither Joomla nor Dolibarr patterns are detected, the repository is classified as generic and validated against `default-repository.xml`.

## Usage

### Basic Usage

```bash
# Auto-detect and validate current repository
python3 scripts/validate/auto_detect_platform.py

# Validate specific repository
python3 scripts/validate/auto_detect_platform.py --repo-path /path/to/repo
```

### Advanced Usage

```bash
# Verbose output with detection details
python3 scripts/validate/auto_detect_platform.py --verbose

# Custom output directory for reports
python3 scripts/validate/auto_detect_platform.py --output-dir ./my-reports

# Specify schema directory location
python3 scripts/validate/auto_detect_platform.py --schema-dir /path/to/schemas/structures
```

## Generated Documentation Files

The script generates three documentation files in the output directory:

### 1. Detection Report (`detection_report_TIMESTAMP.md`)

Contains platform type, confidence score, detection indicators, manifest/descriptor locations, schema mapping, and next steps.

### 2. Validation Report (`validation_report_TIMESTAMP.md`)

Contains validation status, exit code, full validation output with errors, warnings, and info messages.

### 3. Summary Report (`SUMMARY_TIMESTAMP.md`)

Contains overall status, quick facts table, links to reports, and action items.

## Schema Mapping

| Platform | Schema File | Location |
|----------|-------------|----------|
| **Joomla/WaaS** | `waas-component.xml` | `scripts/definitions/waas-component.xml` |
| **Dolibarr/CRM** | `crm-module.xml` | `scripts/definitions/crm-module.xml` |
| **Generic** | `default-repository.xml` | `scripts/definitions/default-repository.xml` |

## Exit Codes

| Exit Code | Meaning | Action Required |
|-----------|---------|-----------------|
| **0** | All validations passed | None - repository is compliant |
| **1** | Validation errors found | Fix required items |
| **2** | Validation warnings only | Optional - consider suggested items |
| **3** | Configuration error | Check schema files and configuration |

## See Also

- [Layered Documentation Guide](../layered-documentation.md)
- [Repository Startup Guide](../../quickstart/repository-startup-guide.md)
- [Validation Scripts](../../../scripts/validate/)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/validation/auto-detection.md                                      |
| Version        | 04.00.03                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.03 with all required fields |
