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
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.CRM
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/crm/dolibarr-development-guide.md
VERSION: 04.00.01
BRIEF: Practical guide for developing custom modules for Dolibarr/MokoCRM
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Dolibarr Development Guide

## Overview

This guide provides practical, step-by-step instructions for developing custom modules for Dolibarr and MokoCRM. It complements the [CRM Development Standards](../../policy/crm/development-standards.md) policy with hands-on examples and tutorials.

## Getting Started

### Development Environment Setup

**Prerequisites**:
- PHP 8.1+ with required extensions
- MySQL 8.0+ or MariaDB 10.4+
- Apache or Nginx web server
- Composer (for dependencies)
- Git (for version control)

**Install Dolibarr locally**:

```bash
# Download Dolibarr
cd /var/www/html
wget https://github.com/Dolibarr/dolibarr/archive/refs/tags/18.0.0.tar.gz
tar -xzf 18.0.0.tar.gz
mv dolibarr-18.0.0 dolibarr

# Set permissions
sudo chown -R www-data:www-data dolibarr/
sudo chmod -R 755 dolibarr/

# Create database
mysql -u root -p <<EOF
CREATE DATABASE dolibarr_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dolibarr'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dolibarr_dev.* TO 'dolibarr'@'localhost';
FLUSH PRIVILEGES;
EOF

# Complete installation via web browser
# Navigate to: http://localhost/dolibarr/htdocs/install/
```

**Configure development tools**:

```bash
# Install PHP CodeSniffer
composer global require "squizlabs/php_codesniffer=*"

# Install Dolibarr coding standards
cd ~/.composer
git clone https://github.com/Dolibarr/dolibarr-standard.git

# Configure phpcs
phpcs --config-set installed_paths ~/.composer/dolibarr-standard
```

## Creating Your First Module

### Module Skeleton

**Create module directory**:

```bash
cd /var/www/html/dolibarr/htdocs/custom
mkdir mokoexample
cd mokoexample
```

**Module structure**:

```
mokoexample/
├── core/
│   ├── modules/
│   │   └── modMokoExample.class.php    # Module descriptor
│   └── boxes/
├── admin/
│   ├── setup.php                        # Module configuration page
│   └── about.php                        # About page
├── class/
│   └── mokoobject.class.php            # Business object class
├── img/
│   └── object_mokoexample.png          # Module icon
├── langs/
│   └── en_US/
│       └── mokoexample.lang            # Translations
├── lib/
│   └── mokoexample.lib.php             # Helper functions
├── sql/
│   ├── llx_mokoexample_object.sql      # Table creation
│   └── llx_mokoexample_object.key.sql  # Indexes and keys
└── README.md
```

### Step 1: Module Descriptor

Create `core/modules/modMokoExample.class.php`:

