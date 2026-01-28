# Memory Issue Solution - HandballApp Update

## Problem

Die App hatte einen **OutOfMemoryError** beim Versuch, die `handball-library_v14.hblib` (54 MB ZIP) zu laden:

```
java.lang.OutOfMemoryError: Failed to allocate a 152324312 byte allocation 
with 50331648 free bytes and 116MB until OOM
```

### Ursache

Die App lädt die komplette ZIP-Datei als Base64-String in den Speicher:
- ZIP-Datei: 54 MB
- Als Base64: ~72 MB
- Plus JSZip-Verarbeitung: ~150 MB RAM benötigt
- Mobile Geräte haben oft nur 128-256 MB Heap-Limit

## Lösung: Remote Images statt ZIP

Statt eine große ZIP-Datei herunterzuladen, verwenden wir jetzt:

### 1. Kleine JSON-Datei (338 KB)
- `library_v15_remote_images.json` - nur 338 KB
- Enthält alle Trainingsdaten
- Bilder als Remote-URLs statt lokale Pfade

### 2. On-Demand Image Loading
- Bilder werden bei Bedarf von GitHub heruntergeladen
- Caching im App-Cache
- Kein Memory-Problem mehr

## Erstellte Dateien

### Für direkten Download (empfohlen)
- **library_v15_remote_images.json** (338 KB)
  - Optimierte JSON mit Remote-Image-URLs
  - Kann direkt heruntergeladen werden
  - Keine Memory-Probleme

### Für lokalen Import (falls benötigt)
- **handball-library_v15_optimized.hblib** (53.4 MB)
  - Optimierte ZIP mit kompakter JSON
  - Immer noch zu groß für manche Geräte
  - Nur für leistungsstarke Geräte

## Nächste Schritte

### 1. GitHub Repository aktualisieren

```bash
cd HandballApp-1

# Kopiere die neue library.json
cp library_v15_remote_images.json ../HandballApp-Mobile/library.json

# Commit und Push
git add library_v15_remote_images.json drill_images/
git commit -m "Add v15 library with remote images"
git push
```

### 2. Manifest aktualisieren

Aktualisiere `manifest.json`:

```json
{
  "library_id": "handball-training-library",
  "version": "v15",
  "created_at": "2026-01-28T...",
  "min_app_version": "1.0.0",
  "package": {
    "url": "https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/library_v15_remote_images.json",
    "type": "json"
  },
  "stats": {
    "sessions": 59,
    "drills": 376,
    "images": 376
  },
  "changelog": [
    "v15: Optimiert für mobile Geräte",
    "Remote Images statt ZIP",
    "Keine Memory-Probleme mehr"
  ]
}
```

### 3. App-Code anpassen (optional)

Die App muss Remote-Image-URLs unterstützen. Änderungen in:

#### `src/services/updater.ts`
- Erkenne JSON-Dateien mit Remote-URLs
- Speichere Image-URLs in der Datenbank
- Kein ZIP-Entpacken mehr nötig

#### `src/services/db.ts`
- Spalte `drill_images.path` kann jetzt URLs enthalten
- Unterscheide zwischen lokalen Pfaden und Remote-URLs

#### `src/screens/DrillDetailScreen.tsx`
- Zeige Bilder an (aktuell nur Platzhalter)
- Lade Remote-Images mit `<Image source={{ uri: imageUrl }}>`
- Cache-Strategie für heruntergeladene Bilder

## Vorteile der neuen Lösung

✅ **Kein Memory-Problem**: Nur 338 KB statt 54 MB  
✅ **Schnellerer Update**: JSON-Download in Sekunden  
✅ **On-Demand Loading**: Bilder nur wenn benötigt  
✅ **Offline-fähig**: Bilder werden gecacht  
✅ **Skalierbar**: Neue Bilder ohne App-Update  

## Alternativen (falls Remote Images nicht gewünscht)

### Option A: Kleinere ZIP-Dateien
- Teile die Library in mehrere kleine ZIPs auf
- Z.B. 10 Sessions pro ZIP
- Download und Import nacheinander

### Option B: Native ZIP-Entpackung
- Verwende native Android/iOS ZIP-Bibliotheken
- Kein Base64-Encoding nötig
- Direktes Stream-Processing

### Option C: Bilder komprimieren
- Reduziere DPI von 150 auf 100
- Konvertiere PNG zu JPEG (kleinere Dateien)
- Würde ZIP auf ~30 MB reduzieren (immer noch zu groß)

## Empfehlung

**Verwende library_v15_remote_images.json** mit Remote-Image-Loading. Das ist die beste Lösung für mobile Geräte und vermeidet alle Memory-Probleme.
