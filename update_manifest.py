#!/usr/bin/env python3
"""
Update manifest.json with new library version.
"""

import json
from datetime import datetime

def update_manifest(manifest_path, library_version, library_url, stats):
    """
    Update manifest.json with new version info.
    
    Args:
        manifest_path: Path to manifest.json
        library_version: Version string (e.g., "v15")
        library_url: URL to library JSON file
        stats: Dict with sessions, drills, images counts
    """
    print(f"Updating {manifest_path}...")
    
    # Load existing manifest
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except FileNotFoundError:
        manifest = {
            "library_id": "handball-training-library",
            "min_app_version": "1.0.0"
        }
    
    # Update fields
    manifest["version"] = library_version
    manifest["created_at"] = datetime.now().isoformat()
    manifest["package"] = {
        "url": library_url,
        "type": "json"
    }
    manifest["stats"] = stats
    
    # Add changelog entry
    if "changelog" not in manifest:
        manifest["changelog"] = []
    
    changelog_entry = f"{library_version}: Optimiert für mobile Geräte mit Remote Images"
    if changelog_entry not in manifest["changelog"]:
        manifest["changelog"].insert(0, changelog_entry)
    
    # Save manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Manifest updated to version {library_version}")
    print(f"  URL: {library_url}")
    print(f"  Stats: {stats}")

if __name__ == '__main__':
    # Configuration
    manifest_path = 'manifest.json'
    library_version = 'v15'
    library_url = 'https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/library_v15_remote_images.json'
    
    stats = {
        "sessions": 59,
        "drills": 376,
        "images": 376
    }
    
    # Update manifest
    update_manifest(manifest_path, library_version, library_url, stats)
    
    print("\n✓ Done! Commit and push manifest.json to GitHub:")
    print("  git add manifest.json")
    print("  git commit -m 'Update to v15 with remote images'")
    print("  git push")
