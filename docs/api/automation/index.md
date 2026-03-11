# Automation Scripts

## Overview

Documentation for automation scripts in `/api/automation/`.

## bulk_sync.php

Synchronizes workflows, configurations, and scripts across multiple repositories.

**Key Features:**
- Auto-detects repository platform
- Generates repository definitions in `api/definitions/sync/`
- Creates Pull Requests with changes
- Supports dry-run mode

**Usage:**
```bash
php api/automation/bulk_sync.php --org mokoconsulting-tech
```

See [Synced Definitions](../definitions/sync/index.md) for details on generated definitions.

---

## deploy_sftp.php

Deploys a local source directory to one or more remote servers using key-based SFTP
authentication via `phpseclib3`. Designed for en-masse deployment of project source
trees to client servers.

**Key Features:**
- Private-key authentication (RSA, ECDSA, Ed25519 via phpseclib3)
- Single-server or multi-server (JSON config) mode
- Recursive directory upload with automatic remote directory creation
- Dry-run mode — lists files that would be transferred without connecting
- Audit-logged operations via `AuditLogger`
- Progress callback for verbose output
- GitHub Actions step summary support

**Usage — single server:**
```bash
php api/automation/deploy_sftp.php \
  --src api/src \
  --host client.example.com \
  --user deploy \
  --key ~/.ssh/id_deploy \
  --remote /var/www/html
```

**Usage — multiple servers (JSON file):**
```bash
php api/automation/deploy_sftp.php \
  --src api/src \
  --servers servers.json \
  --key ~/.ssh/id_deploy
```

The `servers.json` file must be a JSON array of server objects:
```json
[
  {
    "host": "server1.example.com",
    "port": 22,
    "username": "deploy",
    "remote_path": "/var/www/html"
  },
  {
    "host": "server2.example.com",
    "username": "www-data",
    "remote_path": "/opt/app"
  }
]
```

Fields `port` (default 22) and `passphrase` are optional per entry.
The `--key` CLI flag provides a default private key for all entries that
do not specify their own `private_key` field.

**Options:**

| Option | Description |
|--------|-------------|
| `--src <path>` | Local source directory (required) |
| `--host <hostname>` | Remote host (single-server mode) |
| `--port <n>` | SSH port (default: 22) |
| `--user <name>` | SSH username (single-server mode) |
| `--key <path>` | PEM private key file (required) |
| `--passphrase <str>` | Passphrase for encrypted key |
| `--remote <path>` | Absolute remote path (single-server mode) |
| `--servers <file>` | JSON server list (multi-server mode) |
| `--timeout <sec>` | Connection timeout (default: 30) |
| `--dry-run` | List files without transferring |
| `--verbose` | Print per-file progress |

**Related class:** [`SftpDeployer`](../lib/Enterprise/index.md)

---

**Location**: `docs/api/automation/`  
**Mirrors**: `/api/automation/`  
**Last Updated**: 2026-03-11
