


# Service Runbook: Uptime Kuma (self-hosted monitoring tool)

## 0. System Übersicht
| Eigenschaft | Wert | 
|-------------|------| 
| Host | Raspberry Pi 5 | 
| IP | 192.168.2.x | 
| Port Web UI | 3001 |  
| Daten |  `~/homelab/services/uptime-kuma/data/` | 
| Backup |  `/mnt/backup/DATUM/uptime-kuma-data/` 

## 1. Service Overview

Uptime Kuma ist ein selbstgehostetes Monitoring-System zur Überwachung von Diensten, Webseiten und Netzwerkzielen. Der Service prüft definierte Endpunkte in regelmäßigen Intervallen und benachrichtigt bei Ausfällen oder Zustandsänderungen.

### 1.1 Ziele des Services

- Überwachung kritischer Homelab-Dienste  
- Früherkennung von Ausfällen  
- Zentrale Statusübersicht aller Services  
- Benachrichtigungen bei Störungen  
- Historische Verfügbarkeitsdaten (Uptime)

### 1.2 Überwachte Dienste
| Dienst | Zweck |  
|----------|----------|  
| Pi-hole | DNS-Erreichbarkeit |  
| Nginx Proxy Manager | Reverse Proxy |  
| Raspberry Pi | Host-Verfügbarkeit |  
| Internet / WAN | Externe Erreichbarkeit |
| Wiki.JS | Dokumentation |
| vaultwarden | passwort manager |

## 2. Architektur
**Zweck**
Uptime Kuma überwacht die Verfügbarkeit interner und externer Dienste und stellt die Ergebnisse über ein zentrales Dashboard bereit.

Uptime Kuma überwacht:

