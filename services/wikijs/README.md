# Service Runbook: Wiki.js

## 0. System Übersicht
| Eigenschaft | Wert | 
|-------------|------| 
| Host | Raspberry Pi 5 | 
| IP | 192.168.2.x | 
| Port Web UI | 3000 |  
| Daten |  `~/homelab/services/wikijs/data/` | 
| Backup |  `/mnt/backup/DATUM/wikijs/` 

## 1. Service Overview

Wiki.js ist eine moderne, quelloffene (Open-Source) Wiki-Software. Sie dient als zentrale Plattform für Wissensmanagement, Dokumentation oder interne Handbücher und ermöglicht es Teams, Inhalte kollaborativ zu erstellen, zu strukturieren und zu verwalten.

### 1.1 Ziele des Services

- Zentrale Dokumentation des Homelabs
- Dokumentation von Runbooks und Betriebsprozessen
- Wissensmanagement für Infrastruktur und Services
- Nachvollziehbarkeit von Änderungen und Entscheidungen
- Einheitlicher Ablageort für technische Dokumentation

## 2. Architektur
**Zweck**
Wiki.js dient als zentrale Wissens- und Dokumentationsplattform im Homelab.

Alle relevanten Informationen zu Infrastruktur, Services, Runbooks und Troubleshooting werden an einem zentralen Ort gepflegt und versioniert.

### 2.1 Architekturübersicht
```
	    Benutzer 
		│ 
		▼ 
	Wiki.js Port 3000 
		│ 
		▼ 
SQLite Datenbank database.sqlite
```
### 2.3 Datenfluss
1. Benutzer erstellt oder bearbeitet Inhalte 
2. Wiki.js speichert Änderungen in SQLite 
3. Inhalte werden über die Web UI bereitgestellt 
4. Daten werden über das Backup-System gesichert

### 2.4 Persistente Daten
```
~/homelab/services/wikijs/data/
```

Enthält:
- database.sqlite
- Konfigurationen
- Uploads (falls genutzt)


### 2.5 Abhängigkeiten
- Docker Engine
- Docker Compose
- Persistener Speicher
- Backup System

## 3. Netzwerk & Ports

| Port | Protokoll | Zweck |
| ---         |     ---    |          --- |
| 3000  | HTTP       | Web Interface      |



## 4. Deployment (GitOps – Primary Path)
**Ziel**
Der Wiki.js Service wird vollständig reproduzierbar aus einem Git-Repository deployed.  
Das Repository ist die **einzige Quelle der Wahrheit (Single Source of Truth)**.

### 4.1 Vorrausetzung
-   Raspberry Pi ist erreichbar via SSH
-   Docker & Docker Compose installiert
-   Netzwerk (statische IP empfohlen via DHCP Reservation)
-   GitHub SSH Key eingerichtet
- Homelab Repository vorhanden
-   Eine der folgenden Bedingungen ist erfüllt:
	- Vorhandenes Wiki.js Backup (database.sqlite)
	- Durchführung der Erstinstallation gemäß Abschnitt 4.x Erstinstallation

### 4.2 Repository Struktur
```
homelab/  
└── services/  
		└── wikijs/  
				├── docker-compose.yml  
				├── README.md  
				└── data/
```
### 4.3 Repository klonen
```Bash
mkdir  -p ~/homelab/services  
cd ~/homelab/services  
  
git clone git@github.com:DEIN-USERNAME/homelab.git  
cd homelab/services/wikijs
```

### 4.4 Container Stack (Docker Compose)
```YAML
services:
  wiki:
    image: requarks/wiki:2
    restart: unless-stopped
    environment:
      DB_TYPE: sqlite
      DB_FILEPATH: /wiki/database.sqlite

    ports:
      # <Host Port>:<Container Port>
      - "3000:3000"

    volumes:
      - ./data/database.sqlite:/wiki/database.sqlite
```

