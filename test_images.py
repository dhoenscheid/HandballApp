#!/usr/bin/env python3
"""Test script to check if PDF contains images"""

import fitz

pdf_path = "files/trainingseinheit 184.pdf"
doc = fitz.open(pdf_path)

print(f"PDF: {pdf_path}")
print(f"Total pages: {len(doc)}")
print()

total_images = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    
    if image_list:
        print(f"Page {page_num + 1}: {len(image_list)} images")
        total_images += len(image_list)
        
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            print(f"  Image {img_idx + 1}: xref={xref}, info={img}")

print(f"\nTotal images in PDF: {total_images}")

doc.close()
