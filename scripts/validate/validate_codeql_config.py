#!/usr/bin/env python3
"""
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
along with this program. If not, see <https://www.gnu.org/licenses/>.

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Validate
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/validate/validate_codeql_config.py
VERSION: 03.01.03
BRIEF: Validates CodeQL workflow language configuration matches repository contents
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# Language to file extension mapping
LANGUAGE_EXTENSIONS = {
    'python': {'.py'},
    'javascript': {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'},
    'php': {'.php'},
    'java': {'.java'},
    'go': {'.go'},
    'ruby': {'.rb'},
    'cpp': {'.cpp', '.cc', '.cxx', '.c', '.h', '.hpp'},
    'csharp': {'.cs'},
}


def detect_languages_in_repo(repo_path: Path, exclude_dirs: Set[str] = None) -> Dict[str, int]:
    """
    Detect programming languages present in the repository by scanning file extensions.

    Args:
        repo_path: Path to the repository root
        exclude_dirs: Set of directory names to exclude from scanning

    Returns:
        Dictionary mapping language names to file counts
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'vendor', 'node_modules', '.venv', 'venv', '__pycache__'}

    language_counts = {}

    for language, extensions in LANGUAGE_EXTENSIONS.items():
        count = 0
        for ext in extensions:
            for file_path in repo_path.rglob(f'*{ext}'):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                if file_path.is_file():
                    count += 1

        if count > 0:
            language_counts[language] = count

    return language_counts


def parse_codeql_workflow(workflow_path: Path) -> Tuple[List[str], bool]:
    """
    Parse CodeQL workflow file and extract configured languages.

    Args:
        workflow_path: Path to the CodeQL workflow YAML file

    Returns:
        Tuple of (list of configured languages, whether parsing succeeded)
    """
    try:
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        # Navigate to the matrix.language configuration
        jobs = workflow.get('jobs', {})
        for job_name, job_config in jobs.items():
            strategy = job_config.get('strategy', {})
            matrix = strategy.get('matrix', {})
            languages = matrix.get('language', [])

            if languages:
                return languages, True

        return [], False
    except Exception as e:
        print(f"Error parsing workflow: {e}", file=sys.stderr)
        return [], False


def validate_codeql_config(repo_path: Path, workflow_path: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate that CodeQL workflow languages match repository contents.

    Args:
        repo_path: Path to the repository root
        workflow_path: Path to the CodeQL workflow file

    Returns:
        Tuple of (is_valid, list of errors, list of warnings)
    """
    errors = []
    warnings = []

    # Check if workflow file exists
    if not workflow_path.exists():
        errors.append(f"CodeQL workflow not found at: {workflow_path}")
        return False, errors, warnings

    # Detect languages in repository
    detected_languages = detect_languages_in_repo(repo_path)

    if not detected_languages:
        warnings.append("No supported programming languages detected in repository")
        return True, errors, warnings

    # Parse CodeQL workflow configuration
    configured_languages, parse_success = parse_codeql_workflow(workflow_path)

    if not parse_success:
        errors.append("Could not find language configuration in CodeQL workflow")
        return False, errors, warnings

    if not configured_languages:
        errors.append("No languages configured in CodeQL workflow matrix")
        return False, errors, warnings

    # Compare detected vs configured languages
    detected_set = set(detected_languages.keys())
    configured_set = set(configured_languages)

    # Languages configured but not present in repo
    extra_languages = configured_set - detected_set
    if extra_languages:
        for lang in extra_languages:
            errors.append(
                f"Language '{lang}' is configured in CodeQL but no {lang.upper()} files found in repository. "
                f"This will cause CodeQL analysis to fail."
            )

    # Languages present but not configured
    missing_languages = detected_set - configured_set
    if missing_languages:
        for lang in missing_languages:
            file_count = detected_languages[lang]
            warnings.append(
                f"Language '{lang}' has {file_count} files in repository but is not configured in CodeQL workflow. "
                f"Consider adding it for security scanning."
            )

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description='Validate CodeQL workflow language configuration against repository contents'
    )
    parser.add_argument(
        '--repo-path',
        type=Path,
        default=Path('.'),
        help='Path to repository root (default: current directory)'
    )
    parser.add_argument(
        '--workflow-path',
        type=Path,
        help='Path to CodeQL workflow file (default: .github/workflows/codeql-analysis.yml)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    repo_path = args.repo_path.resolve()
    workflow_path = args.workflow_path

    if workflow_path is None:
        workflow_path = repo_path / '.github' / 'workflows' / 'codeql-analysis.yml'
    else:
        workflow_path = workflow_path.resolve()

    print(f"Validating CodeQL configuration...")
    print(f"Repository: {repo_path}")
    print(f"Workflow: {workflow_path}")
    print()

    # Detect languages first for informational purposes
    detected_languages = detect_languages_in_repo(repo_path)
    if detected_languages:
        print("Detected languages in repository:")
        for lang, count in sorted(detected_languages.items()):
            print(f"  - {lang}: {count} files")
        print()

    # Validate configuration
    is_valid, errors, warnings = validate_codeql_config(repo_path, workflow_path)

    # Print results
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()

    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    if is_valid and not warnings:
        print("✅ CodeQL configuration is valid and matches repository contents")
        return 0
    elif is_valid:
        print("✅ CodeQL configuration is valid (with warnings)")
        if args.strict:
            print("❌ Strict mode enabled: treating warnings as errors")
            return 1
        return 0
    else:
        print("❌ CodeQL configuration validation failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
