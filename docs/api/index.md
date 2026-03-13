# API Documentation

## Overview

This directory contains documentation for the MokoStandards API structure. The documentation mirrors the actual API directory structure found in `/api/`.

## Directory Structure

```
docs/api/
├── index.md                    # This file - API documentation overview
├── analysis/                   # Analysis tools documentation
├── automation/                 # Automation scripts (bulk_sync.php)
├── build/                      # Build tools documentation
├── definitions/                # Repository definitions documentation
│   ├── default/               # Default platform definitions documentation
│   └── sync/                  # Synced repository definitions documentation
├── deploy/                    # Deploy scripts (deploy-sftp.php)
├── fix/                       # Fix utilities (fix_*.php)
├── lib/                       # Library documentation
│   ├── Enterprise/            # Enterprise libraries
│   └── plugins/               # Plugin system
├── maintenance/               # Maintenance scripts documentation
├── plugin/                    # Plugin runner scripts (plugin_*.php)
├── release/                   # Release tools documentation
├── tests/                     # Testing documentation
├── validate/                  # Validation scripts (check_*.php)
└── wrappers/                  # Wrapper scripts documentation
```

## Purpose

The API directory (`/api/`) contains all core functionality for:

- **Repository validation** - Scripts to validate repository structure and compliance
- **Automation** - Bulk sync and automated repository management
- **Definitions** - Repository structure definitions for different platforms
- **Enterprise libraries** - Reusable PHP libraries for GitHub API, logging, metrics
- **Build and release** - Tools for building and releasing projects
- **Analysis** - Code analysis and quality tools
- **Testing** - Test infrastructure and utilities

## Documentation Conventions

### File Organization

- Each API directory has corresponding documentation in `docs/api/`
- Documentation files use `.md` (Markdown) format
- Index files (`index.md`) provide directory overview
- Individual scripts/tools have dedicated documentation files

### Naming Conventions

Documentation files follow these patterns:

- `index.md` - Directory overview and contents listing
- `{script-name}.md` - Documentation for specific script
- `{library-name}.md` - Documentation for specific library
- `overview.md` - Conceptual overview for complex subsystems

### Documentation Structure

Each documentation file should include:

1. **Title and Purpose** - What the component does
2. **Usage** - How to use it (command-line examples, API calls)
3. **Parameters/Options** - Detailed parameter documentation
4. **Examples** - Real-world usage examples
5. **Output** - What to expect from the command/function
6. **Related** - Links to related documentation

## API Directories

### automation/

Automation scripts for bulk repository operations:

- **bulk_sync.php** - Bulk synchronization across multiple repositories
- Repository definition generation
- Automated PR creation and management

[View automation documentation →](./automation/index.md)

### definitions/

Repository structure definitions:

