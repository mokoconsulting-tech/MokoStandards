# Scripts Index: /docs/scripts

## Purpose

This directory contains comprehensive documentation guides for all scripts in the MokoStandards repository. Each guide provides detailed usage instructions, examples, requirements, and integration information.

## Documentation Structure

```
/docs/scripts/
├── README.md                  # Main overview (you are here)
├── analysis/                  # Analysis script guides
├── automation/                # Automation script guides  
├── build/                     # Build script guides
├── docs/                      # Documentation script guides
├── fix/                       # Fix script guides
├── lib/                       # Library documentation
├── maintenance/               # Maintenance script guides
├── release/                   # Release script guides
├── run/                       # Runtime script guides
├── tests/                     # Test script guides
└── validate/                  # Validation script guides
```

## Available Documentation

### Completed Guides ✅

| Script | Guide | Category |
|--------|-------|----------|
| `validate/no_secrets.py` | [no-secrets-py.md](validate/no-secrets-py.md) | Security validation |
| `lib/common.py` | [common-py.md](lib/common-py.md) | Python utilities library |

### In Progress 📝

Documentation for the remaining 34 scripts is being created following the same comprehensive template.

## Documentation Categories

### [Validation Scripts](validate/)
Security, quality, and compliance validation tools.
- **Status:** 1/12 documented
- **Priority:** High

### [Library Scripts](lib/)
Shared utilities and common functions.
- **Status:** 1/4 documented
- **Priority:** Critical (dependencies for all other scripts)

### [Automation Scripts](automation/)
GitHub automation and bulk operations.
- **Status:** 0/6 documented
- **Priority:** High

### [Release Scripts](release/)
Release packaging and version management.
- **Status:** 0/4 documented
- **Priority:** Medium

### [Maintenance Scripts](maintenance/)
Repository maintenance and updates.
- **Status:** 0/5 documented
- **Priority:** Medium

### [Other Categories](../scripts/)
Analysis, build, docs, run, tests, and fix scripts.
- **Status:** 0/5 documented
- **Priority:** Low-Medium

## Quick Start

### Finding Documentation

1. **Browse by category:** Use the category links above
2. **Search by script name:** Check the script's corresponding guide file
3. **Use the main README:** See [/docs/scripts/README.md](README.md) for full listing

### Documentation Format

Each script guide includes:
- ✅ Overview and purpose
- ✅ Location and file type
- ✅ **Version requirements** (Python/PowerShell/Bash)
- ✅ Detailed usage examples
- ✅ Command-line options
- ✅ Requirements and dependencies
- ✅ Configuration details
- ✅ Exit codes
- ✅ Integration examples (CI/CD, other scripts)
- ✅ Error handling and troubleshooting
- ✅ Best practices
- ✅ Related scripts

## Related Documentation

- [Scripts Source Code](/scripts/) - Actual script implementations
- [Scripts Index](/scripts/index.md) - Scripts directory index
- [Enterprise Readiness Strategy](/docs/ENTERPRISE_READINESS_SCRIPTS.md) - Consolidation and improvement plan
- [Contributing Guide](/CONTRIBUTING.md) - How to contribute

## Contributing to Documentation

When adding new scripts:

1. Create the script in `/scripts/[category]/`
2. Create corresponding guide in `/docs/scripts/[category]/`
3. Follow the documentation template
4. Update the category index.md
5. Include version requirements (Python/PowerShell/Bash)

See [Contributing Guide](/CONTRIBUTING.md) for details.

## Metadata

- **Document Type:** index
- **Category:** Script Documentation Root
- **Last Updated:** 2026-01-15
- **Completion:** 6% (2/36 guides complete)

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial docs index with completion tracking | GitHub Copilot |
