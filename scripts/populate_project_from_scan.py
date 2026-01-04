#!/usr/bin/env python3
"""
GitHub Project v2 Population Script
Populates an existing GitHub Project v2 with documentation tasks from docs/ and templates/.

Usage:
    export GH_PAT="your_personal_access_token"
    python3 scripts/populate_project_from_scan.py --project-number 7

Or use gh CLI authentication:
    gh auth login
    python3 scripts/populate_project_from_scan.py --project-number 7
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GitHubProjectV2Populator:
    """Handles GitHub Project v2 population with scanned documents."""

    def __init__(self, org: str, project_number: int, token: Optional[str] = None):
        self.org = org
        self.project_number = project_number
        self.token = token
        self.project_id = None
        self.field_ids = {}
        self.field_option_ids = {}
        self.created_items = []
        self.skipped_items = []
        self.errors = []

    def run_graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query using gh CLI or direct API."""
        try:
            if self.token:
                # Use direct API call with token
                import requests
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
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            error_msg = f"GraphQL error: {e.stderr}"
            self.errors.append(error_msg)
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return {}
        except Exception as e:
            error_msg = f"Error: {e}"
            self.errors.append(error_msg)
            print(f"ERROR: {error_msg}", file=sys.stderr)
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

    def get_project_id(self) -> Optional[str]:
        """Get project ID from project number."""
        query = """
        query($org: String!, $number: Int!) {
            organization(login: $org) {
                projectV2(number: $number) {
                    id
                    title
                    url
                }
            }
        }
        """
        result = self.run_graphql(query, {"org": self.org, "number": self.project_number})
        if result and "data" in result and result["data"].get("organization", {}).get("projectV2"):
            project = result["data"]["organization"]["projectV2"]
            self.project_id = project["id"]
            print(f"✅ Found Project: {project['title']}")
            print(f"   Project Number: {self.project_number}")
            print(f"   Project ID: {self.project_id}")
            print(f"   URL: {project.get('url', 'N/A')}")
            return self.project_id
        else:
            print(f"❌ Failed to find project #{self.project_number}")
            return None

    def get_project_fields(self) -> bool:
        """Get existing project fields."""
        query = """
        query($org: String!, $number: Int!) {
            organization(login: $org) {
                projectV2(number: $number) {
                    fields(first: 50) {
                        nodes {
                            ... on ProjectV2Field {
                                id
                                name
                                dataType
                            }
                            ... on ProjectV2SingleSelectField {
                                id
                                name
                                dataType
                                options {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        result = self.run_graphql(query, {"org": self.org, "number": self.project_number})
        
        if result and "data" in result:
            fields = result["data"]["organization"]["projectV2"]["fields"]["nodes"]
            for field in fields:
                field_name = field.get("name")
                field_id = field.get("id")
                self.field_ids[field_name] = field_id
                
                # Store option IDs for single-select fields
                if "options" in field:
                    self.field_option_ids[field_name] = {
                        opt["name"]: opt["id"] for opt in field["options"]
                    }
            
            print(f"✅ Retrieved {len(self.field_ids)} existing fields")
            return True
        else:
            print(f"⚠️  Could not retrieve project fields")
            return False

    def list_subdirectories(self, base_path: Path, relative_to: Path) -> List[Path]:
        """List all subdirectories recursively."""
        subdirs = []
        for item in base_path.rglob("*"):
            if item.is_dir():
                rel_path = item.relative_to(relative_to)
                subdirs.append(rel_path)
        return sorted(subdirs)

    def scan_repository(self, repo_path: Path) -> Tuple[List[Tuple[Path, str]], List[Path]]:
        """Scan repository for documentation files and subdirectories."""
        print("\n🔍 Scanning repository...")
        
        docs_path = repo_path / "docs"
        templates_path = repo_path / "templates"
        
        files = []
        subdirs = []
        
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
            
            # List subdirectories in templates/
            subdirs = self.list_subdirectories(templates_path, repo_path)
        
        print(f"✅ Found {len(files)} documents")
        print(f"✅ Found {len(subdirs)} subdirectories in templates/")
        
        return sorted(files), subdirs

    def print_subdirectories(self, subdirs: List[Path]):
        """Print list of subdirectories."""
        print("\n📁 Subdirectories in templates/:")
        print("="*70)
        for subdir in subdirs:
            print(f"  {subdir}")
        print("="*70)

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
        title = f"{file_path.parent.name}/{file_path.stem}" if file_path.parent.name != "." else file_path.stem
        
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
                projectV2Item {
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
            item_id = result["data"]["addProjectV2DraftIssue"]["projectV2Item"]["id"]
            self.created_items.append(str(file_path))
            
            # Set field values for the item if fields exist
            if self.field_ids:
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
                projectV2Item {
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
                projectV2Item {
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
        
        files, subdirs = self.scan_repository(repo_path)
        
        # Print subdirectories
        self.print_subdirectories(subdirs)
        
        total = len(files)
        for idx, (file_path, purpose) in enumerate(files, 1):
            success = self.create_project_item(file_path, purpose)
            if success:
                print(f"  [{idx}/{total}] ✅ {file_path}")
            else:
                print(f"  [{idx}/{total}] ⚠️  Skipped: {file_path}")
        
        print(f"\n✅ Created {len(self.created_items)} items")
        if self.skipped_items:
            print(f"⚠️  Skipped {len(self.skipped_items)} items")
        
        return True

    def print_summary(self):
        """Print summary report."""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)
        print(f"\n📊 Project Number: {self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"\n📋 Custom Fields: {len(self.field_ids)} found")
        print(f"📄 Documents Scanned: {len(self.created_items) + len(self.skipped_items)}")
        print(f"✅ Project Items Created: {len(self.created_items)}")
        
        if self.skipped_items:
            print(f"⚠️  Items Skipped: {len(self.skipped_items)}")
        
        if self.errors:
            print(f"\n❌ Errors Encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
            if len(self.errors) > 5:
                print(f"   ... and {len(self.errors) - 5} more")
        else:
            print("\n✅ No errors encountered")
        
        print("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Populate GitHub Project v2 with documentation tasks"
    )
    parser.add_argument(
        "--project-number",
        type=int,
        default=7,
        help="GitHub Project number (default: 7)"
    )
    parser.add_argument(
        "--org",
        type=str,
        default="mokoconsulting-tech",
        help="GitHub organization (default: mokoconsulting-tech)"
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        default=Path("/home/runner/work/MokoStandards/MokoStandards"),
        help="Repository path"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("GitHub Project v2 Population Script")
    print("MokoStandards Documentation Control Register")
    print("="*70)
    
    # Get token from environment (GH_PAT secret)
    token = os.environ.get("GH_PAT")
    
    # Initialize populator
    populator = GitHubProjectV2Populator(args.org, args.project_number, token)
    
    # Step 1: Verify authentication
    print("\n🔐 Step 1: Verifying authentication...")
    if not populator.verify_auth():
        print("\n❌ STOP: Authentication required")
        print("\nPlease either:")
        print("  1. Set GH_PAT environment variable: export GH_PAT='your_token'")
        print("  2. Authenticate gh CLI: gh auth login")
        sys.exit(1)
    
    # Step 2: Get project
    print(f"\n📁 Step 2: Getting Project #{args.project_number}...")
    if not populator.get_project_id():
        print("\n❌ STOP: Failed to find project")
        print(f"Ensure Project #{args.project_number} exists in {args.org}")
        sys.exit(1)
    
    # Step 3: Get project fields
    print("\n🔧 Step 3: Retrieving project fields...")
    populator.get_project_fields()
    
    # Step 4: Scan and populate
    print("\n📚 Step 4: Scanning repository and creating items...")
    if not populator.populate_project(args.repo_path):
        print("\n❌ STOP: Failed to populate project")
        sys.exit(1)
    
    # Print summary
    populator.print_summary()
    
    print("\n✅ Project population completed successfully!")
    print(f"\nView your project at:")
    print(f"https://github.com/orgs/{args.org}/projects/{args.project_number}")


if __name__ == "__main__":
    main()
