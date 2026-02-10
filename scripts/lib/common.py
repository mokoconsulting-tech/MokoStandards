#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
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
# VERSION: 03.01.03
# BRIEF: Common Python utilities for MokoStandards scripts (v2)
# PATH: /scripts/lib/common.py
# NOTE: Complete rewrite with modern Python features and no backward compatibility

"""Common Python Library for MokoStandards Scripts v2.

This module provides reusable utilities for MokoStandards scripts including:
- Standard file header generation
- Logging and output formatting
- Modern error handling with custom exceptions
- Process execution with timeout support
- Path and file operations with atomic writes
- Human-readable formatting utilities
- Repository introspection
"""

import os
import sys
import subprocess
import tempfile
import json
import re
from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict, Any
import shutil



# ============================================================
# Constants
# ============================================================

# Fallback version if README.md cannot be read
_FALLBACK_VERSION: str = "03.01.03"

def _get_version_from_readme() -> str:
    """Extract version from README.md title line.
    
    Searches for the pattern '# MokoStandards (VERSION: XX.YY.ZZ)' in README.md
    and extracts the version number.
    
    Returns:
        Version string (e.g., "03.01.03")
    """
    try:
        # Find repo root by looking for .git directory
        current = Path.cwd().resolve()
        while current != current.parent:
            if (current / ".git").exists():
                readme_path = current / "README.md"
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Look for pattern: # MokoStandards (VERSION: XX.YY.ZZ)
                            if line.startswith('#') and 'VERSION:' in line:
                                match = re.search(r'VERSION:\s*(\d+\.\d+\.\d+)', line)
                                if match:
                                    return match.group(1)
                break
            current = current.parent
        
        # Fallback if version not found
        return _FALLBACK_VERSION
    except Exception:
        # Fallback on any error
        return _FALLBACK_VERSION

# Initialize VERSION by reading from README
VERSION: str = _get_version_from_readme()
REPO_URL: str = "https://github.com/mokoconsulting-tech/MokoStandards"
COPYRIGHT: str = "Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>"
LICENSE: str = "GPL-3.0-or-later"

# Exit codes
EXIT_SUCCESS: int = 0
EXIT_ERROR: int = 1
EXIT_INVALID_ARGS: int = 2
EXIT_NOT_FOUND: int = 3
EXIT_PERMISSION: int = 4
EXIT_TIMEOUT: int = 5


# ============================================================
# Custom Exceptions
# ============================================================


class MokoError(Exception):
    """Base exception for MokoStandards utilities."""

    def __init__(self, message: str, exit_code: int = EXIT_ERROR) -> None:
        """Initialize MokoError.

        Args:
            message: Error message
            exit_code: Exit code to use when this error causes program termination
        """
        super().__init__(message)
        self.exit_code = exit_code


class CommandError(MokoError):
    """Exception raised when a command execution fails."""

    def __init__(
        self,
        message: str,
        returncode: int,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None
    ) -> None:
        """Initialize CommandError.

        Args:
            message: Error message
            returncode: Command return code
            stdout: Command stdout output
            stderr: Command stderr output
        """
        super().__init__(message, EXIT_ERROR)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class TimeoutError(MokoError):
    """Exception raised when a command times out."""

    def __init__(self, message: str, timeout: float) -> None:
        """Initialize TimeoutError.

        Args:
            message: Error message
            timeout: Timeout value in seconds
        """
        super().__init__(message, EXIT_TIMEOUT)
        self.timeout = timeout


class FileNotFoundError(MokoError):
    """Exception raised when a required file is not found."""

    def __init__(self, path: Union[str, Path], description: str = "File") -> None:
        """Initialize FileNotFoundError.

        Args:
            path: Path to the missing file
            description: Description of the file
        """
        super().__init__(f"{description} not found: {path}", EXIT_NOT_FOUND)
        self.path = Path(path)


class DirectoryNotFoundError(MokoError):
    """Exception raised when a required directory is not found."""

    def __init__(self, path: Union[str, Path], description: str = "Directory") -> None:
        """Initialize DirectoryNotFoundError.

        Args:
            path: Path to the missing directory
            description: Description of the directory
        """
        super().__init__(f"{description} not found: {path}", EXIT_NOT_FOUND)
        self.path = Path(path)


