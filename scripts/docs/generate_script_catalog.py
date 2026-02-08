#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Docs
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/docs/generate_script_catalog.py
VERSION: 03.01.01
BRIEF: Generates a comprehensive catalog of all scripts in the repository
PATH: /scripts/docs/generate_script_catalog.py
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def extract_script_info(script_path: Path) -> Dict:
    """
    Extract metadata from a script file.

    Args:
        script_path: Path to script file

    Returns:
        Dictionary with script metadata
    """
    info = {
        "name": script_path.name,
        "path": str(script_path),
        "brief": None,
        "description": None,
        "file_info": {},
    }

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read(2000)  # Read first 2000 chars

            # Extract docstring (Python)
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if docstring_match:
                docstring = docstring_match.group(1)

                # Extract BRIEF
                brief_match = re.search(r'BRIEF:\s*(.+)', docstring)
                if brief_match:
                    info["brief"] = brief_match.group(1).strip()

                # Extract FILE
                file_match = re.search(r'FILE:\s*(.+)', docstring)
                if file_match:
                    info["file_info"]["file"] = file_match.group(1).strip()

                # Extract VERSION
                version_match = re.search(r'VERSION:\s*(.+)', docstring)
                if version_match:
                    info["file_info"]["version"] = version_match.group(1).strip()

                # Extract DEFGROUP
                defgroup_match = re.search(r'DEFGROUP:\s*(.+)', docstring)
                if defgroup_match:
                    info["file_info"]["defgroup"] = defgroup_match.group(1).strip()

            # Extract description from comments (for shell scripts)
            if not info["brief"]:
                desc_match = re.search(r'#\s*Description:\s*(.+)', content, re.IGNORECASE)
                if desc_match:
                    info["brief"] = desc_match.group(1).strip()

    except Exception as e:
        # File might be binary or have encoding issues, return partial info
        import sys
        print(f"Warning: Failed to fully parse {script_path}: {e}", file=sys.stderr)

    return info


def scan_scripts_directory(scripts_dir: Path) -> Dict[str, List[Dict]]:
    """
    Scan the scripts directory and organize scripts by category.

    Args:
        scripts_dir: Path to scripts directory

    Returns:
        Dictionary mapping category to list of script info
    """
    categories = {}

    # Scan all subdirectories
    for category_dir in scripts_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith("."):
            category_name = category_dir.name
            scripts = []

            # Find all script files
            for ext in [".py", ".sh", ".ps1", ".bash"]:
                for script_path in category_dir.glob(f"*{ext}"):
                    if script_path.is_file():
                        info = extract_script_info(script_path)
                        scripts.append(info)

            if scripts:
                categories[category_name] = sorted(scripts, key=lambda x: x["name"])

    return categories


def generate_markdown_catalog(categories: Dict[str, List[Dict]], output_path: Optional[Path] = None) -> str:
    """
    Generate markdown catalog of scripts.

    Args:
        categories: Dictionary of categorized scripts
        output_path: Optional path to write output file

    Returns:
        Markdown content
    """
    lines = []

    # Header
    lines.append("# MokoStandards Script Catalog")
    lines.append("")
    lines.append("This document provides a comprehensive catalog of all automation scripts in the repository.")
    lines.append("")
    lines.append(f"**Generated:** {Path('.').resolve().name}")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    for category in sorted(categories.keys()):
        lines.append(f"- [{category.title()}](#{category})")
    lines.append("")

    # Script count summary
    total_scripts = sum(len(scripts) for scripts in categories.values())
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Total Scripts:** {total_scripts}")
    lines.append("")
    lines.append("**By Category:**")
    for category, scripts in sorted(categories.items()):
        lines.append(f"- {category.title()}: {len(scripts)} scripts")
    lines.append("")

    # Detailed listing by category
    for category, scripts in sorted(categories.items()):
        lines.append(f"## {category.title()}")
        lines.append("")

        for script in scripts:
            lines.append(f"### {script['name']}")
            lines.append("")

            if script.get("brief"):
                lines.append(f"**Description:** {script['brief']}")
                lines.append("")

            lines.append(f"**Path:** `{script['path']}`")
            lines.append("")

            if script.get("file_info"):
                if script["file_info"].get("version"):
                    lines.append(f"**Version:** {script['file_info']['version']}")
                if script["file_info"].get("defgroup"):
                    lines.append(f"**Group:** {script['file_info']['defgroup']}")
                lines.append("")

            # Usage placeholder
            lines.append("**Usage:**")
            lines.append("```bash")

            if script["name"].endswith(".py"):
                lines.append(f"python3 {script['path']} --help")
            elif script["name"].endswith((".sh", ".bash")):
                lines.append(f"bash {script['path']} --help")
            elif script["name"].endswith(".ps1"):
                lines.append(f"powershell {script['path']} -Help")

            lines.append("```")
            lines.append("")

    content = "\n".join(lines)

    # Write to file if path provided
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Catalog written to: {output_path}")
        except Exception as e:
            print(f"Error writing to {output_path}: {e}", file=sys.stderr)

    return content


def main() -> int:
    """
    Main entry point for script catalog generator.

    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Generate a comprehensive catalog of all scripts"
    )
    parser.add_argument(
        "--scripts-dir",
        default="scripts",
        help="Path to scripts directory (default: scripts)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: print to stdout)"
    )

    args = parser.parse_args()
    scripts_dir = Path(args.scripts_dir)

    if not scripts_dir.exists():
        print(f"Error: Scripts directory not found: {scripts_dir}", file=sys.stderr)
        return 1

    print(f"Scanning scripts in: {scripts_dir}")

    # Scan scripts
    categories = scan_scripts_directory(scripts_dir)

    if not categories:
        print("No scripts found")
        return 0

    # Generate catalog
    output_path = Path(args.output) if args.output else None
    content = generate_markdown_catalog(categories, output_path)

    # Print to stdout if no output file specified
    if not output_path:
        print("\n" + "=" * 80)
        print(content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
