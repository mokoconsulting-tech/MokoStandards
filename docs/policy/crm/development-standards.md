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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.CRM
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/crm/development-standards.md
VERSION: 03.00.00
BRIEF: Development standards for MokoCRM based on Dolibarr platform
-->

# MokoCRM Development Standards

## Purpose

This policy establishes development standards for MokoCRM, Moko Consulting's customer relationship management platform based on the Dolibarr ERP/CRM framework. It defines coding conventions, module development requirements, customization guidelines, and quality standards specific to the Dolibarr ecosystem.

## Scope

This policy applies to:

- All MokoCRM custom modules and extensions
- Dolibarr core customizations
- MokoCRM API integrations
- Database schema modifications
- Custom workflows and business logic
- UI/UX customizations
- Third-party module integration

This policy does not apply to:

- Dolibarr core framework code (unless creating patches)
- Standard Dolibarr modules without modifications
- Infrastructure configuration (covered by operations policies)

## Responsibilities

### CRM Development Lead

Accountable for:

- Defining CRM development standards
- Approving module architecture
- Reviewing major customizations
- Ensuring Dolibarr compatibility
- Managing technical debt

### CRM Developers

Responsible for:

- Following development standards
- Writing maintainable custom modules
- Testing customizations thoroughly
- Documenting code and configurations
- Maintaining upgrade compatibility

### QA Team

Responsible for:

- Testing custom modules
- Validating upgrade compatibility
- Verifying performance impact
- Ensuring data integrity
- Documenting test results

## Dolibarr Architecture Overview

### Platform Characteristics

**Framework**: Dolibarr ERP/CRM
**Language**: PHP 7.4+
**Database**: MySQL 5.7+ / MariaDB 10.3+
**Architecture**: Modular, MVC-inspired
**License**: GPL-3.0-or-later

### MokoCRM Structure

```
htdocs/
├── custom/                    # Custom modules directory
│   ├── moko*/                # Moko-prefixed custom modules
│   ├── custom_integrations/  # Third-party integrations
│   └── custom_workflows/     # Business logic customizations
├── conf/                     # Configuration files
│   └── conf.php             # Main configuration
└── dolibarr/                # Core Dolibarr files (do not modify)
```

## Module Development Standards

### Module Naming Convention

**All custom modules MUST use "moko" prefix:**

```
mokocrm_[feature]
mokoinvoice_automation
mokokpi_dashboard
mokoworkflow_approval
```

**Rationale**:
- Clear identification of custom vs core modules
- Namespace isolation
- Upgrade safety
- Easier maintenance

### Module Family

**All custom modules MUST use "mokoconsulting" as the module family with proper family info:**

```php
// Module family
$this->family = "mokoconsulting";
$this->familyinfo = array(
    'mokoconsulting' => array(
        'position' => '01',
        'label'    => $langs->trans("Moko Consulting")
    )
);

// Author
$this->editor_name = 'Moko Consulting';
$this->editor_url = 'https://www.mokoconsulting.tech';
$this->editor_squarred_logo = 'logo.png@<module>';
```

**Rationale**:
- Groups all Moko custom modules together in the Dolibarr module manager
- Provides clear branding and identification
- Separates custom modules from standard Dolibarr module families
- Improves user experience when browsing modules

**Standard Dolibarr module families:**
- "products" - Product/service management
- "crm" - CRM and sales
- "financial" - Accounting and finance
- "hr" - Human resources
- "projects" - Project management
- "mokoconsulting" - **Our custom module family**

### Module Structure

**Standard Dolibarr module structure:**

```
htdocs/custom/mokomodule/
├── admin/                    # Module configuration pages
│   ├── setup.php            # Module settings
│   └── about.php            # Module information
├── class/                    # PHP classes
│   ├── mokoobject.class.php # Main object class
│   └── api_mokomodule.class.php # API endpoints
├── core/                     # Core module files
│   ├── modules/             # Numbering modules
│   ├── triggers/            # Event triggers
│   └── boxes/               # Dashboard widgets
├── css/                      # Custom stylesheets
├── img/                      # Module images/icons
├── js/                       # JavaScript files
├── langs/                    # Translations
│   └── en_US/
│       └── mokomodule.lang
├── lib/                      # Library functions
│   └── mokomodule.lib.php
├── sql/                      # Database scripts
│   ├── llx_mokomodule.sql   # Table creation
│   └── llx_mokomodule.key.sql # Indexes and keys
├── mokomoduleindex.php      # Module main page
└── core/
    └── modules/
        └── modMokoModule.class.php # Module descriptor
```

