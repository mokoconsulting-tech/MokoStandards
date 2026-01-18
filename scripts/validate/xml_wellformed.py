#!/usr/bin/env python3
"""
Validate XML well-formedness.

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
DEFGROUP: Moko-Cassiopeia.Scripts
INGROUP: Scripts.Validate
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/xml_wellformed.py
VERSION: 01.00.00
BRIEF: Validate XML well-formedness in all XML files
"""

import argparse
import sys
try:
    from defusedxml import ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


def check_xml_file(file_path: Path) -> Tuple[bool, str]:
    """
    Check if an XML file is well-formed.

    Args:
        file_path: Path to XML file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        ET.parse(file_path)
        return (True, "")
    except ET.ParseError as e:
        return (False, str(e))
    except Exception as e:
        return (False, str(e))


def find_xml_files(src_dir: str, exclude_dirs: List[str] = None) -> List[Path]:
    """
    Find all XML files in a directory.

    Args:
        src_dir: Directory to search
        exclude_dirs: Directories to exclude

    Returns:
        List of XML file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ["vendor", "node_modules", ".git"]

    src_path = Path(src_dir)
    if not src_path.is_dir():
        return []

    xml_files = []
    for xml_file in src_path.rglob("*.xml"):
        # Check if file is in an excluded directory
        if any(excluded in xml_file.parts for excluded in exclude_dirs):
            continue
        xml_files.append(xml_file)

    return sorted(xml_files)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate XML well-formedness in all XML files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-s", "--src-dir",
        default="src",
        help="Source directory to search for XML files (default: src)"
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

    try:
        # Determine which files to check
        if args.files:
            xml_files = [Path(f) for f in args.files]
            for f in xml_files:
                if not f.is_file():
                    common.die(f"File not found: {f}")
        else:
            exclude_dirs = args.exclude or ["vendor", "node_modules", ".git"]
            xml_files = find_xml_files(args.src_dir, exclude_dirs)

        if not xml_files:
            common.die(f"No XML files found in {args.src_dir}")

        if args.verbose:
            common.log_section("XML Well-formedness Validation")
            common.log_info(f"Checking {len(xml_files)} XML file(s)")
            print()

        errors = []
        for xml_file in xml_files:
            is_valid, error_msg = check_xml_file(xml_file)

            if is_valid:
                if args.verbose:
                    common.log_success(f"OK: {xml_file}")
            else:
                errors.append((xml_file, error_msg))
                if args.verbose:
                    common.log_error(f"FAILED: {xml_file}")
                    if error_msg:
                        print(f"  {error_msg}")

        # Output results
        if args.verbose:
            print()

        if errors:
            result = {
                "status": "error",
                "src_dir": args.src_dir,
                "xml_count": len(xml_files),
                "passed": len(xml_files) - len(errors),
                "failed": len(errors),
                "errors": [{"file": str(f), "error": e} for f, e in errors]
            }

            if not args.verbose:
                common.json_output(result)

            common.log_error(f"XML validation failed: {len(errors)} error(s)")

            if not args.verbose:
                for file_path, error_msg in errors:
                    print(f"ERROR: {file_path}")
                    if error_msg:
                        print(f"  {error_msg}")

            return 1
        else:
            result = {
                "status": "ok",
                "src_dir": args.src_dir,
                "xml_count": len(xml_files)
            }

            if not args.verbose:
                common.json_output(result)
                print(f"xml_wellformed: ok")
            else:
                common.log_success(f"All {len(xml_files)} XML file(s) are well-formed")

            return 0

    except Exception as e:
        common.log_error(f"Validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
