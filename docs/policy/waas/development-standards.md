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
INGROUP: MokoStandards.WaaS
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/waas/development-standards.md
VERSION: 04.00.03
BRIEF: Development standards for MokoWaaS based on Joomla platform
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoWaaS Development Standards

## Purpose

This policy establishes development standards for MokoWaaS, Moko Consulting's Website-as-a-Service platform based on the Joomla CMS framework. It defines coding conventions, extension development requirements, customization guidelines, and quality standards specific to the Joomla ecosystem.

## Scope

This policy applies to:

- All MokoWaaS custom extensions (components, modules, plugins)
- Joomla core customizations and overrides
- Template development and customization
- MokoWaaS API integrations
- Database schema modifications
- Custom fields and workflows
- Third-party extension customization

This policy does not apply to:

- Joomla core framework code (unless creating patches)
- Unmodified third-party extensions
- Infrastructure configuration (covered by operations policies)
- Content creation and editorial guidelines

## Responsibilities

### WaaS Development Lead

Accountable for:

- Defining WaaS development standards
- Approving extension architecture
- Reviewing major customizations
- Ensuring Joomla compatibility
- Managing technical debt
- Coordinating with security team

### WaaS Developers

Responsible for:

- Following development standards
- Writing maintainable custom extensions
- Testing customizations thoroughly
- Documenting code and configurations
- Maintaining upgrade compatibility
- Following security best practices

### QA Team

Responsible for:

- Testing custom extensions
- Validating upgrade compatibility
- Verifying performance impact
- Ensuring accessibility compliance
- Documenting test results
- Security testing

## Joomla Architecture Overview

### Platform Characteristics

**Framework**: Joomla CMS
**Language**: PHP 8.1+
**Database**: MySQL 8.0+ / MariaDB 10.4+
**Architecture**: MVC (Model-View-Controller)
**License**: GPL-2.0-or-later

### MokoWaaS Structure

```
site_root/
├── administrator/              # Backend admin interface
│   ├── components/            # Admin components
│   ├── modules/               # Admin modules
│   └── templates/             # Admin templates
├── components/                # Frontend components
├── modules/                   # Frontend modules
├── plugins/                   # System plugins
│   ├── authentication/        # Auth plugins
│   ├── content/              # Content plugins
│   ├── system/               # System plugins
│   └── user/                 # User plugins
├── templates/                 # Frontend templates
├── media/                     # Media files
├── libraries/                 # Shared libraries
└── cli/                      # CLI scripts
```

## Extension Development Standards

### Extension Types

**Components** - Main applications:
- Provide both frontend and backend functionality
- Have their own MVC structure
- Example: com_mokoevents, com_mokoclient

**Modules** - Display blocks:
- Show specific content in template positions
- Can be frontend or backend
- Example: mod_mokoslider, mod_mokocontact

**Plugins** - Event handlers:
- Respond to system events
- Extend functionality without UI
- Example: plg_system_mokoanalytics, plg_content_mokoseo

**Templates** - Site appearance:
- Control layout and styling
- Should use template overrides
- Example: tpl_mokowaas_baseline

### Naming Conventions

**Extensions**:
- Prefix with `moko`: `com_mokoevents`, `mod_mokocontact`
- Use lowercase with underscores
- Be descriptive but concise

**Files**:
- Components: `com_name/name.php`
- Modules: `mod_name/mod_name.php`
- Plugins: `plg_type_name/name.php`

**Classes**:
- Follow Joomla naming: `MokoEventsController`, `ModMokoContactHelper`
- Use PascalCase
- Include extension name

**Database Tables**:
- Prefix with `#__moko_`: `#__moko_events`, `#__moko_clients`
- Use singular nouns for main tables
- Use plural for junction tables

