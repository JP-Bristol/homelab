# Service Runbook: Pi-hole (DNS & Adblocker)

## 0. System Übersicht
| Eigenschaft | Wert | 
|-------------|------| 
| Host | Raspberry Pi 5 | 
| IP | 192.168.2.x | 
| Port Web UI | 8080 | 
| Port DNS | 53 | 
| Daten |  `~/homelab/services/pihole/data/`  | 
| Backup |  `/mnt/backup/DATUM/pihole-data/` 

## 1. Service Overview

Pi-hole ist ein netzwerkweiter DNS-basierter Werbe- und Tracking-Blocker.  
Alle DNS-Anfragen im Netzwerk werden zentral verarbeitet und unerwünschte Domains gefiltert.

### Ziele des Services

-   Netzwerkweites Adblocking
-   Zentrale DNS-Auflösung
-   Tracking-Reduktion auf allen Geräten
-   Transparente DNS-Kontrolle im Homelab

## 2. Architektur

Optional:

-   DHCP wird vom Router bereitgestellt
-   Pi-hole übernimmt ausschließlich DNS Filtering

## 3. Netzwerk & Ports


| Port | Protokoll | Zweck |
| ---         |     ---    |          --- |
| 53   | TCP/UDP     | DNS Resolution    |
| 80     | HTTP       | Web Interface      |
| 443     | HTTPS       | optional (TLS UI)     |

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
		└── pihole/  
				├── docker-compose.yml  
				├── .env.example  
				├── README.md  
				└── data/
```
### 4.3 Repository klonen
```Bash
mkdir  -p ~/homelab/services  
cd ~/homelab/services  
  
git clone git@github.com:DEIN-USERNAME/homelab.git  
cd homelab/services/pi-hole
```

### 4.4 Environment konfigurieren
```Bash
cp .env.example .env  
nano .env
```
Beispiel:
```Bash
TZ=Europe/Berlin  
FTLCONF_webserver_api_password=secure-password
```
### 4.5 Container Stack (Docker Compose)
```YAML
services:  
pihole:  
image: pihole/pihole:latest  
container_name: pihole  
  
ports:  
- "53:53/tcp"  
- "53:53/udp"  
- "8080:80"  
  
environment:  
TZ: "Europe/Berlin"  
FTLCONF_webserver_api_password: ${FTLCONF_webserver_api_password}  
  
volumes:  
- ./etc-pihole:/etc/pihole  
- ./etc-dnsmasq.d:/etc/dnsmasq.d  
  
restart: unless-stopped
```
**Erklärung**
| Teil | Bedeutung | 
| ---         |     ---    |  
| image   | Pi-hole Docker Image   | 
| ports    | DNS + Web UI       | 
| volumes     | persistente Daten      | 
| environment   | Konfiguration     | 
| restart   | Autostart Verhalten    | 

### 4.6 Deployment starten 
```Bash
docker compose up -d
```
### 4.7 Verifikation (Post-Deploy Check)
**Container Status**
```Bash
docker ps
```
**Pi-hole Status**
```Bash
docker exec pihole pihole status
```
**DNS TEST**
```Bash
dig @192.168.2.x google.com
```
### 4.8 Zugriff
-   Web UI:  
    `http://192.168.2.x:8080/admin`
-   Login:  
    Passwort aus `.env` (FTLCONF_webserver_api_password)

### 4.9 Manuelle Einrichtung (Fallback / kein Git verfügbar)
Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist.  
Standardmäßig sollte der Service über Git bereitgestellt werden.
#### 4.9.1. Verzeichnisstruktur erstellen
```Bash
mkdir  -p ~/homelab/services/pi-hole  
cd ~/homelab/services/pi-hole
```
#### 4.9.2 Docker Compose Datei erstellen
```Bash
nano docker-compose.yml
```
Hier wird die Service-Definition manuell hinterlegt (siehe GitOps Template als Referenz).

#### 4.9.3 Environment Datei anlegen
```Bash
cp .env.example .env  
nano .env
```
**Beispiel:**
```YAML
FTLCONF_webserver_api_password=secure-password  
TZ=Europe/Berlin
```
**Hinweis:**

