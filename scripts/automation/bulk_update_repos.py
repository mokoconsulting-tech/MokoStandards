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
PATH: /scripts/automation/bulk_update_repos.py
VERSION: 03.01.02
BRIEF: Schema-driven bulk repository sync - Clean v2 implementation
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set

# Default organization
DEFAULT_ORG = "mokoconsulting-tech"

# Sync override file name (located in root of target repo)
# Changed from XML to Terraform format
SYNC_OVERRIDE_FILE = "MokoStandards.override.tf"


class FileSyncConfig:
    """Configuration for files to sync to target repositories"""

    # Core configuration files (always sync)
    CORE_CONFIGS = {
        ".github/dependabot.yml": ".github/dependabot.yml",
        ".github/copilot.yml": ".github/copilot.yml",
    }

    # Workflow templates by category (conditional based on platform)
    WORKFLOW_TEMPLATES = {
        # Universal workflows (all repositories)
        "universal": {
            "templates/workflows/build.yml.template": ".github/workflows/build.yml",
            "templates/workflows/unified-ci.yml.template": ".github/workflows/ci.yml",
        },

        # Generic platform workflows
        "generic": {
            "templates/workflows/generic/code-quality.yml": ".github/workflows/code-quality.yml",
            "templates/workflows/generic/codeql-analysis.yml": ".github/workflows/codeql-analysis.yml",
            "templates/workflows/generic/repo-health.yml": ".github/workflows/repo-health.yml",
        },

        # Terraform infrastructure workflows
        "terraform": {
            "templates/workflows/terraform/ci.yml": ".github/workflows/terraform-ci.yml",
            "templates/workflows/terraform/deploy.yml.template": ".github/workflows/terraform-deploy.yml",
            "templates/workflows/terraform/drift-detection.yml.template": ".github/workflows/terraform-drift.yml",
        },

        # Dolibarr-specific workflows
        "dolibarr": {
            "templates/workflows/dolibarr/release.yml.template": ".github/workflows/release.yml",
            "templates/workflows/dolibarr/sync-changelogs.yml.template": ".github/workflows/sync-changelogs.yml",
        },

        # Joomla-specific workflows
        "joomla": {
            "templates/workflows/joomla/release.yml.template": ".github/workflows/release.yml",
            "templates/workflows/joomla/repo_health.yml.template": ".github/workflows/repo-health.yml",
        },
    }

    # Reusable workflows (all repositories)
    REUSABLE_WORKFLOWS = {
        "templates/workflows/reusable-build.yml.template": ".github/workflows/reusable-build.yml",
        "templates/workflows/reusable-ci-validation.yml": ".github/workflows/reusable-ci-validation.yml",
        "templates/workflows/reusable-release.yml.template": ".github/workflows/reusable-release.yml",
        "templates/workflows/reusable-php-quality.yml": ".github/workflows/reusable-php-quality.yml",
        "templates/workflows/reusable-platform-testing.yml": ".github/workflows/reusable-platform-testing.yml",
        "templates/workflows/reusable-project-detector.yml": ".github/workflows/reusable-project-detector.yml",
        "templates/workflows/reusable-deploy.yml": ".github/workflows/reusable-deploy.yml",
        "templates/workflows/reusable-script-executor.yml": ".github/workflows/reusable-script-executor.yml",
    }

    # Shared automation workflows (conditional)
    SHARED_AUTOMATION = {
        ".github/workflows/enterprise-firewall-setup.yml": ".github/workflows/enterprise-firewall-setup.yml",
    }

    # Language-specific configuration files
    LANGUAGE_CONFIGS = {
        "php": {
            "templates/configs/phpcs.xml": "phpcs.xml",
            "templates/configs/phpstan.neon": "phpstan.neon",
            "templates/configs/psalm.xml": "psalm.xml",
        },
        "javascript": {
            "templates/configs/.eslintrc.json": ".eslintrc.json",
            "templates/configs/.prettierrc.json": ".prettierrc.json",
        },
        "python": {
            "templates/configs/.pylintrc": ".pylintrc",
            "templates/configs/pyproject.toml": "pyproject.toml",
        },
        "html": {
            "templates/configs/.htmlhintrc": ".htmlhintrc",
        },
    }


