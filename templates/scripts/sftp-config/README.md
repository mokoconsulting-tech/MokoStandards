<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Templates.Scripts
INGROUP: MokoStandards.Templates
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/scripts/sftp-config/README.md
VERSION: 04.00.15
BRIEF: Setup guide for local SFTP deployment configuration files
-->

# SFTP Deploy Config — Local Setup

This directory (`scripts/sftp-config/`) holds per-environment SFTP connection
configs used by `deploy-sftp.php` and the `deploy-dev` / `deploy-release`
GitHub Actions workflows.

> **This directory is gitignored.** Config files contain server hostnames and
> usernames. Never commit them.

---

## Quick Setup

1. **Copy the example templates** from MokoStandards:

   ```bash
   # From your repo root
   mkdir -p scripts/sftp-config scripts/keys
   cp path/to/MokoStandards/templates/scripts/deploy/sftp-config.dev.json.example \
      scripts/sftp-config/sftp-config.dev.json
   cp path/to/MokoStandards/templates/scripts/deploy/sftp-config.rs.json.example \
      scripts/sftp-config/sftp-config.rs.json
   ```

2. **Fill in your values** — edit `sftp-config.dev.json`:

   ```json
   {
     "type": "sftp",
     "host": "iad1-shared-b7-01.dreamhost.com",
     "user": "mokoconsulting_dev",
     "ssh_key_file": "jmiller_private.ppk",
     "port": "22",
     "remote_path": "/home/mokoconsulting_dev/dev.example.com/htdocs/custom/mymodule/"
   }
   ```

3. **Place your SSH key** in `scripts/keys/`:

   ```
   scripts/
     keys/
       jmiller_private.ppk    ← gitignored; never committed
   ```

   `ssh_key_file` may be a bare filename (resolved from `scripts/keys/`) or
   an absolute path (e.g. `J:/My Drive/Keys/jmiller_private.ppk`).

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `sftp-config.dev.json` | Dev server connection (used with `--env dev`) |
| `sftp-config.rs.json` | Production/release server connection (used with `--env rs`) |

---

## Running the Script

```bash
# Preview what would be uploaded (no connection made)
php path/to/MokoStandards/api/deploy/deploy-sftp.php \
  --path . --env dev --dry-run --verbose

# Deploy src/ to dev
php path/to/MokoStandards/api/deploy/deploy-sftp.php \
  --path . --env dev

# Deploy src/ to production
php path/to/MokoStandards/api/deploy/deploy-sftp.php \
  --path . --env rs
```

For full option reference run:
```bash
php path/to/MokoStandards/api/deploy/deploy-sftp.php --help
```

---

**Last Updated:** 2026-03-13
