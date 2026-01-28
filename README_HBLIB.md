# Handball Library Package (.hblib)

## Übersicht

Die `.hblib`-Datei ist ein ZIP-Archiv, das die komplette Trainingsbibliothek mit allen Bildern enthält und in die HandballApp importiert werden kann.

## Erstellte Dateien

- **handball-library_v14.hblib** (54.5 MB)
  - 59 Trainingseinheiten
  - 376 Drills
  - 149 einzigartige Seitenbilder (PNG, 150 DPI)

## Struktur der .hblib-Datei

```
handball-library_v14.hblib (ZIP-Archiv)
├── library.json                              # Trainingsdaten
└── images/
    ├── drill_images_manifest_v2.json        # Bild-Manifest
    └── drill_images_v2/                     # Alle Drill-Bilder
        ├── TE_078/
        │   ├── TE_078_page_2.png
        │   ├── TE_078_page_3.png
        │   └── ...
        ├── TE_104/
        │   └── ...
        └── ...
```

## Unterschied zu v13

**v13 (handball-library_v13.hblib)**:
- Verwendet embedded images (einzelne Icons, Pfeile, Diagramm-Elemente)
- Viele kleine Bilder pro Drill
- Bilder waren oft abgeschnitten

**v14 (handball-library_v14.hblib)**:
- Verwendet full-page screenshots
- Ein Bild pro PDF-Seite
- Komplette Seiten mit allen Diagrammen und Text
- Bessere Qualität und Lesbarkeit

## Import in die App

### Option 1: Direkter Import (empfohlen)
1. Kopiere `handball-library_v14.hblib` auf dein Gerät
2. Öffne die HandballApp
3. Gehe zu Einstellungen → Bibliothek importieren
4. Wähle die .hblib-Datei aus

### Option 2: Cloud-Hosting
1. Lade `handball-library_v14.hblib` auf einen Server hoch
2. Aktualisiere die URL in der App-Konfiguration
3. Die App lädt die Bibliothek automatisch herunter

## Bild-Referenzen in der App

Die Bilder werden in der `library.json` wie folgt referenziert:

```json
{
  "drill_id": "78-1",
  "images": [
    {
      "path": "drill_images/TE_078/TE_078_page_2.png",
      "page": 2,
      "order": 1,
      "type": "full_page"
    }
  ]
}
```

Die App muss die Pfade entsprechend auflösen:
- Im ZIP: `images/drill_images_v2/TE_078/TE_078_page_2.png`
- In der JSON: `drill_images/TE_078/TE_078_page_2.png`

## Manifest-Format

Das `drill_images_manifest_v2.json` enthält eine Übersicht aller Bilder:

```json
{
  "version": "v2",
  "root": "drill_images_v2",
  "type": "full_page_screenshots",
  "created_at": "2026-01-28T...",
  "drills": {
    "78-1": {
      "session_id": 78,
      "images": [
        "drill_images_v2/TE_078/TE_078_page_2.png"
      ]
    }
  }
}
```

## Erstellung einer neuen .hblib

Um eine neue .hblib-Datei zu erstellen:

```bash
# 1. PDFs extrahieren (falls neue PDFs vorhanden)
python pdf_extractor.py all

# 2. Bilder aus PDFs extrahieren
python pdf_to_images.py

# 3. .hblib-Paket erstellen
python create_hblib.py
```

## Technische Details

- **Format**: ZIP-Archiv mit Deflate-Kompression
- **Bildformat**: PNG
- **Bildauflösung**: 150 DPI
- **JSON-Encoding**: UTF-8
- **Dateigröße**: ~54 MB (komprimiert)

## Nächste Schritte

1. Teste den Import in der HandballApp-Mobile
2. Überprüfe, ob die Bilder korrekt angezeigt werden
3. Stelle sicher, dass die Bild-Pfade korrekt aufgelöst werden
4. Ggf. App-Code anpassen, um v2-Manifest zu unterstützen
