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
PATH: docs/policy/planning-guidance.md
VERSION: 04.00.15
BRIEF: Enterprise guidance for implementation planning and sprint documentation
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Planning Guidance

**Document Type**: Policy  
**Version**: 04.00.04  
**Last Updated**: 2026-02-11  
**Status**: Active

## Overview

This document provides guidance for creating and maintaining implementation plans in the `docs/planning/` directory. It complements the root ROADMAP.md (version planning) with detailed execution guidance.

## Two-Tier Planning System

### Tier 1: Version Planning (ROADMAP.md)
- **What**: Versions, releases, features
- **When**: Timeline and milestones
- **Who**: Everyone (broad audience)
- **Update**: Per release

### Tier 2: Implementation Planning (docs/planning/)
- **How**: Tasks, workflows, examples
- **Who**: Team allocation and resources
- **Audience**: Implementation teams
- **Update**: Weekly/sprint cycles

## docs/planning/ Directory Structure

### Required Files

```
docs/planning/
├── README.md              ← Primary implementation roadmap
├── phases/                ← Phase documentation
│   ├── phase-1-*.md
│   ├── phase-2-*.md
│   └── phase-3-*.md
└── milestones/            ← Milestone tracking
    └── README.md
```

### Optional Subdirectories

```
docs/planning/
├── sprints/               ← Sprint planning (Agile teams)
│   ├── sprint-1.md
│   └── sprint-2.md
├── resources/             ← Resource allocation
│   └── team-allocation.md
└── metrics/               ← Success metrics tracking
    └── kpis.md
```

## docs/planning/README.md Structure

### Required Sections

1. **Immediate Actions** (Week 1)
   - Specific tasks with hour estimates
   - Priority levels (HIGH/MEDIUM/LOW)
   - Dependencies and blockers
   
2. **Short-term Goals** (Month 1)
   - Integration milestones
   - Resource requirements
   - Training schedules
   - Success criteria
   
3. **Medium-term Goals** (Quarter 1)
   - Feature completion targets
   - Performance metrics
   - Rollout phases
   
4. **Long-term Vision** (Year 1)
   - Strategic initiatives
   - Advanced capabilities
   - Architectural evolution
   
5. **Success Metrics**
   - KPIs and dashboards
   - Adoption metrics
   - Performance targets
   - Quality metrics
   
6. **Resource Requirements**
   - Team allocation by phase
   - Budget estimates
   - Timeline dependencies
   - Approval checklists

### Recommended Sections

- **Integration Examples**: Code samples and patterns
- **Training Materials**: Team enablement resources
- **Risk Management**: Risks and mitigation strategies
- **Continuous Improvement**: Feedback loops and iteration plans

## Content Guidelines

### Task Descriptions

**Good Examples**:
```markdown
- Update bulk_update_repos.php with enterprise audit logging (4 hours)
- Deploy Grafana dashboard for metrics collection (3 hours)
- Conduct training session on API client usage (2 hours)
```

**Poor Examples**:
```markdown
- Update scripts
- Set up monitoring
- Train team
```

### Resource Allocation

**Format**:
```markdown
### Week 1 Resources
- 2 Senior Developers × 20 hours = 40 hours
- 1 DevOps Engineer × 10 hours = 10 hours
- Total: 50 hours
```

### Success Metrics

**Format**:
```markdown
| Metric | Baseline | Target | Status |
|--------|----------|--------|--------|
| Scripts integrated | 0% | 50% | 📊 Tracking |
| API errors | 10/mo | 0 | 📊 Tracking |
| MTTR | Unknown | <15min | 📊 Tracking |
```

## Phase Documentation

### Location
`docs/planning/phases/phase-X-name.md`

### Structure

Each phase document should include:

1. **Status**: Complete/In Progress/Planned
2. **Delivered**: Date of completion
3. **Effort**: Actual vs estimated time
4. **Overview**: What the phase accomplished
5. **Objectives**: Clear goals
6. **Deliverables**: Specific outputs with details
7. **Success Metrics**: How success was measured
8. **Impact**: Before/after comparison
9. **Lessons Learned**: What worked, what didn't
10. **Next Phase**: Link to subsequent work

### Example

```markdown
# Phase 2: Enterprise Libraries - Complete

**Status**: ✅ COMPLETE  
**Delivered**: 2026-02-11  
**Effort**: 1 session (originally estimated 4 weeks)

## Overview
Transform automation from functional to enterprise-grade...

## Deliverables
1. Enterprise Audit Library (470 lines)
   - Transaction tracking
   - Security event logging
   ...
```

## Milestone Tracking

### Location
`docs/planning/milestones/`

### Format

```markdown
## Q1 2026 Milestones

### Milestone 1: Enterprise Foundation ✅
- Target: 2026-02-11
- Status: Complete
- Deliverables: 8 libraries, 2 frameworks
- Impact: Foundation ready for adoption

### Milestone 2: Integration Phase 📋
- Target: 2026-03-31
- Status: Planned
- Deliverables: 15+ scripts integrated
- Dependencies: Training complete
```

