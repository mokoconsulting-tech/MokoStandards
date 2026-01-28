# common.py Library Guide

## Overview

The `common.py` module provides standard Python utilities for all MokoStandards scripts. It offers reusable functions for logging, error handling, file operations, and repository introspection with consistent emoji-based output formatting.

## Location

- **Path**: `/scripts/lib/common.py`
- **Type**: Python library module
- **Category**: Library / Utilities

## Version Requirements

- **Python**: 3.7+ (3.9+ recommended for optimal type hints)
- **PowerShell**: 7.0+ (PowerShell Core) - Future PowerShell module planned
- **Dependencies**: Standard library only

## Purpose

This library module serves as the foundation for all Python scripts in MokoStandards by providing:

1. **Standardized Logging:** Consistent emoji-based output across all scripts
2. **Error Handling:** Unified exit codes and error reporting
3. **File Operations:** Cross-platform path handling and validation
4. **Repository Utilities:** Git repository introspection
5. **Header Generation:** Standard GPL-3.0 file headers

## Usage

### Importing the Library

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add lib directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

# Import common utilities
import common

# Or import specific functions
from common import log_info, log_error, die, get_repo_root
```

### Basic Usage Examples

```python
# Logging
common.log_info("Processing files...")
common.log_success("Operation completed successfully")
common.log_warning("Skipping optional step")
common.log_error("Failed to process file")
common.log_debug("Debug information", debug=True)

# Error handling
if not config_file.exists():
    common.die(f"Config not found: {config_file}", common.EXIT_NOT_FOUND)

# File validation
config_file = common.require_file("config.json", "Configuration file")
output_dir = common.require_dir("output/", "Output directory")

# Repository operations
repo_root = common.get_repo_root()
relative_path = common.get_relative_path(__file__)

# Path operations
output_dir = common.ensure_dir("dist/release")
is_excluded = common.is_excluded_path("node_modules/pkg", {"node_modules"})

# JSON output
common.json_output({"status": "success", "count": 42})
```

## API Reference

### Constants

#### Exit Codes
```python
EXIT_SUCCESS = 0        # Successful execution
EXIT_ERROR = 1          # General error
EXIT_INVALID_ARGS = 2   # Invalid command-line arguments
EXIT_NOT_FOUND = 3      # Required file/directory not found
EXIT_PERMISSION = 4     # Permission denied
```

### Logging Functions

#### `log_info(message: str) → None`
Print informational message with ℹ️ emoji.

**Example:**
```python
common.log_info("Starting validation process")
# Output: ℹ️  Starting validation process
```

#### `log_success(message: str) → None`
Print success message with ✅ emoji.

**Example:**
```python
common.log_success("All tests passed")
# Output: ✅ All tests passed
```

#### `log_warning(message: str) → None`
Print warning message with ⚠️ emoji.

**Example:**
```python
common.log_warning("Using default configuration")
# Output: ⚠️  Using default configuration
```

#### `log_error(message: str) → None`
Print error message to stderr with ❌ emoji.

**Example:**
```python
common.log_error("Failed to connect to API")
# Output: ❌ Failed to connect to API (to stderr)
```

#### `log_debug(message: str, debug: Optional[bool] = None) → None`
Print debug message with 🔍 emoji (only if DEBUG environment variable is set or debug=True).

**Example:**
```python
common.log_debug("Variable value: " + str(value))
# Output: 🔍 Variable value: 42 (only in debug mode)
```

#### `json_output(data: dict) → None`
Pretty-print JSON data to stdout.

**Example:**
```python
common.json_output({
    "status": "success",
    "files_processed": 10,
    "errors": []
})
# Output: Pretty-printed JSON
```

### Error Handling Functions

#### `die(message: str, exit_code: int = EXIT_ERROR) → None`
Log error message and exit with specified code. **Does not return.**

**Example:**
```python
if not api_token:
    common.die("API token not configured", common.EXIT_INVALID_ARGS)
