# Service Runbook: Syncthing
## 0. System Übersicht
| Eigenschaft | Wert |
| - | - |
| Host | Raspberry Pi 5 |
| IP | 192.168.2.x |
| Port Web UI | 8384 |
| Zugriff | http://syncthing.home |
| Daten | ~/homelab/services/syncthing/data/ |
| Backup | /mnt/backup/DATUM/syncthing-data/ |

## 1. Service Overview 

Syncthing ist eine kostenlose Open-Source-Software für den automatischen Datenabgleich. Es synchronisiert Dateien und Ordner in Echtzeit zwischen Computern, Handys und Tablets. Da es eine sogenannte Peer-to-Peer-Lösung (P2P) ist, werden die Daten direkt zwischen den Geräten ausgetauscht. Es ist kein zentraler Cloud-Anbieter oder Server eines Drittanbieters nötig.

### 1.1 Ziel des Services
-   Synchronisation von Dateien zwischen Desktop, Laptop und mobilen Geräten
-   Keine Abhängigkeit von Cloud-Anbietern
-   Direkter Peer-to-Peer-Datenaustausch
-   Daten verbleiben im eigenen Netzwerk
-   Automatische Synchronisation

### 1.2 Besonderheiten
Syncthing arbeitet nach dem **Peer-to-Peer-Prinzip (P2P)**.

Im Gegensatz zu klassischen Webdiensten reicht es nicht aus, den Service ausschließlich auf dem Raspberry Pi bereitzustellen.

Für die Synchronisation muss Syncthing auf jedem Gerät installiert werden, das Dateien austauschen soll (z. B. Windows-PC, Laptop oder Smartphone).

Vor der ersten Synchronisation sind folgende Schritte erforderlich:

-   Geräte gegenseitig koppeln (Device ID bestätigen)
-   Zu synchronisierende Ordner freigeben
-   Freigaben auf dem Zielgerät bestätigen

Erst danach beginnt die automatische Synchronisation der Dateien.


## 2. Architektur
```
            +----------------+
            | Raspberry Pi   |
            | Syncthing      |
            +--------+-------+
                     |
      +--------------+--------------+
      |                             |
      ▼                             ▼
 Windows PC                    iPhone
      |                             |
      +-------------+---------------+
                    |
                    ▼
          Direkt verschlüsselte
             Synchronisation
```
## 3. Netzwerke & Ports
| Port | Protokoll | Zweck |
| - | - | - |
| 8384| TCP| Web UI |
| 22000 | TCP/UDP | Sync zwischen Geräten |
| 21027 | UDP | Local Discovery |

## 4 Deployment (GitOps – Primary Path)
### 4.1 Voraussetzungen
- Raspberry Pi erreichbar
- Docker & Docker Compose installiert
- GitHub SSH Key eingerichtet
- Homelab Repository vorhanden


### 4.2 Initital Setup / Erstinstallation
Syncthing besitzt standardmäßig **keine Authentifizierung** für die Weboberfläche. Dadurch kann jeder Benutzer im lokalen Netzwerk auf die Konfiguration zugreifen.

Da Syncthing Zugriff auf sensible Daten (z. B. Obsidian-Vaults oder andere synchronisierte Ordner) ermöglicht, sollte die Web UI unmittelbar nach der Erstinstallation mit einem Benutzernamen und Passwort geschützt werden.

#### 4.2.1 Container starten
Syncthing starten:
```Bash
cd ~/homelab/services/syncthing
docker compose up -d
```

#### 4.2.2 Web UI öffnen
```
http://192.168.2.x:8384
```

#### 4.2.3 Anonymes Reporting deaktivieren
Beim ersten Start erscheint die Abfrage zur Teilnahme am anonymen Nutzungsreporting.

Auswahl:

```
No
```

#### 4.2.4 Passwortschutz konfigurieren
`Settings` → `GUI`

Folgende Felder konfigurieren

- **GUI Authentication User** → Benutzername festlegen
- **GUI Authentication Password** → Passwort festlegen

Anschließend **Save** auswählen.

**Hinweis**
In diesem Homelab-Setup wurde die bestehende Web-UI-Verbindung nach dem Aktivieren der GUI-Authentifizierung sofort getrennt. Erst nach einem Neustart des Containers war die Anmeldung mit Benutzername und Passwort wieder möglich.

#### 4.2.5 Container neu starten 
Nach dem Speichern der GUI-Authentifizierung muss der Container neu gestartet werden.

```bash 
docker compose restart syncthing 
``` 
Ohne Neustart kann die Weboberfläche unter Umständen nicht mehr korrekt erreichbar sein.

#### 4.2.6 Verifikation
Web UI erneut öffnen:
```
http://192.168.2.x:8384
```
Erwartung:

