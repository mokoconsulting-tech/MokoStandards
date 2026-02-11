#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Analysis
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/analysis/code_metrics.py
VERSION: 03.02.00
BRIEF: Analyzes code metrics including lines of code, file counts, and language distribution
PATH: /scripts/analysis/code_metrics.py
"""

import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


# Language extensions mapping
LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JSX",
    ".tsx": "TSX",
    ".php": "PHP",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".pl": "Perl",
    ".sh": "Shell",
    ".bash": "Bash",
    ".zsh": "Zsh",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    ".xml": "XML",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".txt": "Text",
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
    "coverage", ".coverage",
    "tmp", "temp",
}


def should_exclude(path: Path) -> bool:
    """
    Check if a path should be excluded from analysis.

    Args:
        path: Path to check

    Returns:
        True if path should be excluded
    """
    parts = path.parts
    return any(part in EXCLUDE_DIRS for part in parts)


def count_lines(file_path: Path) -> Tuple[int, int, int]:
    """
    Count lines in a file.

    Args:
        file_path: Path to file

    Returns:
        Tuple of (total_lines, code_lines, comment_lines)
    """
    total_lines = 0
    code_lines = 0
    comment_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            in_multiline_comment = False

            for line in f:
                total_lines += 1
                stripped = line.strip()

                if not stripped:
                    continue

                # Simple comment detection (not perfect but good enough)
                if stripped.startswith(("#", "//", "--")):
                    comment_lines += 1
                elif stripped.startswith("/*") or stripped.startswith("<!--"):
                    comment_lines += 1
                    in_multiline_comment = True
                elif in_multiline_comment:
                    comment_lines += 1
                    if "*/" in stripped or "-->" in stripped:
                        in_multiline_comment = False
                else:
                    code_lines += 1
    except Exception as e:
        # If we can't read the file (binary, encoding issues), return zeros
        import sys
        print(f"Warning: Failed to analyze {file_path}: {e}", file=sys.stderr)

    return total_lines, code_lines, comment_lines


def analyze_directory(root: Path) -> Dict:
    """
    Analyze code metrics in a directory.

    Args:
        root: Root directory to analyze

    Returns:
        Dictionary with analysis results
    """
    metrics = {
        "total_files": 0,
        "total_lines": 0,
        "total_code_lines": 0,
        "total_comment_lines": 0,
        "by_language": defaultdict(lambda: {
            "files": 0,
            "lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
        }),
        "largest_files": [],
    }

    # Walk through directory
    for file_path in root.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            ext = file_path.suffix.lower()

            if ext in LANGUAGE_EXTENSIONS:
                language = LANGUAGE_EXTENSIONS[ext]
                total, code, comments = count_lines(file_path)

                metrics["total_files"] += 1
                metrics["total_lines"] += total
                metrics["total_code_lines"] += code
                metrics["total_comment_lines"] += comments

                metrics["by_language"][language]["files"] += 1
                metrics["by_language"][language]["lines"] += total
                metrics["by_language"][language]["code_lines"] += code
                metrics["by_language"][language]["comment_lines"] += comments

                # Track largest files
                metrics["largest_files"].append((file_path, total))

    # Sort largest files
    metrics["largest_files"].sort(key=lambda x: x[1], reverse=True)
    metrics["largest_files"] = metrics["largest_files"][:20]

    # Convert defaultdict to regular dict
    metrics["by_language"] = dict(metrics["by_language"])

    return metrics


def print_report(metrics: Dict, root: Path) -> None:
    """
    Print a formatted metrics report.

    Args:
        metrics: Metrics dictionary
        root: Root directory that was analyzed
    """
    print("\n" + "=" * 80)
    print("CODE METRICS REPORT")
    print("=" * 80)
    print(f"\nDirectory: {root}")

    print("\n📊 OVERALL STATISTICS")
    print("-" * 80)
    print(f"Total Files:        {metrics['total_files']:,}")
    print(f"Total Lines:        {metrics['total_lines']:,}")
    print(f"Code Lines:         {metrics['total_code_lines']:,}")
    print(f"Comment Lines:      {metrics['total_comment_lines']:,}")

    if metrics["total_lines"] > 0:
        comment_ratio = (metrics["total_comment_lines"] / metrics["total_lines"]) * 100
        print(f"Comment Ratio:      {comment_ratio:.1f}%")

    print("\n📝 BY LANGUAGE")
    print("-" * 80)

    # Sort languages by lines of code
    sorted_langs = sorted(
        metrics["by_language"].items(),
        key=lambda x: x[1]["code_lines"],
        reverse=True
    )

    print(f"{'Language':<20} {'Files':>8} {'Lines':>12} {'Code':>12} {'Comments':>12}")
    print("-" * 80)

    for language, data in sorted_langs:
        print(f"{language:<20} {data['files']:>8,} {data['lines']:>12,} "
              f"{data['code_lines']:>12,} {data['comment_lines']:>12,}")

    if metrics["largest_files"]:
        print("\n📄 LARGEST FILES (Top 10)")
        print("-" * 80)

        for file_path, lines in metrics["largest_files"][:10]:
            rel_path = file_path.relative_to(root)
            print(f"{lines:>6,} lines - {rel_path}")

    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for code metrics analyzer.

    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Analyze code metrics including lines of code and language distribution"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to analyze (default: current directory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()
    root = Path(args.path).resolve()

    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1

    if not root.is_dir():
        print(f"Error: Path is not a directory: {root}", file=sys.stderr)
        return 1

    print(f"Analyzing code metrics in: {root}")

    metrics = analyze_directory(root)

    if args.json:
        import json
        # Convert Path objects to strings for JSON serialization
        metrics["largest_files"] = [
            (str(p.relative_to(root)), lines) for p, lines in metrics["largest_files"]
        ]
        print(json.dumps(metrics, indent=2))
    else:
        print_report(metrics, root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
