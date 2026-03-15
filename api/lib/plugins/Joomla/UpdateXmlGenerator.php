<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Joomla
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/plugins/Joomla/UpdateXmlGenerator.php
 * VERSION: 04.00.15
 * BRIEF: Generates and updates Joomla extension update.xml files
 */

declare(strict_types=1);

namespace MokoStandards\Plugins\Joomla;

use DOMDocument;
use DOMElement;
use Exception;

/**
 * Joomla Update XML Generator
 * 
 * Generates and updates update.xml files for Joomla extensions
 * following the Joomla update server specification
 */
class UpdateXmlGenerator
{
    private string $extensionName;
    private string $extensionType;
    private string $element;
    private string $clientId;
    
    /**
     * Constructor
     * 
     * @param string $extensionName Human-readable extension name
     * @param string $extensionType Extension type (component, module, plugin, etc.)
     * @param string $element Extension element (e.g., com_example, mod_custom)
     * @param string $clientId Client ID (0 for site, 1 for admin)
     */
    public function __construct(
        string $extensionName,
        string $extensionType = 'component',
        string $element = '',
        string $clientId = '0'
    ) {
        $this->extensionName = $extensionName;
        $this->extensionType = $extensionType;
        $this->element = $element ?: $this->deriveElement($extensionName, $extensionType);
        $this->clientId = $clientId;
    }
    
    /**
     * Generate update.xml from release information
     * 
     * @param array $release Release information
     * @return string XML content
     */
    public function generate(array $release): string
    {
        $dom = new DOMDocument('1.0', 'UTF-8');
        $dom->formatOutput = true;
        $dom->preserveWhiteSpace = false;
        
        // Create root element
        $updates = $dom->createElement('updates');
        $dom->appendChild($updates);
        
        // Add update entry
        $this->addUpdateEntry($dom, $updates, $release);
        
        return $dom->saveXML();
    }
    
    /**
     * Update existing update.xml file with new release
     * 
     * @param string $xmlPath Path to existing update.xml
     * @param array $release New release information
     * @return string Updated XML content
     * @throws Exception If XML cannot be parsed
     */
    public function update(string $xmlPath, array $release): string
    {
        if (!file_exists($xmlPath)) {
            return $this->generate($release);
        }
        
        $dom = new DOMDocument('1.0', 'UTF-8');
        $dom->formatOutput = true;
        $dom->preserveWhiteSpace = false;
        
        if (!@$dom->load($xmlPath)) {
            throw new Exception("Failed to parse existing update.xml at {$xmlPath}");
        }
        
        $updates = $dom->getElementsByTagName('updates')->item(0);
        if (!$updates) {
            throw new Exception("Invalid update.xml: missing <updates> root element");
        }
        
        // Check if this version already exists
        $version = $release['version'];
        $existingUpdates = $updates->getElementsByTagName('update');
        
        foreach ($existingUpdates as $existingUpdate) {
            $versionNode = $existingUpdate->getElementsByTagName('version')->item(0);
            if ($versionNode && $versionNode->textContent === $version) {
                // Remove existing entry for this version
                $updates->removeChild($existingUpdate);
                break;
            }
        }
        
        // Add new update entry at the beginning
        $this->addUpdateEntry($dom, $updates, $release, true);
        
        return $dom->saveXML();
    }
    
    /**
     * Add an update entry to the XML document
     * 
     * @param DOMDocument $dom DOM document
     * @param DOMElement $updates Updates element
     * @param array $release Release information
     * @param bool $prepend Whether to prepend (insert at beginning)
     */
    private function addUpdateEntry(
        DOMDocument $dom,
        DOMElement $updates,
        array $release,
        bool $prepend = false
    ): void {
        $update = $dom->createElement('update');
        
        // Required fields
        $this->addElement($dom, $update, 'name', $this->extensionName);
        $this->addElement($dom, $update, 'description', $release['description'] ?? '');
        $this->addElement($dom, $update, 'element', $this->element);
        $this->addElement($dom, $update, 'type', $this->extensionType);
        $this->addElement($dom, $update, 'version', $release['version']);
        
        // Joomla target platform
        $infourl = $this->addElement($dom, $update, 'infourl', $release['infourl'] ?? '');
        if (!empty($release['infourl'])) {
            $infourl->setAttribute('title', 'Release Information');
        }
        
        // Downloads section
        $downloads = $dom->createElement('downloads');
        $update->appendChild($downloads);
        
        $downloadUrl = $this->addElement($dom, $downloads, 'downloadurl', $release['download_url']);
        $downloadUrl->setAttribute('type', 'full');
        $downloadUrl->setAttribute('format', 'zip');
        
        // Target platform
        if (!empty($release['target_platform'])) {
            $targetPlatform = $dom->createElement('targetplatform');
            $targetPlatform->setAttribute('name', 'joomla');
            $targetPlatform->setAttribute('version', $release['target_platform']);
            $update->appendChild($targetPlatform);
        }
        
        // Optional: PHP minimum version
        if (!empty($release['php_minimum'])) {
            $this->addElement($dom, $update, 'php_minimum', $release['php_minimum']);
        }
        
        // Optional: Tags
        if (!empty($release['tags'])) {
            $tags = $dom->createElement('tags');
            $update->appendChild($tags);
            foreach ($release['tags'] as $tag) {
                $this->addElement($dom, $tags, 'tag', $tag);
            }
        }
        
        // Optional: Maintainer information
        if (!empty($release['maintainer'])) {
            $this->addElement($dom, $update, 'maintainer', $release['maintainer']);
        }
        
        if (!empty($release['maintainer_url'])) {
            $this->addElement($dom, $update, 'maintainerurl', $release['maintainer_url']);
        }
        
        // Optional: Client (site or administrator)
        if ($this->clientId !== '0') {
            $this->addElement($dom, $update, 'client', $this->clientId);
        }
        
        // Optional: Checksums
        if (!empty($release['sha256'])) {
            $this->addElement($dom, $update, 'sha256', $release['sha256']);
        }
        
        if (!empty($release['sha384'])) {
            $this->addElement($dom, $update, 'sha384', $release['sha384']);
        }
        
        if (!empty($release['sha512'])) {
            $this->addElement($dom, $update, 'sha512', $release['sha512']);
        }
        
        // Add to updates element
        if ($prepend && $updates->firstChild) {
            $updates->insertBefore($update, $updates->firstChild);
        } else {
            $updates->appendChild($update);
        }
    }
    
