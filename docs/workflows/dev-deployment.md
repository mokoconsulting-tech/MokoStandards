[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Development Server Deployment

Automated deployment of `src` directory to development server via FTP/SFTP.

## Overview

The dev deployment workflow automatically pushes code changes to a development server when:
- A pull request is merged to `main`, `master`, `develop`, `dev`, or `development` branches
- Code is directly pushed to these branches
- Manually triggered via workflow dispatch

**⚠️ Security Restriction:** Deployment can only be executed by:
- Organization administrators
- Repository administrators (users with `admin` role on the repository)
- Repository maintainers (users with `maintain` role on the repository)

This ensures only authorized personnel can deploy code to the development server.

## Configuration

### Organization Variables (Required)

Set these variables at the organization level:

- **`DEV_FTP_PATH`**: Base deployment path (e.g., `/var/www/html`)

### Organization Secrets (Required)

Set these secrets at the organization level:

- **`DEV_FTP_HOST`**: Development server hostname (e.g., `dev.example.com`)
- **`DEV_FTP_USER`**: FTP/SFTP username
- **`DEV_FTP_PASSWORD`**: FTP/SFTP password (optional if using SSH key)

### Organization Secrets (Optional)

- **`DEV_FTP_KEY`**: SSH private key for SFTP authentication
- **`DEV_FTP_PROTOCOL`**: Transfer protocol - `ftp`, `ftps`, or `sftp` (default: `sftp`)
- **`DEV_FTP_PORT`**: Server port (default: 21 for FTP, 22 for SFTP)

### Repository Variables (Optional)

- **`DEV_FTP_PATH_SUFFIX`**: Path suffix to append to base path
  - Example: `/my-module` → deployed to `/var/www/html/my-module`
  - Useful for multi-project deployments to the same server

## Usage

### Automatic Deployment

The workflow automatically triggers when:

1. **PR Merge**: When a pull request is merged to main/develop branches
   ```yaml
   on:
     pull_request:
       types: [closed]
       branches: [main, develop]
   ```

2. **Direct Push**: When changes are pushed to main/develop branches
   ```yaml
   on:
     push:
       branches: [main, develop]
       paths: ['src/**']
   ```

### Manual Deployment

Trigger manually from GitHub Actions tab:

1. Go to **Actions** → **Deploy to Dev Server**
2. Click **Run workflow**
3. Optionally specify a custom source directory (default: `src`)

### Command Line Deployment

**Note:** The `deploy_to_dev.py` script has been removed. Use the unified release tool or workflows for deployment:

```bash
# Use unified release tool
./scripts/release/unified_release.py release --version 1.2.3

# Or use the reusable deploy workflow
# See .github/workflows/reusable-deploy.yml
```

For advanced deployment scenarios, create a custom workflow that uses the reusable-deploy workflow.

## Examples

### Example 1: Basic SFTP Deployment

**Organization Variables:**
```
DEV_FTP_PATH=/var/www/html
```

**Organization Secrets:**
```
DEV_FTP_HOST=dev.example.com
DEV_FTP_USER=deployuser
DEV_FTP_KEY=<ssh-private-key>
```

**Repository Variable:**
```
DEV_FTP_PATH_SUFFIX=/my-dolibarr-module
```

**Result:** Files from `src/` deployed to `/var/www/html/my-dolibarr-module/`

### Example 2: FTP Deployment

**Organization Variables:**
```
DEV_FTP_PATH=/public_html
```

**Organization Secrets:**
```
DEV_FTP_HOST=ftp.example.com
DEV_FTP_USER=ftpuser
DEV_FTP_PASSWORD=secretpass
DEV_FTP_PROTOCOL=ftp
DEV_FTP_PORT=21
```

**Result:** Files from `src/` deployed to `/public_html/`

### Example 3: Multiple Projects to Same Server

Configure different path suffixes per repository:

**Project A:** `DEV_FTP_PATH_SUFFIX=/project-a`
**Project B:** `DEV_FTP_PATH_SUFFIX=/project-b`

Both deploy to the same server but different directories.

## Security Notes

1. **Access Control**: Only org admins, repo admins, and repo maintainers can deploy to dev server
2. **Variables vs Secrets**: Paths are stored as variables (non-sensitive), credentials as secrets (sensitive)
3. **Use SFTP** when possible for encrypted transfers
4. **SSH Keys** are preferred over passwords
5. **Organization Secrets** ensure credentials are shared securely across repositories
6. **Repository Variables** allow per-project customization without exposing secrets

## Troubleshooting

### Permission Denied

```
Error: Deployment to dev server requires organization admin, repository admin, or repository maintainer permissions
```

**Solution:** Only organization administrators or users with `admin` or `maintain` role on the repository can deploy to the dev server. Contact your organization administrator to request appropriate permissions.

### Missing Configuration Error

```
Error: Missing required variable: DEV_FTP_PATH
```

**Solution:** Ensure all required organization variables and secrets are set.

Variables (non-sensitive):
- `DEV_FTP_PATH` (org variable)
- `DEV_FTP_PATH_SUFFIX` (repo variable, optional)

Secrets (sensitive):
- `DEV_FTP_HOST`, `DEV_FTP_USER`, `DEV_FTP_PASSWORD` or `DEV_FTP_KEY`

### Local Path Does Not Exist

```
Warning: Local path 'src' does not exist. Skipping deployment.
```

**Solution:** This is expected for repositories without a `src` directory. The workflow gracefully skips deployment.

### Connection Refused

```
SFTP deployment failed: [Errno 111] Connection refused
```

**Solution:**
- Check `DEV_FTP_HOST` is correct
- Verify `DEV_FTP_PORT` (default 22 for SFTP)
- Ensure firewall allows connections

### Authentication Failed

```
SFTP deployment failed: Authentication failed
```

**Solution:**
- Verify `DEV_FTP_USER` is correct
- Check `DEV_FTP_PASSWORD` or `DEV_FTP_KEY` is valid
- For SSH keys, ensure the public key is authorized on the server

## Related Documentation

- [Bulk Repository Updates](./bulk-repository-updates.md)
- [Reusable Deploy Workflow](../../.github/workflows/reusable-deploy.yml)
- [Release Pipeline](../../.github/workflows/release_pipeline.yml)

## Version History

| Date       | Version | Author          | Notes                           |
| ---------- | ------- | --------------- | ------------------------------- |
| 2026-01-17 | 01.00.00| Moko Consulting | Initial dev deployment workflow |

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Operations                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/workflows/dev-deployment.md                                      |
| Version        | 04.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.00 with all required fields |