```php
<?php
/**
 * Module descriptor for MokoExample
 */

require_once DOL_DOCUMENT_ROOT.'/core/modules/DolibarrModules.class.php';

class modMokoExample extends DolibarrModules
{
    public function __construct($db)
    {
        global $langs, $conf;

        $this->db = $db;

        // Module ID - use reserved Moko range 185051-185099
        $this->numero = 185056; // Example number - reserve via PR!

        // Module identification
        $this->rights_class = 'mokoexample';

        // Module family
        $this->family = "mokoconsulting";
        $this->familyinfo = array(
            'mokoconsulting' => array(
                'position' => '01',
                'label'    => $langs->trans("Moko Consulting")
            )
        );

        $this->module_position = '1000';
        $this->name = preg_replace('/^mod/i', '', get_class($this));
        $this->description = "Example Moko module for Dolibarr";
        $this->descriptionlong = "Demonstrates best practices for custom module development";

        // Author
        $this->editor_name = 'Moko Consulting';
        $this->editor_url = 'https://www.mokoconsulting.tech';
        $this->editor_squarred_logo = 'logo.png@mokoexample';

        // Version
        $this->version = '1.0.0';
        $this->const_name = 'MAIN_MODULE_'.strtoupper($this->name);

        // Images
        $this->picto = 'mokoexample@mokoexample';

        // Dependencies
        $this->depends = array();
        $this->requiredby = array();
        $this->conflictwith = array();

        // Language files
        $this->langfiles = array("mokoexample@mokoexample");

        // Config pages
        $this->config_page_url = array("setup.php@mokoexample");

        // Constants
        $this->const = array();

        // Boxes
        $this->boxes = array();

        // Permissions
        $this->rights = array();
        $r = 0;

        $r++;
        $this->rights[$r][0] = $this->numero + $r;
        $this->rights[$r][1] = 'Read MokoExample objects';
        $this->rights[$r][3] = 0;
        $this->rights[$r][4] = 'read';

        $r++;
        $this->rights[$r][0] = $this->numero + $r;
        $this->rights[$r][1] = 'Create/Update MokoExample objects';
        $this->rights[$r][3] = 0;
        $this->rights[$r][4] = 'write';

        $r++;
        $this->rights[$r][0] = $this->numero + $r;
        $this->rights[$r][1] = 'Delete MokoExample objects';
        $this->rights[$r][3] = 0;
        $this->rights[$r][4] = 'delete';

        // Database tables
        $this->dictionaries = array();
    }

    /**
     * Initialize module
     */
    public function init($options = '')
    {
        global $conf, $langs;

        $result = $this->_load_tables('/mokoexample/sql/');
        if ($result < 0) {
            return -1;
        }

        return $this->_init(array(), array());
    }

    /**
     * Remove module
     */
    public function remove($options = '')
    {
        $sql = array();
        return $this->_remove($sql, $options);
    }
}
```

### Step 2: Database Table

Create `sql/llx_mokoexample_object.sql`:

```sql
-- Table for MokoExample objects
CREATE TABLE IF NOT EXISTS llx_mokoexample_object (
  rowid INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  entity INT(11) DEFAULT 1 NOT NULL,

  -- Object identification
  ref VARCHAR(128) NOT NULL,
  label VARCHAR(255) NOT NULL,
  description TEXT,

  -- Status
  status SMALLINT DEFAULT 0 NOT NULL,

  -- Audit fields
  date_creation DATETIME NOT NULL,
  tms TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  fk_user_creat INT(11),
  fk_user_modif INT(11),

  -- Additional fields
  note_public TEXT,
  note_private TEXT,

  -- Foreign keys
  fk_project INT(11),

  UNIQUE KEY uk_mokoexample_ref (ref, entity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Create `sql/llx_mokoexample_object.key.sql`:

```sql
-- Indexes
ALTER TABLE llx_mokoexample_object ADD INDEX idx_mokoexample_entity (entity);
ALTER TABLE llx_mokoexample_object ADD INDEX idx_mokoexample_status (status);
ALTER TABLE llx_mokoexample_object ADD INDEX idx_mokoexample_fk_project (fk_project);
```

### Step 3: Business Object Class

Create `class/mokoobject.class.php`:

```php
<?php
/**
 * MokoObject class
 */

require_once DOL_DOCUMENT_ROOT.'/core/class/commonobject.class.php';

class MokoObject extends CommonObject
{
    public $element = 'mokoobject';
    public $table_element = 'mokoexample_object';
    public $fk_element = 'fk_mokoobject';

    public $ismultientitymanaged = 1;
    public $isextrafieldmanaged = 1;

    // Object fields
    public $ref;
    public $label;
    public $description;
    public $status;
    public $note_public;
    public $note_private;
    public $fk_project;

    // Audit fields
    public $date_creation;
    public $tms;
    public $fk_user_creat;
    public $fk_user_modif;

    /**
     * Constructor
     */
    public function __construct($db)
    {
        $this->db = $db;
    }

