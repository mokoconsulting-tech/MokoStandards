#!/usr/bin/env python3
"""
Extension utilities for Joomla and Dolibarr.

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
INGROUP: Extension.Utils
REPO: https://github.com/mokoconsulting-tech/moko-cassiopeia
PATH: /scripts/lib/extension_utils.py
VERSION: 03.01.02
BRIEF: Platform-aware extension utilities for Joomla and Dolibarr
"""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union


class Platform(Enum):
    """Supported extension platforms."""
    JOOMLA = "joomla"
    DOLIBARR = "dolibarr"
    UNKNOWN = "unknown"


@dataclass
class ExtensionInfo:
    """Extension information."""
    platform: Platform
    name: str
    version: str
    extension_type: str
    manifest_path: Path
    description: Optional[str] = None
    author: Optional[str] = None
    author_email: Optional[str] = None
    license: Optional[str] = None


def detect_joomla_manifest(src_dir: Union[str, Path]) -> Optional[Path]:
    """
    Detect Joomla manifest file.

    Args:
        src_dir: Source directory

    Returns:
        Path to manifest file or None
    """
    src_path = Path(src_dir)

    # Common Joomla manifest locations and patterns
    manifest_patterns = [
        "templateDetails.xml",
        "pkg_*.xml",
        "com_*.xml",
        "mod_*.xml",
        "plg_*.xml",
    ]

    # Search in src_dir and subdirectories (max depth 4)
    for pattern in manifest_patterns:
        # Direct match
        matches = list(src_path.glob(pattern))
        if matches:
            return matches[0]

        # Search in subdirectories
        matches = list(src_path.glob(f"*/{pattern}"))
        if matches:
            return matches[0]

        matches = list(src_path.glob(f"*/*/{pattern}"))
        if matches:
            return matches[0]

    # Fallback: search for any XML with <extension tag
    for xml_file in src_path.rglob("*.xml"):
        if xml_file.name.startswith("."):
            continue
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            if root.tag == "extension":
                return xml_file
        except Exception:
            continue

    return None


def detect_dolibarr_manifest(src_dir: Union[str, Path]) -> Optional[Path]:
    """
    Detect Dolibarr module descriptor file.

    Args:
        src_dir: Source directory

    Returns:
        Path to descriptor file or None
    """
    src_path = Path(src_dir)

    # Dolibarr module descriptors follow pattern: core/modules/mod*.class.php
    descriptor_patterns = [
        "core/modules/mod*.class.php",
        "*/modules/mod*.class.php",
        "mod*.class.php",
    ]

    for pattern in descriptor_patterns:
        matches = list(src_path.glob(pattern))
        if matches:
            # Verify it's actually a Dolibarr module descriptor
            # Look for extends DolibarrModules pattern
            for match in matches:
                try:
                    content = match.read_text(encoding="utf-8")
                    # Check for Dolibarr module inheritance pattern
                    if re.search(r'extends\s+DolibarrModules', content):
                        return match
                except Exception:
                    continue

    return None


def parse_joomla_manifest(manifest_path: Path) -> Optional[ExtensionInfo]:
    """
    Parse Joomla manifest XML.

    Args:
        manifest_path: Path to manifest file

    Returns:
        ExtensionInfo or None
    """
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()

        if root.tag != "extension":
            return None

        # Get extension type
        ext_type = root.get("type", "unknown")

        # Get name
        name_elem = root.find("name")
        name = name_elem.text if name_elem is not None else "unknown"

        # Get version
        version_elem = root.find("version")
        version = version_elem.text if version_elem is not None else "0.0.0"

        # Get description
        desc_elem = root.find("description")
        description = desc_elem.text if desc_elem is not None else None

        # Get author
        author_elem = root.find("author")
        author = author_elem.text if author_elem is not None else None

        # Get author email
        author_email_elem = root.find("authorEmail")
        author_email = author_email_elem.text if author_email_elem is not None else None

        # Get license
        license_elem = root.find("license")
        license_text = license_elem.text if license_elem is not None else None

        return ExtensionInfo(
            platform=Platform.JOOMLA,
            name=name,
            version=version,
            extension_type=ext_type,
            manifest_path=manifest_path,
            description=description,
            author=author,
            author_email=author_email,
            license=license_text
        )

    except Exception:
        return None


