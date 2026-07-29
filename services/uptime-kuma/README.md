# Service Runbook: Uptime Kuma

| Metadatum | Wert |
|---|---|
| Dokumentstatus | `AKTIV` |
| Service-Status | Produktiv |
| Service-Typ | Monitoring |
| Verantwortlich | `TODO` |
| Letzte technische Prüfung | `TODO – nach vollständiger Prüfung setzen` |
| Runbook-Version | `1.0` |

---

## 0. Systemübersicht

| Eigenschaft | Wert |
|---|---|
| Host | Raspberry Pi 5 |
| Host-IP | `192.168.2.x` |
| Compose-Service | `uptime-kuma` |
| Service-Pfad | `~/homelab/services/uptime-kuma/` |
| Weboberfläche | `http://192.168.2.x:3001` |
| Web-Host-Port | `3001/TCP` |
| Web-Container-Port | `3001/TCP` |
| Persistente Daten | `~/homelab/services/uptime-kuma/data/` |
| Backup-Ziel | `/mnt/backup/DATUM/uptime-kuma-data/` |
| DNS-Server des Containers | `9.9.9.9` |
| Restart Policy | `unless-stopped` |

---

## 1. Service-Übersicht

### 1.1 Zweck

Uptime Kuma ist ein selbstgehostetes Monitoring-System zur Überwachung von Diensten, Webseiten und Netzwerkzielen. Der Service prüft definierte Endpunkte in regelmäßigen Intervallen und benachrichtigt bei Ausfällen oder Zustandsänderungen.

### 1.2 Ziele

- Überwachung kritischer Homelab-Dienste
- Früherkennung von Ausfällen
- Zentrale Statusübersicht aller Services
- Benachrichtigungen bei Störungen
- Historische Verfügbarkeitsdaten (Uptime)

### 1.3 Überwachte Dienste

| Dienst | Zweck |
|---|---|
| Pi-hole | DNS-Erreichbarkeit |
| Nginx Proxy Manager | Reverse Proxy |
| Raspberry Pi | Host-Verfügbarkeit |
| Internet / WAN | Externe Erreichbarkeit |
| Wiki.js | Dokumentation |
| Vaultwarden | Passwortmanager |
| Syncthing | Datei-Synchronisation |

---

## 2. Architektur

### 2.1 Architekturübersicht

Uptime Kuma überwacht die Verfügbarkeit interner und externer Dienste und stellt die Ergebnisse über ein zentrales Dashboard bereit.

Uptime Kuma überwacht:

- Pi-hole (DNS Health Check)
- Nginx Proxy Manager (HTTP Check)
- Wiki.js (HTTP Check)
- externe Dienste (Internet Reachability)
- Vaultwarden (HTTP Check)
- Syncthing (HTTP Check)

---

## 3. Netzwerk und Ports

### 3.1 Portübersicht

| Host-Port | Container-Port | Protokoll | Zweck |
|---:|---:|---|---|
| 3001 | 3001 | TCP | Weboberfläche |

---

## 4. Deployment

### 4.1 Deployment-Prinzip

Der Uptime-Kuma-Service wird aus dem Git-Repository bereitgestellt.

Die Docker-Compose-Datei und die grundlegende Container-Konfiguration werden im Git-Repository versioniert. Operative Uptime-Kuma-Daten werden persistent unter `data/` gespeichert und sind nicht Bestandteil der versionierten Deployment-Konfiguration.

### 4.2 Voraussetzungen

- Raspberry Pi ist über SSH erreichbar
- Docker und Docker Compose sind installiert
- Netzwerk ist eingerichtet; eine statische IP-Adresse über DHCP-Reservierung wird empfohlen
- GitHub-SSH-Key ist eingerichtet

### 4.3 Verzeichnisstruktur

```text
homelab/
└── services/
    └── uptime-kuma/
        ├── docker-compose.yml
        ├── README.md
        └── data/
```

### 4.4 Repository klonen

```bash
cd ~
git clone git@github.com:DEIN-USERNAME/homelab.git
cd ~/homelab/services/uptime-kuma
```

### 4.5 Docker-Compose-Konfiguration

