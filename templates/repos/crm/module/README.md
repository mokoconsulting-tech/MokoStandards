# MokoCRM Module Repository Template

This is a template repository structure for MokoCRM (Dolibarr-based) custom modules.

## Structure

```
module/
├── admin/           # Backend administration files
├── class/           # Business object classes
├── core/            # Module descriptor
│   └── modules/
├── img/             # Module icons
├── langs/           # Translations
├── lib/             # Helper libraries
├── sql/             # Database schemas
├── docs/            # Documentation
├── scripts/         # Build and automation scripts
├── src/             # Source code (if needed)
├── Makefile         # Build automation
└── README.md        # Module documentation
```

## Usage

1. Copy this template to your new repository
2. Update `Makefile` with your module details:
   - `MODULE_NAME`
   - `MODULE_VERSION`
   - `MODULE_NUMBER` (reserve via PR to MokoStandards)
3. Follow the [MokoCRM Development Guide](../../../docs/guide/crm/dolibarr-development-guide.md)

## Build Commands

```bash
make help              # Show all available commands
make validate          # Run code validation
make build             # Build distribution package
make dev-install       # Create development symlink
make test              # Run tests
```

## Resources

- [CRM Development Standards](../../../docs/policy/crm/development-standards.md)
- [Dolibarr Development Guide](../../../docs/guide/crm/dolibarr-development-guide.md)
- [Coding Style Guide](../../../docs/policy/coding-style-guide.md)
