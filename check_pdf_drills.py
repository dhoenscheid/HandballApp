import fitz  # PyMuPDF
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Open PDF
pdf_path = 'files/Trainingseinheit 078.pdf'
doc = fitz.open(pdf_path)

print(f"=== Checking {pdf_path} ===\n")

drill_pattern = re.compile(r'Nr\.:(\d+-\d+)')

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    # Find drill numbers
    matches = drill_pattern.findall(text)
    if matches:
        print(f"Page {page_num + 1}:")
        for match in matches:
            print(f"  - Drill {match}")
            
            # Get drill title (usually after the drill number)
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if f'Nr.:{match}' in line:
                    # Title is usually the next non-empty line
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].strip() and not lines[j].strip().isdigit():
                            print(f"    Title: {lines[j].strip()}")
                            break
                    break

print(f"\n✓ Total pages: {len(doc)}")