- **default/** - Platform-specific base definitions
- **sync/** - Auto-generated repository-specific definitions

[View definitions documentation →](./definitions/default/index.md)

### validate/

Validation and compliance checking:

- **auto_detect_platform.php** - Platform detection and validation
- **check_repo_health.php** - Repository health scoring
- **check_enterprise_readiness.php** - Enterprise readiness validation

[View validation documentation →](./validate/index.md)

### lib/

Reusable library components:

- **Enterprise/** - GitHub API client, logging, metrics, synchronization
- **plugins/** - Plugin system for platform-specific operations

[View library documentation →](./lib/index.md)

### build/

Build tools and utilities:

- Build automation scripts
- Dependency management
- Asset compilation

[View build documentation →](./build/index.md)

### release/

Release management tools:

- Package generation scripts
- Platform-specific packaging (Joomla, Dolibarr)
- Version management

[View release documentation →](./release/index.md)

### tests/

Testing infrastructure:

- Unit tests
- Integration tests
- Test utilities and helpers

[View testing documentation →](./tests/index.md)

### deploy/

SFTP deployment scripts:

- **deploy-sftp.php** — Upload a repo's `src/` to a remote server using `sftp-config.json`
- Supports PuTTY `.ppk` and OpenSSH PEM keys
- Called by `deploy-dev.yml` and `deploy-release.yml` workflows

[View deploy documentation →](./deploy/index.md)

### plugin/

Plugin-system runner scripts (entry points for governed repos):

- **plugin_validate.php** — Validate project structure and standards
- **plugin_health_check.php** — Run health checks and score
- **plugin_readiness.php** — Check release readiness
- **plugin_metrics.php** — Collect project metrics
- **plugin_list.php** — List all registered project-type plugins

[View plugin script documentation →](./plugin/index.md)

### maintenance/

Maintenance and housekeeping scripts:

- **pin_action_shas.php** — Pin GitHub Actions to immutable SHAs
- **setup_labels.php** — Deploy required GitHub labels
- **sync_dolibarr_readmes.php** — Keep root and src READMEs in sync
- **update_sha_hashes.php** — Regenerate script registry hashes
- **update_version_from_readme.php** — Propagate version from README

[View maintenance documentation →](./maintenance/index.md)

### analysis/

Code analysis tools:

- Static analysis
- Quality metrics
- Dependency analysis

[View analysis documentation →](./analysis/index.md)

### wrappers/

Shell wrappers for cross-platform compatibility:

- **bash/** - Bash wrapper scripts
- **powershell/** - PowerShell wrapper scripts

[View wrappers documentation →](./wrappers/index.md)

## Quick Start

### Repository Validation

```bash
# Auto-detect platform and validate repository
php api/validate/auto_detect_platform.php --path /path/to/repo

# Check repository health score
php api/validate/check_repo_health.php --path /path/to/repo

# Check all validation scripts at once
php api/validate/check_repo_health.php --path . --json
```

### Plugin System

```bash
# Validate a project
php api/plugin_validate.php --project-path /path/to/project

# Check release readiness
php api/plugin_readiness.php --project-path /path/to/project

# Run health check
php api/plugin_health_check.php --project-path /path/to/project

# List all registered plugins
php api/plugin_list.php
```

### Deployment

```bash
# Preview SFTP upload (dry-run)
php api/deploy/deploy-sftp.php --path /path/to/project --dry-run --verbose

# Deploy src/ to remote server
php api/deploy/deploy-sftp.php --path /path/to/project
```

### Bulk Sync

```bash
# Sync templates to multiple repositories
php api/automation/bulk_sync.php \
  --org mokoconsulting-tech \
  --repos "repo1,repo2,repo3"
```

## Development Guidelines

When developing new API components:

1. **Follow existing patterns** - Use established conventions
2. **Add documentation** - Create corresponding docs/api/ documentation
3. **Include examples** - Provide real-world usage examples
4. **Handle errors** - Implement proper error handling and logging
5. **Write tests** - Add test coverage for new functionality
6. **Use type hints** - Declare strict types in PHP code
7. **Log operations** - Use AuditLogger for important operations

## Architecture

### Plugin System

The API uses a plugin architecture for platform-specific operations:

```php
// Auto-detect platform and create plugin
$detector = new ProjectTypeDetector($repoPath);
$projectType = $detector->detect();
$plugin = PluginFactory::createForProject($repoPath);

// Use plugin for platform-specific operations
$health = $plugin->healthCheck();
$metrics = $plugin->collectMetrics();
```

### Enterprise Libraries

Core enterprise libraries provide:

- **ApiClient** - GitHub API client with rate limiting and circuit breaker
- **AuditLogger** - Structured logging with transaction support
- **MetricsCollector** - Metrics collection and reporting
- **RepositorySynchronizer** - Repository synchronization logic

### Validation Pipeline

Repository validation follows this pipeline:

1. **Platform Detection** - Identify repository type
2. **Definition Loading** - Load appropriate structure definition
3. **Structure Validation** - Validate against definition
4. **Health Scoring** - Calculate health score (0-100+)
5. **Report Generation** - Generate validation report

## Related Documentation

- [Validation Guide](../guide/validation/) - Complete validation documentation
- [Automation Guide](../automation/) - Automation workflows and processes
- [Schema Guide](../schemas/repohealth/) - Repository structure schemas
- [Development Guide](../development/) - Development guidelines and standards

---

**Location**: `docs/api/`  
**Purpose**: Documentation for MokoStandards API  
**Mirrors**: `/api/` directory structure  
**Last Updated**: 2026-03-13
**Maintained By**: MokoStandards Team
