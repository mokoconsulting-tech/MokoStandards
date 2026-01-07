# MokoCRM Repository Templates

Repository templates for MokoCRM (Dolibarr-based) projects.

## Available Templates

### Module Template

Complete structure for developing custom Dolibarr modules for MokoCRM.

**Location**: `crm/module/`

**Includes**:
- Module directory structure
- Makefile for build automation
- Standard configuration files (.editorconfig, .gitignore, etc.)
- Documentation templates

**Use Case**: Creating new MokoCRM modules

## Using These Templates

### Option 1: Copy Template

```bash
# Copy the template
cp -r templates/repos/crm/module/ ~/projects/mymodule/

# Update configuration
cd ~/projects/mymodule
# Edit Makefile with your module details

# Initialize git
git init
git add .
git commit -m "Initial commit from MokoStandards template"
```

### Option 2: GitHub Template Repository

If these templates are in a GitHub template repository:

1. Click "Use this template" on GitHub
2. Create your new repository
3. Clone and start developing

### Option 3: Side-Load Build Tools

Keep your existing repo structure and use MokoStandards build tools:

```bash
cd ~/projects/myexistingmodule

# Initialize .moko directory with side-loaded Makefile
python3 /path/to/MokoStandards/scripts/build/resolve_makefile.py --init

# Use moko-make
make -f .moko/Makefile build
```

## Customization

After copying a template:

1. **Update Makefile**:
   - Set `MODULE_NAME`
   - Set `MODULE_VERSION`
   - Set `MODULE_NUMBER` (reserve via PR)
   - Update paths if needed

2. **Update README.md**:
   - Replace with your module description
   - Update installation instructions
   - Add module-specific documentation

3. **Configure Git**:
   - Review and customize `.gitignore`
   - Update `.gitattributes` if needed
   - Set up `.gitmessage` for commit templates

## Resources

- [CRM Development Standards](../../docs/policy/crm/development-standards.md)
- [MokoCRM Client Deployment](../../docs/policy/crm/client-deployment.md)
- [Dolibarr Development Guide](../../docs/guide/crm/dolibarr-development-guide.md)
- [Coding Style Guide](../../docs/policy/coding-style-guide.md)
- [Branching Strategy](../../docs/policy/branching-strategy.md)
