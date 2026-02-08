#!/usr/bin/env python3
"""
SHA-256 Hash Update Script

This script automatically updates SHA-256 hashes in workflow files when
the corresponding source files change. It ensures that security verification
hashes stay in sync with file modifications.

Usage:
    python3 update_sha_hashes.py [--dry-run] [--verbose]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 03.01.01
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Configuration: Map source files to their workflow locations
SHA_MAPPINGS = [
    {
        'source_file': 'scripts/validate/validate_codeql_config.py',
        'workflow_file': '.github/workflows/standards-compliance.yml',
        'pattern': r'EXPECTED_SHA256="([a-f0-9]{64})"',
        'description': 'CodeQL configuration validator'
    }
]


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Hexadecimal SHA-256 hash string
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def update_sha_in_file(
    workflow_file: Path,
    pattern: str,
    new_hash: str,
    dry_run: bool = False
) -> Tuple[bool, str, str]:
    """Update SHA-256 hash in workflow file.
    
    Args:
        workflow_file: Path to workflow file
        pattern: Regex pattern to find the hash
        new_hash: New hash value to set
        dry_run: If True, don't actually write changes
        
    Returns:
        Tuple of (changed, old_hash, new_hash)
    """
    with open(workflow_file, 'r') as f:
        content = f.read()
    
    # Find current hash
    match = re.search(pattern, content)
    if not match:
        return False, '', new_hash
    
    old_hash = match.group(1)
    
    # Check if update needed
    if old_hash == new_hash:
        return False, old_hash, new_hash
    
    # Replace hash
    new_content = re.sub(pattern, f'EXPECTED_SHA256="{new_hash}"', content)
    
    if not dry_run:
        with open(workflow_file, 'w') as f:
            f.write(new_content)
    
    return True, old_hash, new_hash


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Update SHA-256 hashes in workflow files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).parent.parent.parent
    
    print("🔐 SHA-256 Hash Update Script")
    print("=" * 60)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("=" * 60)
    
    changes_made = False
    errors = []
    
    for mapping in SHA_MAPPINGS:
        source_path = repo_root / mapping['source_file']
        workflow_path = repo_root / mapping['workflow_file']
        
        print(f"\n📄 Processing: {mapping['description']}")
        print(f"   Source: {mapping['source_file']}")
        
        # Check if source file exists
        if not source_path.exists():
            error_msg = f"❌ Source file not found: {source_path}"
            print(error_msg)
            errors.append(error_msg)
            continue
        
        # Check if workflow file exists
        if not workflow_path.exists():
            error_msg = f"❌ Workflow file not found: {workflow_path}"
            print(error_msg)
            errors.append(error_msg)
            continue
        
        # Calculate current hash
        current_hash = calculate_sha256(source_path)
        if args.verbose:
            print(f"   Current SHA-256: {current_hash}")
        
        # Update workflow file
        changed, old_hash, new_hash = update_sha_in_file(
            workflow_path,
            mapping['pattern'],
            current_hash,
            args.dry_run
        )
        
        if changed:
            changes_made = True
            print(f"   ✅ Hash updated in: {mapping['workflow_file']}")
            print(f"      Old: {old_hash}")
            print(f"      New: {new_hash}")
            if args.dry_run:
                print(f"      (Would be updated - dry run mode)")
        else:
            if old_hash == new_hash:
                print(f"   ℹ️  Hash already up to date")
            else:
                print(f"   ⚠️  No hash found to update")
    
    print("\n" + "=" * 60)
    
    if errors:
        print(f"❌ Completed with {len(errors)} error(s)")
        for error in errors:
            print(f"   {error}")
        return 1
    
    if changes_made:
        if args.dry_run:
            print("✅ Changes detected (dry run - no files modified)")
        else:
            print("✅ All SHA-256 hashes updated successfully")
        return 0
    else:
        print("ℹ️  No changes needed - all hashes up to date")
        return 0


if __name__ == '__main__':
    sys.exit(main())
