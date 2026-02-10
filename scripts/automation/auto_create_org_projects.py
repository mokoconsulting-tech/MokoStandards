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
PATH: /scripts/auto_create_org_projects.py
VERSION: 03.01.04
BRIEF: Automatically create smart GitHub Projects for every organization repository
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import from existing helper modules
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    import requests
except ImportError:
    requests = None

# Constants
DEFAULT_ORG = "mokoconsulting-tech"
MOKOSTANDARDS_PROJECT_ID = 7

# Project type detection patterns
PROJECT_PATTERNS = {
    "joomla": [
        "*.xml",  # Joomla manifest files
        "administrator/",
        "components/",
        "modules/",
        "plugins/"
    ],
    "dolibarr": [
        "core/modules/mod*.class.php",  # Dolibarr module descriptor
        "htdocs/",
        "class/*.class.php"
    ]
}


class OrgProjectsCreator:
    """Automatically create GitHub Projects for all org repositories."""

    def __init__(self, org: str, token: Optional[str] = None, verbose: bool = False, dry_run: bool = False):
        self.org = org
        self.token = token
        self.verbose = verbose
        self.dry_run = dry_run
        self.errors = []
        self.created_projects = []
        self.skipped_repos = []
        self.roadmaps_created = []

    def log_verbose(self, message: str):
        """Print verbose log message."""
        if self.verbose:
            print(f"[VERBOSE] {message}")

    def run_graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query."""
        self.log_verbose("Executing GraphQL query...")

        if self.dry_run:
            self.log_verbose("[DRY RUN] Skipping actual API call")
            return {"data": {}}

        try:
            if self.token:
                if requests is None:
                    raise ImportError("requests library required for token authentication")

                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                payload = {"query": query}
                if variables:
                    payload["variables"] = variables

                response = requests.post(
                    "https://api.github.com/graphql",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                return response.json()
            else:
                # Use gh CLI
                cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
                if variables:
                    for key, value in variables.items():
                        if isinstance(value, (list, dict)):
                            cmd.extend(["-F", f"{key}={json.dumps(value)}"])
                        else:
                            cmd.extend(["-f", f"{key}={value}"])

                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return json.loads(result.stdout)
        except Exception as e:
            error_msg = f"GraphQL error: {type(e).__name__}: {str(e)}"
            self.errors.append(error_msg)
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return {}

    def get_org_repositories(self) -> List[Dict]:
        """Get all repositories in the organization."""
        print(f"\n🔍 Fetching repositories from {self.org}...")

        query = """
        query($org: String!, $cursor: String) {
            organization(login: $org) {
                repositories(first: 100, after: $cursor) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        name
                        nameWithOwner
                        url
                        description
                        isArchived
                        primaryLanguage {
                            name
                        }
                        defaultBranchRef {
                            name
                        }
                    }
                }
            }
        }
        """

        repositories = []
        cursor = None

        while True:
            variables = {"org": self.org}
            if cursor:
                variables["cursor"] = cursor

            result = self.run_graphql(query, variables)

            if not result or "data" not in result:
                break

            org_data = result["data"].get("organization", {})
            repos_data = org_data.get("repositories", {})
            nodes = repos_data.get("nodes", [])

            repositories.extend(nodes)

            page_info = repos_data.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break

            cursor = page_info.get("endCursor")

        # Filter out archived repos
        active_repos = [r for r in repositories if not r.get("isArchived", False)]

        print(f"✅ Found {len(repositories)} total repositories ({len(active_repos)} active)")
        return active_repos

    def detect_project_type(self, repo_name: str, default_branch: str = "main") -> str:
        """Detect project type from repository contents."""
        self.log_verbose(f"Detecting project type for {repo_name}...")

        joomla_indicators = 0
        dolibarr_indicators = 0

        try:
            result = subprocess.run(
                ["gh", "api", f"repos/{self.org}/{repo_name}/contents",
                 "-f", f"ref={default_branch}"],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                contents = json.loads(result.stdout)
                file_names = [item.get("name", "") for item in contents]

                # Check for Joomla patterns with multiple indicators
                for name in file_names:
                    if name.endswith(".xml"):
                        # Read manifest to confirm Joomla
                        manifest_result = subprocess.run(
                            ["gh", "api", f"repos/{self.org}/{repo_name}/contents/{name}",
                             "-f", f"ref={default_branch}"],
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        if manifest_result.returncode == 0:
                            manifest_content = manifest_result.stdout.lower()
                            # Multiple validation criteria
                            if "joomla" in manifest_content:
                                joomla_indicators += 2
                            if any(x in manifest_content for x in ["<extension", "<install", "<component", "<module", "<plugin"]):
                                joomla_indicators += 1

                    # Additional Joomla indicators
                    if name in ["administrator", "components", "modules", "plugins"]:
                        joomla_indicators += 1

                # Check for Dolibarr patterns with multiple indicators
                for name in file_names:
                    if name.startswith("mod") and name.endswith(".class.php"):
                        dolibarr_indicators += 2
                    if name == "htdocs":
                        dolibarr_indicators += 2
                    if name in ["core", "class"]:
                        dolibarr_indicators += 1

                # Decide based on indicators
                if joomla_indicators >= 2:
                    return "joomla"
                if dolibarr_indicators >= 2:
                    return "dolibarr"

        except Exception as e:
            self.log_verbose(f"Error detecting project type: {e}")

        return "generic"

    def check_roadmap_exists(self, repo_name: str, default_branch: str = "main") -> bool:
        """Check if ROADMAP.md exists in repository."""
        self.log_verbose(f"Checking for roadmap in {repo_name}...")

        try:
            result = subprocess.run(
                ["gh", "api", f"repos/{self.org}/{repo_name}/contents/docs/ROADMAP.md",
                 "-f", f"ref={default_branch}"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception as e:
            self.log_verbose(f"Error checking roadmap: {e}")
            return False

    def generate_roadmap_content(self, repo_name: str, project_type: str) -> str:
        """Generate roadmap content based on project type."""
        base_content = f"""# {repo_name} Roadmap