**Erklärung**
| Teil | Bedeutung | 
| ---         |     ---    |  
| image   | wiki js   | 
| ports    | Web UI       | 
| volumes     | persistente Daten      | 
| restart   | Autostart Verhalten    | 

***Hinweis***

Die `data/database.sqlite` muss aus Backup oder Erstinstallation stammen.
Ohne diese Datei startet Wiki.js im Initial Setup Modus.


### 4.5 Deployment starten 
```Bash
docker compose up -d
```
### 4.6 Verifikation (Post-Deploy Check)
#### 4.6.1 **Container Status**
```Bash
docker ps
```
#### 4.6.2 **Logs Prüfen**
```Bash
docker logs wikijs-wiki-1
```
#### 4.6.3 **Web Ui Prüfen**
```Bash
http://192.168.2.x:3000
```
### 4.7 Zugriff
-   Web UI:  
    `http://192.168.2.x:3000`
-   Login:  
    Benutzer & Passwort beim ersten Login setzen


### 4.8 Erstinstallation (Bootstrap / Initial Setup)
Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist und keine database.sqlite vorhanden ist.

#### 4.8.1 Bootstrap Compose Datei
Für die Erstinstallation wird eine vereinfachte docker-compose.yml verwendet:
```YAML
services:
  wiki:
    image: requarks/wiki:2
    restart: unless-stopped
    environment:
      DB_TYPE: sqlite
      DB_FILEPATH: /wiki/database.sqlite

    ports:
      - "3000:3000"
```

#### 4.8.2 Service starten
```Bash
docker compose up -d
```

#### 4.8.3 Erstinstallation durchführen
Web UI öffnen:
```
http://192.168.2.x:3000
```
Dann:

- Administrator Benutzer anlegen
- Passwort setzen
- Initial Setup abschließen

Dadurch wird automatisch die SQLite-Datenbank erzeugt, falls nicht vorhanden.

#### 4.8.4 SQLite-Datenbank extrahieren
Nach erfolgreicher Initialisierung muss die Datenbank in das GitOps-Setup übernommen werden.

Container ID ermitteln:
```Bash
docker ps
```
SQLite Datei aus dem Contrainer kopieren:
```Bash
docker cp <container-id>:/wiki/database.sqlite ./data/database.sqlite
```

#### 4.8.5 Wechsel in GitOps-Modus
```Bash
docker compose down
docker compose up -d
```

#### 4.8.6 Ergebnis
- Wiki.js läuft im GitOps-Modus
- Datenbank ist persistent unter ./data/database.sqlite
- Alle Inhalte sind versionierbar im Backup-System enthalten


#### 4.9 Manuelle Einrichtung (Fallback / kein Git verfügbar)
Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist.  
Standardmäßig sollte der Service über Git bereitgestellt werden.

Ziel
Manuelle Bereitstellung von Wiki.js ohne GitOps-Workflow.

#### 4.9.1. Verzeichnisstruktur erstellen
```Bash
mkdir  -p ~/homelab/services/wikijs
cd ~/homelab/services/wikijs
```
#### 4.9.2 Docker Compose Datei erstellen
```Bash
nano docker-compose.yml
```
Hier wird die Service-Definition manuell hinterlegt (siehe GitOps Template als Referenz).

**Hinweis:**
Änderungen an der Konfiguration erfolgen ausschließlich über das Git-Repository. Manuelle Änderungen an laufenden Containern sind nicht zulässig und gehen beim nächsten Re-Deployment verloren.

#### 4.9.3 Erstinstallation im Browser
```
http://192.168.2.x:3000
```

#### 4.9.4 Datenbank persistieren (optional nach Setup)
```Bash
docker cp <container-id>:/wiki/database.sqlite ./data/database.sqlite
```
 
## 5. Operations
Alle Befehle im Verzeichnis der `docker-compose.yml` ausführen 
### 5.1 **Start:**
```Bash
docker compose up -d
```
### 5.2 **Stop:**
```Bash
docker compose down
```
### 5.3 **Restart:**
```Bash
docker compose restart wikijs-wiki-1
```
### 5.4 **Logs:**
```Bash
docker logs -f wikijs-wiki-1
```
### 5.5 **Status:**
```Bash
docker ps
```

