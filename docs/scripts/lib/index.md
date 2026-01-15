# Scripts Index: /docs/scripts/lib

## Purpose

Documentation for shared library scripts that provide common utilities, functions, and platform-aware tools for all MokoStandards scripts.

## Available Library Guides

### Python Libraries
- [common-py.md](common-py.md) - Common Python utilities for MokoStandards scripts (✅ Complete)
- common-sh.md - Common Bash utilities for shell scripts (Coming Soon)
- extension-utils-py.md - Platform-aware extension utilities (Coming Soon)
- joomla-manifest-py.md - Joomla manifest parsing utilities (Coming Soon)

## Quick Reference

| Library | Status | Purpose |
|---------|--------|---------|
| `common.py` | ✅ Documented | Python utilities - logging, error handling, file ops |
| `common.sh` | 📝 Pending | Bash utilities - same functionality as Python version |
| `extension_utils.py` | 📝 Pending | Joomla/Dolibarr platform detection |
| `joomla_manifest.py` | 📝 Pending | Joomla manifest parsing and validation |

## Library Usage Patterns

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
```

### Shell Scripts

```bash
#!/usr/bin/env bash

# Source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

# Initialize script
init_script
```

## Navigation

- [⬆️ Back to Scripts Documentation](../README.md)
- [📂 View Library Scripts Source](/scripts/lib/)
- [📖 Library Scripts Index](/scripts/lib/index.md)

## Metadata

- **Document Type:** index
- **Category:** Library Script Documentation
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial library docs index creation | GitHub Copilot |
