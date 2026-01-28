# Terraform Repository Schema Configuration

This directory contains Terraform-based repository schema definitions that replace the legacy XML/JSON schema system.

## Overview

The schema system has been migrated from XML/JSON to Terraform for better:
- Version control and infrastructure-as-code practices
- Type safety and validation
- Integration with automation tools
- Maintainability and readability

## Structure

```
terraform/
├── main.tf                          # Main configuration
├── variables.tf                     # Input variables
├── outputs.tf                       # Output definitions
├── repository-types/               # Repository type definitions
│   ├── repo-health-defaults.tf    # Health check defaults
│   └── default-repository.tf      # Default repository structure
└── README.md                        # This file
```

## Repository Types

### Default Repository (`default-repository.tf`)

Standard structure for generic repositories including:
- Root files (README, LICENSE, etc.)
- Directory structure (.github, docs, tests, etc.)
- Validation rules

### Repository Health Defaults (`repo-health-defaults.tf`)

Health scoring configuration including:
- Scoring categories and point values
- Health thresholds (excellent, good, fair, poor)
- Individual health checks
- Remediation guidance

## Usage

### Initialize Terraform

```bash
cd terraform
terraform init
```

### View Configuration

```bash
# Show all outputs
terraform output

# Show specific output as JSON
terraform output -json repository_schemas

# Show health configuration
terraform output -json repo_health_configuration
```

### Using with Python Scripts

Python scripts can extract Terraform configuration using the helper module:

```python
from terraform_schema_reader import TerraformSchemaReader

# Initialize reader
reader = TerraformSchemaReader('/path/to/terraform')

# Get repository health configuration
health_config = reader.get_health_config()

# Get repository structure
structure = reader.get_repository_structure('default')

# Get specific checks
ci_checks = reader.get_checks_by_category('ci-cd-status')
```

### Validation

The Terraform configuration is validated on every change:

```bash
# Validate configuration
terraform validate

# Format code
terraform fmt -recursive
```

## Migration from XML/JSON

The following files have been deprecated and removed:
- `schemas/repo-health-default.xml`
- `schemas/repo-health.xsd`
- `schemas/repository-structure.schema.json`
- `schemas/repository-structure.xsd`
- `schemas/unified-repository-schema.json`

All functionality has been migrated to the Terraform-based configuration in this directory.

## Scripts Updated

The following scripts have been updated to use Terraform instead of XML/JSON:

- `scripts/validate/check_repo_health.py` - Now reads from Terraform output
- `scripts/validate/validate_structure.py` - Uses Terraform structure definitions
- `scripts/validate/validate_structure_v2.py` - Updated for Terraform
- `scripts/validate/schema_aware_health_check.py` - Reads Terraform config
- `scripts/validate/validate_repo_health.py` - Uses Terraform health config
- `scripts/validate/generate_stubs.py` - Reads structure from Terraform

## Adding New Repository Types

To add a new repository type:

1. Create a new `.tf` file in `repository-types/`
2. Define locals for metadata, root_files, and directories
3. Add output block to expose configuration
4. Update main.tf to include new repository type
5. Run `terraform fmt` and `terraform validate`
6. Test with validation scripts

## Schema Version

Current schema version: **2.0**

This Terraform-based schema system is version 2.0, representing a complete rewrite of the previous XML/JSON schema system (version 1.x).

## Maintenance

- Configuration files are formatted with `terraform fmt`
- Changes are validated with `terraform validate`
- All changes are version controlled in git
- Breaking changes require a schema version bump

## Documentation

For more information, see:
- [MokoStandards Documentation](../docs/)
- [Repository Structure Guide](../docs/guide/structure/)
- [Health Scoring Guide](../docs/guide/validation/)

---

**Migration Date**: January 2026  
**Schema Version**: 2.0  
**Maintainer**: MokoStandards Team
