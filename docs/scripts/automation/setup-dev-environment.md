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
INGROUP: WorkstationProvisioning
REPO: https://github.com/mokoconsulting-tech/
FILE: dev-workstation-provisioner.md
VERSION: 04.00.01
BRIEF: Operational guide for provisioning a Windows development workstation with Winget and optional WSL Ubuntu integration.
PATH: /docs/scripts/automation/dev-workstation-provisioner.md
NOTE:
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Dev Workstation Provisioner Guide

## Purpose

This document defines the operational procedure for provisioning a standardized Windows-based development workstation using a controlled PowerShell bootstrapper. The provisioner coordinates unattended package installation via Winget, scheduled maintenance automation, and optional Windows Subsystem for Linux (WSL) provisioning with Ubuntu.

The goal is repeatable workstation setup with explicit operator consent, auditability, and minimal configuration drift.

## Scope

This guide applies to:

* Windows 10 and Windows 11 development workstations.
* Local developer machines and consultant-managed endpoints.
* Environments requiring pinned runtime versions for Python and PHP.

The provisioner supports:

* GUI-driven configuration and confirmation gates.
* Unattended Winget installs with package exclusions.
* Monthly scheduled update tasks.
* Optional WSL Ubuntu provisioning with PHP tooling.
* Explicit non-interference with existing WSL installations unless approved.

## Roles and responsibilities

* Operator: Executes the provisioner and selects configuration options.
* Approver: Authorizes WSL reset or first-time WSL installation when required.
* Auditor: Reviews scheduled task configuration and script artifacts.

## Prerequisites

### Host system

* Windows 10 or Windows 11.
* Winget installed and functional.
* PowerShell 5.1 or PowerShell 7+.
* Administrative privileges for scheduled task creation and optional WSL setup.

### Optional WSL provisioning

* Hardware virtualization enabled in BIOS.
* Windows features available for WSL and Virtual Machine Platform.

## Provisioning model

### Safety and governance defaults

* Python is pinned to version 3.10 and excluded from automated upgrades.
* PHP is excluded from automated Winget upgrades.
* WSL is never modified without explicit user confirmation.
* Reset operations are opt-in and gated by warning dialogs.

### Workspace folder

The provisioner prompts for a default Workspace directory. This directory is used to store:

* `winget-monthly-update.cmd`
* Future operational artifacts related to workstation maintenance

A suggested default of `~/Documents/Workspace` is provided but may be overridden.

## Monthly maintenance automation

### Winget update script

The provisioner generates a monthly maintenance script with the following characteristics:

* Runs `winget upgrade --all` unattended.
* Explicitly excludes:

	* `Python.Python.3.10`
	* `PHP.PHP`
* Writes execution logs to `C:\Logs\Winget`.
* Generates date-stamped log files for audit review.

### Scheduled task

A Windows Scheduled Task is created or replaced with the following properties:

* Schedule: Monthly.
* Privilege level: Highest.
* Execution context: `cmd.exe` invoking the generated script.
* Idempotent creation to avoid duplicate tasks.

## WSL integration model

### Detection logic

The provisioner evaluates WSL state before taking any action:

* Missing: WSL not available on the system.
* Not installed: WSL available but no distributions present.
* Installed: One or more WSL distributions detected.

### Consent gates

Based on detected state, the operator is prompted:

* Install WSL with Ubuntu if no distribution exists.
* Reset Ubuntu if an existing WSL installation is detected.
* Skip all WSL actions if declined.

No WSL features or distributions are modified without affirmative user action.

### Ubuntu provisioning

When approved, the provisioner installs and configures Ubuntu with:

* PHP 8.3 CLI and core modules.
* Common extensions required for CMS and application development.
* Module enablement using native `phpenmod` tooling.

Manual `php.ini` modification is intentionally avoided to align with Debian and Ubuntu packaging standards.

## Execution

### Standard run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Scripts\DevBootstrap-Winget-WSL.ps1
```

### Verbose mode

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Scripts\DevBootstrap-Winget-WSL.ps1 -VerboseMode
```

Verbose mode emits operational messages to the console while preserving unattended behavior.

## Output artifacts

* Workspace folder containing `winget-monthly-update.cmd`.
* Windows Scheduled Task visible under Task Scheduler.
* Winget execution logs under `C:\Logs\Winget`.
* Optional Ubuntu environment with configured PHP tooling.

## Change control considerations

Recommended operational sequence:

1. Review script version and contents.
2. Execute provisioner in verbose mode for initial rollout.
3. Validate scheduled task configuration.
4. Confirm Winget exclusions are in effect.
5. Approve or decline WSL actions explicitly.

## Risk indicators

* Approval of WSL reset on a machine with active development data.
* Execution without administrative privileges.
* Modification of Workspace path to a shared or synchronized directory.

## Maintenance and lifecycle

* Script updates should increment the FILE INFORMATION version.
* Changes to package lists or exclusions should be documented.
* WSL provisioning logic should be reviewed when Ubuntu LTS versions change.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Development                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/scripts/automation/dev-workstation-provisioner.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
