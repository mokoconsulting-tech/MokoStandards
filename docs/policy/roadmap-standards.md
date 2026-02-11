<!--
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

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/policy/roadmap-standards.md
VERSION: 03.02.00
BRIEF: Standards and requirements for ROADMAP.md files across organization repositories
-->

# ROADMAP.md Standards

## Overview

This document defines standards for roadmap documentation across all Moko Consulting organization repositories. The roadmap system uses a **two-tier structure** that separates high-level version planning from detailed implementation plans.

## Two-Tier Roadmap Structure

### Tier 1: Root ROADMAP.md (Version Planning)

**Location**: Repository root (`ROADMAP.md`)  
**Purpose**: High-level version planning and release strategy  
**Audience**: Everyone (developers, management, stakeholders)  
**Update Frequency**: Per release (monthly for MINOR, quarterly for MAJOR)

**Focus**:
- Current and upcoming versions
- Release schedule and strategy
- Version milestones
- Feature summary per version
- Links to detailed planning

### Tier 2: Implementation Planning (Detailed)

**Location**: `docs/planning/` directory  
**Purpose**: Detailed implementation plans, tasks, and resources  
**Audience**: Implementation teams (developers, team leads)  
**Update Frequency**: Weekly/sprint cycles

**Focus**:
- Week-by-week action items
- Resource allocation
- Integration examples
- Training schedules
- Success metrics tracking
- Sprint planning

## Purpose

The roadmap system serves to:

1. **Communicate Direction**: Provide clear visibility into project evolution and priorities
2. **Manage Expectations**: Set realistic timelines and scope for stakeholders
3. **Track Progress**: Document completed, in-progress, and planned work
4. **Enable Planning**: Support strategic decision-making with version-based milestones
5. **Separate Concerns**: Version planning (what/when) vs implementation (how/who)
6. **Maintain History**: Preserve decisions and rationale for future reference

## Scope

### When ROADMAP.md is Required

- **Suggested** for all organization repositories
- **Highly Recommended** for:
  - Customer-facing products and services
  - Public-facing projects and libraries
  - Projects with external stakeholders or dependencies
  - Long-term initiatives spanning multiple versions

### When ROADMAP.md May Be Optional

- Internal utility scripts with single-purpose scope
- Archived or deprecated repositories
- Repositories that are forks of external projects (use upstream roadmap)

## Content Requirements

### Required Sections for Root ROADMAP.md

All root ROADMAP.md files MUST include:

1. **Scope and Intent**
   - Clear statement of what the roadmap covers
   - Version baseline (starting point)
   - Forward-looking focus statement

2. **Version Sections**
   - At least one version section (current or planned)
   - Version number following semantic versioning
   - Phase name describing the version's focus
   - Status indicator (✅ COMPLETED, 🔄 IN PROGRESS, 📋 PLANNED)

3. **Deliverables**
   - Clear, actionable items
   - Categorized by theme or functional area
   - Status indicators for tracking

4. **Outcomes**
   - Measurable benefits or achievements
   - Value statements for stakeholders

5. **Metadata**
   - Owner/maintainer
   - Last updated date
   - Status (Active, Draft, Archived)

6. **Revision History**
   - Table of changes with dates, authors, and descriptions

### Recommended Sections for Root ROADMAP.md

- **Release Strategy**: MAJOR/MINOR/PATCH cycle explanation
- **Planning Horizon**: Timeframe and confidence levels (Q1, Q2, Year 1)
- **Status Indicators**: Legend for tracking symbols
- **Quick Reference**: Table linking to detailed documentation
- **Role-based Navigation**: Links for developers, team leads, management
- **Links to Implementation Plans**: Point to docs/planning/ for details

### Required Sections for docs/planning/README.md

All implementation planning documents MUST include:

1. **Immediate Actions** (Week 1)
   - Specific tasks with hour estimates
   - Priority levels
   - Assignees or team allocation
   
2. **Short-term Goals** (Month 1)
   - Integration milestones
   - Resource requirements
   - Training schedules
   
3. **Medium-term Goals** (Quarter 1)
   - Feature completion targets
   - Performance metrics
   - Rollout plans
   
4. **Long-term Vision** (Year 1)
   - Strategic initiatives
   - Advanced capabilities
   - Architectural evolution
   
5. **Success Metrics**
   - KPIs and tracking dashboards
   - Adoption metrics
   - Performance targets
   
6. **Resource Requirements**
   - Team allocation by phase
   - Budget estimates
   - Timeline dependencies

## Version Numbering Standards

### Semantic Versioning

Use semantic versioning (MAJOR.MINOR.PATCH) for clarity:

- **MAJOR** (X.0.0): Breaking changes, major architectural shifts, API changes
- **MINOR** (X.Y.0): New features, significant enhancements, backwards-compatible additions
- **PATCH** (X.Y.Z): Bug fixes, documentation updates, minor improvements

### Version Organization

