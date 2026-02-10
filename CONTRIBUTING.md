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
 along with this program (./LICENSE).

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 03.01.03
 PATH: ./CONTRIBUTING.md
 BRIEF: v2.0 contribution guidelines with Python/PowerShell standards, Google docstrings, 100% type hints
 NOTE: Breaking changes from v1 - no backward compatibility
-->

# Contributing to MokoStandards v2.0

Welcome! Thank you for your interest in contributing to MokoStandards. This guide defines contribution requirements, development standards, and workflows for the v2.0 release. Version 2.0 introduces breaking changes with enhanced automation, comprehensive documentation, and strict code quality standards.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Quick Start](#quick-start)
- [Getting Started](#getting-started)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Code Review Process](#code-review-process)
- [Documentation Standards](#documentation-standards)
- [Version Numbering](#version-numbering)
- [Questions and Support](#questions-and-support)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to hello@mokoconsulting.tech.

## Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/MokoStandards.git
cd MokoStandards

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make changes following v2 standards
# - Python: 100% type hints, Google docstrings
# - PowerShell: Full comment-based help
# - All: Proper file headers

# 5. Test your changes
python -m pytest scripts/tests/
python scripts/validate/validate_file_headers.py .

# 6. Commit and push
git add .
git commit -m "Add: Brief description of changes"
git push origin feature/your-feature-name

# 7. Open Pull Request
# Use PR template and reference related issues
```

## Getting Started

### Prerequisites

**Required**:
- Git 2.0+
- Python 3.8+ (scripts and automation)
- Text editor with Python support (VS Code, PyCharm, etc.)

**Optional**:
- PowerShell 5.1+ or PowerShell Core 7+ (Windows scripts)
- Make (for Makefile usage)
- GitHub CLI (`gh`) for workflow automation

### Development Environment Setup

#### 1. Fork and Clone

```bash
# Fork repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/MokoStandards.git
cd MokoStandards
git remote add upstream https://github.com/mokoconsulting-tech/MokoStandards.git
```

#### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python --version  # Should be 3.9+
python scripts/validate/validate_file_headers.py --help
```

#### 3. Configure Git

```bash
# Use provided commit message template
git config commit.template .gitmessage

# Configure your identity
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

#### 4. Verify Setup

```bash
# Run validation scripts
python scripts/validate/validate_file_headers.py .
python scripts/validate/validate_workflows.py .github/workflows/

# Run tests
python -m pytest scripts/tests/ -v
```

## Code Standards

### Python Standards (Primary Language)

MokoStandards v2 uses **Python as the primary automation language**. All new scripts must be written in Python following these standards.

#### File Structure

```python
#!/usr/bin/env python3
"""
Brief one-line description.

Detailed description of what this script does and why it exists.
Multiple paragraphs are allowed.

Usage:
    python script_name.py [options] arguments

Examples:
    python script_name.py --input file.txt
    python script_name.py --verbose --output result.json

Requirements:
    Python 3.8+
    Optional: list external dependencies
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple

# Constants
DEFAULT_VALUE: str = "value"
MAX_RETRIES: int = 3


def main() -> int:
    """Main entry point."""
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### Type Hints (REQUIRED - 100% Coverage)

**All function signatures MUST include complete type hints:**

```python
from typing import Dict, List, Optional, Tuple, Union

# ✅ Correct: Full type hints
def process_files(
    paths: List[str],
    output_dir: str,
    verbose: bool = False
) -> Tuple[int, List[str]]:
    """Process multiple files and return count and errors."""
    errors: List[str] = []
    count: int = 0

    for path in paths:
        count += 1

    return count, errors

# ✅ Correct: Optional return type
def get_config(name: str) -> Optional[Dict[str, str]]:
    """Get configuration by name, returns None if not found."""
    if name == "default":
        return {"key": "value"}
    return None

# ❌ Incorrect: Missing type hints
def process_files(paths, output_dir, verbose=False):
    pass
```

#### Google-Style Docstrings (REQUIRED)

**All public functions, classes, and methods MUST have Google-style docstrings:**

```python
def sync_file_to_project(
    file_path: str,
    project_number: int = 7,
    is_folder: bool = False
) -> bool:
    """
    Sync a file or folder to GitHub Project.

    This function synchronizes documentation files or folders to a GitHub
    Project board for tracking purposes. It validates the path, checks
    permissions, and updates the project board via GitHub API.

    Args:
        file_path: Path to file or folder to sync (relative or absolute)
        project_number: GitHub Project number (default: 7)
        is_folder: Whether path is a folder (default: False)

    Returns:
        True if sync successful, False otherwise

    Raises:
        ValueError: If file_path is invalid or inaccessible
        RuntimeError: If GitHub API call fails
        PermissionError: If insufficient permissions for file

    Examples:
        >>> sync_file_to_project("docs/policy/new.md")
        True
        >>> sync_file_to_project("docs/guide/", is_folder=True)
        True

    Note:
        Requires GITHUB_TOKEN environment variable to be set.
    """
    pass
```

**Docstring Sections**:
- **Brief**: One-line summary (first line)
- **Description**: Detailed explanation (optional, after blank line)
- **Args**: All parameters with types and descriptions
- **Returns**: Return value description and type
- **Raises**: All exceptions that may be raised
- **Examples**: Usage examples (optional but recommended)
- **Note/Warning**: Important information (optional)

#### Naming Conventions

**Files**: `snake_case`
```python
validate_file_headers.py
sync_file_to_project.py
repository_health.py
```

**Functions**: `snake_case`, verb-noun pattern
```python
def create_issue() -> None:
def update_project(project_id: int) -> bool:
def get_file_content(path: str) -> str:
```

**Classes**: `PascalCase`, noun phrases
```python
class ProjectManager:
class GitHubClient:
class DocumentParser:
```

**Constants**: `UPPER_SNAKE_CASE`
```python
DEFAULT_PROJECT_NUMBER: int = 7
MAX_RETRIES: int = 3
API_TIMEOUT: float = 30.0
```

**Variables**: `snake_case`, descriptive
```python
file_path: str = "docs/policy.md"
issue_count: int = 0
is_valid: bool = True
has_permission: bool = False
```

#### Error Handling

```python
import sys
from pathlib import Path
from typing import Optional

def load_file(path: str) -> Optional[str]:
    """
    Load file contents with comprehensive error handling.

    Args:
        path: Path to file

    Returns:
        File contents as string, or None on error

    Raises:
        FileNotFoundError: If file does not exist
        PermissionError: If insufficient permissions
        UnicodeDecodeError: If file encoding is invalid
    """
    file_path = Path(path)

    if not file_path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        raise FileNotFoundError(f"File not found: {path}")

    try:
        return file_path.read_text(encoding="utf-8")
    except PermissionError as e:
        print(f"Error: Permission denied: {path}", file=sys.stderr)
        raise
    except UnicodeDecodeError as e:
        print(f"Error: Invalid UTF-8 encoding: {path}", file=sys.stderr)
        raise

# Exit codes for scripts
def main() -> int:
    """Main entry point with proper exit codes."""
    try:
        content = load_file("example.txt")
        print(content)
        return 0  # Success
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1  # Failure
```

#### Command-Line Arguments

**Use `argparse` for all CLI scripts:**

```python
import argparse
from typing import Optional

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Sync documentation to GitHub Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/policy/new.md
  %(prog)s docs/guide/ --folder
  %(prog)s --project 8 --verbose docs/adr/
        """
    )

    parser.add_argument(
        "path",
        help="Path to file or folder to sync"
    )
    parser.add_argument(
        "--project",
        type=int,
        default=7,
        help="Project number (default: %(default)s)"
    )
    parser.add_argument(
        "--folder",
        action="store_true",
        help="Treat path as folder"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0"
    )

    return parser.parse_args()
```

### PowerShell Standards (Windows Support)

**PowerShell scripts are allowed for Windows-specific functionality** but must follow strict standards.

#### File Structure

```powershell
<#
.SYNOPSIS
    Brief one-line description.

.DESCRIPTION
    Detailed description of what this script does and why it exists.
    Multiple paragraphs are allowed.

.PARAMETER RepoPath
    Path to repository root directory.

.PARAMETER Verbose
    Enable verbose output.

.EXAMPLE
    .\Update-RepositoryMetadata.ps1 -RepoPath "C:\Projects\MyRepo"

    Updates metadata for repository at specified path.

.EXAMPLE
    .\Update-RepositoryMetadata.ps1 -RepoPath "C:\Projects\MyRepo" -Verbose

    Updates metadata with verbose output enabled.

.NOTES
    File Name      : Update-RepositoryMetadata.ps1
    Prerequisite   : PowerShell 5.1+
    Copyright      : 2026 Moko Consulting
    License        : GPL-3.0-or-later

.LINK
    https://github.com/mokoconsulting-tech/MokoStandards
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [ValidateScript({Test-Path $_})]
    [string]$RepoPath,

    [Parameter(Mandatory = $false)]
    [switch]$Verbose
)

# Strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Main logic here
```

#### PowerShell Naming Conventions

**Functions**: `Verb-Noun` (PascalCase)
```powershell
function Update-RepositoryMetadata { }
function Get-FileContent { }
function Test-ValidationRules { }
```

**Variables**: `$PascalCase`
```powershell
$RepoPath = "C:\Projects\MyRepo"
$FileCount = 0
$IsValid = $true
```

### File Headers (REQUIRED)

**All files MUST include proper copyright headers:**

#### Python Files

```python
#!/usr/bin/env python3
"""
Brief description.

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
along with this program (./LICENSE).

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Automation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/category/script_name.py
VERSION: 03.01.03
BRIEF: Brief description of purpose
"""
```

#### Markdown Files

```markdown
<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 [Full license text...]

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Documentation
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /path/to/file.md
 VERSION: 03.01.03
 BRIEF: Brief description
-->

# Document Title
```

### Code Quality Tools

**Run before committing:**

```bash
# Python syntax check (check all scripts)
find scripts -name "*.py" -type f -exec python -m py_compile {} +

# Type checking (if mypy configured)
mypy scripts/

# Linting (if configured)
find scripts -name "*.py" -type f | xargs pylint
find scripts -name "*.py" -type f | xargs flake8

# Format checking (if Black configured)
black --check scripts/
```

## Testing Guidelines

### Unit Tests (Required for Complex Logic)

**Location**: `scripts/tests/`

**Framework**: `unittest` or `pytest`

```python
# In scripts/tests/test_my_script.py
import unittest
from pathlib import Path
from scripts.automation.my_script import process_file, validate_path


class TestProcessFile(unittest.TestCase):
    """Test process_file function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_dir = Path("tests/fixtures")
        self.test_file = self.test_dir / "test.txt"

    def test_process_valid_file(self) -> None:
        """Test processing valid file."""
        result = process_file(str(self.test_file))
        self.assertTrue(result)

    def test_process_invalid_file(self) -> None:
        """Test processing non-existent file."""
        with self.assertRaises(FileNotFoundError):
            process_file("nonexistent.txt")

    def test_process_with_invalid_encoding(self) -> None:
        """Test processing file with invalid encoding."""
        invalid_file = self.test_dir / "invalid_encoding.txt"
        with self.assertRaises(UnicodeDecodeError):
            process_file(str(invalid_file))


if __name__ == "__main__":
    unittest.main()
```

### Manual Testing Checklist

Before submitting PR:

- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test with missing arguments
- [ ] Test `--help` output
- [ ] Test error messages are clear
- [ ] Test in clean environment (new terminal)
- [ ] Test on different platforms (if applicable)

### Running Tests

```bash
# Run all tests
python -m pytest scripts/tests/ -v

# Run specific test file
python -m pytest scripts/tests/test_my_script.py -v

# Run with coverage
python -m pytest scripts/tests/ --cov=scripts --cov-report=html

# Run single test function
python -m pytest scripts/tests/test_my_script.py::TestProcessFile::test_process_valid_file
```

## Pull Request Process

### 1. Before Creating PR

```bash
# Ensure branch is up to date
git fetch upstream
git rebase upstream/main

# Run validation
python scripts/validate/validate_file_headers.py .
python -m pytest scripts/tests/

# Commit changes
git add .
git commit -m "Add: Clear description of changes"
git push origin feature/your-feature
```

### 2. Creating the PR

**Use the Pull Request template:**

```markdown
## Description
Clear and concise description of changes.

## Related Issues
Fixes #123
Relates to #456

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing Performed
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing locally

## Checklist
- [ ] Code follows v2 standards (100% type hints, Google docstrings)
- [ ] File headers updated
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
- [ ] Self-review completed
```

### 3. PR Requirements

**All PRs must**:
- Pass automated CI/CD checks
- Include tests for new functionality
- Update documentation
- Follow code standards
- Have clear commit messages
- Reference related issues

### 4. Review Process

**Timeline**:
- Initial review: 2-3 business days
- Follow-up reviews: 1-2 business days
- Final approval: 1 business day

**Addressing Feedback**:
```bash
# Make requested changes
git add .
git commit -m "Fix: Address review feedback"
git push origin feature/your-feature

# If major changes, run tests again
python -m pytest scripts/tests/ -v
```

### 5. Merge Strategy

MokoStandards uses **squash merge** exclusively:

- PR title becomes commit message subject
- PR description becomes commit message body
- All commits squashed into single commit
- Branch automatically deleted after merge

**Make your PR title and description clear and descriptive!**

## Issue Guidelines

### Reporting Bugs

**Use the Bug Report template:**

```markdown
**Describe the bug**
Clear and concise description.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Run command '....'
3. See error

**Expected behavior**
What should happen.

**Actual behavior**
What actually happens.

**Environment**
- OS: [e.g., Ubuntu 22.04, Windows 11, macOS 14]
- Python version: [e.g., 3.9.7]
- MokoStandards version: [e.g., 2.0.0]

**Logs/Screenshots**
Attach relevant logs or screenshots (remove sensitive data).

**Additional context**
Any other relevant information.
```

### Requesting Features

**Use the Feature Request template:**

```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear and concise description of desired solution.

**Describe alternatives you've considered**
Alternative solutions or features considered.

**Use cases**
Describe how this feature would be used.

**Additional context**
Any other relevant information.
```

### Asking Questions

**Use GitHub Discussions** for:
- General questions
- Design discussions
- Usage help
- Community engagement

**Use GitHub Issues** for:
- Bug reports
- Feature requests
- Specific problems

## Code Review Process

### For Contributors

**Before requesting review**:
- [ ] Self-review completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code follows standards
- [ ] No debug code or comments

**During review**:
- Respond to feedback promptly
- Ask questions if unclear
- Make requested changes
- Push updates to same branch

### For Reviewers

**Review checklist**:
- [ ] Code follows v2 standards
- [ ] 100% type hints present
- [ ] Google docstrings complete
- [ ] File headers correct
- [ ] Tests adequate
- [ ] Documentation updated
- [ ] No security issues
- [ ] No hardcoded credentials
- [ ] Error handling proper
- [ ] Performance acceptable

**Providing feedback**:
- Be constructive and respectful
- Explain reasoning
- Suggest improvements
- Approve when ready

## Documentation Standards

### Documentation Files

**All documentation must**:
- Include proper file header
- Use clear, concise language
- Follow markdown conventions
- Include table of contents (if long)
- Have examples where appropriate
- Be spell-checked

### Markdown Style

```markdown
# H1 - Main Title (One per document)

## H2 - Major Sections

### H3 - Subsections

#### H4 - Minor Subsections

**Bold** for emphasis
*Italic* for subtle emphasis
`code` for inline code
```

### Code Examples

````markdown
```python
# Include language identifier
def example_function(param: str) -> bool:
    """Example with full type hints and docstring."""
    return True
```

```bash
# Shell commands
python script.py --help
```
````

### Links

```markdown
# Relative links to internal docs
[Contributing Guide](./CONTRIBUTING.md)
[Policy](docs/policy/scripting-standards.md)

# External links
[Python Documentation](https://docs.python.org/3/)
```

## Version Numbering

MokoStandards v2 uses **semantic versioning** with format: `vXX.YY.ZZ`

### Version Format

```
v03.05.12
  │  │  │
  │  │  └─ Patch (bug fixes, typos)
  │  └──── Minor (new features, non-breaking)
  └─────── Major (breaking changes)
```

### Examples

- `v03.00.00` - Major v2 release (breaking changes from v1)
- `v02.01.00` - Minor update (new features, backward compatible)
- `v02.01.01` - Patch release (bug fixes only)

### File Version Headers

In file headers, use format: `VERSION: 03.01.03` (no 'v' prefix)

```python
# FILE INFORMATION
VERSION: 03.01.03
```

### Changelog

All changes documented in [CHANGELOG.md](./CHANGELOG.md) following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [03.01.00] - 2026-01-20

### Added
- New validation script for workflows

### Changed
- Updated documentation structure

### Fixed
- Bug in file header validation
```

## Questions and Support

### Getting Help

**Documentation**:
- [README.md](./README.md) - Overview and quick start
- [docs/](./docs/) - Complete documentation
- [scripts/README.md](./scripts/README.md) - Scripts documentation

**Community**:
- [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions) - Q&A and discussions
- [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues) - Bug reports and features

**Contact**:
- General: hello@mokoconsulting.tech
- Security: security@mokoconsulting.tech

### Common Questions

**Q: Do I need to update all existing code to v2 standards?**
A: Only update code you're modifying. Don't refactor just for standards unless explicitly requested.

**Q: What if I can't add type hints to my function?**
A: Type hints are required. If truly impossible, document why in docstring and request exception from maintainers.

**Q: Can I use Shell/Bash scripts?**
A: No. All new scripts must be Python. Existing grandfathered scripts can remain but shouldn't be extended.

**Q: How do I run validation locally?**
A: `python scripts/validate/validate_file_headers.py .`

**Q: How long do PR reviews take?**
A: Initial review within 2-3 business days. Complex PRs may take longer.

**Q: Can I work on multiple issues in one PR?**
A: Prefer one issue per PR. Multiple related issues are acceptable if they're tightly coupled.

## License

By contributing to MokoStandards, you agree that your contributions will be licensed under the **GNU General Public License v3.0 or later** (GPL-3.0-or-later).

See [LICENSE](./LICENSE) for full license text.

---

## Metadata

- **Document**: CONTRIBUTING.md
- **Version**: 03.00.00
- **Last Updated**: 2026-01-19
- **Scope**: Contribution guidelines for v2.0
- **Audience**: Contributors, maintainers, community

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 03.00.00 | 2026-01-19 | GitHub Copilot | Complete v2.0 rebuild with Python/PowerShell standards, type hints, Google docstrings |
| 01.00.00 | 2025-12-17 | Moko Consulting | Initial contribution guidelines |

---

**Thank you for contributing to MokoStandards v2.0!**

Your contributions help maintain consistent, secure, and maintainable standards across the entire Moko Consulting ecosystem.
