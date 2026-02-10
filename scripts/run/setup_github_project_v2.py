#!/usr/bin/env python3
# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Automation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/run/setup_github_project_v2.py
# VERSION: 03.01.03
# BRIEF: GitHub Project v2 setup automation - creates documentation control register
# PATH: /scripts/run/setup_github_project_v2.py
# NOTE: Creates project, custom fields, and populates items from repository scan
"""
GitHub Project v2 Setup Script
Creates a GitHub Project v2 and populates it with documentation tasks.

Usage:
    export GH_PAT="your_personal_access_token"
    python3 scripts/run/setup_github_project_v2.py

    With verbose logging:
    python3 scripts/run/setup_github_project_v2.py --verbose

    Skip view creation:
    python3 scripts/run/setup_github_project_v2.py --skip-views

Or use gh CLI authentication:
    gh auth login
    python3 scripts/run/setup_github_project_v2.py
"""

import argparse
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import requests for API calls with try/except for clearer error messaging
try:
    import requests
except ImportError:
    requests = None  # Will be checked when needed


class GitHubProjectV2Setup:
    """Handles GitHub Project v2 creation and population."""

    def __init__(self, org: str, project_title: str, token: Optional[str] = None, verbose: bool = False):
        self.org = org
        self.project_title = project_title
        self.token = token
        self.verbose = verbose
        self.project_id = None
        self.project_number = None
        self.field_ids = {}
        self.field_option_ids = {}
        self.created_items = []
        self.skipped_items = []
        self.errors = []
        self.view_ids = {}

    def log_verbose(self, message: str):
        """Print verbose log message."""
        if self.verbose:
            print(f"[VERBOSE] {message}")

    def run_graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query using gh CLI or direct API."""
        self.log_verbose("Executing GraphQL query...")
        if variables and self.verbose:
            self.log_verbose(f"Variables: {json.dumps(variables, indent=2)}")

        try:
            if self.token:
                # Use direct API call with token
                if requests is None:
                    error_msg = (
                        "requests library is required for token authentication. "
                        "Please install the 'requests' package for your Python 3 environment "
                        "(for example: pip3 install requests)."
                    )
                    self.errors.append(error_msg)
                    print(f"ERROR: {error_msg}", file=sys.stderr)
                    return {}

                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                payload = {"query": query}
                if variables:
                    payload["variables"] = variables

                self.log_verbose("Making API request to GitHub GraphQL endpoint...")

                response = requests.post(
                    "https://api.github.com/graphql",
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                self.log_verbose(f"Response status code: {response.status_code}")
                response.raise_for_status()
                result = response.json()

                if "errors" in result and self.verbose:
                    self.log_verbose(f"GraphQL errors in response: {json.dumps(result['errors'], indent=2)}")

                return result
            else:
                # Use gh CLI
                cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
                if variables:
                    for key, value in variables.items():
                        if isinstance(value, (list, dict)):
                            cmd.extend(["-F", f"{key}={json.dumps(value)}"])
                        else:
                            cmd.extend(["-f", f"{key}={value}"])

                self.log_verbose("Running gh CLI command...")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                response_data = json.loads(result.stdout)

                if "errors" in response_data and self.verbose:
                    self.log_verbose(f"GraphQL errors in response: {json.dumps(response_data['errors'], indent=2)}")

                return response_data
        except subprocess.CalledProcessError as e:
            error_msg = f"GraphQL subprocess error: {e.stderr}"
            error_details = {
                "command": e.cmd,
                "return_code": e.returncode,
                "stderr": e.stderr,
                "stdout": e.stdout
            }
            self.errors.append(error_details)
            print(f"ERROR: {error_msg}", file=sys.stderr)
            if self.verbose:
                self.log_verbose(f"Error details: {json.dumps(error_details, indent=2)}")
            return {}
        except Exception as e:
            error_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"
            error_details = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "query_snippet": query[:200] + "..." if len(query) > 200 else query
            }
            self.errors.append(error_details)
            print(f"ERROR: {error_msg}", file=sys.stderr)
            if self.verbose:
                self.log_verbose(f"Error details: {json.dumps(error_details, indent=2)}")
                self.log_verbose(f"Traceback:\n{traceback.format_exc()}")
            return {}

    def verify_auth(self) -> bool:
        """Verify GitHub CLI authentication or token."""
        if self.token:
            print(f"✅ Using GH_PAT token (length: {len(self.token)})")
            # Verify token works
            try:
                result = self.run_graphql("query { viewer { login } }")
                if result and "data" in result and result["data"].get("viewer"):
                    print(f"✅ Authenticated as: {result['data']['viewer']['login']}")
                    return True
                else:
                    print("❌ Token authentication failed")
                    return False
            except Exception as e:
                print(f"❌ Token verification failed: {e}")
                return False
        else:
            try:
                result = subprocess.run(
                    ["gh", "auth", "status"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    print("✅ GitHub CLI authenticated")
                    return True
                else:
                    print("❌ GitHub CLI not authenticated")
                    print("Please run: gh auth login OR set GH_PAT environment variable")
                    return False
            except Exception as e:
                print(f"❌ Error checking auth: {e}")
                return False

    def get_org_id(self) -> Optional[str]:
        """Get organization ID."""
        query = """
        query($org: String!) {
            organization(login: $org) {
                id
            }
        }
        """
        result = self.run_graphql(query, {"org": self.org})
        if result and "data" in result and result["data"].get("organization"):
            org_id = result["data"]["organization"]["id"]
            print(f"✅ Organization ID: {org_id}")
            return org_id
        else:
            print(f"❌ Failed to get organization ID")
            return None

    def create_project(self, org_id: str) -> bool:
        """Create GitHub Project v2."""
        mutation = """
        mutation($orgId: ID!, $title: String!) {
            createProjectV2(input: {ownerId: $orgId, title: $title}) {
                projectV2 {
                    id
                    number
                    title
                    url
                }
            }
        }
        """
        result = self.run_graphql(mutation, {"orgId": org_id, "title": self.project_title})

        if result and "data" in result and result["data"].get("createProjectV2"):
            project = result["data"]["createProjectV2"]["projectV2"]
            self.project_id = project["id"]
            self.project_number = project["number"]
            print(f"✅ Created Project: {project['title']}")
            print(f"   Project Number: {self.project_number}")
            print(f"   Project ID: {self.project_id}")
            print(f"   URL: {project.get('url', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to create project")
            if result and "errors" in result:
                for error in result["errors"]:
                    print(f"   Error: {error.get('message', error)}")
            return False

    def create_single_select_field(self, name: str, options: List[str]) -> Optional[str]:
        """Create a single-select field."""
        mutation = """
        mutation($projectId: ID!, $name: String!, $options: [ProjectV2SingleSelectFieldOptionInput!]!) {
            createProjectV2Field(input: {
                projectId: $projectId,
                dataType: SINGLE_SELECT,
                name: $name,
                singleSelectOptions: $options
            }) {
                projectV2Field {
                    ... on ProjectV2SingleSelectField {
                        id
                        name
                        options {
                            id
                            name
                        }
                    }
                }
            }
        }
        """

        option_list = [{"name": opt} for opt in options]

        result = self.run_graphql(mutation, {
            "projectId": self.project_id,
            "name": name,
            "options": option_list
        })

        if result and "data" in result and result["data"].get("createProjectV2Field"):
            field_data = result["data"]["createProjectV2Field"]["projectV2Field"]
            field_id = field_data["id"]

            # Store option IDs for later use
            if "options" in field_data:
                self.field_option_ids[name] = {
                    opt["name"]: opt["id"] for opt in field_data["options"]
                }

            print(f"  ✅ Created field: {name} ({len(options)} options)")
            return field_id
        else:
            print(f"  ❌ Failed to create field: {name}")
            if result and "errors" in result:
                for error in result["errors"]:
                    print(f"     Error: {error.get('message', error)}")
            return None

    def create_text_field(self, name: str) -> Optional[str]:
        """Create a text field."""
        mutation = """
        mutation($projectId: ID!, $name: String!) {
            createProjectV2Field(input: {
                projectId: $projectId,
                dataType: TEXT,
                name: $name
            }) {
                projectV2Field {
                    ... on ProjectV2Field {
                        id
                        name
                    }
                }
            }
        }
        """

        result = self.run_graphql(mutation, {
            "projectId": self.project_id,
            "name": name
        })

        if result and "data" in result and result["data"].get("createProjectV2Field"):
            field_id = result["data"]["createProjectV2Field"]["projectV2Field"]["id"]
            print(f"  ✅ Created field: {name}")
            return field_id
        else:
            print(f"  ❌ Failed to create field: {name}")
            if result and "errors" in result:
                for error in result["errors"]:
                    print(f"     Error: {error.get('message', error)}")
            return None

    def create_all_fields(self) -> bool:
        """Create all custom fields."""
        print("\n📋 Creating custom fields...")

        # Single-select fields (as per requirements)
        single_select_fields = {
            "Status": ["Planned", "In Progress", "In Review", "Approved", "Published", "Blocked", "Archived"],
            "Priority": ["High", "Medium", "Low"],
            "Risk Level": ["High", "Medium", "Low"],
            "Document Type": ["policy", "guide", "checklist", "overview", "index"],
            "Document Subtype": ["core", "waas", "catalog", "guide", "policy"],
            "Owner Role": ["Documentation Owner", "Governance Owner", "Security Owner", "Operations Owner", "Release Owner"],
            "Approval Required": ["Yes", "No"],
            "Evidence Required": ["Yes", "No"],
            "Review Cycle": ["Annual", "Semiannual", "Quarterly", "Ad hoc"],
            "Retention": ["Indefinite", "7 Years", "5 Years", "3 Years"],
        }

        for field_name, options in single_select_fields.items():
            field_id = self.create_single_select_field(field_name, options)
            if field_id:
                self.field_ids[field_name] = field_id
            else:
                print(f"❌ STOP: Failed to create field '{field_name}'")
                return False

        # Text fields (as per requirements)
        text_fields = [
            "Document Path",
            "Dependencies",
            "Acceptance Criteria",
            "RACI",
            "KPIs"
        ]

        for field_name in text_fields:
            field_id = self.create_text_field(field_name)
            if field_id:
                self.field_ids[field_name] = field_id
            else:
                print(f"❌ STOP: Failed to create field '{field_name}'")
                return False

        print(f"\n✅ Created {len(self.field_ids)} custom fields")
        print("\nℹ️  Optional: You can add multi-select fields such as 'Compliance Tags'")
        print("    and 'Evidence Artifacts' manually in the GitHub UI (not managed by this script).")

        return True

    def scan_repository(self, repo_path: Path) -> List[Tuple[Path, str]]:
        """Scan repository for documentation files."""
        print("\n🔍 Scanning repository...")

        docs_path = repo_path / "docs"
        templates_path = repo_path / "templates"

        files = []

        # Scan docs directory
        if docs_path.exists():
            for md_file in docs_path.rglob("*.md"):
                rel_path = md_file.relative_to(repo_path)
                files.append((rel_path, "Documentation"))

        # Scan templates directory
        if templates_path.exists():
            for md_file in templates_path.rglob("*.md"):
                rel_path = md_file.relative_to(repo_path)
                files.append((rel_path, "Template"))

        print(f"✅ Found {len(files)} documents")
        return sorted(files)

    def infer_document_type(self, path: Path) -> str:
        """Infer document type from path."""
        path_str = str(path).lower()
        if "/policy/" in path_str:
            return "policy"
        elif "/guide/" in path_str:
            return "guide"
        elif "/checklist/" in path_str:
            return "checklist"
        elif path.name.lower() in ["index.md", "readme.md"]:
            return "index"
        elif "overview" in path_str:
            return "overview"
        else:
            return "guide"

    def infer_document_subtype(self, path: Path, doc_type: str) -> str:
        """Infer document subtype from path."""
        path_str = str(path).lower()
        if "/waas/" in path_str:
            return "waas"
        elif "/templates/" in path_str:
            return "catalog"
        elif doc_type == "policy":
            return "policy"
        elif doc_type == "guide":
            return "guide"
        else:
            return "core"

    def get_approval_required(self, doc_type: str) -> str:
        """Determine if approval is required."""
        return "Yes" if doc_type == "policy" else "No"

    def create_project_item(self, file_path: Path, purpose: str) -> bool:
        """Create a project item for a document."""
        title = file_path.stem

        doc_type = self.infer_document_type(file_path)
        doc_subtype = self.infer_document_subtype(file_path, doc_type)
        approval_required = self.get_approval_required(doc_type)

        body = f"""Document Path: {file_path}
