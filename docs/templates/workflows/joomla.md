# Joomla Workflow Templates

## Overview

Joomla workflow templates provide specialized CI/CD configurations for Joomla extensions including components, modules, plugins, libraries, templates, and packages. These templates ensure Joomla-specific compliance and quality standards.

## Available Templates

### 1. Joomla CI (`ci-joomla.yml.template`)

**Location**: `templates/workflows/joomla/ci-joomla.yml.template`

**Purpose**: Continuous integration workflow specifically designed for Joomla extensions

**Features**:
- Joomla manifest validation (XML structure and required fields)
- XML well-formedness checking
- PHP syntax validation (Joomla-compatible versions)
- CHANGELOG structure validation
- License header verification
- Version alignment checks (manifest vs CHANGELOG)
- Tab character detection
- Path separator validation
- Secret scanning
- Extension type detection (component, module, plugin, etc.)

**Usage**:
```bash
cp templates/workflows/joomla/ci-joomla.yml.template .github/workflows/ci.yml
```

**Customization Points**:
- PHP version matrix (default: 7.4, 8.0, 8.1)
- Joomla version compatibility
- Manifest file location
- Custom validation scripts
- Extension-specific checks

**Triggers**:
- Push to `main`, `master`, `dev` branches
- Pull requests to `main` and `master`
- Manual workflow dispatch

**Joomla-Specific Validations**:
1. **Manifest Structure**: Validates `<extension>` root element
2. **Required Fields**: name, version, author, license, description
3. **File References**: Verifies all files listed in manifest exist
4. **Joomla API**: Checks for deprecated API usage
5. **Extension Type**: Validates type attribute (component, module, plugin, etc.)

---

### 2. Testing (`test.yml.template`)

**Location**: `templates/workflows/joomla/test.yml.template`

**Purpose**: Comprehensive testing for Joomla extensions with PHPUnit and Joomla framework

**Features**:
- PHPUnit test execution with Joomla test framework
- Code coverage reporting
- Integration with Joomla CMS environment
- Multiple Joomla version matrix testing
- Database testing (MySQL, PostgreSQL)
- Frontend/backend testing
- API endpoint testing

**Usage**:
```bash
cp templates/workflows/joomla/test.yml.template .github/workflows/test.yml
```

**Customization Points**:
- Joomla version matrix (3.x, 4.x, 5.x)
- PHP version compatibility
- Database configuration
- Test suites (unit, integration, e2e)
- Code coverage threshold

**Triggers**:
- Push to any branch
- Pull requests
- Scheduled (nightly)

**Requirements**:
- PHPUnit configuration file (`phpunit.xml`)
- Test classes in `tests/` directory
- Joomla test framework dependency

---

### 3. Release (`release.yml.template`)

**Location**: `templates/workflows/joomla/release.yml.template`

**Purpose**: Automated release workflow for creating and publishing Joomla extension packages

**Features**:
- Extension package creation (.zip)
- Manifest validation before packaging
- Automatic version tagging
- GitHub Release creation
- Update server XML generation
- Package checksums (MD5, SHA256)
- Release notes from CHANGELOG
- Distribution file upload

**Usage**:
```bash
cp templates/workflows/joomla/release.yml.template .github/workflows/release.yml
```

**Customization Points**:
- Package naming convention
- Files/directories to include/exclude
- Update server configuration
- Release asset naming
- Joomla Update System integration

**Triggers**:
- Push to version tags (`v*.*.*`)
- Manual workflow dispatch with version parameter

**Package Structure**:
```
extension-package.zip
├── manifest.xml
├── script.php (if exists)
├── admin/
├── site/
├── media/
├── language/
└── sql/
```

---

### 4. Repository Health (`repo_health.yml.template`)

**Location**: `templates/workflows/joomla/repo_health.yml.template`

**Purpose**: Repository health monitoring specifically for Joomla extensions

**Features**:
- Joomla manifest presence check
- Required Joomla-specific files validation
- Documentation completeness (README, CHANGELOG, CONTRIBUTING)
- License compliance (GPL compatible)
- Joomla coding standards validation
- Directory structure validation
- Update server XML validation

**Usage**:
```bash
cp templates/workflows/joomla/repo_health.yml.template .github/workflows/repo-health.yml
```

**Customization Points**:
- Required files list
- Joomla version compatibility requirements
- Documentation standards
- Custom health checks

**Triggers**:
- Push to main branches
- Weekly schedule
- Manual dispatch

**Joomla-Specific Checks**:
- Manifest XML validity
- Extension type appropriate directory structure
- Language files presence
- SQL install/update scripts
- Media assets organization

---

### 5. Version Branch (`version_branch.yml.template`)

**Location**: `templates/workflows/joomla/version_branch.yml.template`

**Purpose**: Automated version branch management and release preparation for Joomla extensions

**Features**:
- Automatic version branch creation
- CHANGELOG version updates
- Manifest version updates
- Release preparation automation
- Version tagging
- Branch protection setup

**Usage**:
```bash
cp templates/workflows/joomla/version_branch.yml.template .github/workflows/version-branch.yml
```

**Customization Points**:
- Version numbering scheme (semantic versioning)
- Branch naming convention
- Files to update with version
- Pre-release tasks

**Triggers**:
- Manual workflow dispatch with version parameter
- Push to `dev` branch (automatic minor version bump)

**Workflow**:
1. Create version branch from `dev`
2. Update version in manifest and CHANGELOG
3. Run validation checks
4. Create pull request to `main`
5. Tag after merge

---

## Joomla Extension Types

Templates support all Joomla extension types:

### Components (`com_*`)
- Admin and site directories
- Installation SQL
- Uninstallation SQL
- Component manifest

