# Library Scripts

This directory contains shared library code and utility functions used by other scripts.

## Python Libraries

### common.py
Core Python utility functions and common operations.

**Features:**
- Dynamic version extraction from README.md title line
- File system utilities
- Git operations
- GitHub API helpers
- Configuration management
- Logging and error handling
- Path manipulation
- Standard file header generation

### github_client.py
Comprehensive GitHub API client with authentication and rate limiting.

**Features:**
- GitHub API v3 and v4 (GraphQL) support
- Automatic authentication (token, GitHub App)
- Rate limit handling
- Repository management
- Pull request operations
- Issue management
- Project board operations

### config_manager.py
Configuration management for scripts with YAML/JSON support.

**Features:**
- Load and validate configuration files
- Environment variable interpolation
- Default value handling
- Schema validation
- Configuration merging

### extension_utils.py
Utilities for detecting and working with extension types (Joomla, Dolibarr, etc.).

**Features:**
- Extension type detection
- Manifest parsing
- Version extraction
- Platform identification

### joomla_manifest.py
Joomla manifest (XML) parsing and manipulation utilities.

**Features:**
- Parse Joomla manifest files
- Extract metadata (version, name, author)
- Validate manifest structure
- Update manifest fields

### terraform_schema_reader.py
Read and validate Terraform schema definitions.

**Features:**
- Parse Terraform configuration files
- Extract schema definitions
- Validate Terraform syntax
- Schema versioning

### validation_framework.py
Comprehensive validation framework for running multiple validation checks.

**Features:**
- Plugin-based validation system
- Parallel validation execution
- Result aggregation and reporting
- Custom validator creation

### audit_logger.py
Audit logging utilities for tracking script operations.

**Features:**
- Structured audit logs
- Operation tracking
- Change history
- Compliance reporting

### gui_utils.py
GUI utilities for PowerShell and Python scripts (dialogs, file pickers, etc.).

**Features:**
- File selection dialogs
- Folder selection dialogs
- Progress indicators
- Message boxes

## Shell Libraries

### common.sh
Core shell utility functions for bash scripts.

**Features:**
- Dynamic version extraction from README.md title line
- Color output functions
- Error handling
- Git operations
- File system utilities
- Logging functions

## PowerShell Modules

### GuiUtils.psm1
PowerShell GUI utilities module for Windows Forms interfaces.

**Features:**
- File and folder selection dialogs
- Progress bars and status indicators
- Message boxes and confirmations
- Multi-selection controls
- Form creation utilities

**Usage:**
```powershell
Import-Module .\scripts\lib\GuiUtils.psm1
$file = Show-OpenFileDialog -Title "Select File"
```

### Common.psm1
Core PowerShell utility functions and common operations.

**Features:**
- File system operations
- Git commands
- Logging utilities
- Error handling
- Configuration management

### ConfigManager.psm1
PowerShell configuration management module.

**Features:**
- Load and save configuration files
- YAML/JSON/XML support
- Environment variable handling
- Default value management
- Configuration validation

## Template Files

### wrapper-template.ps1
PowerShell wrapper template for Python scripts.

### wrapper-template.sh
Bash wrapper template for Python scripts.

## Purpose

These libraries provide:
- **Reusability**: Common functionality shared across scripts
- **Consistency**: Standard patterns and practices
- **Maintainability**: Centralized updates affect all dependent scripts
- **Testing**: Isolated testing of shared functionality
- **Version Management**: Single source of truth for repository version in README.md

## Version Management

The repository version is maintained in the README.md title line:
```markdown
# README - MokoStandards (VERSION: XX.YY.ZZ)
```

Both `common.py` and `common.sh` dynamically extract this version at runtime:
- **Python**: `VERSION` constant is set by `_get_version_from_readme()`
- **Shell**: `MOKO_VERSION` constant is set by `_get_version_from_readme()`

This ensures:
- Single source of truth for version information
- No manual synchronization needed between scripts
- Automatic version updates when README.md is updated
- Fallback to "04.00.03" if README.md is not accessible

## Usage

Import libraries in your scripts:

```python
# Python
from lib.common import log_info, run_command
from lib.github_client import GitHubClient

# Use library functions
log_info("Starting operation...")
client = GitHubClient()
```

```bash
# Bash
source "$(dirname "$0")/../lib/common.sh"

# Use library functions
log_info "Starting operation..."
```
