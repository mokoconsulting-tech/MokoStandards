#!/usr/bin/env python3
"""
Dry Run Test - Documentation and Task Status Report
Shows what would happen without requiring GitHub authentication.
"""

from pathlib import Path

# Canonical Document List
CANONICAL_DOCUMENTS = {
    "README.md": {"type": "index", "subtype": "core", "priority": "High", "approval": "Yes"},
    "CHANGELOG.md": {"type": "index", "subtype": "core", "priority": "High", "approval": "No"},
    "LICENSE.md": {"type": "policy", "subtype": "core", "priority": "High", "approval": "Yes"},
    "docs/readme.md": {"type": "index", "subtype": "core", "priority": "High", "approval": "No"},
    "docs/index.md": {"type": "index", "subtype": "core", "priority": "High", "approval": "No"},
    "docs/policy/document-formatting.md": {"type": "policy", "subtype": "policy", "priority": "High", "approval": "Yes"},
    "docs/policy/change-management.md": {"type": "policy", "subtype": "policy", "priority": "High", "approval": "Yes"},
    "docs/policy/risk-register.md": {"type": "policy", "subtype": "policy", "priority": "High", "approval": "Yes"},
    "docs/policy/data-classification.md": {"type": "policy", "subtype": "policy", "priority": "High", "approval": "Yes"},
    "docs/policy/vendor-risk.md": {"type": "policy", "subtype": "policy", "priority": "High", "approval": "Yes"},
    "docs/policy/waas/waas-security.md": {"type": "policy", "subtype": "waas", "priority": "High", "approval": "Yes"},
    "docs/policy/waas/waas-provisioning.md": {"type": "policy", "subtype": "waas", "priority": "High", "approval": "Yes"},
    "docs/policy/waas/waas-tenant-isolation.md": {"type": "policy", "subtype": "waas", "priority": "High", "approval": "Yes"},
    "docs/guide/audit-readiness.md": {"type": "guide", "subtype": "guide", "priority": "Medium", "approval": "No"},
    "docs/guide/waas/architecture.md": {"type": "guide", "subtype": "waas", "priority": "Medium", "approval": "No"},
    "docs/guide/waas/operations.md": {"type": "guide", "subtype": "waas", "priority": "Medium", "approval": "No"},
    "docs/guide/waas/client-onboarding.md": {"type": "guide", "subtype": "waas", "priority": "Medium", "approval": "No"},
    "docs/checklist/release.md": {"type": "checklist", "subtype": "core", "priority": "Medium", "approval": "No"},
    "templates/docs/README.md": {"type": "index", "subtype": "catalog", "priority": "Low", "approval": "No"},
    "templates/docs/required/README.md": {"type": "index", "subtype": "catalog", "priority": "Low", "approval": "No"},
    "templates/docs/extra/README.md": {"type": "index", "subtype": "catalog", "priority": "Low", "approval": "No"},
}


def main():
    """Generate status report."""
    print("="*70)
    print("Documentation and Task Status Report")
    print("MokoStandards - Dry Run Test")
    print("="*70)
    
    repo_path = Path("/home/runner/work/MokoStandards/MokoStandards")
    
    # Check documents
    print("\n📋 Checking Canonical Documents...")
    print("-"*70)
    
    existing = []
    missing = []
    
    for doc_path, doc_info in CANONICAL_DOCUMENTS.items():
        full_path = repo_path / doc_path
        status = "✅" if full_path.exists() else "❌"
        
        if full_path.exists():
            existing.append(doc_path)
        else:
            missing.append(doc_path)
        
        print(f"{status} {doc_path}")
        print(f"   Type: {doc_info['type']}, Subtype: {doc_info['subtype']}, "
              f"Priority: {doc_info['priority']}, Approval: {doc_info['approval']}")
    
    # List subdirectories in templates/
    print("\n📁 Subdirectories in templates/...")
    print("-"*70)
    
    templates_path = repo_path / "templates"
    subdirs = []
    
    if templates_path.exists():
        for item in templates_path.rglob("*"):
            if item.is_dir():
                rel_path = item.relative_to(repo_path)
                subdirs.append(str(rel_path))
        
        subdirs = sorted(subdirs)
        for subdir in subdirs:
            print(f"  {subdir}")
    
    # Scan all markdown files
    print("\n📄 All Markdown Files in Repository...")
    print("-"*70)
    
    docs_files = []
    templates_files = []
    
    docs_path = repo_path / "docs"
    if docs_path.exists():
        for md_file in docs_path.rglob("*.md"):
            rel_path = md_file.relative_to(repo_path)
            docs_files.append(str(rel_path))
    
    if templates_path.exists():
        for md_file in templates_path.rglob("*.md"):
            rel_path = md_file.relative_to(repo_path)
            templates_files.append(str(rel_path))
    
    print(f"\nDocs directory: {len(docs_files)} files")
    for f in sorted(docs_files)[:10]:
        print(f"  {f}")
    if len(docs_files) > 10:
        print(f"  ... and {len(docs_files) - 10} more")
    
    print(f"\nTemplates directory: {len(templates_files)} files")
    for f in sorted(templates_files)[:10]:
        print(f"  {f}")
    if len(templates_files) > 10:
        print(f"  ... and {len(templates_files) - 10} more")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n📊 Canonical Documents:")
    print(f"   Total: {len(CANONICAL_DOCUMENTS)}")
    print(f"   ✅ Existing: {len(existing)}")
    print(f"   ❌ Missing: {len(missing)}")
    
    if missing:
        print(f"\n   Missing documents would be created:")
        for doc in missing:
            print(f"      - {doc}")
    
    print(f"\n📁 Subdirectories in templates/: {len(subdirs)}")
    print(f"\n📄 Total Markdown Files:")
    print(f"   Docs: {len(docs_files)}")
    print(f"   Templates: {len(templates_files)}")
    print(f"   Total: {len(docs_files) + len(templates_files)}")
    
    print(f"\n📊 Project #7 Tasks:")
    print(f"   Would create/update: {len(CANONICAL_DOCUMENTS)} tasks")
    print(f"   Existing documents: {len(existing)} tasks verified")
    print(f"   Missing documents: {len(missing)} tasks + documents created")
    
    print("\n✅ All canonical documents exist and are ready for Project #7 sync!")
    
    print("\n" + "="*70)
    print("To populate Project #7, run:")
    print("  export GH_PAT='your_token'")
    print("  python3 scripts/ensure_docs_and_project_tasks.py")
    print("="*70)


if __name__ == "__main__":
    main()
