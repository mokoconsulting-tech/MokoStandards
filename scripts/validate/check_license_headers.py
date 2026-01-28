#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Validate
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/validate/check_license_headers.py
VERSION: 03.00.00
BRIEF: Checks and optionally fixes missing or incorrect license headers in source files
PATH: /scripts/validate/check_license_headers.py
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


# Standard license header template (GPL-3.0-or-later)
LICENSE_HEADER_TEMPLATE = """Copyright (C) {year} Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later"""

# File type configurations
FILE_CONFIGS = {
    ".py": {
        "comment_start": "#",
        "comment_end": "",
        "header_pattern": r'#\s*Copyright.*?GPL-3\.0-or-later',
    },
    ".js": {
        "comment_start": "//",
        "comment_end": "",
        "header_pattern": r'//\s*Copyright.*?GPL-3\.0-or-later',
    },
    ".ts": {
        "comment_start": "//",
        "comment_end": "",
        "header_pattern": r'//\s*Copyright.*?GPL-3\.0-or-later',
    },
    ".php": {
        "comment_start": "/*",
        "comment_end": "*/",
        "header_pattern": r'/\*.*?Copyright.*?GPL-3\.0-or-later.*?\*/',
    },
    ".java": {
        "comment_start": "/*",
        "comment_end": "*/",
        "header_pattern": r'/\*.*?Copyright.*?GPL-3\.0-or-later.*?\*/',
    },
    ".c": {
        "comment_start": "/*",
        "comment_end": "*/",
        "header_pattern": r'/\*.*?Copyright.*?GPL-3\.0-or-later.*?\*/',
    },
    ".cpp": {
        "comment_start": "//",
        "comment_end": "",
        "header_pattern": r'//\s*Copyright.*?GPL-3\.0-or-later',
    },
    ".sh": {
        "comment_start": "#",
        "comment_end": "",
        "header_pattern": r'#\s*Copyright.*?GPL-3\.0-or-later',
    },
}

# Extensions to check
CHECKABLE_EXTENSIONS = set(FILE_CONFIGS.keys())

# Directories to exclude
EXCLUDE_DIRS = {
    ".git", "node_modules", "vendor", "venv", ".venv",
    "build", "dist", "__pycache__", ".pytest_cache",
}


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def has_license_header(file_path: Path) -> bool:
    """
    Check if file has a license header.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if license header is present
    """
    ext = file_path.suffix.lower()
    if ext not in FILE_CONFIGS:
        return True  # Skip files we don't handle
    
    config = FILE_CONFIGS[ext]
    pattern = config["header_pattern"]
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            # Read first 2000 characters (headers should be at the top)
            content = f.read(2000)
            return bool(re.search(pattern, content, re.DOTALL | re.IGNORECASE))
    except Exception:
        return True  # Assume it's fine if we can't read it


def generate_header(file_path: Path, year: Optional[int] = None) -> str:
    """
    Generate a license header for a file.
    
    Args:
        file_path: Path to file
        year: Copyright year (default: current year)
        
    Returns:
        Formatted license header
    """
    if year is None:
        year = datetime.now().year
    
    ext = file_path.suffix.lower()
    if ext not in FILE_CONFIGS:
        return ""
    
    config = FILE_CONFIGS[ext]
    header_text = LICENSE_HEADER_TEMPLATE.format(year=year)
    
    # Format with appropriate comment style
    if config["comment_end"]:
        # Multi-line comment style (/* */)
        lines = ["/*"]
        for line in header_text.split("\n"):
            if line:
                lines.append(f" * {line}")
            else:
                lines.append(" *")
        lines.append(" */")
        return "\n".join(lines)
    else:
        # Single-line comment style (# or //)
        lines = []
        for line in header_text.split("\n"):
            if line:
                lines.append(f"{config['comment_start']} {line}")
            else:
                lines.append(config['comment_start'])
        return "\n".join(lines)


def add_license_header(file_path: Path, year: Optional[int] = None, dry_run: bool = False) -> bool:
    """
    Add license header to a file.
    
    Args:
        file_path: Path to file
        year: Copyright year (default: current year)
        dry_run: If True, don't actually modify file
        
    Returns:
        True if header was added (or would be in dry-run)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return False
    
    # Generate header
    header = generate_header(file_path, year)
    if not header:
        return False
    
    # Handle shebang for scripts
    if content.startswith("#!"):
        shebang_end = content.find("\n")
        if shebang_end != -1:
            shebang = content[:shebang_end + 1]
            rest = content[shebang_end + 1:]
            new_content = f"{shebang}{header}\n\n{rest}"
        else:
            new_content = f"{content}\n{header}\n"
    else:
        new_content = f"{header}\n\n{content}"
    
    if not dry_run:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            print(f"Error: Could not write {file_path}: {e}", file=sys.stderr)
            return False
    
    return True


def scan_directory(root: Path) -> Dict:
    """
    Scan directory for files missing license headers.
    
    Args:
        root: Root directory to scan
        
    Returns:
        Dictionary with scan results
    """
    results = {
        "total_files": 0,
        "missing_headers": [],
        "with_headers": 0,
    }
    
    for file_path in root.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            if file_path.suffix.lower() in CHECKABLE_EXTENSIONS:
                results["total_files"] += 1
                
                if has_license_header(file_path):
                    results["with_headers"] += 1
                else:
                    rel_path = str(file_path.relative_to(root))
                    results["missing_headers"].append(rel_path)
    
    return results


def print_report(results: Dict, root: Path) -> None:
    """Print scan report."""
    print("\n" + "=" * 80)
    print("LICENSE HEADER CHECK REPORT")
    print("=" * 80)
    print(f"\nDirectory: {root}")
    
    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Files scanned:         {results['total_files']:,}")
    print(f"With license headers:  {results['with_headers']:,}")
    print(f"Missing headers:       {len(results['missing_headers']):,}")
    
    if results["missing_headers"]:
        print(f"\n❌ FILES MISSING LICENSE HEADERS")
        print("-" * 80)
        
        for file_path in sorted(results["missing_headers"])[:50]:
            print(f"  {file_path}")
        
        if len(results["missing_headers"]) > 50:
            print(f"  ... and {len(results['missing_headers']) - 50} more")
    else:
        print(f"\n✅ All files have license headers!")
    
    print("\n" + "=" * 80)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check and fix license headers in source files"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to check (default: current directory)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Add missing license headers"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Copyright year (default: current year)"
    )
    
    args = parser.parse_args()
    root = Path(args.path).resolve()
    
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1
    
    print(f"Scanning for license headers in: {root}")
    
    results = scan_directory(root)
    print_report(results, root)
    
    if args.fix and results["missing_headers"]:
        print(f"\n🔧 ADDING LICENSE HEADERS")
        print("-" * 80)
        
        for file_path in results["missing_headers"]:
            full_path = root / file_path
            if add_license_header(full_path, args.year):
                print(f"✅ Added header: {file_path}")
            else:
                print(f"❌ Failed: {file_path}")
        
        print("\n✅ License header update complete!")
    elif results["missing_headers"]:
        print("\n💡 Use --fix to add missing license headers")
    
    return 1 if results["missing_headers"] else 0


if __name__ == "__main__":
    sys.exit(main())
