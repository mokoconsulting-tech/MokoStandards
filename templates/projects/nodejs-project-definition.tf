/**
 * Node.js/TypeScript Project Template
 * Standard project configuration for Node.js and TypeScript application development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Node.js/TypeScript Project"
      description = "Standard project template for Node.js and TypeScript application development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "nodejs"
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
        name        = "Node Version"
        type        = "single_select"
        description = "Minimum Node.js version required"
        options     = ["16 LTS", "18 LTS", "20 LTS", "21 Current", "22 Current"]
      },
      {
        name        = "TypeScript"
        type        = "single_select"
        description = "Is this a TypeScript project?"
        options     = ["Yes", "No", "Mixed"]
      },
      {
        name        = "Package Manager"
        type        = "single_select"
        description = "Node package manager used"
        options     = ["npm", "yarn", "pnpm", "bun"]
      },
      {
        name        = "Framework"
        type        = "single_select"
        description = "Primary Node.js framework"
        options     = ["Express", "NestJS", "Fastify", "Koa", "Next.js", "Nuxt", "React", "Vue", "Angular", "None", "Other"]
      },
      {
        name        = "Runtime Environment"
        type        = "single_select"
        description = "JavaScript runtime platform"
        options     = ["Node.js", "Deno", "Bun", "Browser", "Multiple"]
      },
      {
        name        = "Build Tool"
        type        = "single_select"
        description = "Build and bundling tool"
        options     = ["Webpack", "Vite", "esbuild", "Rollup", "Parcel", "tsup", "None"]
      },
      {
        name        = "Test Framework"
        type        = "single_select"
        description = "Testing framework used"
        options     = ["Jest", "Vitest", "Mocha", "AVA", "Playwright", "Cypress", "None", "Multiple"]
      },
      {
        name        = "Package Status"
        type        = "single_select"
        description = "NPM publication status"
        options     = ["Not Published", "Private Package", "Public Package", "In Review", "Deprecated"]
      },
      {
        name        = "Package Name"
        type        = "text"
        description = "NPM package name (e.g., @org/package-name)"
      },
      {
        name        = "Package Version"
        type        = "text"
        description = "Current package version (semantic versioning)"
      },
      {
        name        = "ESM/CommonJS"
        type        = "single_select"
        description = "Module system used"
        options     = ["ESM Only", "CommonJS Only", "Dual (ESM+CJS)", "UMD"]
      },
      {
        name        = "Dependency Audit"
        type        = "single_select"
        description = "Security audit status"
        options     = ["Pass", "Warnings", "Vulnerabilities", "Critical", "Not Run"]
      },
      {
        name        = "License Type"
        type        = "single_select"
        description = "Software license"
        options     = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC", "Proprietary", "Other"]
      },
      {
        name        = "Has Types"
        type        = "single_select"
        description = "TypeScript type definitions included?"
        options     = ["Yes - Native", "Yes - @types", "No", "N/A"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Assignee", "Sprint", "Framework"]
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
        name        = "Dependency Audit Dashboard"
        type        = "table"
        description = "Security audit status overview"
        columns     = ["Title", "Package Name", "Package Version", "Dependency Audit", "Node Version", "Assignee"]
        filter = {
          field    = "Dependency Audit"
          operator = "not_equals"
          value    = "Pass"
        }
      },
      {
        name        = "Package Pipeline"
        type        = "board"
        description = "NPM publication workflow"
        group_by    = "Package Status"
        columns     = ["Not Published", "Private Package", "In Review", "Public Package"]
      },
      {
        name        = "Framework Distribution"
        type        = "table"
        description = "Projects by framework"
        group_by    = "Framework"
        columns     = ["Title", "Framework", "Node Version", "TypeScript", "Status"]
      },
      {
        name        = "Type Coverage Tracker"
        type        = "table"
        description = "TypeScript adoption and type coverage"
        filter = {
          field    = "TypeScript"
          operator = "not_equals"
          value    = "No"
        }
        columns = ["Title", "TypeScript", "Has Types", "Package Name", "Status"]
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
          }
        ]
      },
      {
        name    = "Auto-status on close"
        trigger = "pull_request_closed"
        actions = [
          {
            set_field = "Status"
            value     = "Cancelled"
          }
        ]
      },
      {
        name    = "Version bump notification"
        trigger = "field_changed"
        field   = "Package Version"
        actions = [
          {
            notify  = "team"
            message = "Package version updated"
          }
        ]
      },
      {
        name    = "Security alert"
        trigger = "field_changed"
        field   = "Dependency Audit"
        condition = {
          operator = "in"
          values   = ["Vulnerabilities", "Critical"]
        }
        actions = [
          {
            notify    = "security_team"
            add_label = "security"
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

output "nodejs_project_config" {
  description = "Node.js/TypeScript project template configuration"
  value       = local.project_config
}
