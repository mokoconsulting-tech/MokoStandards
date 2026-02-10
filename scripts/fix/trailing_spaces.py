#!/usr/bin/env python3
"""
Remove trailing whitespace from files.

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
along with this program (./LICENSE.md).

FILE INFORMATION
DEFGROUP: Script.Fix
INGROUP: Code.Quality
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/fix/trailing_spaces.py
VERSION: 03.01.05
BRIEF: Remove trailing whitespace from files
NOTE: MokoStandards Policy - File formatting: Enforces organizational coding standards

MokoStandards Policy Compliance:
- File formatting: Enforces organizational coding standards
- Reference: docs/policy/file-formatting.md
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Optional

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


# File type mappings
FILE_TYPE_EXTENSIONS = {
    'yaml': ['.yml', '.yaml'],
    'python': ['.py'],
    'shell': ['.sh', '.bash'],
    'markdown': ['.md', '.markdown'],
}


def get_all_extensions() -> Set[str]:
    """
    Get all supported file extensions.

    Returns:
        Set of all file extensions
    """
    extensions = set()
    for exts in FILE_TYPE_EXTENSIONS.values():
        extensions.update(exts)
    return extensions


def get_extensions_for_type(file_type: str) -> List[str]:
    """
    Get file extensions for a given type.

    Args:
        file_type: Type of files (yaml, python, shell, markdown, all)

    Returns:
        List of file extensions
    """
    if file_type == 'all':
        return list(get_all_extensions())
    return FILE_TYPE_EXTENSIONS.get(file_type, [])


def get_files_by_type(file_type: str) -> List[str]:
    """
    Get list of files tracked by git for a given type.

    Args:
        file_type: Type of files to get

    Returns:
        List of file paths
    """
    extensions = get_extensions_for_type(file_type)
    if not extensions:
        return []

    try:
        patterns = [f"*{ext}" for ext in extensions]
        returncode, stdout, stderr = common.run_command(
            ["git", "ls-files"] + patterns,
            capture_output=True,
            check=True
        )
        files = [f.strip() for f in stdout.split('\n') if f.strip()]
        return files
    except subprocess.CalledProcessError:
        return []


def get_files_by_extensions(extensions: List[str]) -> List[str]:
    """
    Get list of files tracked by git for given extensions.

    Args:
        extensions: List of file extensions (e.g., ['.yml', '.py'])

    Returns:
        List of file paths
    """
    try:
        patterns = [f"*{ext}" for ext in extensions]
        returncode, stdout, stderr = common.run_command(
            ["git", "ls-files"] + patterns,
            capture_output=True,
            check=True
        )
        files = [f.strip() for f in stdout.split('\n') if f.strip()]
        return files
    except subprocess.CalledProcessError:
        return []


def fix_trailing_spaces(filepath: str, dry_run: bool = False, verbose: bool = True) -> bool:
    """
    Remove trailing whitespace from a file.

    Args:
        filepath: Path to file to fix
        dry_run: If True, only report what would be changed
        verbose: If True, print detailed information

    Returns:
        True if file was modified (or would be in dry-run), False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Remove trailing whitespace from each line
        modified = False
        new_lines = []
        for line in lines:
            # Keep line ending but strip trailing spaces/tabs
            line_ending = ''
            if line.endswith('\r\n'):
                line_ending = '\r\n'
                line = line[:-2]
            elif line.endswith('\n'):
                line_ending = '\n'
                line = line[:-1]

            stripped = line.rstrip()
            if line != stripped:
                modified = True
            new_lines.append(stripped + line_ending)

        if modified:
            if dry_run:
                if verbose:
                    print(f"Would fix: {filepath}")
            else:
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.writelines(new_lines)
                if verbose:
                    print(f"Fixed: {filepath}")
            return True
        else:
            if verbose:
                print(f"Already clean: {filepath}")
            return False

    except Exception as e:
        if verbose:
            common.log_warn(f"Could not process {filepath}: {e}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Remove trailing whitespace from files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix all YAML files
  python3 scripts/fix/trailing_spaces.py --type yaml

  # Fix specific extensions
  python3 scripts/fix/trailing_spaces.py --ext .yml --ext .py

  # Fix specific files
  python3 scripts/fix/trailing_spaces.py file1.yml file2.py

  # Dry run to see what would be changed
  python3 scripts/fix/trailing_spaces.py --type all --dry-run

  # Quiet mode
  python3 scripts/fix/trailing_spaces.py --type python --quiet
        """
    )

    parser.add_argument(
        '--type',
        choices=['yaml', 'python', 'shell', 'markdown', 'all'],
        help='Type of files to fix'
    )
    parser.add_argument(
        '--ext',
        action='append',
        metavar='EXT',
        help='Specific file extensions to fix (e.g., .yml, .py). Can be specified multiple times.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output (only show summary)'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific files to fix'
    )

    args = parser.parse_args()

    # Determine which files to process
    files_to_process = []

    if args.files:
        # Direct file arguments
        files_to_process = args.files
    elif args.ext:
        # Specific extensions
        files_to_process = get_files_by_extensions(args.ext)
    elif args.type:
        # File type
        files_to_process = get_files_by_type(args.type)
    else:
        # Default: all supported types
        files_to_process = get_files_by_type('all')

    if not files_to_process:
        if not args.quiet:
            print("No files to process")
        return 0

    verbose = not args.quiet

    if verbose:
        if args.dry_run:
            print(f"DRY RUN: Checking {len(files_to_process)} file(s)...")
        else:
            print(f"Fixing {len(files_to_process)} file(s)...")
        print()

    # Process files
    modified_count = 0
    for filepath in files_to_process:
        if fix_trailing_spaces(filepath, args.dry_run, verbose):
            modified_count += 1

    # Summary
    if verbose:
        print()

    if args.dry_run:
        print(f"Would modify {modified_count} file(s)")
    else:
        print(f"Modified {modified_count} file(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
