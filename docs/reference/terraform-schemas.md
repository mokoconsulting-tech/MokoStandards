[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Terraform Schema Definitions

**Version**: 2.0
**Status**: Active
**Last Updated**: 2026-01-27

## Overview

This document provides comprehensive documentation for the Terraform-based schema definitions in MokoStandards. These definitions replace the legacy XML/JSON schema system with infrastructure-as-code best practices.

## Purpose

The Terraform schema definitions serve as:

1. **Single Source of Truth** - Centralized configuration for repository standards
2. **Version-Controlled Standards** - Track changes to standards over time
3. **Type-Safe Configuration** - Terraform validates syntax and structure
4. **Self-Documenting** - Configuration is readable and well-structured
5. **Programmatically Accessible** - Python scripts can read Terraform outputs
6. **Auditable** - Clear history of standard changes

## Architecture

### Directory Structure

```
terraform/
├── main.tf                          # Main Terraform configuration
├── variables.tf                     # Input variables
├── outputs.tf                       # Output definitions
├── README.md                        # Terraform overview
├── repository-types/                # Repository type definitions
│   ├── repo-health-defaults.tf      # Health check configuration
│   └── default-repository.tf        # Repository structure definitions
└── workstation/                     # Workstation provisioning
    ├── dev-workstation.tf           # Developer workstation config
    └── README.md                    # Workstation documentation
```

## Core Definitions

### 1. Repository Health Configuration

**File**: `terraform/repository-types/repo-health-defaults.tf`

Defines the repository health scoring system with categories, checks, and thresholds.

#### Metadata

```hcl
metadata = {
  name            = "MokoStandards Repository Health Default Configuration"
  version         = "1.0.0"
  description     = "Default repository health scoring..."
  effective_date  = "2026-01-08T00:00:00Z"
  maintainer      = "Moko Consulting"
  repository_url  = "https://github.com/mokoconsulting-tech/MokoStandards"
  schema_version  = "1.0"
}
```

#### Scoring Configuration

- **Total Points**: 103 points
- **Categories**: 8 categories
- **Health Levels**: 4 thresholds (excellent, good, fair, poor)

#### Health Check Categories

1. **CI/CD Status** (15 points)
   - Build status indicators
   - Workflow passing checks
   - CI workflow presence

2. **Required Documentation** (16 points)
   - README.md
   - LICENSE
   - SECURITY.md
   - CHANGELOG.md
   - CODE_OF_CONDUCT.md
   - CONTRIBUTING.md
   - docs/ directory

3. **Required Folders** (10 points)
   - .github/ directory
   - .github/workflows/
   - scripts/ directory (optional)
   - tests/ directory (suggested)

4. **Workflows** (12 points)
   - GitHub Actions workflows
   - CI/CD automation

5. **Issue Templates** (5 points)
   - Issue templates
   - PR templates

6. **Security** (15 points)
   - Security scanning
   - Vulnerability management

7. **Repository Settings** (10 points)
   - GitHub repository configuration
   - Branch protection

8. **Deployment Secrets** (20 points)
   - Deployment configuration
   - Secrets management

#### Health Thresholds

| Level | Score | Indicator | Description |
|-------|-------|-----------|-------------|
| Excellent | 90-100% | ✅ | Production-ready, fully compliant |
| Good | 70-89% | ⚠️ | Minor improvements needed |
| Fair | 50-69% | 🟡 | Significant improvements required |
| Poor | 0-49% | ❌ | Critical issues, immediate attention |

#### Check Types

Supported check types:

- `file-exists` - Verify file presence
- `directory-exists` - Verify directory presence
- `directory-exists-any` - Verify at least one directory exists
- `content-pattern` - Check file content matches regex
- `file-size` - Validate file size constraints
- `workflow-exists` - Check workflow file presence
- `workflow-passing` - Verify workflow success (requires GitHub API)
- `branch-exists` - Verify branch presence (requires Git)
- `github-setting` - Check GitHub setting (requires GitHub API)
- `secret-configured` - Verify secret existence (requires GitHub API)

#### Example Check Definition

```hcl
readme_present = {
  id          = "readme-present"
  name        = "README.md present"
  description = "Repository has a README.md file"
  points      = 3
  check_type  = "file-exists"
  category    = "required-documentation"
  required    = true
  remediation = "Create README.md from template"
  parameters = {
    file_path = "README.md"
  }
}
```

### 2. Repository Structure Definitions

**File**: `terraform/repository-types/default-repository.tf`

Defines the expected structure for a default repository.

#### Metadata

```hcl
metadata = {
  name            = "Default Repository Structure"
  description     = "Standard structure for generic repositories"
  platform        = "multi-platform"
  repository_type = "library"
  schema_version  = "1.0"
  last_updated    = "2026-01-16T00:00:00Z"
  maintainer      = "MokoStandards Team"
}
```

#### Root Files

Required and suggested files at repository root:

| File | Status | Description |
|------|--------|-------------|
| README.md | Required | Project documentation |
| LICENSE | Required | Repository license |
| .gitignore | Required | Git ignore patterns |
| SECURITY.md | Required | Security policy |
| CHANGELOG.md | Suggested | Version history |
| CONTRIBUTING.md | Suggested | Contribution guidelines |
| CODE_OF_CONDUCT.md | Suggested | Code of conduct |
| .editorconfig | Suggested | Editor configuration |
| .gitattributes | Optional | Git attributes |

#### Directory Structure

| Directory | Status | Purpose |
|-----------|--------|---------|
| .github/ | Required | GitHub configuration |
| .github/workflows/ | Required | CI/CD automation |
| .github/ISSUE_TEMPLATE/ | Suggested | Issue templates |
| .github/PULL_REQUEST_TEMPLATE/ | Suggested | PR templates |
| docs/ | Suggested | Documentation |
| tests/ | Suggested | Automated testing |
| scripts/ | Optional | Utility scripts |
| src/ | Optional | Source code |

#### Requirement Status Levels

- **Required**: Must exist, validation fails if missing
- **Suggested**: Should exist, warning if missing
- **Optional**: Nice to have, informational if missing

### 3. Dev Workstation Configuration

**File**: `terraform/workstation/dev-workstation.tf`

Defines Windows developer workstation provisioning configuration.

#### Workspace Settings

```hcl
workspace = {
  default_path      = "$env:USERPROFILE\\Documents\\Workspace"
  create_if_missing = true
  artifacts = [
    "winget-monthly-update.cmd",
    "logs",
    "scripts"
  ]
}
```

#### Winget Configuration

- **Update Schedule**: Monthly on 1st at 09:00
- **Excluded Packages**:
  - Python.Python.3.10 (pinned version)
  - PHP.PHP (WSL managed)
- **Log Location**: C:\Logs\Winget
- **Options**: Silent, accept agreements

#### WSL Configuration

```hcl
wsl = {
  enabled              = true
  default_distro       = "Ubuntu"
  require_confirmation = true

  provisioning = {
    auto_install            = false  # User confirmation required
    auto_reset              = false  # User confirmation required
    provision_after_install = true
  }
}
```

#### Ubuntu PHP Setup

- **Version**: PHP 8.3
- **Packages**: CLI, MySQL, cURL, mbstring, intl, GD, ZIP, SOAP, ImageMagick, APCu, IMAP
- **Enabled Modules**: curl, mbstring, intl, gd, zip, soap, imagick, opcache, mysqli, pdo_mysql, apcu, imap

#### Security Configuration

- **Require Admin**: Yes
- **User Confirmation**: Required for destructive actions
- **Confirmation Gates**:
  - WSL Reset (warning dialog)
  - WSL Install (question dialog)

## Python Integration

### TerraformSchemaReader Module

**File**: `scripts/lib/terraform_schema_reader.py`

Python module for reading Terraform outputs programmatically.

#### Basic Usage

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

#### Methods

- `get_health_config()` - Get complete health configuration
- `get_repository_structure(repo_type)` - Get structure for repository type
- `get_checks_by_category(category_id)` - Get checks for a category
- `get_all_categories()` - Get all category definitions
- `get_thresholds()` - Get health level thresholds

### How It Works

1. Reader runs `terraform output -json` in terraform/ directory
2. Parses JSON output to extract configuration
3. Provides dictionary access to configuration
4. Caches results for performance

## Validation Scripts

### Repository Health Checker

**File**: `scripts/validate/check_repo_health.py`

Validates repository against health standards.

```bash
# Check repository health
python3 scripts/validate/check_repo_health.py --repo-path .

# Verbose output
python3 scripts/validate/check_repo_health.py --repo-path . --verbose

# JSON output
python3 scripts/validate/check_repo_health.py --repo-path . --output json
```

### Repository Structure Validator

**File**: `scripts/validate/validate_structure_terraform.py`

Validates repository structure against Terraform definitions.

```bash
# Validate current directory
python3 scripts/validate/validate_structure_terraform.py .

# Validate specific repository type
python3 scripts/validate/validate_structure_terraform.py . --repo-type library

# Verbose output
python3 scripts/validate/validate_structure_terraform.py . --verbose
```

## Terraform Operations

### Initialize Terraform

```bash
cd terraform
terraform init
```

### Validate Configuration

```bash
cd terraform
terraform validate
```

### Format Configuration

```bash
cd terraform
terraform fmt -recursive
```

### View Outputs

```bash
cd terraform

# View all outputs
terraform output

# View specific output
terraform output repository_schemas

# JSON format
terraform output -json repository_schemas
```

### Apply Configuration

```bash
cd terraform
terraform plan -out=tfplan
terraform apply tfplan
```

**Note**: Applying creates Terraform state but doesn't provision infrastructure. It makes outputs available for scripts to consume.

## Configuration Management

### Making Changes

1. **Edit Terraform Files**
   - Modify `.tf` files in `terraform/` directory
   - Update locals blocks with new values

2. **Format and Validate**
   ```bash
   terraform fmt -recursive
   terraform validate
   ```

3. **Test Changes**
   ```bash
   # View what would change
   terraform plan

   # Apply changes
   terraform apply

   # Test Python integration
   python3 scripts/lib/terraform_schema_reader.py
   ```

4. **Update Documentation**
   - Update this file if structure changes
   - Update README files in subdirectories
   - Update CHANGELOG.md

5. **Commit Changes**
   ```bash
   git add terraform/
   git commit -m "Update Terraform schema definitions"
   ```

### Version Control

- **Never commit** `.tfstate` files (in .gitignore)
- **Never commit** `.tfplan` files (in .gitignore)
- **Never commit** `.terraform/` directory (in .gitignore)
- **Do commit** all `.tf` files
- **Do commit** `README.md` documentation

### Excluded from Scans

The confidentiality scan excludes:
- `terraform/*.tfplan` - Binary plan files
- `terraform/*.tfstate*` - State files with computed values
- `terraform/.terraform/*` - Terraform cache

Terraform definition files (*.tf) ARE scanned for secrets.

## Best Practices

### Writing Terraform Configuration

1. **Use Locals for Configuration**
   - Keep all configuration in `locals` blocks
   - Makes it easy to reference and modify

2. **Provide Metadata**
   - Always include version, description, maintainer
   - Add timestamps for tracking changes

3. **Document Inline**
   - Use comments to explain complex logic
   - Document why decisions were made

4. **Use Consistent Naming**
   - Use snake_case for resource names
   - Use descriptive, self-documenting names

5. **Structure Logically**
   - Group related configuration together
   - Use clear section headers in comments

### Schema Design

1. **Required vs Optional**
   - Be explicit about requirement status
   - Document why something is required

2. **Provide Remediation**
   - Include remediation steps for checks
   - Make it actionable and specific

3. **Points Allocation**
   - Higher points for critical items
   - Balance across categories

4. **Check Types**
   - Use appropriate check type for validation
   - Consider performance implications

## Migration from XML/JSON

The Terraform definitions replace:

- `schemas/repo-health-default.xml` (938 lines) → `repo-health-defaults.tf` (351 lines)
- `schemas/repository-structure.schema.json` (259 lines) → `default-repository.tf` (190 lines)
- `schemas/*.xsd` files → Terraform type validation

### Benefits

1. **Reduced Code**: 2,490 lines → ~1,400 lines
2. **Type Safety**: Built-in validation
3. **Better Diffs**: Text-based, not XML
4. **Tooling**: Terraform ecosystem support
5. **Industry Standard**: Common IaC approach

## Troubleshooting

### Terraform Not Found

Install Terraform:
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Python Can't Find Module

Ensure path is correct:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from terraform_schema_reader import TerraformSchemaReader
```

### Terraform State Issues

Reinitialize:
```bash
cd terraform
rm -rf .terraform
terraform init
```

### Output Not Available

Apply configuration first:
```bash
cd terraform
terraform init
terraform apply
```

## Future Enhancements

Planned additions:

1. **Additional Repository Types**
   - Microservice repository structure
   - Monorepo structure
   - Documentation-only repository

2. **Platform-Specific Checks**
   - Joomla extension validation
   - Dolibarr module validation
   - WordPress plugin validation

3. **Advanced Health Checks**
   - Code coverage thresholds
   - Documentation coverage
   - Dependency freshness

4. **Workstation Variations**
   - MacOS developer workstation
   - Linux developer workstation
   - Cloud workspace configuration

5. **Integration Templates**
   - CI/CD pipeline templates
   - Pre-commit hook configurations
   - IDE/editor settings

## References

### Internal Documentation

- [Terraform README](../terraform/README.md) - Overview of Terraform setup
- [Workstation README](../terraform/workstation/README.md) - Workstation config details
- [Schema Reference](../docs/reference/schemas.md) - Legacy and current schema info
- [CHANGELOG](../CHANGELOG.md) - Version history

### External Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Language](https://www.terraform.io/language)
- [Terraform CLI](https://www.terraform.io/cli)

## Support

For questions or issues:

1. Check this documentation
2. Review Terraform README files
3. Check CHANGELOG for recent changes
4. Open an issue in the repository

---

**Document Version**: 1.0
**Last Updated**: 2026-01-27
**Maintainer**: MokoStandards Team

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Reference                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/reference/terraform-schemas.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