-   Login mit Benutzername und Passwort erforderlich
-   Anmeldung erfolgreich
-   Syncthing Dashboard wird angezeigt

### 4.3 Deployment starten
```Bash
cd ~/homelab/services/syncthing
docker compose up -d
```

### 4.4 Verifikation
Container prüfen:
```Bash
docker ps
```
Logs prüfen:
```Bash
docker logs syncthing
```
Webzugriff prüfen:
```
http://syncthing.home
```

## 5. Geräte Koppeln
**Zweck**

Damit Dateien synchronisiert werden können, müssen sich die beteiligten Geräte gegenseitig als vertrauenswürdige Kommunikationspartner kennen.

Dies erfolgt über die eindeutige **Device ID**. Erst nach erfolgreicher Kopplung und Freigabe eines Ordners beginnt die automatische Synchronisation.

### 5.1 Device ID ermitteln 
Jedes Syncthing-Gerät besitzt eine eindeutige Device ID.
Web Ui:

`Actions` → `Show ID`

### 5.2 Gerät hinzufügen
Web UI:
```
Add Remote Device
```
Anschließend die Device ID des Zielgeräts einfügen.

### 5.3 Verbindung bestätigen 
Das Zielgerät erkennt die Verbindungsanfrage und muss diese ebenfalls bestätigen.

Erst danach können Ordner zwischen den Geräten freigegeben werden.

### 5.4 Folder freigeben
Web UI:
`Folder` → `Edit` → `Sharing`

Das gewünschte Gerät auswählen und die Freigabe speichern.

Das Zielgerät muss die Freigabe anschließend bestätigen und einen lokalen Speicherpfad für den Ordner festlegen.

### 5.5 Aktuell gekoppelte Geräte
| Gerät | Betriebssystem | Status |
|-|-|-|
| arasaka (Pi) | Linux | ✅ aktiv |
| Desktop PC | Windows | ✅ aktiv |
| iPhone | iOS | 🔲 geplant |

### Hinweis: Windows Client

Im Homelab wird unter Windows **SyncTrayzor** verwendet.

SyncTrayzor ist ein Open-Source-Frontend für Syncthing und startet den Syncthing-Dienst automatisch mit Windows. Dadurch entfällt das manuelle Starten von `syncthing.exe` nach jedem Systemstart.

Die eigentliche Synchronisation erfolgt weiterhin durch Syncthing.

Download: https://github.com/GermanCoding/SyncTrayzor

## 6. Ordner synchronisieren
### 6.1 Neuen Ordner hinzufügen
Web UI:

```
Add Folder
```

Folgende Felder ausfüllen:

-   **Folder Label** – Lesbarer Name (z. B. `Obsidian Vault`)
-   **Folder Path** – Pfad **im Docker-Container** (z. B. `/var/syncthing/obsidian`)

**Hinweis:**

Der **Folder Path** bezieht sich auf den Pfad **innerhalb des Docker-Containers**, nicht auf den Host-Pfad des Raspberry Pi.

Durch das Volume-Mapping in der `docker-compose.yml` wird der Ordner auf dem Host gespeichert unter:

Container: 
`/var/syncthing/obsidian`

Host: 
`~/homelab/services/syncthing/data/obsidian/`


### 6.2 Ordner mit Gerät teilen
Web UI:

```
Folder → Edit → Sharing
```

Das gewünschte Gerät auswählen und die Freigabe speichern.

Das Zielgerät muss die Freigabe anschließend bestätigen und einen lokalen Speicherpfad für den Ordner festlegen.


### 6.3 Aktuell synchronisierte Ordner
| Ordner | Host-Pfad (Raspberry Pi) | Geräte |
|-|-|-|
| Obsidian Vault | ~/homelab/services/syncthing/data/obsidian/ | Desktop PC |


## 7. Health Checks

### 7.1 Container Status  
  
```bash  
docker ps
```
Erwartung:
```
Up
```
### 7.2 Web UI
```
http://192.168.2.x:8384
```
Erwartung:

-   Login möglich
-   Dashboard wird angezeigt

### 7.3 Geräte Status
Prüfen:
```
Remote Devices
```

Erwartung:

-   Alle gekoppelten Geräte sind **Connected**
-   Keine Verbindungsfehler

**Hinweis:** 
Ist ein Gerät dauerhaft Disconnected, prüfen ob:
- Syncthing auf dem Gerät läuft (SyncTrayzor auf Windows)
- Beide Geräte im gleichen Netzwerk sind

### 7.4 Synchronisationsstatus
Prüfen:
```
Folders
```
Erwartung:

