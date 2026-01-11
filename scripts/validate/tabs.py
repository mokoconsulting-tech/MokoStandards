#!/usr/bin/env python3
"""
Detect TAB characters in YAML files where they are not allowed.

Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/tabs.py
VERSION: 01.00.00
BRIEF: Detect TAB characters in YAML files where they are not allowed
NOTE: YAML specification forbids tab characters
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


def get_yaml_files() -> List[str]:
    """
    Get list of YAML files tracked by git.
    
    Returns:
        List of YAML file paths
    """
    try:
        result = common.run_command(
            ["git", "ls-files", "*.yml", "*.yaml"],
            capture_output=True,
            check=True
        )
        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
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
    yaml_files = get_yaml_files()
    
    if not yaml_files:
        print("No files to check")
        return 0
    
    bad_files = []
    all_violations = {}
    
    for filepath in yaml_files:
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
        print("ERROR: Tabs found in repository files", file=sys.stderr)
        print("", file=sys.stderr)
        print("YAML specification forbids tab characters.", file=sys.stderr)
        print(f"Found tabs in {len(bad_files)} file(s):", file=sys.stderr)
        for f in bad_files:
            print(f"  - {f}", file=sys.stderr)
        print("", file=sys.stderr)
        print("To fix:", file=sys.stderr)
        print("  1. Run: python3 scripts/fix/tabs.py", file=sys.stderr)
        print("  2. Or manually replace tabs with spaces in your editor", file=sys.stderr)
        print("  3. Configure your editor to use spaces (not tabs) for YAML files", file=sys.stderr)
        print("", file=sys.stderr)
        return 2
    
    print("tabs: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
