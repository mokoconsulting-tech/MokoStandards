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
INGROUP: MokoStandards.Security
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/network-egress.md
VERSION: 04.00.15
BRIEF: Policy governing outbound network access from CI/CD runners and development workstations
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Network Egress Policy

## Purpose

This policy defines which external domains and services Moko Consulting CI/CD runners, AI coding tools, and development workstations are permitted to access, and establishes the process for requesting new domain approvals.

## Scope

This policy applies to:

- GitHub Actions workflow runners executing in MokoStandards-governed repositories
- GitHub Copilot and other AI coding tools operating in governed repositories (via `copilot.yml`)
- Enterprise firewall rules protecting outbound internet access from development infrastructure
- Any automated process (scripts, bots, agents) that makes outbound network requests on behalf of a governed repository

## Authoritative Source

The approved domain allow-list is maintained in two places. Both must be kept in sync:

| File | Purpose |
|---|---|
| `.github/copilot.yml` | Restricts domains that GitHub Copilot may access. Synced to all governed repos via bulk sync. |
| `docs/guide/operations/enterprise-firewall-configuration.md` | Firewall rule reference for enterprise network administrators. |

The `templates/workflows/shared/enterprise-firewall-setup.yml.template` contains the same list in machine-readable form (shell and Python) for automated firewall rule generation.

## Approved Domain Groups

### License Providers

Required for GPL compliance verification and license text validation.

| Domain | Purpose |
|---|---|
| `www.gnu.org` | GNU licenses (GPL, LGPL, AGPL) |
| `opensource.org` | Open Source Initiative |
| `choosealicense.com` | GitHub license chooser |
| `spdx.org` | SPDX identifier registry |
| `creativecommons.org` | Creative Commons licenses |
| `apache.org` | Apache Software Foundation |
| `fsf.org` | Free Software Foundation |

### Documentation and Standards

| Domain | Purpose |
|---|---|
| `semver.org` | Semantic Versioning specification |
| `keepachangelog.com` | Changelog standards |
| `conventionalcommits.org` | Commit message standards |
| `json-schema.org` | JSON Schema specification |
| `w3.org` | W3C standards |
| `ietf.org` | IETF RFCs |

### GitHub and Related

| Domain | Purpose |
|---|---|
| `github.com` | GitHub platform |
| `api.github.com` | GitHub REST API |
| `docs.github.com` | GitHub documentation |
| `raw.githubusercontent.com` | Raw file access |
| `upload.github.com` | Release asset uploads |
| `objects.githubusercontent.com` | Release assets and Git LFS |
| `user-images.githubusercontent.com` | Issue and PR image attachments |
| `codeload.github.com` | Archive downloads |
| `ghcr.io` | GitHub Container Registry |
| `pkg.github.com` | GitHub Packages |

### Package Registries

| Domain | Purpose |
|---|---|
| `npmjs.com` | npm registry |
| `registry.npmjs.org` | npm package downloads |
| `pypi.org` | Python Package Index |
| `files.pythonhosted.org` | Python package downloads |
| `packagist.org` | Composer package registry |
| `repo.packagist.org` | Composer downloads |
| `rubygems.org` | Ruby gems |

### Platform-Specific

| Domain | Purpose |
|---|---|
| `joomla.org` | Joomla CMS |
| `downloads.joomla.org` | Joomla downloads |
| `docs.joomla.org` | Joomla documentation |
| `php.net` | PHP documentation |
| `getcomposer.org` | Composer dependency manager |
| `dolibarr.org` | Dolibarr ERP/CRM |
| `wiki.dolibarr.org` | Dolibarr wiki |
| `docs.dolibarr.org` | Dolibarr developer docs |

### Moko Consulting

| Domain | Purpose |
|---|---|
| `mokoconsulting.tech` | Moko Consulting main site |
| `*.mokoconsulting.tech` | All Moko Consulting subdomains (API, docs, CDN, internal services) |

### Google Services

Required for Google Drive file sharing, document collaboration, font hosting, and asset delivery used in client deliverables.

| Domain | Purpose |
|---|---|
| `drive.google.com` | Google Drive file sharing |
| `docs.google.com` | Google Docs |
| `sheets.google.com` | Google Sheets |
| `accounts.google.com` | Google authentication |
| `storage.googleapis.com` | Google Cloud Storage |
| `*.googleapis.com` | Google APIs |
| `*.googleusercontent.com` | Google user content CDN |
| `fonts.googleapis.com` | Google Fonts CSS |
| `fonts.gstatic.com` | Google Fonts static assets |

### Developer Reference

