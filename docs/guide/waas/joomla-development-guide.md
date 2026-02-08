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
INGROUP: MokoStandards.WaaS
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/waas/joomla-development-guide.md
VERSION: 03.01.01
BRIEF: Practical guide for developing custom extensions for Joomla/MokoWaaS
-->

# Joomla Development Guide

## Overview

This guide provides practical, step-by-step instructions for developing custom extensions for Joomla and MokoWaaS. It complements the [WaaS Development Standards](../../policy/waas/development-standards.md) policy with hands-on examples and tutorials.

## Getting Started

### Development Environment Setup

**Prerequisites**:
- PHP 8.1+ with required extensions (mysqli, json, zip, gd, curl, xml, mbstring)
- MySQL 8.0+ or MariaDB 10.4+
- Apache or Nginx web server
- Composer (optional, for dependencies)
- Git (for version control)
- Code editor (VS Code, PHPStorm recommended)

**Install Joomla locally**:

```bash
# Download Joomla
cd /var/www/html
wget https://downloads.joomla.org/cms/joomla4/4-4-1/Joomla_4-4-1-Stable-Full_Package.tar.gz
mkdir joomla
cd joomla
tar -xzf ../Joomla_4-4-1-Stable-Full_Package.tar.gz

# Set permissions
sudo chown -R www-data:www-data /var/www/html/joomla
sudo find /var/www/html/joomla -type d -exec chmod 755 {} \;
sudo find /var/www/html/joomla -type f -exec chmod 644 {} \;

# Create database
mysql -u root -p <<EOF
CREATE DATABASE joomla_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'joomla'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON joomla_dev.* TO 'joomla'@'localhost';
FLUSH PRIVILEGES;
EOF

# Complete installation via web browser
# Navigate to: http://localhost/joomla/
```

**Configure development settings**:

Edit `configuration.php` after installation:

```php
<?php
// Enable error reporting
public $error_reporting = 'development';
public $debug = '1';
public $debug_lang = '1';

// Disable caching during development
public $caching = '0';
```

## Creating Your First Component

### Component Skeleton

**Create component directory structure**:

```bash
cd /var/www/html/joomla
mkdir -p components/com_mokoevents
mkdir -p administrator/components/com_mokoevents
```

**Component structure**:

```
com_mokoevents/
├── site/                        # Frontend
│   ├── mokoevents.php          # Entry point
│   ├── controller.php          # Main controller
│   ├── models/
│   │   ├── event.php
│   │   └── events.php
│   ├── views/
│   │   ├── event/
│   │   │   ├── tmpl/
│   │   │   │   └── default.php
│   │   │   └── view.html.php
│   │   └── events/
│   │       ├── tmpl/
│   │       │   └── default.php
│   │       └── view.html.php
│   └── helpers/
│       └── mokoevents.php
├── admin/                       # Backend
│   ├── mokoevents.php
│   ├── access.xml
│   ├── config.xml
│   ├── controllers/
│   │   └── event.php
│   ├── models/
│   │   ├── event.php
│   │   ├── events.php
│   │   └── forms/
│   │       └── event.xml
│   ├── tables/
│   │   └── event.php
│   ├── views/
│   │   ├── event/
│   │   └── events/
│   └── sql/
│       ├── install.mysql.utf8.sql
│       └── uninstall.mysql.utf8.sql
├── media/
│   ├── css/
│   │   └── mokoevents.css
│   ├── js/
│   │   └── mokoevents.js
│   └── images/
└── mokoevents.xml               # Manifest file
```

### Step 1: Manifest File