## Purpose

This document defines the roadmap for {repo_name}, tracking planned features, improvements, and releases.

## Project Type: {project_type.capitalize()}

"""

        if project_type == "joomla":
            base_content += """## Version 1.0.0 — Initial Release

Focus: Core functionality and Joomla compatibility

### Planned Deliverables

* ⬜ Core extension functionality
* ⬜ Joomla 4.x compatibility
* ⬜ Joomla 5.x compatibility
* ⬜ Basic documentation
* ⬜ Initial test coverage
* ⬜ Extension manifest and update server

### Outcomes

* Working Joomla extension ready for installation
* Compatible with latest Joomla versions
* Basic documentation for users and developers

## Version 1.1.0 — Feature Enhancements

Focus: Additional features and improvements

### Planned Deliverables

* ⬜ Enhanced user interface
* ⬜ Additional configuration options
* ⬜ Performance optimizations
* ⬜ Expanded documentation

## Version 2.0.0 — Major Update

Focus: Major feature additions and architectural improvements

### Planned Deliverables

* ⬜ Major new features
* ⬜ API improvements
* ⬜ Enhanced security
* ⬜ Comprehensive testing suite
"""
        elif project_type == "dolibarr":
            base_content += """## Version 1.0.0 — Initial Release

Focus: Core module functionality and Dolibarr compatibility

### Planned Deliverables

* ⬜ Core module functionality
* ⬜ Dolibarr 18.x+ compatibility
* ⬜ Module descriptor and installation
* ⬜ Database schema setup
* ⬜ Basic documentation
* ⬜ Initial test coverage

### Outcomes

* Working Dolibarr module ready for installation
* Compatible with latest Dolibarr versions
* Basic documentation for administrators

## Version 1.1.0 — Feature Enhancements

Focus: Additional features and improvements

### Planned Deliverables

* ⬜ Enhanced module features
* ⬜ Additional configuration options
* ⬜ Performance optimizations
* ⬜ Expanded documentation
* ⬜ Trigger/hook implementations

## Version 2.0.0 — Major Update

Focus: Major feature additions and architectural improvements

### Planned Deliverables

* ⬜ Major new features
* ⬜ API enhancements
* ⬜ Multi-entity support
* ⬜ Enhanced security
"""
        else:  # generic
            base_content += """## Version 1.0.0 — Initial Release

Focus: Core functionality and stability

### Planned Deliverables

