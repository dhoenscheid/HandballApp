#!/usr/bin/env python3
"""
Create readable (formatted) version of library JSON.
"""

import json
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load compact JSON
with open('library_v15_remote_images.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Save as readable JSON (with indentation)
with open('library_v15_remote_images_readable.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Created readable version: library_v15_remote_images_readable.json")
print("  This is easier to read but larger in size")
print("\nBoth files are valid - use the compact version for production")
