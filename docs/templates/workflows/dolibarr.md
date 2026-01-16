# Dolibarr Workflow Templates

## Overview

Dolibarr workflow templates provide specialized CI/CD configurations for Dolibarr ERP/CRM modules. These templates ensure Dolibarr-specific compliance, module structure validation, and integration with the Dolibarr ecosystem.

## Available Templates

### 1. Dolibarr CI (`ci-dolibarr.yml.template`)

**Location**: `templates/workflows/dolibarr/ci-dolibarr.yml.template`

**Purpose**: Continuous integration workflow specifically designed for Dolibarr modules

**Features**:
- Module descriptor validation (`modYourModule.class.php`)
- Module structure validation
- PHP syntax validation (Dolibarr-compatible versions)
- SQL file validation
- Database migration checks
- Dolibarr coding standards
- Module number uniqueness check
- Hook implementation validation
- Permission class validation

**Usage**:
```bash
cp templates/workflows/dolibarr/ci-dolibarr.yml.template .github/workflows/ci.yml
```

**Customization Points**:
- PHP version matrix (default: 7.4, 8.0, 8.1, 8.2)
- Dolibarr version compatibility
- Module descriptor location
- Custom validation scripts
- SQL migration validation

**Triggers**:
- Push to `main`, `master`, `dev` branches
- Pull requests to `main` and `master`
- Manual workflow dispatch

**Dolibarr-Specific Validations**:
1. **Module Descriptor**: Validates class extends `DolibarrModules`
2. **Module Number**: Checks `$this->numero` uniqueness
3. **SQL Scripts**: Validates SQL install/upgrade scripts
4. **Directory Structure**: core/modules/, class/, langs/, sql/
5. **Permissions**: Validates `$this->rights_class` structure

---

### 2. Testing (`test.yml.template`)

**Location**: `templates/workflows/dolibarr/test.yml.template`

**Purpose**: Comprehensive testing for Dolibarr modules with PHPUnit and Dolibarr integration

**Features**:
- PHPUnit test execution with Dolibarr test framework
- Integration with Dolibarr database
- Code coverage reporting
- Multiple Dolibarr version matrix testing
- Database testing (MySQL, MariaDB, PostgreSQL)
- Module activation testing
- Hook execution testing
- API endpoint testing

**Usage**:
```bash
cp templates/workflows/dolibarr/test.yml.template .github/workflows/test.yml
```

**Customization Points**:
- Dolibarr version matrix (12.x, 13.x, 14.x, 15.x+)
- PHP version compatibility
- Database configuration
- Test suites (unit, integration, module)
- Code coverage threshold

**Triggers**:
- Push to any branch
- Pull requests
- Scheduled (nightly)

**Requirements**:
- PHPUnit configuration file (`phpunit.xml`)
- Test classes in `test/` directory
- Dolibarr test environment setup

---

### 3. Release (`release.yml.template`)

**Location**: `templates/workflows/dolibarr/release.yml.template`

**Purpose**: Automated release workflow for creating and publishing Dolibarr module packages

**Features**:
- Module package creation (.zip)
- Module descriptor validation before packaging
- Automatic version tagging
- GitHub Release creation
- Module info XML generation
- Package checksums (MD5, SHA256)
- Release notes from CHANGELOG
- Dolistore submission preparation

**Usage**:
```bash
cp templates/workflows/dolibarr/release.yml.template .github/workflows/release.yml
```

**Customization Points**:
- Package naming convention
- Files/directories to include/exclude
- Module info XML configuration
- Release asset naming
- Dolistore metadata

**Triggers**:
- Push to version tags (`v*.*.*`)
- Manual workflow dispatch with version parameter

**Package Structure**:
```
module-package.zip
├── core/
│   └── modules/
│       └── modYourModule.class.php
├── class/
├── langs/
│   ├── en_US/
│   └── fr_FR/
├── sql/
│   ├── llx_yourmodule.sql
│   └── llx_yourmodule.key.sql
├── admin/
├── lib/
├── css/
├── js/
└── img/
```

---

## Dolibarr Module Structure

Templates support standard Dolibarr module structure:

### Required Components