```

#### `require_file(file_path: Union[str, Path], description: str = "File") → Path`
Validate file exists, exit if not. Returns Path object.

**Example:**
```python
config_file = common.require_file("config.json", "Configuration file")
# If file doesn't exist: exits with EXIT_NOT_FOUND
```

#### `require_dir(dir_path: Union[str, Path], description: str = "Directory") → Path`
Validate directory exists, exit if not. Returns Path object.

**Example:**
```python
src_dir = common.require_dir("src/", "Source directory")
# If directory doesn't exist: exits with EXIT_NOT_FOUND
```

### Repository Utilities

#### `get_repo_root() → Path`
Find and return repository root directory by walking up directory tree looking for `.git`.

**Example:**
```python
repo_root = common.get_repo_root()
print(f"Repository root: {repo_root}")
# Output: Repository root: /home/user/MokoStandards
```

**Raises:** `SystemExit` if not in a git repository

#### `get_relative_path(file_path: Union[str, Path], from_root: bool = True) → str`
Get relative path from repository root or current working directory.

**Example:**
```python
# From repo root
rel_path = common.get_relative_path(__file__)
# Output: "scripts/validate/no_secrets.py"

# From current directory
rel_path = common.get_relative_path(__file__, from_root=False)
# Output: "../validate/no_secrets.py"
```

### Path Utilities

#### `ensure_dir(dir_path: Union[str, Path], description: str = "Directory") → Path`
Create directory if it doesn't exist. Returns Path object.

**Example:**
```python
output_dir = common.ensure_dir("dist/release", "Release output directory")
# Creates directory if missing, returns Path object
```

#### `is_excluded_path(path: Union[str, Path], exclusions: Set[str]) → bool`
Check if path matches any exclusion pattern.

**Example:**
```python
excluded_dirs = {"node_modules", "vendor", ".git"}
if not common.is_excluded_path(file_path, excluded_dirs):
    process_file(file_path)
```

**Pattern Matching:**
- Exact match: `"node_modules"` matches `path/node_modules/file`
- Wildcard: `"*.tmp"` matches `file.tmp`

### Header Generation

#### `generate_python_header(...) → str`
Generate standard GPL-3.0 file header for Python files.

**Parameters:**
```python
def generate_python_header(
    file_path: Union[str, Path],
    brief: str,
    defgroup: str = "MokoStandards.Scripts",
    ingroup: str = "MokoStandards",
    version: str = "04.01.00",
    note: Optional[str] = None
) → str
```

**Example:**
```python
header = common.generate_python_header(
    file_path="scripts/validate/new_validator.py",
    brief="Validate new feature implementation",
    defgroup="MokoStandards.Validation",
    note="Requires Python 3.9+"
)
print(header)
```

#### `generate_shell_header(...) → str`
Generate standard GPL-3.0 file header for shell scripts.

**Parameters:** Same as `generate_python_header()`

**Example:**
```python
header = common.generate_shell_header(
    file_path="scripts/maintenance/cleanup.sh",
    brief="Clean up temporary files",
    version="01.00.00"
)
with open("cleanup.sh", "w") as f:
    f.write(header)
    f.write("\n# Script content here\n")
```

## Requirements

### Python Version
- Python 3.7+ required
- Python 3.9+ recommended for optimal type hint support

### Dependencies
**Standard Library Only:**
- `os` - Operating system interface
- `sys` - System-specific parameters
- `pathlib` - Object-oriented filesystem paths
- `typing` - Type hint support

No external packages required. ✅

### File System Requirements
- Read/write access to working directory
- Git repository context (for `get_repo_root()`)

## Integration

### Used By Scripts

**Validation Scripts:**
- `validate/no_secrets.py`
- `validate/check_repo_health.py`
- `validate/validate_structure.py`
- `validate/xml_wellformed.py`
- All other validation scripts

**Automation Scripts:**
- `automation/bulk_update_repos.py`
- `automation/sync_file_to_project.py`
- `automation/auto_create_org_projects.py`

**Release Scripts:**
- `release/package_extension.py`
- `release/dolibarr_release.py`

**Maintenance Scripts:**
- `maintenance/validate_file_headers.py`
- `maintenance/update_changelog.py`
- `maintenance/release_version.py`

**Nearly all Python scripts** in MokoStandards import this library.

### Design Patterns

#### Consistent Error Handling
```python
import common

