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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.ADR
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/adr/template.md
VERSION: 03.01.01
BRIEF: Template for creating Architecture Decision Records
-->

# ADR-NNNN: [Short Title of Decision]

## Status

**[Proposed | Accepted | Deprecated | Superseded]**

- Date Proposed: YYYY-MM-DD
- Date Decided: YYYY-MM-DD
- Decision Maker(s): [Names or roles]
- Supersedes: [ADR-XXXX] (if applicable)
- Superseded by: [ADR-YYYY] (if applicable)

## Context

### Problem Statement

Describe the architectural problem or decision that needs to be made. Include:

- What challenge or opportunity prompted this decision?
- What are the business or technical drivers?
- What constraints or requirements must be satisfied?

### Current Situation

Describe the current state:

- How is this currently handled (if at all)?
- What pain points or limitations exist?
- What triggered the need for a decision?

### Goals and Requirements

List the key goals and requirements:

- **Functional Requirements**: What must the solution accomplish?
- **Non-Functional Requirements**: Performance, security, scalability, maintainability, etc.
- **Constraints**: Budget, timeline, technology, organizational, regulatory, etc.

## Decision

### Selected Approach

Clearly state the decision made:

**We will [decision statement].**

Example: "We will adopt Python as the primary language for all automation scripts."

### Rationale

Explain why this decision was made:

- What factors led to this choice?
- How does it address the problem statement?
- What principles or values does it align with?
- What evidence or research supports this decision?

## Alternatives Considered

Document the alternatives that were evaluated and why they were not chosen:

### Alternative 1: [Name]

**Description**: Brief description of the alternative

**Pros**:
- Advantage 1
- Advantage 2

**Cons**:
- Disadvantage 1
- Disadvantage 2

**Reason Not Chosen**: Specific reason(s) why this alternative was rejected

### Alternative 2: [Name]

[Same structure as Alternative 1]

### Alternative 3: Do Nothing

**Description**: Maintain the status quo

**Pros**: [Benefits of maintaining current state]

**Cons**: [Costs of not addressing the problem]

**Reason Not Chosen**: [Why the status quo is insufficient]

## Consequences

### Positive Consequences

List the expected benefits:

- **Benefit 1**: Description and impact
- **Benefit 2**: Description and impact
- **Benefit 3**: Description and impact

### Negative Consequences

List the expected drawbacks or costs:

- **Tradeoff 1**: What we're giving up or accepting
- **Tradeoff 2**: Additional complexity or constraints
- **Tradeoff 3**: Migration costs or technical debt

### Risks and Mitigations

Identify potential risks and how they will be addressed:

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Risk description | High/Medium/Low | High/Medium/Low | Mitigation strategy |

## Implementation

### Action Items

List concrete steps required to implement this decision:

- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

### Timeline

- **Start Date**: YYYY-MM-DD
- **Target Completion**: YYYY-MM-DD
- **Key Milestones**: Important checkpoints

### Success Criteria

How will we know this decision was successful?

- **Metric 1**: Measurable outcome
- **Metric 2**: Measurable outcome
- **Metric 3**: Measurable outcome

### Rollback Plan

If this decision needs to be reversed:

- What are the conditions for rollback?
- What steps are required to revert?
- What is the cost of reverting?

## Related Decisions

Links to related ADRs:

- Depends on: [ADR-XXXX]
- Related to: [ADR-YYYY]
- Conflicts with: [ADR-ZZZZ] (resolved by...)

## References

Links to supporting documents, research, or discussions:

- [Link to discussion thread]
- [Link to research document]
- [Link to external resource]
- [Link to related policy]

## Notes

Additional information, context, or commentary:

- Lessons learned during implementation
- Feedback from early adopters
- Adjustments made after initial rollout
- Future considerations

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | ADR                                       |
| Domain         | Architecture                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/adr/template.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
