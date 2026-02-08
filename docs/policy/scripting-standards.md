<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Development
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/scripting-standards.md
VERSION: 03.01.02
BRIEF: Standards and requirements for automation scripts and tooling
-->

# Scripting Standards Policy

## Purpose

This policy establishes mandatory standards for all automation scripts, build tools, validation utilities, and development tooling across MokoStandards-governed repositories. It defines language requirements, coding standards, documentation expectations, and maintenance obligations to ensure consistent, maintainable, and secure automation.

## Scope

This policy applies to:

- All automation scripts in `scripts/` directory
- CI/CD pipeline scripts
- Build and deployment automation
- Validation and testing utilities
- Development tooling and helpers
- Code generation scripts
- Migration and setup scripts

This policy does not apply to:

- Application source code (governed by language-specific standards)
- Configuration files (YAML, JSON, etc.)
- Documentation markdown files
- Data files or static assets

## Responsibilities

### Script Authors

Responsible for:

- Writing scripts in approved languages
- Following coding standards and conventions
- Documenting script purpose and usage
- Testing scripts before committing
- Maintaining scripts they create

### Repository Maintainers

Responsible for:

- Reviewing script pull requests
- Enforcing scripting standards
- Testing scripts in CI/CD
- Approving exceptions to standards
- Archiving deprecated scripts

### Security Owner

Accountable for:

- Reviewing security implications of scripts
- Approving scripts with elevated privileges
- Ensuring secure coding practices
- Validating input sanitization

## Language Requirements

### Primary Language: Python

**All new automation scripts MUST be written in Python.**

**Rationale**:
- Cross-platform compatibility (Windows, macOS, Linux)
- Rich standard library reduces external dependencies
- Excellent tooling and IDE support
- Strong typing support with type hints
- Widely known by development teams
- Active ecosystem and community

**Version Requirements**:
- Minimum: Python 3.9
- Recommended: Python 3.11 or later
- Use version-agnostic features when possible
- Document minimum version in script header

**Example Header**:
```python
#!/usr/bin/env python3
"""
Script description here.

Requires: Python 3.9+
"""
```

### Prohibited Languages for New Scripts

The following languages are prohibited for new automation scripts:

- **Shell scripts** (bash, sh, zsh): Platform-specific, poor error handling
- **Batch files** (.bat, .cmd): Windows-only, limited functionality
- **PowerShell** (.ps1): Windows-focused, inconsistent cross-platform
- **Perl**: Declining ecosystem, poor readability
- **Ruby**: Less common in our tech stack

### Exceptions for Existing Scripts

**Legacy Validation Scripts** in `templates/scripts/validate/`:
- Existing bash scripts (`.sh`) are **grandfathered**
- May remain as bash for backward compatibility
- Should not be rewritten unless functional changes needed
- New validation scripts must use Python

**Minimal Wrapper Scripts**:
- Simple CI/CD entry points (< 10 lines) may use bash
- Must only call Python scripts or system commands
- Require maintainer approval

**Exception Process**:
1. Document technical justification
2. Provide cross-platform compatibility plan
3. Get Security Owner approval for privileged operations
4. Get maintainer approval
5. Document exception in script header

## Python Coding Standards

### File Structure

```python
#!/usr/bin/env python3
"""
Module docstring with description.

This script does XYZ and is used for ABC.

Usage:
    python script_name.py [arguments]

Examples:
    python script_name.py --input file.txt
    python script_name.py --verbose --output result.json

Requirements:
    Python 3.9+
    No external dependencies (or list them)
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

# Constants
DEFAULT_VALUE = "value"
MAX_RETRIES = 3

def main():
    """Main entry point."""
    pass

if __name__ == "__main__":
    main()
```

### Naming Conventions

**Files**:
- Use `snake_case` for filenames: `sync_file_to_project.py`
- Use descriptive, action-oriented names: `validate_manifest.py`
- Avoid abbreviations unless widely understood

**Functions**:
- Use `snake_case`: `def process_file(path: str):`
- Use verb-noun pattern: `create_issue()`, `update_project()`
- Private functions prefix with underscore: `def _internal_helper():`

**Classes**:
- Use `PascalCase`: `class ProjectManager:`
- Use noun phrases: `GitHubClient`, `DocumentParser`

**Constants**:
- Use `UPPER_SNAKE_CASE`: `DEFAULT_PROJECT_NUMBER = 7`
- Define at module level after imports

