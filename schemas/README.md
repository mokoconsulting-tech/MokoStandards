# MokoStandards Schemas

This directory contains XML schemas and configurations for standardizing repository layouts and health checks across Moko Consulting projects.

## Contents

### Repository Structure Schemas
- **repository-structure.xsd** - XML Schema Definition (XSD) that defines the structure format
- **structures/** - Directory containing specific structure definitions for different project types

### Repository Health Schemas
- **repo-health.xsd** - XML Schema Definition (XSD) for repository health configuration
- **repo-health-default.xml** - Default health check configuration for all Moko Consulting repositories

## Quick Start

### Repository Structure

#### Validate a Repository Structure

```bash
python scripts/validate/validate_structure.py schemas/structures/crm-module.xml .
```

#### Generate Stubs for a New Project

```bash
python scripts/validate/generate_stubs.py schemas/structures/crm-module.xml /path/to/new/project --dry-run
```

### Repository Health

#### Validate Health Configuration

```bash
python scripts/validate/validate_repo_health.py schemas/repo-health-default.xml --verbose
```

#### Check Repository Health

```bash
# Using local configuration
python scripts/validate/check_repo_health.py --config schemas/repo-health-default.xml --repo-path .

# Using remote configuration (default)
python scripts/validate/check_repo_health.py --repo-path . --output json
```

The health checker defaults to the remote configuration at:
`https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`

## Available Structures

### MokoCRM (Dolibarr) Modules
- **File**: `structures/crm-module.xml`
- **Purpose**: Standard structure for Dolibarr modules
- **Key Feature**: Dual README structure
  - Root `README.md`: Developer audience
  - `src/README.md`: End-user audience

### MokoWaaS (Joomla) Extensions
- **Component**: `structures/waas-component.xml` (to be added)
- **Module**: `structures/waas-module.xml` (to be added)
- **Plugin**: `structures/waas-plugin.xml` (to be added)

## Repository Health Configuration

The repository health system provides automated scoring and validation of repository quality across 8 categories:

### Health Check Categories (100 points total)

1. **CI/CD Status** (15 points) - Continuous integration and deployment health
2. **Required Documentation** (15 points) - Core documentation files presence and quality
3. **Required Folders** (10 points) - Standard directory structure compliance
4. **Workflows** (10 points) - GitHub Actions workflow completeness
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

### Remote Configuration

The default health configuration is available remotely at:
```
https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml
```

This allows repositories to reference the configuration without vendoring it locally, ensuring all repositories use the latest standards.

### Customizing Health Checks

Organizations can create custom health configurations by:
1. Copying `repo-health-default.xml` as a template
2. Modifying categories, checks, and scoring as needed
3. Validating against `repo-health.xsd` schema
4. Hosting in a private repository or using locally

See the [coordinating prompt](.copilot-prompts/github-private-integration-repo-health.md) for organization-specific implementation guidance.

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

**Version**: 2.0.0  
**Last Updated**: 2026-01-18

## Changelog

### Version 2.0.0 (2026-01-18) - Enterprise Ready
**Major Release**: Comprehensive enterprise features added to schema

#### New Enterprise Sections
1. **Compliance Requirements**: Support for SOC2, GDPR, HIPAA, ISO27001, PCI-DSS, NIST, FedRAMP, CCPA
2. **Security Policy**: Vulnerability scanning, secret scanning, dependency scanning, code scanning
3. **Dependencies**: Multi-ecosystem package management (npm, pip, composer, maven, etc.) with security requirements
4. **Quality Gates**: Code coverage thresholds, complexity limits, test requirements, performance benchmarks
5. **CI/CD Requirements**: Workflow requirements, deployment strategies, artifact management, pipeline stages
6. **Documentation Requirements**: Required documentation types (README, API docs, architecture, runbooks)
7. **Team Structure**: CODEOWNERS, maintainers, contributors, team permissions
8. **Release Management**: Versioning strategies (semver/calver), changelog requirements, hotfix/deprecation policies
9. **Monitoring**: Health checks, metrics collection, alerting, structured logging

#### Schema Enhancements
- Updated from version 1.0 to 2.0
- Added 48+ new complex types to XSD schema
- Extended JSON schema with enterprise properties
- All new sections are optional (minOccurs="0")
- Comprehensive enum types for standardization
- Default repository definition updated with examples

#### Breaking Changes
- Schema version changed to 2.0 (use schema-version="2.0" in XML files)
- Old 1.0 definitions still compatible (new sections optional)

### Version 1.2.0 (2026-01-18)
- Added `scripts/requirements.txt` to all repository structure definitions
- Updated security requirements: defusedxml>=0.7.1 for safe XML parsing
- Added stub content for Python dependencies in scripts directory
- Updated all schema definition timestamps
- Enhanced security documentation for script dependencies
