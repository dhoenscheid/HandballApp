#!/usr/bin/env python3
"""
Delete all images that don't have 'page' in the filename.
Keep only full-page screenshots (e.g., TE_078_page_2.png)
"""

import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

drill_images_dir = Path('drill_images')

if not drill_images_dir.exists():
    print(f"❌ Directory {drill_images_dir} not found!")
    exit(1)

print(f"Scanning {drill_images_dir}...\n")

# Find all image files
all_images = []
for root, dirs, files in os.walk(drill_images_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            all_images.append(Path(root) / file)

print(f"Found {len(all_images)} total images")

# Separate into keep and delete
keep_images = []
delete_images = []

for img_path in all_images:
    if 'page' in img_path.name.lower():
        keep_images.append(img_path)
    else:
        delete_images.append(img_path)

print(f"  Keep (with 'page'): {len(keep_images)}")
print(f"  Delete (without 'page'): {len(delete_images)}")

if delete_images:
    print(f"\n⚠️  About to delete {len(delete_images)} images!")
    print("Examples of files to delete:")
    for img in delete_images[:5]:
        print(f"  - {img}")
    
    response = input("\nProceed with deletion? (yes/no): ")
    
    if response.lower() == 'yes':
        deleted_count = 0
        for img_path in delete_images:
            try:
                img_path.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to delete {img_path}: {e}")
        
        print(f"\n✓ Deleted {deleted_count} images")
        print(f"✓ Kept {len(keep_images)} full-page screenshots")
        
        # Clean up empty directories
        print("\nCleaning up empty directories...")
        for root, dirs, files in os.walk(drill_images_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"  Removed empty: {dir_path}")
                except:
                    pass
    else:
        print("\n❌ Deletion cancelled")
else:
    print("\n✓ No images to delete - all images have 'page' in filename")
