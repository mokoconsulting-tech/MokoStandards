#!/usr/bin/env python3
"""
Script Registry Generator

Generates a comprehensive registry of all scripts with their SHA-256 hashes.
This provides a security baseline for script integrity verification.

Usage:
    python3 generate_script_registry.py [--output FILENAME] [--update]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 03.01.03
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


# Script priority levels
PRIORITY_CRITICAL = 'critical'
PRIORITY_HIGH = 'high'
PRIORITY_MEDIUM = 'medium'
PRIORITY_LOW = 'low'

# Categories and their priority levels
CATEGORY_PRIORITIES = {
    'validate': PRIORITY_CRITICAL,
    'maintenance': PRIORITY_CRITICAL,
    'security': PRIORITY_CRITICAL,
    'automation': PRIORITY_HIGH,
    'release': PRIORITY_HIGH,
    'build': PRIORITY_HIGH,
    'fix': PRIORITY_HIGH,
    'analysis': PRIORITY_MEDIUM,
    'docs': PRIORITY_MEDIUM,
    'run': PRIORITY_MEDIUM,
    'tests': PRIORITY_MEDIUM,
    'wrappers': PRIORITY_LOW,
    'lib': PRIORITY_LOW
}


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_script_category(script_path: Path, repo_root: Path) -> str:
    """Determine script category from path."""
    rel_path = script_path.relative_to(repo_root / 'scripts')
    parts = rel_path.parts
    
    if len(parts) > 0:
        return parts[0]
    return 'unknown'


def get_priority(category: str) -> str:
    """Get priority level for a category."""
    return CATEGORY_PRIORITIES.get(category, PRIORITY_LOW)


def should_track_script(script_path: Path) -> bool:
    """Determine if a script should be tracked."""
    # Skip certain patterns
    skip_patterns = [
        'index.md',
        'README',
        '.gitkeep',
        'wrapper-template'
    ]
    
    name = script_path.name
    for pattern in skip_patterns:
        if pattern in name:
            return False
    
    # Only track executable scripts or Python/Shell files
    if script_path.suffix not in ['.py', '.sh', '.ps1']:
        return False
    
    return True


def generate_registry(
    repo_root: Path,
    include_low_priority: bool = False
) -> Dict:
    """Generate complete script registry."""
    scripts_dir = repo_root / 'scripts'
    
    if not scripts_dir.exists():
        print(f"❌ Scripts directory not found: {scripts_dir}")
        return {}
    
    registry = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'repository': 'mokoconsulting-tech/MokoStandards',
            'version': '1.0.0'
        },
        'scripts': []
    }
    
    # Find all scripts
    script_extensions = ['*.py', '*.sh', '*.ps1']
    all_scripts = []
    
    for ext in script_extensions:
        all_scripts.extend(scripts_dir.rglob(ext))
    
    print(f"🔍 Found {len(all_scripts)} potential scripts")
    
    tracked_count = 0
    for script_path in sorted(all_scripts):
        if not should_track_script(script_path):
            continue
        
        category = get_script_category(script_path, repo_root)
        priority = get_priority(category)
        
        # Skip low priority if requested
        if not include_low_priority and priority == PRIORITY_LOW:
            continue
        
        try:
            sha256 = calculate_sha256(script_path)
            rel_path = str(script_path.relative_to(repo_root))
            
            script_entry = {
                'path': rel_path,
                'sha256': sha256,
                'category': category,
                'priority': priority,
                'size_bytes': script_path.stat().st_size
            }
            
            registry['scripts'].append(script_entry)
            tracked_count += 1
            
        except Exception as e:
            print(f"⚠️  Error processing {script_path}: {e}")
    
    print(f"✅ Tracked {tracked_count} scripts")
    
    # Add summary statistics
    registry['summary'] = {
        'total_scripts': tracked_count,
        'by_priority': {},
        'by_category': {}
    }
    
    for script in registry['scripts']:
        priority = script['priority']
        category = script['category']
        
        registry['summary']['by_priority'][priority] = \
            registry['summary']['by_priority'].get(priority, 0) + 1
        registry['summary']['by_category'][category] = \
            registry['summary']['by_category'].get(category, 0) + 1
    
    return registry


def load_existing_registry(registry_file: Path) -> Dict:
    """Load existing registry if it exists."""
    if registry_file.exists():
        with open(registry_file, 'r') as f:
            return json.load(f)
    return {}


def compare_registries(old: Dict, new: Dict) -> Dict:
    """Compare old and new registries to find changes."""
    changes = {
        'added': [],
        'removed': [],
        'modified': [],
        'unchanged': 0
    }
    
    if not old or 'scripts' not in old:
        changes['added'] = new.get('scripts', [])
        return changes
    
    old_scripts = {s['path']: s for s in old.get('scripts', [])}
    new_scripts = {s['path']: s for s in new.get('scripts', [])}
    
    # Find added and modified
    for path, new_script in new_scripts.items():
        if path not in old_scripts:
            changes['added'].append(new_script)
        elif old_scripts[path]['sha256'] != new_script['sha256']:
            changes['modified'].append({
                'path': path,
                'old_sha256': old_scripts[path]['sha256'],
                'new_sha256': new_script['sha256']
            })
        else:
            changes['unchanged'] += 1
    
    # Find removed
    for path, old_script in old_scripts.items():
        if path not in new_scripts:
            changes['removed'].append(old_script)
    
    return changes


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Generate script registry with SHA-256 hashes'
    )
    parser.add_argument(
        '--output',
        default='scripts/.script-registry.json',
        help='Output file path (default: scripts/.script-registry.json)'
    )
    parser.add_argument(
        '--include-low-priority',
        action='store_true',
        help='Include low priority scripts (wrappers, libs)'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing registry and show changes'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'summary'],
        default='summary',
        help='Output format'
    )
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent.parent
    output_path = repo_root / args.output
    
    print("🔐 Script Registry Generator")
    print("=" * 60)
    
    # Load existing registry if updating
    old_registry = {}
    if args.update and output_path.exists():
        print(f"📖 Loading existing registry from {output_path}")
        old_registry = load_existing_registry(output_path)
    
    # Generate new registry
    print(f"🔍 Scanning scripts directory...")
    registry = generate_registry(repo_root, args.include_low_priority)
    
    if not registry or not registry.get('scripts'):
        print("❌ No scripts found")
        return 1
    
    # Compare if updating
    if old_registry:
        print("\n" + "=" * 60)
        print("📊 Changes Detected:")
        print("=" * 60)
        
        changes = compare_registries(old_registry, registry)
        
        if changes['added']:
            print(f"\n✅ Added ({len(changes['added'])} scripts):")
            for script in changes['added'][:10]:
                print(f"   + {script['path']}")
            if len(changes['added']) > 10:
                print(f"   ... and {len(changes['added']) - 10} more")
        
        if changes['modified']:
            print(f"\n🔄 Modified ({len(changes['modified'])} scripts):")
            for change in changes['modified'][:10]:
                print(f"   ~ {change['path']}")
                print(f"     Old: {change['old_sha256'][:16]}...")
                print(f"     New: {change['new_sha256'][:16]}...")
            if len(changes['modified']) > 10:
                print(f"   ... and {len(changes['modified']) - 10} more")
        
        if changes['removed']:
            print(f"\n❌ Removed ({len(changes['removed'])} scripts):")
            for script in changes['removed']:
                print(f"   - {script['path']}")
        
        print(f"\nℹ️  Unchanged: {changes['unchanged']} scripts")
    
    # Save registry
    print("\n" + "=" * 60)
    print(f"💾 Saving registry to {output_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Registry Summary:")
    print("=" * 60)
    print(f"Total scripts tracked: {registry['summary']['total_scripts']}")
    print("\nBy Priority:")
    for priority in [PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]:
        count = registry['summary']['by_priority'].get(priority, 0)
        if count > 0:
            print(f"  {priority:10s}: {count:3d} scripts")
    
    print("\nBy Category:")
    for category, count in sorted(registry['summary']['by_category'].items()):
        priority = get_priority(category)
        print(f"  {category:15s}: {count:3d} scripts ({priority})")
    
    print("\n" + "=" * 60)
    print(f"✅ Registry generated successfully!")
    print(f"📄 File: {output_path}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
