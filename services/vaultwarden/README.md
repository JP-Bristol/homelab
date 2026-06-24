# Service Runbook: Vaultwarden

## 0. System Übersicht
| Eigenschaft | Wert |
| - | - |
| Host | Raspberry Pi 5 |
| IP | 192.168.2.x |
| Port Web UI | 11001 |
| Zugriff | https://vaultwarden.home |
| Daten | ~/homelab/services/vaultwarden/data/ |
| Backup | /mnt/backup/DATUM/vaultwarden-data/ |

## 1. Service Overview
Vaultwarden ist eine leichtgewichtige, selbstgehostete Alternative zu Bitwarden und dient als zentraler Passwort-Manager für Benutzerkonten, Zugangsdaten, sichere Notizen und weitere sensible Informationen.

### 1.1 Ziele des Services
- Zentrale Passwortverwaltung
- Synchonisation zwischen Geräten
- Unabhängikeit von Cloud-Anbietern
- Lokaler Betrieb im Homelab
- Backup der Passwortdatenbank

### 1.2 Besonderheiten
Vaultwarden erfordert eine HTTPS-Verbindung für die Nutzung mit Bitwarden-Clients.
Da keine öffentliche Domain vorhanden ist, wird ein selbstsigniertes TLS-Zertifikat verwendet, welches über Nginx Proxy Manager bereitgestellt wird.

## 2. Architektur
Zweck 
Bereitstellung eines sicheren Passwort-Managers innerhalb des Heimnetzwerks.

### 2.1 Architekturübersicht
``` Bitwarden Client 
│ 
▼ 
Nginx Proxy Manager (HTTPS) 
│ 
▼ Vaultwarden Container (HTTP intern) 
│ 
▼ db.sqlite3 (Daten) ```
```
### 2.2 Besonderheit: TLS ohne öffentliche Domain

Erstellung des selbstsignierten Zertifikats:
```Bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \ -keyout vaultwarden.key \ -out vaultwarden.crt \ -subj "/CN=vaultwarden.home"
```
Das Zertifikat wird anschließend als "Custom Certificate" im Nginx Proxy Manager hinterlegt und dem Proxy Host `vaultwarden.home` zugewiesen.

**Zugriff:**
```
https://vaultwarden.home
```
**Hinweis:**
Da das Zertifikat selbstsigniert ist, wird beim ersten Zugriff eine Zertifikatswarnung angezeigt.

Die Warnung muss einmalig bestätigt werden.

Ein öffentlich vertrauenswürdiges Zertifikat ist ohne öffentliche Domain und DNS-Nachweis nicht möglich.

## 3 Netzwerk & Ports

| Port | Protokoll | Zweck |
| - | - | - |
| 11001 | HTTP | Vaultwarden Webinferface (intern)|
| 443 | HTTPS | Zugriff über Nginx Proxy Manager|
| 81 | HTTP | NPM Management | 

## 4 Deployment (GitOps – Primary Path)
### 4.1 Voraussetzung
- Raspberry Pi erreichbar
- Docker & Docker Compise installiert
- GitHub SSH Key eingerichtet
- Homelab Repositiory vorhanden
- TLS-Zertifikat vorhanden

### 4.2 Initial Setup / Erstinstallation
Bei der Erstinstallation ist die Registrierung temporär aktiviert, damit der erste Benutzer angelegt werden kann.

#### 4.2.1 Container starten
Vaultwarten starten: 
```Bash
cd ~/homelab/services/vaultwarden 
docker compose up -d
```
Web UI öffnen:
```
https://vaultwarden.home
```
#### 4.2.2 Administrator Account erstellen
Den ersten Benutzer über die Registrierung anlegen.
Nach erfolgreicher Erstellung muss die öffentliche Registrierung deaktiviert werden.

#### 4.2.3 Registrierung deaktivieren
In der `docker-compose.yml` setzen:
```
environment: 
		SIGNUPS_ALLOWED: "false"
