# Service Runbook: Nginx Proxy Manager

## 0. System Übersicht
| Eigenschaft | Wert | 
|-------------|------| 
| Host | Raspberry Pi 5 | 
| IP | 192.168.2.x | 
| Port Web UI | 81 |  
| Daten |  `~/homelab/services/nginx-proxy-manager/data/` | 
| Backup |  `/mnt/backup/DATUM/nginx-proxy-manager-data/` 

## 1. Service Overview

Nginx Proxy Manager (NPM) ist ein Reverse Proxy mit Weboberfläche zur zentralen Verwaltung interner Webdienste. Der Service leitet Anfragen an die entsprechenden Backend-Dienste weiter und ermöglicht die einfache Verwaltung von Domains, SSL-Zertifikaten und Zugriffskontrollen.

### 1.1 Ziele des Services
-   Zentraler Zugriffspunkt für Webanwendungen im Homelab
-   Vereinfachte Verwaltung von Reverse Proxies
-   Einheitliche URLs für interne Dienste
-   SSL/TLS-Zertifikatsverwaltung
-   Trennung von Backend-Diensten und Benutzerzugriffen

### 1.2 Eingerichtete Proxy Hosts

| Domain | Zielsystem |   Port | 
|----------|----------| ----------| 
| pihole.home | 192.168.2.x |   8080 | 
| uptime.home | 192.168.2.x |   3001 | 
| npm.home| 192.168.2.x |   81 | 
| wiki.home| 192.168.2.x |   3000 |
| vaultwarden.home | 192.168.2.x | 11001 | 

## 2. Architektur
**Zweck**
Nginx Proxy Manager dient als zentraler Reverse Proxy im Homelab.  
Er stellt eine einheitliche Zugriffsschicht für interne Webdienste bereit und trennt dabei Benutzerzugriff von Backend-Services.
### 2.1 Architekturübersicht
```
Internet / LAN Clients
        │
        ▼
Nginx Proxy Manager
        │
 ┌──────┼─────────┬─────────┐
 ▼      ▼         ▼         ▼
Pi-hole  Uptime   NPM UI   weitere Services
```
### 2.3 Datenfluss
1. Client ruft Domain auf (z. B. uptime.home)  
2. DNS löst auf NPM IP auf  
3. NPM empfängt Request  
4. Weiterleitung an Backend-Service  
5. Antwort zurück an Client


## 3. Netzwerk & Ports

| Port | Protokoll | Zweck |
| ---         |     ---    |          --- |
| 81   | HTTP       | Web Interface      |
| 443   | HTTPS     | Public Port      |
| 80   | HTTP       | Public Port      |


## 4. Deployment (GitOps – Primary Path)
**Ziel**
Der Pi-hole Service wird vollständig reproduzierbar aus einem Git-Repository deployed.  
Das Repository ist die **einzige Quelle der Wahrheit (Single Source of Truth)**.

### 4.1 Vorrausetzung
-   Raspberry Pi ist erreichbar via SSH
-   Docker & Docker Compose installiert
-   Netzwerk (statische IP empfohlen via DHCP Reservation)
-   GitHub SSH Key eingerichtet

### 4.2 Repository Struktur
```
homelab/  
└── services/  
		└── nginx-proxy-manager/  
				├── docker-compose.yml  
				├── README.md  
				└── data/
```
### 4.3 Repository klonen
```Bash
mkdir  -p ~/homelab/services  
cd ~/homelab/services  
  
git clone git@github.com:DEIN-USERNAME/homelab.git  
cd homelab/services/nginx-proxy-manager
```

### 4.4 Container Stack (Docker Compose)
```YAML
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped

    ports:
      # These ports are in format <host-port>:<container-port>
      - '80:80' # Public HTTP Port
      - '443:443' # Public HTTPS Port
      - '81:81' # Admin Web Port
      # Add any other Stream port you want to expose
      # - '21:21' # FTP

    environment:
      TZ: "Europe/Berlin"

      # Uncomment this if you want to change the location of
      # the SQLite DB file within the container
      # DB_SQLITE_FILE: "/data/database.sqlite"

      # Uncomment this if IPv6 is not enabled on your host
      # DISABLE_IPV6: 'true'

    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```
**Erklärung**
| Teil | Bedeutung | 
| ---         |     ---    |  
| image   | nginx proxy manager Image   | 
| ports    | DNS + Web UI       | 
| volumes     | persistente Daten      | 
| restart   | Autostart Verhalten    | 

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
docker logs nginx-proxy-manager-app-1
```
#### 4.6.3 **Web Ui Prüfen**
```Bash
http://192.168.2.x:81
```
### 4.7 Zugriff
-   Web UI:  
    `http://192.168.2.x:81`
-   Login:  
    Passwort beim ersten Login setzen

### 4.8 Manuelle Einrichtung (Fallback / kein Git verfügbar)
Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist.  
Standardmäßig sollte der Service über Git bereitgestellt werden.
#### 4.8.1. Verzeichnisstruktur erstellen
```Bash
mkdir  -p ~/homelab/services/nginx-proxy-manager
cd ~/homelab/services/nginx-proxy-manager
```
#### 4.8.2 Docker Compose Datei erstellen
```Bash
nano docker-compose.yml
```
Hier wird die Service-Definition manuell hinterlegt (siehe GitOps Template als Referenz).