### Module Descriptor

**Every module MUST have a descriptor class:**

```php
<?php
// htdocs/custom/mokomodule/core/modules/modMokoModule.class.php

dol_include_once('/core/modules/DolibarrModules.class.php');

class modMokoModule extends DolibarrModules
{
    public function __construct($db)
    {
        global $langs, $conf;
        
        $this->db = $db;
        
        // Module identification
        $this->numero = 185051; // Unique ID (Moko Consulting reserved: 185051-185099)
        $this->rights_class = 'mokomodule';
        
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
        $this->description = "MokoCRM custom module description";
        
        // Author
        $this->editor_name = 'Moko Consulting';
        $this->editor_url = 'https://www.mokoconsulting.tech';
        $this->editor_squarred_logo = 'logo.png@mokomodule';
        
        // Version
        $this->version = '1.0.0';
        $this->const_name = 'MAIN_MODULE_'.strtoupper($this->name);
        
        // Dependencies
        $this->depends = array('modUser', 'modSociete');
        $this->requiredby = array();
        
        // Config pages
        $this->config_page_url = array('setup.php@mokomodule');
        
        // Constants to add
        $this->const = array();
        
        // Boxes
        $this->boxes = array();
        
        // Permissions
        $this->rights = array();
        $r = 0;
        
        $r++;
        $this->rights[$r][0] = $this->numero + $r;
        $this->rights[$r][1] = 'Read MokoModule objects';
        $this->rights[$r][3] = 0;
        $this->rights[$r][4] = 'read';
        
        // Database tables
        $this->dictionaries = array();
    }
}
```

### Module Number Registry

**Reserved Module Numbers**:

Dolibarr module numbers **185051 to 185099** are reserved for Moko Consulting use.

**Dolibarr Extensions Registry**:

