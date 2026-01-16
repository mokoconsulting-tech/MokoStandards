# MokoStandards Scripts Documentation

## Overview

This directory contains comprehensive documentation for all scripts in the MokoStandards repository. Each script has a dedicated guide that explains its purpose, usage, requirements, and integration points.

## Quick Reference

### Script Categories

| Category | Description | Script Count |
|----------|-------------|--------------|
| [Analysis](#analysis) | Analysis and reporting scripts | 2 |
| [Automation](#automation) | Repository automation and bulk operations | 4 |
| [Build](#build) | Build system and Makefile tools | 1 |
| [Docs](#documentation) | Documentation generation and maintenance | 1 |
| [Fix](#fix) | Automated fix and repair scripts | 0 |
| [Lib](#libraries) | Shared libraries and utility functions | 4 |
| [Maintenance](#maintenance) | Repository maintenance and updates | 5 |
| [Release](#release) | Release management and packaging | 4 |
| [Run](#run) | Runtime and setup scripts | 1 |
| [Tests](#tests) | Test scripts and validation tests | 2 |
| [Validate](#validate) | Validation and quality checks | 12 |

**Total Scripts Documented:** 36

## Version Requirements Policy

All scripts in the MokoStandards repository follow these version requirements:

### Python Scripts
- **Minimum Version:** Python 3.7+
- **Recommended:** Python 3.9+ for optimal performance
- **Standard:** All Python scripts use `#!/usr/bin/env python3` shebang

### Shell Scripts
- **Bash Version:** Bash 4.0+ required
- **Features Used:** `set -euo pipefail`, `[[  ]]` conditionals, parameter expansion
- **Compatibility:** POSIX-compliant where possible

### PowerShell Scripts
- **Version:** PowerShell 7.0+ (PowerShell Core)
- **Cross-platform:** Works on Windows, Linux, and macOS
- **Note:** Currently, no PowerShell scripts exist in the repository, but future scripts will follow this standard

## Analysis

Analysis scripts for repository metrics, PR conflicts, and configuration analysis.

| Script | Purpose | Guide |
|--------|---------|-------|
| `analyze_pr_conflicts.py` | Analyze pull request conflicts across repositories | [Guide](analysis/analyze-pr-conflicts-py.md) |
| `generate_canonical_config.py` | Generate canonical configuration files | [Guide](analysis/generate-canonical-config-py.md) |

[📂 View all analysis documentation](analysis/)

## Automation

Automation scripts for bulk repository operations and GitHub integrations.

| Script | Purpose | Guide |
|--------|---------|-------|
| `auto_create_org_projects.py` | Automatically create GitHub Projects for all org repos | [Guide](automation/auto-create-org-projects-py.md) |
| `bulk_update_repos.py` | Bulk update workflows and configs across repositories | [Guide](automation/bulk-update-repos-py.md) |
| `create_repo_project.py` | Create a GitHub Project for a specific repository | [Guide](automation/create-repo-project-py.md) |
| `sync_file_to_project.py` | Sync documentation files to GitHub Project tasks | [Guide](automation/sync-file-to-project-py.md) |

[📂 View all automation documentation](automation/)

## Build

Build system scripts for Makefile resolution and build automation.

| Script | Purpose | Guide |
|--------|---------|-------|
| `resolve_makefile.py` | Resolve and process Makefile includes | [Guide](build/resolve-makefile-py.md) |

[📂 View all build documentation](build/)

## Documentation

Scripts for documentation generation and maintenance.

| Script | Purpose | Guide |
|--------|---------|-------|
| `rebuild_indexes.py` | Rebuild documentation index files | [Guide](docs/rebuild-indexes-py.md) |

[📂 View all docs scripts documentation](docs/)

## Fix

Automated fix and repair scripts (currently empty).

[📂 View all fix documentation](fix/)

## Libraries

Shared library scripts providing common utilities and functions.

| Script | Purpose | Guide |
|--------|---------|-------|
| `common.py` | Common Python utilities for MokoStandards scripts | [Guide](lib/common-py.md) |
| `common.sh` | Common Bash utilities for shell scripts | [Guide](lib/common-sh.md) |
| `extension_utils.py` | Extension platform detection utilities | [Guide](lib/extension-utils-py.md) |
| `joomla_manifest.py` | Joomla manifest parsing utilities | [Guide](lib/joomla-manifest-py.md) |

[📂 View all library documentation](lib/)

## Maintenance

Repository maintenance scripts for updates, versioning, and health checks.

| Script | Purpose | Guide |
|--------|---------|-------|
| `release_version.py` | Update version numbers across repository files | [Guide](maintenance/release-version-py.md) |
| `setup-labels.sh` | Configure GitHub repository labels | [Guide](maintenance/setup-labels-sh.md) |
| `update_changelog.py` | Update CHANGELOG.md with new entries | [Guide](maintenance/update-changelog-py.md) |
| `update_gitignore_patterns.sh` | Update .gitignore patterns across repositories | [Guide](maintenance/update-gitignore-patterns-sh.md) |
| `validate_file_headers.py` | Validate copyright headers in source files | [Guide](maintenance/validate-file-headers-py.md) |

[📂 View all maintenance documentation](maintenance/)

## Release

Release management scripts for packaging, versioning, and deployment.

| Script | Purpose | Guide |
|--------|---------|-------|
| `detect_platform.py` | Detect extension platform (Joomla/Dolibarr) | [Guide](release/detect-platform-py.md) |
| `dolibarr_release.py` | Create Dolibarr module release packages | [Guide](release/dolibarr-release-py.md) |
| `package_extension.py` | Package Joomla/Dolibarr extensions as ZIP | [Guide](release/package-extension-py.md) |
| `update_dates.sh` | Normalize release dates in CHANGELOG and manifests | [Guide](release/update-dates-sh.md) |

[📂 View all release documentation](release/)

## Run

Runtime and setup scripts for project initialization.

| Script | Purpose | Guide |
|--------|---------|-------|
| `setup_github_project_v2.py` | Setup GitHub Projects v2 with custom fields | [Guide](run/setup-github-project-v2-py.md) |

[📂 View all run documentation](run/)

## Tests

Test scripts for validating script functionality.

| Script | Purpose | Guide |
|--------|---------|-------|
| `test_bulk_update_repos.py` | Test bulk repository update functionality | [Guide](tests/test-bulk-update-repos-py.md) |
| `test_dry_run.py` | Test dry-run mode across scripts | [Guide](tests/test-dry-run-py.md) |

[📂 View all test documentation](tests/)

## Validate

Validation scripts for code quality, security, and compliance checks.

| Script | Purpose | Guide |
|--------|---------|-------|
| `check_repo_health.py` | Check repository health against standards | [Guide](validate/check-repo-health-py.md) |
| `generate_stubs.py` | Generate type stubs for validation | [Guide](validate/generate-stubs-py.md) |
| `manifest.py` | Validate extension manifest files | [Guide](validate/manifest-py.md) |
| `no_secrets.py` | Scan for accidentally committed secrets | [Guide](validate/no-secrets-py.md) |
| `paths.py` | Validate file paths and conventions | [Guide](validate/paths-py.md) |
| `php_syntax.py` | Validate PHP syntax | [Guide](validate/php-syntax-py.md) |
| `tabs.py` | Check for tab characters in source files | [Guide](validate/tabs-py.md) |
| `validate_codeql_config.py` | Validate CodeQL configuration files | [Guide](validate/validate-codeql-config-py.md) |
| `validate_repo_health.py` | Validate repository health metrics | [Guide](validate/validate-repo-health-py.md) |
| `validate_structure.py` | Validate repository structure against schema | [Guide](validate/validate-structure-py.md) |
| `workflows.py` | Validate GitHub Actions workflows | [Guide](validate/workflows-py.md) |
| `xml_wellformed.py` | Validate XML file well-formedness | [Guide](validate/xml-wellformed-py.md) |

[📂 View all validation documentation](validate/)

## Common Patterns

### Authentication

Many automation scripts require GitHub authentication:

- **GitHub CLI (`gh`)**: Most scripts use `gh` CLI for authentication
  - Install: `gh auth login`
  - Scopes needed: `repo`, `project`, `read:org`
  
- **Personal Access Token (PAT)**: Some scripts require `GH_PAT` environment variable
  - Create at: https://github.com/settings/tokens
  - Required scopes: `repo`, `project`, `read:org`

### Dry Run Mode

Most automation scripts support `--dry-run` flag:
```bash
# Preview changes without making them
python3 scripts/automation/bulk_update_repos.py --dry-run
```

### Verbose Output

Enable detailed logging with `--verbose` or `-v`:
```bash
python3 scripts/validate/check_repo_health.py --verbose
```

## Integration Points

### CI/CD Workflows

Scripts integrate with GitHub Actions workflows:

- **Validation**: Pre-commit and PR checks use validation scripts
- **Release**: Automated release workflows call packaging scripts
- **Maintenance**: Scheduled workflows run maintenance scripts

See [workflows documentation](../workflows/) for integration details.

### Dependencies

Common dependencies across scripts:

- **Python Libraries**: `argparse`, `pathlib`, `json`, `subprocess`
- **External Tools**: `gh` CLI, `git`, `jq` (for JSON processing)
- **Custom Libraries**: Scripts in `/scripts/lib/` provide shared utilities

## Contributing

When adding new scripts:

1. Create the script in the appropriate `/scripts/` subdirectory
2. Add corresponding documentation in `/docs/scripts/` with matching hierarchy
3. Include Python/PowerShell/Bash version requirements
4. Update this README with a quick reference entry
5. Follow the [documentation template](../templates/script-guide-template.md)

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial comprehensive script documentation | GitHub Copilot |

## Related Documentation

- [Contributing Guide](../../CONTRIBUTING.md)
- [Workflows Documentation](../workflows/)
- [Development Guide](../guide/development.md)
- [Build System Documentation](../build-system/)