    /**
     * Create object in database
     */
    public function create($user, $notrigger = false)
    {
        global $conf;

        $error = 0;

        // Clean parameters
        $this->ref = trim($this->ref);
        $this->label = trim($this->label);

        $this->db->begin();

        // Insert request
        $sql = "INSERT INTO ".MAIN_DB_PREFIX.$this->table_element." (";
        $sql .= "ref,";
        $sql .= "entity,";
        $sql .= "label,";
        $sql .= "description,";
        $sql .= "status,";
        $sql .= "date_creation,";
        $sql .= "fk_user_creat";
        $sql .= ") VALUES (";
        $sql .= " '".$this->db->escape($this->ref)."',";
        $sql .= " ".((int) $conf->entity).",";
        $sql .= " '".$this->db->escape($this->label)."',";
        $sql .= " ".($this->description ? "'".$this->db->escape($this->description)."'" : "null").",";
        $sql .= " ".((int) $this->status).",";
        $sql .= " '".$this->db->idate(dol_now())."',";
        $sql .= " ".((int) $user->id);
        $sql .= ")";

        dol_syslog(get_class($this)."::create", LOG_DEBUG);
        $resql = $this->db->query($sql);

        if (!$resql) {
            $error++;
            $this->errors[] = "Error ".$this->db->lasterror();
        }

        if (!$error) {
            $this->id = $this->db->last_insert_id(MAIN_DB_PREFIX.$this->table_element);

            if (!$notrigger) {
                // Call trigger
                $result = $this->call_trigger('MOKOOBJECT_CREATE', $user);
                if ($result < 0) {
                    $error++;
                }
            }
        }

        if (!$error) {
            $this->db->commit();
            return $this->id;
        } else {
            $this->db->rollback();
            return -1;
        }
    }

    /**
     * Load object from database
     */
    public function fetch($id, $ref = null)
    {
        global $conf;

        $sql = "SELECT";
        $sql .= " t.rowid,";
        $sql .= " t.entity,";
        $sql .= " t.ref,";
        $sql .= " t.label,";
        $sql .= " t.description,";
        $sql .= " t.status,";
        $sql .= " t.date_creation,";
        $sql .= " t.tms,";
        $sql .= " t.fk_user_creat,";
        $sql .= " t.fk_user_modif,";
        $sql .= " t.note_public,";
        $sql .= " t.note_private,";
        $sql .= " t.fk_project";
        $sql .= " FROM ".MAIN_DB_PREFIX.$this->table_element." as t";
        $sql .= " WHERE t.entity IN (".getEntity($this->element).")";

        if (!empty($id)) {
            $sql .= " AND t.rowid = ".((int) $id);
        } elseif (!empty($ref)) {
            $sql .= " AND t.ref = '".$this->db->escape($ref)."'";
        }

        dol_syslog(get_class($this)."::fetch", LOG_DEBUG);
        $resql = $this->db->query($sql);

        if ($resql) {
            if ($this->db->num_rows($resql)) {
                $obj = $this->db->fetch_object($resql);

                $this->id = $obj->rowid;
                $this->entity = $obj->entity;
                $this->ref = $obj->ref;
                $this->label = $obj->label;
                $this->description = $obj->description;
                $this->status = $obj->status;
                $this->date_creation = $this->db->jdate($obj->date_creation);
                $this->tms = !empty($obj->tms) ? $this->db->jdate($obj->tms) : null;
                $this->fk_user_creat = $obj->fk_user_creat;
                $this->fk_user_modif = $obj->fk_user_modif;
                $this->note_public = $obj->note_public;
                $this->note_private = $obj->note_private;
                $this->fk_project = $obj->fk_project;
            }

            $this->db->free($resql);

            return 1;
        } else {
            $this->errors[] = 'Error '.$this->db->lasterror();
            return -1;
        }
    }