| Module Name | Module Number | Status | Description | Repository |
|-------------|---------------|--------|-------------|------------|
| MokoDoliTools | 185051 | Active | Core utilities and admin toolkit for Dolibarr with curated defaults, UI enhancements, and entity-aware operations | [mokoconsulting-tech/MokoDoliTools](https://github.com/mokoconsulting-tech/MokoDoliTools) |
| MokoDoliSign | 185052 | Reserved | Digital signature and document signing module | TBD |
| MokoCRMTheme | 185053 | Reserved | MokoCRM Theme | TBD |
| MokoDoliChimp | 185054 | Reserved | MailChimp integration for Dolibarr | TBD |
| MokoDoliPasskey | 185055 | Reserved | WebAuthn/Passkey authentication module for Dolibarr | TBD |
| MokoDoliForm | 185056 | Reserved | Advanced form builder and workflow module for Dolibarr | TBD |
| MokoDoliG | 185057 | Reserved | Google Workspace integration module for Dolibarr | TBD |
| MokoDoliDeploy | 185058 | Reserved | Deployment automation and management module for Dolibarr | TBD |
| MokoDoliMulti | 185059 | Reserved | Multi-entity management module for Dolibarr | TBD |
| MokoDoliHRM | 185060 | Reserved | Human Resource Management module for Dolibarr | TBD |
| MokoDoliAuth | 185061 | Reserved |  | TBD |
| MokoDoliOffline | 185062 | Reserved |  | TBD |
| MokoDoliReleaseHelper | 185063 | Reserved | Release management and version control helper module for Dolibarr | TBD |
| Available for Assignment | 185064-185099 | Reserved | Reserved for future Moko Consulting modules | - |

**Module ID Reservation Process**:

To reserve a Dolibarr module ID from the Moko Consulting range (185051-185099):

1. **Create a Pull Request** to this repository
2. **Update this table** with:
   - Module name
   - Next available module number from the reserved range
   - Status: "Reserved"
   - Brief description of the module's purpose
   - Repository link (use "TBD" if not yet created)
3. **Get approval** from the CRM Development Lead before merging
4. **Merge the PR** to officially reserve the module ID

**Important**: Module IDs MUST be reserved through a pull request. Direct commits to reserve module IDs are not permitted and are blocked on protected branches via branch protection rules (requiring PRs, code review, and automated checks) for the default and release branches.

### Database Standards

**Table Naming**:
- Use `llx_` prefix (Dolibarr standard)
- Add full module prefix after: `llx_mokocrm_workflow_tablename`
- Use lowercase with underscores
- Example: `llx_mokocrm_workflow_tasks`

**Required Columns**:
```sql
CREATE TABLE llx_mokocrm_example (
  rowid INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  entity INT(11) DEFAULT 1 NOT NULL,
  
  -- Audit fields (required)
  datec DATETIME NOT NULL,
  tms TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  fk_user_creat INT(11),
  fk_user_modif INT(11),
  
  -- Custom fields
  ref VARCHAR(30) NOT NULL,
  label VARCHAR(255),
  description TEXT,
  
  -- Status
  status SMALLINT DEFAULT 0 NOT NULL,
  
  -- Soft delete
  import_key VARCHAR(14)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

**Indexes**:
```sql
ALTER TABLE llx_mokocrm_example ADD INDEX idx_mokocrm_example_entity (entity);
ALTER TABLE llx_mokocrm_example ADD INDEX idx_mokocrm_example_ref (ref);
ALTER TABLE llx_mokocrm_example ADD UNIQUE INDEX uk_mokocrm_example_ref (ref, entity);
```

### PHP Coding Standards

**Follow Dolibarr coding standards:**

```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 */

/**
 * \file       mokomodule/class/mokoobject.class.php
 * \ingroup    mokomodule
 * \brief      File for MokoObject class
 */

require_once DOL_DOCUMENT_ROOT.'/core/class/commonobject.class.php';

/**
 * MokoObject class
 */
class MokoObject extends CommonObject
{
    /**
     * @var string ID to identify managed object
     */
    public $element = 'mokoobject';
    
    /**
     * @var string Name of table without prefix
     */
    public $table_element = 'moko_object';
    
    /**
     * @var int Ref field ID
     */
    public $fk_element = 'fk_mokoobject';
    
    /**
     * @var string Module part for upload dir
     */
    public $picto = 'mokomodule@mokomodule';
    
    /**
     * Constructor
     *
     * @param DoliDB $db Database handler
     */
    public function __construct($db)
    {
        $this->db = $db;
    }
    
    /**
     * Create object in database
     *
     * @param  User $user User creating object
     * @param  int  $notrigger 1=Disable triggers
     * @return int  <0 if KO, >0 if OK
     */
    public function create($user, $notrigger = 0)
    {
        global $conf;
        
        $error = 0;
        
        // Clean parameters
        $this->ref = trim($this->ref);
        
        $this->db->begin();
        
        $sql = "INSERT INTO ".MAIN_DB_PREFIX.$this->table_element;
        $sql .= " (entity, ref, label, datec, fk_user_creat)";
        $sql .= " VALUES (";
        $sql .= " ".((int) $conf->entity).",";
        $sql .= " '".$this->db->escape($this->ref)."',";
        $sql .= " '".$this->db->escape($this->label)."',";
        $sql .= " '".$this->db->idate(dol_now())."',";
        $sql .= " ".((int) $user->id);
        $sql .= ")";
        
        dol_syslog(__METHOD__, LOG_DEBUG);
        $resql = $this->db->query($sql);
        
        if ($resql) {
            $this->id = $this->db->last_insert_id(MAIN_DB_PREFIX.$this->table_element);
            
            if (!$error && !$notrigger) {
                // Call trigger
                $result = $this->call_trigger('MOKOOBJECT_CREATE', $user);
                if ($result < 0) {
                    $error++;
                }
            }
            
            if (!$error) {
                $this->db->commit();
                return $this->id;
            } else {
                $this->db->rollback();
                return -1;
            }
        } else {
            $this->error = $this->db->lasterror();
            $this->db->rollback();
            return -1;
        }
    }
}
```

**Key Standards**:
- Use Dolibarr's CommonObject base class
- Implement standard CRUD methods
- Use database transactions
- Call triggers for events
- Log with dol_syslog()
- Escape all SQL parameters
- Follow Dolibarr naming conventions

### API Development

**Create REST API endpoints:**

```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 */

/**
 * \file    mokomodule/class/api_mokomodule.class.php
 * \ingroup mokomodule
 * \brief   REST API for MokoModule
 */

require_once DOL_DOCUMENT_ROOT.'/api/class/api.class.php';
require_once DOL_DOCUMENT_ROOT.'/custom/mokomodule/class/mokoobject.class.php';

/**
 * API class for MokoModule
 *
 * @access protected
 * @class  DolibarrApiAccess {@requires user,external}
 */
class MokoModuleApi extends DolibarrApi
{
    /**
     * @var MokoObject $mokoobject {@type MokoObject}
     */
    public $mokoobject;
    
    /**
     * Constructor
     */
    public function __construct()
    {
        global $db;
        $this->db = $db;
        $this->mokoobject = new MokoObject($this->db);
    }
    
    /**
     * Get properties of a MokoObject
     *
     * @param int $id ID of object
     * @return array|mixed Data without useless information
     *
     * @url GET /mokoobject/{id}
     *
     * @throws RestException 401 Not allowed
     * @throws RestException 404 Not found
     */
    public function get($id)
    {
        if (!DolibarrApiAccess::$user->rights->mokomodule->read) {
            throw new RestException(401);
        }
        
        $result = $this->mokoobject->fetch($id);
        if (!$result) {
            throw new RestException(404, 'MokoObject not found');
        }
        
        if (!DolibarrApi::_checkAccessToResource('mokomodule', $this->mokoobject->id)) {
            throw new RestException(401, 'Access forbidden');
        }
        
        return $this->_cleanObjectDatas($this->mokoobject);
    }
    
    /**
     * Create MokoObject
     *
     * @param array $request_data Request data
     * @return int  ID of created object
     *
     * @url POST /mokoobject
     */
    public function post($request_data = null)
    {
        if (!DolibarrApiAccess::$user->rights->mokomodule->write) {
            throw new RestException(401);
        }
        
        $this->mokoobject->ref = $request_data['ref'];
        $this->mokoobject->label = $request_data['label'];
        
        if ($this->mokoobject->create(DolibarrApiAccess::$user) < 0) {
            throw new RestException(500, 'Error creating object', array_merge(array($this->mokoobject->error), $this->mokoobject->errors));
        }
        
        return $this->mokoobject->id;
    }
}
```

### Trigger Development

**Event-driven customizations:**

```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 */

/**
 * \file    mokomodule/core/triggers/interface_99_modMokoModule_MokoTriggers.class.php
 * \ingroup mokomodule
 * \brief   Trigger file for MokoModule events
 */

require_once DOL_DOCUMENT_ROOT.'/core/triggers/dolibarrtriggers.class.php';

/**
 * Class of triggers for MokoModule
 */
class InterfaceModMokoModuleMokoTriggers extends DolibarrTriggers
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
        
        $this->name = preg_replace('/^Interface/i', '', get_class($this));
        
        // Module family
        $this->family = "mokoconsulting";
        $this->familyinfo = array(
            'mokoconsulting' => array(
                'position' => '01',
                'label'    => $langs->trans("Moko Consulting")
            )
        );
        
        $this->description = "MokoModule triggers";
        $this->version = '1.0.0';
        $this->picto = 'mokomodule@mokomodule';
    }
    
    /**
     * Trigger function
     *
     * @param string $action Event action code
     * @param Object $object Object
     * @param User   $user   User
     * @param Translate $langs Lang object
     * @param conf   $conf   Conf object
     * @return int <0 if KO, 0 if nothing done, >0 if OK
     */
    public function runTrigger($action, $object, User $user, Translate $langs, Conf $conf)
    {
        if (empty($conf->mokomodule->enabled)) {
            return 0;
        }
        
        // Put your code here
        switch ($action) {
            case 'COMPANY_CREATE':
                dol_syslog("Trigger '".$this->name."' for action '$action' launched by ".__FILE__.". id=".$object->id);
                // Custom logic when company is created
                break;
                
            case 'MOKOOBJECT_CREATE':
                dol_syslog("Trigger '".$this->name."' for action '$action' launched by ".__FILE__.". id=".$object->id);
                // Custom logic when MokoObject is created
                break;
                
            default:
                dol_syslog("Trigger '".$this->name."' for action '$action' launched by ".__FILE__.". id=".$object->id);
        }
        
        return 0;
    }
}
```

## Customization Guidelines

### Core Modifications

**NEVER modify Dolibarr core files directly.**

**Alternatives**:
1. Use hooks and triggers
2. Create custom modules
3. Override with custom classes
4. Use extrafields for data
5. Submit patches upstream if core change needed

### Hooks Usage

**Use Dolibarr hooks for UI customization:**

```php
<?php
// In module descriptor, enable hooks
$this->module_parts = array(
    'hooks' => array('thirdpartycard', 'invoicecard')
);

