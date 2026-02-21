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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Terraform
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/workflows/terraform/index.md
VERSION: 04.00.03
BRIEF: Documentation index for Terraform workflow templates
-->

# Terraform Workflow Templates

## Purpose

This directory contains GitHub Actions workflow templates specifically designed for Terraform infrastructure-as-code projects. These workflows provide automated validation, deployment, security scanning, and drift detection for Terraform configurations.

## Available Templates

### ci.yml
**Terraform Continuous Integration**
- Validates Terraform configuration syntax and formatting
- Runs `terraform fmt -check` to ensure code style compliance
- Executes `terraform validate` to verify configuration correctness
- Generates Terraform plans for multiple environments
- Posts plan results as PR comments
- Includes security scanning with tfsec and Checkov
- Runs on push to main branches and pull requests

**Features:**
- Multi-environment plan generation (dev, staging, prod)
- Automated PR comments with validation results
- Security scanning integration
- SARIF report upload for security findings

### deploy.yml.template
**Terraform Infrastructure Deployment**
- Manual workflow dispatch for controlled deployments
- Supports multiple cloud providers (AWS, Azure, GCP)
- Environment-specific deployments with variable files
- Workspace management for environment isolation
- Plan artifact uploads for audit trail
- Production deployment protection with manual approval
- Infrastructure state output capture

**Features:**
- Choice of actions: plan, apply, destroy
- Auto-approve option (use cautiously, not for production)
- OIDC authentication support
- Environment protection rules
- Deployment summaries and issue comments

### drift-detection.yml.template
**Terraform Drift Detection**
- Scheduled drift detection (daily by default)
- Compares actual infrastructure state to Terraform configuration
- Automatically creates issues when drift is detected
- Updates existing drift issues with new findings
- Auto-closes issues when drift is resolved
- Supports manual triggering for specific environments

**Features:**
- Scheduled runs via cron
- Per-environment drift monitoring
- Automatic issue management
- Detailed drift reports in issues
- Resolution tracking

## Infrastructure Definition

### Supported Cloud Providers

**AWS (Amazon Web Services)**
- OIDC authentication with `aws-actions/configure-aws-credentials@v4`
- S3 backend for state storage
- IAM role-based access

**Azure (Microsoft Azure)**
- Service principal authentication
- Azure Storage backend for state

**GCP (Google Cloud Platform)**
- Workload Identity Federation
- GCS backend for state storage

### Environment Structure

Terraform workflows expect the following directory structure:

```
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── environments/
│   │   ├── dev.tfvars
│   │   ├── staging.tfvars
│   │   └── prod.tfvars
│   └── modules/
│       └── ...
```

### Required Secrets

Configure these secrets in your repository:

**For AWS:**
- `AWS_ROLE_ARN` - IAM role ARN for OIDC authentication
- `TF_STATE_BUCKET` - S3 bucket for Terraform state (can be variable)

**For Azure:**
- `AZURE_CREDENTIALS` - Service principal credentials JSON

**For GCP:**
- `GCP_WORKLOAD_IDENTITY_PROVIDER` - Workload identity provider
- `GCP_SERVICE_ACCOUNT` - Service account email

### Required Variables

- `CLOUD_PROVIDER` - Cloud provider name (aws, azure, gcp)
- `AWS_REGION` - AWS region for deployments (default: us-east-1)
- `TF_STATE_BUCKET` - Terraform state storage bucket name

## Usage

### Setting Up CI

1. Copy `ci.yml` to `.github/workflows/terraform-ci.yml`
2. Update `TF_VERSION` to your Terraform version
3. Update `TF_WORKING_DIR` to your Terraform directory
4. Configure cloud provider authentication
5. Commit and push - CI will run automatically

### Deploying Infrastructure

1. Copy `deploy.yml.template` to `.github/workflows/terraform-deploy.yml`
2. Configure required secrets and variables
3. Set up GitHub environments (dev, staging, prod)
4. Add protection rules for production environment
5. Trigger via GitHub Actions UI:
   - Select environment
   - Choose action (plan/apply/destroy)
   - Optionally auto-approve (not recommended for prod)

