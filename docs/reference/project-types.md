# Project Type Detection

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

MokoStandards workflows automatically detect project types to apply appropriate validation, testing, and deployment procedures. This document explains the detection logic and platform-specific requirements for Joomla (MokoWaaS) and Dolibarr (MokoCRM) projects.

## Detection Priority

Project type detection follows this priority order:

1. **Joomla** - Detected first (if indicators present)
2. **Dolibarr** - Detected second (if indicators present)
3. **Generic** - Fallback for all other projects

**Note**: A repository cannot be detected as multiple types simultaneously. The first match wins.

## Joomla (MokoWaaS) Detection

### Primary Detection Method

Joomla projects are identified by the presence of a **Joomla XML manifest file**:

```bash
# Detection checks for:
joomla.xml                    # Root-level manifest
*.xml in administrator/       # Backend component manifest
*.xml in components/          # Frontend component manifest
mod_*.xml                     # Module manifest
plg_*.xml                     # Plugin manifest
```

### Extension Type Identification

Once Joomla is detected, the specific extension type is determined:

| Extension Type | Detection Criteria |
|---|---|
| **Component** | `administrator/components/com_*/` or `components/com_*/` directories |
| **Module** | `mod_*.xml` manifest OR `modules/mod_*/` directory |
| **Plugin** | `plg_*.xml` manifest OR `plugins/*/*/` directory structure |
| **Template** | `template.xml` OR `templateDetails.xml` file |
| **Library** | `library.xml` manifest OR `libraries/` directory |
| **Package** | `pkg_*.xml` manifest OR multiple sub-manifests |

### Joomla Directory Structure Indicators

**Component structure**:
```
repository/
├── joomla.xml or com_name.xml
├── administrator/
│   └── components/
│       └── com_name/
├── components/
│   └── com_name/
└── media/
    └── com_name/
```

**Module structure**:
```
repository/
├── mod_name.xml
├── mod_name.php
├── tmpl/
└── language/
```

**Plugin structure**:
```
repository/
├── plg_folder_name.xml
├── name.php
└── language/
```

### Joomla-Specific Requirements

When Joomla is detected, the following validations apply:

| Requirement | Purpose | Validation Script |
|---|---|---|
| XML manifest present | Defines extension metadata | `scripts/validate/manifest.sh` |
| XML well-formed | Ensures parseable manifests | `scripts/validate/xml_wellformed.sh` |
| Version format | NN.NN.NN format enforced | `scripts/validate/version_alignment.sh` |
| Joomla namespace | PSR-4 autoloading check | `scripts/validate/php_syntax.sh` |
| SQL install/update files | Database schema management | Manual review |

### Joomla Workflow Selection

When Joomla is detected, use these workflows:

- **CI**: `templates/workflows/joomla/ci.yml`
- **Testing**: `templates/workflows/joomla/test.yml`
- **Release**: `templates/workflows/joomla/release.yml`
- **Repo Health**: `templates/workflows/joomla/repo_health.yml`

### Joomla Build Process

**Standard Joomla build**:
1. Validate manifests
2. Check XML structure
3. PHP syntax validation (7.4-8.2)
4. Create installable ZIP package
5. Generate checksums (SHA256, MD5)
6. Upload to release distribution

**Package structure**:
```
com_name_1.0.0.zip
├── administrator/
├── components/
├── media/
├── language/
└── name.xml (manifest)
```

## Dolibarr (MokoCRM) Detection

### Primary Detection Method

Dolibarr modules are identified by:

```bash
# Detection checks for:
htdocs/                              # Primary indicator
core/modules/mod*.class.php          # Module descriptor
sql/llx_*.sql or sql/llx_*.key.sql  # Database schema files
```

### Dolibarr Module Structure Indicators

**Standard module structure**:
```
repository/
├── htdocs/
│   ├── custom/
│   │   └── modulename/
│   │       ├── admin/
│   │       ├── class/
│   │       ├── core/
│   │       ├── css/
│   │       ├── js/
│   │       ├── langs/
│   │       └── lib/
├── core/
│   └── modules/
│       └── modModuleName.class.php
└── sql/
    └── llx_modulename_*.sql
```

### Module Descriptor Requirements

The module descriptor file must:

- Be located in `core/modules/`
- Follow naming: `modModuleName.class.php`
- Extend `DolibarrModules` class
- Define module ID (5-6 digits)
- Include version, description, and dependencies

