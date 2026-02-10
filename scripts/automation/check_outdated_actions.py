#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Automation
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/automation/check_outdated_actions.py
VERSION: 03.01.03
BRIEF: Checks for outdated GitHub Actions in workflow files
PATH: /scripts/automation/check_outdated_actions.py
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def extract_actions(workflow_file: Path) -> List[Tuple[str, str]]:
    """
    Extract GitHub Actions from a workflow file.

    Args:
        workflow_file: Path to workflow YAML file

    Returns:
        List of (action_name, version) tuples
    """
    actions = []

    try:
        with open(workflow_file, "r") as f:
            for line in f:
                # Match "uses: owner/repo@version"
                match = re.search(r'uses:\s+([^@\s]+)@([^\s]+)', line)
                if match:
                    action_name = match.group(1)
                    version = match.group(2)
                    actions.append((action_name, version))
    except Exception as e:
        print(f"Warning: Could not read {workflow_file}: {e}", file=sys.stderr)

    return actions


def analyze_workflows(workflow_dir: Path) -> Dict[str, List[Tuple[str, Set[str]]]]:
    """
    Analyze all workflow files for GitHub Actions.

    Args:
        workflow_dir: Directory containing workflow files

    Returns:
        Dictionary mapping workflow file to list of (action, versions) tuples
    """
    results = {}

    if not workflow_dir.exists():
        return results

    for workflow_file in workflow_dir.glob("*.yml"):
        actions = extract_actions(workflow_file)
        if actions:
            results[str(workflow_file)] = actions

    for workflow_file in workflow_dir.glob("*.yaml"):
        actions = extract_actions(workflow_file)
        if actions:
            results[str(workflow_file)] = actions

    return results


def aggregate_actions(results: Dict[str, List[Tuple[str, str]]]) -> Dict[str, Set[str]]:
    """
    Aggregate all actions and their versions across workflows.

    Args:
        results: Dictionary of workflow results

    Returns:
        Dictionary mapping action name to set of versions used
    """
    action_versions = {}

    for workflow_file, actions in results.items():
        for action_name, version in actions:
            if action_name not in action_versions:
                action_versions[action_name] = set()
            action_versions[action_name].add(version)

    return action_versions


def identify_sha_versions(action_versions: Dict[str, Set[str]]) -> Dict[str, List[str]]:
    """
    Identify actions using SHA versions instead of semantic versions.

    Args:
        action_versions: Dictionary of actions and their versions

    Returns:
        Dictionary of actions using SHA versions
    """
    sha_pattern = re.compile(r'^[0-9a-f]{40}$')
    sha_versions = {}

    for action, versions in action_versions.items():
        sha_list = [v for v in versions if sha_pattern.match(v)]
        if sha_list:
            sha_versions[action] = sha_list

    return sha_versions


def identify_multiple_versions(action_versions: Dict[str, Set[str]]) -> Dict[str, List[str]]:
    """
    Identify actions with multiple versions in use.

    Args:
        action_versions: Dictionary of actions and their versions

    Returns:
        Dictionary of actions with multiple versions
    """
    multiple = {}

    for action, versions in action_versions.items():
        if len(versions) > 1:
            multiple[action] = sorted(versions)

    return multiple


# Known latest versions of popular actions (as of early 2024)
KNOWN_LATEST = {
    "actions/checkout": "v4",
    "actions/setup-python": "v5",
    "actions/setup-node": "v4",
    "actions/cache": "v4",
    "actions/upload-artifact": "v4",
    "actions/download-artifact": "v4",
    "github/codeql-action/init": "v3",
    "github/codeql-action/analyze": "v3",
    "github/codeql-action/autobuild": "v3",
}


def check_known_outdated(action_versions: Dict[str, Set[str]]) -> Dict[str, Tuple[List[str], str]]:
    """
    Check for known outdated action versions.

    Args:
        action_versions: Dictionary of actions and their versions

    Returns:
        Dictionary of outdated actions with (current_versions, latest_version)
    """
    outdated = {}

    for action, versions in action_versions.items():
        if action in KNOWN_LATEST:
            latest = KNOWN_LATEST[action]
            current = sorted(versions)

            # Check if any version is different from latest
            if latest not in versions or len(versions) > 1:
                outdated[action] = (current, latest)

    return outdated


def print_report(results: Dict, action_versions: Dict) -> None:
    """
    Print analysis report.

    Args:
        results: Workflow analysis results
        action_versions: Aggregated action versions
    """
    print("\n" + "=" * 80)
    print("GITHUB ACTIONS ANALYSIS REPORT")
    print("=" * 80)

    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Workflow files analyzed: {len(results)}")
    print(f"Unique actions found:    {len(action_versions)}")

    # Check for multiple versions
    multiple = identify_multiple_versions(action_versions)
    if multiple:
        print(f"\n⚠️  ACTIONS WITH MULTIPLE VERSIONS")
        print("-" * 80)
        for action, versions in sorted(multiple.items()):
            print(f"\n{action}")
            for version in versions:
                print(f"  - {version}")

    # Check for SHA versions
    sha_versions = identify_sha_versions(action_versions)
    if sha_versions:
        print(f"\n🔒 ACTIONS USING SHA VERSIONS")
        print("-" * 80)
        for action, versions in sorted(sha_versions.items()):
            print(f"{action}")
            for version in versions:
                print(f"  - {version}")

    # Check for known outdated versions
    outdated = check_known_outdated(action_versions)
    if outdated:
        print(f"\n⏰ POTENTIALLY OUTDATED ACTIONS")
        print("-" * 80)
        for action, (current, latest) in sorted(outdated.items()):
            print(f"\n{action}")
            print(f"  Current: {', '.join(current)}")
            print(f"  Latest:  {latest}")

    # List all actions
    print(f"\n📦 ALL ACTIONS")
    print("-" * 80)
    for action, versions in sorted(action_versions.items()):
        versions_str = ", ".join(sorted(versions))
        print(f"{action:<40} {versions_str}")

    print("\n" + "=" * 80)
    print("\n💡 RECOMMENDATIONS")
    print("-" * 80)
    print("1. Review actions with multiple versions for consistency")
    print("2. Consider updating outdated actions to latest versions")
    print("3. SHA versions are secure but harder to update - consider semantic versions")
    print("4. Check the GitHub Marketplace for latest action versions")
    print("5. Test updated actions in a development branch before merging")
    print()


def main() -> int:
    """
    Main entry point for action checker.

    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Check for outdated GitHub Actions in workflow files"
    )
    parser.add_argument(
        "--workflow-dir",
        default=".github/workflows",
        help="Directory containing workflow files (default: .github/workflows)"
    )

    args = parser.parse_args()
    workflow_dir = Path(args.workflow_dir)

    if not workflow_dir.exists():
        print(f"Error: Workflow directory not found: {workflow_dir}", file=sys.stderr)
        return 1

    print(f"Analyzing workflows in: {workflow_dir}")

    # Analyze workflows
    results = analyze_workflows(workflow_dir)

    if not results:
        print("No workflow files found")
        return 0

    # Aggregate actions
    action_versions = aggregate_actions(results)

    # Print report
    print_report(results, action_versions)

    return 0


if __name__ == "__main__":
    sys.exit(main())
