#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Analysis
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/analysis/analyze_dependencies.py
VERSION: 03.00.00
BRIEF: Analyzes project dependencies across Python, npm, and composer
PATH: /scripts/analysis/analyze_dependencies.py
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


def find_files(root: Path, patterns: List[str]) -> List[Path]:
    """
    Find files matching any of the given patterns.
    
    Args:
        root: Root directory to search
        patterns: List of filename patterns to match
        
    Returns:
        List of matching file paths
    """
    matches = []
    for pattern in patterns:
        matches.extend(root.rglob(pattern))
    return matches


def analyze_python_dependencies(root: Path) -> Dict[str, List[str]]:
    """
    Analyze Python dependencies from various sources.
    
    Args:
        root: Root directory to search
        
    Returns:
        Dictionary with dependency information
    """
    deps = {
        "requirements_txt": [],
        "setup_py": [],
        "pyproject_toml": [],
        "pipfile": [],
    }
    
    # Check requirements.txt
    req_files = find_files(root, ["requirements*.txt"])
    for req_file in req_files:
        try:
            with open(req_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        deps["requirements_txt"].append(line)
        except Exception as e:
            print(f"Warning: Could not read {req_file}: {e}", file=sys.stderr)
    
    # Check setup.py
    setup_files = find_files(root, ["setup.py"])
    if setup_files:
        deps["setup_py"].append("Found setup.py (manual inspection required)")
    
    # Check pyproject.toml
    pyproject_files = find_files(root, ["pyproject.toml"])
    if pyproject_files:
        deps["pyproject_toml"].append("Found pyproject.toml (manual inspection required)")
    
    # Check Pipfile
    pipfiles = find_files(root, ["Pipfile"])
    if pipfiles:
        deps["pipfile"].append("Found Pipfile (manual inspection required)")
    
    return deps


def analyze_npm_dependencies(root: Path) -> Dict[str, Dict]:
    """
    Analyze npm dependencies from package.json files.
    
    Args:
        root: Root directory to search
        
    Returns:
        Dictionary with dependency information
    """
    deps = {
        "package_json_files": [],
        "dependencies": {},
        "dev_dependencies": {},
    }
    
    package_files = find_files(root, ["package.json"])
    for pkg_file in package_files:
        try:
            with open(pkg_file, "r") as f:
                data = json.load(f)
                deps["package_json_files"].append(str(pkg_file))
                
                if "dependencies" in data:
                    for name, version in data["dependencies"].items():
                        deps["dependencies"][name] = version
                
                if "devDependencies" in data:
                    for name, version in data["devDependencies"].items():
                        deps["dev_dependencies"][name] = version
        except Exception as e:
            print(f"Warning: Could not read {pkg_file}: {e}", file=sys.stderr)
    
    return deps


def analyze_composer_dependencies(root: Path) -> Dict[str, Dict]:
    """
    Analyze PHP composer dependencies from composer.json files.
    
    Args:
        root: Root directory to search
        
    Returns:
        Dictionary with dependency information
    """
    deps = {
        "composer_json_files": [],
        "require": {},
        "require_dev": {},
    }
    
    composer_files = find_files(root, ["composer.json"])
    for comp_file in composer_files:
        try:
            with open(comp_file, "r") as f:
                data = json.load(f)
                deps["composer_json_files"].append(str(comp_file))
                
                if "require" in data:
                    for name, version in data["require"].items():
                        deps["require"][name] = version
                
                if "require-dev" in data:
                    for name, version in data["require-dev"].items():
                        deps["require_dev"][name] = version
        except Exception as e:
            print(f"Warning: Could not read {comp_file}: {e}", file=sys.stderr)
    
    return deps


def check_outdated_packages(root: Path, package_manager: str) -> Optional[str]:
    """
    Check for outdated packages using package manager commands.
    
    Args:
        root: Root directory
        package_manager: Package manager to check (pip, npm, composer)
        
    Returns:
        Output from outdated check command or None
    """
    commands = {
        "pip": ["pip", "list", "--outdated"],
        "npm": ["npm", "outdated"],
        "composer": ["composer", "outdated"],
    }
    
    if package_manager not in commands:
        return None
    
    try:
        result = subprocess.run(
            commands[package_manager],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 or result.stdout:
            return result.stdout
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def print_report(python_deps: Dict, npm_deps: Dict, composer_deps: Dict) -> None:
    """
    Print a formatted dependency report.
    
    Args:
        python_deps: Python dependency data
        npm_deps: npm dependency data
        composer_deps: Composer dependency data
    """
    print("\n" + "=" * 80)
    print("DEPENDENCY ANALYSIS REPORT")
    print("=" * 80)
    
    # Python dependencies
    print("\n📦 PYTHON DEPENDENCIES")
    print("-" * 80)
    total_python = sum(len(v) for v in python_deps.values() if isinstance(v, list))
    if total_python > 0:
        if python_deps["requirements_txt"]:
            print(f"\nrequirements.txt ({len(python_deps['requirements_txt'])} packages):")
            for dep in sorted(set(python_deps["requirements_txt"]))[:10]:
                print(f"  - {dep}")
            if len(python_deps["requirements_txt"]) > 10:
                print(f"  ... and {len(python_deps['requirements_txt']) - 10} more")
        
        for key in ["setup_py", "pyproject_toml", "pipfile"]:
            if python_deps[key]:
                print(f"\n{key.replace('_', '.')}: {python_deps[key][0]}")
    else:
        print("  No Python dependencies found")
    
    # npm dependencies
    print("\n📦 NPM DEPENDENCIES")
    print("-" * 80)
    if npm_deps["package_json_files"]:
        print(f"\nFound {len(npm_deps['package_json_files'])} package.json file(s)")
        print(f"Dependencies: {len(npm_deps['dependencies'])}")
        print(f"Dev Dependencies: {len(npm_deps['dev_dependencies'])}")
        
        if npm_deps["dependencies"]:
            print("\nProduction Dependencies (top 10):")
            for name, version in sorted(list(npm_deps["dependencies"].items()))[:10]:
                print(f"  - {name}: {version}")
            if len(npm_deps["dependencies"]) > 10:
                print(f"  ... and {len(npm_deps['dependencies']) - 10} more")
    else:
        print("  No npm dependencies found")
    
    # Composer dependencies
    print("\n📦 COMPOSER DEPENDENCIES")
    print("-" * 80)
    if composer_deps["composer_json_files"]:
        print(f"\nFound {len(composer_deps['composer_json_files'])} composer.json file(s)")
        print(f"Required: {len(composer_deps['require'])}")
        print(f"Dev Required: {len(composer_deps['require_dev'])}")
        
        if composer_deps["require"]:
            print("\nRequired Packages (top 10):")
            for name, version in sorted(list(composer_deps["require"].items()))[:10]:
                print(f"  - {name}: {version}")
            if len(composer_deps["require"]) > 10:
                print(f"  ... and {len(composer_deps['require']) - 10} more")
    else:
        print("  No composer dependencies found")
    
    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for dependency analyzer.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Analyze project dependencies across Python, npm, and composer"
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
    parser.add_argument(
        "--check-outdated",
        action="store_true",
        help="Check for outdated packages (requires package managers installed)"
    )
    
    args = parser.parse_args()
    root = Path(args.path).resolve()
    
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1
    
    print(f"Analyzing dependencies in: {root}")
    
    # Analyze dependencies
    python_deps = analyze_python_dependencies(root)
    npm_deps = analyze_npm_dependencies(root)
    composer_deps = analyze_composer_dependencies(root)
    
    if args.json:
        # Output as JSON
        result = {
            "python": python_deps,
            "npm": npm_deps,
            "composer": composer_deps,
        }
        print(json.dumps(result, indent=2))
    else:
        # Output as formatted report
        print_report(python_deps, npm_deps, composer_deps)
    
    # Check for outdated packages if requested
    if args.check_outdated:
        print("\n📊 CHECKING FOR OUTDATED PACKAGES")
        print("=" * 80)
        
        for pm in ["pip", "npm", "composer"]:
            outdated = check_outdated_packages(root, pm)
            if outdated:
                print(f"\n{pm.upper()} outdated packages:")
                print(outdated)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