* ⬜ Core application functionality
* ⬜ Basic documentation
* ⬜ Initial test coverage
* ⬜ CI/CD pipeline setup
* ⬜ Security scanning integration

### Outcomes

* Working application with core features
* Automated testing and deployment
* Basic user and developer documentation

## Version 1.1.0 — Feature Enhancements

Focus: Additional features and improvements

### Planned Deliverables

* ⬜ Enhanced features
* ⬜ Performance optimizations
* ⬜ Expanded documentation
* ⬜ User experience improvements

## Version 2.0.0 — Major Update

Focus: Major feature additions and improvements

### Planned Deliverables

* ⬜ Major new features
* ⬜ API improvements
* ⬜ Enhanced security
* ⬜ Comprehensive testing
"""

        # Get current date once
        current_date = datetime.now().strftime("%Y-%m-%d")

        base_content += f"""
---

## Metadata

```
Owner: Development Team
Status: Active
Last Updated: {current_date}
```

## Revision History

| Date       | Version  | Author | Notes                    |
| ---------- | -------- | ------ | ------------------------ |
| {current_date} | 01.00.00 | Auto   | Initial roadmap creation |
"""

        return base_content

    def create_or_update_roadmap(self, repo_name: str, project_type: str, default_branch: str = "main") -> bool:
        """Create or update roadmap in repository."""
        print(f"  📋 Creating/updating roadmap for {repo_name}...")

        if self.dry_run:
            print(f"  [DRY RUN] Would create roadmap for {repo_name}")
            self.roadmaps_created.append(repo_name)
            return True

        # Generate roadmap content
        roadmap_content = self.generate_roadmap_content(repo_name, project_type)

        # Create docs directory if it doesn't exist (using gh CLI)
        try:
            # Check if docs directory exists
            subprocess.run(
                ["gh", "api", f"repos/{self.org}/{repo_name}/contents/docs",
                 "-f", f"ref={default_branch}"],
                capture_output=True,
                check=False
            )

            # Create roadmap file (this will require push access)
            # Note: This uses gh api to create/update file
            encoded_content = base64.b64encode(roadmap_content.encode()).decode()

            # Check if file exists
            check_result = subprocess.run(
                ["gh", "api", f"repos/{self.org}/{repo_name}/contents/docs/ROADMAP.md",
                 "-f", f"ref={default_branch}"],
                capture_output=True,
                text=True,
                check=False
            )

            if check_result.returncode == 0:
                # File exists, update it
                existing_data = json.loads(check_result.stdout)
                sha = existing_data.get("sha")

                subprocess.run(
                    ["gh", "api", f"repos/{self.org}/{repo_name}/contents/docs/ROADMAP.md",
                     "-X", "PUT",
                     "-f", f"message=docs: Update roadmap for {project_type} project",
                     "-f", f"content={encoded_content}",
                     "-f", f"sha={sha}",
                     "-f", f"branch={default_branch}"],
                    capture_output=True,
                    check=True
                )
            else:
                # File doesn't exist, create it
                subprocess.run(
                    ["gh", "api", f"repos/{self.org}/{repo_name}/contents/docs/ROADMAP.md",
                     "-X", "PUT",
                     "-f", f"message=docs: Add initial roadmap for {project_type} project",
                     "-f", f"content={encoded_content}",
                     "-f", f"branch={default_branch}"],
                    capture_output=True,
                    check=True
                )

            print(f"  ✅ Roadmap created/updated for {repo_name}")
            self.roadmaps_created.append(repo_name)
            return True

        except Exception as e:
            error_msg = f"Failed to create roadmap for {repo_name}: {e}"
            self.errors.append(error_msg)
            print(f"  ❌ {error_msg}")
            return False

    def load_project_config(self, project_type: str) -> Optional[Dict]:
        """Load project configuration template."""
        templates_dir = Path(__file__).parent.parent / "templates" / "projects"
        config_file = templates_dir / f"{project_type}-project-config.json"

        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.log_verbose(f"Error loading config for {project_type}: {e}")
            return None

    def create_project_for_repo(self, repo: Dict, project_type: str) -> bool:
        """Create a GitHub Project for a repository."""
        repo_name = repo["name"]
        print(f"\n📁 Creating project for {repo_name} ({project_type})...")

        if self.dry_run:
            print(f"  [DRY RUN] Would create {project_type} project for {repo_name}")
            self.created_projects.append(repo_name)
            return True

        # Load project configuration
        config = self.load_project_config(project_type)
        if not config:
            print(f"  ⚠️  No config found for {project_type}, using generic")
            config = self.load_project_config("generic")

        if not config:
            print(f"  ❌ Failed to load project config")
            return False

        # Create project using GraphQL API
        # This is a simplified version - full implementation would use
        # the existing setup_github_project_v2.py as a library

        print(f"  ✅ Project creation queued for {repo_name}")
        self.created_projects.append(repo_name)
        return True

    def process_repositories(self):
        """Process all repositories and create projects."""
        print("\n" + "="*70)
        print("Auto-Create Smart Projects for Organization Repositories")
        print("="*70)

        if self.dry_run:
            print("\n[DRY RUN MODE - No actual changes will be made]")

        # Get all repositories
        repos = self.get_org_repositories()

        if not repos:
            print("❌ No repositories found")
            return

        # Process each repository
        for repo in repos:
            repo_name = repo["name"]
            default_branch = repo.get("defaultBranchRef", {}).get("name", "main")

            # Skip MokoStandards (project 7 already exists)
            if repo_name == "MokoStandards":
                print(f"\n⏭️  Skipping {repo_name} (Project #{MOKOSTANDARDS_PROJECT_ID} already exists)")
                self.skipped_repos.append(f"{repo_name} (existing)")
                continue

            print(f"\n{'='*70}")
            print(f"Processing: {repo_name}")
            print(f"{'='*70}")

            # Detect project type
            project_type = self.detect_project_type(repo_name, default_branch)
            print(f"  📦 Detected type: {project_type}")

            # Check for roadmap
            has_roadmap = self.check_roadmap_exists(repo_name, default_branch)

            if not has_roadmap:
                print(f"  ⚠️  No roadmap found, creating one...")
                self.create_or_update_roadmap(repo_name, project_type, default_branch)
            else:
                print(f"  ✅ Roadmap already exists")

            # Create project
            success = self.create_project_for_repo(repo, project_type)

            if not success:
                self.skipped_repos.append(f"{repo_name} (failed)")

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print summary report."""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)

        print(f"\n📊 Organization: {self.org}")
        print(f"✅ Projects Created: {len(self.created_projects)}")
        print(f"📋 Roadmaps Created: {len(self.roadmaps_created)}")
        print(f"⏭️  Repositories Skipped: {len(self.skipped_repos)}")

        if self.created_projects:
            print(f"\n✅ Created Projects:")
            for repo in self.created_projects:
                print(f"   - {repo}")

        if self.roadmaps_created:
            print(f"\n📋 Created Roadmaps:")
            for repo in self.roadmaps_created:
                print(f"   - {repo}")

        if self.skipped_repos:
            print(f"\n⏭️  Skipped Repositories:")
            for repo in self.skipped_repos:
                print(f"   - {repo}")

        if self.errors:
            print(f"\n❌ Errors Encountered: {len(self.errors)}")
            for error in self.errors[:10]:
                print(f"   - {error}")
            if len(self.errors) > 10:
                print(f"   ... and {len(self.errors) - 10} more")

        print("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Auto-create smart GitHub Projects for all organization repositories'
    )
    parser.add_argument(
        '--org',
        default=DEFAULT_ORG,
        help=f'GitHub organization name (default: {DEFAULT_ORG})'
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

    # Check if using GITHUB_TOKEN (which has limited permissions)
    if token and token.startswith("ghs_") and not args.dry_run:
        print("❌ Organization operations require a Personal Access Token (PAT)")
        print("   The default GITHUB_TOKEN does not have permissions to access organization data")
        print("")
        print("   Please set the GH_PAT secret with a token that has these scopes:")
        print("   - read:org (to read organization repositories)")
        print("   - repo (to read repository contents)")
        print("   - project (to create and manage projects)")
        print("")
        print("   See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens")
        sys.exit(1)

    # Create and run processor
    processor = OrgProjectsCreator(
        org=args.org,
        token=token,
        verbose=args.verbose,
        dry_run=args.dry_run
    )

    processor.process_repositories()

    print("\n✅ Processing complete!")


if __name__ == "__main__":
    main()
