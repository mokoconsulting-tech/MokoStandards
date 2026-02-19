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
DEFGROUP: MokoStandards.Development
INGROUP: MokoStandards.CRM
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/development/crm/module-registry.md
VERSION: 04.00.01
BRIEF: Dolibarr module number registry for Moko Consulting
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Dolibarr Module Number Registry

## Overview

This document maintains the official registry of Dolibarr module numbers reserved for Moko Consulting. Module numbers **185051 to 185099** (49 total) are officially reserved for Moko Consulting use.

## Quick Links

- **[CRM Development Guide](../../guide/crm/dolibarr-development-guide.md)** - Comprehensive development guide
- **[Development Standards](../../policy/crm/development-standards.md)** - Development standards and best practices  
- **[Reserve Module ID Workflow](../../workflows/reserve-dolibarr-module-id.md)** - Automated reservation process
- **[Run Workflow](./../../../.github/workflows/reserve-dolibarr-module-id.yml)** - Reserve a module ID now

## Reserved Module Numbers

Dolibarr module numbers **185051 to 185099** are reserved for Moko Consulting use.

**Range**: 185051-185099  
**Total Available**: 49 module IDs  
**Organization**: Moko Consulting

## Dolibarr Extensions Registry

| Module Name | Module Number | Status | Description | Repository |
|-------------|---------------|--------|-------------|------------|
| MokoDoliTools | 185051 | Active | Core utilities and admin toolkit for Dolibarr with curated defaults, UI enhancements, and entity-aware operations | [mokoconsulting-tech/MokoDoliTools](https://github.com/mokoconsulting-tech/MokoDoliTools) |
| MokoDoliSign | 185052 | Reserved | Digital signature and document signing module | TBD |
| MokoCRMTheme | 185053 | Reserved | MokoCRM Theme | TBD |
| MokoDoliChimp | 185054 | Reserved | MailChimp integration for Dolibarr | TBD |
| MokoDoliPasskey | 185055 | Reserved | WebAuthn/Passkey authentication module for Dolibarr | TBD |
| MokoDoliForm | 185056 | Reserved | Advanced form builder and workflow module for Dolibarr | TBD |
| MokoDoliG | 185057 | Reserved | Google Workspace integration module for Dolibarr | TBD |
| MokoDoliDeploy | 185058 | Reserved | Deployment automation and management module for Dolibarr | TBD |
| MokoDoliMulti | 185059 | Reserved | Multi-entity management module for Dolibarr | TBD |
| MokoDoliHRM | 185060 | Reserved | Human Resource Management module for Dolibarr | TBD |
| MokoDoliAuth | 185061 | Reserved | Advanced authentication module for Dolibarr | TBD |
| MokoDoliOffline | 185062 | Reserved | Offline capability module for Dolibarr | TBD |
| MokoDoliReleaseHelper | 185063 | Reserved | Release management and version control helper module for Dolibarr | TBD |
| Available for Assignment | 185064-185099 | Reserved | Reserved for future Moko Consulting modules | - |

## Module ID Reservation Process

### Automated Reservation (Recommended)

Use the **[Reserve Dolibarr Module ID Workflow](../../workflows/reserve-dolibarr-module-id.md)** for automated module ID reservation:

1. **Navigate** to the [workflow](./../../../.github/workflows/reserve-dolibarr-module-id.yml)
2. **Click** "Run workflow"
3. **Provide**:
   - Module description
   - Repository URL (optional, defaults to current repository)
   - Specific module ID (optional, auto-assigns if not provided)
4. **Review** the automatically created pull request
5. **Get approval** from CRM Development Lead
6. **Merge** to officially reserve the module ID

The workflow automatically:
- Finds the next available module ID (or validates your specified ID)
- Updates this registry table
- Creates a pull request with all changes
- Optionally pushes `DOLIBARR_MODULE_ID.txt` to your module repository

### Manual Reservation

If you prefer to reserve manually:

1. **Create a Pull Request** to [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
2. **Update this table** with:
   - Module name
   - Next available module number from the reserved range (185064-185099)
   - Status: "Reserved"
   - Brief description of the module's purpose
   - Repository link (use "TBD" if not yet created)
3. **Get approval** from the CRM Development Lead before merging
4. **Merge the PR** to officially reserve the module ID

**Important**: Module IDs MUST be reserved through a pull request. Direct commits to reserve module IDs are not permitted and are blocked on protected branches via branch protection rules (requiring PRs, code review, and automated checks) for the default and release branches.

## Module ID Usage

Once your module ID is reserved:

### 1. Create Module ID File

Create `src/DOLIBARR_MODULE_ID.txt` in your module repository:

```
DOLIBARR_MODULE_ID=185064

Module Name: YourModuleName
Module ID: 185064
Reserved Range: 185064-185099 (Moko Consulting)
Description: Your module description

This ID is registered in the MokoStandards module registry:
https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md

DO NOT CHANGE THIS ID!
```

### 2. Use in Module Descriptor

In your `core/modules/modYourModule.class.php`:

```php
<?php
class modYourModule extends DolibarrModules
{
    public function __construct($db)
    {
        global $langs, $conf;
        
        $this->db = $db;
        
        // Module ID - FROM MOKO CONSULTING RESERVED RANGE
        $this->numero = 185064; // Your reserved number
        
        // ... rest of your module descriptor
    }
}
```

### 3. Verify No Conflicts

Always verify that:
- Your module ID is in the range 185051-185099
- No other Moko Consulting module uses the same ID
- The ID is officially reserved in this registry

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Active** | Module is deployed and in production use |
| **Reserved** | Module ID is reserved but module not yet developed or deployed |
| **Deprecated** | Module is no longer maintained (ID remains reserved) |
| **Available for Assignment** | Available for new module reservation |

## Module Development Resources

### Documentation

- **[Dolibarr Development Guide](../../guide/crm/dolibarr-development-guide.md)** - Complete guide to developing Dolibarr modules
- **[CRM Development Standards](../../policy/crm/development-standards.md)** - Coding standards and best practices
- **[Module ID Workflow Documentation](../../workflows/reserve-dolibarr-module-id.md)** - Detailed workflow usage guide

### Repositories

All Moko Consulting Dolibarr modules are hosted under:
**[https://github.com/mokoconsulting-tech/](https://github.com/mokoconsulting-tech/)**

### Official Dolibarr Resources

- **[Dolibarr Developer Documentation](https://wiki.dolibarr.org/index.php/Developer_documentation)**
- **[Module Development](https://wiki.dolibarr.org/index.php/Module_development)**
- **[Dolibarr on GitHub](https://github.com/Dolibarr/dolibarr)**

## FAQs

### How do I reserve a module ID?

Use the automated workflow (recommended) or create a manual PR. See [Module ID Reservation Process](#module-id-reservation-process) above.

### Can I request a specific module ID?

Yes! When using the workflow, you can specify a module ID in the range 185064-185099. The workflow will validate it's available.

### What if all IDs are reserved?

Contact the CRM Development Lead. We may need to request additional module number ranges from Dolibarr or deprecate unused reservations.

### Can I use a module ID outside our reserved range?

No. All Moko Consulting modules MUST use IDs from our reserved range (185051-185099) to avoid conflicts with other Dolibarr modules.

### What happens if I use the wrong module ID?

Using a non-reserved ID risks conflicts with other Dolibarr modules. Always reserve your ID through this registry first.

## Support

For questions about module ID reservation or Dolibarr development:

- **Create an issue** in [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards/issues)
- **Contact** the CRM Development Lead
- **Review** the [CRM Development Standards](../../policy/crm/development-standards.md)

---

**Document Version**: 04.00.01  
**Last Updated**: 2026-02-19  
**Maintained By**: CRM Development Lead
