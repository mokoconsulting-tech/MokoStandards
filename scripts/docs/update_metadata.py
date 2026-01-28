#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Update Metadata and Revision History Script

This script updates all markdown documents to follow the standardized metadata
and revision history format defined in the document formatting policy.

Usage:
  python update_metadata.py [--dry-run] [--docs-root DOCS_ROOT]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

# Fixed metadata values
JURISDICTION = "Tennessee, USA"
OWNER = "Moko Consulting"
REPO_BASE = "https://github.com/mokoconsulting-tech/"
TARGET_VERSION = "02.00.00"
REVIEWED_DATE = "2026-01-28"
REVIEWED_BY = "Documentation Team"

# Domain mappings based on path
DOMAIN_MAP = {
    'policy': 'Governance',
    'guide': 'Documentation',
    'checklist': 'Operations',
    'reference': 'Reference',
    'reports': 'Operations',
    'adr': 'Architecture',
    'glossary': 'Reference',
    'products': 'Products',
    'deployment': 'Operations',
    'development': 'Development',
    'build-system': 'Development',
    'quickstart': 'Documentation',
    'release-management': 'Operations',
    'schemas': 'Documentation',
    'scripts': 'Development',
    'templates': 'Documentation',
    'workflows': 'Operations',
}

# Document type mappings based on path
DOCTYPE_MAP = {
    'policy': 'Policy',
    'guide': 'Guide',
    'checklist': 'Checklist',
    'reference': 'Reference',
    'reports': 'Report',
    'adr': 'ADR',
    'glossary': 'Glossary',
    'products': 'Guide',
    'deployment': 'Guide',
    'development': 'Guide',
    'build-system': 'Guide',
    'quickstart': 'Guide',
    'release-management': 'Guide',
    'schemas': 'Reference',
    'scripts': 'Guide',
    'templates': 'Template',
    'workflows': 'Guide',
}

# Files to skip
SKIP_FILES = {'index.md', 'README.md', 'ROADMAP.md'}


def get_doc_type_and_domain(file_path: Path, docs_root: Path) -> Tuple[str, str]:
    """Determine document type and domain based on file path."""
    rel_path = file_path.relative_to(docs_root)
    parts = rel_path.parts
    
    if len(parts) > 0:
        first_dir = parts[0]
        doc_type = DOCTYPE_MAP.get(first_dir, 'Guide')
        domain = DOMAIN_MAP.get(first_dir, 'Documentation')
        return doc_type, domain
    
    return 'Guide', 'Documentation'


