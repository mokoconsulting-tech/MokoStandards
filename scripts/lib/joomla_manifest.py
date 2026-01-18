#!/usr/bin/env python3
"""
Joomla manifest parsing and validation utilities.

Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
along with this program (./LICENSE.md).

FILE INFORMATION
DEFGROUP: Script.Library
INGROUP: Joomla.Manifest
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/lib/joomla_manifest.py
VERSION: 01.00.00
BRIEF: Joomla manifest parsing and validation utilities
"""

try:
    from defusedxml import ElementTree as ET
except ImportError:
    # Fallback to standard library if defusedxml is not available
    import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from . import common
except ImportError:
    import common


# ============================================================================
# Joomla Extension Types
# ============================================================================

class ExtensionType:
    """Joomla extension types."""
    COMPONENT = "component"
    MODULE = "module"
    PLUGIN = "plugin"
    TEMPLATE = "template"
    LIBRARY = "library"
    PACKAGE = "package"
    FILE = "file"
    LANGUAGE = "language"
    
    ALL_TYPES = [
        COMPONENT, MODULE, PLUGIN, TEMPLATE,
        LIBRARY, PACKAGE, FILE, LANGUAGE
    ]


# ============================================================================
# Manifest Data Class
# ============================================================================

@dataclass
class ManifestInfo:
    """Information extracted from a Joomla manifest."""
    path: Path
    extension_type: str
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    author_email: Optional[str] = None
    author_url: Optional[str] = None
    copyright: Optional[str] = None
    license: Optional[str] = None
    creation_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "path": str(self.path),
            "ext_type": self.extension_type,
            "name": self.name,
            "version": self.version,
            "description": self.description or "",
            "author": self.author or "",
            "author_email": self.author_email or "",
            "author_url": self.author_url or "",
            "copyright": self.copyright or "",
            "license": self.license or "",
            "creation_date": self.creation_date or ""
        }


# ============================================================================
# Manifest Discovery
# ============================================================================

def find_manifest(src_dir: str = "src") -> Path:
    """
    Find the primary Joomla manifest in the given directory.
    
    Args:
        src_dir: Source directory to search
        
    Returns:
        Path to manifest file
        
    Raises:
        SystemExit: If no manifest found
    """
    src_path = Path(src_dir)
    
    if not src_path.is_dir():
        common.die(f"Source directory missing: {src_dir}")
    
    # Template manifest (templateDetails.xml)
    template_manifest = src_path / "templateDetails.xml"
    if template_manifest.is_file():
        return template_manifest
    
    # Also check in templates subdirectory
    templates_dir = src_path / "templates"
    if templates_dir.is_dir():
        for template_file in templates_dir.glob("templateDetails.xml"):
            return template_file
    
    # Package manifest (pkg_*.xml)
    pkg_manifests = list(src_path.rglob("pkg_*.xml"))
    if pkg_manifests:
        return pkg_manifests[0]
    
    # Component manifest (com_*.xml)
    com_manifests = list(src_path.rglob("com_*.xml"))
    if com_manifests:
        return com_manifests[0]
    
    # Module manifest (mod_*.xml)
    mod_manifests = list(src_path.rglob("mod_*.xml"))
    if mod_manifests:
        return mod_manifests[0]
    
    # Plugin manifest (plg_*.xml)
    plg_manifests = list(src_path.rglob("plg_*.xml"))
    if plg_manifests:
        return plg_manifests[0]
    
    # Fallback: any XML with <extension
    for xml_file in src_path.rglob("*.xml"):
        try:
            content = xml_file.read_text(encoding="utf-8")
            if "<extension" in content:
                return xml_file
        except Exception:
            continue
    
    common.die(f"No Joomla manifest XML found under {src_dir}")


def find_all_manifests(src_dir: str = "src") -> List[Path]:
    """
    Find all Joomla manifests in the given directory.
    
    Args:
        src_dir: Source directory to search
        
    Returns:
        List of manifest paths
    """
    src_path = Path(src_dir)
    
    if not src_path.is_dir():
        return []
    
    manifests = []
    
    # Template manifests
    manifests.extend(src_path.rglob("templateDetails.xml"))
    
    # Package manifests
    manifests.extend(src_path.rglob("pkg_*.xml"))
    
    # Component manifests
    manifests.extend(src_path.rglob("com_*.xml"))
    
    # Module manifests
    manifests.extend(src_path.rglob("mod_*.xml"))
    
    # Plugin manifests
    manifests.extend(src_path.rglob("plg_*.xml"))
    
    return manifests


# ============================================================================
# Manifest Parsing
# ============================================================================