### Modules (`mod_*`)
- Module files (tmpl, helper)
- Module manifest
- Language files
- Module media

### Plugins (`plg_*`)
- Plugin group directory
- Plugin PHP file
- Plugin manifest
- Event handlers

### Libraries (`lib_*`)
- Library manifest
- Library files
- Autoloader configuration

### Templates (`tpl_*`)
- Template HTML files
- Template CSS/JS
- Template manifest
- Template parameters

### Packages (`pkg_*`)
- Package manifest
- Sub-extension packages
- Installation script

## Common Configuration

### Secrets Required

Joomla templates may require:

- `GITHUB_TOKEN`: Automatically provided
- `JED_TOKEN`: For Joomla Extensions Directory submissions (optional)
- `UPDATE_SERVER_TOKEN`: For update server authentication
- `FTP_CREDENTIALS`: For deployment workflows

### Environment Variables

Common Joomla-specific environment variables:

- `JOOMLA_VERSION`: Target Joomla version (default: 4.2)
- `PHP_VERSION`: PHP version compatible with Joomla
- `EXTENSION_TYPE`: component, module, plugin, library, template, package
- `EXTENSION_NAME`: Extension name without prefix
- `JOOMLA_DB`: Database type (mysql, postgresql)

### Directory Structure

Expected Joomla extension structure:

```
joomla-extension/
├── manifest.xml (or com_name.xml, mod_name.xml, etc.)
├── script.php (installation script)
├── admin/ (for components)
│   ├── sql/
│   ├── language/
│   └── ...
├── site/ (for components)
│   ├── views/
│   ├── models/
│   └── ...
├── media/
│   ├── css/
│   ├── js/
│   └── images/
├── language/
│   ├── en-GB/
│   └── ...
└── sql/
    ├── install.mysql.utf8.sql
    └── updates/
```

## Joomla Coding Standards

Templates enforce Joomla coding standards:

1. **PHP Code Sniffer**: Joomla ruleset
2. **Naming Conventions**: PascalCase for classes, camelCase for methods
3. **File Headers**: GPL license header
4. **Documentation**: PHPDoc blocks
5. **Database**: JDatabase API usage
6. **Language**: Language string constants

## Integration with Joomla Update System

### Update Server XML

Templates generate update server XML for Joomla's update system:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<updates>
  <update>
    <name>Extension Name</name>
    <description>Extension description</description>
    <element>com_extension</element>
    <type>component</type>
    <version>1.0.0</version>
    <downloads>
      <downloadurl type="full" format="zip">
        https://github.com/owner/repo/releases/download/v1.0.0/extension.zip
      </downloadurl>
    </downloads>
    <maintainer>Maintainer Name</maintainer>
    <maintainerurl>https://example.com</maintainerurl>
    <targetplatform name="joomla" version="4.*"/>
  </update>
</updates>
```

## Best Practices

1. **Manifest First**: Always validate manifest before any other checks
2. **Version Consistency**: Keep version aligned across manifest, CHANGELOG, and tags
3. **Test on Multiple Joomla Versions**: Use matrix testing for compatibility
4. **Package Testing**: Test packaged extension installation before release
5. **Update Server**: Maintain update server XML for easy updates
6. **Joomla Coding Standards**: Follow official Joomla coding standards
7. **Language Packs**: Include at least en-GB language files
8. **SQL Migrations**: Provide proper SQL install and update scripts

## Troubleshooting

### Common Issues

**Issue**: Manifest validation fails

**Solution**:
- Check XML syntax with validator
- Ensure all required fields present
- Verify file references exist
- Check extension type attribute

**Issue**: Package creation fails

**Solution**:
- Verify all referenced files exist
- Check file permissions
- Ensure manifest file is in correct location
- Review exclusion patterns

**Issue**: Joomla version compatibility errors

**Solution**:
- Update manifest `targetplatform` version
- Check PHP version compatibility
- Review deprecated API usage
- Test with target Joomla version

**Issue**: Update server not working

**Solution**:
- Validate update XML syntax
- Check downloadurl accessibility
- Verify checksums match
- Ensure correct element name

## Examples

### Example 1: Component Setup

```bash
# Copy Joomla CI template
cp templates/workflows/joomla/ci-joomla.yml.template .github/workflows/ci.yml

# Copy testing template
cp templates/workflows/joomla/test.yml.template .github/workflows/test.yml

# Copy release template
cp templates/workflows/joomla/release.yml.template .github/workflows/release.yml

# Customize ci.yml for your component
# - Set component name
# - Configure PHP versions
# - Add custom validation
```

### Example 2: Module Setup

```bash
# Copy Joomla CI template
cp templates/workflows/joomla/ci-joomla.yml.template .github/workflows/ci.yml

# Customize for module
# - Update manifest path (mod_yourmodule.xml)
# - Remove component-specific checks
# - Add module-specific validation
```

### Example 3: Release Process

```bash
# 1. Update version in manifest and CHANGELOG
# 2. Commit changes
# 3. Push version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 4. Release workflow triggers automatically
# 5. Package is created and uploaded to GitHub Releases
# 6. Update server XML is generated
```

## Additional Resources

- [Joomla Developer Documentation](https://docs.joomla.org/Portal:Development)
- [Joomla Coding Standards](https://developer.joomla.org/coding-standards.html)
- [Joomla Extension Development](https://docs.joomla.org/Category:Extension_Development)
- [Joomla Update System](https://docs.joomla.org/Deploying_an_Update_Server)
- [Template Source Files](../../../templates/workflows/joomla/)
- [Main Workflows Index](./index.md)

---

**Last Updated**: 2026-01-16  
**Category**: Joomla Templates  
**Joomla Versions**: 3.x, 4.x, 5.x  
**Maintained By**: MokoStandards Team