## Sprint Planning (Optional)

For teams using Agile/Scrum:

### Location
`docs/planning/sprints/sprint-N.md`

### Structure

```markdown
# Sprint N - [Sprint Goal]

**Duration**: 2 weeks (YYYY-MM-DD to YYYY-MM-DD)  
**Team**: [Team members]  
**Goal**: [One sentence sprint goal]

## Sprint Backlog
- [ ] Task 1 (8 story points) - @developer1
- [ ] Task 2 (5 story points) - @developer2

## Definition of Done
- Code reviewed and merged
- Tests passing
- Documentation updated

## Sprint Review
[Completed after sprint ends]
```

## Update Frequency

### Weekly Updates
- Update task status
- Add newly identified work
- Adjust resource allocation
- Update blockers and risks

### Monthly Reviews
- Review success metrics
- Update milestone progress
- Adjust medium-term goals
- Archive completed sprints

### Quarterly Planning
- Review long-term vision
- Update Year 1 roadmap
- Adjust strategic priorities
- Update resource forecasts

## Integration with Root ROADMAP.md

### Linking Strategy

Root ROADMAP.md should link to planning details:

```markdown
### Version 03.03.00 (Planned) - Q1 2026

**Planning Documentation**:
- 📋 [Complete Implementation Roadmap](docs/planning/README.md#short-term-goals-month-1)
- 🎯 [Week 1 Actions](docs/planning/README.md#immediate-actions-week-1)
- 📊 [Success Metrics](docs/planning/README.md#success-metrics)
```

Planning docs should reference versions:

```markdown
## Short-term Goals (Month 1)

**Target Version**: 03.03.00  
**See**: [Root ROADMAP.md](../../ROADMAP.md#version-030300) for version details
```

## Best Practices

### Do's

- ✅ Break work into measurable tasks
- ✅ Estimate effort in hours
- ✅ Assign priorities and owners
- ✅ Update frequently (weekly minimum)
- ✅ Link between tiers (version ↔ implementation)
- ✅ Include integration examples
- ✅ Track metrics and KPIs
- ✅ Document lessons learned

### Don'ts

- ❌ Mix version planning with task details
- ❌ Let planning docs go stale
- ❌ Forget to update status indicators
- ❌ Skip resource allocation
- ❌ Ignore dependencies and blockers
- ❌ Make plans without success criteria
- ❌ Duplicate information between tiers

## Validation

Planning documentation quality checklist:

- [ ] All required sections present
- [ ] Tasks have effort estimates
- [ ] Resources allocated by phase
- [ ] Success metrics defined
- [ ] Links to root ROADMAP.md
- [ ] Phase docs exist for completed work
- [ ] Milestones tracked
- [ ] Update dates current (<1 month old)

## Examples

### Good Example: Specific and Actionable

```markdown
## Week 1: Immediate Actions (40 hours)

### Priority 1: Critical Script Updates (13 hours)

1. **bulk_update_repos.php** (4 hours) - @dev1
   - Add AuditLogger integration
   - Use APIClient with rate limiting
   - Add error recovery with checkpointing
   - Success: Script passes integration tests

2. **auto_create_org_projects.py** (3 hours) - @dev2
   - Add audit logging
   - Use APIClient for GitHub API
   - Add metrics tracking
   - Success: Zero API rate limit errors
```

### Poor Example: Vague and Unmeasurable

```markdown
## Month 1

- Update some scripts
- Deploy monitoring
- Train team
- Improve performance
```

## Relationship to Other Documents

| Document | Focus | Update | Owner |
|----------|-------|--------|-------|
| **ROADMAP.md** | Version planning | Per release | Product |
| **docs/planning/README.md** | Implementation | Weekly | Engineering |
| **CHANGELOG.md** | What changed | Per release | All |
| **Sprint docs** | Sprint execution | Daily/Weekly | Team |

## Template Usage

```bash
# Create new planning structure
mkdir -p docs/planning/{phases,milestones,sprints}

# Copy template
cp templates/docs/extra/template-planning-README.md docs/planning/README.md

# Customize for your project
```

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Policy |
| Domain | Planning & Governance |
| Applies To | All Repositories with docs/planning/ |
| Owner | Engineering Leadership |
| Path | docs/policy/planning-guidance.md |
| Version | 03.02.00 |
| Status | Active |
| Last Reviewed | 2026-02-11 |

## Revision History

| Date | Author | Change | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Engineering Team | Initial creation | Establishes two-tier planning guidance |

---

**For version planning, see**: [ROADMAP.md](../../ROADMAP.md)  
**For policy on roadmaps, see**: [roadmap-standards.md](roadmap-standards.md)  
**For MokoStandards implementation plan, see**: [docs/planning/README.md](../planning/README.md)