```yaml
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

| Teil | Bedeutung |
|---|---|
| `image` | Uptime-Kuma-Docker-Image |
| `ports` | Veröffentlichung der Weboberfläche |
| `volumes` | Persistente Daten |
| `dns` | DNS-Server des Containers |
| `restart` | Neustartverhalten |

### 4.6 Deployment starten

```bash
cd ~/homelab/services/uptime-kuma
docker compose up -d
```

### 4.7 Post-Deploy-Verifikation

Containerstatus prüfen:

```bash
cd ~/homelab/services/uptime-kuma
docker compose ps
```

Logs prüfen:

```bash
cd ~/homelab/services/uptime-kuma
docker compose logs --tail 100 uptime-kuma
```

Weboberfläche prüfen:

```text
http://192.168.2.x:3001
```

### 4.8 Zugriff

Weboberfläche:

```text
http://192.168.2.x:3001
```

Beim ersten Login muss ein Passwort gesetzt werden.

### 4.9 Manueller Fallback

Dieser Abschnitt wird nur verwendet, wenn kein GitOps-Deployment möglich ist. Standardmäßig sollte der Service über Git bereitgestellt werden.

Verzeichnisstruktur erstellen:

```bash
mkdir -p ~/homelab/services/uptime-kuma
cd ~/homelab/services/uptime-kuma
```

Docker-Compose-Datei erstellen:

```bash
nano docker-compose.yml
```

Hier wird die Service-Definition manuell hinterlegt. Die Docker-Compose-Konfiguration unter Abschnitt 4.5 dient als Referenz.

> **Hinweis:** Änderungen an der Container-Konfiguration erfolgen über das Git-Repository. Manuelle Änderungen innerhalb des laufenden Containers sind nicht zulässig und gehen beim nächsten Re-Deployment verloren. Einstellungen aus der Uptime-Kuma-Weboberfläche werden im persistenten Datenordner gespeichert.

---

## 5. Betrieb

Alle Docker-Compose-Befehle werden im Service-Verzeichnis ausgeführt:

```bash
cd ~/homelab/services/uptime-kuma
```

### 5.1 Start

```bash
docker compose up -d
```

### 5.2 Stop

```bash
docker compose down
```

### 5.3 Neustart

```bash
docker compose restart uptime-kuma
```

### 5.4 Status

```bash
docker compose ps
```

### 5.5 Logs

Fortlaufende Logs:

```bash
docker compose logs -f uptime-kuma
```

Letzte 100 Logzeilen:

```bash
docker compose logs --tail 100 uptime-kuma
```

---

## 6. Konfiguration

### 6.1 Zugriff und Ersteinrichtung

Die Weboberfläche ist erreichbar unter:

```text
http://192.168.2.x:3001
```

Beim ersten Login muss ein Passwort gesetzt werden.

### 6.2 DNS-Konfiguration

In der Docker-Compose-Konfiguration ist ein externer DNS-Server für den Container hinterlegt:

```yaml
dns:
  - 9.9.9.9
```

### 6.3 Benachrichtigungen

Notification-Einstellungen werden über die Weboberfläche verwaltet:

```text
Settings → Notifications
```

Eine Notification muss dem betroffenen Monitor zugewiesen werden:

```text
Monitor → Edit → Notifications
```

Nach Änderungen sollte eine Test-Notification ausgeführt werden.

### 6.4 Konfigurationsprinzip

Die Container-Konfiguration wird über `docker-compose.yml` im Git-Repository verwaltet.

Operative Einstellungen, Monitore und Benachrichtigungskonfigurationen werden durch Uptime Kuma im persistenten Datenordner gespeichert:

```text
~/homelab/services/uptime-kuma/data/
```

---

## 7. Health Checks

### 7.1 Containerstatus

```bash
cd ~/homelab/services/uptime-kuma
docker compose ps
```

Erwartung:

```text
Status: Up
```

Falls ein Container-Healthcheck angezeigt wird, zusätzlich:

```text
healthy
```

### 7.2 Weboberfläche

Aufruf:

```text
http://192.168.2.x:3001
```

Erwartung:

- Login-Seite ist erreichbar
- Anmeldung funktioniert
- konfigurierte Monitore werden angezeigt

### 7.3 Logprüfung

```bash
cd ~/homelab/services/uptime-kuma
docker compose logs --tail 100 uptime-kuma
```

Erwartete Startmeldungen:

```text
Welcome to Uptime Kuma
Your Node.js version: x.x.x
(Date)(Time) [SERVER] INFO: Uptime Kuma Version: x.x.x
```

### 7.4 Benachrichtigungsprüfung

- Test-Notification ist erfolgreich
- der betroffene Monitor löst Benachrichtigungen aus

Optional kann ein unkritischer Monitor kurzzeitig auf eine ungültige URL umgestellt oder ein Test-Monitor angelegt werden, um die Alarmierung zu verifizieren.

---

## 8. Backup und Restore

### 8.1 Backup-Strategie

```text
TODO: Backup-Strategie für die persistenten Uptime-Kuma-Daten dokumentieren.
```

### 8.2 Backup erstellen

```text
TODO: Verfahren zum Erstellen eines konsistenten Uptime-Kuma-Backups dokumentieren.
```

### 8.3 Backup-Verifikation

```text
TODO: Verfahren zur Verifikation eines Uptime-Kuma-Backups dokumentieren.
```

### 8.4 Restore

In das Service-Verzeichnis wechseln und den Service stoppen:

```bash
cd ~/homelab/services/uptime-kuma
docker compose down
```

Berechtigungen setzen:

```bash
sudo chown -R USER:USER ~/homelab/services/uptime-kuma/data/
```

Daten wiederherstellen:

```bash
rsync -av --no-group --no-times /mnt/backup/DATUM/uptime-kuma-data/ \
  ~/homelab/services/uptime-kuma/data/
