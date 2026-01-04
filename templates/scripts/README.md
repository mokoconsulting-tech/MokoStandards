# Script Templates

This directory contains template scripts for common repository operations including validation, fixes, and release automation.

## Directory Structure

- `validate/` - Validation scripts for CI pipelines
- `fix/` - Automated fix scripts for common issues
- `release/` - Release automation scripts
- `lib/` - Shared library functions

## Validation Scripts

### validate/tabs.sh
Validates that no literal tab characters exist in source files.

### validate/paths.sh
Validates that path separators use forward slashes.

### validate/changelog.sh
Validates CHANGELOG.md structure and format.

### validate/xml_wellformed.sh
Validates XML files are well-formed.

### validate/license_headers.sh
Validates license headers in source files.

### validate/no_secrets.sh
Checks for potential secrets in committed files.

### validate/php_syntax.sh
Validates PHP syntax (Joomla projects).

### validate/version_alignment.sh
Validates version alignment across manifest files.

### validate/manifest.sh
Validates Joomla manifest structure (Joomla projects).

### validate/language_structure.sh
Validates language file structure (Joomla projects).

## Fix Scripts

### fix/line_endings.sh
Fixes line endings to LF.

### fix/permissions.sh
Fixes file permissions (644 for files, 755 for directories and scripts).

## Release Scripts

### release/package.sh
Creates release package with proper structure.

## Library Scripts

### lib/common.sh
Common utility functions for scripts including logging, command checks, and git utilities.

## Usage

### In CI Workflows

Add validation scripts to your CI workflow:

```yaml
- name: Required validations
  run: |
    set -e
    scripts/validate/manifest.sh
    scripts/validate/xml_wellformed.sh
```

### Manual Execution

Make scripts executable and run:

```bash
chmod +x scripts/validate/*.sh
./scripts/validate/tabs.sh
```

### With Library Functions

Source the common library in your scripts:

```bash
#!/usr/bin/env bash
source "$(dirname "$0")/../lib/common.sh"

log_info "Starting validation..."
require_command "xmllint"
```

## Customization

These are template scripts. Adapt them to your project's specific needs:

1. Copy relevant scripts to your project's `scripts/` directory
2. Modify validation rules to match your standards
3. Update file patterns and paths as needed
4. Add project-specific validation logic

## Standards Compliance

All scripts follow MokoStandards requirements:

- SPDX license headers
- GPL-3.0-or-later license
- Proper error handling with `set -euo pipefail`
- Informative logging output
- Exit code conventions (0 = success, 1 = failure)

## Integration with repo_health.yml

The `repo_health.yml` workflow enforces script governance:

- Allowed directories: `scripts/`, `scripts/validate/`, `scripts/fix/`, `scripts/release/`, `scripts/lib/`
- ShellCheck validation (advisory)
- Script structure validation

## Notes

- Scripts in `validate/` should exit with code 1 on failure
- Scripts in `fix/` should be idempotent
- Scripts in `release/` should be safe to run multiple times
- Always test scripts locally before committing
