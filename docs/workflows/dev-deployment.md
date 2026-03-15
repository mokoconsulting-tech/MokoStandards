<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/workflows/dev-deployment.md
VERSION: 04.00.15
BRIEF: Guide for the SFTP development server deployment workflow
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Development Server Deployment

Automated SFTP deployment of the `src/` directory to the development server.

## Overview

The `deploy-dev.yml` workflow pushes the contents of `src/` to a development server over **SFTP only** when:

- A commit is pushed to `main`, `master`, `develop`, `dev`, or `development` branches (and `src/**` changed)
- A pull request that targets those branches is **merged**
- Triggered manually via workflow dispatch

**⚠️ Access control:** Only users with **admin** or **maintain** role on the repository may trigger a deployment. All other actors are rejected before any files are transferred.

---

## Configuration

### Organization Variables (required)

Configure at the **organization** level in **Settings → Secrets and variables → Actions → Variables**:

| Variable | Example | Description |
|----------|---------|-------------|
| `DEV_FTP_HOST` | `dev.example.com` | Dev server hostname. May include an explicit port suffix — `dev.example.com:2222`. |
| `DEV_FTP_PATH` | `/var/www/html` | Base remote path where files are deployed. |
| `DEV_FTP_USERNAME` | `deployuser` | SFTP username for authentication. |

### Organization Variable (optional)

| Variable | Example | Description |
|----------|---------|-------------|
| `DEV_FTP_PORT` | `2222` | Explicit port override. See **Port resolution** below. |

### Repository Variable (optional)

| Variable | Example | Description |
|----------|---------|-------------|
| `DEV_FTP_PATH_SUFFIX` | `/my-module` | Appended to `DEV_FTP_PATH`. Useful for deploying multiple repos to the same server. |

### Organization Secrets (credentials)

At least one of the following must be set:

| Secret | Description |
|--------|-------------|
| `DEV_FTP_KEY` | **Preferred.** SSH private key (any format supported by OpenSSH). |
| `DEV_FTP_PASSWORD` | SFTP password. Also used as the key passphrase when set alongside `DEV_FTP_KEY`. |

---

## Authentication logic

The workflow determines the connection method at runtime:

| Secrets present | Behaviour |
|-----------------|-----------|
| `DEV_FTP_KEY` + `DEV_FTP_PASSWORD` | Key auth with `DEV_FTP_PASSWORD` as the key passphrase. If key auth fails, retries with `DEV_FTP_PASSWORD` alone as an SFTP password. |
| `DEV_FTP_KEY` only | Key auth (no passphrase). Fails hard on auth error — no password fallback. |
| `DEV_FTP_PASSWORD` only | Password auth directly. |
| Neither | Workflow fails with an error message. |

---

## Port resolution

The SFTP port is determined in the following order — the first match wins:

1. **`DEV_FTP_PORT` variable** — explicit override, highest priority.
2. **Port suffix in `DEV_FTP_HOST`** — if the host value contains `:`, the suffix is extracted and the bare hostname is used (e.g. `dev.example.com:2222` → host `dev.example.com`, port `2222`).
3. **Default** — port **22** is assumed when neither of the above is present.

---

## Remote path

The final remote path is constructed as:

```
DEV_FTP_PATH [+ "/" + DEV_FTP_PATH_SUFFIX]
```

`DEV_FTP_PATH_SUFFIX` is optional. When set, exactly one `/` is inserted between the base and the suffix regardless of trailing/leading slashes in the values.

---

## Manual dispatch

1. Go to **Actions → Deploy to Dev Server (SFTP)**.
2. Click **Run workflow**.
3. Optionally override the source directory (default: `src`) or enable **Dry run** to list files without uploading.

---

## Repository health checks

The `check_repo_health.php` script scores deployment readiness as part of the overall health report. When `--repo owner/repo` is supplied, it also calls the GitHub API to verify secrets and variables are configured.

### Deployment category checks

| Check | Points | Requires `--repo` |
|-------|--------|------------------|
| `deploy-dev.yml` workflow exists | 5 | No |
| `DEV_FTP_HOST` variable configured | 3 | Yes |
| `DEV_FTP_PATH` variable configured | 3 | Yes |
| `DEV_FTP_USERNAME` variable configured | 2 | Yes |
| SFTP credentials configured (`DEV_FTP_KEY` or `DEV_FTP_PASSWORD`) | 2 | Yes |

