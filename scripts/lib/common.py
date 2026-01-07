#!/usr/bin/env python3
# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/common.py
# VERSION: 04.01.00
# BRIEF: Common Python utilities for MokoStandards scripts
# PATH: /scripts/lib/common.py
# NOTE: Provides reusable functions for logging, error handling, and file operations

"""
Common Python Library for MokoStandards Scripts

Provides reusable utilities for:
- Standard file header generation
- Logging and output formatting
- Error handling and exit codes
- Path and file operations
- Repository introspection
"""

import os
import sys
from pathlib import Path
from typing import Optional, Set, Union


# ============================================================
# Constants
# ============================================================

VERSION = "04.01.00"
REPO_URL = "https://github.com/mokoconsulting-tech/MokoStandards"
COPYRIGHT = "Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>"
LICENSE = "GPL-3.0-or-later"

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INVALID_ARGS = 2
EXIT_NOT_FOUND = 3
EXIT_PERMISSION = 4


# ============================================================
# File Header Generation
# ============================================================

def generate_python_header(
    file_path: str,
    brief: str,
    defgroup: str = "MokoStandards.Scripts",
    ingroup: str = "MokoStandards",
    version: str = VERSION,
    note: Optional[str] = None
) -> str:
    """
    Generate a Moko Consulting standard file header for Python files.
    
    Args:
        file_path: Relative path from repository root (e.g., /scripts/lib/common.py)
        brief: Brief description of the file
        defgroup: Documentation group definition
        ingroup: Parent documentation group
        version: File version (default: repository version)
        note: Optional additional note
    
    Returns:
        String containing the complete file header
    """
    lines = [
        "#!/usr/bin/env python3",
        f"# {COPYRIGHT}",
        "#",
        "# This file is part of a Moko Consulting project.",
        "#",
        f"# SPDX-License-Identifier: {LICENSE}",
        "#",
        "# This program is free software; you can redistribute it and/or modify",
        "# it under the terms of the GNU General Public License as published by",
        "# the Free Software Foundation; either version 3 of the License, or",
        "# (at your option) any later version.",
        "#",
        "# This program is distributed in the hope that it will be useful,",
        "# but WITHOUT ANY WARRANTY; without even the implied warranty of",
        "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the",
        "# GNU General Public License for more details.",
        "#",
        "# You should have received a copy of the GNU General Public License",
        "# (./LICENSE).",
        "#",
        "# FILE INFORMATION",
        f"# DEFGROUP: {defgroup}",
        f"# INGROUP: {ingroup}",
        f"# REPO: {REPO_URL}",
        f"# FILE: {file_path.lstrip('/')}",
        f"# VERSION: {version}",
        f"# BRIEF: {brief}",
        f"# PATH: {file_path}",
    ]
    
    if note:
        lines.append(f"# NOTE: {note}")
    
    return "\n".join(lines) + "\n"


def generate_shell_header(
    file_path: str,
    brief: str,
    defgroup: str = "MokoStandards.Scripts",
    ingroup: str = "MokoStandards",
    version: str = VERSION,
    note: Optional[str] = None
) -> str:
    """
    Generate a Moko Consulting standard file header for shell scripts.
    
    Args:
        file_path: Relative path from repository root
        brief: Brief description of the file
        defgroup: Documentation group definition
        ingroup: Parent documentation group
        version: File version (default: repository version)
        note: Optional additional note
    
    Returns:
        String containing the complete file header
    """
    lines = [
        "#!/usr/bin/env bash",
        f"# {COPYRIGHT}",
        "#",
        "# This file is part of a Moko Consulting project.",
        "#",
        f"# SPDX-License-Identifier: {LICENSE}",
        "#",
        "# This program is free software; you can redistribute it and/or modify",
        "# it under the terms of the GNU General Public License as published by",
        "# the Free Software Foundation; either version 3 of the License, or",
        "# (at your option) any later version.",
        "#",
        "# This program is distributed in the hope that it will be useful,",
        "# but WITHOUT ANY WARRANTY; without even the implied warranty of",
        "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the",
        "# GNU General Public License for more details.",
        "#",
        "# You should have received a copy of the GNU General Public License",
        "# (./LICENSE).",
        "#",
        "# FILE INFORMATION",
        f"# DEFGROUP: {defgroup}",
        f"# INGROUP: {ingroup}",
        f"# REPO: {REPO_URL}",
        f"# FILE: {file_path.lstrip('/')}",
        f"# VERSION: {version}",
        f"# BRIEF: {brief}",
        f"# PATH: {file_path}",
    ]
    
    if note:
        lines.append(f"# NOTE: {note}")
    
    return "\n".join(lines) + "\n"


# ============================================================
# Logging and Output
# ============================================================

