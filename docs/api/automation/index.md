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

**Location**: `docs/api/automation/`  
**Mirrors**: `/api/automation/`  
**Last Updated**: 2026-03-03
