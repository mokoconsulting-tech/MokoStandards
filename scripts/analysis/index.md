# Scripts Index: /scripts/analysis

## Purpose

Analysis and reporting scripts for repository metrics, PR conflicts, and configuration analysis.

## Scripts in This Directory

### analyze_pr_conflicts.py
**Purpose:** Analyze and report on pull request merge conflicts across repositories  
**Type:** Python 3.7+  
**Usage:** `python3 analyze_pr_conflicts.py [options]`  
**Documentation:** [📖 Guide](/docs/scripts/analysis/analyze-pr-conflicts-py.md)

**Key Features:**
- Detects merge conflicts in PRs
- Analyzes conflict patterns
- Generates conflict reports
- Supports multiple repositories

### generate_canonical_config.py
**Purpose:** Generate canonical configuration files from templates  
**Type:** Python 3.7+  
**Usage:** `python3 generate_canonical_config.py [options]`  
**Documentation:** [📖 Guide](/docs/scripts/analysis/generate-canonical-config-py.md)

**Key Features:**
- Processes configuration templates
- Generates standardized configs
- Validates configuration structure
- Supports multiple formats

## Quick Reference

| Script | Language | Primary Use Case |
|--------|----------|------------------|
| `analyze_pr_conflicts.py` | Python 3.7+ | PR conflict analysis |
| `generate_canonical_config.py` | Python 3.7+ | Config generation |

## Dependencies

**Common Dependencies:**
- Python 3.7 or higher
- `scripts/lib/common.py` - Common utilities
- GitHub CLI (`gh`) for repository operations

## Integration Points

### CI/CD Workflows
- Used in PR validation workflows
- Configuration analysis in release pipelines

### Related Scripts
- [validate/check_repo_health.py](/scripts/validate/check_repo_health.py) - Repository health checks
- [automation/bulk_update_repos.py](/scripts/automation/bulk_update_repos.py) - Bulk updates

## Version Requirements

- **Python:** 3.7+ (3.9+ recommended)
- **PowerShell:** 7.0+ (PowerShell Core) - Future implementations
- **Bash:** 4.0+ (for shell script wrappers)

## Metadata

- **Document Type:** index
- **Category:** Analysis Scripts
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial index creation with script details | GitHub Copilot |

## Related Documentation

- [Scripts Documentation Root](/docs/scripts/README.md)
- [Analysis Scripts Policy](/docs/policy/script-standards.md)
- [Contributing Guide](/CONTRIBUTING.md)