### Monitoring Drift

1. Copy `drift-detection.yml.template` to `.github/workflows/terraform-drift.yml`
2. Configure authentication and environments
3. Adjust schedule as needed (default: daily at 2 AM UTC)
4. Issues will be created automatically when drift is detected

## Security Scanning

### tfsec
- Static analysis of Terraform code
- Identifies security misconfigurations
- Checks against AWS, Azure, GCP best practices
- Soft fail option allows warnings without blocking

### Checkov
- Policy-as-code security scanning
- Over 1000 built-in checks
- SARIF output for GitHub Security tab
- Covers multiple cloud providers

## Best Practices

### State Management
- Always use remote state (S3, Azure Storage, GCS)
- Enable state locking to prevent concurrent modifications
- Use separate state files per environment
- Regular state backups

### Environment Management
- Use Terraform workspaces for environment isolation
- Separate variable files per environment (`.tfvars`)
- Environment-specific state file keys
- GitHub environment protection rules for production

### Security
- Use OIDC for authentication (avoid long-lived credentials)
- Store sensitive values in GitHub Secrets
- Regular security scanning with tfsec and Checkov
- Review plans before applying
- Enable drift detection

### Workflow Configuration
- Pin Terraform version for consistency
- Use `terraform_wrapper: false` for plan output capture
- Enable PR comments for visibility
- Upload plan artifacts for audit trail
- Implement manual approval for production

## Customization

### Adjusting Environments
Modify the environment matrix in workflows:

```yaml
strategy:
  matrix:
    environment: [dev, staging, prod, qa]  # Add/remove as needed
```

### Changing Terraform Version
Update the `TF_VERSION` environment variable:

```yaml
env:
  TF_VERSION: '1.7.0'  # Update to desired version
```

### Custom Backend Configuration
Modify the `terraform init` step:

```yaml
- name: Terraform Init
  run: |
    terraform init \
      -backend-config="key=${{ matrix.environment }}/terraform.tfstate" \
      -backend-config="bucket=my-state-bucket" \
      -backend-config="dynamodb_table=my-lock-table"
```

## Troubleshooting

### Plan Fails with Authentication Error
- Verify cloud provider credentials are configured
- Check OIDC trust relationship (AWS)
- Verify service principal permissions (Azure)
- Confirm workload identity setup (GCP)

### Drift Detection False Positives
- Review excluded resource types
- Check for timestamp fields causing drift
- Consider using `lifecycle { ignore_changes = [...] }`
- Verify state is up-to-date

### State Lock Conflicts
- Check for running workflows
- Verify state locking is enabled
- Manually unlock if needed (use cautiously)
- Review DynamoDB table for locks (AWS)

## Related Documentation

- [Terraform Documentation](https://www.terraform.io/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [tfsec Documentation](https://aquasecurity.github.io/tfsec/)
- [Checkov Documentation](https://www.checkov.io/)

## Metadata

| Field          | Value                                                                 |
| -------------- | --------------------------------------------------------------------- |
| Document Type  | Index                                                                 |
| Domain         | Infrastructure                                                        |
| Applies To     | All Repositories                                                      |
| Jurisdiction   | Tennessee, USA                                                        |
| Owner          | Moko Consulting                                                       |
| Repo           | https://github.com/mokoconsulting-tech/MokoStandards                  |
| Path           | /templates/workflows/terraform/index.md                               |
| Version        | 01.00.00                                                              |
| Status         | Active                                                                |
| Last Reviewed  | 2026-01-28                                                            |
| Reviewed By    | MokoStandards Team                                                    |

## Revision History

| Date       | Author              | Change                                      | Notes                                          |
| ---------- | ------------------- | ------------------------------------------- | ---------------------------------------------- |
| 2026-01-28 | MokoStandards Team  | Created Terraform workflow templates        | Initial CI, deploy, and drift detection        |
