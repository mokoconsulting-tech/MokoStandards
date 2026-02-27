/**
 * API/Microservices Project Template
 * Standard project configuration for API and microservices development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "API/Microservices Project"
      description = "Standard project template for API and microservices development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "api"
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
        name        = "API Type"
        type        = "single_select"
        description = "API architecture style"
        options     = ["REST", "GraphQL", "gRPC", "WebSocket", "SOAP", "Event-Driven", "Hybrid"]
      },
      {
        name        = "API Version"
        type        = "text"
        description = "Current API version (e.g., v1, v2, 1.2.3)"
      },
      {
        name        = "Service Type"
        type        = "single_select"
        description = "Microservice category"
        options     = ["Gateway", "BFF (Backend for Frontend)", "Core Service", "Data Service", "Auth Service", "Notification Service", "Integration Service", "Monolith", "Other"]
      },
      {
        name        = "Authentication"
        type        = "single_select"
        description = "Authentication mechanism"
        options     = ["OAuth 2.0", "JWT", "API Key", "Basic Auth", "mTLS", "SAML", "Multiple", "None"]
      },
      {
        name        = "Documentation"
        type        = "single_select"
        description = "API documentation format"
        options     = ["OpenAPI/Swagger", "GraphQL Schema", "Postman Collection", "AsyncAPI", "RAML", "API Blueprint", "Custom", "None"]
      },
      {
        name        = "Health Check"
        type        = "single_select"
        description = "Health check endpoint status"
        options     = ["Implemented", "Partial", "None"]
      },
      {
        name        = "Monitoring"
        type        = "single_select"
        description = "Monitoring and observability"
        options     = ["Prometheus + Grafana", "Datadog", "New Relic", "App Insights", "CloudWatch", "ELK Stack", "Multiple", "None"]
      },
      {
        name        = "Container Runtime"
        type        = "single_select"
        description = "Containerization platform"
        options     = ["Docker", "Kubernetes", "Docker + Kubernetes", "Serverless", "VM Only", "Bare Metal"]
      },
      {
        name        = "Breaking Change"
        type        = "single_select"
        description = "Does this include breaking changes?"
        options     = ["Yes - Major", "Yes - Minor", "No"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "API Type", "Service Type", "Assignee"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Endpoint Tracker"
        type        = "table"
        description = "API endpoints and services inventory"
        columns     = ["Title", "API Type", "Service Type", "API Version", "Authentication", "Status"]
      },
      {
        name        = "Breaking Changes Tracker"
        type        = "table"
        description = "Breaking API changes management"
        filter = {
          field    = "Breaking Change"
          operator = "not_equals"
          value    = "No"
        }
        columns = ["Title", "Breaking Change", "API Version", "Target Version", "Status"]
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
        name    = "Breaking change alert"
        trigger = "field_changed"
        field   = "Breaking Change"
        condition = {
          operator = "in"
          values   = ["Yes - Major", "Yes - Minor"]
        }
        actions = [
          {
            add_label = "breaking-change"
            notify    = "api_team"
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

output "api_project_config" {
  description = "API/Microservices project template configuration"
  value       = local.project_config
}