## 6. Health Checks

### 6.1 **Container Health**
```bash
docker ps
```
Erwartung: 
- Status `Up` und `(healthy)`
- Kein `Restarting`

### 6.2 **Web UI**
http://192.168.2.x:3000
Erwartung: 
- Login-Seite erreichbar
- Kein 502 / 504 Fehler
- Kein „Cannot connect to database“


### 6.3 **Wiki.js Status**
```bash
docker logs wikijs-wiki-1 --tail 50
```
Erwartung:
- Keine Fehler wie:
	- `SQLITE_CANTOPEN`
	- `EACCES permission denied`
	- `database locked`
- Startmeldung von Wiki.js sichtbar, z. B.:
	- `Loading configuration from /wiki/config.yml... OK`

### 6.4 Datenbank erreichbar
Optionaler Check:
```bash
ls -l ~/homelab/services/wikijs/data/
```
Erwartung:
- database.sqlite existiert
- Datei ist nicht 0 Bytes

## 7. Backup & Restore

### 7.1 **Wiki.js Service stoppen**
```bash
cd ~/homelab/services/wikijs
docker compose down
```
### 7.2 **Berechtigungen setzen**
```bash
sudo chown -R USER:USER ~/homelab/services/wikijs/data/
```

### 7.3 **Daten wiederherstellen**
```bash
rsync -av --no-group --no-times /mnt/backup/DATUM/wikijs-data/ \
~/homelab/services/wikijs/data/
```

### 7.4 **Service starten**
```bash
docker compose up -d
```

Verifikation:
- Webinterface erreichbar 
- Login mit Admin-Account funktioniert
-  Wiki-Inhalte (Seiten) sind vorhanden



## 8. Update & Maintenance
```bash
docker compose pull  
docker compose down  
docker compose up -d
```
### 8.1  **Nach dem Update prüfen:** 
- Container läuft: `docker ps`
- Web UI erreichbar: `http://192.168.2.x:3000` 
- Wiki.js logs: `docker logs wikijs-wiki-1` 

**Hinweis:**
Updates dürfen nur nach erfolgreichem Health Check durchgeführt werden.

## 9. Failure Scenarios
### 9.1 Container startet nicht
#### 9.1.1 **Symptom**
-   Web UI nicht erreichbar
-   `docker ps` zeigt keinen laufenden Container

#### 9.1.2 **Check**
```bash
docker ps  -a
docker logs wikijs-wiki-1
```
#### 9.1.3 **Häufige Ursachen**
-   Port 3000 bereits belegt
-   Fehlerhafte Volume-Mounts
-   Beschädigte SQLite-Datenbank (`database.sqlite`)
-   Falsche Berechtigungen im `data/` Verzeichnis

#### 9.1.4 **Fix 1: Port Prüfen:**
```bash
sudo ss -tlnp |  grep :3000
```
#### 9.1.5 **Fix 2: Container neu starten:**
```bash
docker compose down
docker compose up -d
```

#### 9.1.6 **Verify**
```bash
docker ps
```
Erwartung: Container Status: `Up`


### 9.2 Web UI nicht erreichbar
#### 9.2.1 **Symptom**
Browser kann Wiki.js nicht öffnen.

#### 9.2.2 **Check**
Prüfen ob Container läuft
```bash
docker ps
curl -I http://localhost:3000
```
#### 9.2.3 **Häufige Ursachen**

-   Container läuft nicht
-   Firewall / Netzwerkproblem
-   Falsche IP-Adresse verwendet
-   Port nicht exposed

#### 9.2.4 **Fix: Container neu starten:**
```bash
docker restart wikijs-wiki-1
```

#### 9.2.5 **Verify**
Web UI erreichbar:
```bash
http://192.168.2.x:3000
```


