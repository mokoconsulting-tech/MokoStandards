# Scripts Index: /scripts/maintenance

## Purpose

Repository maintenance scripts for version updates, changelog management, header validation, and repository configuration.

## Scripts in This Directory

### release_version.py
**Purpose:** Update version numbers across repository files  
**Type:** Python 3.7+  
**Usage:** `python3 release_version.py <version> [options]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/release-version-py.md)

**Key Features:**
- Updates version in manifest files
- Updates CHANGELOG.md entries
- Updates package.json, composer.json
- Supports semantic versioning
- Validates version format

**Affected Files:**
- Joomla: `templateDetails.xml`, `updates.xml`
- Dolibarr: `mod*.class.php`
- Node: `package.json`
- PHP: `composer.json`
- Documentation: `CHANGELOG.md`

### setup-labels.sh
**Purpose:** Configure GitHub repository labels with standardized set  
**Type:** Shell script (Bash 4.0+)  
**Usage:** `./setup-labels.sh [repo]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/setup-labels-sh.md)

**Key Features:**
- Creates standard label set
- Configures colors and descriptions
- Removes default GitHub labels
- Idempotent (safe to run multiple times)

**Label Categories:**
- Priority: `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- Type: `type:bug`, `type:feature`, `type:docs`, `type:chore`
- Status: `status:blocked`, `status:in-progress`, `status:review`
- Size: `size:xs`, `size:s`, `size:m`, `size:l`, `size:xl`

### update_changelog.py
**Purpose:** Update CHANGELOG.md with new entries  
**Type:** Python 3.7+  
**Usage:** `python3 update_changelog.py <version> [options]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/update-changelog-py.md)

**Key Features:**
- Adds new version entries
- Maintains Keep a Changelog format
- Updates [Unreleased] section
- Links to GitHub releases
- Validates CHANGELOG structure

**CHANGELOG Format:**
- Follows [Keep a Changelog](https://keepachangelog.com/)
- Sections: Added, Changed, Deprecated, Removed, Fixed, Security
- Semantic versioning links

### update_gitignore_patterns.sh
**Purpose:** Update .gitignore patterns across repositories  
**Type:** Shell script (Bash 4.0+)  
**Usage:** `./update_gitignore_patterns.sh [options]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/update-gitignore-patterns-sh.md)

**Key Features:**
- Adds standard ignore patterns
- Language-specific patterns (PHP, JS, Python)
- IDE-specific patterns (VS Code, PHPStorm)
- Build artifact patterns
- Preserves existing custom patterns

**Pattern Categories:**
- Dependencies: `vendor/`, `node_modules/`, `__pycache__/`
- Build: `dist/`, `build/`, `*.zip`
- IDE: `.idea/`, `.vscode/`, `*.swp`
- OS: `.DS_Store`, `Thumbs.db`

### validate_file_headers.py
**Purpose:** Validate copyright headers in source files  
**Type:** Python 3.7+  
**Usage:** `python3 validate_file_headers.py [options]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/validate-file-headers-py.md)

**Key Features:**
- Validates GPL-3.0 headers
- Checks required metadata fields
- Supports multiple file types
- Reports missing/incorrect headers
- Can auto-fix headers (with `--fix`)

**Validated Fields:**
- Copyright notice
- License identifier (SPDX)
- File metadata: DEFGROUP, INGROUP, REPO, PATH, VERSION, BRIEF

**Supported File Types:**
- Python: `.py`
- PHP: `.php`
- JavaScript: `.js`
- Shell: `.sh`

### flush_actions_cache.py
**Purpose:** Flush GitHub Actions caches for a repository  
**Type:** Python 3.7+  
**Usage:** `python3 flush_actions_cache.py [options]`  
**Documentation:** [📖 Guide](/docs/scripts/maintenance/flush-actions-cache-py.md)

**Key Features:**
- Lists all GitHub Actions caches
- Filters caches by branch or key pattern
- Deletes individual or multiple caches
- Dry-run mode to preview deletions
- Integration with GitHub Actions workflow

**Filter Options:**
- `--repo owner/repo` - Specify repository
- `--branch name` - Filter by branch name
- `--key pattern` - Filter by key pattern (e.g., composer, node)
- `--dry-run` - Preview without deleting

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated
- Token with `actions:write` permission

## Quick Reference

| Script | Language | Primary Use Case |
|--------|----------|------------------|
| `release_version.py` | Python 3.7+ | Version updates |
| `setup-labels.sh` | Bash 4.0+ | GitHub label setup |
| `update_changelog.py` | Python 3.7+ | CHANGELOG management |
| `update_gitignore_patterns.sh` | Bash 4.0+ | .gitignore updates |
| `validate_file_headers.py` | Python 3.7+ | Header validation |
| `flush_actions_cache.py` | Python 3.7+ | GitHub Actions cache management |

## Dependencies

**Common Dependencies:**
- Python 3.7+ or Bash 4.0+
- `scripts/lib/common.py` - Python utilities
- `scripts/lib/common.sh` - Shell utilities
- `git` - Version control operations
- GitHub CLI (`gh`) for label management

## Integration Points

### Release Workflow
```bash
# Typical release process
1. update_changelog.py <version>
2. release_version.py <version>
3. validate_file_headers.py --all
4. git commit -m "Release version X.Y.Z"
5. git tag vX.Y.Z
```

### CI/CD Workflows
- `.github/workflows/validate-headers.yml` - Header validation
- `.github/workflows/release.yml` - Automated releases
- Pre-commit hooks for validation

### Related Scripts
- [release/update_dates.sh](/scripts/release/update_dates.sh) - Date normalization
- [validate/validate_structure.py](/scripts/validate/validate_structure.py) - Structure checks

## Version Requirements

- **Python:** 3.7+ (3.9+ recommended)
- **PowerShell:** 7.0+ (PowerShell Core) - Future implementations
- **Bash:** 4.0+ required for shell scripts
- **Git:** 2.0+ for repository operations
- **GitHub CLI:** 2.0+ for label management

## Best Practices

### Version Updates
```bash
# Always validate before releasing
python3 validate_file_headers.py --all
python3 update_changelog.py 1.2.3
python3 release_version.py 1.2.3 --validate
```

### Changelog Maintenance
- Update [Unreleased] section during development
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Group changes by category (Added, Fixed, etc.)
- Include issue/PR references

### Header Validation
```bash
# Check all files
python3 validate_file_headers.py --all

# Auto-fix headers (use with caution)
python3 validate_file_headers.py --all --fix

# Check specific directory
python3 validate_file_headers.py --path src/
```

## Common Tasks

### Preparing a Release
```bash
# 1. Update changelog
python3 scripts/maintenance/update_changelog.py 2.0.0

# 2. Update versions
python3 scripts/maintenance/release_version.py 2.0.0

# 3. Validate headers
python3 scripts/maintenance/validate_file_headers.py --all

# 4. Update dates in manifests
bash scripts/release/update_dates.sh $(date +%Y-%m-%d) 2.0.0
```

### Setting Up Repository
```bash
# Configure labels
bash scripts/maintenance/setup-labels.sh mokoconsulting-tech/my-repo

# Update .gitignore
bash scripts/maintenance/update_gitignore_patterns.sh
```

## Metadata

- **Document Type:** index
- **Category:** Maintenance Scripts
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial comprehensive maintenance index | GitHub Copilot |

## Related Documentation

- [Scripts Documentation Root](/docs/scripts/README.md)
- [Release Management Guide](/docs/release-management/)
- [Versioning Policy](/docs/policy/versioning.md)
- [File Header Standards](/docs/policy/file-headers.md)
