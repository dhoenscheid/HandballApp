#!/usr/bin/env python3
"""
Extract full page images from PDFs instead of embedded images
This creates complete drill diagrams
"""

import fitz
import json
from pathlib import Path
import re


def extract_page_as_image(pdf_path: str, page_num: int, output_path: str, dpi: int = 150):
    """Extract a full page as an image"""
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # 0-based index
    
    # Render page to image
    zoom = dpi / 72  # 72 is default DPI
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Save as PNG
    pix.save(output_path)
    doc.close()
    
    return output_path


def extract_all_pages_from_pdf(pdf_path: str, output_dir: str, session_id: int, dpi: int = 150):
    """Extract all pages from a PDF as images"""
    doc = fitz.open(pdf_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    images = []
    
    for page_num in range(len(doc)):
        page_number = page_num + 1
        image_filename = f"TE_{session_id:03d}_page_{page_number}.png"
        image_path = output_path / image_filename
        
        # Render page
        page = doc[page_num]
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        pix.save(str(image_path))
        
        relative_path = f"drill_images/TE_{session_id:03d}/{image_filename}"
        
        images.append({
            "path": relative_path,
            "page": page_number,
            "order": 1,
            "type": "full_page"
        })
        
        print(f"  Extracted page {page_number}")
    
    doc.close()
    return images


def update_library_with_page_images(library_path: str, pdf_dir: str, output_path: str, dpi: int = 150):
    """Update library with full page images"""
    
    with open(library_path, 'r', encoding='utf-8') as f:
        library = json.load(f)
    
    pdf_files = sorted(Path(pdf_dir).glob('*.pdf'))
    
    print(f"Processing {len(pdf_files)} PDFs...")
    print(f"DPI: {dpi}")
    
    for pdf_file in pdf_files:
        match = re.search(r'(\d+)', pdf_file.name)
        if not match:
            continue
        
        session_id = int(match.group(1))
        
        # Find session in library
        session = next((s for s in library['sessions'] if s['id'] == session_id), None)
        if not session:
            print(f"Skipping {pdf_file.name} (not in library)")
            continue
        
        print(f"Processing {pdf_file.name}...")
        
        # Extract all pages as images
        output_dir = f"drill_images/TE_{session_id:03d}"
        images = extract_all_pages_from_pdf(str(pdf_file), output_dir, session_id, dpi)
        
        # Assign images to drills based on page numbers
        for drill in session['drills']:
            drill_page = drill.get('source_page_start', 2)
            drill['images'] = [img for img in images if img['page'] == drill_page]
        
        print(f"  ✓ Extracted {len(images)} page images")
    
    # Save updated library
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(library, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Saved to {output_path}")


def extract_single_session(pdf_path: str, session_id: int = None, dpi: int = 150):
    """Extract pages from a single PDF"""
    
    if session_id is None:
        match = re.search(r'(\d+)', Path(pdf_path).name)
        session_id = int(match.group(1)) if match else 999
    
    output_dir = f"drill_images/TE_{session_id:03d}"
    
    print(f"Extracting pages from {pdf_path}...")
    print(f"Output: {output_dir}")
    print(f"DPI: {dpi}")
    
    images = extract_all_pages_from_pdf(pdf_path, output_dir, session_id, dpi)
    
    print(f"\n✓ Extracted {len(images)} pages")
    for img in images:
        print(f"  - {img['path']}")
    
    return images


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pdf_to_images.py single <pdf_file> [dpi]")
        print("  python pdf_to_images.py update <library.json> <pdf_dir> <output.json> [dpi]")
        print("\nDefault DPI: 150 (higher = better quality but larger files)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "single":
        pdf_file = sys.argv[2]
        dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
        extract_single_session(pdf_file, dpi=dpi)
    
    elif command == "update":
        library_file = sys.argv[2]
        pdf_dir = sys.argv[3]
        output = sys.argv[4]
        dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 150
        update_library_with_page_images(library_file, pdf_dir, output, dpi)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
