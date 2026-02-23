# Variables Configuration

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **File** | `terraform/variables.tf` |
| **Version** | 04.00.03 |
| **Last Updated** | 2026-02-21 |
| **Type** | variables |
| **Purpose** | Input variable definitions for terraform configuration |

## Overview

The `variables.tf` file defines all input variables used across the terraform configuration. These variables allow customization of infrastructure and repository management without modifying the main configuration files.

## File Location

```
terraform/variables.tf
```

## Variable Categories

### 1. GitHub Configuration

```terraform
variable "github_token" {
  description = "GitHub personal access token for API authentication"
  type        = string
  sensitive   = true
}

variable "github_organization" {
  description = "GitHub organization name"
  type        = string
  default     = "mokoconsulting-tech"
}

variable "default_branch" {
  description = "Default branch name for repositories"
  type        = string
  default     = "main"
}
```

### 2. Repository Management

```terraform
variable "enable_repository_management" {
  description = "Enable GitHub repository management"
  type        = bool
  default     = true
}

variable "repository_visibility" {
  description = "Default repository visibility (public/private/internal)"
  type        = string
  default     = "private"
  
  validation {
    condition     = contains(["public", "private", "internal"], var.repository_visibility)
    error_message = "Repository visibility must be public, private, or internal."
  }
}
```

### 3. AWS Configuration (if used)

```terraform
variable "aws_region" {
  description = "AWS region for infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}
```

## Usage Examples

### Using Environment Variables

```bash
export TF_VAR_github_token="ghp_xxxxxxxxxxxxx"
export TF_VAR_github_organization="my-org"

terraform plan
```

### Using Variable Files

Create `terraform.tfvars`:

```terraform
github_token       = "ghp_xxxxxxxxxxxxx"
github_organization = "mokoconsulting-tech"
default_branch     = "main"

enable_repository_management = true
repository_visibility = "private"

# AWS Configuration
aws_region  = "us-east-1"
environment = "production"
```

Apply with variable file:

```bash
terraform apply -var-file="terraform.tfvars"
```

### Using Command Line

```bash
terraform apply \
  -var="github_organization=my-org" \
  -var="environment=staging"
```

## Variable Types

### String Variables

```terraform
variable "example_string" {
  description = "Example string variable"
  type        = string
  default     = "default-value"
}
```

### Boolean Variables

```terraform
variable "example_bool" {
  description = "Example boolean variable"
  type        = bool
  default     = true
}
```

### Number Variables

```terraform
variable "example_number" {
  description = "Example number variable"
  type        = number
  default     = 5
}
```

### List Variables

```terraform
variable "example_list" {
  description = "Example list variable"
  type        = list(string)
  default     = ["item1", "item2", "item3"]
}
```

### Map Variables

```terraform
variable "example_map" {
  description = "Example map variable"
  type        = map(string)
  default     = {
    key1 = "value1"
    key2 = "value2"
  }
}
```

### Object Variables

```terraform
variable "example_object" {
  description = "Example object variable"
  type = object({
    name    = string
    enabled = bool
    count   = number
  })
  default = {
    name    = "example"
    enabled = true
    count   = 3
  }
}
```

## Variable Validation

Add validation rules to ensure correct values:

```terraform
variable "environment" {
  description = "Environment name"
  type        = string
  
  validation {
    condition     = can(regex("^(dev|staging|production)$", var.environment))
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "port" {
  description = "Port number"
  type        = number
  
  validation {
    condition     = var.port >= 1 && var.port <= 65535
    error_message = "Port must be between 1 and 65535."
  }
}
```

## Sensitive Variables

Mark sensitive variables to hide values in output:

```terraform
variable "api_key" {
  description = "API key for authentication"
  type        = string
  sensitive   = true
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

## Environment-Specific Variables

Create separate variable files per environment:

### development.tfvars

```terraform
environment             = "dev"
github_organization     = "mokoconsulting-tech-dev"
repository_visibility   = "private"
enable_repository_management = true
```

### production.tfvars

```terraform
environment             = "production"
github_organization     = "mokoconsulting-tech"
repository_visibility   = "private"
enable_repository_management = true
```

## Best Practices

1. ✅ **Use Descriptions**: Always provide clear descriptions
2. ✅ **Set Defaults**: Provide sensible defaults when possible
3. ✅ **Validate Input**: Use validation blocks for critical variables
4. ✅ **Mark Sensitive**: Use `sensitive = true` for secrets
5. ✅ **Type Constraints**: Always specify variable types
6. ✅ **Document**: Keep this documentation updated

## Security Considerations

### Never Commit Secrets

Add to `.gitignore`:

```
*.tfvars
*.tfvars.json
.terraform/
terraform.tfstate*
```

### Use Secure Storage

- Use environment variables for CI/CD
- Use AWS Secrets Manager or similar
- Use Terraform Cloud for remote state
- Use GitHub Secrets for GitHub Actions

### Example: Secure Token Usage

```bash
# Set token from secure storage
export TF_VAR_github_token=$(aws secretsmanager get-secret-value \
  --secret-id github-token \
  --query SecretString \
  --output text)

terraform apply
```

## Related Files

- [main.tf](main.md) - Main configuration that uses these variables
- [outputs.tf](outputs.md) - Output values
- [terraform.tfvars.example] - Example variable file (if exists)

## Standards Compliance

This file follows [Terraform File Standards](../policy/terraform-file-standards.md):

- ✅ Copyright header (GPL-3.0-or-later)
- ✅ FILE INFORMATION section
- ✅ file_metadata locals block
- ✅ Version 04.00.03

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Comprehensive variable documentation |
| 04.00.02 | 2026-02-20 | Additional validation rules |
| 04.00.01 | 2026-02-19 | Initial structured variables |

## See Also

- [Terraform Variable Documentation](https://www.terraform.io/language/values/variables)
- [Terraform File Standards](../policy/terraform-file-standards.md)
- [Main Configuration](main.md)
