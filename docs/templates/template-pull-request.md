<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation; either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
	REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  pull-request.md
 VERSION:  2.0
 BRIEF:  Pull Request Template
 PATH:  ./docs/templates/pull-request.md
 -->

# Pull Request Template

.GitHub: Pull Request issue template → [./.github/PULL_REQUEST_TEMPLATE.md](./docs/templates/pull-request.md)

## Purpose

Explain the objective of this change and the problem it addresses.

## Change Summary

Provide a concise overview of the modifications introduced.

## Testing Evidence

Document tests performed, results, and validation steps.

## Risk and Rollback

Describe potential risks and outline the rollback strategy.

## Checklist

* Code aligns with project standards
* Documentation updated if needed
* Tests added or updated
* Dependencies reviewed
* Security considerations evaluated

## Reviewer Notes

Add any context or guidance to assist reviewers.

## Review and Approval

List reviewers, approvers, and approval date.

## Example

```text
### Summary
This update introduces improvements to API response validation.

### Changes
- Added new validation layer
- Updated unit tests
- Improved error handling

### How to test
1. Run test suite
2. Verify endpoint responses in staging
3. Validate error logs remain clean

### Checklist
- [ ] Follows Conventional Commits
- [ ] Tests added/updated
- [ ] Docs updated
- [ ] License header present
- [ ] Linked issue(s): Closes #123

### Review and Approval
Engineering Lead, QA Lead
```

## Metadata

```
Owner: Documentation Lead
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub |
