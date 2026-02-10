# Maintenance Scripts

This directory contains maintenance and automation scripts for repository upkeep.

**Status**: ⚠️ **REQUIRED** - Key scripts are automatically distributed to all organization repositories via Terraform.

## Required Scripts (Terraform-Managed)

The following scripts are deployed to all repositories and must be maintained:

### clean_old_branches.py
**Status**: REQUIRED (Auto-sync enabled)

Identifies and optionally deletes old Git branches to prevent branch accumulation.

**Usage:**
```bash
# List old branches (older than 90 days)
./scripts/maintenance/clean_old_branches.py --days 90 --list

# Delete old branches (dry run first)
./scripts/maintenance/clean_old_branches.py --days 90 --delete --dry-run

# Delete old branches (actual deletion)
./scripts/maintenance/clean_old_branches.py --days 90 --delete
```

**Features:**
- Identifies branches by last commit date
- Protects main/master/dev branches
- Dry-run mode for safety
- Detailed reporting

### release_version.py
**Status**: REQUIRED (Auto-sync enabled)

Manages version releases in CHANGELOG.md and updates VERSION in files.

**Usage:**
```bash
# Create a new release
./scripts/maintenance/release_version.py --version 1.2.3 --yes

# Update CHANGELOG only
./scripts/maintenance/release_version.py --version 1.2.3 --changelog-only

# Update files and create GitHub release
./scripts/maintenance/release_version.py \
  --version 1.2.3 \
  --update-files \
  --create-release

# Dry run
./scripts/maintenance/release_version.py --version 1.2.3 --dry-run
```

**Features:**
- Moves UNRELEASED items to versioned section
- Updates VERSION in all file headers
- Creates git tags
- GitHub release integration

## Additional Scripts (Repository-Specific)

### update_changelog.py
Add entries to CHANGELOG.md UNRELEASED section.

**Usage:**
```bash
# Add a changelog entry
python3 scripts/maintenance/update_changelog.py \
  --category Added \
  --entry "New feature description"

# Show current UNRELEASED section
python3 scripts/maintenance/update_changelog.py --show
```

### validate_file_headers.py
Validate that all project files have proper copyright and license headers.

**Usage:**
```bash
python3 scripts/maintenance/validate_file_headers.py
```

### update_copyright_year.py
Updates copyright year in all files.

**Usage:**
```bash
python3 scripts/maintenance/update_copyright_year.py --year 2026
```

### validate_terraform_drift.py
Validates terraform drift and configuration.

### update_gitignore_patterns.sh
Update .gitignore patterns across the repository.

### setup-labels.sh
Setup standard GitHub labels for a repository.

## Terraform Distribution

Required scripts are automatically deployed via:
- **Configuration**: `terraform/repository-types/default-repository.tf`
- **Distribution**: `terraform/repository-management/main.tf`
- **Always Overwrite**: `true` (ensures latest version)

**Deployment:**
```bash
# Deploy to all repositories
./scripts/automation/bulk_update_repos.py --yes --set-standards
```

## Related Documentation

- [Branch & Version Automation Distribution](../../terraform/repository-management/VERSION_BUMP_DISTRIBUTION.md)
- [Branching Strategy Policy](../../docs/policy/branching-strategy.md)
- [Release Management](../../docs/policy/governance/release-management.md)

## Support

For issues with these scripts:
1. Check this documentation
2. Review terraform logs
3. Check audit logs in `logs/automation/`
4. Contact MokoStandards maintainers
