# Development Server Deployment

Automated deployment of `src` directory to development server via FTP/SFTP.

## Overview

The dev deployment workflow automatically pushes code changes to a development server when:
- A pull request is merged to `main`, `master`, `develop`, `dev`, or `development` branches
- Code is directly pushed to these branches
- Manually triggered via workflow dispatch

## Configuration

### Organization Secrets (Required)

Set these secrets at the organization level:

- **`DEV_FTP_HOST`**: Development server hostname (e.g., `dev.example.com`)
- **`DEV_FTP_USER`**: FTP/SFTP username
- **`DEV_FTP_PASSWORD`**: FTP/SFTP password (optional if using SSH key)
- **`DEV_FTP_PATH`**: Base deployment path (e.g., `/var/www/html`)

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

Run the deployment script directly:

```bash
# Using password authentication
python scripts/release/deploy_to_dev.py \
  --host dev.example.com \
  --user myuser \
  --password mypassword \
  --remote-path /var/www/html/myapp \
  --local-path src \
  --protocol sftp

# Using SSH key authentication
python scripts/release/deploy_to_dev.py \
  --host dev.example.com \
  --user myuser \
  --key-file ~/.ssh/id_rsa \
  --remote-path /var/www/html/myapp \
  --local-path src \
  --protocol sftp \
  --port 22
```

## Examples

### Example 1: Basic SFTP Deployment

**Organization Secrets:**
```
DEV_FTP_HOST=dev.example.com
DEV_FTP_USER=deployuser
DEV_FTP_KEY=<ssh-private-key>
DEV_FTP_PATH=/var/www/html
```

**Repository Variable:**
```
DEV_FTP_PATH_SUFFIX=/my-dolibarr-module
```

**Result:** Files from `src/` deployed to `/var/www/html/my-dolibarr-module/`

### Example 2: FTP Deployment

**Organization Secrets:**
```
DEV_FTP_HOST=ftp.example.com
DEV_FTP_USER=ftpuser
DEV_FTP_PASSWORD=secretpass
DEV_FTP_PATH=/public_html
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

1. **Use SFTP** when possible for encrypted transfers
2. **SSH Keys** are preferred over passwords
3. **Organization Secrets** ensure credentials are shared securely across repositories
4. **Repository Variables** allow per-project customization without exposing secrets

## Troubleshooting

### Missing Configuration Error

```
Error: Missing required secret: DEV_FTP_HOST
```

**Solution:** Ensure all required organization secrets are set.

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
