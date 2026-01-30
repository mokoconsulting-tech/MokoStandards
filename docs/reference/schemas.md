# MokoStandards Schemas

## ⚠️ MIGRATION NOTICE

**The schema system has been migrated from XML/JSON to Terraform.**

- **Old location**: `schemas/` directory (XML/XSD/JSON files) - **REMOVED**
- **New location**: `terraform/` directory (Terraform configuration)
- **Migration date**: January 2026
- **Schema version**: 2.0

For new projects, use the Terraform-based configuration. See [Terraform Schema Documentation](../../terraform/README.md).

## Overview

This document provides reference for the legacy XML-based schemas (now deprecated) and the new Terraform-based schema system.

### Terraform-Based Schemas (Current - v2.0)

The repository structure and health check configurations are now defined in Terraform:

- **Location**: `terraform/repository-types/`
- **Health Defaults**: `terraform/repository-types/repo-health-defaults.tf`
- **Repository Structure**: `terraform/repository-types/default-repository.tf`

See the [Terraform README](../../terraform/README.md) for complete documentation.

## Quick Start

### Repository Health Checks (Terraform-based)

```bash
# Check repository health using Terraform configuration
python scripts/validate/check_repo_health.py --repo-path .

# Verbose output
python scripts/validate/check_repo_health.py --repo-path . --verbose

# JSON output
python scripts/validate/check_repo_health.py --repo-path . --output json
```

The health checker now reads configuration from Terraform instead of XML.

### Repository Structure Validation (Legacy XML)

Structure definitions in `scripts/definitions/` still use XML format:

```bash
# Validate repository structure
python scripts/validate/validate_structure.py scripts/definitions/crm-module.xml .

# Generate stubs for new project
python scripts/validate/generate_stubs.py scripts/definitions/crm-module.xml /path/to/new/project --dry-run
```

**Note**: These XML definitions will be migrated to Terraform in a future release.

## Available Repository Types (Terraform)

The Terraform configuration defines the following repository types:

1. **Default Repository** - Standard structure for generic repositories
2. **Library** - Structure for reusable libraries
3. **Application** - Structure for standalone applications

See `terraform/repository-types/` for complete definitions.

## Repository Health Configuration

The repository health system provides automated scoring and validation of repository quality across 8 categories:

### Health Check Categories (103 points total)

1. **CI/CD Status** (15 points) - Continuous integration and deployment health
2. **Required Documentation** (16 points) - Core documentation files presence and quality
3. **Required Folders** (10 points) - Standard directory structure compliance
4. **Workflows** (12 points) - GitHub Actions workflow completeness
5. **Issue Templates** (5 points) - Issue and PR template availability
6. **Security** (15 points) - Security scanning and vulnerability management
7. **Repository Settings** (10 points) - GitHub repository configuration compliance
8. **Deployment Secrets** (20 points) - Deployment configuration and secrets management

### Health Levels

| Level | Score | Indicator | Description |
|-------|-------|-----------|-------------|
| **Excellent** | 90-100% | ✅ | Production-ready, fully compliant |
| **Good** | 70-89% | ⚠️ | Minor improvements needed |
| **Fair** | 50-69% | 🟡 | Significant improvements required |
| **Poor** | 0-49% | ❌ | Critical issues, requires immediate attention |

### Configuration Source

Health check configuration is now stored in Terraform:

```
terraform/repository-types/repo-health-defaults.tf
```

The configuration is loaded automatically by validation scripts using the `TerraformSchemaReader` module.

### Customizing Health Checks

Organizations can customize health configurations by:
1. Modifying `terraform/repository-types/repo-health-defaults.tf`
2. Creating custom repository type definitions
3. Using Terraform variables to override defaults
4. Running `terraform fmt` and `terraform validate` to verify changes

See the [Terraform README](../../terraform/README.md) for detailed customization guidance.

## Python API

### Using TerraformSchemaReader

The new Terraform-based schemas can be accessed from Python:

```python
from terraform_schema_reader import TerraformSchemaReader

# Initialize reader
reader = TerraformSchemaReader()

# Get health configuration
health_config = reader.get_health_config()
print(f"Total points: {health_config['scoring']['total_points']}")

# Get repository structure
structure = reader.get_repository_structure('default')
print(f"Root files: {len(structure['root_files'])}")

# Get checks by category
ci_checks = reader.get_checks_by_category('ci-cd-status')
for check in ci_checks:
    print(f"- {check['name']} ({check['points']} pts)")

# Get all categories
categories = reader.get_all_categories()

# Get thresholds
thresholds = reader.get_thresholds()
```

### Backward Compatibility

For scripts that used the old XML-based API, a compatibility adapter is provided:

```python
from terraform_schema_reader import LegacySchemaAdapter

# Old code still works (config_source is ignored)
adapter = LegacySchemaAdapter('ignored.xml', repo_path='.')
adapter.load_config()
config = adapter.get_health_config()
```

## Documentation

For comprehensive documentation, see:
- [Repository Structure Schema Guide](../docs/guide/repository-structure-schema.md)

## Schema Features

1. **Validation**: Verify existing repositories comply with standards
2. **Stub Generation**: Create new projects with correct structure
3. **Template Substitution**: Generate customized content
4. **Dual README Support**: Separate developer and end-user documentation
5. **Flexible Rules**: Define custom validation rules per file/directory

## Example: MokoCRM Module Structure

