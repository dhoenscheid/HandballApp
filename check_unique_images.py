import json
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load library
with open('library_v16_remote_images.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all image URLs
all_image_urls = []
for session in data['sessions']:
    for drill in session['drills']:
        for img in drill.get('images', []):
            all_image_urls.append(img['url'])

# Count unique URLs
unique_urls = set(all_image_urls)

print(f"Total image references: {len(all_image_urls)}")
print(f"Unique image URLs: {len(unique_urls)}")
print(f"Duplicate references: {len(all_image_urls) - len(unique_urls)}")

# Count actual files in drill_images
drill_images_dir = Path('drill_images')
actual_files = []
for root, dirs, files in os.walk(drill_images_dir):
    for file in files:
        if 'page' in file.lower() and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            actual_files.append(file)

print(f"\nActual files with 'page': {len(actual_files)}")

# Example: Show which drills share the same image
print("\n=== Example: Session 78, Page 2 ===")
page_2_url = None
drills_using_page_2 = []

for session in data['sessions']:
    if session['id'] == 78:
        for drill in session['drills']:
            for img in drill.get('images', []):
                if 'TE_078_page_2.png' in img['url']:
                    page_2_url = img['url']
                    drills_using_page_2.append(drill['drill_id'])

if drills_using_page_2:
    print(f"Image: TE_078_page_2.png")
    print(f"Used by {len(drills_using_page_2)} drills: {', '.join(drills_using_page_2)}")
    print("\n✓ This is CORRECT - multiple drills on the same page share the same image!")
