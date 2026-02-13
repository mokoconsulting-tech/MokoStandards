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

If you were using the old XML/JSON schemas in your scripts, update to use the new Terraform-based approach with PHP:

**Old approach (Python with XML):**
```python
from xml.etree import ElementTree as ET

tree = ET.parse('schemas/repo-health-default.xml')
root = tree.getroot()
# Parse XML...
```

**New approach (PHP with Terraform):**
```php
<?php
require_once 'vendor/autoload.php';

use MokoStandards\Enterprise\RepositoryHealthChecker;

$checker = new RepositoryHealthChecker();
$config = $checker->getHealthConfig();
// Use config array directly
```

### Updated Scripts

The following scripts have been updated to use PHP with Terraform:

- ✅ `scripts/validate/check_repo_health.php` - PHP script using Terraform config
- ✅ `scripts/validate/check_enterprise_readiness.php` - PHP enterprise validation
- ✅ `scripts/automation/bulk_update_repos.php` - PHP repository synchronization

**Note**: All validation scripts have been migrated to PHP. Python scripts were removed in February 2026.

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

**Last Updated**: February 2026
**Migration Status**: Complete (PHP-Only)  
**Schema Version**: 2.0 (Terraform-based)
