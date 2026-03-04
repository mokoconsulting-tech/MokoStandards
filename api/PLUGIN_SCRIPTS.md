
[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Plugin System CLI Scripts

Command-line scripts for validating, health checking, and managing projects using the MokoStandards plugin system.

## Available Scripts

| Script | Purpose |
|--------|---------|
| `plugin_validate.php` | Validate project structure and configuration |
| `plugin_health_check.php` | Run comprehensive health checks |
| `plugin_metrics.php` | Collect project metrics |
| `plugin_readiness.php` | Check release readiness |
| `plugin_list.php` | List all available plugins |

## Quick Examples

```bash
# List all available plugins
php api/plugin_list.php

# Validate a project (auto-detect type)
php api/plugin_validate.php --project-path /path/to/project

# Run health check
php api/plugin_health_check.php --project-path /path/to/project

# Collect metrics
php api/plugin_metrics.php --project-path /path/to/project --format table

# Check release readiness
php api/plugin_readiness.php --project-path /path/to/project
```

## Supported Project Types

- **joomla** - Joomla CMS projects and extensions
- **wordpress** - WordPress themes and plugins  
- **nodejs** - Node.js applications and packages
- **python** - Python applications and packages
- **terraform** - Infrastructure as Code
- **mobile** - Mobile applications (iOS/Android)
- **api** - REST API and GraphQL services
- **dolibarr** - Dolibarr ERP/CRM modules
- **documentation** - Documentation projects
- **generic** - Generic project types

## Exit Codes

- **0** - Success
- **1** - Validation/check failed
- **2** - Script error (invalid arguments, plugin not found)

## Documentation

For detailed documentation, see:
- [Plugin Validation Workflow Templates](../templates/workflows/README.md)
- [Plugin System Implementation](lib/Enterprise/README.md)
- Script help: `php api/plugin_*.php --help`

## Integration

These scripts integrate with:
- GitHub Actions workflows (see `templates/workflows/`)
- Plugin system (see `lib/Enterprise/`)
- CI/CD pipelines (GitLab CI, Jenkins, etc.)

## Usage in CI/CD

```yaml
# GitHub Actions example
- name: Validate project
  run: |
    php api/plugin_validate.php --project-path . --json > validation.json
    if jq -e '.valid == false' validation.json > /dev/null; then
      exit 1
    fi
```

For complete usage examples and documentation, run any script with `--help`:
```bash
php api/plugin_validate.php --help
```
