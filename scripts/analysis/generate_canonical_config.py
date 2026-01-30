#!/usr/bin/env python3
"""
Generate canonical documents configuration from enterprise JSON specification
"""

# Enterprise JSON specification
ENTERPRISE_SPEC = [
    {
        "title": "Repository README",
        "body": "Purpose:\n- Define repository scope, entry points, governance references, and documentation navigation links.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Low",
            "Document Type": "overview",
            "Document Subtype": "core",
            "Owner Role": "Documentation Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/README.md",
            "Dependencies": "/docs/readme.md",
            "Acceptance Criteria": "States repository purpose, links to /docs/readme.md and /docs/docs-index.md, and references governance entry points.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated within review cycle\nKPI – Quality: Passes documentation review\nKPI – Compliance: Aligns to governance and documentation policies"
        }
    },
    {
        "title": "Repository CHANGELOG",
        "body": "Purpose:\n- Track notable changes and releases using a consistent versioned log.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Low",
            "Document Type": "index",
            "Document Subtype": "core",
            "Owner Role": "Release Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Release"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/CHANGELOG.md",
            "Dependencies": "/README.md",
            "Acceptance Criteria": "Uses a consistent changelog format, captures notable changes, and aligns versions with releases.",
            "RACI": "Responsible: Release Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated per release\nKPI – Quality: Entries are complete and specific\nKPI – Compliance: Supports release evidence"
        }
    },
    {
        "title": "Repository LICENSE",
        "body": "Purpose:\n- Define the legal license governing repository contents and redistribution.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Medium",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Governance Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Ad hoc",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Published Document"],
            "Document Path": "/LICENSE",
            "Dependencies": "",
            "Acceptance Criteria": "Contains the correct license text and is aligned to repository SPDX expectations.",
            "RACI": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Legal\nInformed: Contributors",
            "KPIs": "KPI – Timeliness: Present prior to first release\nKPI – Quality: License text verified\nKPI – Compliance: Meets open source governance requirements"
        }
    },
    {
        "title": "Documentation README",
        "body": "Purpose:\n- Define documentation taxonomy, folder expectations, and navigation entry points.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Low",
            "Document Type": "overview",
            "Document Subtype": "core",
            "Owner Role": "Documentation Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/docs/readme.md",
            "Dependencies": "",
            "Acceptance Criteria": "Defines documentation layout, links to /docs/docs-index.md, and describes how policies, guides, and checklists are organized.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated within review cycle\nKPI – Quality: Navigation links verified\nKPI – Compliance: Conforms to formatting policy"
        }
    },
    {
        "title": "Documentation Index",
        "body": "Purpose:\n- Provide the canonical catalog of all documentation with working links.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Low",
            "Document Type": "index",
            "Document Subtype": "catalog",
            "Owner Role": "Documentation Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/docs-index.md",
            "Dependencies": "/docs/readme.md",
            "Acceptance Criteria": "Lists every documentation artifact, groups by document type, and ensures all links resolve.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Compliance\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated as docs change\nKPI – Quality: Complete and accurate catalog\nKPI – Compliance: Supports audit navigation"
        }
    },
    {
        "title": "Document Formatting Policy",
        "body": "Purpose:\n- Define mandatory markdown structure requirements, including metadata and revision history rules.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Medium",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Documentation Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/document-formatting.md",
            "Dependencies": "/docs/readme.md",
            "Acceptance Criteria": "Defines required sections, heading rules, and establishes precedence over conflicting guidance.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Compliance\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Reviewed annually\nKPI – Quality: Policy is unambiguous\nKPI – Compliance: Enforced by governance checks"
        }
    },
    {
        "title": "Change Management Policy",
        "body": "Purpose:\n- Define change classification, approvals, implementation controls, and rollback expectations.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Medium",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Governance Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/change-management.md",
            "Dependencies": "/docs/policy/document-formatting.md",
            "Acceptance Criteria": "Defines change classes, approval requirements, rollback steps, and evidence expectations.",
            "RACI": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Operations Owner, Security Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Applied to all changes\nKPI – Quality: Clear approvals and rollback\nKPI – Compliance: Evidence retained"
        }
    },
    {
        "title": "Risk Register",
        "body": "Purpose:\n- Maintain a centralized register of risks, impacts, owners, and mitigation actions.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Governance Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Quarterly",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Published Document"],
            "Document Path": "/docs/policy/risk-register.md",
            "Dependencies": "",
            "Acceptance Criteria": "Tracks risks with consistent fields, assigns ownership, and documents mitigation status.",
            "RACI": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated quarterly\nKPI – Quality: Risks actionable\nKPI – Compliance: Supports audit readiness"
        }
    },
    {
        "title": "Data Classification Policy",
        "body": "Purpose:\n- Define data classification tiers and required handling controls across systems.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Security Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Security", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/data-classification.md",
            "Dependencies": "/docs/policy/document-formatting.md",
            "Acceptance Criteria": "Defines tiers, maps handling requirements, and aligns to access control and retention expectations.",
            "RACI": "Responsible: Security Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Reviewed annually\nKPI – Quality: Clear tier definitions\nKPI – Compliance: Handling requirements enforced"
        }
    },
    {
        "title": "Vendor Risk Policy",
        "body": "Purpose:\n- Establish a standardized process for assessing and approving third-party vendor risk.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "policy",
            "Document Subtype": "core",
            "Owner Role": "Governance Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "7 Years",
            "Compliance Tags": ["Governance", "Security", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/vendor-risk.md",
            "Dependencies": "/docs/policy/risk-register.md",
            "Acceptance Criteria": "Defines evaluation criteria, approval thresholds, reassessment cadence, and evidence capture.",
            "RACI": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Completed before vendor onboarding\nKPI – Quality: Assessments complete\nKPI – Compliance: Evidence retained"
        }
    },
    {
        "title": "WaaS Security Policy",
        "body": "Purpose:\n- Define security requirements, access controls, and incident expectations for WaaS operations.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "policy",
            "Document Subtype": "waas",
            "Owner Role": "Security Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Security", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/waas/waas-security.md",
            "Dependencies": "/docs/policy/document-formatting.md",
            "Acceptance Criteria": "Defines privileged access controls, authentication expectations, logging requirements, and incident handling.",
            "RACI": "Responsible: Security Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Reviewed annually\nKPI – Quality: Security controls explicit\nKPI – Compliance: Meets security policy requirements"
        }
    },
    {
        "title": "WaaS Provisioning Policy",
        "body": "Purpose:\n- Define provisioning workflow, validation gates, and approval requirements for WaaS deployments.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Medium",
            "Document Type": "policy",
            "Document Subtype": "waas",
            "Owner Role": "Operations Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "5 Years",
            "Compliance Tags": ["Operations", "Governance", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/waas/waas-provisioning.md",
            "Dependencies": "/docs/policy/waas/waas-security.md",
            "Acceptance Criteria": "Defines provisioning stages, required validations, approval points, and operational evidence requirements.",
            "RACI": "Responsible: Operations Owner\nAccountable: Governance Owner\nConsulted: Security Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Applied to each provisioning\nKPI – Quality: Validation steps complete\nKPI – Compliance: Evidence captured"
        }
    },
    {
        "title": "WaaS Tenant Isolation Policy",
        "body": "Purpose:\n- Define tenant isolation, segmentation, and data separation controls for multi-tenant WaaS.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "policy",
            "Document Subtype": "waas",
            "Owner Role": "Security Owner",
            "Approval Required": "Yes",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Security", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/policy/waas/waas-tenant-isolation.md",
            "Dependencies": "/docs/policy/waas/waas-security.md",
            "Acceptance Criteria": "Defines isolation model, required controls, validation/testing expectations, and breach containment procedures.",
            "RACI": "Responsible: Security Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Approved before production\nKPI – Quality: Isolation controls verifiable\nKPI – Compliance: Meets tenant separation requirements"
        }
    },
    {
        "title": "Audit Readiness Guide",
        "body": "Purpose:\n- Provide procedures for audit preparation, evidence collection, and control mapping.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "High",
            "Document Type": "guide",
            "Document Subtype": "core",
            "Owner Role": "Governance Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Audit", "Governance"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/docs/guide/audit-readiness.md",
            "Dependencies": "/docs/policy/risk-register.md",
            "Acceptance Criteria": "Defines audit scope, evidence sources, control mapping approach, and a repeatable preparation workflow.",
            "RACI": "Responsible: Governance Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Ready prior to audit window\nKPI – Quality: Evidence pathways complete\nKPI – Compliance: Supports audit requests"
        }
    },
    {
        "title": "WaaS Architecture Guide",
        "body": "Purpose:\n- Describe WaaS architecture, components, trust boundaries, and operational constraints.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Medium",
            "Document Type": "guide",
            "Document Subtype": "waas",
            "Owner Role": "Documentation Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Semiannual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Operations", "Security"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/docs/guide/waas/waas-architecture.md",
            "Dependencies": "/docs/policy/waas/waas-security.md",
            "Acceptance Criteria": "Documents component diagram narrative, trust boundaries, integration points, and links to relevant WaaS policies.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Security Owner, Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated per major platform change\nKPI – Quality: Architecture consistent\nKPI – Compliance: Supports security review"
        }
    },
    {
        "title": "WaaS Operations Guide",
        "body": "Purpose:\n- Provide operational procedures for monitoring, maintenance, escalation, and service continuity.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Medium",
            "Document Type": "guide",
            "Document Subtype": "waas",
            "Owner Role": "Operations Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Semiannual",
            "Retention": "5 Years",
            "Compliance Tags": ["Operations"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/docs/guide/waas/waas-operations.md",
            "Dependencies": "/docs/policy/waas/waas-provisioning.md",
            "Acceptance Criteria": "Defines monitoring expectations, escalation paths, maintenance windows, and operational evidence capture.",
            "RACI": "Responsible: Operations Owner\nAccountable: Governance Owner\nConsulted: Security Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Updated per operational change\nKPI – Quality: Procedures actionable\nKPI – Compliance: Aligns with WaaS policies"
        }
    },
    {
        "title": "WaaS Client Onboarding Guide",
        "body": "Purpose:\n- Define client onboarding prerequisites, provisioning handoff, and acceptance requirements.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Medium",
            "Document Type": "guide",
            "Document Subtype": "waas",
            "Owner Role": "Operations Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "3 Years",
            "Compliance Tags": ["Operations", "Governance"],
            "Evidence Artifacts": ["Pull Request", "Published Document"],
            "Document Path": "/docs/guide/waas/waas-client-onboarding.md",
            "Dependencies": "/docs/policy/waas/waas-provisioning.md",
            "Acceptance Criteria": "Defines onboarding checklist, required inputs, provisioning completion checks, and client acceptance criteria.",
            "RACI": "Responsible: Operations Owner\nAccountable: Governance Owner\nConsulted: Security Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Completed before activation\nKPI – Quality: Steps verifiable\nKPI – Compliance: Aligns to provisioning policy"
        }
    },
    {
        "title": "Release Checklist",
        "body": "Purpose:\n- Provide a verifiable checklist for release readiness, validation, and evidence capture.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Low",
            "Document Type": "checklist",
            "Document Subtype": "core",
            "Owner Role": "Release Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "5 Years",
            "Compliance Tags": ["Release", "Audit"],
            "Evidence Artifacts": ["Pull Request", "Review Approval", "Published Document"],
            "Document Path": "/docs/checklist/release.md",
            "Dependencies": "/CHANGELOG.md",
            "Acceptance Criteria": "Checklist steps are objective, include evidence capture, and can be completed as part of each release.",
            "RACI": "Responsible: Release Owner\nAccountable: Governance Owner\nConsulted: Operations Owner\nInformed: Stakeholders",
            "KPIs": "KPI – Timeliness: Applied per release\nKPI – Quality: Checklist complete\nKPI – Compliance: Evidence retained"
        }
    },
    {
        "title": "Templates Documentation Catalog",
        "body": "Purpose:\n- Provide entry point and navigation for documentation templates.",
        "fields": {
            "Status": "Planned",
            "Priority": "Medium",
            "Risk Level": "Low",
            "Document Type": "index",
            "Document Subtype": "catalog",
            "Owner Role": "Documentation Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance"],
            "Evidence Artifacts": ["Published Document"],
            "Document Path": "/templates/docs/README.md",
            "Dependencies": "/docs/readme.md",
            "Acceptance Criteria": "Lists required and extra templates and links to /templates/docs/required/README.md and /templates/docs/extra/README.md.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nInformed: Contributors",
            "KPIs": "KPI – Timeliness: Updated when templates change\nKPI – Quality: Links valid\nKPI – Compliance: Supports documentation standards"
        }
    },
    {
        "title": "Required Templates README",
        "body": "Purpose:\n- Provide the required template inventory and usage rules for mandatory documentation artifacts.",
        "fields": {
            "Status": "Planned",
            "Priority": "High",
            "Risk Level": "Low",
            "Document Type": "index",
            "Document Subtype": "catalog",
            "Owner Role": "Documentation Owner",
            "Approval Required": "No",
            "Evidence Required": "Yes",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance", "Audit"],
            "Evidence Artifacts": ["Published Document"],
            "Document Path": "/templates/docs/required/README.md",
            "Dependencies": "/templates/docs/README.md",
            "Acceptance Criteria": "Lists required templates, defines when mandatory, and links back to the templates catalog.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nConsulted: Compliance\nInformed: Contributors",
            "KPIs": "KPI – Timeliness: Updated when required templates change\nKPI – Quality: Inventory accurate\nKPI – Compliance: Supports enforcement"
        }
    },
    {
        "title": "Extra Templates README",
        "body": "Purpose:\n- Provide optional template inventory and recommended usage guidance.",
        "fields": {
            "Status": "Planned",
            "Priority": "Low",
            "Risk Level": "Low",
            "Document Type": "index",
            "Document Subtype": "catalog",
            "Owner Role": "Documentation Owner",
            "Approval Required": "No",
            "Evidence Required": "No",
            "Review Cycle": "Annual",
            "Retention": "Indefinite",
            "Compliance Tags": ["Governance"],
            "Evidence Artifacts": ["Published Document"],
            "Document Path": "/templates/docs/extra/README.md",
            "Dependencies": "/templates/docs/README.md",
            "Acceptance Criteria": "Lists optional templates with recommended use cases and links back to the templates catalog.",
            "RACI": "Responsible: Documentation Owner\nAccountable: Governance Owner\nInformed: Contributors",
            "KPIs": "KPI – Timeliness: Updated when optional templates change\nKPI – Quality: Inventory accurate\nKPI – Compliance: Non-blocking guidance"
        }
    }
]

