#!/usr/bin/env python3
"""
Detect extension platform and type.

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
DEFGROUP: Script.Release
INGROUP: Extension.Detection
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/release/detect_platform.py
VERSION: 03.02.00
BRIEF: Detect extension platform and type for build workflow
USAGE: ./scripts/release/detect_platform.py [src_dir]
"""

import argparse
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import extension_utils
except ImportError:
    print("ERROR: Cannot import extension_utils library", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Detect extension platform and type",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "src_dir",
        nargs="?",
        default="src",
        help="Source directory (default: src)"
    )
    parser.add_argument(
        "--format",
        choices=["pipe", "json"],
        default="pipe",
        help="Output format (default: pipe)"
    )

    args = parser.parse_args()

    try:
        ext_info = extension_utils.get_extension_info(args.src_dir)

        if not ext_info:
            print(f"ERROR: No extension detected in {args.src_dir}", file=sys.stderr)
            return 1

        if args.format == "pipe":
            # Format: platform|ext_type
            print(f"{ext_info.platform.value}|{ext_info.extension_type}")
        elif args.format == "json":
            import json
            data = {
                "platform": ext_info.platform.value,
                "extension_type": ext_info.extension_type,
                "name": ext_info.name,
                "version": ext_info.version
            }
            print(json.dumps(data))

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