Create `mokoevents.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<extension type="component" method="upgrade">
    <name>COM_MOKOEVENTS</name>
    <author>Moko Consulting</author>
    <creationDate>2026-01</creationDate>
    <copyright>Copyright (C) 2026 Moko Consulting. All rights reserved.</copyright>
    <license>GPL-3.0-or-later</license>
    <authorEmail>hello@mokoconsulting.tech</authorEmail>
    <authorUrl>https://mokoconsulting.tech</authorUrl>
    <version>1.0.0</version>
    <description>COM_MOKOEVENTS_XML_DESCRIPTION</description>

    <!-- Scripts to run on installation -->
    <scriptfile>script.php</scriptfile>

    <!-- Install SQL -->
    <install>
        <sql>
            <file driver="mysql" charset="utf8">sql/install.mysql.utf8.sql</file>
        </sql>
    </install>

    <!-- Uninstall SQL -->
    <uninstall>
        <sql>
            <file driver="mysql" charset="utf8">sql/uninstall.mysql.utf8.sql</file>
        </sql>
    </uninstall>

    <!-- Update SQL -->
    <update>
        <schemas>
            <schemapath type="mysql">sql/updates/mysql</schemapath>
        </schemas>
    </update>

    <!-- Site files -->
    <files folder="site">
        <filename>mokoevents.php</filename>
        <filename>controller.php</filename>
        <folder>models</folder>
        <folder>views</folder>
        <folder>helpers</folder>
    </files>

    <!-- Administration files -->
    <administration>
        <menu img="components/com_mokoevents/media/images/icon.png">COM_MOKOEVENTS</menu>
        <submenu>
            <menu link="option=com_mokoevents&amp;view=events">COM_MOKOEVENTS_EVENTS</menu>
        </submenu>

        <files folder="admin">
            <filename>mokoevents.php</filename>
            <filename>access.xml</filename>
            <filename>config.xml</filename>
            <folder>controllers</folder>
            <folder>models</folder>
            <folder>views</folder>
            <folder>tables</folder>
            <folder>sql</folder>
        </files>
    </administration>

    <!-- Media files -->
    <media folder="media" destination="com_mokoevents">
        <folder>css</folder>
        <folder>js</folder>
        <folder>images</folder>
    </media>

    <!-- Language files -->
    <languages folder="language">
        <language tag="en-GB">en-GB/com_mokoevents.ini</language>
        <language tag="en-GB">en-GB/com_mokoevents.sys.ini</language>
    </languages>

    <administration>
        <languages folder="admin/language">
            <language tag="en-GB">en-GB/com_mokoevents.ini</language>
            <language tag="en-GB">com_mokoevents.sys.ini</language>
        </languages>
    </administration>

    <!-- Update server -->
    <updateservers>
        <server type="extension" priority="1" name="MokoEvents">
            https://updates.mokoconsulting.tech/mokoevents.xml
        </server>
    </updateservers>
</extension>
```

### Step 2: Database Tables

Create `admin/sql/install.mysql.utf8.sql`:

