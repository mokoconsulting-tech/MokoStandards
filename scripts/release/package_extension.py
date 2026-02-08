#!/usr/bin/env python3
"""
Package Joomla extension as distributable ZIP.

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
DEFGROUP: Script.Release
INGROUP: Extension.Packaging
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/release/package_extension.py
VERSION: 03.01.02
BRIEF: Package Joomla extension as distributable ZIP
USAGE: ./scripts/release/package_extension.py [output_dir] [version]
"""

import argparse
import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Set

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
    import extension_utils
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


# Exclusion patterns for packaging
EXCLUDE_PATTERNS = {
    # Version control
    ".git", ".gitignore", ".gitattributes",
    # IDE
    ".vscode", ".idea", "*.sublime-*",
    # Development
    "node_modules", "vendor", ".env", ".env.*",
    # Documentation (optional, can be included)
    # Build artifacts
    "dist", "build", ".phpunit.cache",
    # Development tool caches and artifacts
    ".phpstan.cache", ".psalm", ".rector",
    "phpmd-cache", ".php-cs-fixer.cache", ".phplint-cache",
    # OS files
    ".DS_Store", "Thumbs.db",
    # Logs
    "*.log",
    # Tests
    "tests", "test", "Tests",
    # CI/CD
    ".github",
    # Scripts
    "scripts",
    # Docs (can be included if needed)
    "docs",
    # Config files
    "composer.json", "composer.lock",
    "package.json", "package-lock.json",
    "phpunit.xml", "phpstan.neon", "phpcs.xml",
    "codeception.yml", "psalm.xml", ".php-cs-fixer.php",
    # Others
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "GOVERNANCE.md",
    "Makefile",
}


def should_exclude(path: Path, base_path: Path, exclude_patterns: Set[str]) -> bool:
    """
    Check if a path should be excluded from packaging.

    Args:
        path: Path to check
        base_path: Base directory path
        exclude_patterns: Set of exclusion patterns

    Returns:
        True if should be excluded
    """
    relative_path = path.relative_to(base_path)

    # Check each part of the path
    for part in relative_path.parts:
        if part in exclude_patterns:
            return True
        # Check wildcard patterns
        for pattern in exclude_patterns:
            if "*" in pattern:
                import fnmatch
                if fnmatch.fnmatch(part, pattern):
                    return True

    return False


def create_package(
    src_dir: str,
    output_dir: str,
    version: str = None,
    repo_name: str = None,
    exclude_patterns: Set[str] = None
) -> Path:
    """
    Create a distributable ZIP package for a Joomla or Dolibarr extension.

    Args:
        src_dir: Source directory containing extension files
        output_dir: Output directory for ZIP file
        version: Version string (auto-detected if not provided)
        repo_name: Repository name for ZIP file naming
        exclude_patterns: Patterns to exclude from packaging

    Returns:
        Path to created ZIP file
    """
    src_path = Path(src_dir)
    if not src_path.is_dir():
        common.die(f"Source directory not found: {src_dir}")

    # Detect extension platform and get info
    ext_info = extension_utils.get_extension_info(src_dir)

    if not ext_info:
        common.die(f"No Joomla or Dolibarr extension found in {src_dir}")

    # Determine version
    if not version:
        version = ext_info.version

    # Determine repo name
    if not repo_name:
        try:
            repo_root = common.git_root()
            repo_name = repo_root.name
        except Exception:
            repo_name = "extension"

    # Determine exclusion patterns
    if exclude_patterns is None:
        exclude_patterns = EXCLUDE_PATTERNS

    # Create output directory
    output_path = Path(output_dir)
    common.ensure_dir(output_path)

    # Generate ZIP filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    platform_suffix = f"{ext_info.platform.value}-{ext_info.extension_type}"
    zip_filename = f"{repo_name}-{version}-{platform_suffix}.zip"
    zip_path = output_path / zip_filename

    # Remove existing ZIP if present
    if zip_path.exists():
        zip_path.unlink()

    common.log_section("Creating Extension Package")
    common.log_kv("Platform", ext_info.platform.value.upper())
    common.log_kv("Extension", ext_info.name)
    common.log_kv("Type", ext_info.extension_type)
    common.log_kv("Version", version)
    common.log_kv("Source", src_dir)
    common.log_kv("Output", str(zip_path))
    print()

    # Create ZIP file
    file_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in src_path.rglob("*"):
            if item.is_file():
                # Check if should be excluded
                if should_exclude(item, src_path, exclude_patterns):
                    continue

                # Add to ZIP with relative path
                arcname = item.relative_to(src_path)
                zipf.write(item, arcname)
                file_count += 1

                if file_count % 10 == 0:
                    common.log_step(f"Added {file_count} files...")

    # Get ZIP file size
    zip_size = zip_path.stat().st_size
    zip_size_mb = zip_size / (1024 * 1024)

    print()
    common.log_success(f"Package created: {zip_path.name}")
    common.log_kv("Files", str(file_count))
    common.log_kv("Size", f"{zip_size_mb:.2f} MB")

    # Output JSON for machine consumption
    result = {
        "status": "ok",
        "platform": ext_info.platform.value,
        "extension": ext_info.name,
        "ext_type": ext_info.extension_type,
        "version": version,
        "package": str(zip_path),
        "files": file_count,
        "size_bytes": zip_size
    }

    print()
    common.json_output(result)

    return zip_path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Package Joomla or Dolibarr extension as distributable ZIP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Package with auto-detected version
  %(prog)s

  # Package to specific directory
  %(prog)s dist

  # Package with specific version
  %(prog)s dist 1.2.3

  # Package with custom source
  %(prog)s --src-dir my-extension dist 1.0.0

Supports both Joomla and Dolibarr extensions with automatic platform detection.
"""
    )

    parser.add_argument(
        "output_dir",
        nargs="?",
        default="dist",
        help="Output directory for ZIP file (default: dist)"
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="Version string (default: auto-detected from manifest)"
    )
    parser.add_argument(
        "-s", "--src-dir",
        default="src",
        help="Source directory (default: src)"
    )
    parser.add_argument(
        "--repo-name",
        help="Repository name for ZIP filename (default: auto-detected)"
    )
    parser.add_argument(
        "--include-docs",
        action="store_true",
        help="Include documentation files in package"
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test files in package"
    )

    args = parser.parse_args()

    try:
        # Adjust exclusion patterns based on arguments
        exclude_patterns = EXCLUDE_PATTERNS.copy()
        if args.include_docs:
            exclude_patterns.discard("docs")
            exclude_patterns.discard("README.md")
            exclude_patterns.discard("CHANGELOG.md")
        if args.include_tests:
            exclude_patterns.discard("tests")
            exclude_patterns.discard("test")
            exclude_patterns.discard("Tests")

        # Create package
        zip_path = create_package(
            src_dir=args.src_dir,
            output_dir=args.output_dir,
            version=args.version,
            repo_name=args.repo_name,
            exclude_patterns=exclude_patterns
        )

        return 0

    except Exception as e:
        common.log_error(f"Packaging failed: {e}")
        result = {
            "status": "error",
            "error": str(e)
        }
        common.json_output(result)
        return 1


if __name__ == "__main__":
    sys.exit(main())