// In custom module, implement hook
function formObjectOptions($parameters, &$object, &$action, $hookmanager)
{
    global $langs;
    
    if (in_array('thirdpartycard', explode(':', $parameters['context']))) {
        print '<tr><td>'.$langs->trans('MokoCustomField').'</td>';
        print '<td>Custom content here</td></tr>';
    }
    
    return 0;
}
```

### Extrafields

**Use extrafields for custom data:**

```php
<?php
// In module descriptor
$this->const = array(
    array(
        'MOKO_EXTRAFIELD_ENABLED',
        'chaine',
        '1',
        'Enable custom extrafields',
        0,
        'current',
        1
    )
);

// Create extrafield programmatically
require_once DOL_DOCUMENT_ROOT.'/core/class/extrafields.class.php';

$extrafields = new ExtraFields($db);
$extrafields->addExtraField(
    'moko_custom_field',
    'Moko Custom Field',
    'varchar',
    1,
    50,
    'thirdparty',
    0,
    0,
    '',
    '',
    1,
    '',
    1
);
```

## Security Standards

### Input Validation

**Always validate and sanitize input:**

```php
<?php
// Use GETPOST() for all user input
$id = GETPOST('id', 'int');
$ref = GETPOST('ref', 'alpha');
$action = GETPOST('action', 'aZ09');

