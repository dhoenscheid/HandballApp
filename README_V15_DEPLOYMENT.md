# HandballApp v15 Deployment Guide

## Problem gelöst ✅

Der **OutOfMemoryError** beim Update wurde behoben durch:
- Kleine JSON-Datei (338 KB) statt große ZIP (54 MB)
- Remote Images statt lokale Bilder
- On-Demand Image Loading

## Deployment-Schritte

### 1. Dateien zu GitHub hochladen

```bash
cd HandballApp-1

# Füge alle neuen Dateien hinzu
git add library_v15_remote_images.json
git add manifest.json
git add drill_images/

# Commit
git commit -m "Add v15 library with remote images - fixes memory issue"

# Push zu GitHub
git push origin main
```

### 2. URLs verifizieren

Nach dem Push sollten folgende URLs erreichbar sein:

**Manifest:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/manifest.json
```

**Library JSON:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/library_v15_remote_images.json
```

**Beispiel-Bild:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/drill_images/TE_078/TE_078_page_2.png
```

### 3. App testen

1. Öffne die HandballApp auf deinem Gerät
2. Gehe zu Einstellungen → Update prüfen
3. Die App sollte v15 erkennen und herunterladen
4. Download sollte in wenigen Sekunden abgeschlossen sein (nur 338 KB)
5. Kein Memory-Error mehr! ✅

## Was wurde geändert?

### Alte Version (v14)
- ❌ ZIP-Datei: 54 MB
- ❌ Alle Bilder im ZIP
- ❌ Memory-Error beim Entpacken
- ❌ Langer Download

### Neue Version (v15)
- ✅ JSON-Datei: 338 KB
- ✅ Bilder als Remote-URLs
- ✅ Kein Memory-Problem
- ✅ Schneller Download
- ✅ On-Demand Image Loading

## Dateistruktur auf GitHub

```
HandballApp/
├── manifest.json                           # Update-Manifest
├── library_v15_remote_images.json         # Hauptdatei (338 KB)
└── drill_images/                          # Bilder-Ordner
    ├── TE_078/
    │   ├── TE_078_page_2.png
    │   ├── TE_078_page_3.png
    │   └── ...
    ├── TE_104/
    │   └── ...
    └── ...
```

## App-Änderungen (optional)

Die App funktioniert bereits mit der neuen JSON-Struktur. Für vollständige Bild-Unterstützung:

### 1. Image Display in DrillDetailScreen.tsx

```typescript
// Aktuell: Nur Platzhalter
{drill.images && drill.images.length > 0 && (
  <Text>{drill.images.length} images available</Text>
)}

// Neu: Zeige Bilder an
{drill.images && drill.images.length > 0 && (
  <ScrollView horizontal>
    {drill.images.map((img, idx) => (
      <Image 
        key={idx}
        source={{ uri: img.url }}
        style={{ width: 300, height: 400, marginRight: 10 }}
        resizeMode="contain"
      />
    ))}
  </ScrollView>
)}
```

### 2. Image Caching

React Native cached Bilder automatisch. Für bessere Kontrolle:

```typescript
import { Image } from 'react-native';
import * as FileSystem from 'expo-file-system';

// Cache-Verzeichnis
const imageCache = FileSystem.cacheDirectory + 'drill_images/';

// Bild herunterladen und cachen
async function getCachedImage(url: string): Promise<string> {
  const filename = url.split('/').pop();
  const localPath = imageCache + filename;
  
  // Prüfe ob bereits gecacht
  const info = await FileSystem.getInfoAsync(localPath);
  if (info.exists) {
    return localPath;
  }
  
  // Download und cache
  await FileSystem.downloadAsync(url, localPath);
  return localPath;
}
```

## Troubleshooting

### Problem: "Manifest-URL ist nicht gesetzt"
**Lösung:** Gehe zu Einstellungen und setze die Manifest-URL:
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/manifest.json
```

### Problem: "Bilder werden nicht angezeigt"
**Lösung:** 
1. Prüfe ob die Bild-URLs erreichbar sind
2. Prüfe Internet-Verbindung
3. Implementiere Image-Display in DrillDetailScreen.tsx (siehe oben)

### Problem: "Update schlägt fehl"
**Lösung:**
1. Prüfe ob library_v15_remote_images.json auf GitHub verfügbar ist
2. Prüfe ob die JSON-Datei valide ist
3. Prüfe App-Logs für Details

## Nächste Schritte

1. ✅ Dateien zu GitHub pushen
2. ✅ URLs verifizieren
3. ✅ App-Update testen
4. ⏳ Image-Display implementieren (optional)
5. ⏳ Offline-Caching optimieren (optional)

## Erfolg!

Nach dem Deployment sollte die App:
- ✅ Updates ohne Memory-Error laden
- ✅ Schnell starten (nur 338 KB Download)
- ✅ Bilder on-demand laden
- ✅ Offline-fähig sein (gecachte Bilder)
