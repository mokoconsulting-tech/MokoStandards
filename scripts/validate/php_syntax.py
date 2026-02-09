#!/usr/bin/env python3
"""
Validate PHP syntax in files.

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
DEFGROUP: Moko-Cassiopeia.Scripts
INGROUP: Scripts.Validate
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/php_syntax.py
VERSION: 03.01.02
BRIEF: Validate PHP syntax in all PHP files
"""

import argparse
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


def check_php_file(file_path: Path) -> Tuple[bool, str]:
    """
    Check PHP syntax of a single file.

    Args:
        file_path: Path to PHP file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        result = subprocess.run(
            ["php", "-l", str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return (True, "")
        else:
            return (False, result.stderr or result.stdout)

    except subprocess.TimeoutExpired:
        return (False, "Syntax check timed out")
    except Exception as e:
        return (False, str(e))


def find_php_files(src_dir: str, exclude_dirs: List[str] = None) -> List[Path]:
    """
    Find all PHP files in a directory.

    Args:
        src_dir: Directory to search
        exclude_dirs: Directories to exclude

    Returns:
        List of PHP file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ["vendor", "node_modules", ".git"]

    src_path = Path(src_dir)
    if not src_path.is_dir():
        return []

    php_files = []
    for php_file in src_path.rglob("*.php"):
        # Check if file is in an excluded directory
        if any(excluded in php_file.parts for excluded in exclude_dirs):
            continue
        php_files.append(php_file)

    return sorted(php_files)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate PHP syntax in all PHP files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-s", "--src-dir",
        default="src",
        help="Source directory to search for PHP files (default: src)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Directories to exclude (can be specified multiple times)"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to check (optional)"
    )

    args = parser.parse_args()

    # Check if PHP is available
    common.require_cmd("php")

    try:
        # Determine which files to check
        if args.files:
            php_files = [Path(f) for f in args.files]
            for f in php_files:
                if not f.is_file():
                    common.die(f"File not found: {f}")
        else:
            exclude_dirs = args.exclude or ["vendor", "node_modules", ".git"]
            php_files = find_php_files(args.src_dir, exclude_dirs)

        if not php_files:
            common.die(f"No PHP files found in {args.src_dir}")

        if args.verbose:
            common.log_section("PHP Syntax Validation")
            common.log_info(f"Checking {len(php_files)} PHP file(s)")
            print()

        errors = []
        for php_file in php_files:
            is_valid, error_msg = check_php_file(php_file)

            if is_valid:
                if args.verbose:
                    common.log_success(f"OK: {php_file}")
            else:
                errors.append((php_file, error_msg))
                if args.verbose:
                    common.log_error(f"FAILED: {php_file}")
                    if error_msg:
                        print(f"  {error_msg}")

        # Output results
        if args.verbose:
            print()

        if errors:
            result = {
                "status": "error",
                "total": len(php_files),
                "passed": len(php_files) - len(errors),
                "failed": len(errors),
                "errors": [{"file": str(f), "error": e} for f, e in errors]
            }

            if not args.verbose:
                common.json_output(result)

            common.log_error(f"PHP syntax check failed: {len(errors)} error(s)")

            if not args.verbose:
                for file_path, error_msg in errors:
                    print(f"ERROR: {file_path}")
                    if error_msg:
                        print(f"  {error_msg}")

            return 1
        else:
            result = {
                "status": "ok",
                "total": len(php_files),
                "passed": len(php_files)
            }

            if not args.verbose:
                common.json_output(result)
                print(f"php_syntax: ok ({len(php_files)} file(s) checked)")
            else:
                common.log_success(f"All {len(php_files)} PHP file(s) are valid")

            return 0

    except Exception as e:
        common.log_error(f"Validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