**Example Component Structure**:
```
com_mokoevents/
├── mokoevents.xml              # Manifest file
├── site/                       # Frontend
│   ├── mokoevents.php         # Entry point
│   ├── controller.php         # Main controller
│   ├── models/                # Data models
│   ├── views/                 # View templates
│   │   ├── event/
│   │   │   ├── tmpl/
│   │   │   │   └── default.php
│   │   │   └── view.html.php
│   │   └── events/
│   └── helpers/               # Helper classes
├── admin/                     # Backend
│   ├── mokoevents.php
│   ├── controller.php
│   ├── models/
│   ├── views/
│   ├── tables/                # Table classes
│   └── sql/
│       ├── install.mysql.utf8.sql
│       └── uninstall.mysql.utf8.sql
└── media/                     # Assets
    ├── css/
    ├── js/
    └── images/
```

## Coding Standards

### PHP Standards

**Follow Joomla Coding Standards**:
- Based on PSR-12 with Joomla-specific conventions
- Use Joomla framework classes
- Follow Joomla API patterns

**File Headers**:
```php
<?php
/**
 * @package     MokoWaaS
 * @subpackage  com_mokoevents
 * @copyright   Copyright (C) 2026 Moko Consulting. All rights reserved.
 * @license     GPL-3.0-or-later
 */

defined('_JEXEC') or die;
```

**Class Structure**:
```php
<?php
/**
 * Events Controller
 *
 * @since  1.0.0
 */
class MokoEventsController extends JControllerLegacy
{
    /**
     * Default view
     *
     * @var    string
     * @since  1.0.0
     */
    protected $default_view = 'events';

    /**
     * Display the view
     *
     * @param   boolean  $cachable   If true, the view output will be cached
     * @param   array    $urlparams  URL parameters
     *
     * @return  JControllerLegacy  This object to support chaining
     *
     * @since   1.0.0
     */
    public function display($cachable = false, $urlparams = array())
    {
        return parent::display($cachable, $urlparams);
    }
}
```

### MVC Pattern

**Models** - Data and business logic:
```php
<?php
class MokoEventsModelEvent extends JModelItem
{
    /**
     * Get an event
     *
     * @return  object|false  Event object or false on error
     *
     * @since   1.0.0
     */
    public function getItem($pk = null)
    {
        $item = parent::getItem($pk);

        if (!empty($item->id)) {
            // Load additional data
            $item->category = $this->getCategory($item->catid);
        }

        return $item;
    }
}
```

**Views** - Presentation logic:
```php
<?php
class MokoEventsViewEvent extends JViewLegacy
{
    /**
     * @var    object  The event object
     * @since  1.0.0
     */
    protected $item;

    /**
     * Display the view
     *
     * @param   string  $tpl  The name of the template file to parse
     *
     * @return  void
     *
     * @since   1.0.0
     */
    public function display($tpl = null)
    {
        $this->item = $this->get('Item');

        // Check for errors
        if (count($errors = $this->get('Errors'))) {
            throw new Exception(implode("\n", $errors), 500);
        }

        parent::display($tpl);
    }
}
```

**Controllers** - User interaction:
```php
<?php
class MokoEventsControllerEvent extends JControllerForm
{
    /**
     * Save an event
     *
     * @param   string  $key     The name of the primary key
     * @param   string  $urlVar  The name of the URL variable
     *
     * @return  boolean  True on success, false otherwise
     *
     * @since   1.0.0
     */
    public function save($key = null, $urlVar = null)
    {
        // Check for request forgeries
        JSession::checkToken() or jexit(JText::_('JINVALID_TOKEN'));

        // Custom validation
        $data = $this->input->post->get('jform', array(), 'array');

        if (!$this->validateEventData($data)) {
            return false;
        }

        return parent::save($key, $urlVar);
    }
}
```

## Database Standards

### Table Design

