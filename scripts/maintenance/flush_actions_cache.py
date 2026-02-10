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
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Maintenance
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/maintenance/flush_actions_cache.py
VERSION: 03.01.05
BRIEF: Flush GitHub Actions caches for a repository
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Dict, List, Optional


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """
    Execute a shell command and return the result.

    Args:
        cmd: Command to execute as list of strings
        check: Whether to raise exception on non-zero exit code

    Returns:
        CompletedProcess object with result
    """
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"   Exit code: {e.returncode}", file=sys.stderr)
        print(f"   stderr: {e.stderr}", file=sys.stderr)
        raise


def check_gh_cli() -> bool:
    """
    Check if GitHub CLI is installed and authenticated.

    Returns:
        True if gh CLI is available and authenticated
    """
    try:
        result = run_command(['gh', 'auth', 'status'], check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) is not installed.", file=sys.stderr)
        print("   Install from: https://cli.github.com/", file=sys.stderr)
        return False


def list_caches(repo: str) -> List[Dict]:
    """
    List all GitHub Actions caches for a repository.

    Args:
        repo: Repository in format 'owner/repo'

    Returns:
        List of cache objects
    """
    print(f"📋 Listing caches for {repo}...")

    result = run_command([
        'gh', 'cache', 'list',
        '--repo', repo,
        '--json', 'id,key,ref,sizeInBytes,createdAt,lastAccessedAt'
    ])

    caches = json.loads(result.stdout)
    return caches


def delete_cache(repo: str, cache_id: int) -> bool:
    """
    Delete a specific cache by ID.

    Args:
        repo: Repository in format 'owner/repo'
        cache_id: Cache ID to delete

    Returns:
        True if deletion was successful
    """
    try:
        run_command([
            'gh', 'cache', 'delete',
            str(cache_id),
            '--repo', repo,
            '--confirm'
        ])
        return True
    except subprocess.CalledProcessError:
        return False


def flush_all_caches(repo: str, branch: Optional[str] = None,
                     key_pattern: Optional[str] = None, dry_run: bool = False) -> int:
    """
    Flush all caches for a repository, optionally filtered by branch or key pattern.

    Args:
        repo: Repository in format 'owner/repo'
        branch: Optional branch name to filter caches
        key_pattern: Optional key pattern to filter caches
        dry_run: If True, only show what would be deleted

    Returns:
        Number of caches deleted
    """
    caches = list_caches(repo)

    if not caches:
        print("✅ No caches found.")
        return 0

    # Filter caches by branch if specified
    if branch:
        caches = [c for c in caches if c.get('ref', '').endswith(f'/{branch}')]
        print(f"🔍 Filtered to caches for branch: {branch}")

    # Filter caches by key pattern if specified
    if key_pattern:
        caches = [c for c in caches if key_pattern in c.get('key', '')]
        print(f"🔍 Filtered to caches matching pattern: {key_pattern}")

    if not caches:
        print("✅ No caches match the specified filters.")
        return 0

    # Display caches
    print(f"\n📦 Found {len(caches)} cache(s):")
    print("-" * 80)
    for cache in caches:
        size_mb = cache.get('sizeInBytes', 0) / (1024 * 1024)
        print(f"  • ID: {cache['id']}")
        print(f"    Key: {cache['key']}")
        print(f"    Ref: {cache.get('ref', 'N/A')}")
        print(f"    Size: {size_mb:.2f} MB")
        print(f"    Created: {cache.get('createdAt', 'N/A')}")
        print(f"    Last Accessed: {cache.get('lastAccessedAt', 'N/A')}")
        print()

    if dry_run:
        print("🔍 Dry run mode - no caches will be deleted.")
        return 0

    # Delete caches
    deleted_count = 0
    failed_count = 0

    print("🗑️  Deleting caches...")
    for cache in caches:
        cache_id = cache['id']
        cache_key = cache['key']

        if delete_cache(repo, cache_id):
            print(f"  ✅ Deleted cache: {cache_key} (ID: {cache_id})")
            deleted_count += 1
        else:
            print(f"  ❌ Failed to delete cache: {cache_key} (ID: {cache_id})")
            failed_count += 1

    print()
    print("-" * 80)
    print(f"✅ Successfully deleted {deleted_count} cache(s)")
    if failed_count > 0:
        print(f"❌ Failed to delete {failed_count} cache(s)")

    return deleted_count


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Flush GitHub Actions caches for a repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Flush all caches for current repository
  %(prog)s

  # Flush all caches for a specific repository
  %(prog)s --repo owner/repo

  # Flush caches for a specific branch
  %(prog)s --branch main

  # Flush caches matching a key pattern
  %(prog)s --key composer

  # Dry run to see what would be deleted
  %(prog)s --dry-run

  # Combine filters
  %(prog)s --branch dev --key node --dry-run
"""
    )

    parser.add_argument(
        '--repo',
        help='Repository in format owner/repo (default: current repository)',
        default=None
    )

    parser.add_argument(
        '--branch',
        help='Filter caches by branch name',
        default=None
    )

    parser.add_argument(
        '--key',
        help='Filter caches by key pattern',
        default=None
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 01.00.00'
    )

    args = parser.parse_args()

    # Check GitHub CLI
    if not check_gh_cli():
        sys.exit(1)

    # Determine repository
    repo = args.repo
    if not repo:
        # Try to detect from current git repository
        try:
            result = run_command(['gh', 'repo', 'view', '--json', 'nameWithOwner'])
            repo_data = json.loads(result.stdout)
            repo = repo_data['nameWithOwner']
            print(f"🔍 Detected repository: {repo}")
        except Exception as e:
            print(f"❌ Could not detect repository. Please specify with --repo", file=sys.stderr)
            sys.exit(1)

    print(f"\n🧹 Flushing GitHub Actions caches")
    print(f"📁 Repository: {repo}")
    if args.branch:
        print(f"🌿 Branch filter: {args.branch}")
    if args.key:
        print(f"🔑 Key pattern: {args.key}")
    if args.dry_run:
        print(f"🔍 Mode: Dry run")
    print()

    # Flush caches
    try:
        deleted = flush_all_caches(
            repo=repo,
            branch=args.branch,
            key_pattern=args.key,
            dry_run=args.dry_run
        )

        if deleted > 0 and not args.dry_run:
            print("\n✅ Cache flush complete!")
        elif args.dry_run:
            print("\n✅ Dry run complete!")
        else:
            print("\n✅ No caches to flush.")

    except Exception as e:
        print(f"\n❌ Error flushing caches: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