Purpose: {purpose} tracking
Source: Imported from repository scan"""

        mutation = """
        mutation($projectId: ID!, $title: String!, $body: String!) {
            addProjectV2DraftIssue(input: {
                projectId: $projectId,
                title: $title,
                body: $body
            }) {
                projectItem {
                    id
                }
            }
        }
        """

        result = self.run_graphql(mutation, {
            "projectId": self.project_id,
            "title": title,
            "body": body
        })

        if result and "data" in result and result["data"].get("addProjectV2DraftIssue"):
            item_id = result["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
            self.created_items.append(str(file_path))

            # Set field values for the item
            self.set_item_fields(item_id, file_path, doc_type, doc_subtype, approval_required)

            return True
        else:
            self.skipped_items.append(str(file_path))
            return False

    def set_item_fields(self, item_id: str, file_path: Path, doc_type: str,
                       doc_subtype: str, approval_required: str):
        """Set field values for a project item."""
        # Set Document Path (text field)
        if "Document Path" in self.field_ids:
            self.set_text_field(item_id, "Document Path", str(file_path))

        # Set single-select fields
        field_values = {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Low",
            "Document Type": doc_type,
            "Document Subtype": doc_subtype,
            "Owner Role": "Documentation Owner",
            "Approval Required": approval_required,
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite"
        }

        for field_name, value in field_values.items():
            if field_name in self.field_ids and field_name in self.field_option_ids:
                option_id = self.field_option_ids[field_name].get(value)
                if option_id:
                    self.set_single_select_field(item_id, field_name, option_id)

    def set_text_field(self, item_id: str, field_name: str, value: str):
        """Set a text field value."""
        mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
            updateProjectV2ItemFieldValue(input: {
                projectId: $projectId,
                itemId: $itemId,
                fieldId: $fieldId,
                value: {
                    text: $value
                }
            }) {
                projectItem {
                    id
                }
            }
        }
        """

        self.run_graphql(mutation, {
            "projectId": self.project_id,
            "itemId": item_id,
            "fieldId": self.field_ids[field_name],
            "value": value
        })

    def set_single_select_field(self, item_id: str, field_name: str, option_id: str):
        """Set a single-select field value."""
        mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
            updateProjectV2ItemFieldValue(input: {
                projectId: $projectId,
                itemId: $itemId,
                fieldId: $fieldId,
                value: {
                    singleSelectOptionId: $optionId
                }
            }) {
                projectItem {
                    id
                }
            }
        }
        """

        self.run_graphql(mutation, {
            "projectId": self.project_id,
            "itemId": item_id,
            "fieldId": self.field_ids[field_name],
            "optionId": option_id
        })

    def populate_project(self, repo_path: Path) -> bool:
        """Populate project with documentation items."""
        print("\n📝 Creating project items...")

        files = self.scan_repository(repo_path)

        total = len(files)
        for idx, (file_path, purpose) in enumerate(files, 1):
            success = self.create_project_item(file_path, purpose)
            if success:
                print(f"  [{idx}/{total}] ✅ {file_path}")
            else:
                print(f"  [{idx}/{total}] ⚠️  Skipped: {file_path}")
                self.log_verbose(f"Skipped item details: {file_path}")

        print(f"\n✅ Created {len(self.created_items)} items")
        if self.skipped_items:
            print(f"⚠️  Skipped {len(self.skipped_items)} items")
            if self.verbose:
                self.log_verbose("Skipped items list:")
                for item in self.skipped_items:
                    self.log_verbose(f"  - {item}")

        return True

    def create_project_views(self) -> bool:
        """Create project views (Board, Table, Roadmap).

        Note: GitHub Projects v2 API has limitations for view creation.
        This method documents the views that should be created manually.
        """
        print("\n👁️  Creating project views...")
        print("⚠️  Note: GitHub Projects v2 API has limited support for programmatic view creation.")
        print("   The following views should be created manually in the GitHub UI:")

        views_to_document = [
            {
                "name": "Documentation Board",
                "layout": "BOARD",
                "description": "Board view organized by status for visual task management",
                "group_by": "Status"
            },
            {
                "name": "Documentation Table",
                "layout": "TABLE",
                "description": "Table view with all fields for detailed overview",
                "fields": "All custom fields"
            },
            {
                "name": "Documentation Roadmap",
                "layout": "ROADMAP",
                "description": "Roadmap view for timeline planning",
                "date_field": "Review Cycle or custom date field"
            }
        ]

        for idx, view_config in enumerate(views_to_document, 1):
            print(f"\n  {idx}. {view_config['name']}")
            print(f"     Layout: {view_config['layout']}")
            print(f"     Description: {view_config['description']}")
            if "group_by" in view_config:
                print(f"     Group by: {view_config['group_by']}")
            if "fields" in view_config:
                print(f"     Fields: {view_config['fields']}")
            if "date_field" in view_config:
                print(f"     Date field: {view_config['date_field']}")
            self.view_ids[view_config['name']] = "manual_creation_required"

        print(f"\n✅ Documented {len(self.view_ids)} views for manual creation")
        print("   See: https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project")
        return True

    def print_summary(self):
        """Print summary report."""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)
        print(f"\n📊 Project: {self.project_title}")
        print(f"   Number: {self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"\n📋 Custom Fields: {len(self.field_ids)} created")
        print(f"👁️  Views: {len(self.view_ids)} documented (manual creation required)")
        print(f"📄 Documents Scanned: {len(self.created_items) + len(self.skipped_items)}")
        print(f"✅ Project Items Created: {len(self.created_items)}")

        if self.skipped_items:
            print(f"⚠️  Items Skipped: {len(self.skipped_items)}")

        if self.errors:
            print(f"\n❌ Errors Encountered: {len(self.errors)}")
            if self.verbose:
                for idx, error in enumerate(self.errors[:10], 1):
                    if isinstance(error, dict):
                        print(f"   {idx}. {json.dumps(error, indent=6)}")
                    else:
                        print(f"   {idx}. {error}")
                if len(self.errors) > 10:
                    print(f"   ... and {len(self.errors) - 10} more")
            else:
                for error in self.errors[:5]:  # Show first 5 errors
                    if isinstance(error, dict):
                        print(f"   - {error.get('error_message', str(error)[:100])}")
                    else:
                        print(f"   - {str(error)[:100]}")
                if len(self.errors) > 5:
                    print(f"   ... and {len(self.errors) - 5} more (use --verbose for full details)")
        else:
            print("\n✅ No errors encountered")

        print("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Setup GitHub Project v2 for MokoStandards Documentation Control'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose error logging and debug output'
    )
    parser.add_argument(
        '--skip-views',
        action='store_true',
        help='Skip creating project views (Board, Table, Roadmap)'
    )

    args = parser.parse_args()

    print("="*70)
    print("GitHub Project v2 Setup")
    print("MokoStandards Documentation Control Register")
    print("="*70)

    if args.verbose:
        print("\n[VERBOSE MODE ENABLED]")

    # Configuration
    ORG = "mokoconsulting-tech"
    PROJECT_TITLE = "MokoStandards Documentation Control Register"

    # Determine repository path (supports CI environments and local execution)
    # Priority: GITHUB_WORKSPACE > current working directory
    repo_path_str = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
    REPO_PATH = Path(repo_path_str).resolve()

    print(f"\n📂 Repository path: {REPO_PATH}")

    # Get token from environment (GH_PAT secret)
    token = os.environ.get("GH_PAT")

    if args.verbose and token:
        print(f"[VERBOSE] GH_PAT token found (length: {len(token)})")

    # Initialize setup
    setup = GitHubProjectV2Setup(ORG, PROJECT_TITLE, token, verbose=args.verbose)

    # Step 1: Verify authentication
    print("\n🔐 Step 1: Verifying authentication...")
    if not setup.verify_auth():
        print("\n❌ STOP: Authentication required")
        print("\nPlease either:")
        print("  1. Set GH_PAT environment variable: export GH_PAT='your_token'")
        print("  2. Authenticate gh CLI: gh auth login")
        sys.exit(1)

    # Step 2: Get organization ID
    print("\n🏢 Step 2: Getting organization ID...")
    org_id = setup.get_org_id()
    if not org_id:
        print("\n❌ STOP: Failed to get organization ID")
        print("Ensure the token has 'read:org' permission")
        sys.exit(1)

    # Step 3: Create project
    print("\n📁 Step 3: Creating GitHub Project v2...")
    if not setup.create_project(org_id):
        print("\n❌ STOP: Failed to create project")
        print("Ensure the token has 'project' (write) permission")
        sys.exit(1)

    # Step 4: Create custom fields
    print("\n🔧 Step 4: Creating custom fields...")
    if not setup.create_all_fields():
        print("\n❌ STOP: Failed to create custom fields")
        sys.exit(1)

    # Step 5: Scan and populate
    print("\n📚 Step 5: Scanning repository and creating items...")
    if not setup.populate_project(REPO_PATH):
        print("\n❌ STOP: Failed to populate project")
        sys.exit(1)

    # Step 6: Document views (unless skipped)
    if not args.skip_views:
        print("\n👁️  Step 6: Documenting project views...")
        setup.create_project_views()
    else:
        print("\n⏭️  Step 6: Skipping view documentation (--skip-views flag)")

    # Print summary
    setup.print_summary()

    print("\n✅ Project v2 setup completed successfully!")
    print(f"\nView your project at:")
    print(f"https://github.com/orgs/{ORG}/projects/{setup.project_number}")


if __name__ == "__main__":
    main()
