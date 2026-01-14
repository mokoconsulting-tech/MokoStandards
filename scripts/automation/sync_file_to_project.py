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
PATH: /scripts/sync_file_to_project.py
VERSION: 05.00.00
BRIEF: Syncs created/updated docs and templates to GitHub Project tasks
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Project configuration
DEFAULT_PROJECT_NUMBER = 7
REPO_OWNER = "mokoconsulting-tech"
REPO_NAME = "MokoStandards"

# Field value mappings
DOCUMENT_TYPE_MAP = {
    "docs/policy": "policy",
    "docs/guide": "guide",
    "docs/checklist": "checklist",
    "docs/index.md": "index",
    "docs/README.md": "overview",
    "docs/readme.md": "overview",
    "templates": "template"
}

DOCUMENT_SUBTYPE_MAP = {
    "waas": "waas",
    "policy": "policy",
    "guide": "guide",
    "checklist": "checklist",
    "docs/required": "core",
    "docs/extra": "catalog",
    "templates/docs": "catalog",
    "templates/repos": "catalog",
    "templates/scripts": "catalog"
}

OWNER_ROLE_MAP = {
    "policy": "Governance Owner",
    "guide": "Documentation Owner",
    "checklist": "Operations Owner",
    "template": "Documentation Owner",
    "overview": "Documentation Owner",
    "index": "Documentation Owner"
}

PRIORITY_MAP = {
    "policy": "High",
    "guide": "Medium",
    "checklist": "Medium",
    "template": "Low",
    "overview": "Medium",
    "index": "Low"
}


def run_gh_command(cmd: List[str]) -> Tuple[bool, str]:
    """Execute a gh CLI command and return success status and output."""
    try:
        # Set up environment with GH_TOKEN if available
        env = os.environ.copy()
        if "GH_TOKEN" in env:
            # gh CLI uses GH_TOKEN automatically, just ensure it's in the environment
            pass
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Error output: {e.stderr}", file=sys.stderr)
        return False, e.stderr.strip()


def get_project_id(project_number: int) -> Optional[str]:
    """Get the project ID from the project number."""
    cmd = [
        "gh", "project", "list",
        "--owner", REPO_OWNER,
        "--format", "json"
    ]
    
    success, output = run_gh_command(cmd)
    if not success:
        return None
    
    try:
        projects = json.loads(output)
        for project in projects.get("projects", []):
            if project.get("number") == project_number:
                return project.get("id")
    except json.JSONDecodeError:
        print(f"Failed to parse project list JSON", file=sys.stderr)
    
    return None


def search_existing_item(project_id: str, file_path: str) -> Optional[str]:
    """Search for existing project item by document path."""
    cmd = [
        "gh", "project", "item-list", project_id,
        "--owner", REPO_OWNER,
        "--format", "json",
        "--limit", "500"
    ]
    
    success, output = run_gh_command(cmd)
    if not success:
        return None
    
    try:
        items = json.loads(output)
        for item in items.get("items", []):
            # Check if Document Path field matches
            # Note: This requires the field to be included in item-list output
            # May need to query items individually
            content = item.get("content", {})
            if content.get("body", "").find(file_path) != -1:
                return item.get("id")
    except json.JSONDecodeError:
        print(f"Failed to parse item list JSON", file=sys.stderr)
    
    return None


def get_document_metadata(file_path: str, is_folder: bool = False) -> Dict[str, str]:
    """Extract metadata from file path and determine field values."""
    path = Path(file_path)
    
    # Determine document type
    doc_type = "overview"
    for key, value in DOCUMENT_TYPE_MAP.items():
        if str(path).startswith(key):
            doc_type = value
            break
    
    # Folders are categorized differently
    if is_folder:
        if "templates" in str(path):
            doc_type = "template"
        elif "policy" in str(path):
            doc_type = "policy"
        elif "guide" in str(path):
            doc_type = "guide"
        elif "checklist" in str(path):
            doc_type = "checklist"
        else:
            doc_type = "overview"
    
    # Determine document subtype
    doc_subtype = "core"
    for key, value in DOCUMENT_SUBTYPE_MAP.items():
        if key in str(path):
            doc_subtype = value
            break
    
    # Determine owner role
    owner_role = OWNER_ROLE_MAP.get(doc_type, "Documentation Owner")
    
    # Determine priority
    priority = PRIORITY_MAP.get(doc_type, "Medium")
    
    # Determine status
    status = "In Progress" if path.exists() else "Planned"
    
    # Generate title with full path as markdown link to the document
    file_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{file_path}"
    title = f"[{file_path}]({file_url})"
    
    return {
        "title": title,
        "document_type": doc_type,
        "document_subtype": doc_subtype,
        "owner_role": owner_role,
        "priority": priority,
        "status": status,
        "document_path": file_path,
        "risk_level": "Low" if doc_type == "template" else "Medium",
        "approval_required": "Yes" if doc_type == "policy" else "No",
        "evidence_required": "Yes" if doc_type in ["policy", "checklist"] else "No",
        "review_cycle": "Annual" if doc_type == "policy" else "Ad hoc",
        "retention": "Indefinite" if doc_type in ["policy", "guide"] else "7 Years",
        "is_folder": "Yes" if is_folder else "No"
    }


