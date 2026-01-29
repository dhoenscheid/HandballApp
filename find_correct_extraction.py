import json
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Find all JSON files
json_files = list(Path('.').glob('*.json'))

print("=== Checking all JSON files for drill 78-7 ===\n")

correct_files = []
incorrect_files = []

for json_file in json_files:
    if json_file.name in ['package.json', 'package-lock.json']:
        continue
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it has sessions
        if 'sessions' not in data:
            continue
        
        sessions_count = len(data['sessions'])
        
        # Find session 78, drill 78-7
        has_update = None
        for session in data['sessions']:
            if session['id'] == 78:
                for drill in session['drills']:
                    if drill['drill_id'] == '78-7':
                        execution = drill.get('text', {}).get('execution', '')
                        has_update = 'UPDATE' in execution.upper()
                        
                        if has_update:
                            incorrect_files.append((json_file.name, sessions_count))
                            print(f"❌ {json_file.name}")
                            print(f"   Sessions: {sessions_count}")
                            print(f"   Contains 'UPDATE' - WRONG extraction")
                        else:
                            correct_files.append((json_file.name, sessions_count))
                            print(f"✅ {json_file.name}")
                            print(f"   Sessions: {sessions_count}")
                            print(f"   Does NOT contain 'UPDATE' - CORRECT extraction!")
                            print(f"   Execution preview: {execution[:150]}...")
                        print()
                        break
                break
                
    except Exception as e:
        print(f"⚠️  {json_file.name} - Error: {e}\n")

print("\n=== Summary ===")
print(f"Correct extractions: {len(correct_files)}")
for name, count in correct_files:
    print(f"  ✅ {name} ({count} sessions)")

print(f"\nIncorrect extractions: {len(incorrect_files)}")
for name, count in incorrect_files:
    print(f"  ❌ {name} ({count} sessions)")

if correct_files:
    print(f"\n🎯 USE THIS FILE: {correct_files[0][0]}")
else:
    print("\n⚠️  No correct extraction found! Need to re-extract PDFs.")