**Variables**:
- Use `snake_case`: `file_path`, `issue_count`
- Use descriptive names, avoid single letters except loops
- Boolean variables use `is_`, `has_`, `should_` prefix

### Type Hints

**Type hints are REQUIRED for all function signatures:**

```python
from typing import Dict, List, Optional, Tuple

def process_files(
    paths: List[str],
    output_dir: str,
    verbose: bool = False
) -> Tuple[int, List[str]]:
    """Process multiple files and return count and errors."""
    pass

def get_config(name: str) -> Optional[Dict[str, str]]:
    """Get configuration by name, returns None if not found."""
    pass
```

**Benefits**:
- Enables static type checking with mypy
- Improves IDE autocomplete
- Self-documenting code
- Catches bugs before runtime

### Documentation

**Docstrings are REQUIRED for all public functions:**

```python
def sync_file_to_project(
    file_path: str,
    project_number: int = 7,
    is_folder: bool = False
) -> bool:
    """
    Sync a file or folder to GitHub Project.

    Args:
        file_path: Path to file or folder to sync
        project_number: GitHub Project number (default: 7)
        is_folder: Whether path is a folder (default: False)

    Returns:
        True if sync successful, False otherwise

    Raises:
        ValueError: If file_path is invalid
        RuntimeError: If GitHub API fails

    Example:
        >>> sync_file_to_project("docs/policy/new.md")
        True
    """
    pass
```

**Docstring Format**: Use Google style docstrings

### Code Formatting

**Indentation**: Use tabs, not spaces (MokoStandards standard)

- Configure editor to use tabs with 2-space visual width
- Follow .editorconfig settings in repository root
- Be consistent throughout script
- **Exception**: YAML configuration files must use spaces (YAML specification requirement)

**Line length**:
- Maximum 120 characters per line
- Break long lines at logical points

**Formatting tools**:
- Use `black` for Python formatting (configure for tabs if possible, or follow project .editorconfig)
- Use `pylint` for style checking
- Use `mypy` for type checking

### Error Handling

**Proper error handling is REQUIRED:**

```python
import sys
from pathlib import Path

def load_file(path: str) -> str:
    """Load file contents with error handling."""
    file_path = Path(path)

    if not file_path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        return file_path.read_text(encoding="utf-8")
    except PermissionError:
        print(f"Error: Permission denied: {path}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Invalid UTF-8 encoding: {path}", file=sys.stderr)
        sys.exit(1)
```

**Best Practices**:
- Use specific exceptions, not bare `except:`
- Print errors to `stderr` using `sys.stderr`
- Exit with non-zero code on failure: `sys.exit(1)`
- Exit with zero on success: `sys.exit(0)`
- Provide helpful error messages with context

### Command-Line Arguments

**Use `argparse` for all command-line scripts:**

```python
import argparse

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Sync documentation to GitHub Project'
    )
    parser.add_argument(
        'path',
        help='Path to file or folder to sync'
    )
    parser.add_argument(
        '--project',
        type=int,
        default=7,
        help='Project number (default: 7)'
    )
    parser.add_argument(
        '--folder',
        action='store_true',
        help='Treat path as folder'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Use args.path, args.project, etc.
```

**Benefits**:
- Automatic `--help` generation
- Type validation
- Default value handling
- Standard argument syntax

### Dry-Run Support

**All scripts that modify files or system state MUST support `--dry-run` mode.**

**Requirements:**

```python
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Show what would be done without making changes'
)
```

**Implementation:**

```python
def process_files(files: List[Path], dry_run: bool = False):
    """Process files with optional dry-run mode."""
    for file in files:
        if dry_run:
            logger.info(f"[DRY-RUN] Would process: {file}")
        else:
            logger.info(f"Processing: {file}")
            # actual processing
```

**Dry-run best practices:**
- Use `[DRY-RUN]` prefix in all log messages during dry-run
- Validate all inputs and logic in dry-run mode
- Exit with same status codes as actual execution would
- Show what would be done, not just what would be checked
- Skip any operations that modify state (file writes, API calls, etc.)

**Scripts requiring dry-run:**
- ✅ File modification scripts (e.g., `file_headers.py`, `tabs.py`)
- ✅ Validation scripts that could fail builds (e.g., `security_scan.py`)
- ✅ Deployment or release scripts
- ✅ Scripts that interact with external systems

