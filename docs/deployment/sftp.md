<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Deployment
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/deployment/sftp.md
VERSION: 04.00.15
BRIEF: SFTP deployment guide for MokoStandards PHP-based deploy script
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# SFTP Deployment Guide

**Version**: 04.00.15 | **Status**: Active | **Last Updated**: 2026-03-15

## Table of Contents

- [Overview](#overview)
- [Important Constraints](#important-constraints)
- [Authentication Policy](#authentication-policy)
- [Local Configuration](#local-configuration)
- [GitHub Secrets and Variables](#github-secrets-and-variables)
- [Workflow Integration](#workflow-integration)
- [Path Resolution](#path-resolution)
- [SSH Key Setup](#ssh-key-setup)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

SFTP deployment in MokoStandards is handled exclusively by `api/deploy/deploy-sftp.php`, a PHP script using **phpseclib3** for all SFTP operations. There are no shell scripts, `lftp` commands, or Python-based deployment utilities.

The script reads connection settings from a **gitignored local config file** (`scripts/sftp-config/sftp-config.json`) when running locally, and from **GitHub Secrets/Variables** when running in CI/CD workflows.

### What the Deploy Script Does

1. Reads `sftp-config.json` (local) or environment variables (CI)
2. Connects to the target server via SFTP using SSH key authentication
3. Computes the final path: `BASE_PATH + PATH_SUFFIX`
4. Uploads the release ZIP package to the target directory

---

## Important Constraints

> **SFTP is used ONLY for uploading release build ZIP packages.**

**SFTP is NOT used for**:
- Live/production website deployment
- Source code synchronization
- Direct file editing on servers
- Database migrations

**SFTP IS used for**:
- Uploading extension release packages (`.zip` files)
- Distributing module builds to update/download servers
- Publishing versioned artifacts to distribution locations

---

## Authentication Policy

> **Password-only SFTP authentication is NOT permitted.**

All SFTP connections **must use SSH key authentication**. An optional passphrase may protect the key (stored separately as `KEY_PASSPHRASE`), but a bare password login is explicitly prohibited.

**Supported key formats**:
- OpenSSH PEM (`-----BEGIN OPENSSH PRIVATE KEY-----`)
- PuTTY PPK (phpseclib3 handles conversion automatically)

**Not supported**:
- Password-only authentication
- Interactive keyboard-interactive auth

---

## Local Configuration

For local development and manual deployments, the deploy script reads from a **gitignored config file**.

### Directory Layout

```
scripts/
├── sftp-config/
│   └── sftp-config.json        # gitignored — local connection config
└── keys/
    ├── deploy_dev.pem           # gitignored — SSH private key (DEV)
    └── deploy_rs.pem            # gitignored — SSH private key (RS)
```

Both `scripts/sftp-config/` and `scripts/keys/` are listed in `.gitignore`. **Never commit keys or config files.**

### sftp-config.json Format

The config file uses the **Sublime Text SFTP plugin** format, which phpseclib3 natively supports:

```json
{
    "type": "sftp",
    "host": "sftp.example.com",
    "user": "deploy-user",
    "port": 22,
    "remote_path": "/var/www/releases",
    "ssh_key_file": "scripts/keys/deploy_dev.pem",
    "ssh_key_passphrase": ""
}
```

> The `remote_path` here is the base path. The repository-specific `PATH_SUFFIX` is appended at runtime.

### Running Locally

```bash
php api/deploy/deploy-sftp.php --config scripts/sftp-config/sftp-config.json --file dist/release.zip
```

---

## GitHub Secrets and Variables

Two deployment environments are supported: **DEV** (development/staging) and **RS** (release server/production). Each environment uses a distinct prefix.

### DEV Environment (`DEV_FTP_*`)

DEV secrets and variables can be configured at either **organization level** or **repository level**.

| Name | Type | Scope | Purpose |
|------|------|-------|---------|
| `DEV_FTP_HOST` | Variable | Org or Repo | SFTP server hostname or IP |
| `DEV_FTP_USER` | Variable | Org or Repo | SFTP username |
| `DEV_FTP_PORT` | Variable | Org or Repo | SFTP port (default: `22`) |
| `DEV_FTP_PATH_SUFFIX` | Variable | Org or Repo | Repo-specific path appended to base path |
| `DEV_FTP_KEY` | Secret | Org or Repo | SSH private key (OpenSSH PEM or PuTTY PPK) |
| `DEV_FTP_PATH` | Secret | Org or Repo | Base deployment path on server |
| `DEV_FTP_KEY_PASSPHRASE` | Secret | Org or Repo | Passphrase for SSH key (empty string if none) |

### RS Environment (`RS_FTP_*`)

RS secrets are configured at **organization level**, except `RS_FTP_PATH_SUFFIX` which is set per repository.

| Name | Type | Scope | Purpose |
|------|------|-------|---------|
| `RS_FTP_HOST` | Variable | **Org** | SFTP server hostname or IP |
| `RS_FTP_USER` | Variable | **Org** | SFTP username |
| `RS_FTP_PORT` | Variable | **Org** | SFTP port (default: `22`) |
| `RS_FTP_PATH_SUFFIX` | Variable | **Repo** | Repo-specific path appended to base path |
| `RS_FTP_KEY` | Secret | **Org** | SSH private key (OpenSSH PEM or PuTTY PPK) |
| `RS_FTP_PATH` | Secret | **Org** | Base deployment path on server |
| `RS_FTP_KEY_PASSPHRASE` | Secret | **Org** | Passphrase for SSH key (empty string if none) |

> **Note**: Repository secrets/variables override organization-level ones when both are defined for the same name.

---

## Workflow Integration

GitHub Actions workflows pass credentials to the PHP deploy script via environment variables.

### DEV Deployment Workflow Example

```yaml
- name: Deploy to DEV via SFTP
  env:
    SFTP_HOST: ${{ vars.DEV_FTP_HOST }}
    SFTP_USER: ${{ vars.DEV_FTP_USER }}
    SFTP_PORT: ${{ vars.DEV_FTP_PORT }}
    SFTP_PATH_SUFFIX: ${{ vars.DEV_FTP_PATH_SUFFIX }}
    SFTP_KEY: ${{ secrets.DEV_FTP_KEY }}
    SFTP_BASE_PATH: ${{ secrets.DEV_FTP_PATH }}
    SFTP_KEY_PASSPHRASE: ${{ secrets.DEV_FTP_KEY_PASSPHRASE }}
  run: |
    php api/deploy/deploy-sftp.php --file dist/release.zip
```

### RS Deployment Workflow Example

```yaml
- name: Deploy to RS via SFTP
  env:
    SFTP_HOST: ${{ vars.RS_FTP_HOST }}
    SFTP_USER: ${{ vars.RS_FTP_USER }}
    SFTP_PORT: ${{ vars.RS_FTP_PORT }}
    SFTP_PATH_SUFFIX: ${{ vars.RS_FTP_PATH_SUFFIX }}
    SFTP_KEY: ${{ secrets.RS_FTP_KEY }}
    SFTP_BASE_PATH: ${{ secrets.RS_FTP_PATH }}
    SFTP_KEY_PASSPHRASE: ${{ secrets.RS_FTP_KEY_PASSPHRASE }}
  run: |
    php api/deploy/deploy-sftp.php --file dist/release.zip
```

---

## Path Resolution

The final upload directory is computed as:

```
FINAL_PATH = BASE_PATH + "/" + PATH_SUFFIX
```

| `BASE_PATH` (from `*_FTP_PATH`) | `PATH_SUFFIX` (from `*_FTP_PATH_SUFFIX`) | Final Path |
|---|---|---|
| `/var/www/releases` | `extensions/mymodule` | `/var/www/releases/extensions/mymodule` |
| `/home/deploy/dist` | `v2.1.0` | `/home/deploy/dist/v2.1.0` |
| `/releases` | *(empty)* | `/releases` |

**Conventions**:
- `BASE_PATH` must be an absolute path (begins with `/`)
- `PATH_SUFFIX` should be relative (no leading `/` required — handled automatically)
- Trailing slashes are normalized

---

## SSH Key Setup

### Generating a New Key Pair

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "deploy@mokoconsulting.tech" -f scripts/keys/deploy_dev.pem

# With passphrase protection (recommended for production/RS)
ssh-keygen -t ed25519 -C "deploy@mokoconsulting.tech" -f scripts/keys/deploy_rs.pem
# Enter passphrase when prompted — store in RS_FTP_KEY_PASSPHRASE

# Files created:
#   scripts/keys/deploy_dev.pem      — private key (store in DEV_FTP_KEY)
#   scripts/keys/deploy_dev.pem.pub  — public key (add to server)
```

### Adding the Public Key to the Server

```bash
# On the SFTP server
cat deploy_dev.pem.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Configuring GitHub Secrets

1. Navigate to **Settings → Secrets and variables → Actions**
2. For org-level: **Organization Settings → Secrets and variables → Actions**
3. Click **New secret** / **New variable**
4. Paste the full private key content (including `-----BEGIN` / `-----END` lines) into `*_FTP_KEY`
5. Set `*_FTP_KEY_PASSPHRASE` to the passphrase, or an empty string if the key has no passphrase

> **PuTTY PPK keys** do not need to be converted — phpseclib3 reads them directly.

---

## Security Best Practices

1. **SSH key auth only** — Password-only SFTP is prohibited
2. **Protect keys with passphrases** for RS/production keys
3. **Never commit keys or sftp-config.json** — both directories are gitignored
4. **Rotate keys annually** or immediately after personnel changes
5. **Limit server access** — SFTP user should have write access only to the deployment directory
6. **Use chroot jails** where the server OS supports it
7. **Enable server-side logging** — monitor all SFTP connections
8. **Pin action versions** in workflows — do not use `@main` or `@latest`

---

## Troubleshooting

### Connection Refused

- Verify `*_FTP_HOST` and `*_FTP_PORT` are correct
- Ensure the server accepts connections from GitHub Actions IP ranges
- Check server firewall rules

### Authentication Failure (`Permission denied (publickey)`)

- Confirm `*_FTP_KEY` contains the complete private key, including header/footer lines
- Verify the corresponding public key is in the server's `~/.ssh/authorized_keys`
- Check `*_FTP_KEY_PASSPHRASE` is correct (or empty if no passphrase)
- phpseclib3 supports both OpenSSH PEM and PuTTY PPK — verify the key format is valid

### Path Not Found

- Verify `*_FTP_PATH` exists on the server and the SFTP user has write access
- Check `*_FTP_PATH_SUFFIX` for typos
- Review the computed `FINAL_PATH` in the workflow log output

### phpseclib3 Not Found

```bash
# Install Composer dependencies
composer install --no-dev --optimize-autoloader
```

---

## See Also

- [Release Management Policy](../policy/governance/release-management.md)
- [PHP-Only Architecture](../guide/php-only-architecture.md)
- [Security Scanning Policy](../policy/security-scanning.md)
- [Akeeba and Panopticon Policy](../policy/waas/akeeba-and-panopticon.md)

---

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Guide |
| Domain | Operations / Deployment |
| Applies To | All Repositories |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/MokoStandards |
| Path | docs/deployment/sftp.md |
| Version | 04.00.15 |
| Status | Active |
| Last Reviewed | 2026-03-15 |

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-15 | 04.00.15 | Full rewrite: PHP/phpseclib3, SSH-key-only auth, DEV_FTP_*/RS_FTP_* secrets tables |
| 2026-01-28 | 03.00.00 | Standardized metadata |
| 2026-01-07 | 01.00.00 | Initial SFTP deployment documentation |
