#!/usr/bin/env python3
"""
Create library.json without images for direct download.
Images will be downloaded on-demand by the app.
"""

import json
from datetime import datetime

def create_library_json_for_app(input_json_path, output_json_path, base_image_url):
    """
    Create optimized library.json with remote image URLs.
    
    Args:
        input_json_path: Path to library_with_full_pages.json
        output_json_path: Output path for optimized library.json
        base_image_url: Base URL for images (e.g., https://raw.githubusercontent.com/.../drill_images/)
    """
    print(f"Creating app-ready library.json...")
    
    # Load library JSON
    with open(input_json_path, 'r', encoding='utf-8') as f:
        library_data = json.load(f)
    
    # Optimize and add remote URLs
    optimized = {
        "library_version": "v15",
        "source": "optimized_for_mobile_with_remote_images",
        "created_at": datetime.now().isoformat(),
        "image_base_url": base_image_url,
        "sessions": []
    }
    
    sessions_count = 0
    drills_count = 0
    images_count = 0
    
    for session in library_data.get('sessions', []):
        sessions_count += 1
        
        optimized_session = {
            "id": session['id'],
            "title": session['title'],
            "duration_total_min": session['duration_total_min'],
            "tags": session.get('tags', {}),
            "drills": []
        }
        
        for drill in session.get('drills', []):
            drills_count += 1
            
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
                "images": []
            }
            
            # Konvertiere lokale Pfade zu Remote-URLs
            for img in drill.get('images', []):
                images_count += 1
                local_path = img['path']  # z.B. drill_images/TE_078/TE_078_page_2.png
                
                # Erstelle Remote-URL
                remote_url = f"{base_image_url}{local_path}"
                
                optimized_drill['images'].append({
                    "url": remote_url,
                    "page": img.get('page'),
                    "order": img.get('order'),
                    "type": img.get('type', 'full_page')
                })
            
            optimized_session['drills'].append(optimized_drill)
        
        optimized['sessions'].append(optimized_session)
    
    # Speichere als kompaktes JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(optimized, f, ensure_ascii=False, separators=(',', ':'))
    
    file_size_kb = len(json.dumps(optimized, ensure_ascii=False)) / 1024
    print(f"✓ Created {output_json_path} ({file_size_kb:.1f} KB)")
    print(f"  Sessions: {sessions_count}")
    print(f"  Drills: {drills_count}")
    print(f"  Images: {images_count} (as remote URLs)")
    print(f"\n  Images will be downloaded on-demand from:")
    print(f"  {base_image_url}")

if __name__ == '__main__':
    # Paths
    input_json = 'library_with_full_pages.json'
    output_json = 'library_v15_remote_images.json'
    
    # Base URL für Bilder (GitHub Raw URL)
    base_image_url = 'https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/'
    
    # Create library.json
    create_library_json_for_app(input_json, output_json, base_image_url)
    
    print("\n✓ Done! Upload this file and the drill_images/ folder to GitHub.")
    print("  The app will download images on-demand, avoiding memory issues.")
