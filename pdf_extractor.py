#!/usr/bin/env python3
"""
PDF Extractor for Handball Training Sessions
Extracts training session data from PDF files and updates library.json
"""

import fitz  # PyMuPDF
import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class HandballPDFExtractor:
    """Extract handball training session data from PDF files"""
    
    def __init__(self, pdf_path: str, extract_images: bool = True, image_output_dir: str = None):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.filename = Path(pdf_path).name
        self.extract_images = extract_images
        
        # Extract session ID from filename
        match = re.search(r'(\d+)', self.filename)
        self.session_id = int(match.group(1)) if match else None
        
        # Setup image output directory
        if image_output_dir:
            self.image_dir = Path(image_output_dir)
        else:
            self.image_dir = Path(pdf_path).parent.parent / "drill_images" / f"TE_{self.session_id:03d}"
        
        if self.extract_images:
            self.image_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_images_from_page(self, page_num: int) -> List[Dict[str, Any]]:
        """Extract all images from a specific page"""
        images = []
        page = self.doc[page_num - 1]  # page_num is 1-based
        
        try:
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list, start=1):
                xref = img_info[0]
                
                try:
                    # Extract image
                    base_image = self.doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Create filename
                    image_filename = f"{self.session_id}-{page_num}_img{img_index}.{image_ext}"
                    image_path = self.image_dir / image_filename
                    
                    # Save image
                    if self.extract_images:
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                    
                    # Store relative path
                    relative_path = f"drill_images/TE_{self.session_id:03d}/{image_filename}"
                    
                    images.append({
                        "path": relative_path,
                        "page": page_num,
                        "order": img_index
                    })
                    
                except Exception as e:
                    print(f"    Warning: Could not extract image {img_index} from page {page_num}: {e}")
                    
        except Exception as e:
            print(f"    Warning: Could not get images from page {page_num}: {e}")
        
        return images
    
    def extract_text_by_page(self) -> List[str]:
        """Extract text from each page"""
        pages = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            pages.append(text)
        return pages
        """Extract text from each page"""
        pages = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            pages.append(text)
        return pages
    
    def extract_title(self, first_page_text: str) -> str:
        """Extract session title from first page"""
        lines = [l.strip() for l in first_page_text.split('\n') if l.strip()]
        
        # Look for "Schwerpunkt:" or similar patterns
        for i, line in enumerate(lines):
            if 'Schwerpunkt' in line or 'schwerpunkt' in line:
                # Title is usually on the same line or next line
                if ':' in line:
                    title = line.split(':', 1)[1].strip()
                    if title and len(title) > 5:
                        return title
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if len(next_line) > 5 and 'Copyright' not in next_line:
                        return next_line
        
        # Look for title after "Trainingseinheit XXX"
        for i, line in enumerate(lines[:15]):
            if f'Trainingseinheit {self.session_id}' in line or f'TE {self.session_id}' in line:
                # Title is likely the next non-empty line
                for j in range(i + 1, min(i + 5, len(lines))):
                    candidate = lines[j]
                    if (len(candidate) > 10 and 
                        'Copyright' not in candidate and 
                        'Seite' not in candidate and
                        'handball-uebungen' not in candidate and
                        not candidate.startswith('http')):
                        return candidate
        
        # Fallback: find longest meaningful line in first 20 lines
        candidates = []
        for line in lines[:20]:
            if (len(line) > 15 and 
                'Copyright' not in line and 
                'Trainingseinheit' not in line and
                'Seite' not in line and
                'handball-uebungen' not in line and
                not line.startswith('http') and
                not re.match(r'^\d+$', line)):
                candidates.append(line)
        
        if candidates:
            return max(candidates, key=len)
        
        return f"Trainingseinheit {self.session_id}"
    
    def extract_duration(self, text: str) -> int:
        """Extract total duration in minutes"""
        # Look for patterns like "90 Minuten", "75 Min", etc.
        patterns = [
            r'(\d+)\s*Minuten',
            r'(\d+)\s*Min\.',
            r'(\d+)\s*min',
            r'Dauer:\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 90  # Default
    
    def extract_equipment(self, text: str) -> List[str]:
        """Extract equipment list"""
        equipment = []
        
        # Look for "Material:" or "Benötigtes Material:" section
        patterns = [
            r'(?:Material|Benötigtes Material|Equipment):\s*\n(.*?)(?:\n\n|\nAblauf|\nGrundaufbau)',
            r'(?:Material|Benötigtes Material):\s*([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\nAblauf)',
        ]
        
        for pattern in patterns:
            material_match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if material_match:
                material_text = material_match.group(1)
                # Split by bullet points, newlines, or special chars
                items = re.split(r'[\n•\-\u0001]', material_text)
                for item in items:
                    item = item.strip()
                    # Clean up common prefixes
                    item = re.sub(r'^\d+[\.\)]\s*', '', item)
                    if item and len(item) > 2 and not item.startswith('http'):
                        equipment.append(item)
                break
        
        return equipment if equipment else ["Bälle", "Hütchen"]
    
    def extract_drills(self, pages: List[str]) -> List[Dict[str, Any]]:
        """Extract individual drills from pages"""
        drills = []
        cumulative_min = 0
        
        for page_num, page_text in enumerate(pages, start=1):
            # Look for drill headers with duration
            # Pattern: "Übung 1: Name (15 Min)" or similar
            drill_pattern = r'(?:Übung|Drill|Teil)\s*(\d+)[:\s]+(.*?)(?:\((\d+)\s*Min)'
            
            matches = re.finditer(drill_pattern, page_text, re.IGNORECASE)
            
            for match in matches:
                drill_num = match.group(1)
                drill_title = match.group(2).strip()
                duration = int(match.group(3)) if match.group(3) else 10
                
                cumulative_min += duration
                
                drill = {
                    "drill_id": f"{self.session_id}-{drill_num}",
                    "title": drill_title,
                    "duration_min": duration,
                    "cumulative_min": cumulative_min,
                    "phase": self._classify_phase(drill_title),
                    "source_page_start": page_num,
                    "text": {
                        "preface": "",
                        "setup": "",
                        "execution": "",
                        "coaching_points": "",
                        "variations": "",
                        "goal": "",
                        "raw_rest": ""
                    },
                    "text_bullets": {
                        "setup": [],
                        "execution": [],
                        "coaching_points": [],
                        "variations": [],
                        "goal": []
                    },
                    "tags": {
                        "formation": "unbekannt",
                        "concept_tags": [],
                        "drill_level": "unbekannt",
                        "requires_goalkeeper": False
                    },
                    "images": []
                }
                
                drills.append(drill)
        
        # If no drills found, create default structure
        if not drills:
            drills = self._create_default_drills()
        
        # Extract images for all pages and distribute to drills
        if self.extract_images:
            all_images = []
            for page_num in range(1, len(pages) + 1):
                page_images = self.extract_images_from_page(page_num)
                all_images.extend(page_images)
            
            # Distribute images to drills based on page numbers
            for drill in drills:
                drill_page = drill["source_page_start"]
                drill["images"] = [img for img in all_images if img["page"] == drill_page]
        
        return drills
    
    def _classify_phase(self, title: str) -> str:
        """Classify drill phase based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['einlaufen', 'aufwärmen', 'warm', 'dehnen']):
            return "Warm-up"
        elif any(word in title_lower for word in ['koordination', 'lauf']):
            return "Koordination"
        elif any(word in title_lower for word in ['ballgewöhnung', 'ballhandling', 'passen']):
            return "Ballhandling"
        elif any(word in title_lower for word in ['torhüter', 'torwart', 'einwerfen']):
            return "Torhüter"
        elif any(word in title_lower for word in ['wurfserie', 'werfen']):
            return "Wurfserie"
        elif any(word in title_lower for word in ['angriff', 'offensive']):
            return "Angriff"
        elif any(word in title_lower for word in ['abwehr', 'defensive']):
            return "Abwehr"
        elif any(word in title_lower for word in ['spiel', 'abschluss']):
            return "Spiel"
        
        return "Angriff"  # Default
    
    def _create_default_drills(self) -> List[Dict[str, Any]]:
        """Create default drill structure when extraction fails"""
        default_phases = [
            ("Einlaufen/Dehnen", "Warm-up", 15),
            ("kleines Spiel", "Spiel", 10),
            ("Ballgewöhnung", "Ballhandling", 10),
            ("Torhüter einwerfen", "Torhüter", 10),
            ("Hauptteil", "Angriff", 35),
            ("Abschlussspiel", "Spiel", 10)
        ]
        
        drills = []
        cumulative = 0
        
        for idx, (title, phase, duration) in enumerate(default_phases, start=1):
            cumulative += duration
            drills.append({
                "drill_id": f"{self.session_id}-{idx}",
                "title": title,
                "duration_min": duration,
                "cumulative_min": cumulative,
                "phase": phase,
                "source_page_start": 2,
                "text": {
                    "preface": "",
                    "setup": "",
                    "execution": "",
                    "coaching_points": "",
                    "variations": "",
                    "goal": "",
                    "raw_rest": ""
                },
                "text_bullets": {
                    "setup": [],
                    "execution": [],
                    "coaching_points": [],
                    "variations": [],
                    "goal": []
                },
                "tags": {
                    "formation": "unbekannt",
                    "concept_tags": [],
                    "drill_level": "unbekannt",
                    "requires_goalkeeper": phase == "Torhüter"
                },
                "images": []
            })
        
        return drills
    
    def extract_session(self) -> Dict[str, Any]:
        """Extract complete session data"""
        pages = self.extract_text_by_page()
        first_page = pages[0] if pages else ""
        all_text = "\n".join(pages)
        
        title = self.extract_title(first_page)
        duration = self.extract_duration(all_text)
        equipment = self.extract_equipment(all_text)
        drills = self.extract_drills(pages)
        
        session = {
            "source_file": self.filename,
            "id": self.session_id,
            "title": title,
            "duration_total_min": duration,
            "equipment": equipment,
            "drills": drills,
            "extraction": {
                "method": "pymupdf_text_regex_v2",
                "notes": "Metadata and drill headers extracted; drill descriptions are referenced via source_page_start to avoid verbatim reproduction."
            },
            "tags": {
                "formation": "unbekannt",
                "focus_area": "unbekannt",
                "concept_tags": [],
                "equipment_tags": self._extract_equipment_tags(equipment)
            }
        }
        
        return session
    
    def _extract_equipment_tags(self, equipment: List[str]) -> List[str]:
        """Extract canonical equipment tags"""
        tags = []
        equipment_text = " ".join(equipment).lower()
        
        tag_mapping = {
            "Hütchen": ["hütchen", "kegel"],
            "Ballkiste": ["ballkiste", "bälle"],
            "Reifen": ["reifen", "ring"],
            "Koordinationsleiter": ["koordinationsleiter", "leiter"],
            "Turnkisten": ["turnkiste", "kasten"],
            "Turnmatte": ["matte", "turnmatte"],
        }
        
        for tag, keywords in tag_mapping.items():
            if any(keyword in equipment_text for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def close(self):
        """Close PDF document"""
        self.doc.close()


def update_library(library_path: str, pdf_dir: str, output_path: str = None, extract_images: bool = True):
    """Update library.json with new sessions from PDF files"""
    
    # Load existing library
    with open(library_path, 'r', encoding='utf-8') as f:
        library = json.load(f)
    
    # Get existing session IDs
    existing_ids = {session['id'] for session in library['sessions']}
    
    # Find all PDF files
    pdf_files = sorted(Path(pdf_dir).glob('*.pdf'))
    
    print(f"Found {len(pdf_files)} PDF files")
    print(f"Existing sessions: {len(existing_ids)}")
    print(f"Image extraction: {'enabled' if extract_images else 'disabled'}")
    
    new_sessions = []
    
    for pdf_file in pdf_files:
        # Extract session ID from filename
        match = re.search(r'(\d+)', pdf_file.name)
        if not match:
            continue
        
        session_id = int(match.group(1))
        
        # Skip if already in library
        if session_id in existing_ids:
            print(f"Skipping {pdf_file.name} (already in library)")
            continue
        
        print(f"Processing {pdf_file.name}...")
        
        try:
            extractor = HandballPDFExtractor(str(pdf_file), extract_images=extract_images)
            session = extractor.extract_session()
            new_sessions.append(session)
            extractor.close()
            
            total_images = sum(len(drill.get('images', [])) for drill in session['drills'])
            print(f"  ✓ Extracted session {session_id}: {session['title']}")
            if extract_images:
                print(f"    Images: {total_images}")
        except Exception as e:
            print(f"  ✗ Error processing {pdf_file.name}: {e}")
    
    # Add new sessions to library
    library['sessions'].extend(new_sessions)
    
    # Sort sessions by ID
    library['sessions'].sort(key=lambda x: x['id'])
    
    # Save updated library
    output_path = output_path or library_path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(library, f, ensure_ascii=False, indent=2)
    
    total_images = sum(
        sum(len(drill.get('images', [])) for drill in session['drills'])
        for session in new_sessions
    )
    
    print(f"\n✓ Added {len(new_sessions)} new sessions")
    print(f"✓ Total sessions: {len(library['sessions'])}")
    if extract_images:
        print(f"✓ Total images extracted: {total_images}")
    print(f"✓ Saved to {output_path}")


def extract_single_pdf(pdf_path: str, output_json: str = None, extract_images: bool = True):
    """Extract a single PDF and optionally save to JSON"""
    print(f"Extracting {pdf_path}...")
    
    extractor = HandballPDFExtractor(pdf_path, extract_images=extract_images)
    session = extractor.extract_session()
    extractor.close()
    
    print(f"\n✓ Extracted session {session['id']}: {session['title']}")
    print(f"  Duration: {session['duration_total_min']} min")
    print(f"  Drills: {len(session['drills'])}")
    print(f"  Equipment: {', '.join(session['equipment'][:3])}...")
    
    if extract_images:
        total_images = sum(len(drill.get('images', [])) for drill in session['drills'])
        print(f"  Images extracted: {total_images}")
    
    if output_json:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        print(f"  Saved to {output_json}")
    
    return session


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pdf_extractor.py single <pdf_file> [output.json] [--no-images]")
        print("  python pdf_extractor.py update <library.json> <pdf_dir> [output.json] [--no-images]")
        sys.exit(1)
    
    command = sys.argv[1]
    extract_images = '--no-images' not in sys.argv
    
    if command == "single":
        pdf_file = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '--no-images' else None
        extract_single_pdf(pdf_file, output, extract_images)
    
    elif command == "update":
        library_file = sys.argv[2]
        pdf_dir = sys.argv[3]
        output = None
        if len(sys.argv) > 4 and sys.argv[4] != '--no-images':
            output = sys.argv[4]
        update_library(library_file, pdf_dir, output, extract_images)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
