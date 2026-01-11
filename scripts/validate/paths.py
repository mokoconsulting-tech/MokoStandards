#!/usr/bin/env python3
"""
Detect Windows-style path separators (backslashes).

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
INGROUP: Path.Normalization
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/paths.py
VERSION: 01.00.00
BRIEF: Detect Windows-style path separators (backslashes)
NOTE: Ensures cross-platform path compatibility
"""

import mimetypes
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


def get_tracked_files() -> List[str]:
    """
    Get list of files tracked by git.
    
    Returns:
        List of file paths
    """
    try:
        result = common.run_command(
            ["git", "ls-files", "-z"],
            capture_output=True,
            check=True
        )
        files = [f for f in result.stdout.split('\0') if f.strip()]
        return files
    except subprocess.CalledProcessError:
        return []


def is_binary_file(filepath: str) -> bool:
    """
    Check if a file is likely binary.
    
    Args:
        filepath: Path to file
        
    Returns:
        True if likely binary
    """
    # Check mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type and mime_type.startswith(('application/', 'audio/', 'image/', 'video/')):
        return True
    
    # Check for null bytes (heuristic for binary files)
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                return True
    except Exception:
        return True
    
    return False


def find_backslashes_in_file(filepath: str) -> List[Tuple[int, str]]:
    """
    Find lines with backslashes in a file.
    
    Args:
        filepath: Path to file
        
    Returns:
        List of (line_number, line_content) tuples
    """
    backslashes = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if '\\' in line:
                    backslashes.append((line_num, line.rstrip()))
    except Exception as e:
        common.log_warn(f"Could not read {filepath}: {e}")
    
    return backslashes


def main() -> int:
    """Main entry point."""
    tracked_files = get_tracked_files()
    
    if not tracked_files:
        print("No files to check")
        return 0
    
    hits: Dict[str, List[Tuple[int, str]]] = {}
    
    for filepath in tracked_files:
        # Skip binary files
        if is_binary_file(filepath):
            continue
        
        # Find backslashes
        backslashes = find_backslashes_in_file(filepath)
        if backslashes:
            hits[filepath] = backslashes
    
    if hits:
        print("ERROR: Windows-style path literals detected", file=sys.stderr)
        print("", file=sys.stderr)
        print(f"Found backslashes in {len(hits)} file(s):", file=sys.stderr)
        
        for filepath, lines in hits.items():
            print("", file=sys.stderr)
            print(f"  File: {filepath}", file=sys.stderr)
            print("  Lines with backslashes:", file=sys.stderr)
            
            # Show first 5 lines
            for line_num, line_content in lines[:5]:
                print(f"    {line_num}: {line_content[:80]}", file=sys.stderr)
            
            if len(lines) > 5:
                print(f"    ... and {len(lines) - 5} more", file=sys.stderr)
        
        print("", file=sys.stderr)
        print("To fix:", file=sys.stderr)
        print("  1. Run: python3 scripts/fix/paths.py", file=sys.stderr)
        print("  2. Or manually replace backslashes (\\) with forward slashes (/)", file=sys.stderr)
        print("  3. Ensure paths use POSIX separators for cross-platform compatibility", file=sys.stderr)
        print("", file=sys.stderr)
        return 2
    
    print("paths: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
