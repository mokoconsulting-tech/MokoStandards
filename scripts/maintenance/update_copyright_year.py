#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Maintenance
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/maintenance/update_copyright_year.py
VERSION: 02.00.00
BRIEF: Updates copyright year in file headers across the codebase
PATH: /scripts/maintenance/update_copyright_year.py
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


# File extensions to process
PROCESSABLE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".php", ".java", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".go", ".rs", ".rb", ".pl",
    ".sh", ".bash", ".zsh", ".ps1",
    ".css", ".scss", ".sass",
    ".html", ".xml", ".yaml", ".yml", ".md",
}

# Directories to exclude
EXCLUDE_DIRS = {
    ".git", ".svn", ".hg",
    "node_modules", "bower_components",
    "vendor", "vendors",
    "__pycache__", ".pytest_cache",
    "venv", ".venv", "env", ".env",
    "build", "dist", "target",
}


def should_exclude(path: Path) -> bool:
    """
    Check if a path should be excluded.
    
    Args:
        path: Path to check
        
    Returns:
        True if path should be excluded
    """
    parts = path.parts
    return any(part in EXCLUDE_DIRS for part in parts)


def update_copyright_in_file(file_path: Path, target_year: int, dry_run: bool = False) -> bool:
    """
    Update copyright year in a file.
    
    Args:
        file_path: Path to file
        target_year: Year to update to
        dry_run: If True, don't actually modify files
        
    Returns:
        True if file was modified (or would be in dry-run)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return False
    
    modified = False
    
    # Pattern 1: Copyright (C) YYYY
    pattern1 = r'Copyright\s+\(C\)\s+(\d{4})'
    matches = list(re.finditer(pattern1, content, re.IGNORECASE))
    
    for match in matches:
        old_year = int(match.group(1))
        if old_year < target_year:
            old_text = match.group(0)
            new_text = f"Copyright (C) {target_year}"
            content = content.replace(old_text, new_text, 1)
            modified = True
    
    # Pattern 2: Copyright YYYY (without (C))
    pattern2 = r'Copyright\s+(\d{4})(?!\d)'
    matches = list(re.finditer(pattern2, content, re.IGNORECASE))
    
    for match in matches:
        old_year = int(match.group(1))
        if old_year < target_year:
            old_text = match.group(0)
            new_text = f"Copyright {target_year}"
            content = content.replace(old_text, new_text, 1)
            modified = True
    
    # Pattern 3: @copyright YYYY
    pattern3 = r'@copyright\s+(\d{4})'
    matches = list(re.finditer(pattern3, content, re.IGNORECASE))
    
    for match in matches:
        old_year = int(match.group(1))
        if old_year < target_year:
            old_text = match.group(0)
            new_text = f"@copyright {target_year}"
            content = content.replace(old_text, new_text, 1)
            modified = True
    
    if modified and not dry_run:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Error: Could not write {file_path}: {e}", file=sys.stderr)
            return False
    
    return modified


def process_directory(root: Path, target_year: int, dry_run: bool = False) -> dict:
    """
    Process all files in a directory.
    
    Args:
        root: Root directory to process
        target_year: Year to update to
        dry_run: If True, don't actually modify files
        
    Returns:
        Dictionary with processing results
    """
    results = {
        "files_scanned": 0,
        "files_modified": 0,
        "modified_files": [],
    }
    
    for file_path in root.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            if file_path.suffix.lower() in PROCESSABLE_EXTENSIONS:
                results["files_scanned"] += 1
                
                if update_copyright_in_file(file_path, target_year, dry_run):
                    results["files_modified"] += 1
                    rel_path = str(file_path.relative_to(root))
                    results["modified_files"].append(rel_path)
    
    return results


def print_report(results: dict, target_year: int, dry_run: bool) -> None:
    """
    Print processing report.
    
    Args:
        results: Processing results
        target_year: Target year
        dry_run: Whether this was a dry run
    """
    print("\n" + "=" * 80)
    print("COPYRIGHT YEAR UPDATE REPORT")
    print("=" * 80)
    
    mode = "DRY RUN" if dry_run else "ACTUAL RUN"
    print(f"\nMode: {mode}")
    print(f"Target Year: {target_year}")
    
    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Files scanned:    {results['files_scanned']:,}")
    print(f"Files modified:   {results['files_modified']:,}")
    
    if results["modified_files"]:
        print(f"\n📝 MODIFIED FILES")
        print("-" * 80)
        
        for file_path in sorted(results["modified_files"])[:50]:
            print(f"  {file_path}")
        
        if len(results["modified_files"]) > 50:
            print(f"  ... and {len(results['modified_files']) - 50} more")
    else:
        print(f"\n✅ No files needed updating")
    
    print("\n" + "=" * 80)
    
    if dry_run and results["files_modified"] > 0:
        print("\n💡 This was a dry run. Use --apply to actually modify files.")


def main() -> int:
    """
    Main entry point for copyright year updater.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Update copyright year in file headers"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to process (default: current directory)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Target year (default: current year)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually modify files (default is dry-run)"
    )
    
    args = parser.parse_args()
    root = Path(args.path).resolve()
    
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1
    
    dry_run = not args.apply
    
    print(f"Processing copyright years in: {root}")
    print(f"Target year: {args.year}")
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified")
        print("Use --apply to actually modify files\n")
    
    results = process_directory(root, args.year, dry_run)
    print_report(results, args.year, dry_run)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