    /**
     * Update object in database
     */
    public function update($user, $notrigger = false)
    {
        $error = 0;

        // Clean parameters
        $this->ref = trim($this->ref);
        $this->label = trim($this->label);

        $this->db->begin();

        $sql = "UPDATE ".MAIN_DB_PREFIX.$this->table_element." SET";
        $sql .= " ref = '".$this->db->escape($this->ref)."',";
        $sql .= " label = '".$this->db->escape($this->label)."',";
        $sql .= " description = ".($this->description ? "'".$this->db->escape($this->description)."'" : "null").",";
        $sql .= " status = ".((int) $this->status).",";
        $sql .= " fk_user_modif = ".((int) $user->id);
        $sql .= " WHERE rowid = ".((int) $this->id);

        dol_syslog(get_class($this)."::update", LOG_DEBUG);
        $resql = $this->db->query($sql);

        if (!$resql) {
            $error++;
            $this->errors[] = "Error ".$this->db->lasterror();
        }

        if (!$error && !$notrigger) {
            $result = $this->call_trigger('MOKOOBJECT_MODIFY', $user);
            if ($result < 0) {
                $error++;
            }
        }

        if (!$error) {
            $this->db->commit();
            return 1;
        } else {
            $this->db->rollback();
            return -1;
        }
    }

    /**
     * Delete object from database
     */
    public function delete($user, $notrigger = false)
    {
        $error = 0;

        $this->db->begin();

        if (!$error && !$notrigger) {
            $result = $this->call_trigger('MOKOOBJECT_DELETE', $user);
            if ($result < 0) {
                $error++;
            }
        }

        if (!$error) {
            $sql = "DELETE FROM ".MAIN_DB_PREFIX.$this->table_element;
            $sql .= " WHERE rowid = ".((int) $this->id);

            dol_syslog(get_class($this)."::delete", LOG_DEBUG);
            $resql = $this->db->query($sql);

            if (!$resql) {
                $error++;
                $this->errors[] = "Error ".$this->db->lasterror();
            }
        }

        if (!$error) {
            $this->db->commit();
            return 1;
        } else {
            $this->db->rollback();
            return -1;
        }
    }

    /**
     * Get status label
     */
    public function getLibStatut($mode = 0)
    {
        return $this->LibStatut($this->status, $mode);
    }

    /**
     * Return status label
     */
    public function LibStatut($status, $mode = 0)
    {
        global $langs;

        $statusType = 'status'.$status;
        if ($status == 0) {
            $statusType = 'status4';
        }
        if ($status == 1) {
            $statusType = 'status6';
        }

        $statusLabel = array(
            0 => 'Draft',
            1 => 'Validated',
            9 => 'Cancelled'
        );

        return dolGetStatus($langs->trans($statusLabel[$status]), '', '', $statusType, $mode);
    }
}
```

### Step 4: Admin Setup Page

Create `admin/setup.php`:

```php
<?php
/**
 * Module configuration page
 */

// Load Dolibarr environment
$res = 0;
if (!$res && file_exists("../../main.inc.php")) {
    $res = @include "../../main.inc.php";
}
if (!$res) {
    die("Main include failed");
}

require_once DOL_DOCUMENT_ROOT.'/core/lib/admin.lib.php';

// Security check
if (!$user->admin) {
    accessforbidden();
}

// Translations
$langs->load("mokoexample@mokoexample");

// Actions
if ($action == 'update') {
    $example_option = GETPOST('MOKOEXAMPLE_OPTION', 'alpha');

    $res = dolibarr_set_const($db, "MOKOEXAMPLE_OPTION", $example_option, 'chaine', 0, '', $conf->entity);

    if ($res > 0) {
        setEventMessages($langs->trans("SetupSaved"), null, 'mesgs');
    } else {
        setEventMessages($langs->trans("Error"), null, 'errors');
    }
}

// Page header
llxHeader('', $langs->trans("MokoExampleSetup"));

$linkback = '<a href="'.DOL_URL_ROOT.'/admin/modules.php">'.$langs->trans("BackToModuleList").'</a>';
print load_fiche_titre($langs->trans("MokoExampleSetup"), $linkback, 'mokoexample@mokoexample');