**Standard Columns** (all tables should have):
```sql
CREATE TABLE IF NOT EXISTS `#__moko_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL DEFAULT '0' COMMENT 'FK to assets table',
  `title` varchar(255) NOT NULL,
  `alias` varchar(400) NOT NULL,
  `description` text,

  -- Publishing fields
  `state` tinyint(4) NOT NULL DEFAULT '0',
  `catid` int(11) NOT NULL DEFAULT '0',
  `created` datetime NOT NULL,
  `created_by` int(11) NOT NULL DEFAULT '0',
  `modified` datetime NOT NULL,
  `modified_by` int(11) NOT NULL DEFAULT '0',
  `publish_up` datetime NOT NULL,
  `publish_down` datetime NOT NULL,

  -- Metadata
  `metadata` text,
  `metakey` text,
  `metadesc` text,
  `language` char(7) NOT NULL DEFAULT '*',

  -- Ordering and access
  `ordering` int(11) NOT NULL DEFAULT '0',
  `access` int(11) NOT NULL DEFAULT '1',
  `params` text,

  PRIMARY KEY (`id`),
  KEY `idx_access` (`access`),
  KEY `idx_state` (`state`),
  KEY `idx_catid` (`catid`),
  KEY `idx_language` (`language`),
  KEY `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
```

### Using Table Classes

```php
<?php
class MokoEventsTableEvent extends JTable
{
    /**
     * Constructor
     *
     * @param   JDatabaseDriver  $db  Database connector
     *
     * @since   1.0.0
     */
    public function __construct(&$db)
    {
        parent::__construct('#__moko_events', 'id', $db);

        // Set field aliases
        $this->setColumnAlias('published', 'state');
    }

    /**
     * Overloaded check method
     *
     * @return  boolean  True on success
     *
     * @since   1.0.0
     */
    public function check()
    {
        // Generate alias
        if (trim($this->alias) == '') {
            $this->alias = $this->title;
        }

        $this->alias = JApplicationHelper::stringURLSafe($this->alias);

        // Check for valid name
        if (trim($this->title) == '') {
            $this->setError(JText::_('COM_MOKOEVENTS_WARNING_PROVIDE_VALID_NAME'));
            return false;
        }

        return true;
    }
}
```

## Security Standards

### Access Control

**Check user permissions**:
```php
<?php
// Component level
if (!JFactory::getUser()->authorise('core.manage', 'com_mokoevents')) {
    throw new Exception(JText::_('JERROR_ALERTNOAUTHOR'), 403);
}

// Item level
if (!JFactory::getUser()->authorise('core.edit', 'com_mokoevents.event.' . $id)) {
    throw new Exception(JText::_('JERROR_ALERTNOAUTHOR'), 403);
}

// View level
$user = JFactory::getUser();
$groups = $user->getAuthorisedViewLevels();

if (!in_array($item->access, $groups)) {
    throw new Exception(JText::_('JERROR_ALERTNOAUTHOR'), 403);
}
```

### Input Validation

**Always validate and filter input**:
```php
<?php
// Get filtered input
$title = $this->input->getString('title', '');
$id = $this->input->getInt('id', 0);
$email = $this->input->getString('email', '');

// Validate email
if (!JMailHelper::isEmailAddress($email)) {
    throw new InvalidArgumentException('Invalid email address');
}

// Use JForm for complex validation
$form = $this->getForm();
$data = $this->input->post->get('jform', array(), 'array');
$validData = $form->filter($data);

if (!$form->validate($validData)) {
    $errors = $form->getErrors();
    // Handle errors
}
```

### SQL Injection Prevention

**Always use query builder or prepared statements**:
```php
<?php
// ✅ Good: Using query builder
$db = JFactory::getDbo();
$query = $db->getQuery(true);

$query->select('*')
    ->from($db->quoteName('#__moko_events'))
    ->where($db->quoteName('state') . ' = 1')
    ->where($db->quoteName('catid') . ' = ' . $db->quote($catid));

$db->setQuery($query);
$results = $db->loadObjectList();

// ❌ Bad: String concatenation
$sql = "SELECT * FROM #__moko_events WHERE catid = " . $catid;
```

### XSS Prevention

**Escape all output**:
```php
<?php
// In template files
echo htmlspecialchars($this->item->title, ENT_COMPAT, 'UTF-8');

// Or use Joomla helper
echo JText::_($this->escape($this->item->title));

// For JavaScript
$title = json_encode($this->item->title);
?>
<script>
const title = <?php echo $title; ?>;
</script>
```

