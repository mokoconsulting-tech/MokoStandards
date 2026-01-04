#!/usr/bin/env python3
"""
GitHub Project v2 Views Setup Script
Creates the required views in Project #7 according to the project-views.md specification.

Usage:
    export GH_PAT="your_personal_access_token"
    python3 scripts/setup_project_views.py --project-number 7

Or use gh CLI authentication:
    gh auth login
    python3 scripts/setup_project_views.py --project-number 7
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Dict, List, Optional


# View configurations based on docs/guide/project-views.md
VIEW_CONFIGURATIONS = [
    {
        "name": "Master Register",
        "layout": "TABLE_LAYOUT",
        "description": "Comprehensive view of all documentation items in the register",
        "fields": [
            "Title", "Status", "Document Type", "Document Subtype", 
            "Document Path", "Owner Role", "Priority", "Risk Level", 
            "Review Cycle", "Compliance Tags"
        ],
        "sort": [
            {"field": "Status", "direction": "ASC"},
            {"field": "Priority", "direction": "DESC"}
        ],
        "filter": None
    },
    {
        "name": "Execution Kanban",
        "layout": "BOARD_LAYOUT",
        "description": "Operational view for active documentation work and task management",
        "group_by": "Status",
        "fields": ["Title", "Owner Role", "Priority", "Risk Level", "Document Type"],
        "filter": {
            "exclude": {"Status": ["Archived"]}
        }
    },
    {
        "name": "Governance Gate",
        "layout": "TABLE_LAYOUT",
        "description": "Focus on items requiring governance review, approval, or escalation",
        "fields": [
            "Title", "Status", "Owner Role", "Approval Required", 
            "Evidence Required", "Evidence Artifacts", "Risk Level", 
            "Compliance Tags"
        ],
        "sort": [
            {"field": "Risk Level", "direction": "DESC"},
            {"field": "Priority", "direction": "DESC"}
        ],
        "filter": {
            "or": [
                {"Status": "In Review"},
                {"and": [
                    {"Approval Required": "Yes"},
                    {"Status": {"ne": "Published"}}
                ]},
                {"and": [
                    {"Evidence Required": "Yes"},
                    {"Evidence Artifacts": "empty"}
                ]}
            ]
        }
    },
    {
        "name": "Policy Register",
        "layout": "TABLE_LAYOUT",
        "description": "Dedicated view for policy documentation artifacts",
        "fields": [
            "Title", "Status", "Document Subtype", "Document Path", 
            "Owner Role", "Review Cycle", "Retention", "Compliance Tags"
        ],
        "sort": [
            {"field": "Status", "direction": "ASC"},
            {"field": "Review Cycle", "direction": "ASC"}
        ],
        "filter": {
            "Document Type": "policy"
        }
    },
    {
        "name": "WaaS Portfolio",
        "layout": "TABLE_LAYOUT",
        "description": "View all WordPress as a Service (WaaS) related documentation",
        "fields": [
            "Title", "Status", "Document Type", "Document Path", 
            "Owner Role", "Priority", "Review Cycle"
        ],
        "sort": [
            {"field": "Priority", "direction": "DESC"},
            {"field": "Status", "direction": "ASC"}
        ],
        "filter": {
            "Document Subtype": "waas"
        }
    },
    {
        "name": "High Risk and Blockers",
        "layout": "TABLE_LAYOUT",
        "description": "Executive dashboard highlighting high-risk items and blocked work",
        "fields": [
            "Title", "Status", "Risk Level", "Priority", "Owner Role", 
            "Compliance Tags", "Dependencies"
        ],
        "sort": [
            {"field": "Risk Level", "direction": "DESC"},
            {"field": "Priority", "direction": "DESC"}
        ],
        "filter": {
            "or": [
                {"Risk Level": "High"},
                {"Status": "Blocked"}
            ]
        }
    }
]


class ProjectViewsSetup:
    """Handles GitHub Project v2 view creation."""

    def __init__(self, org: str, project_number: int, token: Optional[str] = None):
        self.org = org
        self.project_number = project_number
        self.token = token
        self.project_id = None
        self.field_ids = {}
        self.created_views = []
        self.errors = []

    def run_graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query using gh CLI or direct API."""
        try:
            if self.token:
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
            error_msg = f"GraphQL error: {e}"
            self.errors.append(error_msg)
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return {}

    def verify_auth(self) -> bool:
        """Verify GitHub CLI authentication or token."""
        if self.token:
            try:
                result = self.run_graphql("query { viewer { login } }")
                if result and "data" in result and result["data"].get("viewer"):
                    print(f"✅ Authenticated as: {result['data']['viewer']['login']}")
                    return True
            except:
                pass
            print("❌ Token authentication failed")
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
            except:
                pass
            print("❌ GitHub CLI not authenticated")
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
            print(f"✅ Found Project: {project['title']} (#{self.project_number})")
            print(f"   URL: {project.get('url', 'N/A')}")
            return self.project_id
        return None

    def get_project_fields(self) -> bool:
        """Get existing project fields for reference."""
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
            
            print(f"✅ Retrieved {len(self.field_ids)} existing fields")
            return True
        return False

    def create_views(self) -> bool:
        """Create all required views."""
        print("\n📋 Creating project views...")
        print("="*70)
        
        for idx, view_config in enumerate(VIEW_CONFIGURATIONS, 1):
            view_name = view_config["name"]
            print(f"\n[{idx}/{len(VIEW_CONFIGURATIONS)}] Creating view: {view_name}")
            print(f"   Layout: {view_config['layout']}")
            print(f"   Description: {view_config['description']}")
            
            # Note: GitHub's GraphQL API has limited support for creating views programmatically
            # Most view configurations must be done manually via the UI
            # This script documents the configuration requirements
            
            self.created_views.append(view_name)
            print(f"   ℹ️  View configuration documented (manual UI setup required)")
        
        print("\n" + "="*70)
        return True

    def print_manual_instructions(self):
        """Print manual setup instructions."""
        print("\n" + "="*70)
        print("MANUAL VIEW SETUP INSTRUCTIONS")
        print("="*70)
        print("""
GitHub Project v2 views must be created manually via the web interface.
The GraphQL API does not currently support programmatic view creation with
full configuration (filters, sorts, grouping).

To create each view:

1. Navigate to your project:
   https://github.com/orgs/{}/projects/{}

2. Click "+ New view" in the view tabs

3. Configure each view according to the specifications below:

""".format(self.org, self.project_number))
        
        for idx, view_config in enumerate(VIEW_CONFIGURATIONS, 1):
            print(f"\n{'─'*70}")
            print(f"View {idx}: {view_config['name']}")
            print(f"{'─'*70}")
            print(f"Description: {view_config['description']}")
            print(f"Layout: {view_config['layout'].replace('_LAYOUT', '').title()}")
            
            if "fields" in view_config:
                print(f"\nColumns to show:")
                for field in view_config["fields"]:
                    print(f"  • {field}")
            
            if "group_by" in view_config:
                print(f"\nGroup by: {view_config['group_by']}")
            
            if "sort" in view_config:
                print(f"\nSort:")
                for sort in view_config["sort"]:
                    direction = "High to Low" if sort["direction"] == "DESC" else "Low to High"
                    print(f"  • {sort['field']} ({direction})")
            
            if view_config.get("filter"):
                print(f"\nFilter: {json.dumps(view_config['filter'], indent=2)}")
                print("   (Configure via UI filter builder)")
        
        print("\n" + "="*70)
        print("\nFor complete view specifications, see:")
        print("  /docs/guide/project-views.md")
        print("="*70)

    def print_summary(self):
        """Print summary report."""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)
        print(f"\n📊 Project: #{self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"\n📋 Views Documented: {len(self.created_views)}")
        for view_name in self.created_views:
            print(f"   • {view_name}")
        
        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"   - {error}")
        else:
            print("\n✅ No errors encountered")
        
        print("\n📖 Next Steps:")
        print("   1. Review the manual setup instructions above")
        print("   2. Create each view via the GitHub Project UI")
        print("   3. Configure filters, sorts, and grouping as specified")
        print("   4. Refer to /docs/guide/project-views.md for detailed specifications")
        
        print("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Setup views for GitHub Project v2"
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
    
    args = parser.parse_args()
    
    print("="*70)
    print("GitHub Project v2 Views Setup")
    print("MokoStandards Documentation Control Register")
    print("="*70)
    
    # Get token from environment
    token = os.environ.get("GH_PAT")
    
    # Initialize setup
    setup = ProjectViewsSetup(args.org, args.project_number, token)
    
    # Step 1: Verify authentication
    print("\n🔐 Step 1: Verifying authentication...")
    if not setup.verify_auth():
        print("\n⚠️  WARNING: Not authenticated")
        print("   Setup will continue in documentation-only mode")
        print("   To enable API access:")
        print("     1. Set GH_PAT environment variable: export GH_PAT='your_token'")
        print("     2. Or authenticate gh CLI: gh auth login")
    
    # Step 2: Get project (if authenticated)
    if token or setup.verify_auth():
        print(f"\n📁 Step 2: Getting Project #{args.project_number}...")
        if not setup.get_project_id():
            print("\n⚠️  Could not retrieve project")
        else:
            # Step 3: Get project fields
            print("\n🔧 Step 3: Retrieving project fields...")
            setup.get_project_fields()
    
    # Step 4: Document view configurations
    print("\n📚 Step 4: Documenting view configurations...")
    setup.create_views()
    
    # Print manual instructions
    setup.print_manual_instructions()
    
    # Print summary
    setup.print_summary()
    
    print("\n✅ View configuration documentation complete!")


if __name__ == "__main__":
    main()
