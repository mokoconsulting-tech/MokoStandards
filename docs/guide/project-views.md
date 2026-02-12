[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# GitHub Project v2 Views Configuration

## Overview

This document defines the default views to be created manually in the MokoStandards Documentation Control Register GitHub Project v2. Views provide tailored perspectives on the documentation register to support different governance, operational, and compliance activities.

## Required Views

### 1. Master Register

**Purpose:** Comprehensive view of all documentation items in the register.

**Configuration:**
- **Layout:** Table
- **Columns:** Title, Status, Document Type, Document Subtype, Document Path, Owner Role, Priority, Risk Level, Review Cycle, Compliance Tags
- **Sort:** Status (ascending), then Priority (High to Low)
- **Filter:** None (show all items)

**Usage:** Primary reference view for governance oversight, audits, and compliance reporting. Provides complete inventory of all documentation artifacts.

**Audience:** Governance Owners, Auditors, Executive Leadership

---

### 2. Execution Kanban

**Purpose:** Operational view for active documentation work and task management.

**Configuration:**
- **Layout:** Board
- **Group by:** Status
- **Columns:** Planned, In Progress, In Review, Approved, Published, Blocked
- **Card fields:** Title, Owner Role, Priority, Risk Level, Document Type
- **Filter:** Exclude Status = Archived

**Usage:** Daily operational view for Documentation Owners to manage active work, track progress, and identify blockers.

**Audience:** Documentation Owners, Operations Owners, Project Managers

---

### 3. Governance Gate

**Purpose:** Focus on items requiring governance review, approval, or escalation.

**Configuration:**
- **Layout:** Table
- **Columns:** Title, Status, Owner Role, Approval Required, Evidence Required, Evidence Artifacts, Risk Level, Compliance Tags
- **Filter:** Status = In Review OR (Approval Required = Yes AND Status != Published) OR (Evidence Required = Yes AND Evidence Artifacts is empty)
- **Sort:** Risk Level (High to Low), then Priority (High to Low)

**Usage:** Governance Owners use this view to identify items awaiting review, approval, or evidence collection. Ensures governance gates are enforced.

**Audience:** Governance Owners, Compliance Officers, Security Owners

---

### 4. Policy Register

**Purpose:** Dedicated view for policy documentation artifacts.

**Configuration:**
- **Layout:** Table
- **Columns:** Title, Status, Document Subtype, Document Path, Owner Role, Review Cycle, Retention, Compliance Tags
- **Filter:** Document Type = policy
- **Sort:** Status (ascending), then Review Cycle

**Usage:** Track all policy documents, review schedules, and retention requirements. Supports policy lifecycle management and compliance audits.

**Audience:** Governance Owners, Compliance Officers, Policy Managers

---

### 5. WaaS Portfolio

**Purpose:** View all WordPress as a Service (WaaS) related documentation.

**Configuration:**
- **Layout:** Table
- **Columns:** Title, Status, Document Type, Document Path, Owner Role, Priority, Review Cycle
- **Filter:** Document Subtype = waas
- **Sort:** Priority (High to Low), then Status

**Usage:** Operations Owners managing WaaS platform use this view to access all relevant documentation, procedures, and policies.

**Audience:** Operations Owners, WaaS Platform Team, Security Owners

---

### 6. High Risk and Blockers

**Purpose:** Executive dashboard highlighting high-risk items and blocked work.

**Configuration:**
- **Layout:** Table
- **Columns:** Title, Status, Risk Level, Priority, Owner Role, Compliance Tags, Dependencies
- **Filter:** Risk Level = High OR Status = Blocked
- **Sort:** Risk Level (High to Low), then Priority (High to Low)

**Usage:** Executive leadership and governance escalation view. Identifies items requiring immediate attention, resource allocation, or risk mitigation.

**Audience:** Executive Leadership, Governance Owners, Risk Management

---

### 7. Insights Dashboard

**Purpose:** Metrics and analytics view for performance tracking and reporting.

**Configuration:**
- **Layout:** Chart/Insights
- **Metrics to display:**
  - Count of items by Status
  - Count of items by Risk Level
  - Count of items by Document Type
  - Count of items requiring Approval (Approval Required = Yes)
  - Count of items requiring Evidence (Evidence Required = Yes and Evidence Artifacts is empty)
  - Distribution by Owner Role
  - Items by Compliance Tags
- **Date range:** All time

**Usage:** Performance reporting, compliance metrics, capacity planning, and trend analysis. Supports governance reporting and continuous improvement.

**Audience:** Governance Owners, Executive Leadership, Project Managers

---

## Excluded Views

### Roadmap View

**Rationale for Exclusion:**

The Roadmap view is explicitly excluded from this documentation governance framework because:

1. **Governance focus over scheduling:** This Project serves as a documentation register and governance control system, not a project scheduling or roadmap planning tool.

2. **Status-based lifecycle:** Documentation follows a status-based lifecycle (Planned → Published → Archived) rather than a time-based roadmap. Review cycles are defined per-item, not as milestones on a timeline.

3. **Compliance orientation:** Governance and compliance activities are event-driven and policy-driven, not calendar-driven. The Review Cycle field provides scheduled governance triggers without requiring roadmap visualization.

4. **Separate planning systems:** Organizational roadmaps and strategic planning are managed in separate systems. This Project focuses on documentation governance, compliance, and execution.

If time-based planning becomes necessary, a separate GitHub Project can be created for roadmap visualization while maintaining this Project as the authoritative documentation register.

---

## View Creation Instructions

Views must be created manually via the GitHub Project v2 web interface:

1. Navigate to the MokoStandards Documentation Control Register Project
2. Click "+ New view" in the view tabs
3. Select the appropriate layout (Table, Board, or Chart)
4. Configure columns, filters, sorting, and grouping as specified
5. Name the view according to the names above
6. Save the view

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/project-views.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