Variables and secrets are checked at both the **org level** and **repo level** — a check passes if the item exists at either scope.

---

## Examples

### Example 1 — SSH key with passphrase, custom port

**Org variables:**
```
DEV_FTP_HOST     = dev.example.com
DEV_FTP_PORT     = 2222
DEV_FTP_PATH     = /var/www/html
DEV_FTP_USERNAME = deployuser
```

**Org secrets:**
```
DEV_FTP_KEY      = <passphrase-protected SSH private key>
DEV_FTP_PASSWORD = mysecretphrase
```

**Behaviour:** Key loaded with `mysecretphrase` as passphrase. If key auth fails, retries with `mysecretphrase` as the SFTP password.

---

### Example 2 — SSH key, port embedded in host

**Org variables:**
```
DEV_FTP_HOST     = dev.example.com:2222
DEV_FTP_PATH     = /var/www/html
DEV_FTP_USERNAME = deployuser
```

**Org secret:**
```
DEV_FTP_KEY = <unprotected SSH private key>
```

**Behaviour:** Port `2222` extracted from host. Key used without passphrase; no password fallback.

---

### Example 3 — Password only, default port

**Org variables:**
```
DEV_FTP_HOST     = dev.example.com
DEV_FTP_PATH     = /var/www/html
DEV_FTP_USERNAME = deployuser
```

**Org secret:**
```
DEV_FTP_PASSWORD = secretpass
```

**Behaviour:** Port defaults to 22. Connects with password directly.

---

### Example 4 — Multiple repos, same server

Each repo sets its own `DEV_FTP_PATH_SUFFIX`:

| Repo | Suffix | Deploys to |
|------|--------|------------|
| `project-a` | `/project-a` | `/var/www/html/project-a` |
| `project-b` | `/project-b` | `/var/www/html/project-b` |

---

## Troubleshooting

### Permission denied

```
❌ Deployment requires admin or maintain role.
```

Only org/repo administrators and maintainers may deploy. Contact your org administrator.

### No credentials configured

```
❌ No SFTP credentials configured.
   Set DEV_FTP_KEY (preferred) or DEV_FTP_PASSWORD as an org-level secret.
```

Set at least one of `DEV_FTP_KEY` or `DEV_FTP_PASSWORD` in **Org Settings → Secrets**.

### Key authentication failed, no fallback

```
RuntimeError: Key authentication failed and no password fallback is available: ...
```

The SSH private key was rejected and `DEV_FTP_PASSWORD` is not set. Check the key is correct and authorized on the server, or add `DEV_FTP_PASSWORD` as a fallback.

### Missing source directory

```
⚠️ Source directory 'src' not found — skipping deployment
```

Expected behaviour for repos without a `src/` directory. No files are uploaded; the workflow exits successfully.

### Connection refused

```
[Errno 111] Connection refused
```

- Verify `DEV_FTP_HOST` is correct.
- Check the resolved port (shown in the **Resolve SFTP host and port** step log).
- Confirm the server firewall allows inbound SFTP on that port.

---

## Related documentation

- [Workflow inventory](./workflow-inventory.md)
- [Bulk repository sync](./bulk-repo-sync.md)
- [MokoStandards repo-sync guide](../guide/repo-sync.md)
- [Workflow template source](../../templates/workflows/shared/deploy-dev.yml.template)

---

## Metadata

| Field         | Value                                                       |
|---------------|-------------------------------------------------------------|
| Document Type | Guide                                                       |
| Domain        | Operations                                                  |
| Applies To    | All Repositories                                            |
| Jurisdiction  | Tennessee, USA                                              |
| Owner         | Moko Consulting                                             |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards        |
| Path          | /docs/workflows/dev-deployment.md                           |
| Version       | 04.00.04                                                    |
| Status        | Active                                                      |
| Last Reviewed | 2026-03-12                                                  |
| Reviewed By   | Documentation Team                                          |

## Revision History

| Date       | Author          | Change                                                               |
|------------|-----------------|----------------------------------------------------------------------|
| 2026-03-12 | Moko Consulting | Rewrote for SFTP-only workflow; added auth fallback, port resolution, health check docs |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history                           |
| 2026-01-17 | Moko Consulting | Initial dev deployment workflow documentation                        |
