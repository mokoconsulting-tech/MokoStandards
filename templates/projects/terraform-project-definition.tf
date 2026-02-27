/**
 * Terraform/Infrastructure Project Template
 * Standard project configuration for Infrastructure as Code using Terraform
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Terraform/Infrastructure Project"
      description = "Standard project template for Infrastructure as Code using Terraform"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "terraform"
    }

    custom_fields = [
      {
        name        = "Status"
        type        = "single_select"
        description = "Current lifecycle state of the task"
        options     = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done", "Blocked", "Cancelled"]
      },
      {
        name        = "Priority"
        type        = "single_select"
        description = "Urgency and importance of the task"
        options     = ["Critical", "High", "Medium", "Low"]
      },
      {
        name        = "Size/Effort"
        type        = "single_select"
        description = "Estimated complexity and work effort"
        options     = ["XS - 1-2 hours", "S - 2-4 hours", "M - 1-2 days", "L - 3-5 days", "XL - 1-2 weeks", "XXL - 2+ weeks"]
      },
      {
        name        = "Sprint"
        type        = "text"
        description = "Sprint or iteration identifier"
      },
      {
        name        = "Target Version"
        type        = "text"
        description = "Target release version (semantic versioning)"
      },
      {
        name        = "Blocked Reason"
        type        = "text"
        description = "Description of what is blocking progress"
      },
      {
        name        = "Acceptance Criteria"
        type        = "text"
        description = "List of criteria for task completion"
      },
      {
        name        = "Terraform Version"
        type        = "single_select"
        description = "Terraform version required"
        options     = ["1.5.x", "1.6.x", "1.7.x", "1.8.x", "Latest"]
      },
      {
        name        = "Cloud Provider"
        type        = "single_select"
        description = "Primary cloud provider"
        options     = ["AWS", "Azure", "GCP", "DigitalOcean", "Linode", "Oracle Cloud", "IBM Cloud", "Multi-Cloud", "On-Premise"]
      },
      {
        name        = "Region/Zone"
        type        = "text"
        description = "Cloud region or availability zone"
      },
      {
        name        = "Environment"
        type        = "single_select"
        description = "Infrastructure environment"
        options     = ["Development", "Staging", "Production", "DR (Disaster Recovery)", "Testing", "Sandbox"]
      },
      {
        name        = "State Backend"
        type        = "single_select"
        description = "Terraform state storage"
        options     = ["S3", "Azure Blob", "GCS", "Terraform Cloud", "Consul", "etcd", "Local", "Other"]
      },
      {
        name        = "Infrastructure Type"
        type        = "single_select"
        description = "Type of infrastructure resources"
        options     = ["Compute", "Network", "Storage", "Database", "Security", "Monitoring", "CI/CD", "Mixed"]
      },
      {
        name        = "Cost Impact"
        type        = "single_select"
        description = "Estimated monthly cost impact"
        options     = ["None", "< $100", "$100-500", "$500-2K", "$2K-10K", "> $10K", "Unknown"]
      },
      {
        name        = "Deployment Status"
        type        = "single_select"
        description = "Current deployment state"
        options     = ["Not Deployed", "Plan Generated", "Plan Approved", "Applying", "Applied", "Failed", "Destroyed"]
      },
      {
        name        = "Requires Approval"
        type        = "single_select"
        description = "Does this require manual approval?"
        options     = ["Yes - Security", "Yes - Cost", "Yes - Production", "No"]
      },
      {
        name        = "Has Compliance"
        type        = "single_select"
        description = "Compliance requirements applicable"
        options     = ["SOC 2", "HIPAA", "PCI-DSS", "GDPR", "ISO 27001", "Multiple", "None"]
      },
      {
        name        = "Module Registry"
        type        = "single_select"
        description = "Uses Terraform module registry?"
        options     = ["Public Registry", "Private Registry", "Git Modules", "Local Modules", "Mixed"]
      },
      {
        name        = "Last Plan Date"
        type        = "text"
        description = "Date of last terraform plan"
      },
      {
        name        = "Last Apply Date"
        type        = "text"
        description = "Date of last terraform apply"
      },
      {
        name        = "Drift Detection"
        type        = "single_select"
        description = "Infrastructure drift status"
        options     = ["No Drift", "Minor Drift", "Major Drift", "Unknown", "Not Checked"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Environment", "Cloud Provider", "Assignee"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Sprint Board"
        type        = "board"
        description = "Current sprint work board"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "equals"
          value    = "current"
        }
        columns = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done"]
      },
      {
        name        = "Release Roadmap"
        type        = "roadmap"
        description = "Timeline view of planned releases"
        group_by    = "Target Version"
        date_field  = "Target Date"
      },
      {
        name        = "Blocked Items"
        type        = "table"
        description = "Tasks currently blocked"
        filter = {
          field    = "Status"
          operator = "equals"
          value    = "Blocked"
        }
        columns = ["Title", "Priority", "Blocked Reason", "Assignee", "Days Blocked"]
      },
      {
        name        = "Infrastructure State Tracker"
        type        = "table"
        description = "Deployment status by environment"
        group_by    = "Environment"
        columns     = ["Title", "Environment", "Deployment Status", "Last Apply Date", "Cloud Provider", "Drift Detection"]
      },
      {
        name        = "Deployment Pipeline"
        type        = "board"
        description = "Infrastructure deployment workflow"
        group_by    = "Deployment Status"
        columns     = ["Not Deployed", "Plan Generated", "Plan Approved", "Applying", "Applied"]
      },
      {
        name        = "Cost Management"
        type        = "table"
        description = "Cost impact overview"
        columns     = ["Title", "Cost Impact", "Environment", "Infrastructure Type", "Status", "Assignee"]
        sort = [
          {
            field     = "Cost Impact"
            direction = "desc"
          }
        ]
      },
      {
        name        = "Compliance Tracker"
        type        = "table"
        description = "Compliance requirements tracking"
        filter = {
          field    = "Has Compliance"
          operator = "not_equals"
          value    = "None"
        }
        columns = ["Title", "Has Compliance", "Environment", "Requires Approval", "Status"]
      },
      {
        name        = "Drift Detection Dashboard"
        type        = "table"
        description = "Infrastructure drift monitoring"
        filter = {
          field    = "Drift Detection"
          operator = "in"
          values   = ["Minor Drift", "Major Drift"]
        }
        columns = ["Title", "Drift Detection", "Environment", "Last Plan Date", "Assignee"]
      },
    ]

    workflows = [
      {
        name    = "Auto-status on PR"
        trigger = "pull_request_opened"
        actions = [
          {
            set_field = "Status"
            value     = "In Review"
          }
        ]
      },
      {
        name    = "Auto-status on merge"
        trigger = "pull_request_merged"
        actions = [
          {
            set_field = "Status"
            value     = "Testing"
          },
          {
            set_field = "Deployment Status"
            value     = "Plan Generated"
          }
        ]
      },
      {
        name    = "High cost alert"
        trigger = "field_changed"
        field   = "Cost Impact"
        condition = {
          operator = "in"
          values   = ["$2K-10K", "> $10K"]
        }
        actions = [
          {
            add_label = "high-cost"
            notify    = "finance_team"
          }
        ]
      },
      {
        name    = "Production deployment alert"
        trigger = "field_changed"
        field   = "Deployment Status"
        condition = {
          operator    = "equals"
          value       = "Applied"
          environment = "Production"
        }
        actions = [
          {
            notify    = "ops_team"
            add_label = "production-change"
          }
        ]
      },
      {
        name    = "Drift detection alert"
        trigger = "field_changed"
        field   = "Drift Detection"
        condition = {
          operator = "equals"
          value    = "Major Drift"
        }
        actions = [
          {
            add_label = "drift-detected"
            notify    = "ops_team"
          }
        ]
      },
    ]

    metadata = {
      version = "1.0.0"
      created = "2026-02-27"
      author  = "Moko Consulting"
      license = "GPL-3.0-or-later"
    }
  }
}

output "terraform_project_config" {
  description = "Terraform/Infrastructure project template configuration"
  value       = local.project_config
}
