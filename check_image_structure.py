import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

files_to_check = [
    'library_updated.json',
    'library_with_full_pages.json'
]

for filename in files_to_check:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n=== {filename} ===")
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
                break
        if drill.get('images'):
            break