Organize versions in descending order (newest first):
1. Current/Active version (what's being delivered now)
2. Recently completed versions
3. Planned versions (next 2-3 releases)
4. Long-term vision (beyond immediate horizon)

### Version Goals

Each version SHOULD:
- Have a clear, focused theme (e.g., "Security Hardening", "Performance Optimization")
- Target 3-8 major deliverables (not too broad, not too narrow)
- Define measurable outcomes
- Span a reasonable timeframe (weeks to months, not years)

## Content Standards

### Deliverables Format

Structure deliverables clearly:

```markdown
* ✅ **Category Name**
  * ✅ Specific deliverable with concrete scope
  * 🔄 Another deliverable (in progress)
  * 📋 Planned deliverable
```

**Best Practices**:
- Use action-oriented language ("Implement X", "Add support for Y")
- Be specific and measurable
- Avoid vague statements like "improve performance"
- Include success criteria where applicable

### Status Indicators

Use consistent status indicators:

- ✅ **COMPLETED**: Delivered, tested, and validated
- 🔄 **IN PROGRESS**: Active development underway
- 📋 **PLANNED**: Scheduled but not yet started
- ⏸️ **PAUSED**: Temporarily on hold (include reason)
- ❌ **CANCELLED**: No longer pursuing (include reason)
- ⚠️ **AT RISK**: Facing blockers or delays

### Outcomes Format

Frame outcomes as value statements:

```markdown
* ✅ Reduced deployment time by 50%
* ✅ Automated 12 hours/month of manual work
* 🔄 Improved security posture with automated scanning
```

### Writing Style

- **Be concise**: Use bullet points, not paragraphs
- **Be specific**: Include quantifiable goals where possible
- **Be realistic**: Don't overpromise; adjust roadmap as needed
- **Be transparent**: Include completed items to show progress
- **Be forward-looking**: Focus on future state, not detailed past work

## File Structure

### Location - Two-Tier System

**Tier 1: Version Planning**
- **Location**: `ROADMAP.md` in repository root (REQUIRED)
- **Purpose**: Version planning and releases
- **Size**: Typically 5-10KB
- **Format**: Markdown (.md), UTF-8, LF line endings

**Tier 2: Implementation Planning**
- **Location**: `docs/planning/` directory (REQUIRED for complex projects)
- **Primary File**: `docs/planning/README.md`
- **Supporting Files**:
  - `docs/planning/phases/` - Phase documentation
  - `docs/planning/milestones/` - Milestone tracking
  - `docs/planning/sprints/` - Sprint plans (optional)
- **Purpose**: Detailed implementation plans
- **Size**: 10-20KB+ depending on project complexity
- **Format**: Markdown (.md), UTF-8, LF line endings

### Templates

- **Root ROADMAP.md**: `templates/docs/extra/template-ROADMAP.md`
- **Planning Directory**: `templates/docs/extra/template-planning-README.md`

## Integration with Repository Schemas

ROADMAP.md is defined as a **suggested** file in repository structure schemas:

- `scripts/definitions/default-repository.xml`
- `scripts/definitions/waas-component.xml`
- `scripts/definitions/crm-module.xml`
- `scripts/definitions/generic-repository.xml`

Repositories that adopt MokoStandards SHOULD include ROADMAP.md as part of their documentation suite.

## Maintenance Requirements

### Update Frequency

- **Minimum**: Quarterly review and updates
- **Recommended**: Monthly for active projects
- **Required**: When:
  - Major milestones are completed
  - Version scope changes significantly
  - Priorities shift due to business needs
  - New versions are planned

### Review Process

1. Review current version progress
2. Update status indicators
3. Adjust timelines if needed
4. Add newly planned versions
5. Archive completed versions (move to revision history if too many)
6. Update metadata (Last Updated date)
7. Document changes in Revision History table

## Examples

### Good Example: Clear and Focused

```markdown
## Version 2.1.0 — Performance Optimization 🔄 IN PROGRESS

Focus: Reduce API response times and improve scalability

### Completed Deliverables
* ✅ **Database Optimization**
  * ✅ Added indexes on frequently queried tables
  * ✅ Implemented query result caching

### In Progress
* 🔄 Load balancer configuration
* 🔄 CDN integration for static assets

### Outcomes
* ✅ Reduced average API response time from 500ms to 200ms
* 🔄 Supporting 2x concurrent users without performance degradation
```

### Poor Example: Vague and Unfocused

```markdown
## Version 2.1.0 — Various Improvements

* Make things faster
* Fix bugs
* Add new features
* Improve user experience

### Outcomes
* Better performance
* Fewer issues
```

## Relationship to Other Documents

- **CHANGELOG.md**: Detailed change log (past-focused, technical)
- **ROADMAP.md**: Strategic plan (future-focused, value-oriented)
- **README.md**: Project overview (present state, getting started)
- **CONTRIBUTING.md**: How to participate (process, not timeline)

These documents complement each other and serve different purposes.

## Validation

Repositories MAY use automated validation to ensure:
- ROADMAP.md exists (if required by schema)
- Required sections are present
- Metadata is properly formatted
- Version numbers follow semantic versioning
- Revision history is maintained

## Template Usage

To create a new ROADMAP.md:

```bash
# Copy template to repository root
cp templates/docs/extra/template-ROADMAP.md ./ROADMAP.md

# Customize placeholders
# Replace [Project Name], [Version Numbers], [Phase Names], etc.
```

## Best Practices

### Do's

- ✅ Keep versions focused and achievable
- ✅ Update regularly to reflect reality
- ✅ Be transparent about delays or changes
- ✅ Use version numbers that match release tags
- ✅ Include measurable outcomes
- ✅ Archive old versions to keep document manageable
- ✅ Link to related issues/PRs where applicable

### Don'ts

- ❌ Make promises you can't keep
- ❌ Include too much detail (save for issues/docs)
- ❌ Let the roadmap become stale
- ❌ Use vague or unmeasurable goals
- ❌ Forget to update status indicators
- ❌ Hide completed work (show progress!)
- ❌ Plan more than 3-4 versions ahead in detail

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/roadmap-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
