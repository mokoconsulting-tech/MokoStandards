[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Project Type Detection

This document describes how the MokoStandards workflows detect project types and adapt validation accordingly.

## Overview

The MokoStandards CI system automatically detects the type of project being validated to apply appropriate checks and tools. This detection happens in the `reusable-project-detector.yml` workflow and is used by `reusable-ci-validation.yml`.

## Detection Priority

Project types are detected in the following priority order:

1. **Joomla** - Highest priority
2. **Dolibarr** - Medium priority
3. **Generic** - Fallback for all other projects

## Joomla Project Detection

### File Markers

A project is identified as **Joomla** if any of these conditions are met:

- Root-level `joomla.xml` file exists
- XML manifest files matching Joomla extension patterns:
  - `mod_*.xml` - Joomla modules
  - `plg_*.xml` - Joomla plugins
  - `com_*.xml` - Joomla components
  - `pkg_*.xml` - Joomla packages
  - `tpl_*.xml` - Joomla templates

### Extension Type Detection

For Joomla projects, the specific extension type is also detected:

| Extension Type | Detection Criteria |
|----------------|-------------------|
| **Component** | Presence of `administrator/components/` or `components/` directories |
| **Module** | Manifest file matching `mod_*.xml` pattern |
| **Plugin** | Manifest file matching `plg_*.xml` pattern |
| **Package** | Manifest file matching `pkg_*.xml` pattern |
| **Template** | Manifest file matching `tpl_*.xml` pattern |
| **Library** | Manifest file matching `lib_*.xml` pattern |

### Validation Applied

- XML manifest validation (structure, required fields)
- Joomla coding standards (via PHP_CodeSniffer with Joomla ruleset)
- PHP syntax validation
- License header validation
- Security scanning

### Example Joomla Project Structure

```
my-joomla-module/
├── mod_mymodule.xml          # Module manifest (detected)
├── mod_mymodule.php          # Entry point
├── helper.php                # Helper class
├── tmpl/
│   └── default.php          # Template
└── language/
    └── en-GB/
        └── en-GB.mod_mymodule.ini
```

## Dolibarr Project Detection

### File Markers

A project is identified as **Dolibarr** if any of these conditions are met:

- Root-level `dolibarr.xml` file exists
- Directory structure matching Dolibarr modules:
  - `core/modules/` directory
  - `admin/` directory with setup files
  - Presence of both `class/` and `core/` directories

### Module Type Detection

For Dolibarr projects, the module type can be detected:

| Module Type | Detection Criteria |
|-------------|-------------------|
| **Standard Module** | Presence of `core/modules/` directory |
| **Trigger Module** | Presence of `core/triggers/` directory |
| **Widget Module** | Presence of `core/boxes/` directory |

### Validation Applied

- PHP syntax validation
- Dolibarr coding standards
- Module structure validation
- License header validation
- Security scanning

### Example Dolibarr Project Structure

```
mymodule/
├── core/
│   ├── modules/
│   │   └── modMyModule.class.php
│   └── triggers/
│       └── interface_99_modMyModule_MyTrigger.class.php
├── class/
│   └── myclass.class.php
├── admin/
│   └── setup.php
└── langs/
    └── en_US/
        └── mymodule.lang
```

## Generic Project Detection

### Fallback Behavior

If a project doesn't match Joomla or Dolibarr patterns, it's treated as a **Generic** project.

### Technology Detection

For generic projects, we still detect specific technologies:

#### PHP Projects

Detected if any of these are present:
- `composer.json` file
- `.php` files in the repository

#### Node.js Projects

Detected if any of these are present:
- `package.json` file
- `node_modules/` directory (if tracked)
- `.js`, `.ts`, `.jsx`, or `.tsx` files

#### Python Projects

Detected if any of these are present:
- `setup.py` or `pyproject.toml`
- `requirements.txt`
- `.py` files in the repository

### Validation Applied

Based on detected technologies:

- **PHP**: Syntax validation, PHP_CodeSniffer (if configured)
- **Node.js**: ESLint (if configured), npm/yarn builds
- **Python**: Syntax validation, pytest (if configured)
- **All**: License headers, security scanning, changelog validation

### Example Generic Project Structure

```
my-generic-project/
├── README.md
├── LICENSE
├── package.json              # Node.js detected
├── composer.json             # PHP detected
├── src/
│   ├── index.js
│   └── MyClass.php
└── tests/
    ├── test.js
    └── MyClassTest.php
```

## Detection Output

The detection workflow outputs the following information:

```yaml
outputs:
  project-type: 'joomla' | 'dolibarr' | 'generic'
  extension-type: 'component' | 'module' | 'plugin' | ...  # For Joomla
  has-php: 'true' | 'false'
  has-node: 'true' | 'false'
  has-python: 'true' | 'false'  # Future enhancement
```

## Best Practices

### For Joomla Extensions

1. **Always include a properly formatted XML manifest**
   - Use standard naming conventions (`mod_`, `plg_`, `com_`, etc.)
   - Include all required fields
   - Validate against Joomla XSD schemas

2. **Follow Joomla directory structure conventions**
   - Place files in standard locations
   - Use correct naming patterns

3. **Include proper metadata**
   - Version information
   - Author details
   - License declaration

### For Dolibarr Modules

1. **Follow Dolibarr module structure**
   - Use `core/modules/` for module classes
   - Include setup files in `admin/`
   - Provide language files

2. **Implement required classes**
   - Module descriptor class
   - Trigger classes if needed
   - Widget classes if applicable

### For Generic Projects

1. **Clearly indicate technologies used**
   - Include `package.json` for Node.js
   - Include `composer.json` for PHP
   - Include language-specific config files

2. **Follow standard project layouts**
   - Use conventional directory names (`src/`, `lib/`, `tests/`)
   - Include configuration files in standard locations

3. **Provide comprehensive README**
   - Document the project type and technologies
   - Explain the build and test process

## Customizing Detection

### Override Detection

You can override automatic detection by explicitly setting project type in your CI workflow:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      # Override detection - treat as Joomla even if markers aren't found
      project-type-override: 'joomla'
```

### Skip Detection

For projects that don't fit standard patterns:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      # Skip project type detection and only run basic validations
      skip-detection: true
```

## Troubleshooting

### Project Not Detected Correctly

If your project type isn't being detected:

1. Check that file markers are in the repository root
2. Verify manifest files follow naming conventions
3. Review the workflow logs for detection output
4. Consider using explicit project type override

### Multiple Project Types

If your repository contains multiple project types:

1. Use `working-directory` input to target specific subdirectories
2. Create separate workflows for each project type
3. Use monorepo detection (future feature)

### Template Repositories

Template repositories (like MokoStandards itself) are automatically skipped to prevent false positives.

## Future Enhancements

Planned improvements to project detection:

- **Python project detection** - Detect Django, Flask, FastAPI projects
- **Go project detection** - Detect Go modules and projects
- **Monorepo support** - Detect multiple projects in one repository
- **Custom detection scripts** - Allow projects to provide detection logic
- **Project type versioning** - Detect framework/CMS versions

## Related Documentation

- [Reusable CI Validation](../.github/workflows/REUSABLE_WORKFLOWS.md)
- [Public Architecture](PUBLIC_ARCHITECTURE.md)

## Contributing

If you have a project type that isn't detected correctly, please:

1. Open an issue describing the project type and structure
2. Provide example file markers and patterns
3. Submit a PR with detection logic if possible

---

**Version:** 1.0.0
**Last Updated:** 2026-01-13
**License:** GPL-3.0-or-later

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Reference                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/reference/PROJECT_TYPE_DETECTION.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
