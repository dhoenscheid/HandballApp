import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('library_v15_remote_images.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"=== library_v15_remote_images.json ===")
print(f"Sessions: {len(data['sessions'])}")

# Check first session with images
for session in data['sessions']:
    for drill in session.get('drills', []):
        if drill.get('images'):
            print(f"\nFirst drill with images:")
            print(f"  Session: {session['id']} - {session['title']}")
            print(f"  Drill: {drill['drill_id']} - {drill['title']}")
            print(f"  Images: {len(drill['images'])}")
            print(f"  First image structure:")
            img = drill['images'][0]
            for key, value in img.items():
                print(f"    {key}: {value}")
            
            # Check if it's the old or new format
            if 'url' in img:
                if 'TE_078_page_2.png' in img['url']:
                    print("\n✓ This is the NEW extraction (full-page images)!")
                elif '78-1_p02_img1.jpeg' in img['url']:
                    print("\n✗ This is the OLD extraction (embedded images)!")
            break
    if drill.get('images'):
        break