1. **Module Descriptor** (`core/modules/modYourModule.class.php`)
   - Extends `DolibarrModules`
   - Defines module properties
   - Configures permissions
   - Sets up hooks

2. **Class Files** (`class/`)
   - Business logic classes
   - Database table classes
   - API classes

3. **Language Files** (`langs/`)
   - Translation files per language
   - Format: `yourmodule.lang`

4. **SQL Files** (`sql/`)
   - Table creation scripts
   - Table key/index scripts
   - Data files
   - Migration scripts

5. **Admin Pages** (`admin/`)
   - Module configuration
   - Setup pages
   - About page

### Optional Components

- **Library Files** (`lib/`) - Helper functions
- **CSS Files** (`css/`) - Stylesheets
- **JavaScript Files** (`js/`) - Client-side scripts
- **Images** (`img/`) - Module icons and graphics
- **Documentation** (`doc/`) - Module documentation
- **Test Files** (`test/`) - PHPUnit tests

## Module Descriptor Structure

Example `modYourModule.class.php`:

```php
<?php
class modYourModule extends DolibarrModules
{
    public function __construct($db)
    {
        parent::__construct($db);
        
        $this->numero = 123456; // Unique module number
        $this->rights_class = 'yourmodule';
        
        $this->family = "crm";
        $this->module_position = '90';
        $this->name = preg_replace('/^mod/i', '', get_class($this));
        $this->description = "Module description";
        
        $this->version = '1.0.0';
        $this->const_name = 'MAIN_MODULE_'.strtoupper($this->name);
        
        // Permissions
        $this->rights = array();
        $r = 0;
        
        $this->rights[$r][0] = $this->numero . sprintf("%02d", $r+1);
        $this->rights[$r][1] = 'Read objects';
        $this->rights[$r][3] = 0;
        $this->rights[$r][4] = 'read';
        $r++;
    }
}
```

## Common Configuration

### Secrets Required

Dolibarr templates may require:

- `GITHUB_TOKEN`: Automatically provided
- `DOLISTORE_TOKEN`: For Dolistore submissions (optional)
- `DOLIBARR_DB_CREDENTIALS`: For integration testing
- `DEPLOY_CREDENTIALS`: For module deployment

### Environment Variables

Common Dolibarr-specific environment variables:

- `DOLIBARR_VERSION`: Target Dolibarr version (default: 15.0)
- `PHP_VERSION`: PHP version compatible with Dolibarr
- `MODULE_NAME`: Module name without 'mod' prefix
- `MODULE_NUMBER`: Unique module number
- `DOLIBARR_DB`: Database type (mysql, mysqli, pgsql)

### Directory Structure

Expected Dolibarr module structure:

```
dolibarr-module/
├── core/
│   └── modules/
│       └── modYourModule.class.php
├── class/
│   └── yourclass.class.php
├── langs/
│   ├── en_US/
│   │   └── yourmodule.lang
│   └── fr_FR/
│       └── yourmodule.lang
├── sql/
│   ├── llx_yourmodule.sql
│   ├── llx_yourmodule.key.sql
│   └── data.sql
├── admin/
│   ├── setup.php
│   └── about.php
├── lib/
│   └── yourmodule.lib.php
├── css/
│   └── yourmodule.css
├── js/
│   └── yourmodule.js
├── img/
│   └── object_yourmodule.png
├── test/
│   └── YourClassTest.php
├── doc/
│   └── README.md
├── CHANGELOG.md
└── README.md
```

## Dolibarr Coding Standards

Templates enforce Dolibarr coding standards:

1. **File Headers**: GPL license header required
2. **Naming Conventions**: 
   - Classes: PascalCase
   - Functions: camelCase
   - Database tables: llx_ prefix
3. **Database**: Use $db->query() and prepared statements
4. **Language**: Use $langs->trans() for all text
5. **Permissions**: Check user permissions before actions
6. **Hooks**: Use hooks for extensibility

## Module Number Registry

Dolibarr requires unique module numbers:

