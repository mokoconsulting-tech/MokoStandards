#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
File header standardization tool for MokoStandards.

This script scans files for warranty disclaimers and replaces full GPL headers
with compressed SPDX headers where appropriate, according to the policy defined
in docs/policy/file-headers.md.

Full disclaimers are KEPT in:
- All .md files
- Executable scripts (with shebang or executable permission)
- Platform-specific files (Dolibarr, Joomla, WordPress paths)

Compressed headers are APPLIED to:
- GitHub Actions workflows (.github/workflows/*.yml)
- Configuration files (.github/*.yml)
- Template files (templates/**/*.yml)
- Non-executable modules and libraries
"""

import argparse
import os
import re
import stat
import sys
from pathlib import Path
from typing import Tuple, Optional

# Compressed header templates
COMPRESSED_HEADER_YAML = """# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
"""

COMPRESSED_HEADER_HTML = """<!-- Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech> -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
"""

# Pattern to match full GPL warranty disclaimer
WARRANTY_PATTERN = re.compile(
    r'^([#\s]*Copyright.*?)\n'
    r'(.*?)'
    r'(.*?without even the implied warranty of.*?)\n'
    r'(.*?MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.*?)\n'
    r'(.*?GNU General Public License for more details.*?)\n'
    r'(.*?\n)*?'
    r'([#\s]*along with this program.*?)?',
    re.MULTILINE | re.DOTALL
)

# More specific pattern for YAML/shell comments with full GPL header
YAML_WARRANTY_PATTERN = re.compile(
    r'^# Copyright \(C\) (\d{4}) Moko Consulting <[^>]+>\n'
    r'#\n'
    r'# This file is part of[^\n]+\n'
    r'#\n'
    r'# SPDX-License-Identifier:[^\n]+\n'
    r'#\n'
    r'# This program is free software[^\n]+\n'
    r'# [^\n]+\n'  # it under the terms...
    r'# [^\n]+\n'  # the Free Software Foundation...
    r'# [^\n]+\n'  # (at your option) any later version
    r'#\n'
    r'# This program is distributed[^\n]+\n'
    r'# but WITHOUT ANY WARRANTY[^\n]+\n'
    r'# MERCHANTABILITY[^\n]+\n'
    r'# GNU General Public License for more details[^\n]*\n'
    r'#\n'
    r'(?:# You should have received[^\n]+\n)?'
    r'(?:# along with this program[^\n]+\n)?'
    r'(?:#\n)?',
    re.MULTILINE
)


def is_executable(filepath: Path) -> bool:
    """
    Check if a file is executable.

    Args:
        filepath: Path to the file

    Returns:
        True if file has executable permission bit set
    """
    try:
        return os.access(filepath, os.X_OK) and filepath.is_file()
    except OSError:
        return False


def has_shebang(filepath: Path) -> bool:
    """
    Check if a file starts with a shebang (#!).

    Args:
        filepath: Path to the file

    Returns:
        True if file starts with shebang
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            return first_line.startswith('#!')
    except (OSError, UnicodeDecodeError):
        return False


def is_platform_specific(filepath: Path) -> bool:
    """
    Check if a file is platform-specific (Dolibarr, Joomla, WordPress).

    Args:
        filepath: Path to the file

    Returns:
        True if file is in a platform-specific path
    """
    path_str = str(filepath).lower()
    platform_indicators = [
        'dolibarr',
        'joomla',
        'wordpress',
        'wp-content',
        'htdocs',
        '/modules/',
        '/custom/',
        '/plugins/',
        '/themes/',
    ]
    return any(indicator in path_str for indicator in platform_indicators)


def should_keep_full_disclaimer(filepath: Path) -> bool:
    """
    Determine if a file should keep its full warranty disclaimer.

    Args:
        filepath: Path to the file

    Returns:
        True if full disclaimer should be kept
    """
    # Always keep full disclaimer in .md files
    if filepath.suffix == '.md':
        return True

    # Keep for executable scripts
    if is_executable(filepath) or has_shebang(filepath):
        return True

    # Keep for platform-specific files
    if is_platform_specific(filepath):
        return True

    return False


def extract_copyright_info(content: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract copyright and SPDX identifier from existing header.

    Args:
        content: File content

    Returns:
        Tuple of (copyright_line, spdx_line) or (None, None)
    """
    lines = content.split('\n', 20)  # Check first 20 lines

    copyright_line = None
    spdx_line = None

    for line in lines:
        if 'Copyright' in line and 'Moko Consulting' in line:
            # Extract just the copyright part
            match = re.search(r'Copyright.*?<.*?>', line)
            if match:
                copyright_line = match.group(0)

        if 'SPDX-License-Identifier' in line:
            # Extract the SPDX identifier
            match = re.search(r'SPDX-License-Identifier:\s*GPL-3\.0-or-later', line)
            if match:
                spdx_line = match.group(0)

    return copyright_line, spdx_line


def convert_to_compressed_header(content: str, filepath: Path) -> Tuple[str, bool]:
    """
    Convert full GPL header to compressed SPDX header.

    Args:
        content: Original file content
        filepath: Path to the file

    Returns:
        Tuple of (modified_content, was_modified)
    """
    if should_keep_full_disclaimer(filepath):
        return content, False

    # Check if already has compressed header
    lines = content.split('\n', 5)
    if len(lines) >= 2:
        first_two = '\n'.join(lines[:2])
        if ('Copyright (C)' in first_two and
            'SPDX-License-Identifier: GPL-3.0-or-later' in first_two and
            'This program is free software' not in first_two):
            # Already compressed
            return content, False

    # Try to match and replace the full warranty disclaimer
    match = YAML_WARRANTY_PATTERN.search(content)
    if match:
        # Extract year from copyright if present
        copyright_match = re.search(r'Copyright \(C\) (\d{4})', match.group(0))
        year = copyright_match.group(1) if copyright_match else '2025'

        # Create compressed header with correct year
        compressed = f"# Copyright (C) {year} Moko Consulting <hello@mokoconsulting.tech>\n"
        compressed += "# SPDX-License-Identifier: GPL-3.0-or-later\n"

        # Replace the full header with compressed version
        new_content = YAML_WARRANTY_PATTERN.sub(compressed, content, count=1)
        return new_content, True

    return content, False


def process_file(filepath: Path, dry_run: bool = False, verbose: bool = True) -> bool:
    """
    Process a single file to convert headers.

    Args:
        filepath: Path to the file
        dry_run: If True, only report changes without modifying
        verbose: If True, print detailed output

    Returns:
        True if file was modified (or would be in dry_run)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, UnicodeDecodeError) as e:
        if verbose:
            print(f"❌ Error reading {filepath}: {e}", file=sys.stderr)
        return False

    new_content, modified = convert_to_compressed_header(content, filepath)

    if modified:
        if dry_run:
            if verbose:
                print(f"🔄 Would compress header: {filepath}")
        else:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                if verbose:
                    print(f"✅ Compressed header: {filepath}")
            except OSError as e:
                if verbose:
                    print(f"❌ Error writing {filepath}: {e}", file=sys.stderr)
                return False
        return True
    else:
        if verbose and should_keep_full_disclaimer(filepath):
            print(f"⏭️  Keeping full disclaimer: {filepath}")

    return False


def scan_directory(directory: Path, dry_run: bool = False, verbose: bool = True) -> int:
    """
    Recursively scan directory and process files.

    Args:
        directory: Root directory to scan
        dry_run: If True, only report changes without modifying
        verbose: If True, print detailed output

    Returns:
        Number of files modified (or would be in dry_run)
    """
    modified_count = 0

    # File patterns to process
    patterns = [
        '**/*.yml',
        '**/*.yaml',
        '**/*.py',
        '**/*.sh',
    ]

    files_to_process = set()
    for pattern in patterns:
        files_to_process.update(directory.glob(pattern))

    for filepath in sorted(files_to_process):
        if filepath.is_file():
            if process_file(filepath, dry_run=dry_run, verbose=verbose):
                modified_count += 1

    return modified_count


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Standardize file headers according to MokoStandards policy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes
  %(prog)s --dry-run

  # Apply to workflows only
  %(prog)s --dir .github/workflows --fix

  # Apply to entire repository
  %(prog)s --fix

  # Quiet mode
  %(prog)s --fix --quiet
        """
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Apply changes to files (default is dry-run)'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        default=Path.cwd(),
        help='Directory to process (default: current directory)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    args = parser.parse_args()

    # Default to dry-run unless --fix is specified
    dry_run = not args.fix
    verbose = not args.quiet

    if not args.dir.is_dir():
        print(f"❌ Error: {args.dir} is not a directory", file=sys.stderr)
        return 1

    if verbose:
        mode = "DRY RUN" if dry_run else "APPLY CHANGES"
        print(f"🔧 File Header Standardization Tool - {mode}")
        print(f"📁 Processing directory: {args.dir}")
        print()

    modified_count = scan_directory(args.dir, dry_run=dry_run, verbose=verbose)

    if verbose:
        print()
        print(f"{'Would modify' if dry_run else 'Modified'} {modified_count} file(s)")
        if dry_run and modified_count > 0:
            print()
            print("ℹ️  Run with --fix to apply changes")

    return 0


if __name__ == '__main__':
    sys.exit(main())
