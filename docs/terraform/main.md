# Main Terraform Configuration

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **File** | `terraform/main.tf` |
| **Version** | 04.00.03 |
| **Last Updated** | 2026-02-21 |
| **Type** | main |
| **Purpose** | Primary terraform configuration and module orchestration |

## Overview

The `main.tf` file is the primary terraform configuration file that orchestrates all infrastructure and repository management modules. It defines providers, module instantiations, and high-level resource configurations.

## File Location

```
terraform/main.tf
```

## Purpose

- Define terraform backend configuration
- Configure providers (GitHub, AWS, etc.)
- Orchestrate module instantiation
- Define top-level resources
- Set up provider authentication

## Structure

### 1. Terraform Block

```terraform
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    # Backend configuration for state storage
    bucket = "mokostandards-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### 2. Provider Configuration

```terraform
provider "github" {
  token = var.github_token
  owner = var.github_organization
}
```

### 3. File Metadata

All terraform files include a `file_metadata` locals block:

```terraform
locals {
  file_metadata = {
    name              = "Main Configuration"
    description       = "Primary terraform configuration"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    file_type         = "main"
    terraform_version = ">= 1.0"
  }
}
```

## Usage

### Initialize Terraform

```bash
cd terraform
terraform init
```

### Validate Configuration

```bash
terraform validate
```

### Plan Changes

```bash
terraform plan -var-file="environments/production.tfvars"
```

### Apply Changes

```bash
terraform apply -var-file="environments/production.tfvars"
```

## Dependencies

### Required Providers

- **github**: For GitHub resource management
- **aws**: For AWS infrastructure (if used)

### Required Variables

See [variables.md](variables.md) for complete list:

- `github_token`: GitHub personal access token
- `github_organization`: Organization name (default: mokoconsulting-tech)

### Optional Variables

- `enable_repository_management`: Enable/disable repo management
- `default_branch`: Default branch name (default: main)

## Modules Referenced

This configuration may reference:

- `./repository-management/`: GitHub repository automation
- `./repository-types/`: Repository configuration templates
- `./webserver/`: Web server configurations
- `./workstation/`: Workstation configurations

## Outputs

Defined in [outputs.tf](outputs.md):

- Repository URLs
- Resource identifiers
- Configuration summaries

## Best Practices

1. **State Management**: Always use remote state backend
2. **Variable Files**: Use separate `.tfvars` files per environment
3. **Module Versioning**: Pin module versions for stability
4. **Provider Locking**: Use terraform lock file (`.terraform.lock.hcl`)
5. **Validation**: Run `terraform validate` before committing

## Common Operations

### Add New Module

```terraform
module "new_module" {
  source = "./modules/new-module"
  
  # Module variables
  variable1 = var.input1
  variable2 = var.input2
}
```

### Reference Module Outputs

```terraform
resource "example_resource" "example" {
  value = module.new_module.output_value
}
```

## Troubleshooting

### Issue: Provider Authentication Failed

**Solution**: Ensure `GITHUB_TOKEN` environment variable is set or passed via variable file.

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
terraform plan
```

### Issue: State Lock Error

**Solution**: Verify backend configuration and ensure no other terraform process is running.

```bash
terraform force-unlock <LOCK_ID>
```

### Issue: Module Not Found

**Solution**: Run `terraform init` to download modules.

```bash
terraform init -upgrade
```

## Related Files

- [variables.tf](variables.md) - Input variables
- [outputs.tf](outputs.md) - Output definitions
- [.github/config.tf](config-override.md) - Override configuration

## Standards Compliance

This file follows [Terraform File Standards](../policy/terraform-file-standards.md):

- ✅ Copyright header (GPL-3.0-or-later)
- ✅ FILE INFORMATION section
- ✅ file_metadata locals block
- ✅ Version 04.00.03
- ✅ Terraform >= 1.0 requirement

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Updated to new terraform standards |
| 04.00.02 | 2026-02-20 | Provider configuration enhanced |
| 04.00.01 | 2026-02-19 | Initial structured version |

## See Also

- [Terraform Installation Guide](../guide/terraform-installation.md)
- [Terraform File Standards](../policy/terraform-file-standards.md)
- [Repository Management Documentation](repository-management/main.md)
