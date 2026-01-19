# MokoStandards Scripts Architecture

**Version**: 2.0  
**Last Updated**: 2026-01-19  
**Status**: Comprehensive rebuild in progress

## Overview

This document defines the top-down architecture for all MokoStandards scripts and workflows.

## Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Type Safety**: Full type hints on all public interfaces
3. **Error Handling**: Comprehensive error messages with actionable guidance
4. **Documentation**: Docstrings following Google style guide
5. **Testability**: All modules designed for unit testing with clear interfaces
6. **Logging**: Structured logging with consistent levels and formats
7. **Configuration**: Centralized configuration management
8. **Dependencies**: Minimal external dependencies, clear dependency tree

## Module Hierarchy

```
scripts/
├── lib/                    # Core libraries (no external script dependencies)
│   ├── common.py          # Foundation: constants, utilities, decorators
│   ├── validation_framework.py  # Base classes for validators
│   ├── config_manager.py  # Configuration handling
│   ├── github_client.py   # GitHub API wrapper
│   ├── audit_logger.py    # Structured logging
│   ├── extension_utils.py # Extension/package utilities
│   ├── joomla_manifest.py # Joomla-specific manifest handling
│   └── gui_utils.py       # GUI utilities (optional)
│
├── validate/              # Validation scripts (depend on lib/)
│   ├── auto_detect_platform.py  # Platform detection (core)
│   ├── validate_structure_v2.py # Structure validation
│   ├── validate_repo_health.py  # Repository health
│   ├── schema_aware_health_check.py # Schema-based validation
│   ├── check_repo_health.py     # Health checker
│   ├── validate_codeql_config.py # CodeQL validation
│   ├── manifest.py        # Manifest validation
│   ├── workflows.py       # Workflow validation
│   ├── php_syntax.py      # PHP syntax checking
│   ├── xml_wellformed.py  # XML validation
│   ├── no_secrets.py      # Secret detection
│   ├── tabs.py            # Tab/whitespace checking
│   ├── paths.py           # Path validation
│   └── generate_stubs.py  # Stub generation
│
├── automation/            # Automation scripts (depend on lib/, validate/)
│   ├── bulk_update_repos_v2.py  # Bulk repository sync
│   ├── auto_create_org_projects.py # Organization project automation
│   ├── sync_dolibarr_changelog.py  # Dolibarr changelog sync
│   ├── sync_file_to_project.py     # File sync to projects
│   ├── create_repo_project.py      # Repository project creation
│   └── file-distributor.py         # File distribution
│
├── release/               # Release management (depend on lib/, validate/)
│   ├── deploy_to_dev.py   # Development deployment
│   ├── detect_platform.py # Platform detection for releases
│   ├── package_extension.py # Extension packaging
│   └── dolibarr_release.py  # Dolibarr release management
│
├── maintenance/           # Maintenance scripts (depend on lib/)
│   ├── release_version.py  # Version management
│   ├── update_changelog.py # Changelog updates
│   ├── validate_file_headers.py # Header validation
│   └── flush_actions_cache.py   # GitHub Actions cache management
│
├── analysis/              # Analysis tools (depend on lib/)
│   ├── analyze_pr_conflicts.py  # PR conflict analysis
│   └── generate_canonical_config.py # Canonical configuration
│
├── build/                 # Build scripts (depend on lib/)
│   └── resolve_makefile.py # Makefile resolution
│
├── docs/                  # Documentation generation (depend on lib/)
│   └── rebuild_indexes.py  # Index rebuilding
│
├── run/                   # Runtime scripts (depend on lib/, automation/)
│   └── setup_github_project_v2.py # GitHub Project v2 setup
│
└── tests/                 # Test scripts
    ├── test_bulk_update_repos.py # Bulk update tests
    └── test_dry_run.py            # Dry run tests
```

## Core Library Modules (`lib/`)

### common.py
**Purpose**: Foundation module with core utilities  
**Exports**:
- Constants (VERSION, REPO_URL, EXIT codes)
- File header generation
- Logging utilities
- Error handling decorators
- Path utilities

### validation_framework.py
**Purpose**: Base classes and interfaces for validation  
**Exports**:
- `Validator` base class
- `ValidationResult` data class
- `ValidationRule` interface
- Common validation patterns

### config_manager.py
**Purpose**: Centralized configuration management  
**Exports**:
- `ConfigManager` class
- Configuration schema validation
- Environment variable handling
- Default configuration

### github_client.py
**Purpose**: GitHub API wrapper with authentication  
**Exports**:
- `GitHubClient` class
- API request handling with retries
- Rate limit management
- Common GitHub operations

### audit_logger.py
**Purpose**: Structured logging framework  
**Exports**:
- `AuditLogger` class
- Log level management
- Structured log formatting
- Log file handling

## Validation Modules (`validate/`)

All validation modules follow the pattern:
1. Import from `lib/`
2. Define validation rules
3. Implement `Validator` interface
4. Return `ValidationResult` objects
5. Provide CLI interface

### auto_detect_platform.py
**Critical Module**: Platform detection for all automation  
**Dependencies**: `lib/common`, `lib/validation_framework`  
**Exports**: `detect_platform()`, `PlatformType` enum

