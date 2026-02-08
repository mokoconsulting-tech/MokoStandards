#!/usr/bin/env python3
"""
Script Registry Validator

Validates all scripts against the registry to detect unauthorized modifications
or missing scripts. This ensures script integrity across the repository.

Usage:
    python3 validate_script_registry.py [--registry FILE] [--strict]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 03.01.02
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_registry(registry_file: Path) -> Dict:
    """Load script registry."""
    if not registry_file.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_file}")
    
    with open(registry_file, 'r') as f:
        return json.load(f)


def validate_scripts(
    registry: Dict,
    repo_root: Path,
    strict: bool = False
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Validate all scripts against registry.
    
    Returns:
        Tuple of (valid, modified, missing) scripts
    """
    valid = []
    modified = []
    missing = []
    
    for script_entry in registry.get('scripts', []):
        script_path = repo_root / script_entry['path']
        
        if not script_path.exists():
            missing.append(script_entry)
            continue
        
        try:
            current_sha = calculate_sha256(script_path)
            expected_sha = script_entry['sha256']
            
            if current_sha == expected_sha:
                valid.append(script_entry)
            else:
                modified.append({
                    **script_entry,
                    'current_sha256': current_sha
                })
        except Exception as e:
            print(f"⚠️  Error validating {script_entry['path']}: {e}")
            if strict:
                modified.append({
                    **script_entry,
                    'error': str(e)
                })
    
    return valid, modified, missing


def print_results(valid: List, modified: List, missing: List, verbose: bool = False):
    """Print validation results."""
    total = len(valid) + len(modified) + len(missing)
    
    print("\n" + "=" * 70)
    print("📊 Validation Results")
    print("=" * 70)
    
    # Summary
    print(f"\n✅ Valid:    {len(valid):3d} / {total} scripts")
    print(f"🔄 Modified: {len(modified):3d} / {total} scripts")
    print(f"❌ Missing:  {len(missing):3d} / {total} scripts")
    
    # Details for modified scripts
    if modified:
        print("\n" + "=" * 70)
        print("🔄 MODIFIED SCRIPTS (hash mismatch):")
        print("=" * 70)
        
        # Group by priority
        critical = [s for s in modified if s.get('priority') == 'critical']
        high = [s for s in modified if s.get('priority') == 'high']
        others = [s for s in modified if s.get('priority') not in ['critical', 'high']]
        
        if critical:
            print(f"\n⚠️  CRITICAL Priority ({len(critical)} scripts):")
            for script in critical:
                print(f"   {script['path']}")
                if verbose:
                    print(f"     Expected: {script['sha256'][:16]}...")
                    print(f"     Current:  {script.get('current_sha256', 'N/A')[:16]}...")
        
        if high:
            print(f"\n⚠️  HIGH Priority ({len(high)} scripts):")
            for script in high:
                print(f"   {script['path']}")
                if verbose:
                    print(f"     Expected: {script['sha256'][:16]}...")
                    print(f"     Current:  {script.get('current_sha256', 'N/A')[:16]}...")
        
        if others and verbose:
            print(f"\nℹ️  Other Priority ({len(others)} scripts):")
            for script in others:
                print(f"   {script['path']}")
    
    # Details for missing scripts
    if missing:
        print("\n" + "=" * 70)
        print("❌ MISSING SCRIPTS:")
        print("=" * 70)
        for script in missing:
            priority_marker = "⚠️ " if script.get('priority') in ['critical', 'high'] else "  "
            print(f"{priority_marker} {script['path']} ({script.get('priority')})")
    
    # Recommendations
    print("\n" + "=" * 70)
    
    if not modified and not missing:
        print("✅ All scripts are valid and match the registry!")
    else:
        print("📋 RECOMMENDED ACTIONS:")
        print("=" * 70)
        
        if modified:
            print("\nFor MODIFIED scripts:")
            print("  1. Review changes to ensure they are intentional")
            print("  2. If legitimate, update the registry:")
            print("     python3 scripts/maintenance/generate_script_registry.py --update")
            print("  3. If unauthorized, restore from git history:")
            print("     git checkout HEAD -- <script-path>")
        
        if missing:
            print("\nFor MISSING scripts:")
            print("  1. Check if scripts were intentionally removed")
            print("  2. If not, restore from git history")
            print("  3. Update registry to reflect current state")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Validate scripts against registry'
    )
    parser.add_argument(
        '--registry',
        default='scripts/.script-registry.json',
        help='Registry file path (default: scripts/.script-registry.json)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on any modified or missing scripts'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--priority',
        choices=['critical', 'high', 'medium', 'low'],
        help='Only check scripts of specified priority'
    )
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent.parent
    registry_file = repo_root / args.registry
    
    print("🔐 Script Registry Validator")
    print("=" * 70)
    print(f"📖 Registry: {registry_file}")
    
    # Load registry
    try:
        registry = load_registry(registry_file)
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n💡 Generate a registry first:")
        print("   python3 scripts/maintenance/generate_script_registry.py")
        return 1
    except Exception as e:
        print(f"\n❌ Error loading registry: {e}")
        return 1
    
    # Filter by priority if specified
    if args.priority:
        original_count = len(registry.get('scripts', []))
        registry['scripts'] = [
            s for s in registry.get('scripts', [])
            if s.get('priority') == args.priority
        ]
        filtered_count = len(registry['scripts'])
        print(f"🔍 Filtered to {filtered_count} {args.priority} priority scripts (from {original_count})")
    
    # Validate
    print(f"🔍 Validating {len(registry.get('scripts', []))} scripts...")
    valid, modified, missing = validate_scripts(registry, repo_root, args.strict)
    
    # Print results
    print_results(valid, modified, missing, args.verbose)
    
    # Exit code
    if args.strict and (modified or missing):
        print("\n❌ Validation failed (strict mode)")
        return 1
    elif modified or missing:
        print(f"\n⚠️  Validation completed with warnings")
        return 0
    else:
        print(f"\n✅ Validation passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
