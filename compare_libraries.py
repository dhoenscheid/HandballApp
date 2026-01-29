import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check old library.json
with open('library.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

old_sessions = set(s['id'] for s in old_data['sessions'])

# Check new library_v15_remote_images.json
with open('library_v15_remote_images.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

new_sessions = set(s['id'] for s in new_data['sessions'])

print("=== Library Comparison ===\n")
print(f"Old library.json: {len(old_sessions)} sessions")
print(f"  IDs: {sorted(old_sessions)}\n")

print(f"New library_v15_remote_images.json: {len(new_sessions)} sessions")
print(f"  IDs: {sorted(new_sessions)}\n")

# Find differences
added = new_sessions - old_sessions
removed = old_sessions - new_sessions

print(f"Added sessions: {len(added)}")
if added:
    print(f"  IDs: {sorted(added)}\n")

print(f"Removed sessions: {len(removed)}")
if removed:
    print(f"  IDs: {sorted(removed)}\n")

print(f"✓ The new library contains {len(added)} NEW sessions from the PDFs!")
