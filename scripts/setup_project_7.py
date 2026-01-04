#!/usr/bin/env python3
"""
GitHub Project #7 Setup Script
Creates or updates GitHub Project #7 with custom fields including Target Version Number.

Features:
- Targets specific project number (#7)
- Adds "Target Version Number" custom field
- Checks for existing project to avoid duplicates
- Scans docs/ and templates/ directories
- Verbose error handling

Usage:
    export GH_PAT="your_personal_access_token"
    python3 scripts/setup_project_7.py

    With custom version:
    python3 scripts/setup_project_7.py --target-version "1.0.0"

    With verbose logging:
    python3 scripts/setup_project_7.py --verbose --target-version "1.0.0"

Or use gh CLI authentication:
    gh auth login
    python3 scripts/setup_project_7.py
"""

import argparse
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import the base class from setup_github_project_v2
# We'll extend it with Project #7 specific functionality
sys.path.insert(0, str(Path(__file__).parent))
from setup_github_project_v2 import GitHubProjectV2Setup


class GitHubProject7Setup(GitHubProjectV2Setup):
    """Handles GitHub Project #7 creation and population with version tracking."""

    def __init__(self, org: str, target_version: str = "1.0.0", token: Optional[str] = None, verbose: bool = False):
        project_title = "MokoStandards Documentation Control Register (Project #7)"
        super().__init__(org, project_title, token, verbose)
        self.target_version = target_version
        self.target_project_number = 7

    def check_existing_project(self, org_id: str) -> Optional[Tuple[str, int]]:
        """Check if project #7 already exists."""
        query = """
        query($org: String!) {
            organization(login: $org) {
                projectsV2(first: 100) {
                    nodes {
                        id
                        number
                        title
                    }
                }
            }
        }
        """
        result = self.run_graphql(query, {"org": self.org})
        
        if result and "data" in result and result["data"].get("organization"):
            projects = result["data"]["organization"]["projectsV2"]["nodes"]
            for project in projects:
                if project["number"] == self.target_project_number:
                    print(f"✅ Found existing Project #{project['number']}: {project['title']}")
                    self.log_verbose(f"Project ID: {project['id']}")
                    return project["id"], project["number"]
        
        return None

    def create_all_fields(self) -> bool:
        """Create all custom fields including Target Version Number."""
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
        
        # Text fields (including Target Version Number)
        text_fields = [
            "Document Path",
            "Dependencies",
            "Acceptance Criteria",
            "RACI",
            "KPIs",
            "Target Version Number"
        ]
        
        for field_name in text_fields:
            field_id = self.create_text_field(field_name)
            if field_id:
                self.field_ids[field_name] = field_id
            else:
                print(f"❌ STOP: Failed to create field '{field_name}'")
                return False
        
        print(f"\n✅ Created {len(self.field_ids)} custom fields")
        print(f"   Including 'Target Version Number' field for version tracking")
        print("\n⚠️  Note: Multi-select fields (Compliance Tags, Evidence Artifacts)")
        print("   must be created manually via UI as they are not fully supported via API")
        
        return True

    def create_project_item(self, file_path: Path, purpose: str) -> bool:
        """Create a project item for a document with version tracking."""
        title = file_path.stem
        
        doc_type = self.infer_document_type(file_path)
        doc_subtype = self.infer_document_subtype(file_path, doc_type)
        approval_required = self.get_approval_required(doc_type)
        
        body = f"""Document Path: {file_path}
Purpose: {purpose} tracking
Target Version: {self.target_version}
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
            
            # Set field values for the item including target version
            self.set_item_fields_with_version(item_id, file_path, doc_type, doc_subtype, approval_required)
            
            return True
        else:
            self.skipped_items.append(str(file_path))
            return False

    def set_item_fields_with_version(self, item_id: str, file_path: Path, doc_type: str, 
                                     doc_subtype: str, approval_required: str):
        """Set field values for a project item including version number."""
        # Set Document Path (text field)
        if "Document Path" in self.field_ids:
            self.set_text_field(item_id, "Document Path", str(file_path))
        
        # Set Target Version Number (text field)
        if "Target Version Number" in self.field_ids:
            self.set_text_field(item_id, "Target Version Number", self.target_version)
        
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

    def print_summary(self):
        """Print summary report with version information."""
        print("\n" + "="*70)
        print("SUMMARY REPORT - PROJECT #7")
        print("="*70)
        print(f"\n📊 Project: {self.project_title}")
        print(f"   Target Project Number: #{self.target_project_number}")
        print(f"   Actual Project Number: #{self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"   Target Version: {self.target_version}")
        print(f"\n📋 Custom Fields: {len(self.field_ids)} created")
        print(f"👁️  Views: {len(self.view_ids)} documented")
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
                for error in self.errors[:5]:
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
        description='Setup GitHub Project #7 for MokoStandards Documentation Control'
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
    parser.add_argument(
        '--target-version',
        default='1.0.0',
        help='Target version number for documentation (default: 1.0.0)'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("GitHub Project #7 Setup")
    print("MokoStandards Documentation Control Register")
    print("="*70)
    
    if args.verbose:
        print("\n[VERBOSE MODE ENABLED]")
    
    print(f"\n🎯 Target Version: {args.target_version}")
    print(f"🎯 Target Project Number: #7")
    
    # Configuration
    ORG = "mokoconsulting-tech"
    REPO_PATH = Path("/home/runner/work/MokoStandards/MokoStandards")
    
    # Get token from environment (GH_PAT secret)
    token = os.environ.get("GH_PAT")
    
    if args.verbose and token:
        print(f"[VERBOSE] GH_PAT token found (length: {len(token)})")
    
    # Initialize setup
    setup = GitHubProject7Setup(ORG, target_version=args.target_version, token=token, verbose=args.verbose)
    
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
    
    # Step 3: Check if project already exists
    print(f"\n🔍 Step 3: Checking for existing Project #7...")
    existing_project = setup.check_existing_project(org_id)
    
    if existing_project:
        project_id, project_number = existing_project
        setup.project_id = project_id
        setup.project_number = project_number
        print(f"⚠️  Project #{project_number} already exists")
        print(f"   Use the existing project ID: {project_id}")
        print(f"   Skipping project creation, but will continue with field and item creation")
    else:
        # Step 4: Create project
        print(f"\n📁 Step 4: Creating GitHub Project #7...")
        if not setup.create_project(org_id):
            print("\n❌ STOP: Failed to create project")
            print("Ensure the token has 'project' (write) permission")
            sys.exit(1)
    
    # Step 5: Create custom fields
    print("\n🔧 Step 5: Creating custom fields...")
    if not setup.create_all_fields():
        print("\n❌ STOP: Failed to create custom fields")
        sys.exit(1)
    
    # Step 6: Scan and populate
    print("\n📚 Step 6: Scanning repository and creating items...")
    if not setup.populate_project(REPO_PATH):
        print("\n❌ STOP: Failed to populate project")
        sys.exit(1)
    
    # Step 7: Document views (unless skipped)
    if not args.skip_views:
        print("\n👁️  Step 7: Documenting project views...")
        setup.create_project_views()
    else:
        print("\n⏭️  Step 7: Skipping view documentation (--skip-views flag)")
    
    # Print summary
    setup.print_summary()
    
    print(f"\n✅ Project #7 setup completed successfully!")
    print(f"\nView your project at:")
    print(f"https://github.com/orgs/{ORG}/projects/{setup.project_number}")


if __name__ == "__main__":
    main()
