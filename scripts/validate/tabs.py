#!/usr/bin/env python3
"""
Detect TAB characters in files where spaces are required by language specification.

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
DEFGROUP: Script.Validate
INGROUP: Code.Quality
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/validate/tabs.py
VERSION: 03.01.05
BRIEF: Detect TAB characters in files where spaces are required
NOTE: Enforces MokoStandards indentation policy - tabs by default, spaces for specific languages
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Set

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


# File type mappings - languages that REQUIRE spaces (tabs will break them)
FILE_TYPE_EXTENSIONS = {
    'yaml': ['.yml', '.yaml'],
    'python': ['.py'],
    'haskell': ['.hs', '.lhs'],
    'fsharp': ['.fs', '.fsx', '.fsi'],
    'coffeescript': ['.coffee', '.litcoffee'],
    'nim': ['.nim', '.nims', '.nimble'],
    'json': ['.json'],
    'rst': ['.rst'],
}

# Language-specific reasons for requiring spaces
LANGUAGE_REASONS = {
    'yaml': 'YAML specification forbids tab characters',
    'python': 'PEP 8 standard requires spaces; tabs can cause IndentationError',
    'haskell': 'Haskell layout rules require spaces',
    'fsharp': 'F# indentation-sensitive syntax requires spaces',
    'coffeescript': 'CoffeeScript is whitespace-significant and requires spaces',
    'nim': 'Nim style guide requires spaces',
    'json': 'JSON spec and many parsers reject tabs',
    'rst': 'reStructuredText indentation rules require spaces',
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
        file_type: Type of files (yaml, python, shell, all)

    Returns:
        List of file extensions
    """
    if file_type == 'all':
        return list(get_all_extensions())
    return FILE_TYPE_EXTENSIONS.get(file_type, [])


def get_yaml_files() -> List[str]:
    """
    Get list of YAML files tracked by git.

    Returns:
        List of YAML file paths
    """
    try:
        returncode, stdout, stderr = common.run_command(
            ["git", "ls-files", "*.yml", "*.yaml"],
            capture_output=True,
            check=True
        )
        files = [f.strip() for f in stdout.split('\n') if f.strip()]
        return files
    except subprocess.CalledProcessError:
        return []


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


def check_tabs_in_file(filepath: str) -> List[Tuple[int, str]]:
    """
    Check for tab characters in a file.

    Args:
        filepath: Path to file to check

    Returns:
        List of (line_number, line_content) tuples with tabs
    """
    tabs_found = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if '\t' in line:
                    tabs_found.append((line_num, line.rstrip()))
    except Exception as e:
        common.log_warn(f"Could not read {filepath}: {e}")

    return tabs_found


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Detect TAB characters in files where spaces are required',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
MokoStandards Indentation Policy:
  - Default: Use tabs for most languages
  - Exception: Spaces required for languages where tabs break functionality
  
Languages requiring spaces (tabs forbidden):
  - YAML (.yml, .yaml) - Spec forbids tabs
  - Python (.py) - PEP 8 standard; tabs can cause IndentationError
  - Haskell (.hs, .lhs) - Layout rules require spaces
  - F# (.fs, .fsx, .fsi) - Indentation-sensitive syntax
  - CoffeeScript (.coffee) - Whitespace-significant language
  - Nim (.nim) - Style guide requirement
  - JSON (.json) - Parser compatibility
  - reStructuredText (.rst) - Indentation requirement

Examples:
  # Check all YAML files (default)
  python3 scripts/validate/tabs.py

  # Check Python files
  python3 scripts/validate/tabs.py --type python

  # Check all languages requiring spaces
  python3 scripts/validate/tabs.py --type all

  # Check specific extensions
  python3 scripts/validate/tabs.py --ext .yml --ext .py

  # Auto-fix detected tabs
  python3 scripts/validate/tabs.py --fix
        """
    )

    parser.add_argument(
        '--type',
        choices=['yaml', 'python', 'haskell', 'fsharp', 'coffeescript', 'nim', 'json', 'rst', 'all'],
        default='yaml',
        help='Type of files to check (default: yaml)'
    )
    parser.add_argument(
        '--ext',
        action='append',
        metavar='EXT',
        help='Specific file extensions to check (e.g., .yml, .py). Can be specified multiple times.'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix tabs by calling scripts/fix/tabs.py'
    )

    args = parser.parse_args()

    # If --fix is specified, call the fix script and exit
    if args.fix:
        fix_script = Path(__file__).parent.parent / "fix" / "tabs.py"
        cmd = [sys.executable, str(fix_script)]

        if args.type and args.type != 'yaml':
            cmd.extend(['--type', args.type])
        elif args.ext:
            for ext in args.ext:
                cmd.extend(['--ext', ext])

        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode
        except Exception as e:
            common.log_error(f"Failed to run fix script: {e}")
            return 1

    # Determine which files to check
    files_to_check = []

    if args.ext:
        # Specific extensions
        files_to_check = get_files_by_extensions(args.ext)
    else:
        # File type
        files_to_check = get_files_by_type(args.type)

    if not files_to_check:
        print("No files to check")
        return 0

    bad_files = []
    all_violations = {}

    for filepath in files_to_check:
        tabs = check_tabs_in_file(filepath)
        if tabs:
            bad_files.append(filepath)
            all_violations[filepath] = tabs

            print(f"TAB found in {filepath}", file=sys.stderr)
            print("  Lines with tabs:", file=sys.stderr)

            # Show first 5 lines with tabs
            for line_num, line_content in tabs[:5]:
                print(f"    {line_num}: {line_content[:80]}", file=sys.stderr)

            if len(tabs) > 5:
                print(f"    ... and {len(tabs) - 5} more", file=sys.stderr)
            print("", file=sys.stderr)

    if bad_files:
        print("", file=sys.stderr)
        print("ERROR: Tabs found in files that require spaces", file=sys.stderr)
        print("", file=sys.stderr)
        
        # Show language-specific reason if checking single type
        if args.type and args.type != 'all' and args.type in LANGUAGE_REASONS:
            print(f"Reason: {LANGUAGE_REASONS[args.type]}", file=sys.stderr)
            print("", file=sys.stderr)
        else:
            print("MokoStandards Policy: Tabs by default, spaces for specific languages", file=sys.stderr)
            print("Languages requiring spaces: YAML, Python, Haskell, F#, CoffeeScript, Nim, JSON, RST", file=sys.stderr)
            print("", file=sys.stderr)
        
        print(f"Found tabs in {len(bad_files)} file(s):", file=sys.stderr)
        for f in bad_files:
            print(f"  - {f}", file=sys.stderr)
        print("", file=sys.stderr)
        print("To fix:", file=sys.stderr)
        print("  1. Run: python3 scripts/validate/tabs.py --fix", file=sys.stderr)
        print("  2. Or run: python3 scripts/fix/tabs.py", file=sys.stderr)
        print("  3. Or manually replace tabs with spaces in your editor", file=sys.stderr)
        print("", file=sys.stderr)
        return 2

    print("tabs: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
