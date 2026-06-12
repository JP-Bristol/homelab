# Runbook Backup & Restore

## 1.System-Übersicht
-   **Host-System:** Raspberry Pi 5
-   **IP-Adresse:** 192.168.2.x
-   **Backup-Speicher:** USB-Stick
-   **Mount-Pfad:** `/mnt/backup`

## 2. Backup-Prozess
**Ziel**
Schutz vor Datenverlust durch automatisierte tägliche Sicherungen.

**Backup-Script Pfad**
```
~/homelab/scripts/backup.sh
```

**Ausführung**
Die Backups werden täglich um **03:00 Uhr** via Cronjob erstellt.

**Aufbewahrung**
-   Retention: **7 Tage**
-   Ältere Backups werden automatisch gelöscht
## 3. Backup-Inhalt
### 3.1 Homelab-Konfiguration
```
~/homelab/
```
Enthält:

-   Docker Compose Dateien
-   Dokumentation
-   Skripte
-   Konfigurationsdateien

### 3.2 Service-Daten
#### Pi-hole

-   DNS-Listen
-   Whitelists / Blacklists
-   DNS-Konfiguration

#### Uptime Kuma

-   Monitore
-   Statushistorie
-   Benutzereinstellungen

#### Nginx Proxy Manager

-   Proxy Hosts
-   SSL-Zertifikate
-   Access Lists

## 4. Backup-Speicherort
```
/mnt/backup/
```
Beispiel
```
/mnt/backup/  
├── 2026-06-07/  
├── 2026-06-08/  
└── 2026-06-09/
```
## 5. Restore-Prozess
**Voraussetzungen**
Vor jedem Restore:

-   Passendes Backup identifizieren
-   Betroffenen Service stoppen
-   Daten zurückkopieren
-   Service starten
-   Funktion prüfen

## 5.1 Allgemeines Restore-Schema (Standardverfahren)
Dieses Schema gilt für alle Services im Homelab
**Schritt 1: Backup auswählen**
```
/mnt/backup/<DATUM>/
```
-   korrektes Backup-Verzeichnis identifizieren
-   prüfen, ob Zeitpunkt plausibel ist

**Schritt 2: Service stoppen**
```Bash
docker compose down
```
**Schritt 3: Berechtigungen setzen**
```Bash
sudo chown -R USER:USER ~/homelab/services/SERVICE/data/
```
**Schritt 4: Daten wiederherstellen**
```Bash
rsync -av --no-group --no-times /mnt/backup/<DATUM>/<service>/data/ <service-path>/data/
```
**Schritt 5: Service starten**
```Bash
docker compose up -d
```
**Schritt 6: Funktion prüfen**
-   Web UI erreichbar?
-   Logs fehlerfrei?
-   Kernfunktion getestet?

**Schritt 7: Optional – Logs prüfen**
```Bash
docker logs <container>
```
**Hinweis:**
Jeder Restore folgt diesem Schema. Abweichungen müssen im jeweiligen Service-Runbook dokumentiert werden.

**Restore-Anleitungen siehe:**
-   `services/pihole/README.md`
-   `services/uptime-kuma/README.md`
-   `services/nginx-proxy-manager/README.md`

## 6 Verifikation

**Verfügbare Backups anzeigen**
```Bash
ls -lah /mnt/backup
```
**Backup-Größe prüfen**
```Bash
du -sh /mnt/backup/*
```
**Letztes Backup prüfen**
```Bash
ls -lt /mnt/backup
```

## 7 Troubleshooting
**USB-Stick nicht verfügbar**
```Bash
df -h
mount | grep backup
```
**Backup-Verzeichnis leer**
```Bash
ls -lah /mnt/backup
```
**Restore fehlgeschlagen**
```Bash
docker logs <container>
```
**Berechtigungsprobleme**
```Bash
sudo chown -R jp:jp /mnt/backup
```
**Hinweis:**
Weitere bekannte Probleme → `troubleshooting/log.md`
