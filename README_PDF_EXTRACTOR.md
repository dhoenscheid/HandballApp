# PDF Extractor für Handball Trainingseinheiten

Dieses Python-Script extrahiert Trainingseinheiten aus PDF-Dateien und aktualisiert die `library.json`.

## Installation

1. **Python installieren** (falls noch nicht vorhanden):
   - Download von https://python.org/downloads/
   - Bei Installation "Add Python to PATH" aktivieren!

2. **PyMuPDF installieren**:
   ```bash
   pip install PyMuPDF
   ```

## Verwendung

### Einzelne PDF analysieren

```bash
python pdf_extractor.py single "files/trainingseinheit 184.pdf" output.json
```

Dies extrahiert die Trainingseinheit und speichert sie in `output.json`.

### Alle fehlenden PDFs verarbeiten

```bash
python pdf_extractor.py update library.json files library_updated.json
```

Dies:
- Lädt die bestehende `library.json`
- Findet alle PDFs im `files/` Ordner
- Extrahiert nur neue Sessions (überspringt bereits vorhandene)
- Speichert das Ergebnis in `library_updated.json`

### Library direkt aktualisieren

```bash
python pdf_extractor.py update library.json files
```

Ohne dritten Parameter wird die `library.json` direkt überschrieben.

## Was wird extrahiert?

Das Script extrahiert folgende Informationen aus den PDFs:

### Session-Level:
- **ID**: Aus dem Dateinamen (z.B. 184 aus "trainingseinheit 184.pdf")
- **Titel**: Schwerpunkt der Trainingseinheit
- **Dauer**: Gesamtdauer in Minuten (Standard: 90)
- **Equipment**: Liste der benötigten Materialien

### Drill-Level:
- **Drill-ID**: Eindeutige ID (z.B. "184-1")
- **Titel**: Name der Übung
- **Dauer**: Dauer in Minuten
- **Phase**: Klassifizierung (Warm-up, Ballhandling, Angriff, etc.)
- **Tags**: Formation, Konzepte, Torhüter-Bedarf

## Struktur der extrahierten Daten

```json
{
  "source_file": "trainingseinheit 184.pdf",
  "id": 184,
  "title": "Abwehrarbeit auf der Außenposition",
  "duration_total_min": 90,
  "equipment": ["Bälle", "Hütchen"],
  "drills": [
    {
      "drill_id": "184-1",
      "title": "Einlaufen/Dehnen",
      "duration_min": 15,
      "phase": "Warm-up",
      ...
    }
  ],
  "tags": {
    "formation": "unbekannt",
    "focus_area": "Abwehr",
    "concept_tags": [],
    "equipment_tags": ["Hütchen", "Ballkiste"]
  }
}
```

## Aktueller Stand

Nach der letzten Ausführung:
- **59 PDFs** gefunden
- **59 Sessions** in der Library
- **40 neue Sessions** hinzugefügt

## Hinweise

- Das Script überspringt automatisch bereits vorhandene Sessions
- Die Extraktion verwendet Default-Werte, wenn spezifische Informationen nicht gefunden werden
- Drill-Beschreibungen werden nicht vollständig extrahiert (nur Referenzen via `source_page_start`)
- Die Struktur ist kompatibel mit der HandballApp-Mobile

## Troubleshooting

**"ModuleNotFoundError: No module named 'fitz'"**
→ PyMuPDF installieren: `pip install PyMuPDF`

**"Python wurde nicht gefunden"**
→ Python installieren und zum PATH hinzufügen

**Falscher Titel extrahiert**
→ Das Script versucht verschiedene Muster, manchmal muss der Titel manuell korrigiert werden

## Weiterentwicklung

Mögliche Verbesserungen:
- Bessere Drill-Extraktion mit detaillierten Beschreibungen
- Automatische Erkennung von Formationen (6:0, 5:1, 3:3)
- Extraktion von Concept-Tags aus dem Text
- Bild-Extraktion und Speicherung
- Spieleranzahl-Erkennung
