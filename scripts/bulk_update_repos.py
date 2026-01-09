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
DEFGROUP: MokoStandards.Automation
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/bulk_update_repos.py
VERSION: 01.00.00
BRIEF: Bulk update script to push workflows, scripts, and configurations to organization repositories
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Default organization
DEFAULT_ORG = "mokoconsulting-tech"

# Files to sync with their destination paths
DEFAULT_FILES_TO_SYNC = {
    # Dependabot configuration
    ".github/dependabot.yml": ".github/dependabot.yml",
    
    # Workflow templates
    ".github/workflow-templates/build-universal.yml": ".github/workflows/build.yml",
    ".github/workflow-templates/codeql-analysis.yml": ".github/workflows/codeql-analysis.yml",
    ".github/workflow-templates/dependency-review.yml": ".github/workflows/dependency-review.yml",
    ".github/workflow-templates/standards-compliance.yml": ".github/workflows/standards-compliance.yml",
    ".github/workflow-templates/code-quality.yml": ".github/workflows/code-quality.yml",
    ".github/workflow-templates/release-cycle.yml": ".github/workflows/release-cycle.yml",
    
    # Reusable workflows
    ".github/workflows/reusable-build.yml": ".github/workflows/reusable-build.yml",
    ".github/workflows/reusable-ci-validation.yml": ".github/workflows/reusable-ci-validation.yml",
    ".github/workflows/reusable-release.yml": ".github/workflows/reusable-release.yml",
    
    # Automation workflows
    ".github/workflows/sync-changelogs.yml": ".github/workflows/sync-changelogs.yml",
    
    # Code quality configurations (optional - only copy if language is detected)
    # PHP configurations
    "templates/configs/phpcs.xml": "phpcs.xml",
    "templates/configs/phpstan.neon": "phpstan.neon",
    "templates/configs/psalm.xml": "psalm.xml",
    
    # JavaScript/TypeScript configurations
    "templates/configs/.eslintrc.json": ".eslintrc.json",
    "templates/configs/.prettierrc.json": ".prettierrc.json",
    
    # Python configurations
    "templates/configs/.pylintrc": ".pylintrc",
    "templates/configs/pyproject.toml": "pyproject.toml",
    
    # HTML configurations
    "templates/configs/.htmlhintrc": ".htmlhintrc",
}

# Scripts to sync
DEFAULT_SCRIPTS_TO_SYNC = [
    "scripts/validate_file_headers.py",
    "scripts/update_changelog.py",
    "scripts/release_version.py",
    "scripts/validate/validate_codeql_config.py",
]


