import fitz  # PyMuPDF
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Open PDF
pdf_path = 'files/Trainingseinheit 078.pdf'
doc = fitz.open(pdf_path)

print(f"=== Checking {pdf_path} ===\n")

# Page 6 should have drill 78-7 (Abschlussspiel)
page_num = 5  # 0-indexed, so page 6 is index 5
page = doc[page_num]
text = page.get_text()

print(f"Page {page_num + 1} text:\n")
print(text)
print("\n" + "="*80)

# Check if UPDATE is in the text
if 'UPDATE' in text.upper():
    print("\n❌ 'UPDATE' IS in the PDF!")
    # Find the context
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'UPDATE' in line.upper():
            print(f"\nLine {i}: {line}")
            if i > 0:
                print(f"Previous line: {lines[i-1]}")
            if i < len(lines) - 1:
                print(f"Next line: {lines[i+1]}")
else:
    print("\n✅ 'UPDATE' is NOT in the PDF!")