def parse_manifest(manifest_path: Path) -> ManifestInfo:
    """
    Parse a Joomla manifest file.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        ManifestInfo object
        
    Raises:
        SystemExit: If parsing fails
    """
    if not manifest_path.is_file():
        common.die(f"Manifest not found: {manifest_path}")
    
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        # Extract extension type
        ext_type = root.attrib.get("type", "").strip().lower()
        if not ext_type:
            common.die(f"Manifest missing type attribute: {manifest_path}")
        
        # Extract name
        name_elem = root.find("name")
        if name_elem is None or not name_elem.text:
            common.die(f"Manifest missing name element: {manifest_path}")
        name = name_elem.text.strip()
        
        # Extract version
        version_elem = root.find("version")
        if version_elem is None or not version_elem.text:
            common.die(f"Manifest missing version element: {manifest_path}")
        version = version_elem.text.strip()
        
        # Extract optional fields
        description = None
        desc_elem = root.find("description")
        if desc_elem is not None and desc_elem.text:
            description = desc_elem.text.strip()
        
        author = None
        author_elem = root.find("author")
        if author_elem is not None and author_elem.text:
            author = author_elem.text.strip()
        
        author_email = None
        email_elem = root.find("authorEmail")
        if email_elem is not None and email_elem.text:
            author_email = email_elem.text.strip()
        
        author_url = None
        url_elem = root.find("authorUrl")
        if url_elem is not None and url_elem.text:
            author_url = url_elem.text.strip()
        
        copyright_text = None
        copyright_elem = root.find("copyright")
        if copyright_elem is not None and copyright_elem.text:
            copyright_text = copyright_elem.text.strip()
        
        license_text = None
        license_elem = root.find("license")
        if license_elem is not None and license_elem.text:
            license_text = license_elem.text.strip()
        
        creation_date = None
        date_elem = root.find("creationDate")
        if date_elem is not None and date_elem.text:
            creation_date = date_elem.text.strip()
        
        return ManifestInfo(
            path=manifest_path,
            extension_type=ext_type,
            name=name,
            version=version,
            description=description,
            author=author,
            author_email=author_email,
            author_url=author_url,
            copyright=copyright_text,
            license=license_text,
            creation_date=creation_date
        )
        
    except ET.ParseError as e:
        common.die(f"Failed to parse manifest {manifest_path}: {e}")
    except Exception as e:
        common.die(f"Error reading manifest {manifest_path}: {e}")


def get_manifest_version(manifest_path: Path) -> str:
    """
    Extract version from manifest.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        Version string
    """
    info = parse_manifest(manifest_path)
    return info.version


def get_manifest_name(manifest_path: Path) -> str:
    """
    Extract name from manifest.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        Name string
    """
    info = parse_manifest(manifest_path)
    return info.name


def get_manifest_type(manifest_path: Path) -> str:
    """
    Extract extension type from manifest.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        Extension type string
    """
    info = parse_manifest(manifest_path)
    return info.extension_type


# ============================================================================
# Manifest Validation
# ============================================================================

def validate_manifest(manifest_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a Joomla manifest.
    
    Args:
        manifest_path: Path to manifest file
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
    """
    warnings = []
    
    try:
        info = parse_manifest(manifest_path)
        
        # Check for recommended fields
        if not info.description:
            warnings.append("Missing description element")
        
        if not info.author:
            warnings.append("Missing author element")
        
        if not info.copyright:
            warnings.append("Missing copyright element")
        
        if not info.license:
            warnings.append("Missing license element")
        
        if not info.creation_date:
            warnings.append("Missing creationDate element")
        
        # Validate extension type
        if info.extension_type not in ExtensionType.ALL_TYPES:
            warnings.append(f"Unknown extension type: {info.extension_type}")
        
        return (True, warnings)
        
    except SystemExit:
        return (False, ["Failed to parse manifest"])


# ============================================================================
# Main Entry Point (for testing)
# ============================================================================

def main() -> None:
    """Test the manifest utilities."""
    import sys
    
    common.log_section("Testing Joomla Manifest Utilities")
    
    src_dir = sys.argv[1] if len(sys.argv) > 1 else "src"
    
    try:
        manifest = find_manifest(src_dir)
        common.log_success(f"Found manifest: {manifest}")
        
        info = parse_manifest(manifest)
        
        common.log_section("Manifest Information")
        common.log_kv("Type", info.extension_type)
        common.log_kv("Name", info.name)
        common.log_kv("Version", info.version)
        
        if info.description:
            common.log_kv("Description", info.description[:60] + "..." if len(info.description) > 60 else info.description)
        
        if info.author:
            common.log_kv("Author", info.author)
        
        is_valid, warnings = validate_manifest(manifest)
        
        if is_valid:
            common.log_success("Manifest is valid")
            if warnings:
                common.log_warn(f"Warnings: {len(warnings)}")
                for warning in warnings:
                    print(f"  - {warning}")
        else:
            common.log_error("Manifest validation failed")
            
    except SystemExit as e:
        sys.exit(e.code)


if __name__ == "__main__":
    main()