def run_command(cmd: List[str], cwd: Optional[str] = None) -> Tuple[bool, str, str]:
    """Execute a command and return success status, stdout, and stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=True
        )
        return True, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else ""


def get_org_repositories(org: str, exclude_archived: bool = True) -> List[str]:
    """Get list of repositories in the organization that begin with 'Moko'."""
    cmd = [
        "gh", "repo", "list", org,
        "--json", "name,isArchived",
        "--limit", "1000"
    ]
    
    success, stdout, stderr = run_command(cmd)
    if not success:
        print(f"Error fetching repositories: {stderr}", file=sys.stderr)
        return []
    
    try:
        repos = json.loads(stdout)
        if exclude_archived:
            repos = [r for r in repos if not r.get("isArchived", False)]
        # Filter to only repositories beginning with "Moko"
        return [r["name"] for r in repos if r["name"].startswith("Moko")]
    except json.JSONDecodeError as e:
        print(f"Error parsing repository list: {e}", file=sys.stderr)
        return []


def clone_repository(org: str, repo: str, target_dir: str) -> bool:
    """Clone a repository to a temporary directory."""
    repo_url = f"https://github.com/{org}/{repo}.git"
    cmd = ["git", "clone", repo_url, target_dir]
    
    success, stdout, stderr = run_command(cmd)
    if not success:
        print(f"Error cloning {repo}: {stderr}", file=sys.stderr)
        return False
    
    return True


def create_branch(repo_dir: str, branch_name: str) -> bool:
    """Create and checkout a new branch in the repository."""
    # Check if branch already exists
    cmd = ["git", "rev-parse", "--verify", branch_name]
    success, _, _ = run_command(cmd, cwd=repo_dir)
    
    if success:
        # Branch exists, checkout
        cmd = ["git", "checkout", branch_name]
    else:
        # Create new branch
        cmd = ["git", "checkout", "-b", branch_name]
    
    success, stdout, stderr = run_command(cmd, cwd=repo_dir)
    if not success:
        print(f"Error creating/checking out branch: {stderr}", file=sys.stderr)
        return False
    
    return True


def copy_file(source_file: str, dest_dir: str, dest_path: str) -> bool:
    """Copy a file from source to destination, creating directories as needed."""
    source = Path(source_file)
    if not source.exists():
        print(f"Warning: Source file does not exist: {source_file}", file=sys.stderr)
        return False
    
    dest = Path(dest_dir) / dest_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        shutil.copy2(source, dest)
        return True
    except Exception as e:
        print(f"Error copying {source_file} to {dest}: {e}", file=sys.stderr)
        return False


def commit_changes(repo_dir: str, message: str) -> bool:
    """Commit changes in the repository."""
    # Add all changes
    cmd = ["git", "add", "."]
    success, _, stderr = run_command(cmd, cwd=repo_dir)
    if not success:
        print(f"Error adding files: {stderr}", file=sys.stderr)
        return False
    
    # Check if there are changes to commit
    cmd = ["git", "diff", "--cached", "--quiet"]
    success, _, _ = run_command(cmd, cwd=repo_dir)
    if success:
        # No changes to commit
        print("No changes to commit")
        return True
    
    # Commit changes
    cmd = ["git", "commit", "-m", message]
    success, _, stderr = run_command(cmd, cwd=repo_dir)
    if not success:
        print(f"Error committing changes: {stderr}", file=sys.stderr)
        return False
    
    return True


def push_branch(repo_dir: str, branch_name: str) -> bool:
    """Push branch to remote."""
    cmd = ["git", "push", "-u", "origin", branch_name]
    success, _, stderr = run_command(cmd, cwd=repo_dir)
    if not success:
        print(f"Error pushing branch: {stderr}", file=sys.stderr)
        return False
    
    return True


def create_pull_request(org: str, repo: str, branch_name: str, title: str, body: str) -> bool:
    """Create a pull request for the branch."""
    cmd = [
        "gh", "pr", "create",
        "--repo", f"{org}/{repo}",
        "--head", branch_name,
        "--title", title,
        "--body", body
    ]
    
    success, stdout, stderr = run_command(cmd)
    if not success:
        # Check if PR already exists
        if "already exists" in stderr.lower():
            print(f"Pull request already exists for branch {branch_name}")
            return True
        print(f"Error creating pull request: {stderr}", file=sys.stderr)
        return False
    
    print(f"Created pull request: {stdout}")
    return True


def update_repository(
    org: str,
    repo: str,
    source_dir: str,
    files_to_sync: Dict[str, str],
    scripts_to_sync: List[str],
    branch_name: str,
    commit_message: str,
    pr_title: str,
    pr_body: str,
    temp_dir: str,
    dry_run: bool = False
) -> bool:
    """Update a single repository with files and scripts."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing repository: {org}/{repo}")
    
    if dry_run:
        print(f"  Would sync {len(files_to_sync)} files and {len(scripts_to_sync)} scripts")
        return True
    
    # Create temporary directory for this repo
    repo_dir = Path(temp_dir) / repo
    
    # Clone repository
    print(f"  Cloning repository...")
    if not clone_repository(org, repo, str(repo_dir)):
        return False
    
    # Create branch
    print(f"  Creating branch: {branch_name}")
    if not create_branch(str(repo_dir), branch_name):
        return False
    
    # Copy files
    files_copied = 0
    for source_rel, dest_rel in files_to_sync.items():
        source_file = Path(source_dir) / source_rel
        if copy_file(str(source_file), str(repo_dir), dest_rel):
            files_copied += 1
            print(f"    Copied: {source_rel} -> {dest_rel}")
    
    # Copy scripts
    for script in scripts_to_sync:
        source_file = Path(source_dir) / script
        if copy_file(str(source_file), str(repo_dir), script):
            files_copied += 1
            print(f"    Copied: {script}")
    
    if files_copied == 0:
        print(f"  No files were copied, skipping commit")
        return True
    
    # Commit changes
    print(f"  Committing changes...")
    if not commit_changes(str(repo_dir), commit_message):
        return False
    
    # Push branch
    print(f"  Pushing branch...")
    if not push_branch(str(repo_dir), branch_name):
        return False
    
    # Create pull request
    print(f"  Creating pull request...")
    if not create_pull_request(org, repo, branch_name, pr_title, pr_body):
        return False
    
    print(f"  ✓ Successfully updated {org}/{repo}")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Bulk update organization repositories with workflows, scripts, and configurations'
    )
    parser.add_argument(
        '--org',
        default=DEFAULT_ORG,
        help=f'Organization name (default: {DEFAULT_ORG})'
    )
    parser.add_argument(
        '--repos',
        nargs='+',
        help='Specific repositories to update (default: all non-archived repos in org)'
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=[],
        help='Repositories to exclude from update'
    )
    parser.add_argument(
        '--source-dir',
        default='.',
        help='Source directory containing files to sync (default: current directory)'
    )
    parser.add_argument(
        '--branch',
        default='chore/sync-mokostandards-updates',
        help='Branch name for changes (default: chore/sync-mokostandards-updates)'
    )
    parser.add_argument(
        '--commit-message',
        default='chore: sync workflows, scripts, and configurations from MokoStandards',
        help='Commit message for changes'
    )
    parser.add_argument(
        '--pr-title',
        default='chore: Sync MokoStandards workflows and configurations',
        help='Pull request title'
    )
    parser.add_argument(
        '--pr-body',
        default='This PR syncs workflows, scripts, and configurations from the MokoStandards repository.\n\n'
                'Updated files:\n'
                '- GitHub workflows (CI, CodeQL, dependency review, build, release)\n'
                '- Dependabot configuration (monthly schedule)\n'
                '- Maintenance scripts (validation, changelog, release)\n\n'
                'Please review and merge if appropriate for this repository.',
        help='Pull request body'
    )
    parser.add_argument(
        '--files-only',
        action='store_true',
        help='Only sync workflow files, not scripts'
    )
    parser.add_argument(
        '--scripts-only',
        action='store_true',
        help='Only sync scripts, not workflow files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--temp-dir',
        default='/tmp/bulk-update-repos',
        help='Temporary directory for cloning repositories'
    )
    parser.add_argument(
        '--yes',
        '-y',
        action='store_true',
        help='Skip confirmation prompt (use for automation)'
    )
    
    args = parser.parse_args()
    
    # Check for gh CLI
    success, _, _ = run_command(["gh", "--version"])
    if not success:
        print("Error: gh CLI is not installed or not in PATH", file=sys.stderr)
        print("Install from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)
    
    # Check for authentication
    success, _, _ = run_command(["gh", "auth", "status"])
    if not success:
        print("Error: Not authenticated with gh CLI", file=sys.stderr)
        print("Run: gh auth login", file=sys.stderr)
        sys.exit(1)
    
    # Determine files to sync
    files_to_sync = {} if args.scripts_only else DEFAULT_FILES_TO_SYNC.copy()
    scripts_to_sync = [] if args.files_only else DEFAULT_SCRIPTS_TO_SYNC.copy()
    
    # Get repositories to update
    if args.repos:
        repos = args.repos
    else:
        print(f"Fetching repositories from {args.org}...")
        repos = get_org_repositories(args.org)
        if not repos:
            print("No repositories found or error fetching repositories", file=sys.stderr)
            sys.exit(1)
    
    # Apply exclusions
    repos = [r for r in repos if r not in args.exclude]
    
    print(f"\n{'DRY RUN: ' if args.dry_run else ''}Will update {len(repos)} repositories:")
    for repo in repos:
        print(f"  - {repo}")
    
    if not args.dry_run and not args.yes:
        response = input("\nContinue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted")
            sys.exit(0)
    
    # Create temp directory
    temp_dir = Path(args.temp_dir)
    if not args.dry_run:
        temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Update each repository
    success_count = 0
    failed_repos = []
    
    for repo in repos:
        try:
            if update_repository(
                args.org,
                repo,
                args.source_dir,
                files_to_sync,
                scripts_to_sync,
                args.branch,
                args.commit_message,
                args.pr_title,
                args.pr_body,
                str(temp_dir),
                args.dry_run
            ):
                success_count += 1
            else:
                failed_repos.append(repo)
        except Exception as e:
            print(f"Error updating {repo}: {e}", file=sys.stderr)
            failed_repos.append(repo)
    
    # Summary
    print(f"\n{'DRY RUN ' if args.dry_run else ''}Summary:")
    print(f"  Successfully {'would update' if args.dry_run else 'updated'}: {success_count}/{len(repos)} repositories")
    
    if failed_repos:
        print(f"  Failed repositories:")
        for repo in failed_repos:
            print(f"    - {repo}")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