| Status | Bedeutung|
| Up to Date | Alle Dateien synchronisiert |
| Syncing | Synchronisation läuft |
| Out of Sync | Dateien unterscheiden sich|
| Disconnected| Gegenstelle nicht erreichbar |

Für den Normalbetrieb wird erwartet:
```
Up to Date
```

### 7.5 Letzte Synchronisation

Prüfen:

-   Letzte Synchronisation erfolgreich
-   Keine Fehlermeldungen im Event Log

### 7.6 Logs
```Bash
docker logs syncthing --tail  50
```
Erwartung:

-   Keine Fehler
-   Keine dauerhaft wiederkehrenden Warnungen

## 8. Backup & Restore

### 8.1 Besonderheit bei Syncthing Backups
Syncthing synchronisiert Dateien zwischen mehreren Geräten. Dadurch existieren die Daten (z. B. der Obsidian Vault) gleichzeitig auf Raspberry Pi und Desktop-PC.

Vorteile:

-   Die synchronisierten Dateien liegen auf mehreren Geräten vor.
-   Fällt der Raspberry Pi aus, befinden sich die Daten weiterhin auf dem Desktop-PC.
-   Die Peer-to-Peer-Synchronisation bietet eine zusätzliche Redundanz.

**Wichtig:**

Das Backup des Raspberry Pi bleibt dennoch erforderlich, da es zusätzlich die Syncthing-Konfiguration sichert:

-   Gerätekopplungen (Device IDs)
-   Ordnerfreigaben
-   Konfiguration
-   Syncthing-Datenbank

### 8.2 Backup
Service stoppen:
```Bash
cd ~/homelab/services/syncthing 
docker compose down
```
### 8.3 Daten sichern
```Bash
rsync -av \ ~/homelab/services/syncthing/data/ \ /mnt/backup/DATUM/syncthing-data/
```

### 8.4 Restore
Service stoppen:
```Bash
docker compose down
```

Berechtigungen prüfen:
```Bash
sudo chown -R USER:USER ~/homelab/services/syncthing/data/
```

Daten wiederherstellen:
```Bash
rsync -av --no-group --no-times \ /mnt/backup/DATUM/syncthing-data/ \ ~/homelab/services/syncthing/data/
```
Service starten:
```Bash
docker compose up -d
```

### 8.5 Restore Verifikation
Nach einem Restore muss die Funktion geprüft werden.

Checkliste:

-   Container läuft:

```Bash
docker compose ps
```

-   Web UI erreichbar:

```
http://syncthing.home
```
oder
```
http://192.168.2.x:8384
```
-   Anmeldung an der Web UI möglich
-   Gekoppelte Geräte vorhanden
-   Freigegebene Ordner vorhanden
-   Synchronisationsstatus: **Up to Date**

## 9. Update & Maintenance
```Bash
docker compose pull 
docker compose down 
docker compose up -d
```
### 9.1 Nach dem Update prüfen
Nach dem Update prüfen:

-   Container läuft
-   Anmeldung an der Web UI möglich
-   Gekoppelte Geräte verbunden
-   Synchronisation funktioniert
-   Alle Ordner haben den Status **Up to Date**

## 10 Failure Scenarios
Dieser Abschnitt enthält häufige Fehlerbilder und deren Behebung.  
  
Weitere dokumentierte Vorfälle:  
`troubleshooting/log.md`
### 10.1 Container startet nicht
-   `docker ps`
-   `docker logs syncthing`
-   Port 8384 bereits belegt
-   Volume-Probleme
-   Container neu starten

### 10.2 Web UI nicht erreichbar
-   Container läuft?
-   Port 8384 erreichbar?
-   Firewall?
-   Browser öffnen:
    
    ```
    http://192.168.2.x:8384
    ```
    
-   `curl http://localhost:8384`

### 10.3 Geräte verbinden sich nicht
**Symptom:**
`Disconnected`

**Häufige Ursachen**

-   Gerät ausgeschaltet
-   Firewall blockiert Port 22000
-   Device nicht bestätigt
-   Unterschiedliches Netzwerk

**Check**

-   Remote Devices
-   `docker logs syncthing`

### 10.4 Ordner synchronisiert nicht
**Symptom**

```
Out of Sync
```

oder

```
Syncing
```

bleibt dauerhaft bestehen.

**Ursachen**

-   Zielgerät nicht verbunden
-   Freigabe nicht bestätigt
-   Ordnerpfad falsch
-   Berechtigungen

**Verifikation**

Status:

```
Up to Date
```

### 10.5 Änderungen werden auf Windows nicht erkannt
**Symptom**

Dateien ändern sich auf Windows, werden aber nicht synchronisiert.

**Check**

-   Läuft SyncTrayzor?
-   Läuft Syncthing Service?