def main():
    try:
        # Script logic
        config = common.require_file("config.json")
        # ... processing ...
        common.log_success("Processing complete")
        sys.exit(common.EXIT_SUCCESS)
    
    except KeyboardInterrupt:
        common.log_warning("Interrupted by user")
        sys.exit(common.EXIT_ERROR)
    
    except Exception as e:
        common.die(f"Unexpected error: {e}", common.EXIT_ERROR)
```

#### Progress Logging
```python
import common

common.log_info("Starting multi-step process...")

# Step 1
common.log_info("Step 1: Loading configuration")
config = load_config()
common.log_success("Configuration loaded")

# Step 2
common.log_info("Step 2: Processing files")
process_files(config)
common.log_success("Files processed")

# Complete
common.log_success("All steps completed successfully")
```

#### Repository-Relative Paths
```python
import common
from pathlib import Path

# Get repository root
repo_root = common.get_repo_root()

# Construct paths relative to repo
templates_dir = repo_root / "templates"
output_dir = repo_root / "dist"

# Log relative paths for clarity
rel_path = common.get_relative_path(output_file)
common.log_info(f"Writing to: {rel_path}")
```

## Best Practices

### 1. Always Import at Script Start
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Import common library first
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
import common
```

### 2. Use Appropriate Log Levels
```python
# Info: Informational messages about progress
common.log_info("Processing 42 files...")

# Success: Successful completion of operations
common.log_success("All files processed")

# Warning: Non-fatal issues
common.log_warning("Skipping optional validation")

# Error: Fatal errors (also use die() for immediate exit)
common.log_error("Failed to connect to service")
common.die("Cannot continue without connection", common.EXIT_ERROR)
```

### 3. Validate Early with require_*
```python
# Validate all inputs at script start
def main():
    args = parse_args()
    
    # Validate required files/directories immediately
    config_file = common.require_file(args.config)
    input_dir = common.require_dir(args.input_dir)
    output_dir = common.ensure_dir(args.output_dir)
    
    # Continue with script logic knowing inputs are valid
```

### 4. Use Consistent Exit Codes
```python
# Return appropriate exit codes
if validation_failed:
    sys.exit(common.EXIT_ERROR)
elif invalid_arguments:
    sys.exit(common.EXIT_INVALID_ARGS)
else:
    sys.exit(common.EXIT_SUCCESS)
```

### 5. Leverage Path Utilities
```python
# Use ensure_dir() instead of manual mkdir
output_dir = common.ensure_dir("dist/release")

# Use get_repo_root() for repository-relative operations
repo_root = common.get_repo_root()
config_file = repo_root / "config" / "settings.json"
```

## Error Handling

### Common Patterns

**Pattern 1: Graceful Degradation**
```python
try:
    optional_config = load_optional_config()
except FileNotFoundError:
    common.log_warning("Optional config not found, using defaults")
    optional_config = get_defaults()
```

**Pattern 2: Fail Fast**
```python
# Use die() for unrecoverable errors
if not api_token:
    common.die("API_TOKEN environment variable not set", common.EXIT_INVALID_ARGS)
```

**Pattern 3: Detailed Error Context**
```python
try:
    result = process_file(file_path)
except Exception as e:
    common.log_error(f"Failed to process {file_path}: {e}")
    # Continue with other files or exit depending on requirements
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.01.00 | 2026-01-15 | Current version with full feature set |
| 04.00.00 | 2025-12-01 | Added header generation functions |
| 03.00.00 | 2025-11-01 | Added path utilities |
| 02.00.00 | 2025-10-01 | Added repository utilities |
| 01.00.00 | 2025-09-01 | Initial release with logging and error handling |

## Related Libraries

- [common.sh](common-sh.md) - Shell script equivalent
- [extension_utils.py](extension-utils-py.md) - Platform detection utilities
- [joomla_manifest.py](joomla-manifest-py.md) - Joomla manifest handling

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