def log_info(message: str) -> None:
    """Print an info message to stdout."""
    print(f"ℹ️  {message}")


def log_success(message: str) -> None:
    """Print a success message to stdout."""
    print(f"✅ {message}")


def log_warning(message: str) -> None:
    """Print a warning message to stdout."""
    print(f"⚠️  {message}")


def log_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"❌ {message}", file=sys.stderr)


def log_debug(message: str, debug: Optional[bool] = None) -> None:
    """Print a debug message if debug mode is enabled.
    
    Args:
        message: Debug message to print
        debug: Override debug mode (default: check DEBUG environment variable)
    """
    if debug is None:
        debug = os.environ.get('DEBUG', '').lower() in ('1', 'true', 'yes')
    if debug:
        print(f"🔍 {message}", file=sys.stderr)


# ============================================================
# Error Handling
# ============================================================

def die(message: str, exit_code: int = EXIT_ERROR) -> None:
    """
    Print an error message and exit with the specified code.
    
    Args:
        message: Error message to display
        exit_code: Exit code (default: EXIT_ERROR)
    """
    log_error(message)
    sys.exit(exit_code)


def require_file(file_path: Union[str, Path], description: str = "File") -> Path:
    """
    Ensure a file exists, or exit with error.
    
    Args:
        file_path: Path to file
        description: Description for error message
    
    Returns:
        Path object for the file
    """
    path = Path(file_path)
    if not path.exists():
        die(f"{description} not found: {path}", EXIT_NOT_FOUND)
    if not path.is_file():
        die(f"{description} is not a file: {path}", EXIT_ERROR)
    return path


def require_dir(dir_path: Union[str, Path], description: str = "Directory") -> Path:
    """
    Ensure a directory exists, or exit with error.
    
    Args:
        dir_path: Path to directory
        description: Description for error message
    
    Returns:
        Path object for the directory
    """
    path = Path(dir_path)
    if not path.exists():
        die(f"{description} not found: {path}", EXIT_NOT_FOUND)
    if not path.is_dir():
        die(f"{description} is not a directory: {path}", EXIT_ERROR)
    return path


# ============================================================
# Repository Utilities
# ============================================================

def get_repo_root() -> Path:
    """
    Find the repository root by looking for .git directory.
    
    Returns:
        Path to repository root
    
    Raises:
        SystemExit if repository root cannot be found
    """
    current = Path.cwd().resolve()
    
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    
    die("Not in a git repository", EXIT_ERROR)


def get_relative_path(file_path: Union[str, Path], from_root: bool = True) -> str:
    """
    Get relative path from repository root or current directory.
    
    Args:
        file_path: Path to file
        from_root: If True, relative to repo root; if False, relative to cwd
    
    Returns:
        Relative path as string
    """
    path = Path(file_path).resolve()
    
    if from_root:
        root = get_repo_root()
        try:
            rel = path.relative_to(root)
            return f"/{rel}"
        except ValueError:
            return str(path)
    else:
        try:
            return str(path.relative_to(Path.cwd()))
        except ValueError:
            return str(path)


# ============================================================
# Path Utilities
# ============================================================

def ensure_dir(dir_path: Union[str, Path], description: str = "Directory") -> Path:
    """
    Ensure directory exists, creating it if necessary.
    
    Args:
        dir_path: Path to directory
        description: Description for logging
    
    Returns:
        Path object for the directory
    """
    path = Path(dir_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        log_info(f"Created {description}: {path}")
    return path


def is_excluded_path(path: Union[str, Path], exclusions: Set[str]) -> bool:
    """
    Check if a path matches any exclusion pattern.
    
    Args:
        path: Path to check
        exclusions: Set of directory/file names to exclude
    
    Returns:
        True if path should be excluded
    """
    path_obj = Path(path)
    
    # Check if any part of the path matches exclusions
    for part in path_obj.parts:
        if part in exclusions or part.startswith('.'):
            return True
    
    return False


# ============================================================
# Main (for testing)
# ============================================================

if __name__ == "__main__":
    print("MokoStandards Common Library v" + VERSION)
    print("=" * 70)
    
    # Test header generation
    print("\nPython Header Example:")
    print("-" * 70)
    print(generate_python_header(
        "/scripts/example.py",
        "Example Python script",
        note="This is a test"
    ))
    
    print("\nShell Header Example:")
    print("-" * 70)
    print(generate_shell_header(
        "/scripts/example.sh",
        "Example shell script",
        note="This is a test"
    ))
    
    # Test repository utilities
    print("\nRepository Info:")
    print("-" * 70)
    try:
        root = get_repo_root()
        print(f"Repository root: {root}")
        print(f"Current dir relative to root: {get_relative_path(Path.cwd())}")
    except SystemExit:
        print("Not in a git repository")
    
    print("\n✅ Common library loaded successfully")
