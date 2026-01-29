#!/usr/bin/env python3
"""
Create v16 library with LOCAL image paths (for testing before GitHub upload)
"""

import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def create_library_with_local_paths(input_json_path, output_json_path):
    """
    Create library.json with local file:// paths for testing
    """
    print(f"Creating library with local paths...")
    
    with open(input_json_path, 'r', encoding='utf-8') as f:
        library_data = json.load(f)
    
    # Change all image URLs to local paths
    for session in library_data.get('sessions', []):
        for drill in session.get('drills', []):
            for img in drill.get('images', []):
                if 'url' in img:
                    # Extract the path part from URL
                    # URL: https://raw.githubusercontent.com/.../drill_images/TE_078/TE_078_page_2.png
                    # Local: drill_images/TE_078/TE_078_page_2.png
                    url = img['url']
                    if 'drill_images/' in url:
                        local_path = url.split('drill_images/')[-1]
                        img['path'] = f'drill_images/{local_path}'
                        del img['url']  # Remove URL, use path instead
    
    # Save with nice formatting
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(library_data, f, ensure_ascii=False, indent=2)
    
    file_size_kb = len(json.dumps(library_data, ensure_ascii=False)) / 1024
    print(f"✓ Created {output_json_path} ({file_size_kb:.1f} KB)")
    print(f"  This version uses LOCAL paths for testing")

if __name__ == '__main__':
    create_library_with_local_paths(
        'library_v16_remote_images.json',
        'library_v16_local_test.json'
    )
    
    print("\n✓ Done! Use this file for local testing:")
    print("  1. Copy library_v16_local_test.json and drill_images/ to the app")
    print("  2. Import manually via DocumentPicker")
    print("  3. Images will load from local files")
