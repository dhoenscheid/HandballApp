import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('library_complete_fresh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Sessions: {len(data['sessions'])}")

# Find session 78
for session in data['sessions']:
    if session['id'] == 78:
        print(f"\nSession 78: {session['title']}")
        print(f"Drills: {len(session['drills'])}")
        
        for drill in session['drills']:
            print(f"  - {drill['drill_id']}: {drill['title']}")
        
        # Check if 78-7 exists
        drill_78_7 = [d for d in session['drills'] if d['drill_id'] == '78-7']
        if drill_78_7:
            print(f"\n✓ Found drill 78-7!")
            execution = drill_78_7[0]['text']['execution']
            if 'UPDATE' in execution.upper():
                print("❌ Contains 'UPDATE'")
                print(f"Execution: {execution[:300]}")
            else:
                print("✅ Does NOT contain 'UPDATE'")
                print(f"Execution: {execution[:300]}")
        else:
            print("\n❌ Drill 78-7 NOT FOUND!")
        break
