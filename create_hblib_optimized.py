#!/usr/bin/env python3
"""
Create optimized .hblib package with minimal JSON size.
Removes verbose text content and keeps only essential data.
"""

import json
import zipfile
import os
from pathlib import Path
from datetime import datetime

def optimize_library_json(library_data):
    """
    Optimize library JSON by removing verbose content.
    Keep only essential data for the app.
    """
    optimized = {
        "library_version": library_data.get("library_version", "v4_optimized"),
        "source": "optimized_for_mobile",
        "sessions": []
    }
    
    for session in library_data.get('sessions', []):
        optimized_session = {
            "id": session['id'],
            "title": session['title'],
            "duration_total_min": session['duration_total_min'],
            "tags": session.get('tags', {}),
            "drills": []
        }
        
        for drill in session.get('drills', []):
            # Nur die wichtigsten Text-Felder behalten
            text = drill.get('text', {})
            optimized_drill = {
                "drill_id": drill['drill_id'],
                "title": drill['title'],
                "duration_min": drill['duration_min'],
                "phase": drill['phase'],
                "text": {
                    "setup": text.get('setup', ''),
                    "execution": text.get('execution', ''),
                    "coaching_points": text.get('coaching_points', ''),
                    "variations": text.get('variations', '')
                },
                "tags": drill.get('tags', {}),
                "images": drill.get('images', [])
            }
            
            optimized_session['drills'].append(optimized_drill)
        
        optimized['sessions'].append(optimized_session)
    
    return optimized

def create_hblib_optimized(library_json_path, images_dir, output_hblib_path):
    """
    Create optimized .hblib package with minimal JSON.
    
    Args:
        library_json_path: Path to library_with_full_pages.json
        images_dir: Path to drill_images/ directory
        output_hblib_path: Output path for .hblib file
    """
    print(f"Creating optimized {output_hblib_path}...")
    
    # Load and optimize library JSON
    with open(library_json_path, 'r', encoding='utf-8') as f:
        library_data = json.load(f)
    
    print("  Optimizing JSON...")
    optimized_data = optimize_library_json(library_data)
    
    # Create compact JSON string (no indentation)
    compact_json = json.dumps(optimized_data, ensure_ascii=False, separators=(',', ':'))
    
    original_size = len(json.dumps(library_data, ensure_ascii=False))
    optimized_size = len(compact_json)
    print(f"  JSON size: {original_size / 1024 / 1024:.1f} MB → {optimized_size / 1024 / 1024:.1f} MB ({optimized_size * 100 / original_size:.0f}%)")
    
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
    
    for session in optimized_data.get('sessions', []):
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
                    original_path = img['path']
                    new_path = original_path.replace('drill_images/', 'drill_images_v2/')
                    
                    manifest['drills'][drill_id]['images'].append(new_path)
                    
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
    with zipfile.ZipFile(output_hblib_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Add optimized library.json (compact, no indentation)
        print("  Adding optimized library.json...")
        zf.writestr('library.json', compact_json)
        
        # Add manifest (also compact)
        print("  Adding image manifest...")
        compact_manifest = json.dumps(manifest, ensure_ascii=False, separators=(',', ':'))
        zf.writestr('images/drill_images_manifest_v2.json', compact_manifest)
        
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
    output_hblib = 'handball-library_v15_optimized.hblib'
    
    # Create optimized .hblib
    create_hblib_optimized(library_json, images_dir, output_hblib)
    
    print("\n✓ Done! Optimized .hblib created with minimal JSON size.")
    print("  This version should work better on mobile devices with limited memory.")