| Domain | Purpose |
|---|---|
| `developer.mozilla.org` | MDN Web Docs |
| `stackoverflow.com` | Stack Overflow |
| `git-scm.com` | Git documentation |

### CDN and Infrastructure

| Domain | Purpose |
|---|---|
| `cdn.jsdelivr.net` | jsDelivr CDN |
| `unpkg.com` | unpkg CDN |
| `cdnjs.cloudflare.com` | Cloudflare CDN |
| `img.shields.io` | Shields.io badge images |
| `shields.io` | Shields.io badge service |

### Container Registries

| Domain | Purpose |
|---|---|
| `hub.docker.com` | Docker Hub |
| `registry-1.docker.io` | Docker registry |
| `index.docker.io` | Docker index |

### CI and Code Quality

| Domain | Purpose |
|---|---|
| `codecov.io` | Code coverage reporting |
| `coveralls.io` | Coverage service |
| `sonarcloud.io` | Static analysis |

### Terraform and Infrastructure

| Domain | Purpose |
|---|---|
| `registry.terraform.io` | Terraform provider registry |
| `releases.hashicorp.com` | HashiCorp release downloads |
| `checkpoint-api.hashicorp.com` | HashiCorp update checks |

## Requesting a New Domain

To add a domain to the allow-list:

1. **Open an issue** in the MokoStandards repository using the feature request template. Include:
   - The domain(s) to be added
   - The business justification
   - Which workflows or tools require access
   - Whether wildcard (`*.example.com`) or exact-domain access is needed

2. **Security review**: The domain will be assessed for:
   - Reputation (known-malicious, phishing, or data-exfiltration risk)
   - Data-in-transit controls (HTTPS required)
   - Necessity (is there an already-approved equivalent?)

3. **Approval**: Domains are approved by the repository owner. Wildcard domains require additional justification.

4. **Implementation**: Once approved, add the domain to **all three** of:
   - `.github/copilot.yml` (`allowed_domains` list)
   - `docs/guide/operations/enterprise-firewall-configuration.md` (domain table)
   - `templates/workflows/shared/enterprise-firewall-setup.yml.template` (both the shell heredoc and the Python `TRUSTED_DOMAINS` dict)

5. **Sync**: The updated `copilot.yml` is pushed to all governed repos on the next bulk sync run.

## Removing a Domain

Domains should be removed when:

- The service is no longer used by any workflow or tool
- The domain becomes associated with security risks
- A migration to an alternative service is complete

Follow the same process as adding — open an issue, get approval, update all three files, and sync.

## Enforcement

### GitHub Copilot

GitHub Copilot enforces the `allowed_domains` list in `.github/copilot.yml` natively. Requests to domains not on the list are blocked at the Copilot layer.

### CI Runners

GitHub Actions runners are ephemeral and run in GitHub's infrastructure, which has its own network policies. The `enterprise-firewall-setup.yml` workflow documents which domains are accessed and validates connectivity, but does not enforce blocking at the runner layer.

### Enterprise Workstations

For on-premise or VPN-connected development environments, apply the rules in `enterprise-firewall-configuration.md` using the appropriate firewall tool for your infrastructure (iptables, UFW, firewalld, AWS Security Groups, etc.). The `enterprise-firewall-setup.yml` workflow can generate configuration snippets on demand.

## Related Documentation

| Document | Purpose |
|---|---|
| [docs/guide/operations/enterprise-firewall-configuration.md](../guide/operations/enterprise-firewall-configuration.md) | Firewall rule reference and implementation examples |
| [templates/workflows/shared/enterprise-firewall-setup.yml.template](../../templates/workflows/shared/enterprise-firewall-setup.yml.template) | Automated firewall rule generator |
| [`.github/copilot.yml`](../../.github/copilot.yml) | GitHub Copilot domain allow-list |
| [ai-tool-governance.md](ai-tool-governance.md) | AI tool governance policy |
| [security-scanning.md](security-scanning.md) | Security scanning policy |

## Metadata

| Field         | Value |
| ------------- | ----- |
| Document Type | Policy |
| Domain        | Security |
| Applies To    | All Repositories |
| Jurisdiction  | Tennessee, USA |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/ |
| Path          | /docs/policy/network-egress.md |
| Version       | 04.00.04 |
| Status        | Active |
| Last Reviewed | 2026-03-08 |
| Reviewed By   | Documentation Team |

## Revision History

| Date       | Author          | Change  | Notes |
| ---------- | --------------- | ------- | ----- |
| 2026-03-08 | Moko Consulting | Created | Initial network egress and domain allow-list policy |
