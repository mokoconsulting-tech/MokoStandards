#!/usr/bin/env python3
"""
Analyze pull request merge conflicts with the main branch and provide resolution
guidance.

This module uses the GitHub CLI (`gh`) to list open pull requests, inspects their
mergeability status, and classifies likely conflict types based on PR metadata
(such as the title). The analysis is printed to standard output and is intended
to help maintainers quickly see which PRs are blocked by conflicts and how they
might be resolved.

Usage:
    python scripts/analysis/analyze_pr_conflicts.py

By default, the script queries up to 100 open pull requests. You can override
this limit with the ``PR_LIMIT`` environment variable:

    PR_LIMIT=200 python scripts/analysis/analyze_pr_conflicts.py

Requirements:
* GitHub CLI (`gh`) must be installed and authenticated for the current
  repository.
* Network access to GitHub is required for querying pull requests.

The script exits with the same status code as the underlying GitHub CLI command
when fetching pull requests fails, and will emit diagnostic information to
standard error in that case.
"""

import subprocess
import json
import sys
import os
from typing import List, Dict, Tuple, Optional
import re

def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr.

    On failure, prints additional context (command, exit code, stderr) to stderr
    to aid in diagnosing subprocess issues.
    """
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # Provide meaningful error context while preserving existing behavior.
        joined_cmd = " ".join(cmd)
        print(
            f"Command failed (exit code {result.returncode}): {joined_cmd}\n"
            f"stderr:\n{result.stderr}",
            file=sys.stderr,
        )
    return result.returncode, result.stdout, result.stderr

def get_pr_limit() -> str:
    """Return the PR fetch limit as a string, configurable via PR_LIMIT env var."""
    env_limit = os.getenv("PR_LIMIT")
    if env_limit is not None:
        try:
            value = int(env_limit)
            if value > 0:
                return str(value)
            else:
                print(f"Warning: PR_LIMIT={env_limit} is not positive, using default (100)", file=sys.stderr)
        except ValueError:
            # Fall back to default if env var is not a valid integer
            print(f"Warning: PR_LIMIT={env_limit} is not a valid integer, using default (100)", file=sys.stderr)
    # Default limit matches previous behavior
    return "100"

def get_open_prs() -> Tuple[List[Dict], Optional[Dict]]:
    """Fetch list of open PRs using GitHub CLI.

    Returns a tuple (prs, error_info) where prs is the list of PRs (possibly empty)
    and error_info is a dict with keys 'exit_code' and 'stderr' if the command
    failed, or None on success.
    """
    code, stdout, stderr = run_command([
        'gh', 'pr', 'list',
        '--json', 'number,title,headRefName,baseRefName,mergeable,mergeStateStatus',
        '--limit', get_pr_limit()
    ])

    if code != 0:
        return [], {"exit_code": code, "stderr": stderr.strip()}

    try:
        prs = json.loads(stdout)
    except json.JSONDecodeError as e:
        return [], {
            "exit_code": code,
            "stderr": f"Failed to parse GitHub CLI output as JSON: {e}"
        }

    return prs, None

# Compile regex patterns once at module level for efficiency
_TEMPLATE_PATTERN = re.compile(r'\btemplate(s)?\b', re.IGNORECASE)
_HEADER_PATTERN = re.compile(r'\bheader(s)?\b', re.IGNORECASE)
_AUTOMATION_PATTERN = re.compile(r'\bautomation\b', re.IGNORECASE)
_SCRIPT_PATTERN = re.compile(r'\bscript(s)?\b', re.IGNORECASE)

def classify_pr_conflict_types(pr: Dict) -> Dict[str, bool]:
    """Classify likely conflict types for a PR based on its title."""
    title = str(pr.get('title', ''))

    # Use basic word-boundary-aware patterns to reduce accidental matches.
    return {
        'template': bool(_TEMPLATE_PATTERN.search(title)),
        'header': bool(_HEADER_PATTERN.search(title)),
        'automation_or_script': bool(_AUTOMATION_PATTERN.search(title) or _SCRIPT_PATTERN.search(title)),
    }

def analyze_pr_conflicts(pr: Dict) -> Dict:
    """Analyze a specific PR for conflicts."""
    mergeable = pr.get('mergeable')
    merge_state = pr.get('mergeStateStatus', 'UNKNOWN')

    # Consider both the mergeable field and merge state status to detect conflicts.
    # - mergeable can be 'CONFLICTING', 'MERGEABLE', or None (unknown/not computed).
    # - merge_state may also indicate conflicts (e.g., 'CONFLICTING', 'DIRTY').
    has_conflicts = (
        mergeable == 'CONFLICTING'
        or merge_state in ('CONFLICTING', 'DIRTY')
    )

    analysis = {
        'pr_number': pr['number'],
        'title': pr['title'],
        'branch': pr['headRefName'],
        'base': pr['baseRefName'],
        'has_conflicts': has_conflicts,
        'merge_state': merge_state,
        'recommendations': []
    }

    # Add specific recommendations based on PR characteristics
    if analysis['has_conflicts']:
        conflict_types = classify_pr_conflict_types(pr)

        if conflict_types.get('template'):
            analysis['recommendations'].append(
                "Template conflicts: Preserve new structures, merge documentation updates"
            )
        if conflict_types.get('header'):
            analysis['recommendations'].append(
                "File header conflicts: Keep new headers, preserve functional changes"
            )
        if conflict_types.get('automation_or_script'):
            analysis['recommendations'].append(
                "Script conflicts: Test automation after merge, regenerate indexes"
            )

    return analysis

def print_analysis(analyses: List[Dict]):
    """Print formatted analysis of PR conflicts."""
    print("=" * 80)
    print("PR CONFLICT ANALYSIS")
    print("=" * 80)
    print()

    # PRs with conflicts
    conflicted = [a for a in analyses if a['has_conflicts']]
    if conflicted:
        print("PRs WITH CONFLICTS:")
        print("-" * 80)
        for analysis in conflicted:
            print(f"PR #{analysis['pr_number']}: {analysis['title']}")
            print(f"  Branch: {analysis['branch']}")
            print(f"  Base: {analysis['base']}")
            print(f"  Merge State: {analysis['merge_state']}")
            if analysis['recommendations']:
                print("  Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"    - {rec}")
            print()
    else:
        print("No PRs with conflicts found.")
        print()

    # PRs without conflicts
    clean = [a for a in analyses if not a['has_conflicts'] and a['base'] == 'main']
    if clean:
        print("PRs WITHOUT CONFLICTS (targeting main):")
        print("-" * 80)
        for analysis in clean:
            print(f"PR #{analysis['pr_number']}: {analysis['title']}")
            print(f"  Branch: {analysis['branch']}")
            print(f"  Merge State: {analysis['merge_state']}")
            print()

    # PRs targeting other branches
    indirect = [a for a in analyses if a['base'] != 'main']
    if indirect:
        print("PRs TARGETING OTHER BRANCHES (not main):")
        print("-" * 80)
        for analysis in indirect:
            print(f"PR #{analysis['pr_number']}: {analysis['title']}")
            print(f"  Branch: {analysis['branch']} -> {analysis['base']}")
            print(f"  Note: Will inherit conflicts from base branch")
            print()

    print("=" * 80)
    print(f"Total PRs analyzed: {len(analyses)}")
    print(f"PRs with conflicts: {len(conflicted)}")
    print(f"PRs without conflicts: {len(clean)}")
    print(f"PRs targeting other branches: {len(indirect)}")
    print("=" * 80)
    print()
    print("For detailed resolution guidance, see: CONFLICT_RESOLUTION_GUIDE.md")

def main():
    """Main entry point."""
    print("Fetching open pull requests...", file=sys.stderr)

    prs, error = get_open_prs()
    if error is not None:
        stderr_msg = error.get("stderr", "")
        exit_code = error.get("exit_code")

        # Try to provide more specific guidance based on the failure mode.
        lower_err = stderr_msg.lower()
        print("Unable to fetch open PRs from GitHub.", file=sys.stderr)
        if "command not found" in lower_err or "executable file not found" in lower_err:
            print("GitHub CLI (gh) does not appear to be installed. "
                  "Install it and ensure it is on your PATH.", file=sys.stderr)
        elif "authenticate" in lower_err or "authorization" in lower_err or "must be logged in" in lower_err:
            print("GitHub CLI (gh) is not authenticated. Run 'gh auth login' and try again.",
                  file=sys.stderr)
        elif stderr_msg:
            print(f"gh exited with code {exit_code}. Error output:", file=sys.stderr)
            print(stderr_msg, file=sys.stderr)
            print("This may be due to network issues, repository permissions, or GitHub API problems.",
                  file=sys.stderr)
        else:
            print(f"gh exited with code {exit_code} with no additional error output.", file=sys.stderr)
        sys.exit(1)

    if not prs:
        print("No open PRs found.", file=sys.stderr)
        return

    print(f"Analyzing {len(prs)} pull requests...", file=sys.stderr)
    print()

    analyses = [analyze_pr_conflicts(pr) for pr in prs]
    print_analysis(analyses)

if __name__ == '__main__':
    main()
