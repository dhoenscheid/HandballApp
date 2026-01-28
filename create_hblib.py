#!/usr/bin/env python3
"""
Create .hblib package from library JSON and drill images.
.hblib is a ZIP archive containing:
- library.json (training sessions data)
- images/drill_images_manifest_v2.json (image manifest)
- images/drill_images_v2/ (folder with all drill images)
"""

import json
import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_hblib(library_json_path, images_dir, output_hblib_path):
    """
    Create .hblib package from library JSON and images.
    
    Args:
        library_json_path: Path to library_with_full_pages.json
        images_dir: Path to drill_images/ directory
        output_hblib_path: Output path for .hblib file
    """
    print(f"Creating {output_hblib_path}...")
    
    # Load library JSON
    with open(library_json_path, 'r', encoding='utf-8') as f:
        library_data = json.load(f)
    
    # Create image manifest
    manifest = {
        "version": "v2",
        "root": "drill_images_v2",
        "type": "full_page_screenshots",
        "created_at": datetime.now().isoformat(),
        "drills": {}
    }
    
    # Collect all drill images (use set to avoid duplicates)
    image_files_set = set()
    sessions_count = 0
    drills_count = 0
    images_count = 0
    
    for session in library_data.get('sessions', []):
        session_id = session['id']
        sessions_count += 1
        
        for drill in session.get('drills', []):
            drill_id = drill['drill_id']
            drills_count += 1
            
            if 'images' in drill and drill['images']:
                manifest['drills'][drill_id] = {
                    "session_id": session_id,
                    "images": []
                }
                
                for img in drill['images']:
                    # Original path: drill_images/TE_078/TE_078_page_2.png
                    # New path in .hblib: drill_images_v2/TE_078/TE_078_page_2.png
                    original_path = img['path']
                    
                    # Replace drill_images with drill_images_v2
                    new_path = original_path.replace('drill_images/', 'drill_images_v2/')
                    
                    manifest['drills'][drill_id]['images'].append(new_path)
                    
                    # Add to files to include in ZIP (use set to avoid duplicates)
                    if os.path.exists(original_path):
                        image_files_set.add((original_path, new_path))
                        images_count += 1
                    else:
                        print(f"  Warning: Image not found: {original_path}")
    
    # Convert set to list for processing
    image_files = sorted(list(image_files_set))
    
    print(f"  Sessions: {sessions_count}")
    print(f"  Drills: {drills_count}")
    print(f"  Image references: {images_count}")
    print(f"  Unique images: {len(image_files)}")
    
    # Create ZIP file (.hblib)
    with zipfile.ZipFile(output_hblib_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add library.json
        print("  Adding library.json...")
        zf.writestr('library.json', json.dumps(library_data, ensure_ascii=False, indent=2))
        
        # Add manifest
        print("  Adding image manifest...")
        zf.writestr('images/drill_images_manifest_v2.json', 
                   json.dumps(manifest, ensure_ascii=False, indent=2))
        
        # Add all images
        print(f"  Adding {len(image_files)} images...")
        for i, (original_path, zip_path) in enumerate(image_files, 1):
            if i % 50 == 0:
                print(f"    Progress: {i}/{len(image_files)}")
            zf.write(original_path, f'images/{zip_path}')
    
    file_size_mb = os.path.getsize(output_hblib_path) / (1024 * 1024)
    print(f"✓ Created {output_hblib_path} ({file_size_mb:.1f} MB)")
    print(f"  Contains {sessions_count} sessions, {drills_count} drills, {images_count} images")

if __name__ == '__main__':
    # Paths
    library_json = 'library_with_full_pages.json'
    images_dir = 'drill_images'
    output_hblib = 'handball-library_v14.hblib'
    
    # Create .hblib
    create_hblib(library_json, images_dir, output_hblib)
    
    print("\n✓ Done! You can now import handball-library_v14.hblib into the app.")