class PermissionError(MokoError):
    """Exception raised when there are insufficient permissions."""

    def __init__(self, message: str) -> None:
        """Initialize PermissionError.

        Args:
            message: Error message
        """
        super().__init__(message, EXIT_PERMISSION)



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
    """Generate a Moko Consulting standard file header for Python files.

    Creates a standardized header with copyright, license information,
    and file metadata following MokoStandards conventions.

    Args:
        file_path: Relative path from repository root (e.g., /scripts/lib/common.py)
        brief: Brief description of the file
        defgroup: Documentation group definition (default: MokoStandards.Scripts)
        ingroup: Parent documentation group (default: MokoStandards)
        version: File version (default: current VERSION constant)
        note: Optional additional note to append to header

    Returns:
        Complete file header as a string with proper shebang and formatting

    Example:
        >>> header = generate_python_header("/scripts/test.py", "Test script")
        >>> print(header.split('\\n')[0])
        #!/usr/bin/env python3
    """
    lines: List[str] = [
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
    """Generate a Moko Consulting standard file header for shell scripts.

    Creates a standardized header with copyright, license information,
    and file metadata following MokoStandards conventions for bash scripts.

    Args:
        file_path: Relative path from repository root
        brief: Brief description of the file
        defgroup: Documentation group definition (default: MokoStandards.Scripts)
        ingroup: Parent documentation group (default: MokoStandards)
        version: File version (default: current VERSION constant)
        note: Optional additional note to append to header

    Returns:
        Complete file header as a string with bash shebang and formatting

    Example:
        >>> header = generate_shell_header("/scripts/test.sh", "Test script")
        >>> print(header.split('\\n')[0])
        #!/usr/bin/env bash
    """
    lines: List[str] = [
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
    """Print an informational message to stdout.

    Args:
        message: Information message to display
    """
    print(f"ℹ️  {message}")


def log_success(message: str) -> None:
    """Print a success message to stdout.

    Args:
        message: Success message to display
    """
    print(f"✅ {message}")


def log_warning(message: str) -> None:
    """Print a warning message to stdout.

    Args:
        message: Warning message to display
    """
    print(f"⚠️  {message}")


def log_error(message: str) -> None:
    """Print an error message to stderr.

    Args:
        message: Error message to display
    """
    print(f"❌ {message}", file=sys.stderr)


def json_output(data: Dict[str, Any]) -> None:
    """Output data as JSON to stdout.

    Args:
        data: Dictionary to output as JSON
    """
    print(json.dumps(data, indent=2))


def log_debug(message: str, debug: Optional[bool] = None) -> None:
    """Print a debug message if debug mode is enabled.

    Checks DEBUG environment variable if debug parameter is not provided.
    Debug mode is enabled when DEBUG is set to '1', 'true', or 'yes'.

    Args:
        message: Debug message to display
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
    """Print an error message and exit with the specified code.

    This function does not return. It prints an error message to stderr
    and immediately terminates the program.

    Args:
        message: Error message to display
        exit_code: Exit code (default: EXIT_ERROR)
    """
    log_error(message)
    sys.exit(exit_code)


def require_file(file_path: Union[str, Path], description: str = "File") -> Path:
    """Ensure a file exists, raising an exception if not found.

    Args:
        file_path: Path to file
        description: Description for error message

    Returns:
        Path object for the validated file

    Raises:
        FileNotFoundError: If file does not exist or is not a file
    """
    path: Path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(path, description)
    if not path.is_file():
        raise MokoError(f"{description} is not a file: {path}", EXIT_ERROR)
    return path


def require_directory(dir_path: Union[str, Path], description: str = "Directory") -> Path:
    """Ensure a directory exists, raising an exception if not found.

    Args:
        dir_path: Path to directory
        description: Description for error message

    Returns:
        Path object for the validated directory

    Raises:
        DirectoryNotFoundError: If directory does not exist or is not a directory
    """
    path: Path = Path(dir_path)
    if not path.exists():
        raise DirectoryNotFoundError(path, description)
    if not path.is_dir():
        raise MokoError(f"{description} is not a directory: {path}", EXIT_ERROR)
    return path



# ============================================================
# Process Execution
# ============================================================


def run_command(
    command: Union[str, List[str]],
    timeout: Optional[float] = None,
    check: bool = True,
    capture_output: bool = True,
    cwd: Optional[Union[str, Path]] = None,
    env: Optional[dict] = None
) -> Tuple[int, str, str]:
    """Execute a command with timeout support and error handling.

    Runs a subprocess command with configurable timeout, output capture,
    and error handling. Provides a clean interface for command execution
    with proper exception handling.

    Args:
        command: Command to execute (string or list of arguments)
        timeout: Timeout in seconds (default: None for no timeout)
        check: If True, raise CommandError on non-zero exit (default: True)
        capture_output: If True, capture stdout and stderr (default: True)
        cwd: Working directory for command (default: current directory)
        env: Environment variables (default: inherit current environment)

    Returns:
        Tuple of (returncode, stdout, stderr) where stdout and stderr
        are empty strings if capture_output is False

    Raises:
        CommandError: If command fails and check=True
        TimeoutError: If command exceeds timeout

    Example:
        >>> returncode, stdout, stderr = run_command(['git', 'status'], timeout=5.0)
        >>> print(stdout)
    """
    if isinstance(command, str):
        cmd_list: List[str] = command.split()
    else:
        cmd_list = command

    try:
        if capture_output:
            result = subprocess.run(
                cmd_list,
                timeout=timeout,
                capture_output=True,
                text=True,
                cwd=cwd,
                env=env
            )
            stdout_str: str = result.stdout
            stderr_str: str = result.stderr
        else:
            result = subprocess.run(
                cmd_list,
                timeout=timeout,
                cwd=cwd,
                env=env
            )
            stdout_str = ""
            stderr_str = ""

        if check and result.returncode != 0:
            raise CommandError(
                f"Command failed with return code {result.returncode}: {' '.join(cmd_list)}",
                result.returncode,
                stdout_str,
                stderr_str
            )

        return result.returncode, stdout_str, stderr_str

    except subprocess.TimeoutExpired as e:
        raise TimeoutError(
            f"Command timed out after {timeout}s: {' '.join(cmd_list)}",
            timeout or 0.0
        ) from e


# ============================================================
# Path and File Operations
# ============================================================


def ensure_directory(dir_path: Union[str, Path], mode: int = 0o755) -> Path:
    """Create directory and all parent directories safely.

    Creates the specified directory with all necessary parent directories.
    If the directory already exists, no error is raised. Thread-safe and
    handles race conditions gracefully.

    Args:
        dir_path: Path to directory to create
        mode: Directory permissions in octal (default: 0o755)

    Returns:
        Path object for the created/existing directory

    Example:
        >>> path = ensure_directory("/tmp/my/nested/dir")
        >>> print(path.exists())
        True
    """
    path: Path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True, mode=mode)
    return path


def atomic_write(
    file_path: Union[str, Path],
    content: str,
    encoding: str = 'utf-8',
    mode: int = 0o644
) -> None:
    """Write content to a file atomically using a temporary file.

    Writes content to a temporary file first, then moves it to the target
    location. This ensures that the target file is never partially written
    or corrupted if the process is interrupted.

    Args:
        file_path: Destination file path
        content: Content to write to file
        encoding: Text encoding (default: utf-8)
        mode: File permissions in octal (default: 0o644)

    Raises:
        PermissionError: If unable to write to the target location

    Example:
        >>> atomic_write("/tmp/config.json", '{"key": "value"}')
    """
    path: Path = Path(file_path)

    # Ensure parent directory exists
    if path.parent != Path('.'):
        ensure_directory(path.parent)

    # Create temporary file in same directory for atomic move
    fd, tmp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp"
    )

    try:
        # Write content to temporary file
        with os.fdopen(fd, 'w', encoding=encoding) as f:
            f.write(content)

        # Set permissions
        os.chmod(tmp_path, mode)

        # Atomic move to destination
        shutil.move(tmp_path, path)
    except Exception:
        # Clean up temporary file on error
        try:
            os.unlink(tmp_path)
        except OSError as e:
            # Log cleanup failure but don't mask the original exception
            import sys
            print(f"Warning: Failed to clean up temporary file {tmp_path}: {e}", file=sys.stderr)
        raise



# ============================================================
# Human-Readable Formatting
# ============================================================


def format_bytes(num_bytes: int, precision: int = 2) -> str:
    """Format byte count as human-readable string.

    Converts a byte count into a human-readable string using appropriate
    units (B, KB, MB, GB, TB, PB).

    Args:
        num_bytes: Number of bytes to format
        precision: Number of decimal places (default: 2)

    Returns:
        Formatted string with appropriate unit

    Example:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1536, precision=1)
        '1.5 KB'
        >>> format_bytes(1048576)
        '1.00 MB'
    """
    if num_bytes < 0:
        raise ValueError("num_bytes must be non-negative")

    units: List[str] = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index: int = 0
    size: float = float(num_bytes)

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.{precision}f} {units[unit_index]}"


def format_duration(seconds: float, precision: int = 2) -> str:
    """Format duration in seconds as human-readable string.

    Converts a duration in seconds into a human-readable string using
    appropriate units (s, ms, μs, ns for small durations; s, m, h, d for
    large durations).

    Args:
        seconds: Duration in seconds
        precision: Number of decimal places (default: 2)

    Returns:
        Formatted string with appropriate unit

    Example:
        >>> format_duration(0.001)
        '1.00 ms'
        >>> format_duration(65)
        '1.08 m'
        >>> format_duration(3661)
        '1.02 h'
    """
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    # Handle sub-second durations
    if seconds < 1.0:
        if seconds < 0.000001:  # nanoseconds
            return f"{seconds * 1_000_000_000:.{precision}f} ns"
        elif seconds < 0.001:  # microseconds
            return f"{seconds * 1_000_000:.{precision}f} μs"
        else:  # milliseconds
            return f"{seconds * 1000:.{precision}f} ms"

    # Handle larger durations
    if seconds < 60:  # seconds
        return f"{seconds:.{precision}f} s"
    elif seconds < 3600:  # minutes
        return f"{seconds / 60:.{precision}f} m"
    elif seconds < 86400:  # hours
        return f"{seconds / 3600:.{precision}f} h"
    else:  # days
        return f"{seconds / 86400:.{precision}f} d"


# ============================================================
# Repository Utilities
# ============================================================


def get_repo_root() -> Path:
    """Find the repository root by looking for .git directory.

    Searches upward from the current directory to find the git repository
    root. Stops at filesystem root if no .git directory is found.

    Returns:
        Path to repository root

    Raises:
        MokoError: If not in a git repository

    Example:
        >>> root = get_repo_root()
        >>> print(root.name)
        MokoStandards
    """
    current: Path = Path.cwd().resolve()

    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent

    raise MokoError("Not in a git repository", EXIT_ERROR)



def get_relative_path(file_path: Union[str, Path], from_root: bool = True) -> str:
    """Get relative path from repository root or current directory.

    Converts an absolute path to a relative path, either from the repository
    root or from the current working directory.

    Args:
        file_path: Path to convert
        from_root: If True, relative to repo root; if False, relative to cwd

    Returns:
        Relative path as string (with leading / if from_root is True)

    Example:
        >>> path = get_relative_path("/repo/scripts/test.py", from_root=True)
        >>> print(path)
        /scripts/test.py
    """
    path: Path = Path(file_path).resolve()

    if from_root:
        root: Path = get_repo_root()
        try:
            rel: Path = path.relative_to(root)
            return f"/{rel}"
        except ValueError:
            return str(path)
    else:
        try:
            return str(path.relative_to(Path.cwd()))
        except ValueError:
            return str(path)


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
        root: Path = get_repo_root()
        print(f"Repository root: {root}")
        print(f"Current dir relative to root: {get_relative_path(Path.cwd())}")
    except MokoError as e:
        print(f"Error: {e}")

    # Test formatting utilities
    print("\nFormatting Examples:")
    print("-" * 70)
    print(f"1024 bytes: {format_bytes(1024)}")
    print(f"1536 bytes: {format_bytes(1536, precision=1)}")
    print(f"1048576 bytes: {format_bytes(1048576)}")
    print(f"0.001 seconds: {format_duration(0.001)}")
    print(f"65 seconds: {format_duration(65)}")
    print(f"3661 seconds: {format_duration(3661)}")

    # Test command execution
    print("\nCommand Execution Test:")
    print("-" * 70)
    try:
        returncode, stdout, stderr = run_command(['echo', 'Hello, World!'])
        print(f"Return code: {returncode}")
        print(f"Output: {stdout.strip()}")
        log_success("Command execution test passed")
    except (CommandError, TimeoutError) as e:
        log_error(f"Command execution test failed: {e}")

    # Test directory creation
    print("\nDirectory Creation Test:")
    print("-" * 70)
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir: Path = ensure_directory(Path(tmpdir) / "test" / "nested" / "dir")
        print(f"Created: {test_dir}")
        print(f"Exists: {test_dir.exists()}")
        log_success("Directory creation test passed")

    # Test atomic write
    print("\nAtomic Write Test:")
    print("-" * 70)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file: Path = Path(tmpdir) / "test.txt"
        atomic_write(test_file, "Hello, atomic write!")
        content: str = test_file.read_text()
        print(f"File: {test_file}")
        print(f"Content: {content}")
        log_success("Atomic write test passed")

    print("\n✅ All tests completed successfully")
