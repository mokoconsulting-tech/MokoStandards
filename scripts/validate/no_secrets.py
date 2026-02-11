#!/usr/bin/env python3
"""
Scan for accidentally committed secrets and credentials.

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
INGROUP: Security
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/no_secrets.py
VERSION: 03.02.00
BRIEF: Scan for accidentally committed secrets and credentials
NOTE: High-signal pattern detection to prevent credential exposure
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


# High-signal patterns only. Any match is a hard fail.
SECRET_PATTERNS = [
    # Private keys
    r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
    r'PuTTY-User-Key-File-',
    # AWS keys
    r'AKIA[0-9A-Z]{16}',
    r'ASIA[0-9A-Z]{16}',
    # GitHub tokens
    r'ghp_[A-Za-z0-9]{36}',
    r'gho_[A-Za-z0-9]{36}',
    r'ghu_[A-Za-z0-9]{36}',  # GitHub user token
    r'ghs_[A-Za-z0-9]{36}',  # GitHub server token
    r'github_pat_[A-Za-z0-9_]{20,}',
    # Slack tokens
    r'xox[baprs]-[0-9A-Za-z-]{10,48}',
    # Stripe keys
    r'sk_live_[0-9a-zA-Z]{20,}',
    r'rk_live_[0-9a-zA-Z]{20,}',  # Stripe restricted key
    # Azure keys
    r'[0-9a-zA-Z/+]{86}==',  # Azure Storage Account Key
    # Google Cloud keys  
    r'AIza[0-9A-Za-z\\-_]{35}',  # Google API Key
    # NPM tokens
    r'npm_[A-Za-z0-9]{36}',
    # PyPI tokens
    r'pypi-AgEIcHlwaS5vcmc[A-Za-z0-9-_]{50,}',
    # Docker Hub
    r'dckr_pat_[A-Za-z0-9_-]{20,}',
    # GitLab tokens
    r'glpat-[0-9a-zA-Z\-]{20}',
]

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    'vendor',
    'node_modules',
    'dist',
    'build',
    '.git',
    'docs',  # Documentation often contains examples
    'templates',  # Templates contain example patterns
}

# File names to exclude from scanning (exact filename match)
EXCLUDE_FILES = {
    'no_secrets.py',  # This file contains the patterns
}

# File extensions to exclude from scanning
EXCLUDE_EXTENSIONS = {
    '.md',  # Markdown documentation files
}


def scan_file(filepath: Path, patterns: List[re.Pattern]) -> List[Dict[str, str]]:
    """
    Scan a file for secret patterns.

    Args:
        filepath: Path to file to scan
        patterns: Compiled regex patterns to search for

    Returns:
        List of matches with file, line number, and content
    """
    hits = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in patterns:
                    if pattern.search(line):
                        hits.append({
                            'file': str(filepath),
                            'line': line_num,
                            'content': line.strip()[:100]  # Limit to 100 chars
                        })
    except Exception as e:
        common.log_warn(f"Could not read {filepath}: {e}")

    return hits


def scan_directory(src_dir: str, patterns: List[re.Pattern]) -> List[Dict[str, str]]:
    """
    Recursively scan directory for secrets.

    Args:
        src_dir: Directory to scan
        patterns: Compiled regex patterns

    Returns:
        List of all matches
    """
    src_path = Path(src_dir)
    all_hits = []

    for item in src_path.rglob("*"):
        # Skip directories
        if not item.is_file():
            continue

        # Skip excluded directories
        if any(excluded in item.parts for excluded in EXCLUDE_DIRS):
            continue

        # Skip excluded files by name
        if item.name in EXCLUDE_FILES:
            continue

        # Skip excluded file extensions
        if item.suffix in EXCLUDE_EXTENSIONS:
            continue

        # Skip binary files (heuristic)
        try:
            with open(item, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:  # Contains null bytes = likely binary
                    continue
        except Exception:
            continue

        # Scan the file
        hits = scan_file(item, patterns)
        all_hits.extend(hits)

    return all_hits


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scan for accidentally committed secrets and credentials"
    )
    parser.add_argument(
        "-s", "--src-dir",
        default=os.environ.get("SRC_DIR", "src"),
        help="Source directory to scan (default: src)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be checked without executing"
    )

    args = parser.parse_args()

    if args.dry_run:
        print("[DRY-RUN] Would scan directory:", args.src_dir)
        print("[DRY-RUN] Would check for secret patterns")
        print(json.dumps({"status": "pass", "message": "dry-run mode"}))
        return 0

    # Check if source directory exists
    if not Path(args.src_dir).is_dir():
        result = {
            "status": "fail",
            "error": "src directory missing"
        }
        common.json_output(result)
        return 1

    # Compile patterns
    compiled_patterns = [re.compile(pattern) for pattern in SECRET_PATTERNS]

    # Scan directory
    hits = scan_directory(args.src_dir, compiled_patterns)

    if hits:
        # Limit to first 50 hits
        hits = hits[:50]

        result = {
            "status": "fail",
            "error": "secret_pattern_detected",
            "hits": [{"hit": f"{h['file']}:{h['line']}: {h['content']}"} for h in hits]
        }

        common.json_output(result)

        # Also print human-readable output
        print("\nERROR: Potential secrets detected!", file=sys.stderr)
        print(f"\nFound {len(hits)} potential secret(s):", file=sys.stderr)
        for hit in hits[:10]:  # Show first 10 in detail
            print(f"  {hit['file']}:{hit['line']}", file=sys.stderr)
            print(f"    {hit['content']}", file=sys.stderr)

        if len(hits) > 10:
            print(f"  ... and {len(hits) - 10} more", file=sys.stderr)

        print("\nPlease remove any secrets and use environment variables or secret management instead.", file=sys.stderr)

        return 1

    result = {
        "status": "ok",
        "src_dir": args.src_dir
    }
    common.json_output(result)
    print("no_secrets: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