## Automation Modules (`automation/`)

### bulk_update_repos_v2.py
**Status**: ✅ Rebuilt (2026-01-19)  
**Purpose**: Schema-driven bulk repository synchronization  
**Dependencies**: `lib/`, `validate/auto_detect_platform`

### auto_create_org_projects.py
**Purpose**: Automated organization project creation  
**Dependencies**: `lib/github_client`, `lib/config_manager`

## Workflows (`.github/workflows/`)

### Reusable Workflows
All reusable workflows follow the pattern:
1. Clear input parameters with descriptions
2. Minimal dependencies
3. Comprehensive error handling
4. Status reporting

### Workflow Categories
1. **CI/CD**: Build, test, deploy workflows
2. **Quality**: Code quality, linting, validation
3. **Automation**: Bulk updates, project management
4. **Security**: Secret scanning, CodeQL, confidentiality
5. **Maintenance**: Cache management, changelog updates

## Coding Standards

### Python
- **Style**: PEP 8 compliant
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style, required for all public functions
- **Error Handling**: Use specific exception types
- **Logging**: Use `audit_logger` for all logging
- **Testing**: Unit tests for all public functions

### YAML (Workflows)
- **Naming**: `kebab-case` for file names
- **Indentation**: 2 spaces
- **Comments**: Document all non-obvious steps
- **Secrets**: Use repository/organization secrets, never hardcode
- **Permissions**: Minimal required permissions only

## File Header Standard

All files must include:
```python
#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# [License text...]
#
# FILE INFORMATION
# DEFGROUP: [Group]
# INGROUP: [Parent Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: [Relative path from repo root]
# VERSION: [X.Y.Z]
# BRIEF: [One-line description]
```

## Error Handling Strategy

### Exit Codes
- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: File/resource not found
- `4`: Permission error
- `5`: Validation failed
- `6`: External dependency error

### Error Messages
Format: `[LEVEL] Component: Message (Context)`
- **ERROR**: Unrecoverable errors
- **WARNING**: Non-fatal issues
- **INFO**: Informational messages
- **DEBUG**: Detailed diagnostic information

## Testing Strategy

### Unit Tests
- Located in `scripts/tests/`
- Use `pytest` framework
- Mock external dependencies
- 80%+ code coverage target

### Integration Tests
- Test workflows end-to-end
- Use test repositories
- Validate against schemas

### Validation Tests
- All validators must have test cases
- Test both valid and invalid inputs
- Test edge cases

## Configuration Management

### Configuration Hierarchy
1. Command-line arguments (highest priority)
2. Environment variables
3. Configuration files (`.mokostandards-sync.yml`)
4. Default values (lowest priority)

### Configuration Schema
Validated against `schemas/unified-repository-schema.json`

## Logging Strategy

### Log Levels
- **DEBUG**: Detailed diagnostic for development
- **INFO**: General informational messages
- **WARNING**: Warning messages, recoverable issues
- **ERROR**: Error messages, unrecoverable issues
- **CRITICAL**: Critical failures requiring immediate attention

### Log Format
```
[TIMESTAMP] [LEVEL] [COMPONENT] Message (context_key=value)
```

## Dependency Management

### Python Dependencies
Minimal external dependencies:
- **Required**: None (stdlib only for core modules)
- **Optional**: 
  - `requests` for GitHub API (fallback to `subprocess` + `gh` CLI)
  - `PyYAML` for YAML parsing (fallback to `json`)
  - `pytest` for testing (dev only)

### Dependency Installation
```bash
pip install -r requirements.txt  # Production
pip install -r requirements-dev.txt  # Development
```

## Migration Guide

### From v1 to v2
1. Update imports to use `lib/` modules
2. Replace ad-hoc validation with `validation_framework`
3. Use `ConfigManager` instead of manual config parsing
4. Replace print statements with `audit_logger`
5. Add type hints to all functions
6. Add docstrings to all public functions

## Performance Considerations

### Caching
- Platform detection results
- GitHub API responses (with expiry)
- Validation results for unchanged files

### Parallelization
- Repository operations can run in parallel
- Use `concurrent.futures` for I/O-bound tasks
- Respect GitHub API rate limits

## Security Considerations

1. **No Hardcoded Secrets**: Use GitHub secrets
2. **Input Validation**: Validate all user inputs
3. **Path Traversal Prevention**: Validate all file paths
4. **Command Injection Prevention**: Use `subprocess` safely
5. **Least Privilege**: Minimal permissions in workflows

## Maintenance

### Version Numbering
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes

### Changelog
All changes documented in `CHANGELOG.md` following Keep a Changelog format.

### Review Process
1. All changes require pull request
2. Automated validation must pass
3. Manual review required
4. Tests must pass

## Future Enhancements

1. **Plugin System**: Allow custom validators
2. **Web Dashboard**: UI for health monitoring
3. **Metrics Collection**: Track validation trends
4. **AI Integration**: Automated issue detection
5. **Multi-language Support**: Beyond Python

## References

- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

**Maintained by**: Moko Consulting  
**Questions**: hello@mokoconsulting.tech  
**Repository**: https://github.com/mokoconsulting-tech/MokoStandards
