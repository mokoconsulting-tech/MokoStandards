# Required Templates

This directory contains **REQUIRED** files that must be present in all MokoStandards-compliant repositories.

## Overview

Required templates are essential files that provide core functionality and ensure consistency across all repositories in the organization. These files must be copied to target repositories and kept synchronized with MokoStandards updates.

## Required Files

### 1. setup-labels.sh

**Status**: ✅ REQUIRED  
**Target Location**: `scripts/maintenance/setup-labels.sh`  
**Purpose**: Deploy standardized GitHub labels to repository

**Installation**:
```bash
# Quick install
curl -fsSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/required/setup-labels.sh > scripts/maintenance/setup-labels.sh
chmod +x scripts/maintenance/setup-labels.sh

# Or copy from MokoStandards
cp /path/to/MokoStandards/templates/required/setup-labels.sh scripts/maintenance/setup-labels.sh
chmod +x scripts/maintenance/setup-labels.sh
```

**Usage**:
```bash
# Preview labels (dry-run)
./scripts/maintenance/setup-labels.sh --dry-run

# Deploy labels
./scripts/maintenance/setup-labels.sh
```

**Features**:
- 46 standard labels across 8 categories
- Project types (joomla, dolibarr, generic)
- Languages (php, javascript, typescript, python, css, html)
- Components (documentation, ci-cd, docker, tests, security, dependencies, config, build)
- Workflow (automation, mokostandards, needs-review, work-in-progress, breaking-change)
- Priority (critical, high, medium, low)
- Type (bug, feature, enhancement, refactor, chore)
- Status (pending, in-progress, blocked, on-hold, wontfix)
- Size (xs, s, m, l, xl, xxl)
- Health (excellent, good, fair, poor)

**Requirements**:
- GitHub CLI (gh) installed
- Authenticated with GitHub CLI
- Admin access to repository

**Validation**:
```bash
# Check if present
[ -f scripts/maintenance/setup-labels.sh ] && echo "✅ Present" || echo "❌ Missing"

# Check if executable
[ -x scripts/maintenance/setup-labels.sh ] && echo "✅ Executable" || echo "❌ Not executable"

# Verify labels deployed
gh label list | wc -l  # Should show 46+ labels
```

## Compliance Checking

### Check Repository Compliance

```bash
# Check if all required files are present
required_files=(
    "scripts/maintenance/setup-labels.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING"
    fi
done
```

### Automated Compliance

Use the MokoStandards validation scripts:

```bash
# From MokoStandards repository
python3 scripts/validate/validate_repo_health.py --check-required-files

# Or use bulk validation
python3 scripts/automation/bulk_update_repos.py --validate-only
```

## Syncing Updates

Required files should be kept in sync with MokoStandards:

```bash
# Update single file
curl -fsSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/required/setup-labels.sh > scripts/maintenance/setup-labels.sh

# Or use bulk sync
cd /path/to/MokoStandards
./scripts/automation/bulk_update_repos.sh --org mokoconsulting-tech --sync-required
```

## Using with GitHub Copilot

To deploy required files to a repository using GitHub Copilot:

```markdown
Deploy required MokoStandards files to this repository.

Required files to deploy:
1. setup-labels.sh - Label deployment script

Process:
1. Create scripts/maintenance/ directory if not exists
2. Download setup-labels.sh from mokoconsulting-tech/MokoStandards
3. Copy to scripts/maintenance/setup-labels.sh
4. Make executable: chmod +x scripts/maintenance/setup-labels.sh
5. Test with dry-run: ./scripts/maintenance/setup-labels.sh --dry-run
6. Deploy labels: ./scripts/maintenance/setup-labels.sh
7. Verify labels in repository settings

Source: https://github.com/mokoconsulting-tech/MokoStandards/tree/main/templates/required
```

## Future Required Files

As MokoStandards evolves, additional required files may be added:

- **PLANNED**: `.github/labeler.yml` - Auto-labeling configuration
- **PLANNED**: `.editorconfig` - Editor configuration
- **PLANNED**: `scripts/validate/check_compliance.sh` - Standards compliance checker
- **PLANNED**: `.github/workflows/standards-check.yml` - Automated standards validation

## Support

- **Documentation**: [Copilot Sync Standards Guide](../../docs/guide/copilot-sync-standards.md)
- **Label Guide**: [Label Deployment Guide](../../docs/guides/label-deployment.md)
- **Issues**: https://github.com/mokoconsulting-tech/MokoStandards/issues
- **Contact**: hello@mokoconsulting.tech

## Related Documentation

- [Copilot Sync Standards Guide](../../docs/guide/copilot-sync-standards.md)
- [Label Deployment Guide](../../docs/guides/label-deployment.md)
- [Bulk Repository Updates](../../docs/guide/bulk-repository-updates.md)
- [Template Catalog](../README.md)

---

**Last Updated**: 2026-01-28  
**Version**: 03.01.00  
**Maintained By**: MokoStandards Team
