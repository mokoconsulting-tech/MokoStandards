# Scripts Index: /docs/scripts/maintenance

## Purpose

Documentation for repository maintenance scripts including version updates, changelog management, header validation, and repository configuration.

## Available Script Guides

### Version Management
- release-version-py.md - Update version numbers across repository files (Coming Soon)
- update-changelog-py.md - Update CHANGELOG.md with new entries (Coming Soon)

### Repository Configuration
- setup-labels-sh.md - Configure GitHub repository labels (Coming Soon)
- update-gitignore-patterns-sh.md - Update .gitignore patterns (Coming Soon)

### Code Quality
- validate-file-headers-py.md - Validate copyright headers in source files (Coming Soon)

## Quick Reference

| Script | Status | Purpose |
|--------|--------|---------|
| `release_version.py` | 📝 Pending | Version updates |
| `update_changelog.py` | 📝 Pending | CHANGELOG management |
| `setup-labels.sh` | 📝 Pending | GitHub label setup |
| `update_gitignore_patterns.sh` | 📝 Pending | .gitignore updates |
| `validate_file_headers.py` | 📝 Pending | Header validation |

## Release Preparation Workflow

```bash
# 1. Update changelog
python3 scripts/maintenance/update_changelog.py 2.0.0

# 2. Update versions
python3 scripts/maintenance/release_version.py 2.0.0

# 3. Validate headers
python3 scripts/maintenance/validate_file_headers.py --all

# 4. Commit changes
git commit -m "Release version 2.0.0"
```

## Navigation

- [⬆️ Back to Scripts Documentation](../README.md)
- [📂 View Maintenance Scripts Source](/scripts/maintenance/)
- [📖 Maintenance Scripts Index](/scripts/maintenance/index.md)

## Metadata

- **Document Type:** index
- **Category:** Maintenance Script Documentation
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial maintenance docs index creation | GitHub Copilot |
