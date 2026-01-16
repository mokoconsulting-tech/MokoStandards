#!/usr/bin/env python3
# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Documentation Index Generator

Scans the documentation directory and generates index.md files for each folder.
Index files list immediate child markdown files and subfolders with links.

Usage:
  python rebuild_indexes.py [--root DOCS_ROOT] [--check]

Options:
  --root DOCS_ROOT    Root documentation directory (default: docs)
  --check             Check mode: exit nonzero if changes would occur
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple


EXCLUDED_DIRS = {'.git', 'node_modules', 'vendor', 'dist', 'build'}
INDEX_FILENAME = 'index.md'
PROJECT_NAME = 'MokoStandards'


def is_excluded_dir(dir_name: str) -> bool:
    """Check if directory should be excluded from indexing."""
    return dir_name.startswith('.') or dir_name in EXCLUDED_DIRS


def get_folder_context_title(folder_path: Path, root_path: Path) -> str:
    """Generate a contextual title for the folder."""
    relative_path = folder_path.relative_to(root_path.parent)
    return f"Docs Index: /{relative_path}"


def get_immediate_children(folder_path: Path) -> Tuple[List[Path], List[Path]]:
    """
    Get immediate child folders and markdown files.
    
    Returns:
        Tuple of (child_folders, child_files) sorted alphabetically
    """
    if not folder_path.is_dir():
        return [], []
    
    child_folders = []
    child_files = []
    
    try:
        for item in folder_path.iterdir():
            if item.is_dir() and not is_excluded_dir(item.name):
                child_folders.append(item)
            elif item.is_file() and item.suffix == '.md' and item.name != INDEX_FILENAME:
                child_files.append(item)
    except PermissionError as exc:
        # Intentionally skip folders we cannot read; log for diagnostics.
        print(f"Warning: cannot access directory '{folder_path}': {exc}", file=sys.stderr)
    
    # Sort alphabetically for deterministic output
    child_folders.sort(key=lambda p: p.name.lower())
    child_files.sort(key=lambda p: p.name.lower())
    
    return child_folders, child_files


def add_section_with_subdirs(
    lines: List[str],
    categories: dict,
    category_key: str,
    section_title: str,
    section_description: str,
) -> None:
    """Append a section grouped by subdirectories to the lines list.

    This groups entries in categories[category_key] by their directory path,
    using 'General' for items not in a specific subdirectory, and then
    renders an H2 section header, an optional description, and bullet links.
    """
    items = categories.get(category_key) or []
    if not items:
        return

    lines.append(f"## {section_title}")
    lines.append("")
    if section_description:
        lines.append(section_description)
        lines.append("")

    # Group by subdirectory
    groups: dict = {}
    for name, path, dir_path in items:
        if "/" in dir_path and dir_path != category_key.lower():
            parts = dir_path.split("/")
            subdir = parts[1] if len(parts) > 1 else category_key.lower()
        else:
            subdir = "General"

        groups.setdefault(subdir, []).append((name, path))

    for subdir in sorted(groups.keys()):
        if subdir != "General":
            lines.append(f"### {subdir.upper()}")
            lines.append("")
        for name, path in sorted(groups[subdir]):
            lines.append(f"- [{name}](./{path})")
        lines.append("")