**Scripts exempt from dry-run:**
- ❌ Read-only analysis scripts
- ❌ Simple query scripts with no side effects
- ❌ Scripts that only display information

### Dependencies

**Minimize external dependencies:**

**Prefer standard library**:
- ✅ Use `pathlib` for paths (not `os.path`)
- ✅ Use `subprocess` for external commands
- ✅ Use `json` for JSON parsing
- ✅ Use `argparse` for CLI arguments
- ✅ Use `typing` for type hints

**Avoid unnecessary packages**:
- ❌ Don't use `requests` if `urllib` works
- ❌ Don't use `click` for simple CLIs
- ❌ Don't use `sh` when `subprocess` works

**If external dependencies are required**:
1. Document in script docstring
2. Add to `requirements.txt`
3. Use virtual environments
4. Pin versions for reproducibility
5. Get maintainer approval

### File Permissions

**Scripts must be executable:**

```bash
chmod +x scripts/my_script.py
```

**Include shebang line:**

```python
#!/usr/bin/env python3
```

**Git should track executable bit:**

```bash
git add --chmod=+x scripts/my_script.py
```

## Security Requirements

### Input Validation

**All user input MUST be validated:**

```python
from pathlib import Path

def validate_file_path(path: str) -> Path:
    """Validate and sanitize file path."""
    file_path = Path(path).resolve()

    # Check for path traversal
    if ".." in path:
        raise ValueError("Path traversal not allowed")

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File not found: {path}")

    # Check file is within allowed directory
    allowed_dir = Path.cwd()
    if not str(file_path).startswith(str(allowed_dir)):
        raise ValueError("Access outside repository not allowed")

    return file_path
```

**Requirements**:
- Validate all command-line arguments
- Sanitize file paths (prevent path traversal)
- Validate file types and extensions
- Check file sizes before processing
- Escape shell commands properly

### Credentials and Secrets

**Credentials MUST NEVER be hardcoded:**

```python
import os

# ✅ Correct: Use environment variables
github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
    sys.exit(1)

# ❌ Incorrect: Hardcoded credentials
github_token = "ghp_xxxxxxxxxxxx"  # NEVER DO THIS
```

**Best Practices**:
- Use environment variables for credentials
- Use GitHub Secrets in CI/CD
- Never log credentials
- Never commit credentials
- Document required environment variables

### Shell Command Execution

**Use `subprocess` safely:**

```python
import subprocess
from typing import List

# ✅ Correct: List of arguments (no shell injection)
def run_command(args: List[str]) -> str:
    """Run command safely without shell."""
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

# ❌ Incorrect: Shell=True with user input (injection risk)
def run_command_unsafe(user_input: str):
    subprocess.run(f"echo {user_input}", shell=True)  # VULNERABLE
```

**Requirements**:
- Use `subprocess.run()` with list of arguments
- Never use `shell=True` with user input
- Validate all command arguments
- Use `check=True` to raise on errors
- Capture output properly

### Privilege Management

**Scripts requiring elevated privileges need approval:**

**Requirements**:
- Document why elevated privileges needed
- Minimize scope of privileged operations
- Use principle of least privilege
- Get Security Owner approval
- Add security warning in documentation

## Testing Requirements

### Unit Tests

**Scripts with complex logic MUST have unit tests:**

```python
# In script: scripts/my_script.py
def calculate_priority(doc_type: str) -> str:
    """Calculate priority based on document type."""
    if doc_type == "policy":
        return "High"
    return "Medium"

# In test: tests/test_my_script.py
import unittest
from scripts.my_script import calculate_priority

class TestPriorityCalculation(unittest.TestCase):
    def test_policy_priority(self):
        self.assertEqual(calculate_priority("policy"), "High")

    def test_default_priority(self):
        self.assertEqual(calculate_priority("guide"), "Medium")

if __name__ == "__main__":
    unittest.main()
```

**Test Requirements**:
- Test all public functions
- Test error cases and edge cases
- Use `unittest` or `pytest`
- Place tests in `tests/` directory
- Run tests in CI/CD

### Manual Testing

**All scripts MUST be manually tested before commit:**

**Testing Checklist**:
- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test with missing arguments
- [ ] Test `--help` output
- [ ] Test error messages
- [ ] Test in clean environment
- [ ] Test cross-platform (if applicable)

### CI/CD Validation