### CSRF Protection

**Check tokens on all form submissions**:
```php
<?php
// In controller
JSession::checkToken() or jexit(JText::_('JINVALID_TOKEN'));

// In forms
echo JHtml::_('form.token');
```

## Template Development

### Template Structure

```
tpl_mokowaas/
├── templateDetails.xml         # Manifest
├── index.php                   # Main template file
├── component.php              # Component layout
├── error.php                  # Error page
├── offline.php                # Offline page
├── html/                      # Template overrides
│   ├── com_content/
│   │   └── article/
│   │       └── default.php
│   └── mod_menu/
│       └── default.php
├── css/
│   └── template.css
├── js/
│   └── template.js
├── images/
└── language/
    └── en-GB/
        └── en-GB.tpl_mokowaas.ini
```

### Template index.php

```php
<?php
defined('_JEXEC') or die;

/** @var JDocumentHtml $this */

$app = JFactory::getApplication();
$doc = JFactory::getDocument();
$user = JFactory::getUser();
$sitename = htmlspecialchars($app->get('sitename'), ENT_QUOTES, 'UTF-8');

// Add stylesheets
$doc->addStyleSheet($this->baseurl . '/templates/' . $this->template . '/css/template.css');

// Add scripts
$doc->addScript($this->baseurl . '/templates/' . $this->template . '/js/template.js');
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <jdoc:include type="head" />
</head>
<body class="site <?php echo $this->pageclass_sfx; ?>">
    <header class="site-header">
        <jdoc:include type="modules" name="header" style="none" />
    </header>

    <main class="site-main">
        <jdoc:include type="message" />
        <jdoc:include type="component" />
    </main>

    <footer class="site-footer">
        <jdoc:include type="modules" name="footer" style="none" />
    </footer>
</body>
</html>
```

### Template Overrides

Place in `/templates/template_name/html/extension_name/`:

```php
<?php
// templates/mokowaas/html/com_content/article/default.php
defined('_JEXEC') or die;

/** @var object $this->item */
?>
<article class="article">
    <h1><?php echo $this->escape($this->item->title); ?></h1>

    <?php if (!empty($this->item->images)): ?>
        <?php $images = json_decode($this->item->images); ?>
        <img src="<?php echo $images->image_fulltext; ?>"
             alt="<?php echo $this->escape($images->image_fulltext_alt); ?>">
    <?php endif; ?>

    <div class="article-content">
        <?php echo $this->item->text; ?>
    </div>
</article>
```

## Plugin Development

### Plugin Types and Events

**System Plugin** - Global events:
```php
<?php
class PlgSystemMokoanalytics extends JPlugin
{
    /**
     * After render event
     *
     * @return  void
     *
     * @since   1.0.0
     */
    public function onAfterRender()
    {
        $app = JFactory::getApplication();

        // Only run on site
        if ($app->isClient('site')) {
            $body = $app->getBody();

            // Add analytics code
            $analytics = $this->getAnalyticsCode();
            $body = str_replace('</body>', $analytics . '</body>', $body);

            $app->setBody($body);
        }
    }
}
```

**Content Plugin** - Content events:
```php
<?php
class PlgContentMokoseo extends JPlugin
{
    /**
     * Before content save event
     *
     * @param   string   $context  The context
     * @param   object   $article  The article object
     * @param   boolean  $isNew    Is new article
     *
     * @return  boolean
     *
     * @since   1.0.0
     */
    public function onContentBeforeSave($context, $article, $isNew)
    {
        // Validate SEO requirements
        if (strlen($article->metadesc) < 50) {
            JFactory::getApplication()->enqueueMessage(
                JText::_('PLG_CONTENT_MOKOSEO_WARNING_SHORT_DESCRIPTION'),
                'warning'
            );
        }

        return true;
    }
}
```

**User Plugin** - User events:
```php
<?php
class PlgUserMokonotify extends JPlugin
{
    /**
     * After user login
     *
     * @param   array  $options  Login options
     *
     * @return  void
     *
     * @since   1.0.0
     */
    public function onUserAfterLogin($options)
    {
        $user = JFactory::getUser($options['user']->id);

        // Send login notification
        $this->sendLoginNotification($user);
    }
}
```

