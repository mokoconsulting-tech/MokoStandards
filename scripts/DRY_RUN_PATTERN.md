
# Standard Dry-Run Pattern for MokoStandards Scripts

## 1. Add --dry-run argument to argparse

```python
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Show what would be done without making changes'
)
```

## 2. Store in args and use throughout script

```python
args = parser.parse_args()
dry_run = args.dry_run

if dry_run:
    print("[DRY-RUN] Mode enabled - no changes will be made")
```

## 3. Add dry-run checks before write operations

```python
if dry_run:
    print(f"[DRY-RUN] Would create file: {filepath}")
else:
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created file: {filepath}")
```

## 4. Pattern for file operations

```python
def write_file(path, content, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would write to: {path}")
        print(f"[DRY-RUN] Content length: {len(content)} bytes")
        return
    
    with open(path, 'w') as f:
        f.write(content)
    print(f"Wrote to: {path}")
```

## 5. Pattern for API calls

```python
def update_repository(repo, data, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would update repository: {repo}")
        print(f"[DRY-RUN] Data: {data}")
        return None
    
    response = api.update(repo, data)
    print(f"Updated repository: {repo}")
    return response
```

## 6. Pattern for shell commands

```python
import subprocess

def run_command(cmd, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would execute: {cmd}")
        return 0
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode
```

## 7. Summary reporting

```python
def main():
    # ... script logic ...
    
    if dry_run:
        print()
        print("=" * 60)
        print("[DRY-RUN] Summary:")
        print(f"  Files that would be modified: {modified_count}")
        print(f"  Files that would be created: {created_count}")
        print(f"  API calls that would be made: {api_call_count}")
        print("=" * 60)
    else:
        print()
        print("Summary:")
        print(f"  Files modified: {modified_count}")
        print(f"  Files created: {created_count}")
        print(f"  API calls made: {api_call_count}")
```