// Validate before use
if (empty($id) || $id <= 0) {
    setEventMessages($langs->trans('ErrorFieldRequired', $langs->transnoentities('Id')), null, 'errors');
    header('Location: index.php');
    exit;
}

// Use restrictedArea() for access control
restrictedArea($user, 'mokomodule', $id, 'moko_object');
```

### Permission Checks

**Always check permissions:**

```php
<?php
// Check module permission
if (!$user->rights->mokomodule->read) {
    accessforbidden();
}

// Check object permission
if (!$user->rights->mokomodule->write) {
    setEventMessages($langs->trans('NotEnoughPermissions'), null, 'errors');
    header('Location: index.php');
    exit;
}
```

### SQL Injection Prevention

**Use prepared statements or escaping:**

```php
<?php
// Use placeholders
$sql = "SELECT * FROM ".MAIN_DB_PREFIX."moko_object";
$sql .= " WHERE entity = ".((int) $conf->entity);
$sql .= " AND ref = '".$db->escape($ref)."'";

// Or use parameterized queries
$sql = "SELECT * FROM ".MAIN_DB_PREFIX."moko_object WHERE rowid = ?";
$resql = $db->query($sql, array($id));
```

## Testing Requirements

### Unit Testing

**Write PHPUnit tests for custom classes:**

```php
<?php
use PHPUnit\Framework\TestCase;

class MokoObjectTest extends TestCase
{
    private $db;
    private $object;
    
    protected function setUp(): void
    {
        global $db;
        $this->db = $db;
        $this->object = new MokoObject($this->db);
    }
    
