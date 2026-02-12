[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Automation Documentation

Documentation for all automation systems deployed across MokoStandards organization repositories.

## Available Documentation

### [Branch and Version Automation](branch-version-automation.md)
Comprehensive guide covering all automation scripts, terraform distribution, and integration patterns.

**Topics Covered:**
- Version bump detection and application
- Branch cleanup and lifecycle management  
- Release orchestration and packaging
- Terraform-based script distribution
- Troubleshooting and best practices
- CI/CD integration patterns

**Quick Links:**
- [Version Automation](branch-version-automation.md#version-automation)
- [Branch Management](branch-version-automation.md#branch-management)
- [Release Automation](branch-version-automation.md#release-automation)
- [Troubleshooting](branch-version-automation.md#troubleshooting)

## Related Documentation

### Scripts Documentation
- [Maintenance Scripts](../../scripts/maintenance/README.md)
- [Release Scripts](../../scripts/release/README.md)
- [Automation Scripts](../../scripts/automation/README.md)

### Policy & Strategy
- [Branching Strategy](../policy/branching-strategy.md)
- [Release Management](../policy/governance/release-management.md)
- [Enterprise Readiness](../reports/ENTERPRISE_READINESS_SCRIPTS.md)

### Technical Reference
- [Terraform Distribution](../../terraform/repository-management/VERSION_BUMP_DISTRIBUTION.md)
- [Common Utilities](../scripts/lib/common-py.md)
- [Version Bump Detector API](../scripts/lib/version-bump-detector.md)

## Quick Start

### Version Bump
```bash
./scripts/automation/detect_version_bump.py --text "New feature" --apply
```

### Branch Cleanup
```bash
./scripts/maintenance/clean_old_branches.py --days 90 --delete --dry-run
```

### Release
```bash
./scripts/release/unified_release.py --version 1.3.0 --release-type stable
```

## Support

For automation-related issues:
1. Check the [comprehensive guide](branch-version-automation.md)
2. Review [troubleshooting section](branch-version-automation.md#troubleshooting)
3. Check audit logs in `logs/automation/`
4. Contact MokoStandards maintainers

---

**Last Updated**: 2026-02-10  
**Status**: Production Ready
