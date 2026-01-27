#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Maintenance
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/maintenance/clean_old_branches.py
VERSION: 02.00.00
BRIEF: Identifies and optionally deletes old Git branches
PATH: /scripts/maintenance/clean_old_branches.py
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple


def run_git_command(args: List[str]) -> Optional[str]:
    """
    Run a git command and return output.
    
    Args:
        args: Git command arguments
        
    Returns:
        Command output or None on error
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: git command not found", file=sys.stderr)
        return None


def get_current_branch() -> Optional[str]:
    """
    Get the current branch name.
    
    Returns:
        Current branch name or None
    """
    return run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])


def get_all_branches(include_remote: bool = False) -> List[str]:
    """
    Get list of all branches.
    
    Args:
        include_remote: Include remote branches
        
    Returns:
        List of branch names
    """
    if include_remote:
        output = run_git_command(["branch", "-a"])
    else:
        output = run_git_command(["branch"])
    
    if not output:
        return []
    
    branches = []
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("*"):
            line = line[1:].strip()
        if line and not line.startswith("remotes/"):
            branches.append(line)
    
    return branches


def get_branch_last_commit_date(branch: str) -> Optional[datetime]:
    """
    Get the date of the last commit on a branch.
    
    Args:
        branch: Branch name
        
    Returns:
        Datetime of last commit or None
    """
    output = run_git_command(["log", "-1", "--format=%ct", branch])
    
    if output:
        try:
            timestamp = int(output)
            return datetime.fromtimestamp(timestamp)
        except ValueError:
            pass
    
    return None


def is_branch_merged(branch: str, into: str = "main") -> bool:
    """
    Check if a branch is merged into another branch.
    
    Args:
        branch: Branch to check
        into: Base branch (default: main)
        
    Returns:
        True if branch is merged
    """
    output = run_git_command(["branch", "--merged", into])
    
    if output:
        merged_branches = [b.strip().lstrip("* ") for b in output.split("\n")]
        return branch in merged_branches
    
    return False


def delete_branch(branch: str, force: bool = False) -> bool:
    """
    Delete a branch.
    
    Args:
        branch: Branch name to delete
        force: Force delete (use -D instead of -d)
        
    Returns:
        True if successful
    """
    flag = "-D" if force else "-d"
    output = run_git_command(["branch", flag, branch])
    return output is not None


def analyze_branches(days_old: int, base_branch: str = "main") -> dict:
    """
    Analyze branches to identify old ones.
    
    Args:
        days_old: Number of days to consider a branch old
        base_branch: Base branch for merge checks
        
    Returns:
        Dictionary with analysis results
    """
    results = {
        "current_branch": None,
        "total_branches": 0,
        "old_branches": [],
        "merged_branches": [],
        "protected_branches": [],
    }
    
    current = get_current_branch()
    results["current_branch"] = current
    
    branches = get_all_branches()
    results["total_branches"] = len(branches)
    
    # Protected branches that should never be deleted
    protected = {"main", "master", "develop", "development", current}
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    for branch in branches:
        if branch in protected:
            results["protected_branches"].append(branch)
            continue
        
        last_commit_date = get_branch_last_commit_date(branch)
        
        if last_commit_date and last_commit_date < cutoff_date:
            is_merged = is_branch_merged(branch, base_branch)
            
            branch_info = {
                "name": branch,
                "last_commit": last_commit_date.strftime("%Y-%m-%d"),
                "days_old": (datetime.now() - last_commit_date).days,
                "is_merged": is_merged,
            }
            
            results["old_branches"].append(branch_info)
            
            if is_merged:
                results["merged_branches"].append(branch_info)
    
    return results


def print_report(results: dict, days_old: int) -> None:
    """
    Print analysis report.
    
    Args:
        results: Analysis results
        days_old: Threshold for old branches
    """
    print("\n" + "=" * 80)
    print("OLD BRANCH ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\nCurrent branch: {results['current_branch']}")
    
    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Total branches:      {results['total_branches']}")
    print(f"Protected branches:  {len(results['protected_branches'])}")
    print(f"Old branches:        {len(results['old_branches'])} (>{days_old} days)")
    print(f"Merged old branches: {len(results['merged_branches'])}")
    
    if results["protected_branches"]:
        print(f"\n🛡️  PROTECTED BRANCHES (will not be deleted)")
        print("-" * 80)
        for branch in sorted(results["protected_branches"]):
            print(f"  {branch}")
    
    if results["old_branches"]:
        print(f"\n📅 OLD BRANCHES (>{days_old} days since last commit)")
        print("-" * 80)
        print(f"{'Branch':<30} {'Last Commit':<15} {'Days Old':<10} {'Merged?'}")
        print("-" * 80)
        
        for branch in sorted(results["old_branches"], key=lambda x: x["days_old"], reverse=True):
            merged_status = "✓ Yes" if branch["is_merged"] else "✗ No"
            print(f"{branch['name']:<30} {branch['last_commit']:<15} "
                  f"{branch['days_old']:<10} {merged_status}")
    else:
        print(f"\n✅ No old branches found!")
    
    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for branch cleaner.
    
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Identify and optionally delete old Git branches"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Number of days to consider a branch old (default: 90)"
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch for merge checks (default: main)"
    )
    parser.add_argument(
        "--delete-merged",
        action="store_true",
        help="Delete merged old branches"
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all old branches (including unmerged)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force delete branches (use with caution)"
    )
    
    args = parser.parse_args()
    
    # Verify we're in a git repository
    if not Path(".git").exists():
        print("Error: Not in a git repository", file=sys.stderr)
        return 1
    
    print(f"Analyzing branches older than {args.days} days...")
    
    results = analyze_branches(args.days, args.base_branch)
    print_report(results, args.days)
    
    # Delete branches if requested
    if args.delete_merged or args.delete_all:
        branches_to_delete = []
        
        if args.delete_all:
            branches_to_delete = [b["name"] for b in results["old_branches"]]
        elif args.delete_merged:
            branches_to_delete = [b["name"] for b in results["merged_branches"]]
        
        if branches_to_delete:
            print(f"\n🗑️  DELETING BRANCHES")
            print("-" * 80)
            
            for branch in branches_to_delete:
                if delete_branch(branch, args.force):
                    print(f"✅ Deleted: {branch}")
                else:
                    print(f"❌ Failed to delete: {branch}")
            
            print("\n✅ Branch cleanup complete!")
        else:
            print("\nℹ️  No branches to delete")
    else:
        print("\n💡 Use --delete-merged to delete merged old branches")
        print("   Use --delete-all to delete all old branches (caution!)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