**Scripts MUST pass CI/CD checks:**

- Syntax validation with `python -m py_compile`
- Type checking with `mypy` (if configured)
- Linting with `pylint` or `flake8` (if configured)
- Unit tests execution
- Integration tests in workflow

## Documentation Requirements

### README Files

**Script directories MUST have README.md:**

```markdown
# Scripts

## Available Scripts

### sync_file_to_project.py

Syncs documentation files and folders to GitHub Project.

**Usage**:
```bash
python scripts/sync_file_to_project.py <path> [project_number]
```

**Examples**:
```bash
python scripts/sync_file_to_project.py docs/policy/new.md
python scripts/sync_file_to_project.py docs/guide/ --folder
```

**Requirements**:
- Python 3.9+
- GitHub CLI (`gh`) installed and authenticated
```

### Inline Comments

**Use comments for complex logic only:**

```python
# ✅ Good: Explains non-obvious logic
# Calculate priority based on business rules where policies
# are high priority due to governance requirements
priority = "High" if doc_type == "policy" else "Medium"

# ❌ Bad: States the obvious
# Set priority to High
priority = "High"
```

**When to comment**:
- Explain "why", not "what"
- Document workarounds
- Explain complex algorithms
- Reference external documentation
- Note TODOs with issue numbers

### File Headers

**All scripts MUST have standard headers:**

```python
#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

[Full license header...]

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Automation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/my_script.py
VERSION: 03.01.02
BRIEF: Brief description of script purpose
"""
```

## Maintenance Requirements

### Version Control

**Scripts MUST follow version control best practices:**

- Commit scripts with descriptive messages
- Reference issue numbers in commits
- Use feature branches for changes
- Submit pull requests for review
- Tag releases when appropriate

### Deprecation Process

**Deprecated scripts MUST follow proper sunset process:**

1. **Mark as deprecated**:
   - Add deprecation warning to script
   - Update documentation
   - Announce in CHANGELOG

2. **Provide migration path**:
   - Document replacement script
   - Provide migration guide
   - Offer transition period

3. **Archive**:
   - Move to `scripts/deprecated/`
   - Keep for historical reference
   - Remove after 6 months

### Update Requirements

**Scripts MUST be kept up to date:**

- Update for Python version changes
- Update for dependency changes
- Update for API changes
- Fix bugs promptly
- Improve based on feedback

## Compliance and Enforcement

### Code Review

**All scripts require code review:**

**Review Checklist**:
- [ ] Written in Python (unless exception approved)
- [ ] Follows naming conventions
- [ ] Has type hints
- [ ] Has docstrings
- [ ] Has error handling
- [ ] Has unit tests (if complex)
- [ ] Validates inputs
- [ ] No hardcoded credentials
- [ ] Documentation complete
- [ ] Tested manually

### Automated Checks

**CI/CD MUST validate scripts:**

```yaml
# In .github/workflows/ci.yml
- name: Validate Python scripts
  run: |
    python -m py_compile scripts/*.py

- name: Check script executability
  run: |
    find scripts -name "*.py" -type f ! -executable -print
    # Should return no results
```

### Exceptions and Waivers

**Exception requests require**:

1. Written justification
2. Technical rationale
3. Maintainer approval
4. Security Owner approval (if security relevant)
5. Documentation in script header
6. Expiration date for review

## Metrics and Reporting

### Quality Metrics

**Track script quality:**

- Number of scripts with tests
- Test coverage percentage
- Number of scripts with type hints
- Number of scripts with proper documentation
- Number of security findings

### Usage Metrics

**Track script usage:**

- Execution frequency in CI/CD
- Manual execution patterns
- Error rates
- Performance metrics

## Dependencies

This policy depends on:

- [Document Formatting Policy](document-formatting.md) - For file headers
- [Security Scanning Policy](security-scanning.md) - For security requirements
- [Dependency Management Policy](dependency-management.md) - For external dependencies
- Python 3.9+ installed in development and CI/CD environments

## Acceptance Criteria

- [ ] All new scripts written in Python
- [ ] All scripts have proper headers
- [ ] All scripts have docstrings
- [ ] All scripts use type hints
- [ ] All scripts handle errors properly
- [ ] All scripts validate inputs
- [ ] No hardcoded credentials
- [ ] All scripts executable with shebang
- [ ] Documentation complete
- [ ] CI/CD validation passes

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/scripting-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
