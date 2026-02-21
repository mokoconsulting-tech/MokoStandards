[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Branch and Version Automation - Comprehensive Guide

**Document Version**: 1.0.0  
**Last Updated**: 2026-02-10  
**Status**: Production Ready  
**Audience**: Developers, DevOps Engineers, Repository Maintainers

## Overview

This guide provides comprehensive documentation for the branch and version automation systems deployed across all MokoStandards organization repositories via Terraform.

### Quick Links

- [Version Automation](#version-automation)
- [Branch Management](#branch-management)
- [Release Automation](#release-automation)
- [Terraform Distribution](#terraform-distribution)
- [Troubleshooting](#troubleshooting)

## Required Scripts (9 Total)

All organization repositories automatically receive these scripts:

| Script | Category | Purpose | Auto-Sync |
|--------|----------|---------|-----------|
| `version_bump_detector.py` | Core Library | Semantic version detection | ✅ |
| `detect_version_bump.py` | Automation | Version bump CLI | ✅ |
| `common.py` | Core Library | Shared utilities | ⚠️ |
| `clean_old_branches.py` | Maintenance | Branch cleanup | ✅ |
| `release_version.py` | Maintenance | Release management | ✅ |
| `unified_release.py` | Release | Release orchestration | ✅ |
| `detect_platform.py` | Release | Platform detection | ✅ |
| `package_extension.py` | Release | Extension packaging | ✅ |
| `test_version_bump_detector.py` | Testing | Unit tests | ✅ |

## Version Automation

### Semantic Version Bump Rules

```
Breaking change         → MAJOR (X.y.z)
New feature             → MINOR (x.Y.z)
Bug fix                 → PATCH (x.y.Z)
Documentation update    → PATCH (x.y.Z)
Performance improvement → PATCH (x.y.Z)
Code refactoring        → PATCH (x.y.Z)
Dependency update       → PATCH (x.y.Z)
Security fix            → PATCH (x.y.Z)
```

### Quick Start

**Detect version bump:**
```bash
./scripts/automation/detect_version_bump.py --file pr_template.md
```

**Apply version bump:**
```bash
./scripts/automation/detect_version_bump.py \
  --text "New feature" \
  --apply \
  --stats
```

### Enterprise Features

- ✅ **Audit Logging**: Complete operation trail in JSON format
- ✅ **Backup/Rollback**: Automatic backup before modifications
- ✅ **SHA-256 Integrity**: File integrity validation
- ✅ **Performance Metrics**: Detailed statistics
- ✅ **Dry-Run Mode**: Preview changes safely

**Audit Log Location**: `logs/automation/version_bump_*.json`

### CLI Reference

```bash
./scripts/automation/detect_version_bump.py [OPTIONS]

Input Sources:
  --file FILE              Read from file
  --stdin                  Read from stdin
  --text TEXT              Analyze text
  --checkboxes TEXT        Analyze checkboxes

Actions:
  --apply                  Apply version bump
  --dry-run                Preview only

Options:
  --bump-type {major,minor,patch}  Override detection
  --backup / --no-backup           Toggle backup
  --audit-log / --no-audit-log     Toggle logging
  --verbose, -v                    Verbose output
  --json                           JSON output
  --stats                          Performance stats
```

## Branch Management

### Automated Branch Cleanup

**List old branches:**
```bash
./scripts/maintenance/clean_old_branches.py --days 90 --list
```

**Delete with dry-run:**
```bash
./scripts/maintenance/clean_old_branches.py --days 90 --delete --dry-run
```

**Actually delete:**
```bash
./scripts/maintenance/clean_old_branches.py --days 90 --delete --yes
```

**Protected Branches** (never deleted):
- `main`, `master`, `dev`, `staging`, `production`

### Release Version Management

**Create release:**
```bash
./scripts/maintenance/release_version.py --version 1.3.0 --yes
```

**Update CHANGELOG only:**
```bash
./scripts/maintenance/release_version.py --version 1.3.0 --changelog-only
```

**What it does:**
1. Moves UNRELEASED to versioned section
2. Updates VERSION in headers
3. Creates git tags (optional)
4. Triggers GitHub releases (optional)

## Release Automation

### Unified Release

**Create stable release:**
```bash
./scripts/release/unified_release.py --version 1.3.0 --release-type stable
```

**Release candidate:**
```bash
./scripts/release/unified_release.py --version 1.3.0-rc1 --release-type rc
```

### Release Types

| Type | Example | Use Case |
|------|---------|----------|
| `stable` | 1.3.0 | Production |
| `rc` | 1.3.0-rc1 | Release candidate |
| `beta` | 1.3.0-beta1 | Beta testing |
| `alpha` | 1.3.0-alpha1 | Early testing |

### Platform Detection

```bash
./scripts/release/detect_platform.py
```

**Supported:** Joomla, Dolibarr, WordPress, Python, Node.js, Generic

### Extension Packaging

```bash
./scripts/release/package_extension.py --version 1.3.0
```

**Output:** `release/ProjectName-1.3.0.zip` + checksums

## Terraform Distribution

### Deployment

**Automatic:**
```bash
./scripts/automation/bulk_update_repos.py --yes --set-standards
```

**Manual:**
```bash
cd terraform/repository-management
terraform apply -var="github_token=$GITHUB_TOKEN"
```

### Configuration Files

- `terraform/repository-types/default-repository.tf` - Structure definition
- `terraform/repository-management/main.tf` - Distribution config

## Troubleshooting

### Version Not Found

**Error:** `Version not found in README.md`

**Fix:** Ensure format is `# README - ProjectName (VERSION: 01.02.03)`

### Permission Denied

```bash
chmod -R 755 scripts/
chmod 644 scripts/**/*.py
```

### Failed Mid-Operation

```bash
# Check backup
ls -la .version_bump_backup/

# Rollback
cp -r .version_bump_backup/* ./

# Retry
./scripts/automation/detect_version_bump.py --text "Fix" --apply
```

### Debug Mode

```bash
# Verbose output
./scripts/automation/detect_version_bump.py --verbose --text "..."

# Check logs
cat logs/automation/version_bump_*.json | jq '.'
```

## Integration Patterns

### GitHub Actions

```yaml
name: Auto Version Bump
on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  version-bump:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Apply Version Bump
        run: |
          ./scripts/automation/detect_version_bump.py \
            --text "${{ github.event.pull_request.body }}" \
            --apply \
            --stats
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -qE '(\.py|\.md)$'; then
    ./scripts/automation/detect_version_bump.py --validate || {
        echo "❌ Version inconsistency"
        exit 1
    }
fi
```

## Best Practices

### Version Management

1. Always run dry-run first
2. Review audit logs regularly
3. Keep backups for 30+ days
4. Use semantic versioning consistently

### Branch Management

1. Run cleanup monthly
2. Always dry-run before delete
3. Maintain protected branch list
4. Document exceptions

### Release Automation

1. Detect platform before release
2. Test packaging in non-prod
3. Verify checksums
4. Maintain release notes

## Reference

### Related Documentation

- [Terraform Distribution Guide](../../terraform/repository-management/VERSION_BUMP_DISTRIBUTION.md)
- [Maintenance Scripts](../../scripts/maintenance/README.md)
- [Release Scripts](../../scripts/release/README.md)
- [Branching Strategy](../policy/branching-strategy.md)

### External Resources

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Support

**Getting Help:**
1. Check this documentation
2. Review troubleshooting section
3. Check audit logs: `logs/automation/*.json`
4. Contact MokoStandards maintainers

**Reporting Issues:**
Include: script name, command, error message, audit log, context

---

**Document Version**: 1.0.0  
**Next Review**: 2026-03-10  
**Maintainer**: MokoStandards Team
