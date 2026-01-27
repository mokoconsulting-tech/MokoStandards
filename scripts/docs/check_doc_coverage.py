#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Docs
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/docs/check_doc_coverage.py
VERSION: 02.00.00
BRIEF: Checks documentation coverage by identifying undocumented scripts and templates
PATH: /scripts/docs/check_doc_coverage.py
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set


def find_documentation_files(docs_dir: Path) -> Set[str]:
    """
    Find all documentation markdown files.
    
    Args:
        docs_dir: Documentation directory
        
    Returns:
        Set of documented topics/files
    """
    documented = set()
    
    if not docs_dir.exists():
        return documented
    
    for md_file in docs_dir.rglob("*.md"):
        # Add the file's name without extension
        documented.add(md_file.stem.lower())
        
        # Also extract topics mentioned in the file
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read().lower()
                # Extract code references, script names, etc.
                # This is a simple heuristic
                for line in content.split("\n"):
                    if "script" in line or "template" in line:
                        words = line.split()
                        for word in words:
                            if word.endswith(".py") or word.endswith(".sh"):
                                documented.add(word.lower())
        except Exception:
            pass
    
    return documented


def find_scripts(scripts_dir: Path) -> List[Path]:
    """
    Find all script files.
    
    Args:
        scripts_dir: Scripts directory
        
    Returns:
        List of script paths
    """
    scripts = []
    
    if not scripts_dir.exists():
        return scripts
    
    for ext in [".py", ".sh", ".ps1", ".bash"]:
        scripts.extend(scripts_dir.rglob(f"*{ext}"))
    
    return [s for s in scripts if not any(part.startswith(".") for part in s.parts)]


def find_templates(templates_dir: Path) -> List[Path]:
    """
    Find all template files.
    
    Args:
        templates_dir: Templates directory
        
    Returns:
        List of template paths
    """
    templates = []
    
    if not templates_dir.exists():
        return templates
    
    # Common template extensions
    for ext in [".template", ".yml", ".yaml", ".xml", ".json"]:
        templates.extend(templates_dir.rglob(f"*{ext}"))
    
    return templates


def check_documentation_coverage(root: Path) -> Dict:
    """
    Check documentation coverage.
    
    Args:
        root: Root directory
        
    Returns:
        Dictionary with coverage analysis
    """
    results = {
        "scripts": {
            "total": 0,
            "documented": 0,
            "undocumented": [],
        },
        "templates": {
            "total": 0,
            "documented": 0,
            "undocumented": [],
        },
        "readmes": {
            "present": [],
            "missing": [],
        }
    }
    
    docs_dir = root / "docs"
    scripts_dir = root / "scripts"
    templates_dir = root / "templates"
    
    # Find documented items
    documented = find_documentation_files(docs_dir)
    
    # Check scripts
    scripts = find_scripts(scripts_dir)
    results["scripts"]["total"] = len(scripts)
    
    for script in scripts:
        script_name = script.name.lower()
        if script_name not in documented:
            results["scripts"]["undocumented"].append(str(script.relative_to(root)))
        else:
            results["scripts"]["documented"] += 1
    
    # Check templates
    templates = find_templates(templates_dir)
    results["templates"]["total"] = len(templates)
    
    for template in templates:
        template_name = template.name.lower()
        if template_name not in documented:
            results["templates"]["undocumented"].append(str(template.relative_to(root)))
        else:
            results["templates"]["documented"] += 1
    
    # Check for README files in subdirectories
    for directory in [scripts_dir, templates_dir]:
        if directory.exists():
            for subdir in directory.iterdir():
                if subdir.is_dir() and not subdir.name.startswith("."):
                    readme_path = subdir / "README.md"
                    index_path = subdir / "index.md"
                    
                    if readme_path.exists() or index_path.exists():
                        results["readmes"]["present"].append(str(subdir.relative_to(root)))
                    else:
                        results["readmes"]["missing"].append(str(subdir.relative_to(root)))
    
    return results


def print_report(results: Dict, root: Path) -> None:
    """
    Print documentation coverage report.
    
    Args:
        results: Coverage analysis results
        root: Root directory
    """
    print("\n" + "=" * 80)
    print("DOCUMENTATION COVERAGE REPORT")
    print("=" * 80)
    print(f"\nDirectory: {root}")
    
    # Scripts coverage
    print(f"\n📜 SCRIPTS COVERAGE")
    print("-" * 80)
    print(f"Total scripts:        {results['scripts']['total']}")
    print(f"Documented:           {results['scripts']['documented']}")
    print(f"Undocumented:         {len(results['scripts']['undocumented'])}")
    
    if results['scripts']['total'] > 0:
        coverage = (results['scripts']['documented'] / results['scripts']['total']) * 100
        print(f"Coverage:             {coverage:.1f}%")
    
    if results['scripts']['undocumented']:
        print(f"\nUndocumented scripts (first 20):")
        for script in sorted(results['scripts']['undocumented'])[:20]:
            print(f"  {script}")
        if len(results['scripts']['undocumented']) > 20:
            print(f"  ... and {len(results['scripts']['undocumented']) - 20} more")
    
    # Templates coverage
    print(f"\n📄 TEMPLATES COVERAGE")
    print("-" * 80)
    print(f"Total templates:      {results['templates']['total']}")
    print(f"Documented:           {results['templates']['documented']}")
    print(f"Undocumented:         {len(results['templates']['undocumented'])}")
    
    if results['templates']['total'] > 0:
        coverage = (results['templates']['documented'] / results['templates']['total']) * 100
        print(f"Coverage:             {coverage:.1f}%")
    
    if results['templates']['undocumented']:
        print(f"\nUndocumented templates (first 20):")
        for template in sorted(results['templates']['undocumented'])[:20]:
            print(f"  {template}")
        if len(results['templates']['undocumented']) > 20:
            print(f"  ... and {len(results['templates']['undocumented']) - 20} more")
    
    # README files
    print(f"\n📖 README FILES")
    print("-" * 80)
    print(f"Directories with README: {len(results['readmes']['present'])}")
    print(f"Missing README:          {len(results['readmes']['missing'])}")
    
    if results['readmes']['missing']:
        print(f"\nDirectories missing README.md:")
        for directory in sorted(results['readmes']['missing']):
            print(f"  {directory}")
    
    # Overall summary
    print(f"\n📊 OVERALL SUMMARY")
    print("-" * 80)
    total_items = results['scripts']['total'] + results['templates']['total']
    documented_items = results['scripts']['documented'] + results['templates']['documented']
    
    if total_items > 0:
        overall_coverage = (documented_items / total_items) * 100
        print(f"Overall documentation coverage: {overall_coverage:.1f}%")
        
        if overall_coverage >= 80:
            print("✅ Good documentation coverage!")
        elif overall_coverage >= 50:
            print("⚠️  Fair documentation coverage - consider improving")
        else:
            print("❌ Poor documentation coverage - needs improvement")
    
    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for documentation coverage checker.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Check documentation coverage for scripts and templates"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to check (default: current directory)"
    )
    
    args = parser.parse_args()
    root = Path(args.path).resolve()
    
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1
    
    print(f"Checking documentation coverage in: {root}")
    
    results = check_documentation_coverage(root)
    print_report(results, root)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
