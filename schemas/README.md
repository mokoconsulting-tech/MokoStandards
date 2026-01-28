# Schema Directory - DEPRECATED

## ⚠️ NOTICE: This Directory Has Been Deprecated

**Date**: January 2026  
**Status**: DEPRECATED - Do not use

## Migration to Terraform

The schema system has been migrated from XML/JSON to Terraform for better infrastructure-as-code practices.

### What Changed

The following legacy schema files have been **removed**:

- ~~`repo-health-default.xml`~~ → Migrated to `terraform/repository-types/repo-health-defaults.tf`
- ~~`repo-health.xsd`~~ → No longer needed (Terraform provides type safety)
- ~~`repository-structure.schema.json`~~ → Migrated to `terraform/repository-types/default-repository.tf`
- ~~`repository-structure.xsd`~~ → No longer needed (Terraform provides validation)
- ~~`unified-repository-schema.json`~~ → Migrated to Terraform configuration

### Where to Find Schemas Now

All schema definitions have been moved to **Terraform configuration**:

```
terraform/
├── repository-types/
│   ├── repo-health-defaults.tf      # Health check configuration
│   └── default-repository.tf        # Repository structure definitions
├── main.tf                          # Main configuration
├── variables.tf                     # Input variables
└── outputs.tf                       # Output definitions
```

### For Script Developers

If you were using the old XML/JSON schemas in your scripts, update to use the new Terraform-based approach:

**Old approach (XML):**
```python
from xml.etree import ElementTree as ET

tree = ET.parse('schemas/repo-health-default.xml')
root = tree.getroot()
# Parse XML...
```

**New approach (Terraform):**
```python
from terraform_schema_reader import TerraformSchemaReader

reader = TerraformSchemaReader()
config = reader.get_health_config()
# Use config dictionary directly
```

### Updated Scripts

The following scripts have been updated to use Terraform:

- ✅ `scripts/validate/check_repo_health.py` - Uses `TerraformSchemaReader`
- ✅ `scripts/lib/terraform_schema_reader.py` - New helper module

Scripts still being updated:
- 🔄 `scripts/validate/validate_structure.py`
- 🔄 `scripts/validate/validate_structure_v2.py`
- 🔄 `scripts/validate/schema_aware_health_check.py`
- 🔄 `scripts/validate/validate_repo_health.py`
- 🔄 `scripts/validate/generate_stubs.py`

### Documentation

For complete documentation on the new Terraform-based schema system, see:

- [Terraform README](../terraform/README.md)
- [Migration Guide](../docs/migration/xml-to-terraform.md)
- [Schema Guide](../docs/schemas/terraform-schemas.md)

### Benefits of Terraform

The migration to Terraform provides:

1. **Infrastructure as Code**: Treat schemas like infrastructure
2. **Type Safety**: Built-in validation and type checking
3. **Version Control**: Better diff and merge support
4. **Tooling**: Terraform ecosystem tools (fmt, validate, plan)
5. **Modularity**: Reusable modules and compositions
6. **Community**: Standard IaC approach used industry-wide

## Questions?

If you have questions about the migration or need help updating your scripts, please:

1. Read the [Terraform README](../terraform/README.md)
2. Check the [migration documentation](../docs/migration/)
3. Open an issue in the repository

---

**Last Updated**: January 2026  
**Migration Status**: Complete  
**Schema Version**: 2.0 (Terraform-based)