def create_issue_for_document(file_path: str, metadata: Dict[str, str], is_folder: bool = False) -> Optional[str]:
    """Create a GitHub issue for the document or folder."""
    title = metadata["title"]
    
    if is_folder:
        body = f"""# Folder Structure Task

**Folder Path**: `{file_path}`

**Type**: {metadata['document_type']} / {metadata['document_subtype']}

**Owner**: {metadata['owner_role']}

## Task Details

This task tracks the folder structure and organization at `{file_path}`.

## Acceptance Criteria

- [ ] Folder structure follows standards
- [ ] Contains appropriate index.md or README.md
- [ ] Subfolders and files properly organized
- [ ] Documentation complete for folder contents
- [ ] Linked to Project #{DEFAULT_PROJECT_NUMBER}

## Metadata

- **Priority**: {metadata['priority']}
- **Risk Level**: {metadata['risk_level']}
- **Review Cycle**: {metadata['review_cycle']}

---

*Auto-generated by sync_file_to_project.py*
"""
    else:
        body = f"""# Documentation Task

**Document Path**: `{file_path}`

**Type**: {metadata['document_type']} / {metadata['document_subtype']}

**Owner**: {metadata['owner_role']}

## Task Details

This task tracks the creation and maintenance of the documentation file at `{file_path}`.

## Acceptance Criteria

- [ ] Document created and follows formatting standards
- [ ] All required sections included
- [ ] Metadata header present and complete
- [ ] Content reviewed for accuracy
- [ ] Linked to Project #{DEFAULT_PROJECT_NUMBER}

## Metadata

- **Priority**: {metadata['priority']}
- **Risk Level**: {metadata['risk_level']}
- **Approval Required**: {metadata['approval_required']}
- **Evidence Required**: {metadata['evidence_required']}
- **Review Cycle**: {metadata['review_cycle']}
- **Retention**: {metadata['retention']}

---

*Auto-generated by sync_file_to_project.py*
"""
    
    labels = ["documentation", metadata['document_type']]
    if is_folder:
        labels.append("folder-structure")
    
    cmd = [
        "gh", "issue", "create",
        "--repo", f"{REPO_OWNER}/{REPO_NAME}",
        "--title", title,
        "--body", body,
        "--label", ",".join(labels)
    ]
    
    success, output = run_gh_command(cmd)
    if not success:
        return None
    
    # Extract issue number from output (format: "https://github.com/owner/repo/issues/123")
    if output:
        issue_num = output.split("/")[-1]
        return issue_num
    
    return None


def add_issue_to_project(project_id: str, issue_url: str) -> Optional[str]:
    """Add an issue to the project and return the item ID."""
    cmd = [
        "gh", "project", "item-add", project_id,
        "--owner", REPO_OWNER,
        "--url", issue_url
    ]
    
    success, output = run_gh_command(cmd)
    if not success:
        return None
    
    # Parse output to get item ID
    try:
        result = json.loads(output)
        return result.get("id")
    except json.JSONDecodeError:
        # If output is just the ID
        return output.strip()


def update_project_item_fields(project_id: str, item_id: str, metadata: Dict[str, str]) -> bool:
    """Update project item fields with metadata."""
    # Map of field names to values
    fields = {
        "Status": metadata.get("status", "Planned"),
        "Priority": metadata.get("priority", "Medium"),
        "Risk Level": metadata.get("risk_level", "Medium"),
        "Document Type": metadata.get("document_type", "guide"),
        "Document Subtype": metadata.get("document_subtype", "core"),
        "Owner Role": metadata.get("owner_role", "Documentation Owner"),
        "Approval Required": metadata.get("approval_required", "No"),
        "Evidence Required": metadata.get("evidence_required", "No"),
        "Review Cycle": metadata.get("review_cycle", "Ad hoc"),
        "Retention": metadata.get("retention", "7 Years"),
        "Document Path": metadata.get("document_path", "")
    }
    
    all_success = True
    for field_name, field_value in fields.items():
        if not field_value:
            continue
        
        cmd = [
            "gh", "project", "item-edit",
            "--id", item_id,
            "--project-id", project_id,
            "--field-name", field_name,
            "--text", field_value if field_name == "Document Path" else None,
            "--single-select-option-id" if field_name != "Document Path" else "--text"
        ]
        
        # Simplify command based on field type
        if field_name == "Document Path":
            cmd = [
                "gh", "project", "item-edit",
                "--id", item_id,
                "--project-id", project_id,
                "--field-name", field_name,
                "--text", field_value
            ]
        else:
            # For single-select fields, we need to set the option
            cmd = [
                "gh", "project", "item-edit",
                "--id", item_id,
                "--project-id", project_id,
                "--field-name", field_name,
                "--text", field_value  # gh CLI will handle matching to options
            ]
        
        success, _ = run_gh_command(cmd)
        if not success:
            print(f"Warning: Failed to set field '{field_name}' to '{field_value}'", file=sys.stderr)
            all_success = False
    
    return all_success


