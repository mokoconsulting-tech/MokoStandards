# Terraform Configuration Documentation

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **VERSION** | 04.00.03 |
| **LAST UPDATED** | 2026-02-21 |
| **STATUS** | Active |

## Overview

This directory contains documentation for all Terraform configurations in the MokoStandards repository. Terraform is used to manage infrastructure, GitHub repositories, and automation workflows.

## Directory Structure

```
docs/terraform/
├── README.md                           # This file
├── main.md                             # Main terraform configuration
├── variables.md                        # Variable definitions
├── outputs.md                          # Output definitions
├── config-override.md                  # Override configuration (.github/config.tf)
├── repository-management/
│   └── main.md                         # Repository management module
├── repository-types/
│   ├── default-repository.md           # Default repository configuration
│   └── repo-health-defaults.md         # Repository health defaults
├── webserver/
│   ├── ubuntu-dev-webserver.md         # Ubuntu development webserver
│   ├── ubuntu-prod-webserver.md        # Ubuntu production webserver
│   ├── windows-dev-webserver.md        # Windows development webserver
│   └── windows-prod-webserver.md       # Windows production webserver
└── workstation/
    ├── ubuntu-dev-workstation.md       # Ubuntu development workstation
    └── windows-dev-workstation.md      # Windows development workstation
```

## Terraform Files in Repository

| Category | File | Documentation | Purpose |
|----------|------|---------------|---------|
| **Core** | `terraform/main.tf` | [main.md](main.md) | Main terraform configuration |
| **Core** | `terraform/variables.tf` | [variables.md](variables.md) | Input variable definitions |
| **Core** | `terraform/outputs.tf` | [outputs.md](outputs.md) | Output value definitions |
| **Override** | `.github/config.tf` | [config-override.md](config-override.md) | Repository-specific overrides |
| **Management** | `terraform/repository-management/main.tf` | [repository-management/main.md](repository-management/main.md) | GitHub repository management |
| **Types** | `terraform/repository-types/default-repository.tf` | [repository-types/default-repository.md](repository-types/default-repository.md) | Default repo settings |
| **Types** | `terraform/repository-types/repo-health-defaults.tf` | [repository-types/repo-health-defaults.md](repository-types/repo-health-defaults.md) | Health check defaults |
| **Webserver** | `terraform/webserver/ubuntu-dev-webserver.tf` | [webserver/ubuntu-dev-webserver.md](webserver/ubuntu-dev-webserver.md) | Ubuntu dev server |
| **Webserver** | `terraform/webserver/ubuntu-prod-webserver.tf` | [webserver/ubuntu-prod-webserver.md](webserver/ubuntu-prod-webserver.md) | Ubuntu prod server |
| **Webserver** | `terraform/webserver/windows-dev-webserver.tf` | [webserver/windows-dev-webserver.md](webserver/windows-dev-webserver.md) | Windows dev server |
| **Webserver** | `terraform/webserver/windows-prod-webserver.tf` | [webserver/windows-prod-webserver.md](webserver/windows-prod-webserver.md) | Windows prod server |
| **Workstation** | `terraform/workstation/ubuntu-dev-workstation.tf` | [workstation/ubuntu-dev-workstation.md](workstation/ubuntu-dev-workstation.md) | Ubuntu workstation |
| **Workstation** | `terraform/workstation/windows-dev-workstation.tf` | [workstation/windows-dev-workstation.md](workstation/windows-dev-workstation.md) | Windows workstation |

## Quick Start

### Prerequisites

- Terraform >= 1.0
- GitHub token with appropriate permissions
- AWS credentials (for infrastructure modules)

### Basic Usage

```bash
# Initialize terraform
terraform init

# Validate configuration
terraform validate

# Plan changes
terraform plan

# Apply changes
terraform apply
```

### Working with Overrides

Each repository can have a `.github/config.tf` file that overrides default behavior:

```terraform
# .github/config.tf
locals {
  exclude_files = [
    {
      path   = ".github/workflows/build.yml"
      reason = "Custom build process"
    }
  ]
  
  protected_files = [
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    }
  ]
}
```

See [config-override.md](config-override.md) for complete documentation.

## Configuration Categories

### Core Configuration
Essential terraform files that define the infrastructure foundation.

- **main.tf**: Primary configuration and module orchestration
- **variables.tf**: Input parameters for customization
- **outputs.tf**: Values exposed for use by other modules

### Repository Management
Configuration for managing GitHub repositories across the organization.

- **repository-management/**: GitHub organization and repository automation
- **repository-types/**: Reusable repository configuration templates

### Infrastructure Modules
Pre-configured infrastructure patterns for common use cases.

- **webserver/**: Web server configurations (Ubuntu/Windows, dev/prod)
- **workstation/**: Development workstation configurations

### Override System
Repository-specific customization without forking.

- **config.tf**: Located in `.github/` directory of each repository
- Controls which files are synced during bulk updates
- See [Bulk Sync Documentation](../workflows/bulk-repo-sync.md)

## Standards and Conventions

All terraform files in this repository follow [Terraform File Standards](../policy/terraform-file-standards.md):

1. ✅ GPL-3.0-or-later copyright header
2. ✅ FILE INFORMATION section
3. ✅ `file_metadata` locals block
4. ✅ Version 04.00.03
5. ✅ ISO 8601 timestamps
6. ✅ Schema version 2.0

## Related Documentation

- [Terraform File Standards](../policy/terraform-file-standards.md) - Structure and format requirements
- [Bulk Repository Sync](../workflows/bulk-repo-sync.md) - Automated synchronization
- [Override Files Guide](../guide/terraform-override-files.md) - How to customize sync behavior
- [Terraform Installation Guide](../guide/terraform-installation.md) - Setup instructions

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Comprehensive terraform documentation added |
| 04.00.02 | 2026-02-20 | Override system standardized |
| 04.00.01 | 2026-02-19 | Initial terraform structure |

## Contributing

When adding new terraform configurations:

1. Follow [terraform-file-standards.md](../policy/terraform-file-standards.md)
2. Add documentation in this directory
3. Update this README with links
4. Include examples and usage instructions
5. Test with `terraform validate` and `terraform plan`

## Support

For questions or issues:

- Review individual file documentation
- Check [Terraform File Standards](../policy/terraform-file-standards.md)
- See [Contributing Guide](../../CONTRIBUTING.md)
- Contact: MokoStandards Team