- Pi-hole (DNS Health Check)
- Nginx Proxy Manager (HTTP Check)
- Wiki.JS (HTTP Check)
- externe Dienste (Internet Reachability


## 3. Netzwerk & Ports


| Port | Protokoll | Zweck |
| ---         |     ---    |          --- |
| 3001   | HTTP       | Web Interface      |


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
		└── uptime-kuma/  
				├── docker-compose.yml  
				├── README.md  
				└── data/
```
### 4.3 Repository klonen
```Bash
mkdir  -p ~/homelab/services  
cd ~/homelab/services  
  
git clone git@github.com:DEIN-USERNAME/homelab.git  
cd homelab/services/uptime-kuma
```

### 4.4 Container Stack (Docker Compose)
```YAML
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    restart: unless-stopped
    volumes:
      - ./data:/app/data
    ports:
      # <Host Port>:<Container Port>
      - "3001:3001"
    dns: 
      - 9.9.9.9
```
**Erklärung**
| Teil | Bedeutung | 
| ---         |     ---    |  
| image   | Uptime Kuma Docker Image   | 
| ports    | DNS + Web UI       | 
| volumes     | persistente Daten      | 
| restart   | Autostart Verhalten    | 

### 4.5 Deployment starten 
```Bash
docker compose up -d
```
### 4.6 Verifikation (Post-Deploy Check)
**Container Status**
```Bash
docker ps
```
**Logs Prüfen**
```Bash
docker logs uptime-kuma-uptime-kuma-1
```
**Web Ui Prüfen**
```Bash
http://192.168.2.x:3001
```
### 4.7 Zugriff
-   Web UI:  
    `http://192.168.2.x:3001`
-   Login:  
    Passwort beim ersten Login setzen

### 4.8 Manuelle Einrichtung (Fallback / kein Git verfügbar)
Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist.  
Standardmäßig sollte der Service über Git bereitgestellt werden.
#### 4.8.1. Verzeichnisstruktur erstellen
```Bash
mkdir  -p ~/homelab/services/uptime-kuma
cd ~/homelab/services/uptime-kuma
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
docker compose restart uptime-kuma-uptime-kuma-1
```
**Logs:**
```Bash
docker logs -f uptime-kuma-uptime-kuma-1
```
**Status:**
```Bash
docker ps
```

## 6. Health Checks

**Container Health**
```bash
docker ps
```
Erwartung: Status `Up` und `(healthy)`

**Web UI**
http://192.168.2.x:3001
Erwartung: Login-Seite erreichbar


**Uptime Kuma Status**
```bash
docker logs uptime-kuma-uptime-kuma-1
```
Erwartung:
```
Welcome to Uptime Kuma
Your Node.js version: x.x.x
(Date)(Time) [SERVER] INFO: Uptime Kuma Version: x.x.x
```
## 7. Backup & Restore

**Uptime Kuma Service stoppen**
```bash
cd ~/homelab/services/uptime-kuma
docker compose down
```

**Berechtigungen setzen**
```bash
sudo chown -R USER:USER ~/homelab/services/uptime-kuma/data/
```

**Daten wiederherstellen**
```bash
rsync -av --no-group --no-times /mnt/backup/DATUM/uptime-kuma-data/ \
~/homelab/services/uptime-kuma/data/
```

**Service starten**
```bash
docker compose up -d
```

Verifikation:
- Webinterface erreichbar 
- Monitore werden angezeigt 
- Benachrichtigungen funktionieren


## 8. Update & Maintenance
```bash
docker compose pull  
docker compose down  
docker compose up -d
```
**Nach dem Update prüfen:** 
- Container läuft: `docker ps`
- Web UI erreichbar: `http://192.168.2.x:3001` 
-  Docker logs: `docker logs uptime-kuma-uptime-kuma-1` 

**Hinweis:**
Updates dürfen nur nach erfolgreichem Health Check durchgeführt werden.

## 9. Failure Scenarios
### 9.1 Container startet nicht
**Symptom**
-   Web UI nicht erreichbar
-   `docker ps` zeigt keinen laufenden Container

**Check**
```bash
docker ps  -a
docker logs uptime-kuma-uptime-kuma-1
```
**Häufige Ursachen**
-   Port 3001 bereits belegt
-   Fehlerhafte Volume-Mounts
-   Beschädigte Datenbank

**Fix 1: Port Prüfen:**
```bash
sudo ss -tlnp |  grep :3001
```
**Fix 2: Container neu starten:**
```bash
docker compose down
docker compose up -d
```

**Verify**
```bash
docker ps
```
Erwartung: `Up x (healthy)`

### 9.2 Web UI nicht erreichbar
**Symptom**
Browser kann Uptime Kuma nicht öffnen.

**Check**
Prüfen ob Container läuft
```bash
docker ps
```
Ist der Port erreichbar
```bash
curl http://localhost:3001
```
**Häufige Ursachen**

-   Container läuft nicht
-   Firewall blockiert
-   Falsche IP-Adresse verwendet

**Fix: Container neu starten:**
```bash
docker compose restart uptime-kuma-uptime-kuma-1
```

**Verify**
Web UI erreichbar:
```bash
http://192.168.2.x:3001
```

### 9.3 Benachrichtigungen werden nicht versendet

**Symptom**
Monitore schlagen fehl, aber keine Nachricht wird versendet.

**Check**
Notification-Einstellungen prüfen(Web Ui):
```
Settings → Notifications
```
Logs prüfen:
```bash
docker logs uptime-kuma-uptime-kuma-1
```
**Häufige Ursachen**

-   Falscher API-Key
-   Falscher Webhook
-   SMTP-Konfiguration fehlerhaft
-   Notification wurde keinem Monitor zugewiesen
-   DNS-Auflösung aus dem Container funktioniert nicht

**Fix 1: Notification nicht zugewiesen:**
Prüfen, ob die Notification dem betroffenen Monitor zugeordnet wurde:

`Monitor → Edit → Notifications`

Notification aktivieren und speichern.

**Fix 2: DNS-Probleme**
Testen, ob der Container externe Ziele erreichen kann:
```bash
docker exec -it uptime-kuma-uptime-kuma-1 ping -c 4 google.com
```
Falls die DNS-Auflösung fehlschlägt, einen externen DNS-Server in der `docker-compose.yml` hinterlegen:

dns: 
- 9.9.9.9

Container anschließend neu starten:
```bash
docker compose up -d
```


**Verifiy**
- Test Notification erfolgreich
- Betroffener Monitor löst Benachrichtigungen aus

**Optionaler Funktionstest**
Einen unkritischen Monitor kurzzeitig auf eine ungültige URL umstellen oder einen Test-Monitor anlegen, um die Alarmierung zu verifizieren.
