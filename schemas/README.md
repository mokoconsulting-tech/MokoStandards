# Repository Structure Schemas

This directory contains XML schemas and structure definitions for standardizing repository layouts across Moko Consulting projects.

## Contents

- **repository-structure.xsd** - XML Schema Definition (XSD) that defines the structure format
- **structures/** - Directory containing specific structure definitions for different project types

## Quick Start

### Validate a Repository

```bash
python scripts/validate/validate_structure.py schemas/structures/crm-module.xml .
```

### Generate Stubs for a New Project

```bash
python scripts/validate/generate_stubs.py schemas/structures/crm-module.xml /path/to/new/project --dry-run
```

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

### Validation Tool
- **Location**: `scripts/validate/validate_structure.py`
- **Purpose**: Validate existing repositories
- **Exit Codes**: 0 = pass, 1 = fail (errors found)

### Stub Generation Tool
- **Location**: `scripts/validate/generate_stubs.py`
- **Purpose**: Generate missing files and directories
- **Modes**: Normal, dry-run, force-overwrite

## Integration

### Makefile

```makefile
validate-structure:
	python scripts/validate/validate_structure.py schemas/structures/crm-module.xml .

generate-stubs:
	python scripts/validate/generate_stubs.py schemas/structures/crm-module.xml .
```

### GitHub Actions

```yaml
- name: Validate Structure
  run: python .mokostandards/scripts/validate/validate_structure.py \
         .mokostandards/schemas/structures/crm-module.xml .
```

## Benefits

1. **Consistency**: All projects follow same structure
2. **Automation**: Generate boilerplate automatically
3. **Validation**: Catch structure issues in CI/CD
4. **Documentation**: Self-documenting structure definitions
5. **Onboarding**: New team members understand layout instantly
6. **Quality**: Enforce best practices across all projects

## Support

- Documentation: [docs/guide/repository-structure-schema.md](../docs/guide/repository-structure-schema.md)
- Issues: Open in MokoStandards repository
- Contact: support@mokoconsulting.com

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-07