## Module Development

```php
<?php
/**
 * @package     MokoWaaS
 * @subpackage  mod_mokocontact
 */

defined('_JEXEC') or die;

// Include helper
$helper = modMokoContactHelper::class;
JLoader::register($helper, __DIR__ . '/helper.php');

// Get module parameters
$email = $params->get('email', '');
$showPhone = $params->get('show_phone', 1);

// Get data from helper
$contactInfo = modMokoContactHelper::getContactInfo($params);

// Load template
require JModuleHelper::getLayoutPath('mod_mokocontact', $params->get('layout', 'default'));
```

**Module Helper**:
```php
<?php
class modMokoContactHelper
{
    /**
     * Get contact information
     *
     * @param   Joomla\Registry\Registry  $params  Module parameters
     *
     * @return  array  Contact information
     *
     * @since   1.0.0
     */
    public static function getContactInfo($params)
    {
        $db = JFactory::getDbo();
        $query = $db->getQuery(true);

        $query->select('*')
            ->from($db->quoteName('#__moko_contacts'))
            ->where($db->quoteName('published') . ' = 1')
            ->order($db->quoteName('ordering'));

        $db->setQuery($query);

        return $db->loadObjectList();
    }
}
```

## Testing Standards

### Unit Testing

Use PHPUnit with Joomla test framework:

```php
<?php
use Joomla\CMS\Factory;
use PHPUnit\Framework\TestCase;

class MokoEventsModelEventTest extends TestCase
{
    protected $model;

    protected function setUp(): void
    {
        parent::setUp();

        $this->model = new MokoEventsModelEvent();
    }

    public function testGetItem()
    {
        $item = $this->model->getItem(1);

        $this->assertNotNull($item);
        $this->assertGreaterThan(0, $item->id);
        $this->assertNotEmpty($item->title);
    }
}
```

### Integration Testing

- Test extension installation/uninstallation
- Test with different Joomla versions
- Test with different PHP versions
- Test database migrations
- Test permissions
- Test frontend and backend views

### Browser Testing

- Test responsive design (mobile, tablet, desktop)
- Test in major browsers (Chrome, Firefox, Safari, Edge)
- Test accessibility (WCAG 2.1 AA compliance)
- Test performance (PageSpeed Insights)

## Performance Standards

### Optimization Guidelines

**Database**:
- Use indexes appropriately
- Avoid N+1 queries
- Use joins instead of multiple queries
- Cache query results when appropriate
- Implement pagination

**Caching**:
```php
<?php
// Use Joomla cache
$cache = JFactory::getCache('com_mokoevents', '');
$cache->setCaching(true);

$events = $cache->get(function() {
    return $this->getEvents();
}, array(), md5('events_list'));
```

**Assets**:
- Minify CSS and JavaScript
- Optimize images
- Use lazy loading for images
- Combine asset files when possible
- Use CDN for common libraries

## Accessibility Standards

### WCAG 2.1 Compliance

**Level AA required for all extensions**:

- Proper heading hierarchy (h1, h2, h3)
- Alt text for all images
- Keyboard navigation support
- ARIA labels where appropriate
- Color contrast ratios meet requirements
- Form labels properly associated

**Example**:
```php
<form action="<?php echo JRoute::_('index.php'); ?>" method="post">
    <label for="event-title">
        <?php echo JText::_('COM_MOKOEVENTS_FIELD_TITLE'); ?>
        <span class="required" aria-label="required">*</span>
    </label>
    <input type="text"
           id="event-title"
           name="jform[title]"
           required
           aria-required="true"
           aria-describedby="title-desc">
    <p id="title-desc" class="help-text">
        <?php echo JText::_('COM_MOKOEVENTS_FIELD_TITLE_DESC'); ?>
    </p>

    <?php echo JHtml::_('form.token'); ?>
</form>
```

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/development-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