**Example descriptor**:
```php
<?php
class modMokoDoliForm extends DolibarrModules
{
    public function __construct($db)
    {
        global $langs, $conf;
        
        $this->numero = 185056;  // Module ID (reserved in MokoStandards)
        
        // Module family
        $this->family = "mokoconsulting";
        $this->familyinfo = array(
            'mokoconsulting' => array(
                'position' => '01',
                'label'    => $langs->trans("Moko Consulting")
            )
        );
        
        $this->module_position = '50';
        $this->name = preg_replace('/^mod/i', '', get_class($this));
        $this->version = '1.0.0';
        $this->description = "Advanced form builder";
        
        // Author
        $this->editor_name = 'Moko Consulting';
        $this->editor_url = 'https://www.mokoconsulting.tech';
        $this->editor_squarred_logo = 'logo.png@mokodoliForm';
        
        // ... additional configuration
    }
}
```

### Dolibarr-Specific Requirements

When Dolibarr is detected, the following validations apply:

| Requirement | Purpose | Validation Script |
|---|---|---|
| Module descriptor present | Defines module metadata | `scripts/validate/dolibarr_structure.sh` |
| htdocs/ structure | Proper module organization | Manual review |
| Database schema | SQL files for installation | `scripts/validate/sql_syntax.sh` |
| Module ID unique | Prevents conflicts | Module registry check |
| Dolibarr API usage | Version compatibility | `scripts/validate/dolibarr_api.sh` |

### Dolibarr Workflow Selection

When Dolibarr is detected, use these workflows:

- **CI**: `templates/workflows/dolibarr/ci.yml`
- **Testing**: `templates/workflows/dolibarr/test.yml`
- **Repo Health**: `templates/workflows/generic/repo_health.yml` (adapted)

### Dolibarr Build Process

**Standard Dolibarr build**:
1. Validate module descriptor
2. Check htdocs/ structure
3. PHP syntax validation (7.4-8.2)
4. Test with Dolibarr 16.0-18.0
5. Create installable ZIP package
6. Upload to module distribution server

**Package structure**:
```
modulename_1.0.0.zip
├── htdocs/
│   └── custom/
│       └── modulename/
├── core/
│   └── modules/
│       └── modModuleName.class.php
└── sql/
    ├── llx_modulename_table.sql
    └── llx_modulename_table.key.sql
```

### Module ID Registry

All Dolibarr modules must have a reserved module ID in the MokoStandards registry:

**Current Reserved IDs**:
- 185055: MokoDoliPasskey (WebAuthn/Passkey authentication)
- 185056: MokoDoliForm (Form builder and workflow)
- 185057: MokoDoliG (Google Workspace integration)
- 185058: MokoDoliDeploy (Deployment automation)
- 185059-185099: Available for reservation

**Reservation Process**:
1. Request ID in MokoStandards repository
2. Document module purpose
3. Update `docs/policy/crm/development-standards.md`
4. Use reserved ID in module descriptor

## Generic Project Fallback

### When Generic Detection Triggers

Projects are treated as generic when:

- No `joomla.xml` or `*.xml` manifests found
- No `htdocs/` directory or Dolibarr structure
- Multi-language project (Node.js + Python + Go, etc.)
- Non-CMS/ERP project

### Automatic Language Detection

For generic projects, workflows automatically detect languages:

```bash
# Language detection logic
if [ -f "package.json" ]; then
  LANGUAGES+=("nodejs")
fi

if [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  LANGUAGES+=("python")
fi

if [ -f "composer.json" ]; then
  LANGUAGES+=("php")
fi

if [ -f "go.mod" ]; then
  LANGUAGES+=("go")
fi

if [ -f "Gemfile" ]; then
  LANGUAGES+=("ruby")
fi

if [ -f "Cargo.toml" ]; then
  LANGUAGES+=("rust")
fi
```

### Generic Workflow Selection

For generic projects, use:

- **CI**: `templates/workflows/generic/ci.yml`
- **Testing**: `templates/workflows/generic/test.yml`
- **Deployment**: `templates/workflows/generic/deploy.yml`
- **Code Quality**: `templates/workflows/generic/code-quality.yml`
- **Repo Health**: `templates/workflows/generic/repo_health.yml`

### Generic Build Process

Build process adapts to detected languages:

**Node.js**:
```bash
npm ci
npm run build
npm test
```

**Python**:
```bash
pip install -r requirements.txt
python setup.py build
pytest
```

**PHP**:
```bash
composer install
vendor/bin/phpunit
```

**Go**:
```bash
go build ./...
go test ./...
```