def generate_catalog_content(root_path: Path) -> str:
    """Generate comprehensive catalog content for the root docs/index.md file."""
    lines = [
        f"# {PROJECT_NAME} Documentation Catalog",
        "",
        f"This is a comprehensive catalog of all documentation in the {PROJECT_NAME} repository.",
        "",
        "## Quick Links",
        "",
        "- [README](./README.md) - Documentation governance framework",
        "- [ROADMAP](./ROADMAP.md) - Documentation roadmap and future plans",
        "",
    ]
    
    # Collect all documentation organized by category
    categories = {
        'Policies': [],
        'Guides': [],
        'Checklists': [],
        'Glossaries': [],
        'Product Documentation': [],
        'Reference': [],
        'Reports': []
    }
    
    # Walk through all documentation
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        dirnames.sort()
        
        rel_path = Path(dirpath).relative_to(root_path)
        
        # Categorize files
        for filename in sorted(filenames):
            if filename.endswith('.md') and filename not in ['index.md', 'README.md', 'ROADMAP.md']:
                file_path = Path(dirpath) / filename
                rel_file_path = file_path.relative_to(root_path)
                display_name = filename[:-3]  # Remove .md extension
                
                # Determine category based on path
                path_str = str(rel_path)
                if path_str.startswith('policy'):
                    categories['Policies'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('guide'):
                    categories['Guides'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('checklist'):
                    categories['Checklists'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('glossary'):
                    categories['Glossaries'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('products'):
                    categories['Product Documentation'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('reference'):
                    categories['Reference'].append((display_name, rel_file_path, path_str))
                elif path_str.startswith('reports'):
                    categories['Reports'].append((display_name, rel_file_path, path_str))
    
    # Add Policies section
    add_section_with_subdirs(
        lines,
        categories,
        category_key="Policies",
        section_title="Policies",
        section_description="Standards, requirements, and compliance documentation.",
    )
    
    # Add Guides section
    add_section_with_subdirs(
        lines,
        categories,
        category_key="Guides",
        section_title="Guides",
        section_description="Step-by-step tutorials and how-to documentation.",
    )
    
    # Add other categories
    for category_name, items in [
        ('Checklists', categories['Checklists']),
        ('Glossaries', categories['Glossaries']),
        ('Product Documentation', categories['Product Documentation']),
        ('Reference', categories['Reference']),
        ('Reports', categories['Reports'])
    ]:
        if items:
            lines.append(f"## {category_name}")
            lines.append("")
            for name, path, _ in sorted(items):
                lines.append(f"- [{name}](./{path})")
            lines.append("")
    
    # Add directory navigation
    lines.extend([
        "## Directory Structure",
        "",
        "Browse documentation by folder:",
        "",
        "- [checklist/](./checklist/index.md) - Checklists and procedures",
        "- [glossary/](./glossary/index.md) - Terminology definitions",
        "- [guide/](./guide/index.md) - How-to guides and tutorials",
        "- [policy/](./policy/index.md) - Policies and standards",
        "- [products/](./products/index.md) - Product-specific documentation",
        "- [reference/](./reference/index.md) - Technical references and directories",
        "- [reports/](./reports/index.md) - Reports and status documents",
        "",
    ])
    
    # Add metadata
    lines.extend([
        "## Metadata",
        "",
        "- **Document Type:** catalog",
        "- **Auto-generated:** This file is automatically generated by rebuild_indexes.py",
        "- **Last Updated:** This catalog is regenerated whenever documentation is added or removed",
        "",
        "## Revision History",
        "",
        "| Change | Notes | Author |",
        "| --- | --- | --- |",
        "| Automated update | Generated by documentation index automation | rebuild_indexes.py |",
        ""
    ])
    
    return '\n'.join(lines)


def generate_index_content(folder_path: Path, root_path: Path) -> str:
    """Generate the content for an index.md file."""
    # Special handling for root docs directory - generate full catalog
    if folder_path == root_path:
        return generate_catalog_content(root_path)
    
    title = get_folder_context_title(folder_path, root_path)
    child_folders, child_files = get_immediate_children(folder_path)
    
    # Build content
    lines = [
        f"# {title}",
        "",
        "## Purpose",
        "",
        "This index provides navigation to documentation within this folder.",
        "",
    ]
    
    # Add folders section if there are any
    if child_folders:
        lines.append("## Subfolders")
        lines.append("")
        for folder in child_folders:
            folder_name = folder.name
            # Link to the index.md in the subfolder
            lines.append(f"- [{folder_name}/](./{folder_name}/index.md)")
        lines.append("")
    
    # Add files section if there are any
    if child_files:
        lines.append("## Documents")
        lines.append("")
        for file in child_files:
            file_name = file.name
            # Display name without .md extension
            display_name = file_name[:-3] if file_name.endswith('.md') else file_name
            lines.append(f"- [{display_name}](./{file_name})")
        lines.append("")
    
    # Add metadata section
    lines.extend([
        "## Metadata",
        "",
        "- **Document Type:** index",
        "- **Auto-generated:** This file is automatically generated by rebuild_indexes.py",
        "",
        "## Revision History",
        "",
        "| Change | Notes | Author |",
        "| --- | --- | --- |",
        "| Automated update | Generated by documentation index automation | rebuild_indexes.py |",
        ""
    ])
    
    return '\n'.join(lines)


def process_directory(folder_path: Path, root_path: Path, check_mode: bool = False) -> bool:
    """
    Process a directory and create/update its index.md file.
    
    Returns:
        True if changes were made (or would be made in check mode), False otherwise
    """
    index_file = folder_path / INDEX_FILENAME
    
    try:
        new_content = generate_index_content(folder_path, root_path)
    except Exception as e:
        print(f"ERROR: Failed to generate content for {folder_path}: {e}", file=sys.stderr)
        return False
    
    # Check if file exists and compare content
    try:
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            if existing_content == new_content:
                return False  # No changes needed
    except (IOError, UnicodeDecodeError) as e:
        print(f"WARNING: Error reading {index_file}: {e}", file=sys.stderr)
        # Continue to try writing the new content
    
    # Changes needed
    if check_mode:
        print(f"Would update: {index_file.relative_to(root_path.parent)}")
        return True
    else:
        try:
            print(f"Writing: {index_file.relative_to(root_path.parent)}")
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except (IOError, PermissionError) as e:
            print(f"ERROR: Failed to write {index_file}: {e}", file=sys.stderr)
            return False


def scan_and_generate(root_path: Path, check_mode: bool = False) -> int:
    """
    Scan the documentation tree and generate index files.
    
    Returns:
        0 if no changes (or all successful), 1 if changes would occur in check mode
    """
    if not root_path.exists():
        print(f"ERROR: Documentation root not found: {root_path}", file=sys.stderr)
        return 1
    
    if not root_path.is_dir():
        print(f"ERROR: Documentation root is not a directory: {root_path}", file=sys.stderr)
        return 1
    
    changes_detected = False
    
    # Process root directory
    if process_directory(root_path, root_path, check_mode):
        changes_detected = True
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        
        # Sort for deterministic order
        dirnames.sort()
        
        # Process each subdirectory
        for dirname in dirnames:
            folder_path = Path(dirpath) / dirname
            if process_directory(folder_path, root_path, check_mode):
                changes_detected = True
    
    if check_mode and changes_detected:
        print("\nERROR: Documentation indexes are out of date", file=sys.stderr)
        print("Run 'python scripts/docs/rebuild_indexes.py' to update them", file=sys.stderr)
        return 1
    
    if not check_mode:
        print("\nDocumentation indexes updated successfully")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate index.md files for documentation folders'
    )
    parser.add_argument(
        '--root',
        default='docs',
        help='Root documentation directory (default: docs)'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check mode: exit nonzero if changes would occur'
    )
    
    args = parser.parse_args()
    
    # Resolve root path
    root_path = Path(args.root).resolve()
    
    # Run the scan and generate
    exit_code = scan_and_generate(root_path, args.check)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