```sql
CREATE TABLE IF NOT EXISTS `#__mokoevents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL DEFAULT '0' COMMENT 'FK to #__assets',
  `title` varchar(255) NOT NULL,
  `alias` varchar(400) NOT NULL,
  `description` text,
  `event_date` datetime NOT NULL,
  `location` varchar(255),

  -- Publishing fields
  `state` tinyint(4) NOT NULL DEFAULT '0',
  `catid` int(11) NOT NULL DEFAULT '0',
  `created` datetime NOT NULL,
  `created_by` int(11) NOT NULL DEFAULT '0',
  `modified` datetime NOT NULL,
  `modified_by` int(11) NOT NULL DEFAULT '0',
  `publish_up` datetime NOT NULL,
  `publish_down` datetime NOT NULL,
  `checked_out` int(11) NOT NULL DEFAULT '0',
  `checked_out_time` datetime NOT NULL,

  -- Metadata
  `metadata` text,
  `metakey` text,
  `metadesc` text,
  `language` char(7) NOT NULL DEFAULT '*',

  -- Ordering and access
  `ordering` int(11) NOT NULL DEFAULT '0',
  `access` int(11) NOT NULL DEFAULT '1',
  `params` text,
  `featured` tinyint(4) NOT NULL DEFAULT '0',
  `hits` int(11) NOT NULL DEFAULT '0',

  PRIMARY KEY (`id`),
  KEY `idx_access` (`access`),
  KEY `idx_checkout` (`checked_out`),
  KEY `idx_state` (`state`),
  KEY `idx_catid` (`catid`),
  KEY `idx_language` (`language`),
  KEY `idx_createdby` (`created_by`),
  KEY `idx_featured_catid` (`featured`,`catid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
```

Create `admin/sql/uninstall.mysql.utf8.sql`:

```sql
DROP TABLE IF EXISTS `#__mokoevents`;
```

### Step 3: Table Class

Create `admin/tables/event.php`:

```php
<?php
defined('_JEXEC') or die;

use Joomla\CMS\Table\Table;
use Joomla\Database\DatabaseDriver;

class MokoeventsTableEvent extends Table
{
    /**
     * Constructor
     */
    public function __construct(DatabaseDriver $db)
    {
        parent::__construct('#__mokoevents', 'id', $db);
    }

    /**
     * Overloaded check method to ensure data integrity
     */
    public function check()
    {
        // Check for valid title
        if (trim($this->title) == '') {
            throw new \UnexpectedValueException('Title is required');
        }

        // Generate alias if empty
        if (trim($this->alias) == '') {
            $this->alias = $this->title;
        }

        $this->alias = \JApplicationHelper::stringURLSafe($this->alias);

        // Check dates
        if (empty($this->created)) {
            $this->created = \JFactory::getDate()->toSql();
        }

        return true;
    }

    /**
     * Method to store a row
     */
    public function store($updateNulls = false)
    {
        $date = \JFactory::getDate();
        $user = \JFactory::getUser();

        // Set created date if new
        if (!$this->id) {
            $this->created = $date->toSql();
            $this->created_by = $user->id;
        }

        // Always update modified date
        $this->modified = $date->toSql();
        $this->modified_by = $user->id;

        return parent::store($updateNulls);
    }
}
```

### Step 4: Model (Backend)

Create `admin/models/event.php`:

```php
<?php
defined('_JEXEC') or die;

use Joomla\CMS\MVC\Model\AdminModel;
use Joomla\CMS\Factory;

class MokoeventsModelEvent extends AdminModel
{
    /**
     * Get the form
     */
    public function getForm($data = array(), $loadData = true)
    {
        $form = $this->loadForm(
            'com_mokoevents.event',
            'event',
            array('control' => 'jform', 'load_data' => $loadData)
        );

        if (empty($form)) {
            return false;
        }

        return $form;
    }

    /**
     * Method to get the data
     */
    protected function loadFormData()
    {
        $data = Factory::getApplication()->getUserState('com_mokoevents.edit.event.data', array());

        if (empty($data)) {
            $data = $this->getItem();
        }

        return $data;
    }

    /**
     * Method to get a table object
     */
    public function getTable($type = 'Event', $prefix = 'MokoeventsTable', $config = array())
    {
        return parent::getTable($type, $prefix, $config);
    }

    /**
     * Prepare and sanitise the table data prior to saving
     */
    protected function prepareTable($table)
    {
        $table->title = htmlspecialchars_decode($table->title, ENT_QUOTES);
        $table->alias = \JApplicationHelper::stringURLSafe($table->alias);

        if (empty($table->alias)) {
            $table->alias = \JApplicationHelper::stringURLSafe($table->title);
        }
    }
}
```

### Step 5: Form Definition

Create `admin/models/forms/event.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<form>
    <fieldset name="details" label="COM_MOKOEVENTS_FIELDSET_DETAILS">
        <field
            name="id"
            type="number"
            label="JGLOBAL_FIELD_ID_LABEL"
            default="0"
            readonly="true"
            class="readonly"
        />

        <field
            name="title"
            type="text"
            label="COM_MOKOEVENTS_FIELD_TITLE_LABEL"
            description="COM_MOKOEVENTS_FIELD_TITLE_DESC"
            size="40"
            required="true"
        />

        <field
            name="alias"
            type="text"
            label="JFIELD_ALIAS_LABEL"
            description="JFIELD_ALIAS_DESC"
            size="40"
            hint="JFIELD_ALIAS_PLACEHOLDER"
        />

        <field
            name="event_date"
            type="calendar"
            label="COM_MOKOEVENTS_FIELD_EVENT_DATE_LABEL"
            description="COM_MOKOEVENTS_FIELD_EVENT_DATE_DESC"
            format="%Y-%m-%d %H:%M:%S"
            filter="user_utc"
            required="true"
        />

        <field
            name="location"
            type="text"
            label="COM_MOKOEVENTS_FIELD_LOCATION_LABEL"
            description="COM_MOKOEVENTS_FIELD_LOCATION_DESC"
            size="40"
        />

        <field
            name="description"
            type="editor"
            label="JGLOBAL_DESCRIPTION"
            description="COM_MOKOEVENTS_FIELD_DESCRIPTION_DESC"
            filter="JComponentHelper::filterText"
            buttons="true"
        />

        <field
            name="state"
            type="list"
            label="JSTATUS"
            description="JFIELD_PUBLISHED_DESC"
            default="1"
            required="true"
        >
            <option value="1">JPUBLISHED</option>
            <option value="0">JUNPUBLISHED</option>
            <option value="2">JARCHIVED</option>
            <option value="-2">JTRASHED</option>
        </field>

        <field
            name="catid"
            type="category"
            extension="com_mokoevents"
            label="JCATEGORY"
            description="JFIELD_CATEGORY_DESC"
            required="true"
        />

        <field
            name="access"
            type="accesslevel"
            label="JFIELD_ACCESS_LABEL"
            description="JFIELD_ACCESS_DESC"
            default="1"
            required="true"
        />

        <field
            name="language"
            type="contentlanguage"
            label="JFIELD_LANGUAGE_LABEL"
            description="JFIELD_LANGUAGE_DESC"
        />

        <field
            name="featured"
            type="list"
            label="JFEATURED"
            description="JFIELD_FEATURED_DESC"
            default="0"
        >
            <option value="0">JNO</option>
            <option value="1">JYES</option>
        </field>
    </fieldset>

    <fieldset name="publishing" label="JGLOBAL_FIELDSET_PUBLISHING">
        <field
            name="created_by"
            type="user"
            label="JGLOBAL_FIELD_CREATED_BY_LABEL"
            description="JGLOBAL_FIELD_CREATED_BY_DESC"
        />

        <field
            name="created"
            type="calendar"
            label="JGLOBAL_FIELD_CREATED_LABEL"
            description="JGLOBAL_FIELD_CREATED_DESC"
            format="%Y-%m-%d %H:%M:%S"
            filter="user_utc"
        />

        <field
            name="publish_up"
            type="calendar"
            label="JGLOBAL_FIELD_PUBLISH_UP_LABEL"
            description="JGLOBAL_FIELD_PUBLISH_UP_DESC"
            format="%Y-%m-%d %H:%M:%S"
            filter="user_utc"
        />

        <field
            name="publish_down"
            type="calendar"
            label="JGLOBAL_FIELD_PUBLISH_DOWN_LABEL"
            description="JGLOBAL_FIELD_PUBLISH_DOWN_DESC"
            format="%Y-%m-%d %H:%M:%S"
            filter="user_utc"
        />
    </fieldset>

    <fieldset name="metadata" label="JGLOBAL_FIELDSET_METADATA_OPTIONS">
        <field
            name="metadesc"
            type="textarea"
            label="JFIELD_META_DESCRIPTION_LABEL"
            description="JFIELD_META_DESCRIPTION_DESC"
            rows="3"
            cols="40"
        />

        <field
            name="metakey"
            type="textarea"
            label="JFIELD_META_KEYWORDS_LABEL"
            description="JFIELD_META_KEYWORDS_DESC"
            rows="3"
            cols="40"
        />
    </fieldset>
</form>
```

### Step 6: Frontend View

Create `site/views/event/view.html.php`:

```php
<?php
defined('_JEXEC') or die;

use Joomla\CMS\MVC\View\HtmlView;
use Joomla\CMS\Factory;

class MokoeventsViewEvent extends HtmlView
{
    protected $item;
    protected $params;

    public function display($tpl = null)
    {
        // Get data from the model
        $this->item = $this->get('Item');
        $this->params = Factory::getApplication()->getParams();

        // Check for errors
        if (count($errors = $this->get('Errors'))) {
            throw new \Exception(implode("\n", $errors), 500);
        }

        // Prepare the document
        $this->prepareDocument();

        parent::display($tpl);
    }

    protected function prepareDocument()
    {
        $app = Factory::getApplication();
        $menus = $app->getMenu();
        $menu = $menus->getActive();

        if ($menu) {
            $this->params->def('page_heading', $this->params->get('page_title', $menu->title));
        }

        // Set page title
        $title = $this->params->get('page_title', '');

        if (empty($title)) {
            $title = $this->item->title;
        }

        $this->document->setTitle($title);

        // Set meta description
        if ($this->item->metadesc) {
            $this->document->setDescription($this->item->metadesc);
        }

        // Set meta keywords
        if ($this->item->metakey) {
            $this->document->setMetadata('keywords', $this->item->metakey);
        }
    }
}
```

Create `site/views/event/tmpl/default.php`:

```php
<?php
defined('_JEXEC') or die;

use Joomla\CMS\HTML\HTMLHelper;
use Joomla\CMS\Language\Text;

/** @var object $this->item */
?>

<div class="mokoevents-event">
    <h1><?php echo $this->escape($this->item->title); ?></h1>

    <div class="event-meta">
        <span class="event-date">
            <i class="icon-calendar"></i>
            <?php echo HTMLHelper::_('date', $this->item->event_date, Text::_('DATE_FORMAT_LC3')); ?>
        </span>

        <?php if ($this->item->location): ?>
            <span class="event-location">
                <i class="icon-location"></i>
                <?php echo $this->escape($this->item->location); ?>
            </span>
        <?php endif; ?>
    </div>

    <?php if ($this->item->description): ?>
        <div class="event-description">
            <?php echo $this->item->description; ?>
        </div>
    <?php endif; ?>
</div>
```

## Testing Your Extension

### Install the Extension

1. Create a zip file of your component
2. Navigate to `System → Install → Extensions`
3. Upload and install the zip file
4. Check for any errors

### Test Functionality

- Backend: Create, edit, delete events
- Frontend: View events list and details
- Check permissions
- Test with different user groups
- Verify responsive design

## Best Practices

### Security Checklist

- [ ] All input validated and filtered
- [ ] Output escaped
- [ ] CSRF tokens used
- [ ] ACL checked
- [ ] SQL injection prevented
- [ ] XSS prevented

### Performance Optimization

- Use Joomla caching
- Optimize database queries
- Minify CSS/JS
- Lazy load images
- Use CDN for assets

### Accessibility

- Proper heading hierarchy
- Alt text for images
- Keyboard navigation
- ARIA labels
- Color contrast ratios

## Additional Resources

- [Joomla Documentation](https://docs.joomla.org/)
- [Joomla Developer Network](https://developer.joomla.org/)
- [WaaS Development Standards](../../policy/waas/development-standards.md)
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
| Path           | /docs/guide/waas/joomla-development-guide.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