// Configuration form
print '<form method="post" action="'.$_SERVER["PHP_SELF"].'">';
print '<input type="hidden" name="token" value="'.newToken().'">';
print '<input type="hidden" name="action" value="update">';

print '<table class="noborder centpercent">';
print '<tr class="liste_titre">';
print '<td>'.$langs->trans("Parameter").'</td>';
print '<td>'.$langs->trans("Value").'</td>';
print '</tr>';

print '<tr class="oddeven">';
print '<td>'.$langs->trans("ExampleOption").'</td>';
print '<td>';
print '<input type="text" name="MOKOEXAMPLE_OPTION" value="'.$conf->global->MOKOEXAMPLE_OPTION.'" size="50">';
print '</td>';
print '</tr>';

print '</table>';

print '<div class="center">';
print '<input type="submit" class="button" value="'.$langs->trans("Save").'">';
print '</div>';

print '</form>';

// Page footer
llxFooter();
$db->close();
```

### Step 5: Translation File

Create `langs/en_US/mokoexample.lang`:

```
# Module
Module185056Name=MokoExample
Module185056Desc=Example Moko module for Dolibarr

# Menu
TopMenuMokoExample=MokoExample
LeftMenuMokoExample=MokoExample

# Permissions
Permission185057=Read MokoExample objects
Permission185058=Create/Update MokoExample objects
Permission185059=Delete MokoExample objects

# Setup
MokoExampleSetup=MokoExample Setup
ExampleOption=Example Option

# Common
MokoObject=MokoObject
MokoObjects=MokoObjects
NewMokoObject=New MokoObject
```

## Testing Your Module

### Enable the Module

1. Navigate to `Home → Setup → Modules`
2. Find "MokoExample" in the list
3. Click "Activate"
4. Verify no errors appear

### Test Functionality

```php
<?php
// Test script - save as test_mokoexample.php in module root

require_once '../../main.inc.php';
require_once './class/mokoobject.class.php';

// Create object
$object = new MokoObject($db);
$object->ref = 'TEST001';
$object->label = 'Test Object';
$object->description = 'This is a test';
$object->status = 1;

$result = $object->create($user);

if ($result > 0) {
    print "Object created with ID: ".$result."<br>";

    // Fetch object
    $object2 = new MokoObject($db);
    $object2->fetch($result);
    print "Fetched object: ".$object2->ref." - ".$object2->label."<br>";

    // Update object
    $object2->label = 'Updated Label';
    $object2->update($user);
    print "Object updated<br>";

    // Delete object
    $object2->delete($user);
    print "Object deleted<br>";
} else {
    print "Error creating object<br>";
    print_r($object->errors);
}
```

## Best Practices

### Code Quality

- Run PHPCodeSniffer before committing
- Follow Dolibarr coding standards
- Write PHPDoc comments
- Use type hints where possible

### Security

- Always validate user input
- Use prepared statements
- Check user permissions
- Escape output
- Use CSRF tokens

### Performance

- Use indexes on database tables
- Cache query results when appropriate
- Avoid N+1 queries
- Optimize slow queries

### Debugging

```php
// Enable debug mode in conf.php
$dolibarr_main_prod = '0';

// Use dol_syslog for logging
dol_syslog("My debug message: ".print_r($variable, true), LOG_DEBUG);

// Check logs in documents/dolibarr.log
```

## Additional Resources

- [Dolibarr Wiki](https://wiki.dolibarr.org/)
- [Dolibarr Developer Documentation](https://wiki.dolibarr.org/index.php/Developer_documentation)
- [MokoCRM Development Standards](../../policy/crm/development-standards.md)
- [Coding Style Guide](../../policy/coding-style-guide.md)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/crm/dolibarr-development-guide.md                                      |
| Version        | 04.00.01                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.01 with all required fields |
