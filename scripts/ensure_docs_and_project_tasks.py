#!/usr/bin/env python3
"""
Documentation Generation + Project #7 Task Sync
Ensures all required documentation files exist and have corresponding tasks in Project #7.

Usage:
    export GH_PAT="your_personal_access_token"
    python3 scripts/ensure_docs_and_project_tasks.py

Or use gh CLI authentication:
    gh auth login
    python3 scripts/ensure_docs_and_project_tasks.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Canonical Document List - Mandatory deliverables with enterprise field specifications
CANONICAL_DOCUMENTS = {
    # Repository-Level
    "README.md": {
        "path": "README.md",
        "title": "Repository README",
        "type": "overview",
        "subtype": "core",
        "priority": "High",
        "risk_level": "Low",
        "approval": "Yes",
        "evidence": "Yes",
        "review_cycle": "Annual",
        "retention": "Indefinite",
        "compliance_tags": ["Governance"],
        "evidence_artifacts": ["Pull Request", "Review Approval", "Published Document"],
        "dependencies": "/docs/readme.md",
        "acceptance_criteria": "States repository purpose, links to /docs/readme.md and /docs/docs-index.md, and references governance entry points.",
        "raci": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
        "kpis": "KPI – Timeliness: Updated within review cycle\nKPI – Quality: Passes documentation review\nKPI – Compliance: Aligns to governance and documentation policies",
        "purpose": "Define repository scope, entry points, governance references, and documentation navigation links."
    },
    "CHANGELOG.md": {
        "path": "CHANGELOG.md",
        "title": "Repository CHANGELOG",
        "type": "index",
        "subtype": "core",
        "priority": "Medium",
        "risk_level": "Low",
        "approval": "No",
        "evidence": "Yes",
        "review_cycle": "Annual",
        "retention": "Indefinite",
        "compliance_tags": ["Release"],
        "evidence_artifacts": ["Pull Request", "Published Document"],
        "dependencies": "/README.md",
        "acceptance_criteria": "Uses a consistent changelog format, captures notable changes, and aligns versions with releases.",
        "raci": "Responsible: Release Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
        "kpis": "KPI – Timeliness: Updated per release\nKPI – Quality: Entries are complete and specific\nKPI – Compliance: Supports release evidence",
        "purpose": "Track notable changes and releases using a consistent versioned log.",
        "owner_role": "Release Owner"
    },
    "LICENSE.md": {
        "path": "LICENSE.md",
        "title": "Repository LICENSE",
        "type": "policy",
        "subtype": "core",
        "priority": "High",
        "risk_level": "Medium",
        "approval": "Yes",
        "evidence": "Yes",
        "review_cycle": "Ad hoc",
        "retention": "Indefinite",
        "compliance_tags": ["Governance", "Audit"],
        "evidence_artifacts": ["Published Document"],
        "dependencies": "",
        "acceptance_criteria": "Contains the correct license text and is aligned to repository SPDX expectations.",
        "raci": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Legal\nInformed: Contributors",
        "kpis": "KPI – Timeliness: Present prior to first release\nKPI – Quality: License text verified\nKPI – Compliance: Meets open source governance requirements",
        "purpose": "Define the legal license governing repository contents and redistribution.",
        "owner_role": "Governance Owner"
    },
    
    # Documentation Root and Index
    "docs/readme.md": {
        "path": "docs/readme.md",
        "title": "Documentation README",
        "type": "overview",
        "subtype": "core",
        "priority": "High",
        "risk_level": "Low",
        "approval": "Yes",
        "evidence": "Yes",
        "review_cycle": "Annual",
        "retention": "Indefinite",
        "compliance_tags": ["Governance"],
        "evidence_artifacts": ["Pull Request", "Published Document"],
        "dependencies": "",
        "acceptance_criteria": "Defines documentation layout, links to /docs/docs-index.md, and describes how policies, guides, and checklists are organized.",
        "raci": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
        "kpis": "KPI – Timeliness: Updated within review cycle\nKPI – Quality: Navigation links verified\nKPI – Compliance: Conforms to formatting policy",
        "purpose": "Define documentation taxonomy, folder expectations, and navigation entry points."
    },
    "docs/index.md": {
        "path": "docs/index.md",
        "title": "Documentation Index",
        "type": "index",
        "subtype": "catalog",
        "priority": "High",
        "risk_level": "Low",
        "approval": "Yes",
        "evidence": "Yes",
        "review_cycle": "Annual",
        "retention": "Indefinite",
        "compliance_tags": ["Governance", "Audit"],
        "evidence_artifacts": ["Pull Request", "Review Approval", "Published Document"],
        "dependencies": "/docs/readme.md",
        "acceptance_criteria": "Lists every documentation artifact, groups by document type, and ensures all links resolve.",
        "raci": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Compliance\nInformed: Stakeholders",
        "kpis": "KPI – Timeliness: Updated as docs change\nKPI – Quality: Complete and accurate catalog\nKPI – Compliance: Supports audit navigation",
        "purpose": "Provide the canonical catalog of all documentation with working links."
    },
    
    # Core Policies
    "docs/policy/document-formatting.md": {
        "path": "docs/policy/document-formatting.md",
        "type": "policy",
        "subtype": "policy",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/change-management.md": {
        "path": "docs/policy/change-management.md",
        "type": "policy",
        "subtype": "policy",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/risk-register.md": {
        "path": "docs/policy/risk-register.md",
        "type": "policy",
        "subtype": "policy",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/data-classification.md": {
        "path": "docs/policy/data-classification.md",
        "type": "policy",
        "subtype": "policy",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/vendor-risk.md": {
        "path": "docs/policy/vendor-risk.md",
        "type": "policy",
        "subtype": "policy",
        "priority": "High",
        "approval": "Yes",
    },
    
    # WaaS Policies
    "docs/policy/waas/waas-security.md": {
        "path": "docs/policy/waas/waas-security.md",
        "type": "policy",
        "subtype": "waas",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/waas/waas-provisioning.md": {
        "path": "docs/policy/waas/waas-provisioning.md",
        "type": "policy",
        "subtype": "waas",
        "priority": "High",
        "approval": "Yes",
    },
    "docs/policy/waas/waas-tenant-isolation.md": {
        "path": "docs/policy/waas/waas-tenant-isolation.md",
        "type": "policy",
        "subtype": "waas",
        "priority": "High",
        "approval": "Yes",
    },
    
    # Core Guides
    "docs/guide/audit-readiness.md": {
        "path": "docs/guide/audit-readiness.md",
        "type": "guide",
        "subtype": "guide",
        "priority": "Medium",
        "approval": "No",
    },
    
    # WaaS Guides
    "docs/guide/waas/waas-architecture.md": {
        "path": "docs/guide/waas/waas-architecture.md",
        "type": "guide",
        "subtype": "waas",
        "priority": "Medium",
        "approval": "No",
    },
    "docs/guide/waas/waas-operations.md": {
        "path": "docs/guide/waas/waas-operations.md",
        "type": "guide",
        "subtype": "waas",
        "priority": "Medium",
        "approval": "No",
    },
    "docs/guide/waas/waas-client-onboarding.md": {
        "path": "docs/guide/waas/waas-client-onboarding.md",
        "type": "guide",
        "subtype": "waas",
        "priority": "Medium",
        "approval": "No",
    },
    
    # Checklists
    "docs/checklist/release.md": {
        "path": "docs/checklist/release.md",
        "type": "checklist",
        "subtype": "core",
        "priority": "Medium",
        "approval": "No",
    },
    
    # Templates Catalog
    "templates/docs/README.md": {
        "path": "templates/docs/README.md",
        "type": "index",
        "subtype": "catalog",
        "priority": "Low",
        "approval": "No",
    },
    "templates/docs/required/README.md": {
        "path": "templates/docs/required/README.md",
        "type": "index",
        "subtype": "catalog",
        "priority": "Low",
        "approval": "No",
    },
    "templates/docs/extra/README.md": {
        "path": "templates/docs/extra/README.md",
        "type": "index",
        "subtype": "catalog",
        "priority": "Low",
        "approval": "No",
    },
}


class DocumentationManager:
    """Manages documentation generation and Project #7 synchronization."""

    def __init__(self, org: str, project_number: int, repo_path: Path, token: Optional[str] = None):
        self.org = org
        self.project_number = project_number
        self.repo_path = repo_path
        self.token = token
        self.project_id = None
        self.field_ids = {}
        self.field_option_ids = {}
        self.existing_items = {}
        self.created_docs = []
        self.existing_docs = []
        self.created_tasks = []
        self.updated_tasks = []
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
            error_msg = f"Unexpected error: {type(e).__name__}: {e}"
            self.errors.append(error_msg)
            print(f"❌ ERROR: {error_msg}", file=sys.stderr)
            import traceback
            print(f"   Traceback: {traceback.format_exc()}", file=sys.stderr)
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
                result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)
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
            return self.project_id
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
                
                if "options" in field:
                    self.field_option_ids[field_name] = {
                        opt["name"]: opt["id"] for opt in field["options"]
                    }
            
            print(f"✅ Retrieved {len(self.field_ids)} project fields")
            return True
        return False

    def get_existing_project_items(self) -> bool:
        """Get existing items in the project."""
        query = """
        query($org: String!, $number: Int!) {
            organization(login: $org) {
                projectV2(number: $number) {
                    items(first: 100) {
                        nodes {
                            id
                            content {
                                ... on DraftIssue {
                                    title
                                    body
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
            items = result["data"]["organization"]["projectV2"]["items"]["nodes"]
            for item in items:
                if item.get("content"):
                    title = item["content"].get("title", "")
                    self.existing_items[title] = item["id"]
            
            print(f"✅ Found {len(self.existing_items)} existing project items")
            return True
        return False

    def check_document_exists(self, doc_path: str) -> bool:
        """Check if a document exists."""
        full_path = self.repo_path / doc_path
        return full_path.exists()

    def generate_document_content(self, doc_key: str, doc_info: Dict) -> str:
        """Generate document content based on type."""
        doc_path = doc_info["path"]
        doc_type = doc_info["type"]
        doc_name = Path(doc_path).stem
        
        # Common header
        header = f"""<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
 (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP: MokoStandards.{doc_type.capitalize()}
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: {doc_path}
 VERSION: 01.00.00
 BRIEF: {doc_name.replace('-', ' ').replace('_', ' ').title()}
 PATH: /{doc_path}
-->

"""

        if doc_type == "policy":
            content = header + f"""# {doc_name.replace('-', ' ').replace('_', ' ').title()}

## Purpose

This policy document defines the requirements and standards for {doc_name.replace('-', ' ')}.

## Scope

This policy applies to all {doc_name.replace('-', ' ')} activities within the MokoStandards ecosystem.

## Policy Statement

[Policy requirements to be defined]

## Roles and Responsibilities

* **Documentation Owner**: Maintains and updates this policy
* **Governance Owner**: Ensures compliance and enforcement
* **Security Owner**: Reviews security implications

## Compliance

Compliance with this policy is mandatory for all projects adopting MokoStandards.

## Review Cycle

This policy must be reviewed annually or when significant changes occur.

## Metadata

* Document: {doc_path}
* Repository: https://github.com/mokoconsulting-tech/MokoStandards
* Owner: Moko Consulting
* Approval Required: Yes
* Evidence Required: Yes
* Review Cycle: Annual
* Retention: Indefinite

## Revision History

| Version  | Date       | Author                          | Notes                    |
| -------- | ---------- | ------------------------------- | ------------------------ |
| 01.00.00 | 2026-01-04 | Jonathan Miller (@jmiller-moko) | Initial policy creation. |
"""

        elif doc_type == "guide":
            content = header + f"""# {doc_name.replace('-', ' ').replace('_', ' ').title()}

## Overview

This guide provides practical guidance for {doc_name.replace('-', ' ')}.

## Audience

This guide is intended for engineers, maintainers, and operators working with MokoStandards.

## Prerequisites

* Understanding of MokoStandards ecosystem
* Access to relevant systems and tools

## Guidance

[Detailed guidance to be provided]

## Best Practices

* Follow established patterns
* Document decisions and rationale
* Maintain consistency across implementations

## Related Documents

* See [docs/index.md](../index.md) for related policies and guides

## Metadata

* Document: {doc_path}
* Repository: https://github.com/mokoconsulting-tech/MokoStandards
* Owner: Moko Consulting
* Approval Required: No
* Review Cycle: Annual

## Revision History

| Version  | Date       | Author                          | Notes                  |
| -------- | ---------- | ------------------------------- | ---------------------- |
| 01.00.00 | 2026-01-04 | Jonathan Miller (@jmiller-moko) | Initial guide creation. |
"""

        elif doc_type == "checklist":
            content = header + f"""# {doc_name.replace('-', ' ').replace('_', ' ').title()}

## Purpose

This checklist ensures all requirements are met for {doc_name.replace('-', ' ')}.

## Checklist Items

### Pre-{doc_name.replace('-', ' ').title()}

- [ ] All prerequisites verified
- [ ] Documentation reviewed
- [ ] Stakeholders notified

### During {doc_name.replace('-', ' ').title()}

- [ ] Follow established procedures
- [ ] Document any deviations
- [ ] Verify compliance

### Post-{doc_name.replace('-', ' ').title()}

- [ ] Verify completion
- [ ] Update documentation
- [ ] Archive evidence

## Metadata

* Document: {doc_path}
* Repository: https://github.com/mokoconsulting-tech/MokoStandards
* Owner: Moko Consulting

## Revision History

| Version  | Date       | Author                          | Notes                       |
| -------- | ---------- | ------------------------------- | --------------------------- |
| 01.00.00 | 2026-01-04 | Jonathan Miller (@jmiller-moko) | Initial checklist creation. |
"""

        else:  # index or overview
            content = header + f"""# {doc_name.replace('-', ' ').replace('_', ' ').title()}

## Overview

This document provides an index and overview of {doc_name.replace('-', ' ')}.

## Contents

[Table of contents to be populated]

## Purpose

This index helps navigate the documentation structure and locate relevant documents.

## Metadata

* Document: {doc_path}
* Repository: https://github.com/mokoconsulting-tech/MokoStandards
* Owner: Moko Consulting

## Revision History

| Version  | Date       | Author                          | Notes                     |
| -------- | ---------- | ------------------------------- | ------------------------- |
| 01.00.00 | 2026-01-04 | Jonathan Miller (@jmiller-moko) | Initial index creation. |
"""

        return content

    def create_document(self, doc_key: str, doc_info: Dict) -> bool:
        """Create a missing document."""
        doc_path = self.repo_path / doc_info["path"]
        
        # Create parent directory if needed
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate content
        content = self.generate_document_content(doc_key, doc_info)
        
        # Write file
        try:
            with open(doc_path, 'w') as f:
                f.write(content)
            self.created_docs.append(doc_info["path"])
            return True
        except Exception as e:
            self.errors.append(f"Failed to create {doc_info['path']}: {e}")
            return False

    def create_project_task(self, doc_key: str, doc_info: Dict) -> bool:
        """Create a task in Project #7 for a document."""
        doc_path = doc_info["path"]
        doc_name = Path(doc_path).stem
        
        # Check if task already exists
        if doc_name in self.existing_items:
            self.updated_tasks.append(doc_path)
            return True
        
        title = doc_name
        body = f"""Document Path: {doc_path}
Purpose: {doc_info['type'].title()} document tracking
Acceptance Criteria:
- Document exists at correct path
- Content matches enterprise standards
- Required approvals obtained (if applicable)
- Evidence documented (if applicable)

Dependencies: None

Source: Generated from canonical document list"""
        
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
            self.created_tasks.append(doc_path)
            
            # Set field values
            self.set_task_fields(item_id, doc_info)
            
            return True
        else:
            self.errors.append(f"Failed to create task for {doc_path}")
            return False

    def set_task_fields(self, item_id: str, doc_info: Dict):
        """Set field values for a project task using enterprise field model."""
        # Set Document Path (text field)
        if "Document Path" in self.field_ids:
            self.set_text_field(item_id, "Document Path", doc_info["path"])
        
        # Set Acceptance Criteria (text field)
        if "Acceptance Criteria" in self.field_ids:
            criteria = f"""- Document exists at {doc_info['path']}
- Content matches enterprise standards
- {'Required approvals obtained' if doc_info['approval'] == 'Yes' else 'No approval required'}"""
            self.set_text_field(item_id, "Acceptance Criteria", criteria)
        
        # Set single-select fields using enterprise field model
        field_values = {
            "Status": "Planned",
            "Priority": doc_info["priority"],
            "Risk Level": "Low",
            "Document Type": doc_info["type"],
            "Document Subtype": doc_info["subtype"],
            "Owner Role": "Documentation Owner",
            "Approval Required": doc_info["approval"],
            "Evidence Required": "Yes" if doc_info["approval"] == "Yes" else "No",
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
                value: { text: $value }
            }) {
                projectV2Item { id }
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
                value: { singleSelectOptionId: $optionId }
            }) {
                projectV2Item { id }
            }
        }
        """
        self.run_graphql(mutation, {
            "projectId": self.project_id,
            "itemId": item_id,
            "fieldId": self.field_ids[field_name],
            "optionId": option_id
        })

    def process_documents(self):
        """Process all canonical documents."""
        print("\n📋 Processing canonical documents...")
        
        for doc_key, doc_info in CANONICAL_DOCUMENTS.items():
            doc_path = doc_info["path"]
            
            # Check if document exists
            if self.check_document_exists(doc_path):
                print(f"  ✅ Exists: {doc_path}")
                self.existing_docs.append(doc_path)
            else:
                print(f"  📝 Creating: {doc_path}")
                if self.create_document(doc_key, doc_info):
                    print(f"     ✅ Created: {doc_path}")
                else:
                    print(f"     ❌ Failed: {doc_path}")
            
            # Create or verify project task
            print(f"  📊 Task: {doc_path}")
            if self.create_project_task(doc_key, doc_info):
                if doc_path in self.created_tasks:
                    print(f"     ✅ Created task")
                else:
                    print(f"     ✅ Task exists")

    def print_summary(self):
        """Print summary report."""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)
        print(f"\n📊 Project: #{self.project_number}")
        print(f"   Organization: {self.org}")
        print(f"\n📄 Canonical Documents: {len(CANONICAL_DOCUMENTS)}")
        print(f"✅ Existing Documents: {len(self.existing_docs)}")
        print(f"📝 Created Documents: {len(self.created_docs)}")
        print(f"📊 Created Tasks: {len(self.created_tasks)}")
        print(f"📊 Existing Tasks: {len(self.updated_tasks)}")
        
        if self.created_docs:
            print(f"\n📝 Created Documents:")
            for doc in self.created_docs:
                print(f"   - {doc}")
        
        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"   - {error}")
            if len(self.errors) > 5:
                print(f"   ... and {len(self.errors) - 5} more")
        else:
            print("\n✅ No errors encountered")
        
        print("\n" + "="*70)


def main():
    """Main execution function."""
    print("="*70)
    print("Documentation Generation + Project #7 Task Sync")
    print("MokoStandards Enterprise Documentation Control")
    print("="*70)
    
    # Configuration
    ORG = "mokoconsulting-tech"
    PROJECT_NUMBER = 7
    REPO_PATH = Path("/home/runner/work/MokoStandards/MokoStandards")
    
    # Get token from environment
    token = os.environ.get("GH_PAT")
    
    # Initialize manager
    manager = DocumentationManager(ORG, PROJECT_NUMBER, REPO_PATH, token)
    
    # Step 1: Verify authentication
    print("\n🔐 Step 1: Verifying authentication...")
    if not manager.verify_auth():
        print("\n❌ STOP: Authentication required")
        print("\nPlease either:")
        print("  1. Set GH_PAT environment variable: export GH_PAT='your_token'")
        print("  2. Authenticate gh CLI: gh auth login")
        sys.exit(1)
    
    # Step 2: Get project
    print(f"\n📁 Step 2: Getting Project #{PROJECT_NUMBER}...")
    if not manager.get_project_id():
        print("\n❌ STOP: Failed to find project")
        sys.exit(1)
    
    # Step 3: Get project fields
    print("\n🔧 Step 3: Retrieving project fields...")
    manager.get_project_fields()
    
    # Step 4: Get existing items
    print("\n📊 Step 4: Retrieving existing project items...")
    manager.get_existing_project_items()
    
    # Step 5: Process documents
    print("\n📚 Step 5: Processing canonical documents...")
    manager.process_documents()
    
    # Print summary
    manager.print_summary()
    
    print("\n✅ Documentation and task sync completed!")
    print(f"\nView your project at:")
    print(f"https://github.com/orgs/{ORG}/projects/{PROJECT_NUMBER}")


if __name__ == "__main__":
    main()
