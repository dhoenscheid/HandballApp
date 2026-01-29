# Deployment Checklist - HandballApp v16

## ⚠️ WICHTIG: Reihenfolge beachten!

Die Bilder müssen **VOR** dem App-Update auf GitHub sein!

## Schritt 1: GitHub aktualisieren ✅ ZUERST!

```bash
cd HandballApp-1

# Füge alle Dateien hinzu
git add library_v16_remote_images.json
git add manifest.json
git add drill_images/

# Prüfe was hinzugefügt wird
git status

# Commit
git commit -m "Add v16 with cleaned data and full-page images"

# Push zu GitHub
git push origin main
```

**Warte bis der Push abgeschlossen ist!**

## Schritt 2: URLs verifizieren

Öffne im Browser und prüfe, ob die Dateien erreichbar sind:

**Manifest:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/manifest.json
```

**Library:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/library_v16_remote_images.json
```

**Test-Bild:**
```
https://raw.githubusercontent.com/dhoenscheid/HandballApp/main/drill_images/TE_078/TE_078_page_6.png
```

Wenn alle URLs funktionieren → Weiter zu Schritt 3

## Schritt 3: App-Update durchführen

1. **App öffnen**
2. **Einstellungen → Update prüfen**
3. **Warte auf Download:**
   - 338 KB JSON
   - 149 Bilder (~50 MB)
   - Dauer: ~10-30 Sekunden
4. **App neu starten**
5. **Drill öffnen und Bilder prüfen**

## Troubleshooting

### Problem: "unknown image format"
**Ursache:** Bilder sind noch nicht auf GitHub oder wurden als HTML-Fehlerseiten heruntergeladen

**Lösung:**
1. Prüfe ob Bilder auf GitHub sind (siehe Schritt 2)
2. Wenn nicht: Push zu GitHub durchführen
3. App-Daten löschen und Update erneut durchführen

### Problem: "No such file or directory"
**Ursache:** Bilder wurden nicht heruntergeladen oder nicht korrekt verschoben

**Lösung:**
1. App-Daten löschen
2. Update erneut durchführen
3. Prüfe Logs: "Downloaded X/149 images"

### Problem: Update dauert zu lange
**Ursache:** Langsame Internet-Verbindung

**Lösung:**
- Warte oder verwende besseres WLAN
- 149 Bilder à ~350 KB = ~50 MB Download

## Aktueller Status

- ✅ library_v16_remote_images.json erstellt (338 KB)
- ✅ manifest.json aktualisiert (zeigt auf v16)
- ✅ drill_images/ bereinigt (nur full-page screenshots)
- ✅ App-Code angepasst (Bild-Anzeige + Download)
- ⏳ GitHub Push (noch nicht gemacht)
- ⏳ App-Update testen

## Nach erfolgreichem Deployment

- ✅ Bilder werden in der App angezeigt
- ✅ Offline-Funktionalität funktioniert
- ✅ Kein Memory-Problem mehr
- ✅ Kein "UPDATE"-Fehler mehr
- ✅ Alle 59 Sessions verfügbar
- ✅ Alle 376 Drills verfügbar
