#!/usr/bin/env python3
"""
Convert tabs to spaces in files.

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
PATH: /scripts/fix/tabs.py
VERSION: 03.01.02
BRIEF: Convert tabs to spaces in files where spaces are required
NOTE: MokoStandards Policy - Enforces indentation standards for specific languages

MokoStandards Policy Compliance:
- File formatting: Enforces organizational coding standards
- Reference: docs/policy/coding-style-guide.md
- Languages requiring spaces: YAML, Python, Haskell, F#, CoffeeScript, Nim, JSON, RST
- Makefiles: tabs preserved (required by Make syntax)
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


# File type mappings and tab conversion rules
FILE_TYPE_RULES = {
    'yaml': {
        'extensions': ['.yml', '.yaml'],
        'spaces': 2,
        'convert': True
    },
    'python': {
        'extensions': ['.py'],
        'spaces': 4,
        'convert': True
    },
    'haskell': {
        'extensions': ['.hs', '.lhs'],
        'spaces': 2,
        'convert': True
    },
    'fsharp': {
        'extensions': ['.fs', '.fsx', '.fsi'],
        'spaces': 4,
        'convert': True
    },
    'coffeescript': {
        'extensions': ['.coffee', '.litcoffee'],
        'spaces': 2,
        'convert': True
    },
    'nim': {
        'extensions': ['.nim', '.nims', '.nimble'],
        'spaces': 2,
        'convert': True
    },
    'json': {
        'extensions': ['.json'],
        'spaces': 2,
        'convert': True
    },
    'rst': {
        'extensions': ['.rst'],
        'spaces': 3,
        'convert': True
    },
    'makefile': {
        'extensions': [],  # Special case: handled by filename
        'spaces': 0,
        'convert': False  # Don't convert tabs in Makefiles
    }
}


def get_all_extensions() -> Set[str]:
    """
    Get all supported file extensions (excluding makefiles).

    Returns:
        Set of all file extensions
    """
    extensions = set()
    for file_type, rules in FILE_TYPE_RULES.items():
        if rules['convert']:  # Only convertible types
            extensions.update(rules['extensions'])
    return extensions


def get_extensions_for_type(file_type: str) -> List[str]:
    """
    Get file extensions for a given type.

    Args:
        file_type: Type of files (yaml, python, shell, all)

    Returns:
        List of file extensions
    """
    if file_type == 'all':
        return list(get_all_extensions())

    rules = FILE_TYPE_RULES.get(file_type)
    if rules and rules['convert']:
        return rules['extensions']
    return []


def is_makefile(filepath: str) -> bool:
    """
    Check if file is a Makefile.

    Args:
        filepath: Path to file

    Returns:
        True if file is a Makefile
    """
    filename = Path(filepath).name.lower()
    return filename in ['makefile', 'gnumakefile'] or filename.startswith('makefile.')


def get_tab_settings(filepath: str) -> tuple:
    """
    Get tab conversion settings for a file.

    Args:
        filepath: Path to file

    Returns:
        Tuple of (should_convert, num_spaces)
    """
    # Check if it's a Makefile
    if is_makefile(filepath):
        return (False, 0)

    # Check by extension
    ext = Path(filepath).suffix.lower()

    for file_type, rules in FILE_TYPE_RULES.items():
        if ext in rules['extensions']:
            return (rules['convert'], rules['spaces'])

    # Default: convert tabs to 4 spaces
    return (True, 4)


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


def fix_tabs(filepath: str, dry_run: bool = False, verbose: bool = True) -> bool:
    """
    Convert tabs to spaces in a file.

    Args:
        filepath: Path to file to fix
        dry_run: If True, only report what would be changed
        verbose: If True, print detailed information

    Returns:
        True if file was modified (or would be in dry-run), False otherwise
    """
    # Get conversion settings
    should_convert, num_spaces = get_tab_settings(filepath)

    if not should_convert:
        if verbose:
            print(f"Skipped (Makefile): {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check if file contains tabs
        if '\t' not in content:
            if verbose:
                print(f"Already clean: {filepath}")
            return False

        # Replace tabs with spaces
        spaces = ' ' * num_spaces
        new_content = content.replace('\t', spaces)

        if dry_run:
            if verbose:
                tab_count = content.count('\t')
                print(f"Would fix: {filepath} ({tab_count} tabs → {num_spaces} spaces)")
        else:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(new_content)
            if verbose:
                tab_count = content.count('\t')
                print(f"Fixed: {filepath} ({tab_count} tabs → {num_spaces} spaces)")

        return True

    except Exception as e:
        if verbose:
            common.log_warn(f"Could not process {filepath}: {e}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert tabs to spaces in files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix all YAML files (tabs → 2 spaces)
  python3 scripts/fix/tabs.py --type yaml

  # Fix all Python files (tabs → 4 spaces)
  python3 scripts/fix/tabs.py --type python

  # Fix specific extensions
  python3 scripts/fix/tabs.py --ext .yml --ext .py

  # Fix specific files
  python3 scripts/fix/tabs.py file1.yml file2.py

  # Dry run to see what would be changed
  python3 scripts/fix/tabs.py --type all --dry-run

  # Quiet mode
  python3 scripts/fix/tabs.py --type python --quiet

Note: Makefiles are automatically detected and tabs are preserved.
        """
    )

    parser.add_argument(
        '--type',
        choices=['yaml', 'python', 'haskell', 'fsharp', 'coffeescript', 'nim', 'json', 'rst', 'all'],
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
        if fix_tabs(filepath, args.dry_run, verbose):
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
