import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check library_with_full_pages.json
with open('library_with_full_pages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"library_with_full_pages.json:")
print(f"  Sessions: {len(data['sessions'])}")
print(f"  Session IDs: {sorted([s['id'] for s in data['sessions']])}")

# Check library_v15_remote_images.json
with open('library_v15_remote_images.json', 'r', encoding='utf-8') as f:
    data_v15 = json.load(f)

print(f"\nlibrary_v15_remote_images.json:")
print(f"  Sessions: {len(data_v15['sessions'])}")
print(f"  Session IDs: {sorted([s['id'] for s in data_v15['sessions']])}")

# Check library_updated.json
with open('library_updated.json', 'r', encoding='utf-8') as f:
    data_updated = json.load(f)

print(f"\nlibrary_updated.json:")
print(f"  Sessions: {len(data_updated['sessions'])}")
print(f"  Session IDs: {sorted([s['id'] for s in data_updated['sessions']])}")
