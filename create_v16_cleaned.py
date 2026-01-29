#!/usr/bin/env python3
"""
Create v16 library by cleaning the text artifacts from library_with_full_pages.json
"""

import json
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def clean_text(text: str) -> str:
    """Remove extraction artifacts from text"""
    if not text:
        return text
    
    # Remove common artifacts
    cleaned = text
    
    # Remove "- Text.execution NEU UPDATE "
    cleaned = re.sub(r'-\s*Text\.execution\s+NEU\s+UPDATE\s+', '', cleaned, flags=re.IGNORECASE)
    
    # Remove other "Text.fieldname" patterns
    cleaned = re.sub(r'-\s*Text\.\w+\s+', '', cleaned, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)  # Max 2 newlines
    cleaned = cleaned.strip()
    
    return cleaned

def clean_library(input_file: str, output_file: str):
    """Clean entire library file"""
    print(f"Cleaning {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_count = 0
    
    for session in data.get('sessions', []):
        for drill in session.get('drills', []):
            if 'text' in drill:
                text_obj = drill['text']
                for field in ['setup', 'execution', 'coaching_points', 'variations', 'preface', 'goal']:
                    if field in text_obj and isinstance(text_obj[field], str):
                        original = text_obj[field]
                        cleaned = clean_text(original)
                        if original != cleaned:
                            text_obj[field] = cleaned
                            cleaned_count += 1
    
    # Save cleaned data with nice formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Cleaned {cleaned_count} text fields")
    print(f"✓ Saved to {output_file}")
    
    return data

if __name__ == '__main__':
    # Clean library_with_full_pages.json
    cleaned_data = clean_library('library_with_full_pages.json', 'library_v16_cleaned.json')
    
    # Verify the fix for drill 78-7
    print("\n=== Verification for drill 78-7 ===")
    for session in cleaned_data['sessions']:
        if session['id'] == 78:
            for drill in session['drills']:
                if drill['drill_id'] == '78-7':
                    execution = drill.get('text', {}).get('execution', '')
                    if 'UPDATE' in execution.upper():
                        print("❌ Still contains 'UPDATE'!")
                        print(f"Execution: {execution[:200]}")
                    else:
                        print("✅ 'UPDATE' removed successfully!")
                        print(f"Execution: {execution[:200]}")
                    break
            break
    
    print("\n✓ Done! Now create v16 remote images JSON from this cleaned file.")