def sync_file_to_project(file_path: str, project_number: int = DEFAULT_PROJECT_NUMBER, is_folder: bool = False) -> bool:
    """Main function to sync a file or folder to the project."""
    print(f"Syncing {'folder' if is_folder else 'file'}: {file_path}")
    
    # Validate path
    if not file_path.startswith(("docs/", "templates/")):
        print(f"Skipping path outside docs/ or templates/: {file_path}")
        return True
    
    if not is_folder and not file_path.endswith(".md"):
        print(f"Skipping non-markdown file: {file_path}")
        return True
    
    # Get project ID
    print(f"Getting project ID for project #{project_number}...")
    project_id = get_project_id(project_number)
    if not project_id:
        print(f"Failed to find project #{project_number}", file=sys.stderr)
        return False
    
    print(f"Project ID: {project_id}")
    
    # Get document metadata
    metadata = get_document_metadata(file_path, is_folder)
    print(f"Document metadata: {json.dumps(metadata, indent=2)}")
    
    # Check if item already exists
    print(f"Checking for existing item...")
    existing_item_id = search_existing_item(project_id, file_path)
    
    if existing_item_id:
        print(f"Found existing item: {existing_item_id}")
        print(f"Updating item fields...")
        success = update_project_item_fields(project_id, existing_item_id, metadata)
        if success:
            print(f"✓ Successfully updated existing task for {file_path}")
        else:
            print(f"⚠ Partially updated task for {file_path}", file=sys.stderr)
        return success
    
    # Create new issue
    print(f"Creating new issue...")
    issue_number = create_issue_for_document(file_path, metadata, is_folder)
    if not issue_number:
        print(f"Failed to create issue for {file_path}", file=sys.stderr)
        return False
    
    issue_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    print(f"Created issue: {issue_url}")
    
    # Add issue to project
    print(f"Adding issue to project...")
    item_id = add_issue_to_project(project_id, issue_url)
    if not item_id:
        print(f"Failed to add issue to project", file=sys.stderr)
        return False
    
    print(f"Added to project with item ID: {item_id}")
    
    # Update project item fields
    print(f"Updating item fields...")
    success = update_project_item_fields(project_id, item_id, metadata)
    
    if success:
        print(f"✓ Successfully created and configured task for {file_path}")
    else:
        print(f"⚠ Created task but failed to set all fields for {file_path}", file=sys.stderr)
    
    return success


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Sync documentation files and folders to GitHub Project'
    )
    parser.add_argument(
        'path',
        help='Path to file or folder to sync'
    )
    parser.add_argument(
        'project_number',
        nargs='?',
        type=int,
        default=DEFAULT_PROJECT_NUMBER,
        help=f'Project number (default: {DEFAULT_PROJECT_NUMBER})'
    )
    parser.add_argument(
        '--folder',
        action='store_true',
        help='Treat path as a folder instead of a file'
    )
    
    args = parser.parse_args()
    
    file_path = args.path
    project_number = args.project_number
    is_folder = args.folder
    
    # Check for GH CLI
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: gh CLI is not installed or not in PATH", file=sys.stderr)
        print("Install from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)
    
    # Check for authentication via GH_TOKEN or gh auth
    gh_token = os.environ.get("GH_TOKEN")
    if gh_token:
        print("Using GH_TOKEN for authentication")
    else:
        # Check for gh CLI authentication
        result = subprocess.run(["gh", "auth", "status"], capture_output=True)
        if result.returncode != 0:
            print("Error: Not authenticated with gh CLI", file=sys.stderr)
            print("Run: gh auth login or set GH_TOKEN environment variable", file=sys.stderr)
            sys.exit(1)
    
    # Sync file to project
    success = sync_file_to_project(file_path, project_number, is_folder)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
