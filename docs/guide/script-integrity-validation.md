[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Comprehensive Script Integrity Validation System

## Overview

This system provides comprehensive SHA-256 validation for all scripts in the repository, ensuring integrity and detecting unauthorized modifications.

## Components

### 1. Script Registry (`scripts/.script-registry.json`)

Central registry containing SHA-256 hashes for all tracked scripts.

**Structure:**
```json
{
  "metadata": {
    "generated_at": "2026-02-02T09:03:47Z",
    "repository": "mokoconsulting-tech/MokoStandards",
    "version": "1.0.0"
  },
  "scripts": [
    {
      "path": "scripts/validate/validate_codeql_config.py",
      "sha256": "b79bf71adc8968805fac1a36a764ffde543099d110a93593767bdc9fa890673d",
      "category": "validate",
      "priority": "critical",
      "size_bytes": 8210
    }
  ],
  "summary": {
    "total_scripts": 73,
    "by_priority": {...},
    "by_category": {...}
  }
}
```

### 2. Registry Generator (`scripts/maintenance/generate_script_registry.py`)

Generates and updates the script registry.

**Usage:**
```bash
# Generate initial registry
python3 scripts/maintenance/generate_script_registry.py

# Update existing registry and show changes
python3 scripts/maintenance/generate_script_registry.py --update

# Include low-priority scripts (wrappers, libs)
python3 scripts/maintenance/generate_script_registry.py --include-low-priority

# Custom output location
python3 scripts/maintenance/generate_script_registry.py --output my-registry.json
```

**Features:**
- Automatic script discovery
- Priority classification (critical, high, medium, low)
- Category detection
- Change tracking (added, modified, removed)
- Summary statistics

### 3. Registry Validator (`scripts/maintenance/validate_script_registry.py`)

Validates all scripts against the registry.

**Usage:**
```bash
# Validate all scripts
python3 scripts/maintenance/validate_script_registry.py

# Validate only critical priority scripts
python3 scripts/maintenance/validate_script_registry.py --priority critical

# Strict mode (fail on any discrepancy)
python3 scripts/maintenance/validate_script_registry.py --strict

# Detailed output
python3 scripts/maintenance/validate_script_registry.py --verbose
```

**Features:**
- SHA-256 verification for all tracked scripts
- Priority-based filtering
- Detailed change reports
- Actionable recommendations

### 4. Validation Workflow (`.github/workflows/validate-script-integrity.yml`)

Automated validation on every PR and push.

**Triggers:**
- Pull requests to main
- Push to main
- Manual dispatch

**Features:**
- Validates critical and high priority scripts
- Generates detailed reports in GitHub Actions summary
- Fails CI if critical scripts are modified without registry update
- Provides remediation instructions

## Priority Levels

### Critical Priority
**Scripts that affect security, validation, and core maintenance:**
- `scripts/validate/` - All validation scripts
- `scripts/maintenance/` - Maintenance and integrity scripts
- Security-related scripts

### High Priority
**Scripts that affect builds, releases, and automation:**
- `scripts/automation/` - Automation scripts
- `scripts/release/` - Release management
- `scripts/build/` - Build scripts
- `scripts/fix/` - Fixing utilities

### Medium Priority
**Scripts for analysis, documentation, and testing:**
- `scripts/analysis/` - Analysis tools
- `scripts/docs/` - Documentation generators
- `scripts/run/` - Runtime utilities
- `scripts/tests/` - Test scripts

### Low Priority
**Generated wrappers and libraries:**
- `scripts/wrappers/` - Wrapper scripts (often generated)
- `scripts/lib/` - Library modules

## Workflows

### On Pull Request

```
Developer creates PR with script changes
            ↓
Validation workflow triggers
            ↓
Checks critical & high priority scripts
            ↓
┌──────────┴──────────┐
│                     │
Pass                  Fail
│                     │
✅ Merge allowed      ❌ CI fails
                      │
                      Developer must:
                      1. Review changes
                      2. Update registry
                      3. Push update
```

### On Merge to Main

```
PR merged to main
       ↓
Auto-update workflow runs
       ↓
Checks if scripts changed
       ↓
Updates registry if needed
       ↓
Commits changes
```

## Common Operations

### Adding a New Script

1. **Create your script**
2. **Update the registry:**
   ```bash
   python3 scripts/maintenance/generate_script_registry.py --update
   ```
3. **Commit both the script and registry:**
   ```bash
   git add scripts/your-new-script.py scripts/.script-registry.json
   git commit -m "feat: add new script with registry update"
   ```

### Modifying an Existing Script

1. **Make your changes**
2. **Test the script**
3. **Update the registry:**
   ```bash
   python3 scripts/maintenance/generate_script_registry.py --update
   ```
4. **Commit both:**
   ```bash
   git add scripts/modified-script.py scripts/.script-registry.json
   git commit -m "fix: update script with registry sync"
   ```

### Validating Before Commit

```bash
# Check what would change
python3 scripts/maintenance/generate_script_registry.py --update

# Validate all scripts are legitimate
python3 scripts/maintenance/validate_script_registry.py --verbose

# If all good, proceed with commit
git add scripts/.script-registry.json
git commit -m "chore: update script registry"
```

### Emergency: Unauthorized Script Modification Detected

```bash
# 1. Review what changed
python3 scripts/maintenance/validate_script_registry.py --verbose

# 2. If unauthorized, restore from git
git checkout HEAD -- scripts/path/to/modified-script.py

# 3. Re-validate
python3 scripts/maintenance/validate_script_registry.py

# 4. If legitimate, update registry
python3 scripts/maintenance/generate_script_registry.py --update
git add scripts/.script-registry.json
git commit -m "chore: update registry after legitimate changes"
```

## Configuration

### Excluding Scripts from Tracking

Edit `scripts/maintenance/generate_script_registry.py` and update `should_track_script()`:

```python
def should_track_script(script_path: Path) -> bool:
    skip_patterns = [
        'index.md',
        'README',
        '.gitkeep',
        'wrapper-template',
        'your-pattern-here'  # Add your pattern
    ]
    # ...
```

### Changing Priority Levels

Edit `CATEGORY_PRIORITIES` in `generate_script_registry.py`:

```python
CATEGORY_PRIORITIES = {
    'validate': PRIORITY_CRITICAL,
    'maintenance': PRIORITY_CRITICAL,
    'your-category': PRIORITY_HIGH,  # Adjust as needed
    # ...
}
```

## Integration with Existing Tools

### Works With

- ✅ `update_sha_hashes.py` - Complements workflow-specific hash tracking
- ✅ `auto-update-sha.yml` - Workflow for single-file updates
- ✅ All existing validation scripts
- ✅ Pre-commit hooks (can be added)

### Differences from `update_sha_hashes.py`

| Feature | update_sha_hashes.py | Script Registry System |
|---------|---------------------|------------------------|
| Scope | Single file (validate_codeql_config.py) | All 73+ scripts |
| Storage | Embedded in workflow YAML | Centralized JSON registry |
| Updates | Workflow-only | Registry + validation |
| Priority | N/A | 4 levels (critical/high/medium/low) |
| Use Case | Auto-sync workflow hashes | Comprehensive integrity |

## Troubleshooting

### "Registry file not found"

```bash
# Generate the registry
python3 scripts/maintenance/generate_script_registry.py
```

### "Multiple scripts modified"

```bash
# Review changes
python3 scripts/maintenance/validate_script_registry.py --verbose

# If legitimate, update registry
python3 scripts/maintenance/generate_script_registry.py --update
```

### "Workflow failing on PR"

1. Check which scripts were modified
2. Update the registry in your PR:
   ```bash
   python3 scripts/maintenance/generate_script_registry.py --update
   git add scripts/.script-registry.json
   git commit --amend --no-edit
   git push --force-with-lease
   ```

### "Want to check only critical scripts"

```bash
python3 scripts/maintenance/validate_script_registry.py --priority critical
```

## Security Considerations

1. **Registry is Version Controlled**: Any changes are auditable
2. **Multi-level Validation**: Critical scripts always checked
3. **Automated Detection**: CI catches unauthorized changes
4. **Clear Audit Trail**: Git history shows all registry updates
5. **Priority-based**: Critical scripts get highest scrutiny

## Future Enhancements

Potential improvements:
- Pre-commit hook integration
- Automated PR comments with validation results
- Dashboard showing script health
- Historical tracking of changes
- Integration with vulnerability scanning
- Support for additional hash algorithms (SHA-512)

## Related Documentation

- [SHA Auto-Update](sha-auto-update.md) - Single-file auto-update system
- [Security Scanning](../scripts/validate/SECURITY_SCANNING.md) - General security practices
- [Script Architecture](../scripts/docs/ARCHITECTURE.md) - Overall script structure

## Support

For issues or questions:
1. Check validation output for specific errors
2. Review this documentation
3. Check git history for recent changes
4. Open an issue with validation logs