    public function testCreate()
    {
        global $user;
        
        $this->object->ref = 'TEST001';
        $this->object->label = 'Test Object';
        
        $result = $this->object->create($user);
        
        $this->assertGreaterThan(0, $result);
        $this->assertGreaterThan(0, $this->object->id);
    }
}
```

### Integration Testing

**Test with actual Dolibarr environment:**

- Test module installation/uninstallation
- Test database migrations
- Test API endpoints
- Test permissions
- Test triggers
- Test hooks

### Upgrade Testing

**Test compatibility with Dolibarr upgrades:**

- Test on multiple Dolibarr versions
- Verify database schema compatibility
- Check deprecated function usage
- Validate module still works after upgrade

## Performance Standards

### Database Optimization

- Use indexes on foreign keys and search fields
- Avoid SELECT * queries
- Use JOINs instead of multiple queries
- Implement pagination for large result sets
- Cache frequently accessed data

### Code Optimization

- Use Dolibarr's caching mechanisms
- Minimize database queries
- Lazy load related objects
- Optimize hook implementations
- Profile slow pages

## Documentation Requirements

### Module Documentation

**Every module MUST have**:

1. README.md with installation instructions
2. CHANGELOG.md with version history
3. API documentation if exposing endpoints
4. User guide for custom features
5. Developer guide for customizations

### Code Comments

**Use Dolibarr documentation format:**

```php
/**
 * Calculate total amount
 *
 * @param  float $subtotal Subtotal before tax
 * @param  float $taxrate  Tax rate percentage
 * @return float           Total amount with tax
 */
public function calculateTotal($subtotal, $taxrate)
{
    return $subtotal * (1 + $taxrate / 100);
}
```

## Version Control

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `hotfix/*` - Production fixes
- `release/*` - Release preparation

### Commit Messages

```
feat(mokomodule): add new workflow automation
fix(mokoinvoice): correct tax calculation
docs(mokocrm): update API documentation
refactor(mokoworkflow): simplify approval logic
```

## Deployment Standards

### Module Packaging

**Create distribution package:**

```
mokomodule-1.0.0.zip
├── mokomodule/           # Module files
├── README.md
├── CHANGELOG.md
└── doc/
    └── manual.pdf
```

### Installation Process

1. Extract to htdocs/custom/
2. Enable in Module Setup
3. Run database migrations
4. Configure module settings
5. Set permissions
6. Test functionality

### Automatic Updates Deployment

**All Dolibarr and Joomla extensions MUST use Akeeba Release System (ARS) for automatic updates:**

- **Distribution**: All production releases must be published through Akeeba Release System
- **Update Streams**: Configure proper update streams for stable, beta, and alpha releases
- **Version Management**: Follow semantic versioning (MAJOR.MINOR.PATCH) in ARS releases
- **Download IDs**: Each deployment must use unique download IDs for tracking
- **Update Server**: Extensions must include proper update XML configuration pointing to ARS

**Dolibarr Module Updates**:

Dolibarr modules **MUST** implement a custom update checking mechanism (not via `module_parts`) that:

- Provides an admin page that checks for updates from ARS.
- Parses the update XML from `https://releases.mokoconsulting.tech/dolibarr/updates/mokomodule.xml`.
- Displays an update notification and download link to administrators when a newer version is available.
- Provides manual update instructions or a one-click update, where technically feasible.

Example implementation in an admin page:
```php
// Example: automatic updates for Dolibarr modules using a custom mechanism (not via module_parts).
// Example implementation of update checking mechanism:
// 1. Create an admin page that checks for updates from ARS
// 2. Parse update XML from: https://releases.mokoconsulting.tech/dolibarr/updates/mokomodule.xml
// 3. Display update notification and download link to administrators
$updateXmlUrl = 'https://releases.mokoconsulting.tech/dolibarr/updates/mokomodule.xml';
$latestVersion = $this->checkForUpdates($updateXmlUrl);
if (version_compare($latestVersion, $this->version, '>')) {
    print '<div class="info">Update available: ' . $latestVersion . '</div>';
}
```

**Joomla Extension Updates**:
```xml
<!-- In extension manifest XML -->
<updateservers>
    <server type="extension" priority="1" name="MokoExtension Updates">
        https://releases.mokoconsulting.tech/joomla/updates/mokoextension.xml
    </server>
</updateservers>
```

### User Key Requirements

**All Moko Consulting extensions MUST require a valid user key/license key to function:**

**Implementation Requirements**:

1. **Key Validation**: Extensions must validate user key before enabling functionality
2. **Key Storage**: Store license keys only in encrypted form and only in secure configuration/storage mechanisms; never store them in plain text or alongside their encryption keys.
   - Use AES-256-GCM for at-rest encryption of license keys
   - Encryption keys MUST NOT be stored in the same location as encrypted license keys
   - Use platform-specific secure storage APIs or environment variables for encryption key management
   - Use established cryptographic libraries (OpenSSL, libsodium, or framework-specific APIs)
3. **Grace Period**: Provide 14-day grace period for key entry after installation
4. **Key Format**: Use format `MOKO-PRODUCT-XXXX-XXXX-XXXX`, where `PRODUCT` is the extension code (e.g., `DOLITOOLS`) and each `XXXX` segment is exactly 4 alphanumeric characters (example: `MOKO-DOLITOOLS-A1B2-C3D4-E5F6`)
5. **Validation Endpoint**: Validate keys against `https://license.mokoconsulting.tech/validate`
   - **HTTP Method**: POST
   - **Request Headers**: `Content-Type: application/json`, `X-Extension-Version: {version}`
   - **Request Body**: `{"license_key": "MOKO-...", "domain": "example.com", "installation_id": "..."}`
   - **Success Response**: `{"valid": true, "expires": "2026-12-31", "features": []}`
   - **Error Response**: `{"valid": false, "error": "INVALID_KEY|EXPIRED|DOMAIN_MISMATCH"}`
6. **Offline Mode**: Support offline validation with cached validation results
   - Successful validations are cached for up to 7 consecutive days to allow offline operation
   - If no successful validation occurs within a rolling 7-day period, extensions become non-functional until validation succeeds

**Dolibarr Implementation**:
```php
// In module class
/**
 * Validate license key according to Moko Consulting standards.
 *
 * Requirements:
 * - Enforce key format: MOKO-PRODUCT-XXXX-XXXX-XXXX (4-char alphanumeric segments)
 *   Product code can be variable length (e.g., DOLITOOLS, CRM, FORM)
 * - Call validation endpoint https://license.mokoconsulting.tech/validate via POST
 * - Send JSON body: {"license_key": "...", "domain": "...", "installation_id": "..."}
 * - Cache successful validations for up to 7 consecutive days for offline use
 */