def parse_dolibarr_descriptor(descriptor_path: Path) -> Optional[ExtensionInfo]:
    """
    Parse Dolibarr module descriptor PHP file.

    Args:
        descriptor_path: Path to descriptor file

    Returns:
        ExtensionInfo or None
    """
    try:
        content = descriptor_path.read_text(encoding="utf-8")

        # Extract module name from class that extends DolibarrModules
        # Pattern: class ModMyModule extends DolibarrModules
        class_match = re.search(r'class\s+(\w+)\s+extends\s+DolibarrModules', content)
        if not class_match:
            # Fallback: try to find any class definition
            class_match = re.search(r'class\s+(\w+)', content)

        name = class_match.group(1) if class_match else "unknown"

        # Extract version
        version_match = re.search(r'\$this->version\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        version = version_match.group(1) if version_match else "0.0.0"

        # Extract description
        desc_match = re.search(r'\$this->description\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        description = desc_match.group(1) if desc_match else None

        # Extract author
        author_match = re.search(r'\$this->editor_name\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        author = author_match.group(1) if author_match else None

        return ExtensionInfo(
            platform=Platform.DOLIBARR,
            name=name,
            version=version,
            extension_type="module",
            manifest_path=descriptor_path,
            description=description,
            author=author,
            author_email=None,
            license=None
        )

    except Exception:
        return None


def get_extension_info(src_dir: Union[str, Path]) -> Optional[ExtensionInfo]:
    """
    Detect and parse extension information from source directory.
    Supports both Joomla and Dolibarr platforms.

    Args:
        src_dir: Source directory containing extension files

    Returns:
        ExtensionInfo or None if not detected
    """
    src_path = Path(src_dir)

    if not src_path.is_dir():
        return None

    # Try Joomla first
    joomla_manifest = detect_joomla_manifest(src_path)
    if joomla_manifest:
        ext_info = parse_joomla_manifest(joomla_manifest)
        if ext_info:
            return ext_info

    # Try Dolibarr
    dolibarr_descriptor = detect_dolibarr_manifest(src_path)
    if dolibarr_descriptor:
        ext_info = parse_dolibarr_descriptor(dolibarr_descriptor)
        if ext_info:
            return ext_info

    return None


def is_joomla_extension(src_dir: Union[str, Path]) -> bool:
    """
    Check if directory contains a Joomla extension.

    Args:
        src_dir: Source directory

    Returns:
        True if Joomla extension detected
    """
    ext_info = get_extension_info(src_dir)
    return ext_info is not None and ext_info.platform == Platform.JOOMLA


def is_dolibarr_extension(src_dir: Union[str, Path]) -> bool:
    """
    Check if directory contains a Dolibarr module.

    Args:
        src_dir: Source directory

    Returns:
        True if Dolibarr module detected
    """
    ext_info = get_extension_info(src_dir)
    return ext_info is not None and ext_info.platform == Platform.DOLIBARR


def main() -> None:
    """Test the extension utilities."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import common

    common.log_section("Testing Extension Utilities")

    # Test with current directory's src
    repo_root = common.repo_root()
    src_dir = repo_root / "src"

    if not src_dir.is_dir():
        common.log_warn(f"Source directory not found: {src_dir}")
        return

    ext_info = get_extension_info(src_dir)

    if ext_info:
        common.log_success("Extension detected!")
        common.log_kv("Platform", ext_info.platform.value.upper())
        common.log_kv("Name", ext_info.name)
        common.log_kv("Version", ext_info.version)
        common.log_kv("Type", ext_info.extension_type)
        common.log_kv("Manifest", str(ext_info.manifest_path))
        if ext_info.description:
            common.log_kv("Description", ext_info.description[:60] + "...")
        if ext_info.author:
            common.log_kv("Author", ext_info.author)
    else:
        common.log_error("No extension detected")
        sys.exit(1)


if __name__ == "__main__":
    main()
