<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of
 the GNU General Public License as published by the Free Software Foundation; either version 3
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE).

 FILE INFORMATION
 DEFGROUP: {{org}}.{{repo_name}}
 INGROUP: MokoStandards.Governance
 REPO: https://github.com/{{org}}/{{repo_name}}
 VERSION: {{standards_version}}
 PATH: /GOVERNANCE.md
 BRIEF: Project governance rules, roles, and decision process for {{repo_name}}
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-{{standards_version}}-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Project Governance

## Overview

This document defines the governance model for the `{{repo_name}}` repository within the
`{{org}}` organization. It is automatically maintained by
[MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) v{{standards_version}}.

Full governance policy is defined in the MokoStandards source repository:
[docs/policy/GOVERNANCE.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/GOVERNANCE.md)

---

## Roles and Responsibilities

### Maintainer

**GitHub**: @mokoconsulting-tech

**Authority**: Final decision-making authority on all matters for this repository.

**Responsibilities**:
- Review and merge pull requests
- Maintain code quality and standards compliance
- Manage releases and versioning
- Respond to issues and security reports

### Contributors

**Authority**: Submit changes via pull requests.

**Requirements**:
- Read and accept `CODE_OF_CONDUCT.md`
- Follow `CONTRIBUTING.md` guidelines

---

## Decision-Making

All changes must be submitted as pull requests. The maintainer (@mokoconsulting-tech)
reviews and approves all changes before they are merged.

### Sole Operator Policy

This organization operates under a **sole operator** model. The maintainer (@mokoconsulting-tech)
is the sole employee and owner and may self-approve pull requests when no second reviewer is
available. The following requirements remain mandatory regardless:

1. **Pull Requests Required** — all changes to protected branches go through a PR.
2. **Automated Checks** — all CI checks must pass before merging.
3. **Audit Trail** — issues, pull requests, and commit history are preserved.
4. **Documentation** — changes are documented in `CHANGELOG.md`.

See the full policy:
[Sole Operator Policy](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/GOVERNANCE.md#sole-operator-policy)

---

## Change Management

| Change Type | Approval | Process |
|-------------|----------|---------|
| Routine (docs, bug fixes) | Maintainer | PR → CI pass → merge |
| Significant (new features) | Maintainer | PR with description → CI pass → merge |
| Major (breaking, architecture) | Maintainer | Issue discussion → PR → CI pass → merge |
| Emergency (security) | Maintainer | Labelled `EMERGENCY` → immediate merge → post-mortem |

---

## Reporting Issues

- **Bugs / Features**: Open a [GitHub Issue](https://github.com/{{org}}/{{repo_name}}/issues)
- **Security vulnerabilities**: See [SECURITY.md](./SECURITY.md)
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- **Contact**: dev@mokoconsulting.tech

---

## Metadata

| Field         | Value                                           |
| ------------- | ----------------------------------------------- |
| Document Type | Policy                                          |
| Domain        | Governance                                      |
| Applies To    | {{org}}/{{repo_name}}                           |
| Jurisdiction  | Tennessee, USA                                  |
| Maintainer    | @mokoconsulting-tech                            |
| Standards     | MokoStandards v{{standards_version}}            |
| Repo          | https://github.com/{{org}}/{{repo_name}}        |
| Path          | /GOVERNANCE.md                                  |
| Status        | Active — auto-maintained by MokoStandards       |
