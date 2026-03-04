# Makefile Templates

This directory contains Makefile templates for different repository types.

## Template Files

### Makefile.generic.template
Generic Makefile for standard repositories. Includes common targets for:
- Building and compiling
- Testing and linting
- Cleaning and maintenance
- Development workflow automation

**Usage:**
```bash
cp templates/makefiles/Makefile.generic.template ./Makefile
```

### Makefile.joomla.template
Joomla-specific Makefile for extensions (components, modules, plugins, etc.). Includes targets for:
- Joomla manifest validation
- Extension packaging
- Installation and deployment
- Testing with Joomla framework
- Build artifact creation

**Usage:**
```bash
cp templates/makefiles/Makefile.joomla.template ./Makefile
```

### Makefile.dolibarr.template
Dolibarr-specific Makefile for modules. Includes targets for:
- Module descriptor validation
- SQL migration management
- Module packaging
- Installation and deployment
- Testing with Dolibarr framework
- Build artifact creation

**Usage:**
```bash
cp templates/makefiles/Makefile.dolibarr.template ./Makefile
```

## Template Naming Convention

All Makefile templates use the `.template` extension to clearly distinguish them from active Makefile files. When copying to your repository:

1. **Remove the .template extension**: `Makefile.generic.template` → `Makefile`
2. **Customize for your project**: Update variables and targets as needed
3. **Test the targets**: Run `make help` to see available targets

## Customization

After copying a template:

1. Update project-specific variables at the top of the Makefile
2. Modify paths to match your repository structure
3. Add or remove targets based on your needs
4. Update dependencies between targets if necessary

## Schema Integration

These Makefile templates are referenced in the repository structure schemas:

- **default-repository.xml**: Uses `Makefile.generic.template` (suggested)
- **waas-component.xml**: Uses `Makefile.joomla.template` (required)
- **crm-module.xml**: Uses `Makefile.dolibarr.template` (required)

The schemas define source/destination mappings that automatically convert `.template` extensions to the final `Makefile` name.

## Common Targets

Most templates include these standard targets:

- `make help` - Display available targets
- `make build` - Build the project
- `make test` - Run tests
- `make lint` - Run linters
- `make clean` - Clean build artifacts
- `make install` - Install dependencies
- `make package` - Create distribution package

Platform-specific templates may include additional targets relevant to their ecosystem.

## Support

For questions or issues with Makefile templates:
- See main MokoStandards documentation
- Check the platform-specific guides (Joomla, Dolibarr)
- Review the schema documentation for source/destination details
