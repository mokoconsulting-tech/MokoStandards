#!/usr/bin/env python3
"""
Analyze PR conflicts with main branch and provide resolution guidance.

This script analyzes open pull requests to identify which have merge conflicts
with the main branch and provides specific guidance for resolving them.
"""

import subprocess
import json
import sys
from typing import List, Dict

def run_command(cmd: List[str]) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def get_open_prs() -> List[Dict]:
    """Fetch list of open PRs using GitHub CLI."""
    code, stdout, stderr = run_command([
        'gh', 'pr', 'list',
        '--json', 'number,title,headRefName,baseRefName,mergeable,mergeStateStatus',
        '--limit', '100'
    ])
    
    if code != 0:
        print(f"Error fetching PRs: {stderr}", file=sys.stderr)
        return []
    
    return json.loads(stdout)

def analyze_pr_conflicts(pr: Dict) -> Dict:
    """Analyze a specific PR for conflicts."""
    analysis = {
        'pr_number': pr['number'],
        'title': pr['title'],
        'branch': pr['headRefName'],
        'base': pr['baseRefName'],
        'has_conflicts': pr.get('mergeable') == 'CONFLICTING',
        'merge_state': pr.get('mergeStateStatus', 'UNKNOWN'),
        'recommendations': []
    }
    
    # Add specific recommendations based on PR characteristics
    if analysis['has_conflicts']:
        if 'template' in pr['title'].lower():
            analysis['recommendations'].append(
                "Template conflicts: Preserve new structures, merge documentation updates"
            )
        if 'header' in pr['title'].lower():
            analysis['recommendations'].append(
                "File header conflicts: Keep new headers, preserve functional changes"
            )
        if 'automation' in pr['title'].lower() or 'script' in pr['title'].lower():
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
    
    prs = get_open_prs()
    if not prs:
        print("No open PRs found or unable to fetch PRs.", file=sys.stderr)
        print("Make sure GitHub CLI (gh) is installed and authenticated.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Analyzing {len(prs)} pull requests...", file=sys.stderr)
    print()
    
    analyses = [analyze_pr_conflicts(pr) for pr in prs]
    print_analysis(analyses)

if __name__ == '__main__':
    main()
