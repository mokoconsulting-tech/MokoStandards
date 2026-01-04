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
                
                print(f"  🔄 Executing GraphQL query via API...", file=sys.stderr)
                response = requests.post(
                    "https://api.github.com/graphql",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                
                if "errors" in result:
                    error_details = "; ".join([err.get("message", str(err)) for err in result["errors"]])
                    error_msg = f"GraphQL API returned errors: {error_details}"
                    self.errors.append(error_msg)
                    print(f"❌ ERROR: {error_msg}", file=sys.stderr)
                    return {}
                
                return result
            else:
                cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
                if variables:
                    for key, value in variables.items():
                        if isinstance(value, (list, dict)):
                            cmd.extend(["-F", f"{key}={json.dumps(value)}"])
                        elif isinstance(value, (int, float, bool)):
                            # Use -F for numbers and booleans to preserve type
                            cmd.extend(["-F", f"{key}={value}"])
                        else:
                            # Use -f for strings
                            cmd.extend(["-f", f"{key}={value}"])
                
                print(f"  🔄 Executing GraphQL query via gh CLI...", file=sys.stderr)
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            error_msg = f"gh CLI command failed (exit code {e.returncode})"
            if e.stderr:
                error_msg += f": {e.stderr.strip()}"
            self.errors.append(error_msg)
            print(f"❌ ERROR: {error_msg}", file=sys.stderr)
            print(f"   Command: {' '.join(e.cmd)}", file=sys.stderr)
            return {}
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON response: {e}"
            self.errors.append(error_msg)
            print(f"❌ ERROR: {error_msg}", file=sys.stderr)
            return {}
        except Exception as e:
            error_msg = f"Unexpected error during GraphQL query: {type(e).__name__}: {e}"
            self.errors.append(error_msg)
            print(f"❌ ERROR: {error_msg}", file=sys.stderr)
            import traceback
            print(f"   Traceback: {traceback.format_exc()}", file=sys.stderr)
            return {}

    def verify_auth(self) -> bool:
        """Verify GitHub CLI authentication or token."""
        print("  🔐 Checking authentication...", file=sys.stderr)
        if self.token:
            try:
                result = self.run_graphql("query { viewer { login } }")
                if result and "data" in result and result["data"].get("viewer"):
                    username = result['data']['viewer']['login']
                    print(f"✅ Authenticated as: {username}")
                    return True
                else:
                    print("❌ Token authentication failed: No viewer data returned")
                    return False
            except Exception as e:
                print(f"❌ Token verification failed: {type(e).__name__}: {e}")
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
                    if result.stderr:
                        print(f"   Details: {result.stderr.strip()}")
                    return False
            except FileNotFoundError:
                print("❌ GitHub CLI (gh) not found in PATH")
                return False
            except Exception as e:
                print(f"❌ Error checking auth: {type(e).__name__}: {e}")
                return False

    def get_existing_views(self) -> Dict[str, str]:
        """Get existing views in the project."""
        print(f"  🔍 Checking for existing views...", file=sys.stderr)
        query = """
        query($org: String!, $number: Int!) {
            organization(login: $org) {
                projectV2(number: $number) {
                    views(first: 20) {
                        nodes {
                            id
                            name
                            layout
                        }
                    }
                }
            }
        }
        """
        result = self.run_graphql(query, {"org": self.org, "number": self.project_number})
        
        existing_views = {}
        if result and "data" in result:
            views = result["data"]["organization"]["projectV2"]["views"]["nodes"]
            for view in views:
                view_name = view.get("name")
                view_id = view.get("id")
                view_layout = view.get("layout")
                existing_views[view_name] = {"id": view_id, "layout": view_layout}
            
            if existing_views:
                print(f"✅ Found {len(existing_views)} existing views")
                for name in existing_views.keys():
                    print(f"   • {name}")
            else:
                print(f"ℹ️  No existing views found")
        else:
            print(f"⚠️  Could not retrieve existing views")
        
        return existing_views

    def create_project_view(self, view_name: str, layout: str) -> Optional[str]:
        """Create a new project view via GraphQL API."""
        print(f"  🔨 Creating view '{view_name}'...", file=sys.stderr)
        
        mutation = """
        mutation($projectId: ID!, $name: String!, $layout: ProjectV2ViewLayout!) {
            createProjectV2View(input: {
                projectId: $projectId
                name: $name
                layout: $layout
            }) {
                projectV2View {
                    id
                    name
                    layout
                }
            }
        }
        """
        
        variables = {
            "projectId": self.project_id,
            "name": view_name,
            "layout": layout
        }
        
        result = self.run_graphql(mutation, variables)
        
        if result and "data" in result and result["data"].get("createProjectV2View"):
            view_data = result["data"]["createProjectV2View"]["projectV2View"]
            view_id = view_data.get("id")
            print(f"  ✅ Created view: {view_name} (ID: {view_id})")
            return view_id
        else:
            error_msg = f"Failed to create view '{view_name}'"
            self.errors.append(error_msg)
            print(f"  ❌ {error_msg}", file=sys.stderr)
            return None

    def get_project_id(self) -> Optional[str]:
        """Get project ID from project number."""
        print(f"  🔍 Looking up project #{self.project_number}...", file=sys.stderr)
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
        else:
            error_msg = f"Project #{self.project_number} not found in organization {self.org}"
            self.errors.append(error_msg)
            print(f"❌ ERROR: {error_msg}", file=sys.stderr)
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

    def create_views(self, existing_views: Dict[str, Dict]) -> bool:
        """Create all required views programmatically."""
        print("\n📋 Creating/Updating project views...")
        print("="*70)
        
        views_created = []
        views_existing = []
        views_failed = []
        
        for idx, view_config in enumerate(VIEW_CONFIGURATIONS, 1):
            view_name = view_config["name"]
            view_layout = view_config["layout"]
            
            print(f"\n[{idx}/{len(VIEW_CONFIGURATIONS)}] Processing view: {view_name}")
            print(f"   Layout: {view_layout.replace('_LAYOUT', '').title()}")
            print(f"   Description: {view_config['description']}")
            
            if view_name in existing_views:
                print(f"   ✅ View already exists (ID: {existing_views[view_name]['id']})")
                print(f"   ℹ️  Skipping creation - view already configured")
                views_existing.append(view_name)
                self.created_views.append(view_name)
            else:
                # Attempt to create the view
                if self.project_id:
                    view_id = self.create_project_view(view_name, view_layout)
                    if view_id:
                        views_created.append(view_name)
                        self.created_views.append(view_name)
                        print(f"   ℹ️  Note: Advanced configuration (filters, sorts, grouping) must be done manually")
                    else:
                        views_failed.append(view_name)
                else:
                    print(f"   ⚠️  Cannot create view - project ID not available")
                    print(f"   💡 Authenticate to create views programmatically")
                    views_failed.append(view_name)
        
        print("\n" + "="*70)
        print(f"\n📊 View Creation Summary:")
        print(f"   ✅ Views created: {len(views_created)}")
        if views_created:
            for name in views_created:
                print(f"      • {name}")
        print(f"   ℹ️  Views already exist: {len(views_existing)}")
        if views_existing:
            for name in views_existing:
                print(f"      • {name}")
        if views_failed:
            print(f"   ❌ Views failed: {len(views_failed)}")
            for name in views_failed:
                print(f"      • {name}")
        print("="*70)
        
        # If views were created, print note about manual configuration
        if views_created:
            print(f"\n📝 Important: Views have been created with basic configuration.")
            print(f"   Advanced settings (filters, sorts, field visibility) require manual setup:")
            print(f"   1. Visit: https://github.com/orgs/{self.org}/projects/{self.project_number}")
            print(f"   2. Click on each view")
            print(f"   3. Use view menu (⋯) → Settings to configure:")
            print(f"      - Field visibility")
            print(f"      - Filters")
            print(f"      - Sort order")
            print(f"      - Grouping (for Board views)")
        
        return True

    def print_manual_instructions(self):
        """Print manual setup instructions."""
        print("\n" + "="*70)
        print("MANUAL VIEW SETUP INSTRUCTIONS")
        print("="*70)
        print("""
GitHub Project v2 views must be created/updated manually via the web interface.
The GraphQL API does not currently support programmatic view creation with
full configuration (filters, sorts, grouping).

To create a new view:

1. Navigate to your project:
   https://github.com/orgs/{}/projects/{}

2. Click "+ New view" in the view tabs

3. Select the layout type (Table, Board, etc.)

4. Name the view and configure according to specifications below

To update an existing view:

1. Navigate to the view in your project

2. Click the view menu (⋯) and select "Settings"

3. Update fields, filters, sorts, and grouping as needed

4. Save changes

View Configurations:

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
        print(f"\n📊 Project Configuration:")
        print(f"   Project Number: #{self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"   Project ID: {self.project_id if self.project_id else 'Not retrieved'}")
        
        print(f"\n📋 Views Processed: {len(self.created_views)}")
        for idx, view_name in enumerate(self.created_views, 1):
            print(f"   {idx}. {view_name}")
        
        print(f"\n📈 Execution Summary:")
        print(f"   Total views in spec: {len(VIEW_CONFIGURATIONS)}")
        print(f"   Views processed: {len(self.created_views)}")
        print(f"   API mode: {'Yes' if self.project_id else 'No (documentation only)'}")
        print(f"   Fields retrieved: {len(self.field_ids)}")
        
        if self.errors:
            print(f"\n❌ Errors Encountered: {len(self.errors)}")
            print("   " + "-"*66)
            for idx, error in enumerate(self.errors, 1):
                print(f"   {idx}. {error}")
            print("   " + "-"*66)
            if not self.project_id:
                print("\n   ⚠️  Script ran in documentation-only mode")
                print("   💡 Tip: Set GH_PAT environment variable or run 'gh auth login'")
        else:
            print("\n✅ No errors encountered")
        
        print("\n📖 Next Steps:")
        if self.project_id and len(self.created_views) > 0:
            print("   1. Visit your project to see the newly created views")
            print(f"      https://github.com/orgs/{self.org}/projects/{self.project_number}")
            print("   2. Configure advanced settings for each view:")
            print("      - Field visibility and order")
            print("      - Filters")
            print("      - Sort order")
            print("      - Grouping (for Board views)")
            print("   3. Refer to /docs/guide/project-views.md for detailed specifications")
        else:
            print("   1. Authenticate with GitHub (set GH_PAT or run 'gh auth login')")
            print("   2. Run this script again to create views programmatically")
            print(f"   3. Visit: https://github.com/orgs/{self.org}/projects/{self.project_number}")
            print("   4. Review the manual setup instructions above")
        print("   5. Refer to /docs/guide/project-views.md for complete details")
        
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
    existing_views = {}
    if token or setup.verify_auth():
        print(f"\n📁 Step 2: Getting Project #{args.project_number}...")
        if not setup.get_project_id():
            print("\n⚠️  Could not retrieve project")
        else:
            # Step 3: Get project fields
            print("\n🔧 Step 3: Retrieving project fields...")
            setup.get_project_fields()
            
            # Step 3.5: Get existing views
            print("\n🔍 Step 3.5: Checking existing views...")
            existing_views = setup.get_existing_views()
    
    # Step 4: Create/document view configurations
    print("\n📚 Step 4: Creating project views...")
    setup.create_views(existing_views)
    
    # Print manual instructions (for advanced configuration)
    setup.print_manual_instructions()
    
    # Print summary
    setup.print_summary()
    
    if setup.project_id and len(setup.created_views) > 0:
        print("\n✅ View creation complete!")
    else:
        print("\n✅ View configuration documentation complete!")


if __name__ == "__main__":
    main()
