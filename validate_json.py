import json
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Validate library_v15_remote_images.json
with open('library_v15_remote_images.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sessions = len(data['sessions'])
drills = sum(len(s['drills']) for s in data['sessions'])
images = sum(len(drill['images']) for s in data['sessions'] for drill in s['drills'])

print(f"✓ Valid JSON!")
print(f"  Sessions: {sessions}")
print(f"  Drills: {drills}")
print(f"  Images: {images}")
print(f"  File size: {len(json.dumps(data)) / 1024:.1f} KB")
print(f"\nFirst session: {data['sessions'][0]['title']}")
print(f"First drill: {data['sessions'][0]['drills'][0]['title']}")
if data['sessions'][0]['drills'][0]['images']:
    print(f"First image URL: {data['sessions'][0]['drills'][0]['images'][0]['url']}")