**Hinweis:**
Änderungen an der Konfiguration erfolgen ausschließlich über das Git-Repository. Manuelle Änderungen an laufenden Containern sind nicht zulässig und gehen beim nächsten Re-Deployment verloren.
 
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
docker compose restart nginx-proxy-manager-app-1
```
### 5.4 **Logs:**
```Bash
docker logs -f nginx-proxy-manager-app-1
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
Erwartung: Status `Up` und `(healthy)`

### 6.2 **Web UI**
http://192.168.2.x:81
Erwartung: Login-Seite erreichbar


### 6.3 **Nginx Proxy Manager Status**
```bash
docker logs nginx-proxy-manager-app-1
```
Erwartung:
```
❯ Starting nginx ...
❯ Starting backend ...
```
## 7. Backup & Restore

### 7.1 **Nginx Proxy Manager Service stoppen**
```bash
cd ~/homelab/services/nginx-proxy-manager
docker compose down
```
### 7.2 **Berechtigungen setzen**
```bash
sudo chown -R USER:USER ~/homelab/services/nginx-proxy-manager/data/
```

### 7.3 **Daten wiederherstellen**
```bash
rsync -av --no-group --no-times /mnt/backup/DATUM/nginx-proxy-manager-data/ \
~/homelab/services/nginx-proxy-manager/data/
```

### 7.4 **Service starten**
```bash
docker compose up -d
```

Verifikation:
- Webinterface erreichbar 
-  Proxy Hosts funktionieren 
-  SSL-Zertifikate aktiv


## 8. Update & Maintenance
```bash
docker compose pull  
docker compose down  
docker compose up -d
```
### 8.1  **Nach dem Update prüfen:** 
- Container läuft: `docker ps`
- Web UI erreichbar: `http://192.168.2.x:81` 
-  nginx logs: `docker logs nginx-proxy-manager-app-1` 

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
docker logs nginx-proxy-manager-app-1
```
#### 9.1.3 **Häufige Ursachen**
-   Port 81 bereits belegt
-   Fehlerhafte Volume-Mounts
-   Beschädigte Datenbank

#### 9.1.4 **Fix 1: Port Prüfen:**
```bash
sudo ss -tlnp |  grep :81
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
Erwartung: `Up x (healthy)`

### 9.2 Web UI nicht erreichbar
#### 9.2.1 **Symptom**
Browser kann Nginx Proxy Manager nicht öffnen.

#### 9.2.2 **Check**
Prüfen ob Container läuft
```bash
docker ps
```
Ist der Port erreichbar
```bash
curl -I http://localhost:81
```
#### 9.2.3 **Häufige Ursachen**

-   Container läuft nicht
-   Firewall blockiert
-   Falsche IP-Adresse verwendet

#### 9.2.4 **Fix: Container neu starten:**
```bash
docker restart nginx-proxy-manager-app-1
```

#### 9.2.5 **Verify**
Web UI erreichbar:
```bash
http://192.168.2.x:81
```

### 9.3 Proxy Host liefert Fehler (403 / 502 / 504)

#### 9.3.1 Symptom 

-   403 Forbidden
-   502 Bad Gateway
-   504 Gateway Timeout

#### 9.3.2 Grundverständnis
Diese Fehler bedeuten:
| Fehler | Bedeutung |
|  --------  |  -------  |
| 403 | Zugriff verweigert |
| 502 | Backend nicht erreichbar |
| 504 | Backend antwortet nicht rechtzeitig |

#### 9.3.3 Prüfen Zielsystem erreichbar
```bash
ping  192.168.2.x
curl http://192.168.2.x:81
```
Erwartung: Dienst muss direkt erreichbar sein (ohne NPM)

#### 9.3.4 Check: Proxy Host Konfiguration
Im Nginx Proxy Manager:
```
Hosts → Proxy Hosts → Edit
```
Prüfen:

-   Domain korrekt?
-   Forward Hostname / IP korrekt?
-   Port korrekt gesetzt?

Beispiel Pi-hole:
```
Forward Host: 192.168.2.x  
Forward Port: 80
```
Wichtig:  
`/admin` gehört **NICHT** in NPM, sondern in den Browserpfad des Services.

 #### 9.3.5 Check: läuft Service 
```bash
docker ps
```
oder spezifisch:
```bash
docker logs pihole
```
 #### 9.3.6 Häufige Ursachen
**502 Bad Gateway**

-   Backend Container down
-   falsche IP / Port
-   Service crashed

----------

**504 Gateway Timeout**

-   Service hängt
-   Firewall blockiert
-   falsches Netzwerk (Docker bridge Problem)

----------

**403 Forbidden**

-   Zugriffsbeschränkung im Service selbst
-   falscher Pfad (z. B. `/admin` vs `/`)

#### 9.3.7 Fix
##### 9.3.7.1 Proxy neu laden
```bash
NPM UI → Save → Apply
```
##### 9.3.7.2 Container neu starten
```bash
docker restart nginx-proxy-manager-app-1
```

##### 9.3.7.3 Backend testen
```bash
curl -I http://192.168.2.x:PORT
```
Erwartung:
```
HTTP/1.1 200 OK
```
#### 9.3.8 Verify 
-   Domain erreichbar (z. B. `http://pihole.home`)
-   Keine Fehlerseite
-   Backend UI funktioniert direkt + über Proxy