def extract_current_version(content: str) -> Optional[str]:
    """Extract current version from file header."""
    version_match = re.search(r'^VERSION:\s*(\d+\.\d+\.\d+)', content, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    return None


def extract_metadata_section(content: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """Extract existing metadata section if it exists."""
    # Look for ## Metadata header
    metadata_match = re.search(r'^## Metadata\s*\n', content, re.MULTILINE)
    if not metadata_match:
        return None, None, None
    
    start_pos = metadata_match.start()
    
    # Find the next ## header or end of file
    next_section = re.search(r'\n## [^#]', content[metadata_match.end():])
    if next_section:
        end_pos = metadata_match.end() + next_section.start()
    else:
        end_pos = len(content)
    
    metadata_content = content[start_pos:end_pos]
    return metadata_content, start_pos, end_pos


def extract_revision_history(content: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """Extract existing revision history section if it exists."""
    # Look for ## Revision History header
    history_match = re.search(r'^## Revision History\s*\n', content, re.MULTILINE)
    if not history_match:
        return None, None, None
    
    start_pos = history_match.start()
    
    # Find the next ## header or end of file
    next_section = re.search(r'\n## [^#]', content[history_match.end():])
    if next_section:
        end_pos = history_match.end() + next_section.start()
    else:
        end_pos = len(content)
    
    history_content = content[start_pos:end_pos]
    return history_content, start_pos, end_pos


def create_metadata_section(file_path: Path, docs_root: Path, status: str = "Active") -> str:
    """Create a standardized metadata section."""
    doc_type, domain = get_doc_type_and_domain(file_path, docs_root)
    rel_path = file_path.relative_to(docs_root.parent)
    
    # Determine applies_to based on document type
    if doc_type in ['Policy', 'Guide']:
        applies_to = "All Repositories"
    else:
        applies_to = "Specific Projects"
    
    metadata = f"""## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | {doc_type}                                       |
| Domain         | {domain}                                         |
| Applies To     | {applies_to}                                     |
| Jurisdiction   | {JURISDICTION}                                   |
| Owner          | {OWNER}                                          |
| Repo           | {REPO_BASE}                                      |
| Path           | /{rel_path}                                      |
| Version        | {TARGET_VERSION}                                 |
| Status         | {status}                                         |
| Last Reviewed  | {REVIEWED_DATE}                                  |
| Reviewed By    | {REVIEWED_BY}                                    |
"""
    return metadata


def create_revision_history() -> str:
    """Create a standardized revision history section."""
    history = f"""## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| {REVIEWED_DATE} | Moko Consulting | Standardized metadata and revision history   | Updated to version {TARGET_VERSION} with all required fields |
"""
    return history


def update_document(file_path: Path, docs_root: Path, dry_run: bool = False) -> bool:
    """Update a single document with standardized metadata and revision history."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Failed to read {file_path}: {e}", file=sys.stderr)
        return False
    
    # Skip if file is empty or doesn't have proper markdown structure
    if not content.strip() or '# ' not in content:
        return False
    
    # Update VERSION in file header
    current_version = extract_current_version(content)
    if current_version and current_version != TARGET_VERSION:
        content = re.sub(
            r'^VERSION:\s*\d+\.\d+\.\d+',
            f'VERSION: {TARGET_VERSION}',
            content,
            flags=re.MULTILINE
        )
    
    # Extract and determine status
    status = "Active"
    if "Authoritative" in content[:500]:  # Check in first part of file
        status = "Authoritative"
    elif "Draft" in content[:500]:
        status = "Draft"
    elif "Deprecated" in content[:500]:
        status = "Deprecated"
    
    # Extract existing metadata
    metadata_section, metadata_start, metadata_end = extract_metadata_section(content)
    
    # Extract existing revision history
    history_section, history_start, history_end = extract_revision_history(content)
    
    # Create new sections
    new_metadata = create_metadata_section(file_path, docs_root, status)
    new_history = create_revision_history()
    
    # Update content
    if metadata_section:
        # Replace existing metadata
        content = content[:metadata_start] + new_metadata + "\n" + content[metadata_end:]
        # Adjust positions if we replaced metadata
        offset = len(new_metadata) - (metadata_end - metadata_start)
        if history_start is not None:
            history_start += offset
            history_end += offset
    else:
        # Add metadata at the end if not present
        if not content.endswith('\n'):
            content += '\n'
        content += '\n' + new_metadata + '\n'
    
    # Re-extract revision history with updated positions
    if history_section:
        _, history_start, history_end = extract_revision_history(content)
        if history_start is not None and history_end is not None:
            content = content[:history_start] + new_history
    else:
        # Add revision history at the end if not present
        if not content.endswith('\n'):
            content += '\n'
        content += '\n' + new_history
    
    # Write updated content
    if dry_run:
        print(f"Would update: {file_path.relative_to(docs_root.parent)}")
        return True
    else:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path.relative_to(docs_root.parent)}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to write {file_path}: {e}", file=sys.stderr)
            return False


def process_directory(docs_root: Path, dry_run: bool = False) -> Tuple[int, int]:
    """Process all markdown files in the documentation directory."""
    updated_count = 0
    skipped_count = 0
    
    for md_file in docs_root.rglob('*.md'):
        # Skip certain files
        if md_file.name in SKIP_FILES:
            skipped_count += 1
            continue
        
        # Skip auto-generated files
        if md_file.name == 'index.md':
            skipped_count += 1
            continue
        
        # Update the file
        if update_document(md_file, docs_root, dry_run):
            updated_count += 1
    
    return updated_count, skipped_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Update metadata and revision history in documentation files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    parser.add_argument(
        '--docs-root',
        default='docs',
        help='Root documentation directory (default: docs)'
    )
    
    args = parser.parse_args()
    
    docs_root = Path(args.docs_root).resolve()
    
    if not docs_root.exists():
        print(f"ERROR: Documentation root not found: {docs_root}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Processing documentation in: {docs_root}")
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
    print()
    
    updated_count, skipped_count = process_directory(docs_root, args.dry_run)
    
    print()
    print(f"Summary:")
    print(f"  Updated: {updated_count} files")
    print(f"  Skipped: {skipped_count} files")
    
    if args.dry_run:
        print()
        print("Run without --dry-run to apply changes")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