```
Anschließend Container neu starten:
```Bash 
docker compose down docker compose up -d
```
#### 4.4.4 Verifikation  
  
Prüfen, ob die Einstellung aktiv ist:  
  
```bash  
docker inspect vaultwarden-vaultwarden-1 | grep SIGNUPS_ALLOWED
```

Erwartung:
```bash  
SIGNUPS_ALLOWED=false
```
Zusätzlich testen:

-   Login mit vorhandenem Benutzer funktioniert
-   Neue Registrierung ist deaktiviert



### 4.3 Deployment starten
```Bash
cd ~/homelab/services/vaultwarden 
docker compose up -d
```
### 4.4 Verifikation 
Container prüfen:
```Bash
docker ps
```
Logs prüfen:
```Bash
docker logs vaultwarden
```
Webzugriff prüfen:
```
https://vaultwarden.home
```

## 5 Health Checks
### 5.1 Container Status
```Bash
docker ps
```
Erwartung:
```
Up (healthy)
```

### 5.2 Web UI
Erwartung:
```
Login-Seite erreichbar.
```
### 5.3 Datenbank
Logs prüfen:
```
docker logs vaultwarden-vaultwarden-1 --tail 50
```
Erwartung:
Keine Datenbankfehler

## 6. Backup & Restore
### 6.1 Besonderheit bei Vaultwarden Backups
Vaultwarden wird beim Backup anders behandelt als normale Services.
Grund:
Vaultwarden enthält sensible Passwortdaten und eine kritische Datenbank.
Daher:
- Service vor dem Backup stoppen  
- SQLite-Datenbank konsistent sichern  
- Restore immer funktional prüfen  
- Login und Synchronisation testen

Ein erfolgreich kopiertes Backup garantiert nicht automatisch ein funktionierendes Restore.

### 6.2 Backup
```Bash
cd ~/homelab/services/vaultwarden docker compose down
```
### 6.3 Backup der Daten:
```Bash
rsync -av \ ~/homelab/services/vaultwarden/data/ \ /mnt/backup/DATUM/vaultwarden-data/
```
### 6.4 Restore
Service stoppen:
```Bash
docker compose down
```
Berechtigungen prüfen:
```Bash
sudo chown -R USER:USER ~/homelab/services/vaultwarden/data/
```
Daten wiederherstellen:
```Bash
rsync -av --no-group --no-times \ /mnt/backup/DATUM/vaultwarden-data/ \ ~/homelab/services/vaultwarden/data/
docker compose up -d
```

Service starten:
```Bash
docker compose up -d
```

#### 6.5 Restore Verifikation
Nach einem Restore muss die Funktion geprüft werden.

Checkliste:

-   Container läuft:

```
docker compose ps
```

-   Web UI erreichbar:

```
https://vaultwarden.home
```

-   Login mit bestehendem Account funktioniert
-   Tresore sind vorhanden
-   Bitwarden Client synchronisiert erfolgreich
-   Anhänge können geöffnet werden

**Hinweis**

Ein erfolgreich kopiertes Backup bedeutet nicht automatisch ein funktionierendes Vaultwarden-Backup.

Ein Restore-Test sollte regelmäßig durchgeführt werden.

Verifikation:
- Login funktioniert
- Tresore vorhanden
- Synchronisation funktioniert

### 7. Update & Maintenance
```Bash
docker compose pull 
docker compose down 
docker compose up -d
```
Nach dem Update prüfen:
- Login möglich
- Synchronisation funktioniert
- Container läuft

## 8. Failure Scenarios
### 8.1 Container startet nicht
#### 8.1.1 Symptom
-   Web UI nicht erreichbar
-   `docker ps` zeigt keinen laufenden Container

#### 8.1.2 Check
```Bash
docker ps  -a
docker logs vaultwarden
```

#### 8.1.3 Häufige Ursachen
-   Port 11001 bereits belegt
-   Fehlerhafte Volume-Mounts
-   Beschädigte Datenbank

####  8.1.4 **Fix 1: Port Prüfen:**
```Bash
sudo ss -tlnp |  grep :11001
```
#### 8.1.5 **Fix 2: Container neu starten:**
```Bash
docker compose down
docker compose up -d
```
#### 8.1.6 **Verify**
Prüfen ob Container läuft:
```Bash
docker ps
```
Erwartung: `Up x (healthy)`

### 8.2 HTTPS funktioniert nicht
#### 8.2.1 Symptom
Browser meldet Zertifikatsfehler oder Verbindung nicht sicher.

**Check**
Nginx Proxy Manager prüfen:

-   Proxy Host vorhanden
-   SSL Certificate zugewiesen

#### 8.2.2 Ursachen
-   Zertifikat fehlt
-   Zertifikat abgelaufen
-   Falscher Hostname

#### 8.2.3 Fix
Neues Zertifikat erzeugen:

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout vaultwarden.key \
  -out vaultwarden.crt \
  -subj "/CN=vaultwarden.home"
```
Im Nginx Proxy Manager neu importieren.

**Hinweis:** 
Zertifikat und Key nach `data/` verschieben: 
```Bash
mv vaultwarden.key vaultwarden.crt ~/homelab/services/vaultwarden/data/
```
So werden sie nicht versehentlich ins Git-Repo aufgenomm


### 8.3 Bitwarden Client kann nicht synchronisieren

#### 8.3.1 Symptom 
Bitwarden App zeigt Verbindungsfehler oder "Cannot connect to server". 
#### 8.3.2 Ursachen 
- Falsche Server-URL im Client eingetragen 
- HTTPS nicht aktiv - Zertifikat nicht akzeptiert 
#### 8.3.3 Fix
- Server-URL im Bitwarden Client korrekt setzen:
```Bash
https://vaultwarden.home
```
#### 8.3.4 Verify 
- Login im Client funktioniert - Tresore werden synchronisiert
