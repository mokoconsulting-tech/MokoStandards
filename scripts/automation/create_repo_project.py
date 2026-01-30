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
PATH: /scripts/create_repo_project.py
VERSION: 01.00.00
BRIEF: Create a smart GitHub Project for a specific repository
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))
sys.path.insert(0, str(Path(__file__).parent / "run"))

try:
    from setup_github_project_v2 import GitHubProjectV2Setup
except ImportError:
    print("ERROR: Could not import GitHubProjectV2Setup")
    print("Make sure setup_github_project_v2.py is in scripts/run/ directory")
    sys.exit(1)


class RepoProjectCreator:
    """Create a GitHub Project for a specific repository based on its type."""

    def __init__(self, org: str, repo_name: str, project_type: str,
                 token: str = None, verbose: bool = False, dry_run: bool = False):
        self.org = org
        self.repo_name = repo_name
        self.project_type = project_type
        self.token = token
        self.verbose = verbose
        self.dry_run = dry_run

    def log_verbose(self, message: str):
        """Print verbose log message."""
        if self.verbose:
            print(f"[VERBOSE] {message}")

    def load_project_config(self) -> dict:
        """Load project configuration template."""
        templates_dir = Path(__file__).parent.parent / "templates" / "projects"
        config_file = templates_dir / f"{self.project_type}-project-config.json"

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.log_verbose(f"Loaded config from {config_file}")
                return config
        except Exception as e:
            print(f"ERROR: Could not load config for {self.project_type}: {e}")
            return None

    def create_custom_fields(self, setup: GitHubProjectV2Setup, config: dict) -> bool:
        """Create custom fields from config."""
        print(f"\n📋 Creating custom fields for {self.project_type} project...")

        custom_fields = config.get("custom_fields", [])

        for field in custom_fields:
            field_name = field.get("name")
            field_type = field.get("type")

            if field_type == "single_select":
                options = field.get("options", [])
                field_id = setup.create_single_select_field(field_name, options)
            elif field_type == "text":
                field_id = setup.create_text_field(field_name)
            elif field_type == "number":
                # Note: Number fields require additional handling
                self.log_verbose(f"Number fields not yet implemented: {field_name}")
                continue
            else:
                self.log_verbose(f"Unknown field type {field_type} for {field_name}")
                continue

            if field_id:
                setup.field_ids[field_name] = field_id
            else:
                print(f"  ❌ Failed to create field: {field_name}")
                return False

        print(f"✅ Created {len(setup.field_ids)} custom fields")
        return True

    def create_project(self) -> bool:
        """Create the GitHub Project."""
        print(f"\n{'='*70}")
        print(f"Creating {self.project_type.capitalize()} Project for {self.repo_name}")
        print(f"{'='*70}")

        if self.dry_run:
            print("\n[DRY RUN MODE - No actual changes will be made]")

        # Load configuration
        config = self.load_project_config()
        if not config:
            return False

        # Customize project title
        project_title = f"{self.repo_name} - {config['project']['name']}"

        # Initialize project setup
        setup = GitHubProjectV2Setup(
            org=self.org,
            project_title=project_title,
            token=self.token,
            verbose=self.verbose
        )

        # Verify authentication
        print("\n🔐 Verifying authentication...")
        if not setup.verify_auth():
            print("❌ Authentication failed")
            return False

        # Get organization ID
        print(f"\n🏢 Getting organization ID for {self.org}...")
        org_id = setup.get_org_id()
        if not org_id:
            print("❌ Failed to get organization ID")
            return False

        if self.dry_run:
            print(f"\n[DRY RUN] Would create project: {project_title}")
            print(f"[DRY RUN] Project type: {self.project_type}")
            print(f"[DRY RUN] Custom fields: {len(config.get('custom_fields', []))}")
            print(f"[DRY RUN] Views: {len(config.get('views', []))}")
            return True

        # Create project
        print(f"\n📁 Creating project...")
        if not setup.create_project(org_id):
            print("❌ Failed to create project")
            return False

        # Create custom fields
        if not self.create_custom_fields(setup, config):
            print("❌ Failed to create custom fields")
            return False

        # Document views (views must be created manually via UI)
        print("\n👁️  Documenting project views...")
        views = config.get("views", [])
        for view in views:
            print(f"  - {view.get('name')} ({view.get('layout')})")
            print(f"    {view.get('description')}")

        print("\n✅ Project created successfully!")
        print(f"\nView your project at:")
        print(f"https://github.com/orgs/{self.org}/projects/{setup.project_number}")

        print("\nℹ️  Next steps:")
        print("  1. Create views manually in the GitHub UI")
        print("  2. Add initial issues/tasks to the project")
        print("  3. Configure project automations")

        return True


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Create a smart GitHub Project for a specific repository'
    )
    parser.add_argument(
        'repo_name',
        help='Repository name'
    )
    parser.add_argument(
        '--org',
        default='mokoconsulting-tech',
        help='GitHub organization name (default: mokoconsulting-tech)'
    )
    parser.add_argument(
        '--type',
        choices=['joomla', 'dolibarr', 'generic'],
        required=True,
        help='Project type (joomla, dolibarr, or generic)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )

    args = parser.parse_args()

    # Get token from environment
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")

    if not token and not args.dry_run:
        print("❌ GitHub token required. Set GH_PAT or GITHUB_TOKEN environment variable")
        print("   Or authenticate with: gh auth login")
        sys.exit(1)

    # Create project
    creator = RepoProjectCreator(
        org=args.org,
        repo_name=args.repo_name,
        project_type=args.type,
        token=token,
        verbose=args.verbose,
        dry_run=args.dry_run
    )

    success = creator.create_project()

    if success:
        print("\n✅ Done!")
        sys.exit(0)
    else:
        print("\n❌ Failed to create project")
        sys.exit(1)


if __name__ == "__main__":
    main()