public function validateUserKey($licenseKey)
{
    global $conf;

    // 1) Basic format validation
    // Product code limited to 2-12 characters to prevent abuse
    $pattern = '/^MOKO-[A-Z0-9]{2,12}-(?:[A-Z0-9]{4}-){2}[A-Z0-9]{4}$/';
    if (!preg_match($pattern, $licenseKey)) {
        return false;
    }

    // 2) Determine cache file location (example: module-specific temp directory)
    // Note: Replace '{MODULE_NAME}' with your actual module name for production use
    // Note: In production, consider encrypting cache file contents to prevent information disclosure
    $cacheDir = DOL_DATA_ROOT . '/{MODULE_NAME}';
    if (!is_dir($cacheDir)) {
        dol_mkdir($cacheDir);
    }
    $cacheFile = $cacheDir . '/license_cache.json';

    // 3) Try to use cached validation (offline mode) if endpoint not reachable
    $now = time();
    if (is_readable($cacheFile)) {
        $fileSize = filesize($cacheFile);
        // Validate file size to prevent reading excessively large files
        if ($fileSize > 0 && $fileSize < 10240) { // Max 10KB
            $cacheData = json_decode(file_get_contents($cacheFile), true);
            if (json_last_error() === JSON_ERROR_NONE
                && is_array($cacheData)
                && !empty($cacheData['license_key'])
                && $cacheData['license_key'] === $licenseKey
                && !empty($cacheData['validated_at'])
                && ($now - (int) $cacheData['validated_at']) <= 7 * 24 * 60 * 60
            ) {
                // Cached result still valid (within 7 days)
                return !empty($cacheData['valid']);
            }
        }
    }

    // 4) Online validation against Moko license server
    $domain = (!empty($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : 'cli');
    // Note: dol_hash with length 5 is a Dolibarr convention for installation IDs
    // For production use, consider: bin2hex(random_bytes(16)) or a UUID library for a robust installation ID
    $installationId = !empty($conf->global->MAIN_INSTALL_ID) ? $conf->global->MAIN_INSTALL_ID : dol_hash($domain, 5);

    $payload = json_encode([
        'license_key'      => $licenseKey,
        'domain'           => $domain,
        'installation_id'  => $installationId,
    ]);

    $ch = curl_init('https://license.mokoconsulting.tech/validate');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_HTTPHEADER     => [
            'Content-Type: application/json',
            // Note: Replace DOL_VERSION with your module version constant for production
            'X-Extension-Version: ' . DOL_VERSION,
        ],
        CURLOPT_POSTFIELDS     => $payload,
        CURLOPT_TIMEOUT        => 10,
    ]);

    $responseBody = curl_exec($ch);
    $curlError    = curl_error($ch);
    $httpCode     = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // If request failed, fall back to any still-valid cache (handled above in step 3)
    // If cache was also invalid/missing, we fail closed for security
    if ($responseBody === false || $httpCode !== 200) {
        if (!empty($curlError)) {
            dol_syslog('License validation cURL error: ' . $curlError, LOG_ERR);
        }
        return false;
    }

    $response = json_decode($responseBody, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        dol_syslog('License validation JSON decode error: ' . json_last_error_msg(), LOG_ERR);
        return false;
    }
    $isValid  = is_array($response) && !empty($response['valid']);

    // 5) Update cache for offline mode
    $cachePayload = [
        'license_key'   => $licenseKey,
        'valid'         => $isValid,
        'validated_at'  => $now,
        'raw_response'  => $response,
    ];
    if (file_put_contents($cacheFile, json_encode($cachePayload)) === false) {
        // Log cache write failure but continue (validation already succeeded)
        dol_syslog('Failed to write license validation cache', LOG_WARNING);
    }

    return $isValid;
}

