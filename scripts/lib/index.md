# Scripts Index: /scripts/lib

## Purpose

Shared library scripts providing common utilities, functions, and platform-aware tools for all MokoStandards scripts.

## Library Scripts in This Directory

### common.py
**Purpose:** Common Python utilities for MokoStandards scripts  
**Type:** Python Library (3.7+)  
**Import:** `from scripts.lib import common`  
**Documentation:** [📖 Guide](/docs/scripts/lib/common-py.md)

**Exported Functions:**
- **Logging:** `log_info()`, `log_success()`, `log_warning()`, `log_error()`, `log_debug()`
- **Error Handling:** `die()`, `require_file()`, `require_dir()`
- **Repository Utils:** `get_repo_root()`, `get_relative_path()`
- **File Operations:** `ensure_dir()`, `is_excluded_path()`
- **Header Generation:** `generate_python_header()`, `generate_shell_header()`
- **JSON Output:** `json_output()`

**Exit Codes:**
- `EXIT_SUCCESS = 0`
- `EXIT_ERROR = 1`
- `EXIT_INVALID_ARGS = 2`
- `EXIT_NOT_FOUND = 3`
- `EXIT_PERMISSION = 4`

### common.sh
**Purpose:** Common Bash utilities for shell scripts  
**Type:** Shell Library (Bash 4.0+)  
**Source:** `source scripts/lib/common.sh`  
**Documentation:** [📖 Guide](/docs/scripts/lib/common-sh.md)

**Exported Functions:**
- **Logging:** `log_info()`, `log_success()`, `log_warning()`, `log_error()`, `log_debug()`
- **Error Handling:** `die()`, `require_command()`, `require_file()`, `require_dir()`
- **Repository Utils:** `get_repo_root()`, `get_relative_path()`
- **Path Utils:** `ensure_dir()`, `is_excluded_path()`
- **File Operations:** `safe_copy()`
- **String Utils:** `trim()`, `to_lower()`, `to_upper()`
- **Validation:** `is_set()`, `is_root()`, `is_port_in_use()`
- **Git Integration:** `get_git_branch()`, `get_git_commit()`, `is_git_clean()`
- **Script Init:** `init_script()`, `print_header()`, `print_footer()`

### extension_utils.py
**Purpose:** Platform-aware extension utilities for Joomla and Dolibarr  
**Type:** Python Library (3.7+)  
**Import:** `from scripts.lib import extension_utils`  
**Documentation:** [📖 Guide](/docs/scripts/lib/extension-utils-py.md)

**Key Classes:**
- `Platform` - Enum: JOOMLA, DOLIBARR, UNKNOWN
- `ExtensionInfo` - Dataclass with platform, name, version, type, manifest path

**Key Functions:**
- `detect_joomla_manifest(src_dir)` - Find Joomla manifest files
- `parse_joomla_manifest(path)` - Parse Joomla XML manifest
- `detect_dolibarr_manifest(src_dir)` - Find Dolibarr descriptor files
- `parse_dolibarr_descriptor(path)` - Parse Dolibarr PHP descriptor
- `get_extension_info(src_dir)` - Unified detection (tries both platforms)
- `is_joomla_extension(src_dir)` - Quick Joomla check
- `is_dolibarr_extension(src_dir)` - Quick Dolibarr check

### joomla_manifest.py
**Purpose:** Joomla manifest parsing and validation utilities  
**Type:** Python Library (3.7+)  
**Import:** `from scripts.lib import joomla_manifest`  
**Documentation:** [📖 Guide](/docs/scripts/lib/joomla-manifest-py.md)

**Key Classes:**
- `ExtensionType` - Constants for Joomla extension types
- `ManifestInfo` - Dataclass with parsed manifest data

**Key Functions:**
- `find_manifest(src_dir)` - Find primary manifest file
- `find_all_manifests(src_dir)` - Find all manifest files
- `parse_manifest(path)` - Parse XML manifest into ManifestInfo
- `get_manifest_version(path)` - Extract version only
- `get_manifest_name(path)` - Extract name only
- `get_manifest_type(path)` - Extract type only
- `validate_manifest(path)` - Validate manifest completeness

## Quick Reference

| Library | Language | Primary Use Case |
|---------|----------|------------------|
| `common.py` | Python 3.7+ | Standard utilities |
| `common.sh` | Bash 4.0+ | Shell utilities |
| `extension_utils.py` | Python 3.7+ | Platform detection |
| `joomla_manifest.py` | Python 3.7+ | Joomla manifest handling |

## Usage Patterns

### Python Scripts
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

# Import libraries
import common
from extension_utils import get_extension_info
from joomla_manifest import find_manifest

# Use utilities
common.log_info("Starting script...")
repo_root = common.get_repo_root()
```

### Shell Scripts
```bash
#!/usr/bin/env bash

# Source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

# Initialize script
init_script

# Use utilities
log_info "Starting script..."
REPO_ROOT=$(get_repo_root)
```

## Dependencies

**Python Libraries:**
- Standard library only (no external packages)
- `pathlib`, `os`, `sys`, `re`, `json`
- `xml.etree.ElementTree` for XML parsing
- `dataclasses` and `typing` for type hints

**Shell Tools:**
- Bash 4.0+ with standard utilities
- `git` for repository operations
- `lsof` or `netstat` for port checking

## Design Principles

1. **No External Dependencies:** Libraries use only standard library modules
2. **Cross-Platform:** Works on Linux, macOS, and Windows (with appropriate shell)
3. **Consistent Interface:** Python and shell libraries mirror each other
4. **Emoji Logging:** Consistent emoji-based logging across all scripts
5. **Error Handling:** Standardized exit codes and error messages

## Integration Points

### Used By All Scripts
Nearly all scripts in MokoStandards import these libraries:
- Validation scripts use common utilities
- Release scripts use extension utilities
- Automation scripts use all libraries

### Platform Detection
Extension utilities enable cross-platform builds:
- Auto-detect Joomla vs Dolibarr projects
- Extract version information
- Validate manifest files

## Version Requirements

- **Python:** 3.7+ (3.9+ recommended for optimal type hints)
- **PowerShell:** 7.0+ (PowerShell Core) - Future library implementations
- **Bash:** 4.0+ required for shell library
- **Git:** 2.0+ for repository utilities

## Best Practices

### Error Handling
```python
# Python: Use die() for fatal errors
if not config_file.exists():
    common.die(f"Config file not found: {config_file}", common.EXIT_NOT_FOUND)
```

```bash
# Bash: Use die for fatal errors
if [[ ! -f "$config_file" ]]; then
    die "Config file not found: $config_file" "$EXIT_NOT_FOUND"
fi
```

### Logging
```python
# Use appropriate log levels
common.log_info("Processing files...")
common.log_success("All files processed successfully")
common.log_warning("Skipping optional step")
common.log_error("Failed to process file")
```

### Path Handling
```python
# Always use pathlib for cross-platform compatibility
from pathlib import Path
file_path = Path("relative/path/to/file")
absolute_path = common.get_repo_root() / file_path
```

## Metadata

- **Document Type:** index
- **Category:** Library Scripts
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial comprehensive lib index with usage patterns | GitHub Copilot |

## Related Documentation

- [Scripts Documentation Root](/docs/scripts/README.md)
- [Python Style Guide](/docs/policy/python-standards.md)
- [Shell Scripting Guide](/docs/policy/shell-standards.md)
- [API Reference](/docs/api/) - Detailed function references
