# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Terraform.Main
# INGROUP: MokoStandards.Configuration
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /terraform/main.tf
# VERSION: 04.00.03
# BRIEF: Main Terraform configuration for MokoStandards repository schemas

# Terraform configuration for MokoStandards repository schemas
# This replaces the legacy XML/JSON schema system with Terraform-based configuration

locals {
  # Standard metadata for this terraform file
  file_metadata = {
    name              = "MokoStandards Main Terraform Configuration"
    description       = "Primary terraform file that orchestrates repository schema definitions"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    file_type         = "main"
    terraform_version = ">= 1.0"
  }
  
  # Configuration metadata
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "MokoStandards Repository Schemas"
    description       = "Terraform configuration for repository structure schemas and type definitions"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "standards"
    format            = "terraform"
    enterprise_ready  = true
    monitoring_enabled = true
    audit_logging     = true
  }
}

terraform {
  required_version = ">= 1.0"
}

# Load repository type definitions
module "default_repository" {
  source = "./repository-types"
}

# Output combined configuration
output "repository_schemas" {
  description = "All repository structure schemas"
  value       = module.default_repository
}
