# MokoWaaS Repository Templates

Repository templates for MokoWaaS (Joomla-based) projects.

## Available Templates

### Component Template
Complete structure for developing Joomla components for MokoWaaS.

**Location**: `waas/component/`

**Includes**: Makefile, directory structure, configuration files

### Module Template
Structure for developing Joomla modules (frontend or backend) for MokoWaaS.

**Location**: `waas/module/`

**Includes**: Makefile, directory structure, configuration files

### Plugin Template
Structure for developing Joomla plugins for MokoWaaS.

**Location**: `waas/plugin/`

**Includes**: Makefile, directory structure, configuration files

### Template Template
Structure for developing Joomla site templates for MokoWaaS.

**Location**: `waas/template/`

## Using These Templates

### Option 1: Copy Template

```bash
# Copy the appropriate template
cp -r templates/repos/waas/component/ ~/projects/com_mycomponent/

# Update configuration
cd ~/projects/com_mycomponent
# Edit Makefile with your extension details

# Initialize git
git init
git add .
git commit -m "Initial commit from MokoStandards template"
```

### Option 2: Side-Load Build Tools

```bash
cd ~/projects/myexistingextension

# Initialize .moko directory with side-loaded Makefile
python3 /path/to/MokoStandards/scripts/build/resolve_makefile.py --init

# Use moko-make wrapper
/path/to/MokoStandards/scripts/build/moko-make build
```

## Customization

After copying a template:

1. **Update Makefile**:
   - Set extension name (`COMPONENT_NAME`, `MODULE_NAME`, etc.)
   - Set version (`COMPONENT_VERSION`)
   - Update author information
   - Configure paths if needed

2. **Update manifest XML**:
   - Replace extension details
   - Update author, license, description
   - Configure installation files

3. **Configure Git**:
   - Review `.gitignore`
   - Set up `.gitmessage` for commit templates

## Resources

- [WaaS Development Standards](../../docs/policy/waas/development-standards.md)
- [Joomla Development Guide](../../docs/guide/waas/joomla-development-guide.md)
- [Coding Style Guide](../../docs/policy/coding-style-guide.md)
- [Branching Strategy](../../docs/policy/branching-strategy.md)