// In module setup page
// Note: Call validateUserKey() before enabling module functionality
if (!$this->validateUserKey($conf->global->MOKOMODULE_LICENSE_KEY)) {
    setEventMessages($langs->trans('InvalidLicenseKey'), null, 'errors');
    // Disable module functionality (implement appropriate checks throughout module)
}
```

**Joomla Implementation**:
```php
// In extension installation script
// Note: Implement validateLicenseKey() in your extension class to:
//   - Enforce key format: MOKO-PRODUCT-XXXX-XXXX-XXXX
//   - Validate keys against https://license.mokoconsulting.tech/validate
//   - Apply the 7-day offline cache/expiry rules defined in this policy
public function preflight($type, $parent) {
    $params = JComponentHelper::getParams('com_mokoextension');
    $licenseKey = $params->get('license_key');
    if (!$this->validateLicenseKey($licenseKey)) {
        throw new RuntimeException('Valid license key required');
    }
}
```

**Key Management**:
- Users obtain keys from Moko Consulting customer portal
- Each deployment requires unique key (no key sharing)
- Keys are tied to domain/installation URL
- Extensions become non-functional if validation fails for 7 consecutive days
- Support team can issue temporary keys for troubleshooting

## Compliance and Governance

### License Compliance

- All custom modules: GPL-3.0-or-later
- Include license headers in all files
- Document third-party dependencies
- Respect Dolibarr's GPL license

### Code Review

- All custom modules require review
- Security review for sensitive operations
- Performance review for database changes
- Documentation review for user-facing features

## Dependencies

This policy depends on:

- [Scripting Standards](../scripting-standards.md) - For automation scripts
- [Security Scanning Policy](../security-scanning.md) - For vulnerability detection
- [Dependency Management](../dependency-management.md) - For third-party modules
- Dolibarr version 14.0+ installed

## Acceptance Criteria

- [ ] All custom modules use "moko" prefix
- [ ] Module descriptors properly configured
- [ ] Database tables follow naming convention
- [ ] All code follows Dolibarr standards
- [ ] Input validation implemented
- [ ] Permission checks in place
- [ ] API endpoints documented
- [ ] Unit tests written
- [ ] Module documentation complete
- [ ] Upgrade compatibility verified

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/crm/development-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