-   Passwort wird beim ersten Start verwendet
-   danach persistiert Pi-hole intern

#### 4.9.4 Passwort & Login Recovery
Falls der Login nicht funktioniert:
```Bash
docker exec pihole pihole setpassword NEUESPASSWORT
```
**Hinweis:**
Änderungen an der Konfiguration erfolgen ausschließlich über das Git-Repository. Manuelle Änderungen an laufenden Containern sind nicht zulässig und gehen beim nächsten Re-Deployment verloren.
 
## 5. Operations
Alle Befehle im Verzeichnis der `docker-compose.yml` ausführen 
**Start:**
```Bash
docker compose up -d
```
**Stop:**
```Bash
docker compose down
```
**Restart:**
```Bash
docker compose restart pihole
```
**Logs:**
```Bash
docker logs -f pihole
```
**Status:**
```Bash
docker ps
```
## 6. Configuration
**Admin Passwort Setzen**
```Bash
docker exec pihole pihole setpassword
```

## 7. Health Checks

**Container Health**
```bash
docker ps
```
Erwartung: Status `Up` und `(healthy)`

**DNS-Auflösung**
```bash
dig @192.168.2.x google.com
```
Erwartung: `status: NOERROR`

**Web UI**
http://192.168.2.x:8080/admin
Erwartung: Login-Seite erreichbar

**Pi-hole Status**
```bash
docker exec pihole pihole status
```

Erwartung: Pi-hole blocking is enabled

## 8. Backup & Restore

**Pi-hole Service stoppen**
```bash
cd ~/homelab/services/pihole
docker compose down
```

**Berechtigungen setzen**
```bash
sudo chown -R USER:USER ~/homelab/services/pihole/data/
```

**Daten wiederherstellen**
```bash
rsync -av --no-group --no-times /mnt/backup/DATUM/pihole-data/ \
~/homelab/services/pihole/data/
```

**Service starten**
```bash
docker compose up -d
```

Verifikation:
- Webinterface erreichbar
- DNS-Auflösung funktioniert
- Blocklisten vorhanden


## 9. Update & Maintenance
```bash
docker compose pull  
docker compose down  
docker compose up -d
```
**Nach dem Update prüfen:** 
- Container läuft: `docker ps`
- Web UI erreichbar: `http://192.168.2.x:8080/admin` 
-  DNS funktioniert: `dig @192.168.2.x google.com` 

**Hinweis:**
Updates dürfen nur nach erfolgreichem Health Check durchgeführt werden.

## 10. Failure Scenarios
### 10.1 Passwort funktioniert nicht (Pi-hole Login)
**Symptom**

-   Login im Web UI schlägt fehl
-   Passwort wird als falsch abgelehnt

**Check**
```Bash
docker logs pihole
docker exec pihole pihole status
```
### Ursache (häufig)

-   falsches `.env` Passwort
-   Passwort wurde nach Initial Start geändert
-   Cache / Browser Session Problem

**Fix**
```Bash
docker exec pihole pihole setpassword NEUESPASSWORT
```
Danach:

-   Browser Cache löschen
-   neu einloggen

**Verify**

-   Web UI erreichbar
-   Login funktioniert

### 10.2 Container startet nicht
**Symptom**

-   `docker ps` zeigt Container nicht als „Up“
-   Container startet und stoppt sofort

**Check 1: Status**
```Bash
docker ps  -a
```
**Check 2: Logs**
```Bash
docker logs pihole
```
### Häufige Ursachen

-   Port bereits belegt (53 / 80)
-   falsche Volume Permissions
-   fehlerhafte `.env`
-   kaputte docker-compose.yml

**Fix 1: Ports prüfen**
```Bash
sudo ss -tlnp |  grep :53 
sudo ss -tlnp |  grep :80
```

**Fix 2: Neustart**
```Bash
docker compose down  
docker compose up -d
```
**Fix 3: Image neu ziehen**
```Bash
docker compose pull  
docker compose up -d
```
**Verify**
```Bash
docker ps
```
-   Container ist „Up“
-   keine Restart-Loops

