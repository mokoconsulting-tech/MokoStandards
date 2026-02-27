/**
 * Generic Development Project Template
 * Standard project configuration for multi-language software development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Generic Development Project"
      description = "Standard project template for multi-language software development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "generic"
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
        name        = "Technology Stack"
        type        = "text"
        description = "Primary languages and frameworks used"
      },
      {
        name        = "Environment"
        type        = "single_select"
        description = "Target deployment environment"
        options     = ["Development", "Staging", "Production", "All"]
      },
      {
        name        = "Release Channel"
        type        = "single_select"
        description = "Software release maturity level"
        options     = ["Alpha", "Beta", "RC", "Stable", "LTS"]
      },
      {
        name        = "API Version"
        type        = "text"
        description = "API version number if applicable"
      },
      {
        name        = "Deployment Status"
        type        = "single_select"
        description = "Current deployment state"
        options     = ["Not Deployed", "Deploying", "Deployed", "Failed", "Rollback", "N/A"]
      },
      {
        name        = "Infrastructure"
        type        = "single_select"
        description = "Hosting infrastructure type"
        options     = ["On-Premise", "Cloud", "Hybrid", "Serverless", "N/A"]
      },
      {
        name        = "Database Type"
        type        = "single_select"
        description = "Primary database technology"
        options     = ["MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Multiple", "None"]
      },
      {
        name        = "Has Tests"
        type        = "single_select"
        description = "Does this task include automated tests?"
        options     = ["Yes", "No", "N/A"]
      },
      {
        name        = "Test Coverage"
        type        = "text"
        description = "Code coverage percentage if applicable"
      },
      {
        name        = "Security Review"
        type        = "single_select"
        description = "Has security review been completed?"
        options     = ["Not Started", "In Progress", "Completed", "Not Required"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Assignees", "Sprint", "Technology Stack", "Environment"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          },
          {
            field     = "Status"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Sprint Board"
        type        = "board"
        description = "Kanban board for current sprint"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "is_not_empty"
          value    = ""
        }
        columns = ["Title", "Priority", "Size/Effort", "Assignees", "Technology Stack"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Release Roadmap"
        type        = "roadmap"
        description = "Timeline view of releases"
        group_by    = "Target Version"
        filter = {
          field    = "Status"
          operator = "not_equals"
          value    = "Cancelled"
        }
        columns = ["Title", "Status", "Priority", "Release Channel"]
        sort = [
          {
            field     = "Target Version"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Blocked Items"
        type        = "table"
        description = "All blocked items"
        filter = {
          field    = "Status"
          operator = "equals"
          value    = "Blocked"
        }
        columns = ["Title", "Priority", "Blocked Reason", "Assignees", "Sprint"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Deployment Pipeline"
        type        = "board"
        description = "Track deployment progress"
        group_by    = "Deployment Status"
        columns     = ["Title", "Environment", "Target Version", "Assignees"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Technology Stack View"
        type        = "table"
        description = "Overview by technology"
        group_by    = "Technology Stack"
        columns     = ["Title", "Status", "Database Type", "Infrastructure"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
    ]

    workflows = [
      {
        name    = "Auto-status on PR creation"
        trigger = "pull_request_opened"
        actions = [
          {
            set_field = "Status"
            value     = "In Review"
          }
        ]
      },
      {
        name    = "Auto-status on PR merge"
        trigger = "pull_request_merged"
        actions = [
          {
            set_field = "Status"
            value     = "Testing"
          }
        ]
      },
      {
        name    = "Deployment status sync"
        trigger = "deployment_success"
        actions = [
          {
            set_field = "Deployment Status"
            value     = "Deployed"
          }
        ]
      },
      {
        name    = "Failed deployment alert"
        trigger = "deployment_failure"
        actions = [
          {
            set_field = "Deployment Status"
            value     = "Failed"
          },
          {
            add_label = "deployment-failed"
          },
          {
            notify = "assignees"
          }
        ]
      },
    ]

    metadata = {
      version = "1.0.0"
      created = "2026-01-04"
      author  = "Moko Consulting"
      license = "GPL-3.0-or-later"
    }
  }
}

output "generic_project_config" {
  description = "Generic Development project template configuration"
  value       = local.project_config
}