```

Service starten:

```bash
cd ~/homelab/services/uptime-kuma
docker compose up -d
```

### 8.5 Restore-Verifikation

Prüfen:

- Weboberfläche ist erreichbar
- Monitore werden angezeigt
- Benachrichtigungen funktionieren

---

## 9. Update und Wartung

### 9.1 Voraussetzungen

Updates dürfen nur nach einem erfolgreichen Health Check durchgeführt werden.

### 9.2 Update durchführen

```bash
cd ~/homelab/services/uptime-kuma
docker compose pull
docker compose down
docker compose up -d
```

### 9.3 Update-Verifikation

Containerstatus prüfen:

```bash
cd ~/homelab/services/uptime-kuma
docker compose ps
```

Weboberfläche prüfen:

```text
http://192.168.2.x:3001
```

Logs prüfen:

```bash
cd ~/homelab/services/uptime-kuma
docker compose logs --tail 100 uptime-kuma
```

---

## 10. Bekannte Störungen und Troublelogs

### 10.1 Schnellübersicht

| Störung | Erste Prüfung | Troublelog |
|---|---|---|
| Pi-hole-Monitor zeigt HTTP 403 | Monitorstatus und zurückgegebenen HTTP-Status prüfen | [2026-05-27 – Uptime Kuma Pi-hole Monitor zeigt 403](../../troubleshooting/log.md) |
| Discord-Benachrichtigung fehlt | Notification-Zuordnung und Uptime-Kuma-Logs prüfen | [2026-05-28 – Uptime Kuma: Discord-Benachrichtigung fehlt](../../troubleshooting/log.md) |
| Keine Discord-Benachrichtigung wegen DNS-Fehler | DNS-Erreichbarkeit aus dem Container und Logs prüfen | [2026-05-28 – Uptime Kuma: Keine Discord-Benachrichtigung (DNS-Fehler)](../../troubleshooting/log.md) |
| Domainauflösung funktioniert nicht | DNS-Auflösung aus dem Uptime-Kuma-Container prüfen | [2026-06-06 – Fehler Domainauflösung in Uptime Kuma](../../troubleshooting/log.md) |
| `rsync`-Fehler während des Backups | Backup-Log und ausgeführten `rsync`-Befehl prüfen | [2026-06-08 – rsync-Fehler während des Backups](../../troubleshooting/log.md) |

### 10.2 Basisdiagnose

Alle Docker-Compose-Befehle werden im Service-Verzeichnis ausgeführt:

```bash
cd ~/homelab/services/uptime-kuma
```

**Containerstatus prüfen:**

```bash
docker compose ps
```

**Containerlogs prüfen:**

```bash
docker compose logs uptime-kuma
```

**Port 3001 prüfen:**

```bash
sudo ss -tlnp | grep :3001
```

**Lokale Erreichbarkeit der Weboberfläche prüfen:**

```bash
curl http://localhost:3001
```

**DNS-Erreichbarkeit aus dem Container prüfen:**

```bash
docker compose exec uptime-kuma ping -c 4 google.com
```

**Notification-Einstellungen prüfen:**

```text
Settings → Notifications
```

Zusätzlich prüfen, ob die Notification dem betroffenen Monitor zugewiesen ist:

```text
Monitor → Edit → Notifications
```

Ausführliche Ursachen, Maßnahmen und Lessons Learned sind im zentralen Troublelog dokumentiert.

---

## 11. Verweise

### 11.1 Interne Dokumentation

- [`docker-compose.yml`](docker-compose.yml)
- [Zentrales Störungs- und Troublelog](../../troubleshooting/log.md)
- [Backup- und Restore-Runbook](../../runbooks/backup-restore.md)
- [Netzwerkübersicht](../../infrastructure/network/network-overview.md)
- [DNS-Dokumentation](../../infrastructure/network/dns.md)

### 11.2 Troublelogs

Die folgenden Uptime-Kuma-Störungen sind im zentralen Troublelog dokumentiert:

- [Zentrales Störungs- und Troublelog](../../troubleshooting/log.md)

### 11.3 Externe Dokumentation

TODO: Offizielle Uptime-Kuma-Dokumentation verlinken.

TODO: Offizielle Dokumentation des Uptime-Kuma-Docker-Images verlinken.


---

## 12. Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 2026-07-28 | Runbook in die einheitliche Referenzstruktur überführt |
