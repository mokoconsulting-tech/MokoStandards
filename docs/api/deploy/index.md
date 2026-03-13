<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/deploy/index.md
VERSION: 04.00.15
BRIEF: API reference for deployment scripts in api/deploy/
-->

# Deploy Scripts

Scripts in `api/deploy/` upload repository source files to remote web servers via SFTP.

---

## deploy-sftp.php

**Path:** `api/deploy/deploy-sftp.php`
**Base class:** `CLIApp`

Reads connection details from a `sftp-config.json` file and recursively uploads
a repository's `src/` directory to the configured remote path.
Supports PuTTY `.ppk` keys and OpenSSH PEM keys via phpseclib. Strips `//`
line comments from the config file so the Sublime Text SFTP plugin format works
without modification.

### Usage

```bash
php api/deploy/deploy-sftp.php [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path <dir>` | `.` | Repository root to deploy |
| `--src-dir <dir>` | `src` | Sub-directory inside the repo to upload |
| `--config <file>` | `{path}/script/sftp-config.json` | Explicit config file path |
| `--key-passphrase <pw>` | _(none)_ | Passphrase for encrypted SSH key |
| `--dry-run` | off | Preview uploads without connecting |
| `--verbose` / `-v` | off | Show per-file transfer details |
| `--quiet` / `-q` | off | Suppress all output except errors |
| `--help` / `-h` | — | Show help and exit |

### Key Resolution

`ssh_key_file` in `sftp-config.json` may be an absolute path or a bare filename.
When not absolute, the script looks for the key under `{path}/scripts/keys/` first,
then falls back to the value as a path relative to CWD.

Store keys locally at:
```
{repo_root}/
  scripts/
    keys/          ← gitignored via *.ppk; place your .ppk / PEM file here
  script/
    sftp-config.dev.json    ← gitignored; copy from template
    sftp-config.rs.json     ← gitignored; copy from template
```

### Examples

```bash
# Preview what would be uploaded (no connection)
php api/deploy/deploy-sftp.php --dry-run --verbose

# Deploy src/ of a specific repository
php api/deploy/deploy-sftp.php --path /repos/mymodule

# Use a different source directory
php api/deploy/deploy-sftp.php --path /repos/mymodule --src-dir htdocs

# Deploy to production using explicit config
php api/deploy/deploy-sftp.php \
  --path /repos/mymodule \
  --config /repos/mymodule/script/sftp-config.rs.json \
  --key-passphrase "my passphrase"
```

### Config Format

Copy a template from `templates/scripts/deploy/` and fill in your values:

```json
{
  "type": "sftp",
  "host": "iad1-shared-b7-01.dreamhost.com",
  "user": "mokoconsulting_dev",
  "ssh_key_file": "jmiller_private.ppk",
  "port": "22",
  "remote_path": "/home/mokoconsulting_dev/crm.dev.mokoconsulting.tech/htdocs/custom/mymodule/",
  "ignore_regexes": [
    "\\.git*",
    "sftp-config(-alt\\d?)?\\.json",
    "\\.DS_Store",
    "Thumbs\\.db"
  ]
}
```

`ssh_key_file` may be a bare filename (resolved from `scripts/keys/`) or an
absolute path (e.g. `J:/My Drive/Keys/jmiller_private.ppk`).

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All files uploaded successfully |
| `1` | Connection failed or one or more files could not be uploaded |
| `2` | Invalid arguments or config file error |

### Called by Workflows

| Workflow | Trigger | Target |
|----------|---------|--------|
| `deploy-dev.yml` | `workflow_call`, `workflow_dispatch` | Dev server |
| `deploy-release.yml` | `workflow_call`, `workflow_dispatch` | Production server (requires `production` environment approval) |

See [Deploy Workflows](../../workflows/deploy-dev.md) for workflow usage.

---

**Location:** `docs/api/deploy/`
**Mirrors:** `api/deploy/`
**Last Updated:** 2026-03-13
