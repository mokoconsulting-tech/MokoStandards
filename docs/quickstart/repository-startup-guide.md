# Repository Startup Guide for Organization Repositories

## Purpose

This guide provides step-by-step instructions for creating and configuring new repositories within the `mokoconsulting-tech` organization that comply with MokoStandards requirements. It covers initial setup, required documentation, structure creation, and GitHub configuration.

## Scope

This guide applies to:

- New repositories in the `mokoconsulting-tech` organization
- All repository types: Generic, Joomla (WaaS), and Dolibarr (CRM)
- Repository administrators and maintainers
- Developers setting up new projects

This guide does not apply to:

- External repositories outside the organization
- Temporary or experimental repositories
- Fork repositories (different process)

## Prerequisites

Before starting, ensure you have:

- [ ] GitHub organization member access
- [ ] Permission to create repositories in `mokoconsulting-tech` organization
- [ ] Git installed locally (`git --version`)
- [ ] Access to MokoStandards repository
- [ ] Decided on repository type (Generic, Joomla, or Dolibarr)
- [ ] Repository name following naming conventions
- [ ] Project description prepared

## Quick Start

Choose your repository type:

- **[Generic Repository Setup](#generic-repository-setup)** - For libraries, tools, and general projects
- **[Joomla Repository Setup](#joomla-repository-setup)** - For WaaS components and plugins
- **[Dolibarr Repository Setup](#dolibarr-repository-setup)** - For CRM modules

## Generic Repository Setup

### Step 1: Create Repository on GitHub

1. Navigate to https://github.com/organizations/mokoconsulting-tech/repositories/new
2. Configure repository settings:
   - **Name**: Use lowercase with hyphens (e.g., `moko-library-name`)
   - **Description**: Clear, concise project description
   - **Visibility**: Select appropriate visibility (usually Private for org repos)
   - **Initialize**: ✅ Check "Add a README file"
   - **Add .gitignore**: Select appropriate template (Node, Python, etc.)
   - **Choose a license**: Select "GNU General Public License v3.0"
3. Click "Create repository"

### Step 2: Clone Repository Locally

```bash
# Clone the repository
git clone https://github.com/mokoconsulting-tech/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

# Set up git user (if not already configured)
git config user.name "Your Name"
git config user.email "your.email@mokoconsulting.tech"
```

### Step 3: Add Required Documentation

```bash
# Ensure you have MokoStandards repository cloned
# If not: git clone https://github.com/mokoconsulting-tech/MokoStandards.git ~/MokoStandards

# Copy required templates
cp ~/MokoStandards/templates/docs/required/template-CHANGELOG.md ./CHANGELOG.md
cp ~/MokoStandards/templates/docs/required/template-CONTRIBUTING.md ./CONTRIBUTING.md
cp ~/MokoStandards/templates/docs/required/template-SECURITY.md ./SECURITY.md
cp ~/MokoStandards/templates/docs/required/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Copy LICENSE from authoritative source (no extension!)
cp ~/MokoStandards/templates/licenses/GPL-3.0 ./LICENSE

# Copy configuration files
cp ~/MokoStandards/.editorconfig ./
cp ~/MokoStandards/.gitattributes ./

# Update .gitignore if needed (GitHub created one already)
# Optionally merge with MokoStandards template
# cat ~/MokoStandards/templates/configs/.gitignore.generic >> .gitignore
```

### Step 4: Create Required Directory Structure

```bash
# Create required directories for all repository types
mkdir -p docs
mkdir -p scripts
mkdir -p src
mkdir -p .github/workflows

# Optional: Create tests directory if your project needs testing infrastructure
# mkdir -p tests/unit

# Create index files
cat > docs/index.md << 'EOF'
# Documentation Index

## Purpose

Project documentation directory.

## Contents

- Technical documentation
- API documentation (if applicable)
- Architecture diagrams
EOF

cat > scripts/index.md << 'EOF'
# Scripts Index

## Purpose

Build, automation, and utility scripts.

## Contents

- Build scripts
- Deployment scripts
- Maintenance utilities
EOF
```

### Step 5: Customize Documentation

Edit each file to replace placeholders:

```bash
# Edit README.md (GitHub already created this)
# - Replace placeholder content with actual project information
# - Add installation instructions
# - Add usage examples

# Edit CHANGELOG.md
# - Update with initial version 01.00.00
# - Document initial release

# Edit CONTRIBUTING.md
# - Customize contribution guidelines
# - Add project-specific requirements

# Edit SECURITY.md
# - Update supported versions
# - Customize security contact information

# Edit CODE_OF_CONDUCT.md
# - Update contact email
```

**Example CHANGELOG.md entry:**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [01.00.00] - 2026-01-16

### Added
- Initial repository setup
- Basic project structure
- Required documentation
```

### Step 6: Commit Initial Structure

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial repository setup with MokoStandards compliance

- Add required documentation (CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT)
- Add configuration files (.editorconfig, .gitattributes)
- Create required directory structure (docs/, scripts/)
- Add documentation index files"

# Push to GitHub
git push origin main
```

### Step 7: Configure GitHub Settings

1. **Branch Protection** (Settings → Branches → Add rule):
   - Branch name pattern: `main`
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

2. **Enable Security Features** (Settings → Security):
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Secret scanning

3. **Add Topics** (Repository home → ⚙️ Settings icon next to About):
   - Add relevant topics (e.g., `mokostandards`, `typescript`, `library`)

4. **Create Initial GitHub Workflows** (Optional but recommended):

```bash
mkdir -p .github/workflows

# Copy universal build workflow
cp ~/MokoStandards/templates/workflows/build-universal.yml.template .github/workflows/build.yml

# Copy security workflows
cp ~/MokoStandards/templates/workflows/generic/codeql-analysis.yml .github/workflows/
cp ~/MokoStandards/templates/workflows/generic/dependency-review.yml.template .github/workflows/dependency-review.yml
cp ~/MokoStandards/templates/workflows/standards-compliance.yml.template .github/workflows/standards-compliance.yml

# Commit workflows
git add .github/
git commit -m "Add GitHub Actions workflows for CI/CD"
git push origin main
```

### Step 8: Validate Setup

```bash
# Check required files present
ls -la README.md LICENSE CHANGELOG.md CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md .editorconfig .gitattributes .gitignore

# Check required directories
ls -d docs scripts

# Optional: Check tests directory if you created it
# ls -d tests

# Verify GitHub workflows (if added)
ls -la .github/workflows/
```

**Success Checklist:**
- [ ] All required files present
- [ ] All required directories created
- [ ] Documentation customized (no template placeholders)
- [ ] Initial commit pushed to main branch
- [ ] Branch protection rules configured
- [ ] Security features enabled
- [ ] Repository topics added

## Joomla Repository Setup

### Step 1: Create Repository on GitHub

Follow [Generic Repository Setup - Step 1](#step-1-create-repository-on-github)

### Step 2: Clone and Set Up Base Structure

```bash
# Clone the repository
git clone https://github.com/mokoconsulting-tech/YOUR-COMPONENT-NAME.git
cd YOUR-COMPONENT-NAME

# Set up git user (if not already configured)
git config user.name "Your Name"
git config user.email "your.email@mokoconsulting.tech"
```

### Step 3: Add Required Documentation

```bash
# Copy all required templates
cp ~/MokoStandards/templates/docs/required/template-CHANGELOG.md ./CHANGELOG.md
cp ~/MokoStandards/templates/docs/required/template-CONTRIBUTING.md ./CONTRIBUTING.md
cp ~/MokoStandards/templates/docs/required/template-SECURITY.md ./SECURITY.md
cp ~/MokoStandards/templates/docs/required/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Copy configuration files
cp ~/MokoStandards/.editorconfig ./
cp ~/MokoStandards/.gitattributes ./

# Copy Joomla-specific .gitignore
cp ~/MokoStandards/templates/configs/.gitignore.joomla ./.gitignore

# Copy Makefile for Joomla
cp ~/MokoStandards/Makefiles/Makefile.joomla ./Makefile
```

### Step 4: Create Joomla Directory Structure

```bash
# Create site (frontend) structure
mkdir -p site/controllers
mkdir -p site/models
mkdir -p site/views
mkdir -p site/helpers

# Create admin (backend) structure
mkdir -p admin/controllers
mkdir -p admin/models
mkdir -p admin/views
mkdir -p admin/sql/install
mkdir -p admin/sql/updates/mysql

# Create media structure
mkdir -p media/css
mkdir -p media/js
mkdir -p media/images

# Create language structure
mkdir -p language/en-GB

# Create documentation and scripts
mkdir -p docs
mkdir -p scripts/build
mkdir -p scripts/validate

# Create tests structure
mkdir -p tests/unit
mkdir -p tests/integration
```

### Step 5: Create Required Joomla Files

```bash
# Create site controller
cat > site/controller.php << 'EOF'
<?php
/**
 * Component Site Controller
 *
 * @package     YourComponent
 * @subpackage  Site
 * @copyright   Copyright (C) 2026 Moko Consulting
 * @license     GPL-3.0-or-later
 */

defined('_JEXEC') or die;

use Joomla\CMS\MVC\Controller\BaseController;

/**
 * Component Site Controller
 */
class YourComponentController extends BaseController
{
    /**
     * The default view.
     *
     * @var    string
     */
    protected $default_view = 'main';
}
EOF

# Create admin controller
cat > admin/controller.php << 'EOF'
<?php
/**
 * Component Admin Controller
 *
 * @package     YourComponent
 * @subpackage  Administrator
 * @copyright   Copyright (C) 2026 Moko Consulting
 * @license     GPL-3.0-or-later
 */

defined('_JEXEC') or die;

use Joomla\CMS\MVC\Controller\BaseController;

/**
 * Component Admin Controller
 */
class YourComponentController extends BaseController
{
    /**
     * The default view.
     *
     * @var    string
     */
    protected $default_view = 'dashboard';
}
EOF

# Create component manifest
cat > site/manifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<extension type="component" version="4.0" method="upgrade">
    <name>COM_YOURCOMPONENT</name>
    <author>Moko Consulting</author>
    <creationDate>2026-01-16</creationDate>
    <copyright>Copyright (C) 2026 Moko Consulting</copyright>
    <license>GPL-3.0-or-later</license>
    <authorEmail>hello@mokoconsulting.tech</authorEmail>
    <authorUrl>https://mokoconsulting.tech</authorUrl>
    <version>01.00.00</version>
    <description>COM_YOURCOMPONENT_XML_DESCRIPTION</description>

    <!-- Site files -->
    <files folder="site">
        <filename>controller.php</filename>
        <folder>controllers</folder>
        <folder>models</folder>
        <folder>views</folder>
    </files>

    <!-- Admin files -->
    <administration>
        <files folder="admin">
            <filename>controller.php</filename>
            <folder>controllers</folder>
            <folder>models</folder>
            <folder>views</folder>
            <folder>sql</folder>
        </files>
    </administration>

    <!-- Media files -->
    <media folder="media" destination="com_yourcomponent">
        <folder>css</folder>
        <folder>js</folder>
        <folder>images</folder>
    </media>

    <!-- Language files -->
    <languages folder="language">
        <language tag="en-GB">en-GB/com_yourcomponent.ini</language>
        <language tag="en-GB">en-GB/com_yourcomponent.sys.ini</language>
    </languages>
</extension>
EOF

# Create docs index
cat > docs/index.md << 'EOF'
# Component Documentation

## Purpose

Technical documentation for the Joomla component.

## Contents

- Architecture documentation
- API documentation
- Development guides
- Deployment procedures
EOF
```

### Step 6: Customize Files

```bash
# Edit Makefile - Update configuration section at top
# - Set component name
# - Set version number
# - Update paths if needed

# Edit manifest.xml - Replace placeholders
# - Change "yourcomponent" to actual component name
# - Update version number
# - Update descriptions

# Edit controller files
# - Update class names
# - Update component name references

# Customize all documentation files (README, CHANGELOG, etc.)
```

### Step 7: Commit Initial Structure

```bash
git add .
git commit -m "Initial Joomla component structure with MokoStandards compliance

- Add required documentation and configuration files
- Create Joomla site and admin directory structure
- Add component manifest and controllers
- Set up media, language, and test directories
- Add Makefile for build automation"

git push origin main
```

### Step 8: Configure GitHub and Validate

Follow [Generic Repository Setup - Step 7 & 8](#step-7-configure-github-settings)

**Joomla-Specific Success Checklist:**
- [ ] site/ and admin/ directories created
- [ ] Component controllers present (site/controller.php, admin/controller.php)
- [ ] Component manifest present (site/manifest.xml)
- [ ] language/ directory created
- [ ] media/ directory structure created
- [ ] Makefile configured for Joomla
- [ ] tests/unit/ directory present

## Dolibarr Repository Setup

### Step 1: Create Repository on GitHub

Follow [Generic Repository Setup - Step 1](#step-1-create-repository-on-github)

### Step 2: Clone and Set Up Base Structure

```bash
# Clone the repository
git clone https://github.com/mokoconsulting-tech/YOUR-MODULE-NAME.git
cd YOUR-MODULE-NAME

# Set up git user (if not already configured)
git config user.name "Your Name"
git config user.email "your.email@mokoconsulting.tech"
```

### Step 3: Add Required Documentation

```bash
# Copy all required templates (CODE_OF_CONDUCT is suggested for Dolibarr)
cp ~/MokoStandards/templates/docs/required/template-CHANGELOG.md ./CHANGELOG.md
cp ~/MokoStandards/templates/docs/required/template-CONTRIBUTING.md ./CONTRIBUTING.md
cp ~/MokoStandards/templates/docs/required/template-SECURITY.md ./SECURITY.md

# Optional: Add CODE_OF_CONDUCT
cp ~/MokoStandards/templates/docs/required/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Copy configuration files
cp ~/MokoStandards/.editorconfig ./
cp ~/MokoStandards/.gitattributes ./
cp ~/MokoStandards/templates/configs/.gitignore.dolibarr ./.gitignore

# Copy Makefile for Dolibarr
cp ~/MokoStandards/Makefiles/Makefile.dolibarr ./Makefile
```

### Step 4: Create Dolibarr Directory Structure

```bash
# Create source structure
mkdir -p src/core/modules
mkdir -p src/langs/en_US
mkdir -p src/class
mkdir -p src/lib
mkdir -p src/sql

# Optional directories (add as needed)
mkdir -p src/css
mkdir -p src/js
mkdir -p src/img

# Create documentation and scripts
mkdir -p docs
mkdir -p scripts/build
mkdir -p scripts/validate

# Create tests structure
mkdir -p tests/unit
mkdir -p tests/integration

# Create templates (optional)
mkdir -p templates
```

### Step 5: Create Required Dolibarr Files

```bash
# Create src/README.md (end-user documentation)
cat > src/README.md << 'EOF'
# Your Module Name

## For End Users

This module provides [MODULE FUNCTIONALITY DESCRIPTION].

### Installation

1. Navigate to Home → Setup → Modules/Applications
2. Find "Your Module Name" in the list
3. Click "Activate"

### Configuration

After activation, configure the module:
1. Go to Home → Setup → Modules/Applications
2. Click on the module settings icon
3. Configure as needed

### Usage

[USAGE INSTRUCTIONS]

### Support

For support, contact: hello@mokoconsulting.tech

## Version

Current version: 01.00.00

See CHANGELOG.md for version history.
EOF

# Create module descriptor
cat > src/core/modules/modYourModule.class.php << 'EOF'
<?php
/**
 * Module Descriptor Class
 *
 * @package     YourModule
 * @copyright   Copyright (C) 2026 Moko Consulting
 * @license     GPL-3.0-or-later
 */

require_once DOL_DOCUMENT_ROOT.'/core/modules/DolibarrModules.class.php';

/**
 * Module descriptor class
 */
class modYourModule extends DolibarrModules
{
    /**
     * Constructor
     *
     * @param DoliDB $db Database handler
     */
    public function __construct($db)
    {
        global $langs, $conf;

        $this->db = $db;
        $this->numero = 500000; // TODO: Get official number
        $this->rights_class = 'yourmodule';
        
        // Module family
        $this->family = "mokoconsulting";
        $this->familyinfo = array(
            'mokoconsulting' => array(
                'position' => '01',
                'label'    => $langs->trans("Moko Consulting")
            )
        );
        
        $this->module_position = '90';
        $this->name = preg_replace('/^mod/i', '', get_class($this));
        $this->description = "Your module description";
        $this->descriptionlong = "Extended module description";
        
        // Author
        $this->editor_name = 'Moko Consulting';
        $this->editor_url = 'https://www.mokoconsulting.tech';
        $this->editor_squarred_logo = 'logo.png@<module>';
        
        $this->version = '01.00.00';
        $this->const_name = 'MAIN_MODULE_'.strtoupper($this->name);
        $this->picto = 'generic';

        // Dependencies
        $this->depends = array();
        $this->requiredby = array();
        $this->conflictwith = array();

        // Language files
        $this->langfiles = array("yourmodule@yourmodule");

        // Config pages
        $this->config_page_url = array("setup.php@yourmodule");

        // Constants
        $this->const = array();

        // Boxes
        $this->boxes = array();

        // Permissions
        $this->rights = array();

        // Menus
        $this->menu = array();
    }
}
EOF

# Create language file
cat > src/langs/en_US/yourmodule.lang << 'EOF'
# Dolibarr language file - Source file is en_US - yourmodule
CHARSET=UTF-8

# Module
Module500000Name=Your Module Name
Module500000Desc=Your module description

# Permissions
Permission500001=Read module data
Permission500002=Create/modify module data
Permission500003=Delete module data
EOF

# Create docs index
cat > docs/index.md << 'EOF'
# Module Documentation

## Purpose

Technical documentation for the Dolibarr module.

## Contents

- Architecture documentation
- API documentation
- Development guides
- Database schema
EOF
```

### Step 6: Customize Files

```bash
# Edit Makefile - Update configuration section
# - Set module name
# - Set version number
# - Update paths if needed

# Edit modYourModule.class.php
# - Update class name to match your module
# - Get official module number (not 500000)
# - Update descriptions
# - Configure dependencies
# - Add permissions
# - Add menu items

# Edit language file
# - Update module number
# - Add all language strings

# Customize all documentation files
```

### Step 7: Commit Initial Structure

```bash
git add .
git commit -m "Initial Dolibarr module structure with MokoStandards compliance

- Add required documentation and configuration files
- Create Dolibarr src directory structure
- Add module descriptor and language files
- Set up tests and documentation directories
- Add Makefile for build automation"

git push origin main
```

### Step 8: Configure GitHub and Validate

Follow [Generic Repository Setup - Step 7 & 8](#step-7-configure-github-settings)

**Dolibarr-Specific Success Checklist:**
- [ ] src/ directory structure created
- [ ] src/README.md present (end-user documentation)
- [ ] Module descriptor present (src/core/modules/modYourModule.class.php)
- [ ] src/core/ and src/langs/ directories created
- [ ] Language files present
- [ ] Makefile configured for Dolibarr
- [ ] tests/unit/ directory present

## Post-Setup Activities

### Add to Organization Project Board

1. Navigate to organization Projects: https://github.com/orgs/mokoconsulting-tech/projects
2. Find "Repository Health" or appropriate project board
3. Add your repository to the project
4. Set initial status (e.g., "In Development")

### Configure Repository Variables and Secrets

If your repository requires specific variables or secrets:

1. Navigate to Settings → Secrets and variables → Actions
2. Add repository-specific secrets (API keys, credentials, etc.)
3. Use organization-level secrets when possible

### Set Up Continuous Integration

1. Verify workflows are running (Actions tab)
2. Fix any failing workflows
3. Ensure all required status checks pass
4. Configure required status checks in branch protection

### Create Initial Issues

Create tracking issues for:

- [ ] Complete documentation
- [ ] Add comprehensive tests
- [ ] Set up deployment pipeline
- [ ] Create user guides
- [ ] Add API documentation (if applicable)

## Common Issues and Solutions

### Issue: "Permission denied" when pushing

**Solution:**
```bash
# Verify you have correct access
gh auth status

# Re-authenticate if needed
gh auth login

# Verify remote URL is correct
git remote -v

# Update remote URL if using HTTPS
git remote set-url origin https://github.com/mokoconsulting-tech/YOUR-REPO-NAME.git
```

### Issue: Files not copied correctly

**Solution:**
```bash
# Ensure MokoStandards path is correct
ls ~/MokoStandards/templates/docs/required/

# If path is different, update commands
# For example, if MokoStandards is in a different location:
export MOKO_STANDARDS_PATH="/path/to/MokoStandards"
cp $MOKO_STANDARDS_PATH/templates/docs/required/template-README.md ./README.md
```

### Issue: Build workflow fails immediately

**Solution:**
```bash
# Check if Makefile is properly configured
cat Makefile | head -20

# Verify file structure matches expected layout
# For Joomla: Check site/ and admin/ exist
ls -la site/ admin/

# For Dolibarr: Check src/core/ exists
ls -la src/core/

# Review workflow logs in GitHub Actions tab
```

### Issue: Standards compliance check fails

**Solution:**
```bash
# Run local validation (if validation scripts available)
python3 ~/MokoStandards/scripts/validate/validate_structure.py

# Check for missing required files
ls -la README.md LICENSE CHANGELOG.md CONTRIBUTING.md SECURITY.md

# Verify file headers follow standards
head -30 your-file.php
```

## Quick Reference

### Required Files - All Repository Types

- ✅ README.md
- ✅ LICENSE (no extension - use `LICENSE`, not `LICENSE.md`)
- ✅ CHANGELOG.md
- ✅ CONTRIBUTING.md
- ✅ SECURITY.md
- ✅ .gitignore
- ✅ .gitattributes
- ✅ .editorconfig
- ✅ docs/
- ✅ scripts/

### Additional Required - Joomla

- ✅ CODE_OF_CONDUCT.md
- ✅ Makefile
- ✅ site/controller.php
- ✅ site/manifest.xml
- ✅ admin/controller.php
- ✅ language/
- ✅ tests/unit/

### Additional Required - Dolibarr

- ✅ Makefile
- ✅ src/README.md
- ✅ src/core/modules/mod{Name}.class.php
- ✅ src/core/
- ✅ src/langs/
- ✅ tests/unit/

### One-Line Setup Commands

**Generic Repository:**
```bash
# Clone and setup generic repository
git clone https://github.com/mokoconsulting-tech/YOUR-REPO.git && \
  cd YOUR-REPO && \
  mkdir -p docs scripts tests && \
  cp ~/MokoStandards/templates/docs/required/*.md ./ && \
  cp ~/MokoStandards/.editorconfig ~/MokoStandards/.gitattributes ./
```

**Joomla Repository:**
```bash
# Clone and setup Joomla repository
git clone https://github.com/mokoconsulting-tech/YOUR-REPO.git && \
  cd YOUR-REPO && \
  mkdir -p site/{controllers,models,views} \
           admin/{controllers,models,views,sql} \
           media/{css,js,images} \
           language docs scripts tests/unit && \
  cp ~/MokoStandards/templates/docs/required/*.md ./ && \
  cp ~/MokoStandards/Makefiles/Makefile.joomla ./Makefile && \
  cp ~/MokoStandards/.editorconfig ~/MokoStandards/.gitattributes ./
```

**Dolibarr Repository:**
```bash
# Clone and setup Dolibarr repository
git clone https://github.com/mokoconsulting-tech/YOUR-REPO.git && \
  cd YOUR-REPO && \
  mkdir -p src/{core/modules,langs,class,lib,sql} \
           docs scripts tests/unit && \
  cp ~/MokoStandards/templates/docs/required/template-{CHANGELOG,CONTRIBUTING,SECURITY}.md ./ && \
  cp ~/MokoStandards/Makefiles/Makefile.dolibarr ./Makefile && \
  cp ~/MokoStandards/.editorconfig ~/MokoStandards/.gitattributes ./ && \
  touch src/README.md
```

## Related Documentation

- [Layered Documentation Guide](/docs/guide/layered-documentation.md) - Complete file requirements by repository type
- [Repository Organization Guide](/docs/guide/repository-organization.md) - Golden architecture and structure
- [Repository Health Scoring](/docs/policy/health-scoring.md) - How repositories are scored
- [File Header Standards](/docs/policy/file-header-standards.md) - Required file headers
- [Workflow Standards](/docs/policy/workflow-standards.md) - GitHub Actions standards
- [Branching Strategy](/docs/policy/branching-strategy.md) - Git branching model

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/quickstart/repository-startup-guide.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