def convert_to_canonical_format():
    """Convert enterprise spec to canonical documents format."""
    canonical = {}

    for spec in ENTERPRISE_SPEC:
        # Strip leading slash from path
        path = spec["fields"]["Document Path"].lstrip("/")

        # Get purpose from body
        purpose_lines = spec["body"].split("\n")
        purpose = ""
        for line in purpose_lines:
            if line.startswith("- "):
                purpose = line[2:]
                break

        canonical[path] = {
            "path": path,
            "title": spec["title"],
            "type": spec["fields"]["Document Type"],
            "subtype": spec["fields"]["Document Subtype"],
            "priority": spec["fields"]["Priority"],
            "risk_level": spec["fields"]["Risk Level"],
            "approval": spec["fields"]["Approval Required"],
            "evidence": spec["fields"]["Evidence Required"],
            "review_cycle": spec["fields"]["Review Cycle"],
            "retention": spec["fields"]["Retention"],
            "compliance_tags": spec["fields"]["Compliance Tags"],
            "evidence_artifacts": spec["fields"]["Evidence Artifacts"],
            "dependencies": spec["fields"]["Dependencies"],
            "acceptance_criteria": spec["fields"]["Acceptance Criteria"],
            "raci": spec["fields"]["RACI"],
            "kpis": spec["fields"]["KPIs"],
            "purpose": purpose,
            "owner_role": spec["fields"]["Owner Role"]
        }

    return canonical

if __name__ == "__main__":
    canonical_docs = convert_to_canonical_format()

    print("# Generated Canonical Documents Configuration")
    print(f"# Total documents: {len(canonical_docs)}\n")

    print("CANONICAL_DOCUMENTS = {")
    for path, config in canonical_docs.items():
        print(f'    "{path}": {{')
        for key, value in config.items():
            if isinstance(value, list):
                print(f'        "{key}": {value},')
            elif isinstance(value, str):
                # Escape quotes and newlines
                escaped_value = value.replace('"', '\\"').replace('\n', '\\n')
                print(f'        "{key}": "{escaped_value}",')
            else:
                print(f'        "{key}": {value},')
        print('    },')
    print("}")