# Scripts to sync (required for platform detection and validation)
DEFAULT_SCRIPTS_TO_SYNC = [
    "scripts/maintenance/validate_file_headers.py",
    "scripts/maintenance/update_changelog.py",
    "scripts/maintenance/release_version.py",
    "scripts/validate/validate_codeql_config.py",
    "scripts/validate/auto_detect_platform.py",
    "scripts/validate/validate_structure_v2.py",
    # Schema definitions needed by auto_detect_platform.py
    "scripts/definitions/crm-module.xml",
    "scripts/definitions/default-repository.xml",
    "scripts/definitions/waas-component.xml",
]


def parse_override_file(override_path: str) -> Tuple[Set[str], Set[str], Optional[str]]:
    """
    Parse the MokoStandards.override.tf file.

    Args:
        override_path: Path to the override Terraform file

    Returns:
        Tuple of (exclude_files, protected_files, repository_type) where:
        - exclude_files: set of file paths to exclude from sync
        - protected_files: set of file paths to protect from overwrite
        - repository_type: platform type from override (None if not specified)
    """
    exclude_files = set()
    protected_files = set()
    repository_type = None

    try:
        with open(override_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse repository_type from metadata
        # Look for: repository_type = "terraform" or "dolibarr" or "joomla" etc.
        type_match = re.search(
            r'repository_type\s*=\s*"([^"]+)"',
            content
        )
        if type_match:
            repository_type = type_match.group(1)
            # Map "standards" to None (shouldn't use platform-specific templates)
            if repository_type == "standards":
                repository_type = None

        # Parse exclude_files list
        # Look for: exclude_files = [ { path = "..." reason = "..." }, ... ]
        exclude_match = re.search(
            r'exclude_files\s*=\s*\[(.*?)\]',
            content,
            re.DOTALL
        )
        if exclude_match:
            exclude_block = exclude_match.group(1)
            # Find all path values in the block
            for path_match in re.finditer(r'path\s*=\s*"([^"]+)"', exclude_block):
                path = path_match.group(1)
                if path:
                    exclude_files.add(path)

        # Parse protected_files list
        # Look for: protected_files = [ { path = "..." reason = "..." }, ... ]
        protected_match = re.search(
            r'protected_files\s*=\s*\[(.*?)\]',
            content,
            re.DOTALL
        )
        if protected_match:
            protected_block = protected_match.group(1)
            # Find all path values in the block
            for path_match in re.finditer(r'path\s*=\s*"([^"]+)"', protected_block):
                path = path_match.group(1)
                if path:
                    protected_files.add(path)

    except Exception as e:
        print(f"Warning: Failed to parse override file {override_path}: {e}")

    return exclude_files, protected_files, repository_type


def load_override_config(repo_dir: str, source_dir: str) -> Tuple[Set[str], Set[str], Optional[str]]:
    """
    Load override configuration from target repo or MokoStandards default.

    Args:
        repo_dir: Path to the target repository
        source_dir: Path to MokoStandards source directory

    Returns:
        Tuple of (exclude_files, protected_files, repository_type) where:
        - exclude_files: set of file paths to exclude from sync
        - protected_files: set of file paths to protect from overwrite
        - repository_type: platform type from override (None if not specified or should auto-detect)
    """
    # First, check if target repo has an override file
    repo_override = Path(repo_dir) / SYNC_OVERRIDE_FILE
    if repo_override.exists():
        print(f"    Using override configuration from target repository")
        return parse_override_file(str(repo_override))

    # Otherwise, check if MokoStandards has a default override file
    default_override = Path(source_dir) / SYNC_OVERRIDE_FILE
    if default_override.exists():
        print(f"    Using default override configuration from MokoStandards")
        return parse_override_file(str(default_override))

    print(f"    No override configuration found, using default behavior")
    return set(), set(), None


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


def get_org_repositories(org: str, exclude_archived: bool = True, include_templates: bool = True) -> List[str]:
    """Get list of repositories in the organization that begin with 'Moko'."""
    cmd = [
        "gh", "repo", "list", org,
        "--json", "name,isArchived,isTemplate",
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
        # Include templates if requested (default: True)
        if not include_templates:
            repos = [r for r in repos if not r.get("isTemplate", False)]
        # Filter to only repositories beginning with "Moko"
        return [r["name"] for r in repos if r["name"].startswith("Moko")]
    except json.JSONDecodeError as e:
        print(f"Error parsing repository list: {e}", file=sys.stderr)
        return []


def detect_platform(repo_dir: str, source_dir: str) -> Optional[str]:
    """
    Detect the platform type of a repository using auto_detect_platform.py
    and additional terraform detection logic.

    Args:
        repo_dir: Path to the cloned repository
        source_dir: Path to MokoStandards source directory

    Returns:
        Platform type string (terraform, joomla, dolibarr, generic) or None if detection fails
    """
    # First check for terraform repository
    terraform_dir = Path(repo_dir) / "terraform"
    if terraform_dir.exists() and terraform_dir.is_dir():
        # Check for terraform files
        tf_files = list(Path(repo_dir).rglob("*.tf"))
        if tf_files:
            print(f"    Detected Terraform repository (found {len(tf_files)} .tf files)")
            return "terraform"

    script_path = Path(source_dir) / "scripts" / "validate" / "auto_detect_platform.py"

    if not script_path.exists():
        print(f"    Warning: auto_detect_platform.py not found at {script_path}", file=sys.stderr)
        return None

    try:
        # Run platform detection script
        cmd = ["python3", str(script_path), "--repo-path", repo_dir, "--json"]
        success, stdout, stderr = run_command(cmd)

        if success and stdout:
            try:
                result = json.loads(stdout)
                return result.get("platform_type", "generic")
            except json.JSONDecodeError:
                print(f"    Warning: Failed to parse platform detection output", file=sys.stderr)
                return None
        else:
            print(f"    Warning: Platform detection failed: {stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"    Warning: Platform detection error: {e}", file=sys.stderr)
        return None


def get_files_to_sync(platform: str = "generic") -> Dict[str, str]:
    """
    Get the list of files to sync based on platform type.

    Args:
        platform: Platform type (terraform, generic, dolibarr, joomla)

    Returns:
        Dictionary mapping source files to destination paths
    """
    files = {}

    # Always include core configs
    files.update(FileSyncConfig.CORE_CONFIGS)

    # Add universal workflows
    files.update(FileSyncConfig.WORKFLOW_TEMPLATES["universal"])

    # Add platform-specific workflows
    if platform in FileSyncConfig.WORKFLOW_TEMPLATES:
        files.update(FileSyncConfig.WORKFLOW_TEMPLATES[platform])
    else:
        # Default to generic if platform not recognized
        files.update(FileSyncConfig.WORKFLOW_TEMPLATES["generic"])

    # Add reusable workflows
    files.update(FileSyncConfig.REUSABLE_WORKFLOWS)

    # Add shared automation (can be conditional based on needs)
    files.update(FileSyncConfig.SHARED_AUTOMATION)

    return files


def validate_source_files(files_to_sync: Dict[str, str], source_dir: str) -> Tuple[List[str], List[str]]:
    """
    Validate that all source files exist before attempting sync.

    Returns:
        Tuple of (existing_files, missing_files)
    """
    existing = []
    missing = []

    for source_rel, _ in files_to_sync.items():
        source_path = Path(source_dir) / source_rel
        if source_path.exists():
            existing.append(source_rel)
        else:
            missing.append(source_rel)

    return existing, missing


def copy_file(source_file: str, dest_dir: str, dest_path: str) -> Tuple[bool, str]:
    """
    Copy a file from source to destination, creating directories as needed.

    Returns:
        Tuple of (success, action) where action is 'created' or 'overwritten'
    """
    source = Path(source_file)
    if not source.exists():
        print(f"Warning: Source file does not exist: {source_file}", file=sys.stderr)
        return False, "missing"

    dest = Path(dest_dir) / dest_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Check if file already exists to determine action
    action = "overwritten" if dest.exists() else "created"

    try:
        shutil.copy2(source, dest)
        return True, action
    except Exception as e:
        print(f"Error copying {source_file} to {dest}: {e}", file=sys.stderr)
        return False, "error"


def cleanup_obsolete_files(
    repo_dir: str,
    current_files: Dict[str, str],
    current_scripts: List[str],
    protected_files: Set[str],
    cleanup_mode: str = "conservative"
) -> Tuple[List[str], int]:
    """
    Remove obsolete files from target repository that are no longer in the sync list.
    
    Args:
        repo_dir: Path to repository directory
        current_files: Dictionary of files currently being synced (dest_path -> source_path)
        current_scripts: List of scripts currently being synced
        protected_files: Set of files that should never be deleted
        cleanup_mode: "none", "conservative", or "aggressive"
    
    Returns:
        Tuple of (deleted_files list, count)
    """
    deleted_files = []
    
    if cleanup_mode == "none":
        return deleted_files, 0
    
    repo_path = Path(repo_dir)
    
    # Define directories to clean
    cleanup_dirs = {
        ".github/workflows": "workflows",
        "scripts/maintenance": "scripts",
        "scripts/validate": "scripts",
        "scripts/release": "scripts",
        "scripts/definitions": "scripts",
    }
    
    # Get list of all files we're syncing (destinations)
    current_dest_files = set(current_files.values())
    current_dest_files.update(current_scripts)
    
    for dir_path, category in cleanup_dirs.items():
        dir_full = repo_path / dir_path
        
        if not dir_full.exists():
            continue
        
        # Get all files in this directory
        for file_path in dir_full.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Get relative path from repo root
            rel_path = str(file_path.relative_to(repo_path))
            
            # Skip if this file is protected
            if rel_path in protected_files:
                continue
            
            # Skip if this file is in our current sync list
            if rel_path in current_dest_files:
                continue
            
            # In conservative mode, only remove workflow and script files we would sync
            if cleanup_mode == "conservative":
                # Only remove .yml files from workflows directory
                if category == "workflows" and not rel_path.endswith(('.yml', '.yaml')):
                    continue
                # Only remove .py files from scripts directory
                if category == "scripts" and not rel_path.endswith('.py'):
                    continue
            
            # Delete the file
            try:
                file_path.unlink()
                deleted_files.append(rel_path)
                print(f"    🗑  Removed obsolete: {rel_path}")
            except Exception as e:
                print(f"    Warning: Could not remove {rel_path}: {e}", file=sys.stderr)
    
    return deleted_files, len(deleted_files)


def clone_repository(org: str, repo: str, target_dir: str) -> bool:
    """Clone a repository to a temporary directory."""
    # Use gh CLI to clone with authentication
    cmd = ["gh", "repo", "clone", f"{org}/{repo}", target_dir]

    success, stdout, stderr = run_command(cmd)
    if not success:
        print(f"Error cloning {repo}: {stderr}", file=sys.stderr)
        return False

    # Configure git to use gh as credential helper for push operations
    cmd = ["git", "config", "--local", "credential.helper", ""]
    run_command(cmd, cwd=target_dir)

    cmd = ["git", "config", "--local", "credential.helper", "!gh auth git-credential"]
    success, _, stderr = run_command(cmd, cwd=target_dir)
    if not success:
        print(f"Warning: Could not configure gh credential helper: {stderr}", file=sys.stderr)

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
    """Push branch to remote using gh CLI for proper authentication."""
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
    branch_name: str,
    commit_message: str,
    pr_title: str,
    pr_body: str,
    temp_dir: str,
    dry_run: bool = False,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Update a single repository with files and scripts.

    Returns:
        Tuple of (success, stats) where stats contains:
        - files_created: count of new files
        - files_overwritten: count of updated files
        - files_copied: list of copied file paths
        - files_overwritten_list: list of overwritten file paths
        - platform: detected platform type
    """
    stats = {
        "files_created": 0,
        "files_overwritten": 0,
        "files_deleted": 0,
        "files_copied": [],
        "files_overwritten_list": [],
        "deleted_files_list": [],
        "platform": "unknown",
    }

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing repository: {org}/{repo}")

    # Create temporary directory for this repo
    repo_dir = Path(temp_dir) / repo

    if dry_run:
        print(f"  Would clone and sync repository")
        return True, stats

    # Clone repository
    print(f"  Cloning repository...")
    if not clone_repository(org, repo, str(repo_dir)):
        return False, stats

    # Load override configuration FIRST (before platform detection)
    # This allows override to specify platform type and avoid unnecessary detection
    print(f"  Loading override configuration...")
    exclude_files, protected_files, override_platform = load_override_config(str(repo_dir), source_dir)
    
    # Determine platform type: use override if specified, otherwise auto-detect
    if override_platform:
        print(f"    Platform type from override: {override_platform}")
        platform_type = override_platform
        stats["platform"] = f"{override_platform} (from override)"
    else:
        # Detect platform using auto_detect_platform.py
        print(f"  Detecting platform type...")
        platform_type = detect_platform(str(repo_dir), source_dir)
        if platform_type:
            print(f"    Detected platform: {platform_type}")
            stats["platform"] = platform_type
        else:
            print(f"    Platform detection failed, using generic defaults")
            platform_type = "generic"
            stats["platform"] = "generic"
    
    # Parse cleanup mode from override file if present
    cleanup_mode = "conservative"  # default
    override_file = Path(repo_dir) / SYNC_OVERRIDE_FILE
    if override_file.exists():
        try:
            with open(override_file, 'r') as f:
                content = f.read()
                # Look for cleanup_mode in sync_config
                mode_match = re.search(r'cleanup_mode\s*=\s*"([^"]+)"', content)
                if mode_match:
                    cleanup_mode = mode_match.group(1)
                    print(f"    Cleanup mode from override: {cleanup_mode}")
        except Exception as e:
            print(f"    Warning: Could not parse cleanup mode: {e}")

    # Get files to sync based on platform
    files_to_sync = get_files_to_sync(platform_type)

    # Filter out excluded files based on override configuration
    if exclude_files:
        original_count = len(files_to_sync)
        files_to_sync = {k: v for k, v in files_to_sync.items() if v not in exclude_files}
        filtered_count = original_count - len(files_to_sync)
        if filtered_count > 0:
            print(f"    Filtered out {filtered_count} excluded files from override config")

    # Validate source files exist
    existing, missing = validate_source_files(files_to_sync, source_dir)
    if missing:
        print(f"  Warning: {len(missing)} source files missing:")
        for f in missing[:5]:  # Show first 5 missing files
            print(f"    - {f}")
        if len(missing) > 5:
            print(f"    ... and {len(missing) - 5} more")
        # Filter out missing files
        files_to_sync = {k: v for k, v in files_to_sync.items() if k in existing}

    # Create branch
    print(f"  Creating branch: {branch_name}")
    if not create_branch(str(repo_dir), branch_name):
        return False, stats
    
    # Clean up obsolete files before syncing new ones
    if cleanup_mode != "none":
        print(f"  Cleaning up obsolete files (mode: {cleanup_mode})...")
        deleted_files, delete_count = cleanup_obsolete_files(
            str(repo_dir),
            files_to_sync,
            DEFAULT_SCRIPTS_TO_SYNC,
            protected_files,
            cleanup_mode
        )
        if delete_count > 0:
            stats["files_deleted"] = delete_count
            stats["deleted_files_list"] = deleted_files
            print(f"    Removed {delete_count} obsolete file(s)")
    
    # Place override file in target repo if it doesn't exist and if one exists in MokoStandards
    override_source = Path(source_dir) / SYNC_OVERRIDE_FILE
    override_dest = Path(repo_dir) / SYNC_OVERRIDE_FILE
    if override_source.exists() and not override_dest.exists():
        print(f"  Placing override configuration file...")
        success, action = copy_file(str(override_source), str(repo_dir), SYNC_OVERRIDE_FILE)
        if success and action == "created":
            stats["files_created"] += 1
            stats["files_copied"].append(SYNC_OVERRIDE_FILE)
            print(f"    ✓ Created: {SYNC_OVERRIDE_FILE}")

    # Copy files and track actions
    for source_rel, dest_rel in files_to_sync.items():
        # Skip protected files
        if dest_rel in protected_files:
            print(f"    ⊗ Skipped (protected): {dest_rel}")
            continue

        source_file = Path(source_dir) / source_rel
        success, action = copy_file(str(source_file), str(repo_dir), dest_rel)
        if success:
            if action == "created":
                stats["files_created"] += 1
                stats["files_copied"].append(dest_rel)
                print(f"    ✓ Created: {dest_rel}")
            elif action == "overwritten":
                stats["files_overwritten"] += 1
                stats["files_overwritten_list"].append(dest_rel)
                print(f"    ↻ Updated: {dest_rel}")

    # Copy scripts and track actions
    for script in DEFAULT_SCRIPTS_TO_SYNC:
        # Skip protected files
        if script in protected_files:
            print(f"    ⊗ Skipped (protected): {script}")
            continue

        source_file = Path(source_dir) / script
        success, action = copy_file(str(source_file), str(repo_dir), script)
        if success:
            if action == "created":
                stats["files_created"] += 1
                stats["files_copied"].append(script)
                print(f"    ✓ Created: {script}")
            elif action == "overwritten":
                stats["files_overwritten"] += 1
                stats["files_overwritten_list"].append(script)
                print(f"    ↻ Updated: {script}")

    total_files = stats["files_created"] + stats["files_overwritten"]

    if total_files == 0:
        print(f"  No files were copied, skipping commit")
        return True, stats

    # Commit changes
    print(f"  Committing changes...")
    if not commit_changes(str(repo_dir), commit_message):
        return False, stats

    # Push branch
    print(f"  Pushing branch...")
    if not push_branch(str(repo_dir), branch_name):
        return False, stats

    # Create pull request
    print(f"  Creating pull request...")
    if not create_pull_request(org, repo, branch_name, pr_title, pr_body):
        return False, stats

    print(f"  ✓ Successfully updated {org}/{repo}")
    print(f"    - Platform: {stats['platform']}")
    print(f"    - Created: {stats['files_created']} files")
    print(f"    - Updated: {stats['files_overwritten']} files")

    return True, stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Schema-driven bulk repository sync (v2) - Syncs MokoStandards to organization repositories',
        epilog="""
IMPORTANT: This script defaults to the mokoconsulting-tech organization.
Use --org only if you need to sync to a different organization.

TYPICAL USAGE:
  # Dry run to preview changes for one repo:
  python3 bulk_update_repos.py --repos moko-cassiopeia --dry-run
  
  # Sync specific repos with auto-confirmation:
  python3 bulk_update_repos.py --repos moko-cassiopeia moko-dolibarr --yes
  
  # Sync all repos except specific ones:
  python3 bulk_update_repos.py --exclude MokoStandards test-repo --yes

SYNC BEHAVIOR:
  1. Checks MokoStandards.override.tf in target repo for:
     - Platform type (repository_type field)
     - Files to exclude (exclude_files list)
     - Files to protect (protected_files list)
  2. Falls back to auto-detection if override doesn't specify platform
  3. Syncs appropriate workflows, scripts, and configs based on platform
  4. Creates a PR with changes (never pushes to main/master directly)

OVERRIDE FILE PRIORITY:
  The script ALWAYS checks for MokoStandards.override.tf before running
  platform detection. This allows repositories to explicitly specify their
  platform type and avoid unnecessary auto-detection.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--org',
        default=DEFAULT_ORG,
        help=f'Organization name (default: {DEFAULT_ORG}) - Use default for mokoconsulting-tech'
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
                '- GitHub workflows (CI, build, release, etc.)\n'
                '- Dependabot configuration\n'
                '- Maintenance scripts\n'
                '- Platform-specific configurations\n\n'
                'Files are synced based on detected platform type (terraform/generic/dolibarr/joomla).\n\n'
                'Please review and merge if appropriate for this repository.',
        help='Pull request body'
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
    all_stats = {}
    total_created = 0
    total_overwritten = 0

    for repo in repos:
        try:
            success, stats = update_repository(
                args.org,
                repo,
                args.source_dir,
                args.branch,
                args.commit_message,
                args.pr_title,
                args.pr_body,
                str(temp_dir),
                args.dry_run,
            )
            if success:
                success_count += 1
                all_stats[repo] = stats
                total_created += stats["files_created"]
                total_overwritten += stats["files_overwritten"]
            else:
                failed_repos.append(repo)
        except Exception as e:
            print(f"Error updating {repo}: {e}", file=sys.stderr)
            failed_repos.append(repo)

    # Summary
    print(f"\n{'=' * 70}")
    print(f"{'DRY RUN ' if args.dry_run else ''}SUMMARY")
    print(f"{'=' * 70}")
    print(f"Successfully {'would update' if args.dry_run else 'updated'}: {success_count}/{len(repos)} repositories")
    print(f"\nFile Operations:")
    print(f"  - Total files created: {total_created}")
    print(f"  - Total files updated: {total_overwritten}")
    
    # Count total deleted files
    total_deleted = sum(stats.get("files_deleted", 0) for stats in all_stats.values())
    if total_deleted > 0:
        print(f"  - Total files deleted: {total_deleted}")
    
    total_ops = total_created + total_overwritten + total_deleted
    print(f"  - Total operations: {total_ops}")

    if all_stats:
        print(f"\nPer-Repository Details:")
        for repo, stats in all_stats.items():
            ops = stats["files_created"] + stats["files_overwritten"] + stats.get("files_deleted", 0)
            if ops > 0:
                print(f"  {repo}:")
                print(f"    Platform: {stats['platform']}")
                print(f"    Created: {stats['files_created']}, Updated: {stats['files_overwritten']}", end="")
                if stats.get("files_deleted", 0) > 0:
                    print(f", Deleted: {stats['files_deleted']}")
                else:
                    print()

    if failed_repos:
        print(f"\nFailed Repositories ({len(failed_repos)}):")
        for repo in failed_repos:
            print(f"  - {repo}")
        sys.exit(1)

    print(f"\n{'=' * 70}")
    sys.exit(0)


if __name__ == "__main__":
    main()
