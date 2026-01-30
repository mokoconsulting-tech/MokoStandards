#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Validate
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/validate/find_todos.py
VERSION: 03.00.00
BRIEF: Finds and reports TODO, FIXME, and other code comments across the codebase
PATH: /scripts/validate/find_todos.py
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


# Comment markers to search for
MARKERS = {
    "TODO": "Tasks to be done",
    "FIXME": "Issues to be fixed",
    "HACK": "Temporary workarounds",
    "XXX": "Warning or caution",
    "BUG": "Known bugs",
    "NOTE": "Important notes",
}

# File extensions to search
SEARCHABLE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".php", ".java", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".go", ".rs", ".rb", ".pl",
    ".sh", ".bash", ".zsh", ".ps1",
    ".sql", ".css", ".scss", ".sass",
    ".html", ".xml", ".yaml", ".yml",
}

# Directories to exclude
EXCLUDE_DIRS = {
    ".git", ".svn", ".hg",
    "node_modules", "bower_components",
    "vendor", "vendors",
    "__pycache__", ".pytest_cache",
    "venv", ".venv", "env", ".env",
    "build", "dist", "target",
    ".idea", ".vscode",
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


def find_markers_in_file(file_path: Path, markers: Set[str]) -> List[Dict]:
    """
    Find marker comments in a file.

    Args:
        file_path: Path to file to search
        markers: Set of marker strings to search for

    Returns:
        List of dictionaries with marker information
    """
    findings = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, start=1):
                # Check for each marker
                for marker in markers:
                    # Look for marker in various comment styles
                    patterns = [
                        rf'#\s*{marker}[:\s]+(.*)',      # Python, Shell
                        rf'//\s*{marker}[:\s]+(.*)',     # C++, JavaScript
                        rf'/\*\s*{marker}[:\s]+(.*)',    # C-style multi-line
                        rf'<!--\s*{marker}[:\s]+(.*)',   # HTML/XML
                    ]

                    for pattern in patterns:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            comment_text = match.group(1).strip()
                            findings.append({
                                "marker": marker,
                                "line": line_num,
                                "text": comment_text if comment_text else "(no description)",
                                "full_line": line.strip(),
                            })
                            break

    except Exception as e:
        # File might be binary or have encoding issues, skip silently
        # but log in debug mode if needed
        import sys
        if '--verbose' in sys.argv or '-v' in sys.argv:
            print(f"Warning: Failed to process {file_path}: {e}", file=sys.stderr)

    return findings


def search_directory(root: Path, markers: Set[str]) -> Dict:
    """
    Search directory for marker comments.

    Args:
        root: Root directory to search
        markers: Set of marker strings to search for

    Returns:
        Dictionary with search results
    """
    results = {
        "files_searched": 0,
        "total_findings": 0,
        "by_marker": {marker: [] for marker in markers},
        "by_file": {},
    }

    for file_path in root.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            if file_path.suffix.lower() in SEARCHABLE_EXTENSIONS:
                results["files_searched"] += 1

                findings = find_markers_in_file(file_path, markers)

                if findings:
                    rel_path = str(file_path.relative_to(root))
                    results["by_file"][rel_path] = findings
                    results["total_findings"] += len(findings)

                    for finding in findings:
                        marker = finding["marker"]
                        results["by_marker"][marker].append({
                            "file": rel_path,
                            "line": finding["line"],
                            "text": finding["text"],
                            "full_line": finding["full_line"],
                        })

    return results


def print_report(results: Dict, root: Path, group_by: str) -> None:
    """
    Print search results report.

    Args:
        results: Search results
        root: Root directory searched
        group_by: How to group results ('marker' or 'file')
    """
    print("\n" + "=" * 80)
    print("CODE MARKER ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nDirectory: {root}")

    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Files searched:   {results['files_searched']:,}")
    print(f"Total findings:   {results['total_findings']:,}")

    # Count by marker type
    print(f"\nBy marker type:")
    for marker, findings in sorted(results["by_marker"].items()):
        count = len(findings)
        if count > 0:
            print(f"  {marker:<10} {count:>5}")

    if results["total_findings"] == 0:
        print(f"\n✅ No markers found!")
        print("=" * 80)
        return

    # Print detailed findings
    if group_by == "marker":
        print(f"\n📝 FINDINGS BY MARKER TYPE")
        print("=" * 80)

        for marker, findings in sorted(results["by_marker"].items()):
            if findings:
                print(f"\n{marker} ({len(findings)} occurrences)")
                print("-" * 80)

                for finding in findings[:20]:  # Limit to 20 per marker
                    print(f"\n{finding['file']}:{finding['line']}")
                    print(f"  {finding['text']}")

                if len(findings) > 20:
                    print(f"\n  ... and {len(findings) - 20} more")

    else:  # group_by == "file"
        print(f"\n📁 FINDINGS BY FILE")
        print("=" * 80)

        for file_path, findings in sorted(results["by_file"].items()):
            print(f"\n{file_path} ({len(findings)} markers)")
            print("-" * 80)

            for finding in findings:
                print(f"  Line {finding['line']:>4}: {finding['marker']:<10} {finding['text']}")

    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for TODO finder.

    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Find TODO, FIXME, and other code markers"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to search (default: current directory)"
    )
    parser.add_argument(
        "--markers",
        nargs="+",
        choices=list(MARKERS.keys()),
        default=list(MARKERS.keys()),
        help="Markers to search for (default: all)"
    )
    parser.add_argument(
        "--group-by",
        choices=["marker", "file"],
        default="marker",
        help="Group results by marker type or file (default: marker)"
    )

    args = parser.parse_args()
    root = Path(args.path).resolve()

    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1

    print(f"Searching for markers in: {root}")
    print(f"Markers: {', '.join(args.markers)}")

    results = search_directory(root, set(args.markers))
    print_report(results, root, args.group_by)

    return 0


if __name__ == "__main__":
    sys.exit(main())