**Multi-language**:
```bash
# All applicable language steps run in parallel
```

## Manual Override

### Forcing Project Type

Create `.mokostandards.yml` in repository root to override detection:

```yaml
project_type: joomla
# Options: joomla, dolibarr, generic

joomla:
  extension_type: component
  # Options: component, module, plugin, template, library, package

dolibarr:
  module_id: 185056
  module_name: MokoDoliForm
```

### Disabling Auto-Detection

To skip auto-detection in specific workflows:

```yaml
# In workflow file
env:
  SKIP_DETECTION: "true"
  PROJECT_TYPE: "joomla"
```

## Platform-Specific Features

### Joomla-Specific

**Extension Manager Integration**:
- Installable ZIP packages
- Update server XML for extensions
- Manifest schema validation
- Joomla API version compatibility

**Testing Features**:
- Matrix testing across Joomla 4.4-5.0
- PHPUnit integration with Joomla framework
- Mock Joomla application environment

### Dolibarr-Specific

**Module System Integration**:
- Module activation/deactivation
- Database schema installation
- Dolibarr hooks integration
- Module dependency management

**Testing Features**:
- Matrix testing across Dolibarr 16.0-18.0
- Automatic Dolibarr installation
- Database migrations testing
- Module API compatibility checks

## Detection Best Practices

1. **Use standard structures** - Follow platform conventions
2. **Include required files** - Ensure detection indicators present
3. **Document deviations** - Use `.mokostandards.yml` for custom setups
4. **Test detection** - Run CI workflow to verify correct type
5. **Maintain consistency** - Don't mix platform structures
6. **Update manifests** - Keep version numbers aligned
7. **Reserve module IDs** - For Dolibarr projects
8. **Follow naming conventions** - Platform-specific file naming

## Troubleshooting Detection

### Joomla Not Detected

**Symptoms**: Generic workflows used instead of Joomla workflows

**Solutions**:
1. Verify `joomla.xml` or extension manifest present
2. Check manifest filename matches pattern (e.g., `com_*.xml`, `mod_*.xml`)
3. Ensure XML is well-formed and validates
4. Place manifest in repository root or standard directory
5. Use manual override in `.mokostandards.yml`

### Dolibarr Not Detected

**Symptoms**: Generic workflows used instead of Dolibarr workflows

**Solutions**:
1. Verify `htdocs/` directory exists
2. Check `core/modules/mod*.class.php` present
3. Ensure proper directory structure
4. Add SQL files in `sql/` directory
5. Use manual override in `.mokostandards.yml`

### Wrong Project Type Detected

**Symptoms**: Joomla detected for Dolibarr project (or vice versa)

**Solutions**:
1. Review detection priority (Joomla checked first)
2. Remove conflicting indicators (e.g., stray XML files)
3. Use `.mokostandards.yml` to force correct type
4. Reorganize repository to match platform standards

## Integration with Other Systems

### Health Scoring System

Project type affects scoring criteria:
- Joomla projects scored on extension-specific requirements
- Dolibarr projects scored on module-specific requirements
- Generic projects use language-specific criteria

See [Health Scoring System](health-scoring.md) for details.

### Repository Structure Schema

XML schema validation adapts to project type:
- `scripts/definitions/crm-module.xml` for Dolibarr
- `scripts/definitions/waas-component.xml` for Joomla (future)
- `scripts/definitions/generic-project.xml` for others (future)

See [Repository Structure Schema](guide/repository-structure-schema.md) for details.

### Build Automation

Makefile templates vary by project type:
- `templates/build/dolibarr/Makefile` for Dolibarr
- `templates/build/joomla/Makefile.*` for Joomla
- Generic makefiles for multi-language projects

## Metadata

| Field | Value |
|---|---|
| Document | Project Type Detection |
| Path | /docs/project-types.md |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
| Owner | Moko Consulting |
| Status | Active |
| Version | 01.00.00 |
| Effective | 2026-01-07 |

## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial project type detection documentation |

## See Also

- [Workflow Templates](workflows/README.md)
- [Health Scoring System](health-scoring.md)
- [Repository Structure Schema](guide/repository-structure-schema.md)
- [MokoWaaS Development Standards](policy/waas/development-standards.md)
- [MokoCRM Development Standards](policy/crm/development-standards.md)
- [Dolibarr Development Guide](guide/crm/dolibarr-development-guide.md)
- [Joomla Development Guide](guide/waas/joomla-development-guide.md)