```
my-module/
├── README.md              # For developers (setup, build, test)
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE                # License file (no extension)
├── CHANGELOG.md          # Version history
├── Makefile              # Build automation
├── .editorconfig         # Editor settings
├── .gitignore            # Git ignore rules
├── .gitattributes        # Git attributes
├── src/                  # Deployable module code
│   ├── README.md         # For end users (install, config, usage)
│   ├── core/             # Core module files
│   ├── langs/            # Translations
│   ├── sql/              # Database schemas
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript
│   ├── class/            # PHP classes
│   └── lib/              # Libraries
├── docs/                 # Developer documentation
│   └── index.md
├── scripts/              # Build scripts
├── tests/                # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── templates/            # Code templates
└── .github/              # GitHub configuration
    └── workflows/        # CI/CD workflows
```

## Creating Custom Structures

1. Copy an existing structure XML as a template
2. Modify metadata section
3. Define your file and folder hierarchy
4. Add validation rules as needed
5. Test with validation and stub generation tools

See the [guide](../docs/guide/repository-structure-schema.md) for detailed instructions.

## Validation Rules

Supported validation rule types:
- `naming-convention` - Regex pattern for names
- `content-pattern` - Regex pattern for file content
- `file-exists` - Check file existence
- `directory-exists` - Check directory existence
- `min-size` - Minimum file size
- `max-size` - Maximum file size
- `header-required` - Require file headers
- `license-required` - Require license headers
- `custom` - Custom validation logic

## Tools

### Repository Structure Tools

#### Validation Tool
- **Location**: `scripts/validate/validate_structure.py`
- **Purpose**: Validate existing repositories against structure schemas
- **Exit Codes**: 0 = pass, 1 = fail (errors found)

#### Stub Generation Tool
- **Location**: `scripts/validate/generate_stubs.py`
- **Purpose**: Generate missing files and directories
- **Modes**: Normal, dry-run, force-overwrite

### Repository Health Tools

#### Health Configuration Validator
- **Location**: `scripts/validate/validate_repo_health.py`
- **Purpose**: Validate health configuration XML against schema
- **Features**:
  - Local file and remote URL support
  - Comprehensive validation of structure, metadata, scoring, and checks
  - Error and warning reporting
  - Can be used in CI/CD pipelines

**Usage**:
```bash
# Validate local config
python scripts/validate/validate_repo_health.py schemas/repo-health-default.xml

# Validate remote config
python scripts/validate/validate_repo_health.py https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml
```

#### Health Checker
- **Location**: `scripts/validate/check_repo_health.py`
- **Purpose**: Perform health checks on repositories based on XML configuration
- **Features**:
  - Loads configuration from local files or remote URLs
  - Executes all defined checks
  - Calculates scores and health levels
  - Outputs results in text or JSON format
  - Defaults to remote configuration from MokoStandards GitHub

**Usage**:
```bash
# Check current repository with remote config
python scripts/validate/check_repo_health.py --repo-path .

# Check with custom config
python scripts/validate/check_repo_health.py --config custom-health.xml --repo-path /path/to/repo

# Output as JSON
python scripts/validate/check_repo_health.py --output json > health-report.json
```

## Integration

### Repository Structure Integration

#### Makefile

```makefile
validate-structure:
	python scripts/validate/validate_structure.py schemas/structures/crm-module.xml .

generate-stubs:
	python scripts/validate/generate_stubs.py schemas/structures/crm-module.xml .
```

#### GitHub Actions

```yaml
- name: Validate Structure
  run: python .mokostandards/scripts/validate/validate_structure.py \
         .mokostandards/schemas/structures/crm-module.xml .
```

### Repository Health Integration

#### Makefile

```makefile
check-health:
	python scripts/validate/check_repo_health.py --repo-path .

validate-health-config:
	python scripts/validate/validate_repo_health.py schemas/repo-health-default.xml
```

#### GitHub Actions

```yaml
- name: Check Repository Health
  run: |
    # Download health checker script
    curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py -o check_repo_health.py

    # Run health check with remote config (default)
    python3 check_repo_health.py --repo-path . --output json > health-report.json

    # Display results
    cat health-report.json

- name: Upload Health Report
  uses: actions/upload-artifact@v3
  with:
    name: health-report
    path: health-report.json
```

#### Workflow Dispatch with Custom Config

```yaml
on:
  workflow_dispatch:
    inputs:
      config_url:
        description: 'Health configuration URL'
        required: false
        default: 'https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml'

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download health checker
        run: curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py -o check_repo_health.py

      - name: Run health check
        run: python3 check_repo_health.py --config "${{ github.event.inputs.config_url }}" --repo-path . --output json
```

## Benefits

### Repository Structure Benefits
1. **Consistency**: All projects follow same structure
2. **Automation**: Generate boilerplate automatically
3. **Validation**: Catch structure issues in CI/CD
4. **Documentation**: Self-documenting structure definitions
5. **Onboarding**: New team members understand layout instantly
6. **Quality**: Enforce best practices across all projects

### Repository Health Benefits
1. **Objective Scoring**: 100-point scale provides clear quality metrics
2. **Automated Validation**: Continuous monitoring of repository health
3. **Remote Configuration**: Central standards without local vendoring
4. **Customizable**: Extend with organization-specific checks
5. **Actionable Feedback**: Clear remediation guidance for each check
6. **Trend Analysis**: Track improvement over time with JSON output
7. **CI/CD Integration**: Fail builds on poor health scores
8. **Standards Enforcement**: Ensure all repositories meet quality baselines

## Support

- Documentation:
  - [Repository Structure Schema Guide](../docs/guide/repository-structure-schema.md)
  - [Repository Health Scoring System](../docs/health-scoring.md)
  - [GitHub Private Integration Prompt](../.copilot-prompts/github-private-integration-repo-health.md)
- Issues: Open in MokoStandards repository
- Contact: support@mokoconsulting.com

---

**Version**: 1.1.0
**Last Updated**: 2026-01-08

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Reference                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/reference/schemas.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
