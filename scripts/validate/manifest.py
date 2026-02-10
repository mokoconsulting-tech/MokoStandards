#!/usr/bin/env python3
"""
Validate Joomla manifest files.

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
PATH: /scripts/validate/manifest.py
VERSION: 03.01.03
BRIEF: Validate Joomla extension manifest files
"""

import argparse
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
    import joomla_manifest
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


def validate_manifest_file(manifest_path: Path, verbose: bool = False) -> bool:
    """
    Validate a single manifest file.

    Args:
        manifest_path: Path to manifest file
        verbose: Show detailed output

    Returns:
        True if valid, False otherwise
    """
    try:
        info = joomla_manifest.parse_manifest(manifest_path)
        is_valid, warnings = joomla_manifest.validate_manifest(manifest_path)

        if verbose:
            common.log_section(f"Manifest: {manifest_path}")
            common.log_kv("Type", info.extension_type)
            common.log_kv("Name", info.name)
            common.log_kv("Version", info.version)

            if warnings:
                common.log_warn(f"Warnings ({len(warnings)}):")
                for warning in warnings:
                    print(f"  - {warning}")

        # Output JSON for machine consumption
        result = {
            "status": "ok" if is_valid else "error",
            "manifest": str(manifest_path),
            "ext_type": info.extension_type,
            "name": info.name,
            "version": info.version,
            "warnings": warnings
        }

        if not verbose:
            common.json_output(result)

        if is_valid:
            if not verbose:
                print(f"manifest: ok ({manifest_path})")
            else:
                common.log_success("Manifest is valid")
            return True
        else:
            common.log_error(f"Manifest validation failed: {manifest_path}")
            return False

    except SystemExit:
        common.log_error(f"Failed to parse manifest: {manifest_path}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Joomla extension manifest files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-s", "--src-dir",
        default="src",
        help="Source directory to search for manifests (default: src)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "manifest",
        nargs="?",
        help="Specific manifest file to validate (optional)"
    )

    args = parser.parse_args()

    try:
        if args.manifest:
            # Validate specific manifest
            manifest_path = Path(args.manifest)
            if not manifest_path.is_file():
                common.die(f"Manifest file not found: {args.manifest}")

            success = validate_manifest_file(manifest_path, args.verbose)
            return 0 if success else 1
        else:
            # Find and validate all manifests in src directory
            manifests = joomla_manifest.find_all_manifests(args.src_dir)

            if not manifests:
                common.die(f"No manifest files found in {args.src_dir}")

            if args.verbose:
                common.log_section("Validating Manifests")
                common.log_info(f"Found {len(manifests)} manifest(s)")
                print()

            all_valid = True
            for manifest in manifests:
                if not validate_manifest_file(manifest, args.verbose):
                    all_valid = False

            if args.verbose:
                print()
                if all_valid:
                    common.log_success(f"All {len(manifests)} manifest(s) are valid")
                else:
                    common.log_error("Some manifests failed validation")

            return 0 if all_valid else 1

    except Exception as e:
        common.log_error(f"Validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
