#!/usr/bin/env python3
"""
Validate GitHub Actions workflow files.

Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
INGROUP: CI.Validation
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/validate/workflows.py
VERSION: 01.00.00
BRIEF: Validate GitHub Actions workflow files
NOTE: Checks YAML syntax, structure, and best practices
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    sys.exit(1)


def validate_yaml_syntax(filepath: Path) -> bool:
    """
    Validate YAML syntax of a workflow file.

    Args:
        filepath: Path to workflow file

    Returns:
        True if valid
    """
    try:
        import yaml
    except ImportError:
        common.log_warning("PyYAML module not installed. Install with: pip3 install pyyaml")
        return True  # Skip validation if yaml not available

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        common.log_success(f"Valid YAML: {filepath.name}")
        return True
    except yaml.YAMLError as e:
        common.log_error(f"YAML Error in {filepath.name}: {e}")
        return False
    except Exception as e:
        common.log_error(f"Error reading {filepath.name}: {e}")
        return False


def check_no_tabs(filepath: Path) -> bool:
    """
    Check that file contains no tab characters.

    Args:
        filepath: Path to file

    Returns:
        True if no tabs found
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if '\t' in content:
                common.log_error(f"✗ File contains tab characters: {filepath.name}")
                return False
    except Exception as e:
        common.log_warn(f"Could not read {filepath}: {e}")
        return False

    return True


def check_workflow_structure(filepath: Path) -> bool:
    """
    Check workflow file structure for required keys.

    Args:
        filepath: Path to workflow file

    Returns:
        True if structure is valid
    """
    errors = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required top-level keys
        if 'name:' not in content and not content.startswith('name:'):
            common.log_warn(f"Missing 'name:' in {filepath.name}")

        if 'on:' not in content and not content.startswith('on:'):
            common.log_error(f"✗ Missing 'on:' trigger in {filepath.name}")
            errors += 1

        if 'jobs:' not in content and not content.startswith('jobs:'):
            common.log_error(f"✗ Missing 'jobs:' in {filepath.name}")
            errors += 1

    except Exception as e:
        common.log_error(f"Error reading {filepath}: {e}")
        return False

    return errors == 0


def validate_workflow_file(filepath: Path) -> bool:
    """
    Validate a single workflow file.

    Args:
        filepath: Path to workflow file

    Returns:
        True if valid
    """
    common.log_info(f"Validating: {filepath.name}")

    errors = 0

    # Check YAML syntax
    if not validate_yaml_syntax(filepath):
        errors += 1

    # Check for tabs
    if not check_no_tabs(filepath):
        errors += 1

    # Check structure
    if not check_workflow_structure(filepath):
        errors += 1

    if errors == 0:
        common.log_info(f"✓ {filepath.name} passed all checks")
        return True
    else:
        common.log_error(f"✗ {filepath.name} failed {errors} check(s)")
        return False


def main() -> int:
    """Main entry point."""
    common.log_info("GitHub Actions Workflow Validation")
    common.log_info("===================================")
    print()

    workflows_dir = Path(".github/workflows")

    if not workflows_dir.is_dir():
        common.log_error(f"Workflows directory not found: {workflows_dir}")
        return 1

    # Find all workflow files
    workflow_files = []
    for pattern in ["*.yml", "*.yaml"]:
        workflow_files.extend(workflows_dir.glob(pattern))

    if not workflow_files:
        common.log_warn("No workflow files found")
        return 0

    total = len(workflow_files)
    passed = 0
    failed = 0

    for workflow in workflow_files:
        if validate_workflow_file(workflow):
            passed += 1
        else:
            failed += 1
        print()

    common.log_info("===================================")
    common.log_info("Summary:")
    common.log_info(f"  Total workflows: {total}")
    common.log_info(f"  Passed: {passed}")
    common.log_info(f"  Failed: {failed}")
    common.log_info("===================================")

    if failed > 0:
        common.log_error("Workflow validation failed")
        return 1

    common.log_info("All workflows validated successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
