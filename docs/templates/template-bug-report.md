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
 FILE:  bug-report.md
 VERSION:  2.0
 BRIEF:  Bug Report Template
 PATH:  ./docs/templates/bug-report.md
 -->

# Bug Report Template

.GitHub: Bug Report issue template → [./.github/ISSUE_TEMPLATE/bug_report.md](file-6VwUu35kv6oSymh43SKkjn)

## Summary

Provide a concise description of the bug and its impact.

## Environment

Specify the environment where the bug occurs:

* Application version
* Browser / OS
* Device
* Configuration details

## Steps to Reproduce

Provide clear, sequential steps.
1.
2.
3.

## Expected Behavior

Describe what should have happened.

## Actual Behavior

Describe what actually happened.

## Logs / Screenshots

Attach logs, stack traces, screenshots, or recordings.

## Severity & Impact

Define severity level and describe affected workflows.

## Related Incidents or Tickets

Link associated incident reports, PRs, or issues.

## Review and Approval

List reviewers, approvers, and date.

## Example

```text
### Summary
User profile page crashes when loading.

### Environment
- App Version: 2.1.4
- Browser: Chrome 120
- OS: Windows 11

### Steps to Reproduce
1. Log in
2. Navigate to /profile
3. Page crashes with error

### Expected Behavior
Profile page loads successfully.

### Actual Behavior
White screen with console error: "TypeError: undefined is not a function".

### Logs
See attached screenshot and browser console output.

### Severity & Impact
Severity: High
Impact: Blocks all users from accessing profile settings.

### Related Incidents or Tickets
- INC-0042 User profile outage

### Review and Approval
QA Lead, Engineering Manager
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