- **Range**: 100000 - 999999
- **Registry**: Check [Dolibarr module numbers](https://wiki.dolibarr.org/index.php/List_of_modules_numbers)
- **Validation**: CI workflow validates uniqueness

## SQL Migration Best Practices

1. **Naming**: `llx_yourmodule_tablename.sql`
2. **Keys**: Separate file `llx_yourmodule_tablename.key.sql`
3. **Upgrades**: Version-specific in `sql/` directory
4. **Rollback**: Provide uninstall scripts
5. **Charset**: UTF-8 with utf8mb4 for MySQL

## Integration with Dolistore

### Module Info XML

Templates generate module info for Dolistore:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module>
    <name>YourModule</name>
    <version>1.0.0</version>
    <description>Module description</description>
    <editor>Your Company</editor>
    <url>https://github.com/yourorg/yourmodule</url>
    <dolibarr_min>12.0</dolibarr_min>
    <php_min>7.4</php_min>
</module>
```

## Best Practices

1. **Module Number**: Register unique number before development
2. **Version Consistency**: Keep version aligned across descriptor, CHANGELOG, and tags
3. **Test on Multiple Dolibarr Versions**: Use matrix testing
4. **SQL Migrations**: Test install, upgrade, and uninstall scripts
5. **Permissions**: Define granular permissions for module features
6. **Hooks**: Use hooks instead of modifying core files
7. **Languages**: Provide at least en_US and fr_FR translations
8. **Database Tables**: Use llx_ prefix for all tables

## Troubleshooting

### Common Issues

**Issue**: Module descriptor validation fails

**Solution**:
- Ensure class extends DolibarrModules
- Check $this->numero is unique
- Verify all required properties set
- Check constructor calls parent::__construct()

**Issue**: SQL migration fails

**Solution**:
- Validate SQL syntax
- Check table name uses llx_ prefix
- Ensure charset is utf8mb4
- Test on clean database

**Issue**: Module number conflict

**Solution**:
- Check Dolibarr module number registry
- Choose number in available range
- Update $this->numero in descriptor
- Register your number

**Issue**: Permission issues

**Solution**:
- Verify $this->rights_class is set
- Check permissions array is correct
- Test with different user permission levels
- Use $user->rights->yourmodule->action

## Examples

### Example 1: Basic Module Setup

```bash
# Copy Dolibarr CI template
cp templates/workflows/dolibarr/ci-dolibarr.yml.template .github/workflows/ci.yml

# Copy testing template
cp templates/workflows/dolibarr/test.yml.template .github/workflows/test.yml

# Copy release template
cp templates/workflows/dolibarr/release.yml.template .github/workflows/release.yml

# Customize ci.yml for your module
# - Set module name
# - Configure module number
# - Add custom validation
```

### Example 2: Testing Setup

```bash
# Create test directory structure
mkdir -p test/phpunit

# Add PHPUnit configuration
cat > phpunit.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="test/bootstrap.php">
    <testsuites>
        <testsuite name="Module Tests">
            <directory>test</directory>
        </testsuite>
    </testsuites>
</phpunit>
EOF

# Copy test template
cp templates/workflows/dolibarr/test.yml.template .github/workflows/test.yml
```

### Example 3: Release Process

```bash
# 1. Update version in module descriptor
# 2. Update CHANGELOG.md
# 3. Commit changes
# 4. Push version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 5. Release workflow triggers automatically
# 6. Module package is created
# 7. GitHub Release is published
# 8. Module info XML is generated
```

## Additional Resources

- [Dolibarr Developer Documentation](https://wiki.dolibarr.org/index.php/Developer_documentation)
- [Module Development](https://wiki.dolibarr.org/index.php/Module_development)
- [Dolibarr Coding Standards](https://wiki.dolibarr.org/index.php/Coding_standards)
- [Module Numbers Registry](https://wiki.dolibarr.org/index.php/List_of_modules_numbers)
- [Dolistore](https://www.dolistore.com/)
- [Template Source Files](../../../templates/workflows/dolibarr/)
- [Main Workflows Index](./index.md)

---

**Last Updated**: 2026-01-16  
**Category**: Dolibarr Templates  
**Dolibarr Versions**: 12.x, 13.x, 14.x, 15.x+  
**Maintained By**: MokoStandards Team