    /**
     * Add a text element to parent
     * 
     * @param DOMDocument $dom DOM document
     * @param DOMElement $parent Parent element
     * @param string $name Element name
     * @param string $value Element value
     * @return DOMElement Created element
     */
    private function addElement(
        DOMDocument $dom,
        DOMElement $parent,
        string $name,
        string $value
    ): DOMElement {
        $element = $dom->createElement($name);
        $element->textContent = $value;
        $parent->appendChild($element);
        return $element;
    }
    
    /**
     * Derive element name from extension name and type
     * 
     * @param string $name Extension name
     * @param string $type Extension type
     * @return string Element name
     */
    private function deriveElement(string $name, string $type): string
    {
        $prefix = match($type) {
            'component' => 'com_',
            'module' => 'mod_',
            'plugin' => 'plg_',
            'library' => 'lib_',
            'template' => 'tpl_',
            'package' => 'pkg_',
            default => '',
        };
        
        // Convert name to lowercase and replace spaces with underscores
        $element = strtolower(preg_replace('/[^a-z0-9]+/i', '_', $name));
        
        // Add prefix if not already present
        if (!str_starts_with($element, $prefix)) {
            $element = $prefix . $element;
        }
        
        return $element;
    }
    
    /**
     * Validate update.xml structure
     * 
     * @param string $xmlContent XML content to validate
     * @return array Validation result ['valid' => bool, 'errors' => array]
     */
    public static function validate(string $xmlContent): array
    {
        $errors = [];
        
        $dom = new DOMDocument();
        libxml_use_internal_errors(true);
        
        if (!$dom->loadXML($xmlContent)) {
            foreach (libxml_get_errors() as $error) {
                $errors[] = "XML Error: {$error->message}";
            }
            libxml_clear_errors();
            return ['valid' => false, 'errors' => $errors];
        }
        
        // Validate structure
        $updates = $dom->getElementsByTagName('updates')->item(0);
        if (!$updates) {
            $errors[] = "Missing <updates> root element";
            return ['valid' => false, 'errors' => $errors];
        }
        
        $updateElements = $updates->getElementsByTagName('update');
        if ($updateElements->length === 0) {
            $errors[] = "No <update> elements found";
            return ['valid' => false, 'errors' => $errors];
        }
        
        // Validate each update entry
        foreach ($updateElements as $update) {
            $required = ['name', 'element', 'type', 'version'];
            foreach ($required as $field) {
                if ($update->getElementsByTagName($field)->length === 0) {
                    $errors[] = "Missing required field: <{$field}>";
                }
            }
            
            // Check for download URL
            $downloads = $update->getElementsByTagName('downloads');
            if ($downloads->length > 0) {
                $downloadUrl = $downloads->item(0)->getElementsByTagName('downloadurl');
                if ($downloadUrl->length === 0) {
                    $errors[] = "Missing <downloadurl> in <downloads>";
                }
            }
        }
        
        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }
    
    /**
     * Extract release information from manifest XML
     * 
     * @param string $manifestPath Path to extension manifest XML
     * @return array Release information
     * @throws Exception If manifest cannot be parsed
     */
    public static function extractFromManifest(string $manifestPath): array
    {
        if (!file_exists($manifestPath)) {
            throw new Exception("Manifest file not found: {$manifestPath}");
        }
        
        $dom = new DOMDocument();
        if (!@$dom->load($manifestPath)) {
            throw new Exception("Failed to parse manifest XML: {$manifestPath}");
        }
        
        $root = $dom->documentElement;
        
        return [
            'name' => self::getElementText($dom, 'name') ?: 'Unknown Extension',
            'version' => self::getElementText($dom, 'version') ?: '1.0.0',
            'description' => self::getElementText($dom, 'description') ?: '',
            'author' => self::getElementText($dom, 'author') ?: '',
            'author_url' => self::getElementText($dom, 'authorUrl') ?: '',
            'type' => $root->getAttribute('type') ?: 'component',
            'target_platform' => self::getElementText($dom, 'version', 'targetplatform') ?: '4.0',
        ];
    }
    
    /**
     * Get text content of an element
     * 
     * @param DOMDocument $dom DOM document
     * @param string $tagName Tag name
     * @param string $parentTag Optional parent tag name
     * @return string|null Element text content
     */
    private static function getElementText(
        DOMDocument $dom,
        string $tagName,
        string $parentTag = ''
    ): ?string {
        if ($parentTag) {
            $parents = $dom->getElementsByTagName($parentTag);
            if ($parents->length > 0) {
                $elements = $parents->item(0)->getElementsByTagName($tagName);
                if ($elements->length > 0) {
                    return trim($elements->item(0)->textContent);
                }
            }
        } else {
            $elements = $dom->getElementsByTagName($tagName);
            if ($elements->length > 0) {
                return trim($elements->item(0)->textContent);
            }
        }
        
        return null;
    }
}
