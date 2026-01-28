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
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: Scripts.Utility
INGROUP: FileDistribution
REPO: https://github.com/mokoconsulting-tech/
FILE: guide-file-distributor.md
VERSION: 02.00.00
BRIEF: Operational guide for distributing a file across folder trees with PowerShell and Python utilities.
PATH: /docs/scripts/automation/guide-file-distributor.md
NOTE:
-->

# File Distributor Utility Guide

## Purpose

This guide defines the operational procedure for distributing a single source file into a controlled set of target folders under a root directory. The utility is designed for enterprise execution with change control support, audit logging, and user-confirmation gates.

## Scope

This guide covers two coordinating implementations:

* PowerShell WinForms utility for Windows-first operations.
* Python Tkinter utility for cross-environment operations where Python is approved.

Both implementations support:

* Dry Run execution for preflight validation.
* Overwrite governance.
* Depth-based traversal control, including full recursion.
* Per-folder confirmation gates with "Yes to All" option.
* Hidden folder inclusion control.
* Audit log export to CSV and JSON.

## Roles and responsibilities

* Operator: Executes the tool, validates scope, reviews audit outputs.
* Approver: Confirms overwrite usage and full recursion usage when governed.
* Auditor: Reviews logs and validates change intent and outcomes.

## Prerequisites

### PowerShell utility

* Windows PowerShell 5.1 or PowerShell 7+.
* WinForms support available on the host.
* File system permissions for the root directory and all target folders.

### Python utility

* Python 3.10+ recommended.
* Tkinter available (typically included with standard Python on Windows).
* File system permissions for the root directory and all target folders.

## Operational controls

### Safety defaults

* Dry Run should be enabled by default for initial execution.
* Overwrite should be disabled unless explicitly approved.
* Depth should be minimized to the required scope.
* Hidden folder inclusion should be evaluated based on use case and security requirements.

### Depth model

Depth defines the maximum folder levels under the selected root.

* Depth 0: Root folder only.
* Depth 1: Root folder plus immediate subfolders.
* Depth N: Root folder plus N levels.
* Depth -1: Full recursion (entire directory tree).

### Per-folder confirmation

When enabled, the tool will prompt for each folder.

* Yes: execute for this folder.
* No: skip this folder.
* Yes to All: execute for all remaining folders without additional prompts.
* Cancel: terminate execution.

### Hidden folder control

Both utilities provide control over whether hidden folders are included in the distribution scope.

* **Default behavior:** Hidden folders are included by default for maximum reach.
* **PowerShell:** Uses the `-Force` flag with `Get-ChildItem` when hidden folders are enabled.
* **Python:** Filters folders starting with `.` (Unix/Linux/macOS) and folders with the hidden file attribute (Windows).
* **Governance note:** Operators should evaluate whether hidden folders (e.g., `.git`, `.vscode`, system folders) should be included based on operational requirements.

## Deployment and placement

Recommended repository structure for operational artifacts:

* `/scripts/automation/file-distributor.ps1`
* `/scripts/automation/file-distributor.py`
* `/docs/scripts/automation/guide-file-distributor.md`

## PowerShell execution

### Launch

Run from an elevated or standard session based on required permissions.

```powershell
# Example: run directly
powershell -ExecutionPolicy Bypass -File .\file-distributor.ps1

# Example: PowerShell 7
pwsh -File .\file-distributor.ps1
```

### UI workflow

1. Select the source file.
2. Select the root folder.
3. Configure options:

	* Dry run
	* Overwrite
	* Confirm each folder
	* Include hidden folders
	* Depth
	* Audit log folder
4. Execute and review the completion summary.

### Output artifacts

* CSV audit log file
* JSON audit log file

The completion dialog provides the absolute paths for both audit outputs.

## Python execution

### Launch

Recommended pattern is to run within an approved virtual environment.

```bash
# Windows PowerShell
python .\file_distributor.py

# Bash
python3 ./file_distributor.py
```

### UI workflow

1. Select the source file.
2. Select the root folder.
3. Configure options:

	* Dry run
	* Overwrite
	* Confirm each folder
	* Include hidden folders
	* Depth
	* Audit log folder
4. Execute and review the completion summary.

### Output artifacts

* CSV audit log file
* JSON audit log file

## Audit logging specification

### Record model

Each action results in a record with the following governance attributes:

* RunId and timestamp for traceability.
* Folder and target path.
* Action planned vs action taken.
* Decision source (auto vs user prompt outcome).
* Policy controls in effect (dry run, overwrite, depth).
* Source file metadata (size, SHA-256 hash).
* Result and error field.

### Recommended storage

Store logs in a controlled directory with retention policy alignment, for example:

* `~/Documents/FileDistributorLogs/`
* A centralized IT-managed share with access control.

## Change control alignment

### Recommended preflight procedure

1. Execute Dry Run.
2. Review console output for unexpected paths.
3. Validate target folder count vs expectation.
4. Confirm overwrite and full recursion usage with approver if applicable.
5. Execute production run.
6. Archive audit logs alongside the change ticket.

### High-risk indicators

* Depth set to -1.
* Overwrite enabled.
* Root directory is a repository root with build artifacts and vendor folders.
* Root directory contains system paths or profile directories.

## Troubleshooting

### GUI does not open

* PowerShell: confirm WinForms is available and session is running on Windows.
* Python: confirm Tkinter is installed and not blocked by the environment.

### Permission denied errors

* Validate that the operator has write permissions in all target folders.
* Validate that the root does not include protected system directories.

### Unexpected folder count

* Confirm depth configuration.
* Confirm the root folder selection.
* Confirm that hidden folders are included or excluded as required by governance.

### Logs not created

* Confirm the selected log folder is writable.
* Confirm storage device has adequate capacity.

## Security and compliance considerations

* Treat the source file as a controlled artifact if it contains credentials, license keys, or operational secrets.
* Use a secrets scanning control upstream of distribution where applicable.
* Store audit logs in a restricted location.
* Do not distribute executable content into untrusted directories.

## Maintenance and lifecycle

* Version changes should be tracked through repository change management.
* Audit schema changes should be communicated to stakeholders.
* Validate the utility against a test directory tree prior to production releases.

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Development                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/scripts/automation/guide-file-distributor.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
