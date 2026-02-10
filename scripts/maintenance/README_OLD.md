# Maintenance Scripts

This directory contains scripts for repository maintenance tasks including changelog management, versioning, and code standards validation.

## Scripts

### update_changelog.py
Add entries to CHANGELOG.md UNRELEASED section.

**Usage:**
```bash
# Add a changelog entry
python3 scripts/maintenance/update_changelog.py \
  --category Added \
  --entry "New feature description"

# Add entry with subcategory
python3 scripts/maintenance/update_changelog.py \
  --category Changed \
  --entry "Updated API endpoint" \
  --subcategory "API"

# Show current UNRELEASED section
python3 scripts/maintenance/update_changelog.py --show
```

### release_version.py
Finalize a release version by updating CHANGELOG.md and project files.

**Usage:**
```bash
# Create a release
python3 scripts/maintenance/release_version.py --version 05.01.00

# Dry run to preview changes
python3 scripts/maintenance/release_version.py --version 05.01.00 --dry-run

# Update files and create GitHub release
python3 scripts/maintenance/release_version.py \
  --version 05.01.00 \
  --update-files \
  --create-release
```

### validate_file_headers.py
Validate that all project files have proper copyright and license headers.

**Usage:**
```bash
python3 scripts/maintenance/validate_file_headers.py
```

### update_gitignore_patterns.sh
Update .gitignore patterns across the repository.

### setup-labels.sh
Setup standard GitHub labels for a repository.
