# Service Runbook: Nginx Proxy Manager

| Metadatum | Wert |
|---|---|
| Dokumentstatus | `AKTIV` |
| Service-Status | Produktiv |
| Service-Typ | Reverse Proxy |
| Verantwortlich | `TODO` |
| Letzte technische Prüfung | `TODO – nach vollständiger Prüfung setzen` |
| Runbook-Version | `1.0` |

---

## 0. Systemübersicht

| Eigenschaft | Wert |
|---|---|
| Host | Raspberry Pi 5 |
| Host-IP | `192.168.2.x` |
| Compose-Service | `app` |
| Service-Pfad | `~/homelab/services/nginx-proxy-manager/` |
| Regulärer Zugriff | `npm.home` |
| Direkter Diagnosezugriff | `http://192.168.2.x:81` |
| HTTP-Port | `80/TCP` |
| HTTPS-Port | `443/TCP` |
| Administrationsport | `81/TCP` |
| Persistente Daten | `~/homelab/services/nginx-proxy-manager/data/` |
| Zertifikatsordner | `~/homelab/services/nginx-proxy-manager/letsencrypt/` |
| Backup-Ziel | `/mnt/backup/DATUM/npm-data/` |
| Restart Policy | `unless-stopped` |

---

## 1. Service-Übersicht

### 1.1 Zweck

Nginx Proxy Manager (NPM) ist ein Reverse Proxy mit Weboberfläche zur zentralen Verwaltung interner Webdienste.

Der Service leitet Anfragen an die entsprechenden Backend-Dienste weiter und ermöglicht die Verwaltung von Domains, TLS-Zertifikaten und Zugriffskontrollen.

Nginx Proxy Manager wird ausschließlich innerhalb des lokalen Netzwerks verwendet.

### 1.2 Ziele

- Zentraler Zugriffspunkt für Webanwendungen im Homelab
- Vereinfachte Verwaltung von Reverse Proxies
- Einheitliche Hostnamen für interne Dienste
- TLS-Zertifikatsverwaltung
- Trennung von Backend-Diensten und Benutzerzugriffen
- Zentralisierte Verwaltung der Weiterleitungsziele

### 1.3 Eingerichtete Proxy Hosts

| Domain | Zielsystem | Zielport |
|---|---|---:|
| `pihole.home` | `192.168.2.x` | 8080 |
| `uptime.home` | `192.168.2.x` | 3001 |
| `npm.home` | `192.168.2.x` | 81 |
| `wiki.home` | `192.168.2.x` | 3000 |
| `vaultwarden.home` | `192.168.2.x` | 11001 |
| `syncthing.home` | `192.168.2.x` | 8384 |

---

## 2. Architektur

### 2.1 Architekturübersicht

```text
Clients im lokalen Netzwerk
             │
             │ interner Hostname
             ▼
           Pi-hole
             │
             │ lokale DNS-Auflösung
             ▼
   Nginx Proxy Manager
        │      │      │
        ▼      ▼      ▼
     Pi-hole  Uptime  weitere Backend-Services
```

Nginx Proxy Manager dient als zentrale Zugriffsschicht für interne Webdienste.

Pi-hole löst die lokalen Hostnamen auf die IP-Adresse des Reverse-Proxy-Hosts auf. Nginx Proxy Manager wertet den Hostnamen der HTTP- oder HTTPS-Anfrage aus und leitet sie an das konfigurierte Backend weiter.

### 2.2 Komponenten und Abhängigkeiten

| Komponente | Aufgabe |
|---|---|
| Raspberry Pi 5 | Docker-Host |
| Docker | Container-Laufzeit |
| Docker Compose | Deployment und Container-Konfiguration |
| Nginx Proxy Manager | Reverse Proxy und Verwaltung der Proxy Hosts |
| Pi-hole | Lokale DNS-Auflösung der internen Hostnamen |
| Backend-Services | Bereitstellung der internen Webanwendungen |
| Persistenter Datenordner `data/` | Datenbank, Proxy-Konfigurationen und benutzerdefinierte Zertifikate |
| Persistenter Ordner `letsencrypt/` | Separat eingebundene ACME- und Zertifikatsdaten |
| Git-Repository | Versionierung der Deployment-Konfiguration |

### 2.3 Datenfluss

1. Ein Client ruft einen internen Hostnamen auf, beispielsweise `uptime.home`.
2. Pi-hole löst den Hostnamen auf die IP-Adresse des Reverse-Proxy-Hosts auf.
3. Nginx Proxy Manager empfängt die HTTP- oder HTTPS-Anfrage.
4. Nginx Proxy Manager wählt anhand des Hostnamens den konfigurierten Proxy Host aus.
5. Die Anfrage wird an den jeweiligen Backend-Service weitergeleitet.
6. Die Antwort des Backend-Services wird an den Client zurückgegeben.

---

## 3. Netzwerk und Ports

### 3.1 Portübersicht

| Host-Port | Container-Port | Protokoll | Zweck |
|---:|---:|---|---|
| 80 | 80 | TCP | Interne HTTP-Anfragen an Proxy Hosts |
| 443 | 443 | TCP | Interne HTTPS-Anfragen an Proxy Hosts |
| 81 | 81 | TCP | Interne Administrationsoberfläche |

### 3.2 Netzwerkzugriff

Nginx Proxy Manager ist ausschließlich aus dem lokalen Netzwerk erreichbar.

An der EasyBox bestehen keine Portweiterleitungen für Port `80` oder `443`. Der Reverse Proxy ist daher nicht direkt aus dem Internet erreichbar.

Der reguläre Zugriff auf die Administrationsoberfläche erfolgt über:

```text
npm.home
```

Für Diagnosezwecke ist zusätzlich der direkte Zugriff möglich:

```text
http://192.168.2.x:81
```

### 3.3 Lokale DNS-Auflösung

Die internen Hostnamen werden in Pi-hole als Local DNS Records verwaltet.

Beispiele:

- `pihole.home`
- `uptime.home`
- `npm.home`
- `wiki.home`
- `vaultwarden.home`
- `syncthing.home`

Weitere Informationen:

```text
infrastructure/network/dns.md
```

---

## 4. Deployment

### 4.1 Deployment-Prinzip

Die Docker-Compose-Datei und die grundlegende Container-Konfiguration werden im Git-Repository versioniert.

Das Git-Repository ist die Quelle der Wahrheit für:

- Containerdefinition
- Portfreigaben
- Volume-Mounts
- Umgebungsvariablen
- Deployment-Ablauf

Operative Nginx-Proxy-Manager-Daten werden persistent unter `data/` und `letsencrypt/` gespeichert. Einstellungen aus der Weboberfläche sind daher nicht vollständig Bestandteil der versionierten Deployment-Konfiguration.

### 4.2 Voraussetzungen

- Raspberry Pi ist über SSH erreichbar
- Docker ist installiert
- Docker Compose ist installiert
- Homelab-Git-Repository ist vorhanden
- Host besitzt eine feste IP-Adresse oder DHCP-Reservierung
- Ports `80/TCP`, `443/TCP` und `81/TCP` sind frei
- Pi-hole ist für die lokale DNS-Auflösung erreichbar
- benötigte Local DNS Records sind vorhanden

### 4.3 Verzeichnisstruktur

```text
~/homelab/services/nginx-proxy-manager/
├── docker-compose.yml
├── README.md
├── data/
└── letsencrypt/
```

| Pfad | Zweck |
|---|---|
| `docker-compose.yml` | Definition des Nginx-Proxy-Manager-Containers |
| `data/` | Datenbank, Proxy-Konfigurationen, Schlüssel und benutzerdefinierte Zertifikate |
| `letsencrypt/` | Separat eingebundene ACME- und Zertifikatsdaten |

### 4.4 Repository klonen

Falls das Repository noch nicht vorhanden ist:

```bash
cd ~
git clone git@github.com:DEIN-USERNAME/homelab.git
cd ~/homelab/services/nginx-proxy-manager
```

### 4.5 Docker-Compose-Konfiguration

```yaml
services:
  app:
    image: jc21/nginx-proxy-manager:latest
    restart: unless-stopped

    ports:
      - "80:80"
      - "443:443"
      - "81:81"

    environment:
      TZ: "Europe/Berlin"

    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```

| Teil | Bedeutung |
|---|---|
| `image` | Nginx-Proxy-Manager-Docker-Image |
| `ports` | Veröffentlichung der internen HTTP-, HTTPS- und Administrationsports |
| `environment` | Zeitzone des Containers |
| `volumes` | Persistente Daten und Zertifikatsdaten |
| `restart` | Neustartverhalten |

### 4.6 Compose-Konfiguration prüfen

Vor dem Deployment:

```bash
cd ~/homelab/services/nginx-proxy-manager
docker compose config
```

Erwartung:

- keine YAML-Fehler
- Volume-Pfade sind korrekt
- Ports sind korrekt definiert
- Compose-Service `app` wird erkannt

### 4.7 Deployment starten

```bash
cd ~/homelab/services/nginx-proxy-manager
docker compose up -d
```

Containerstatus prüfen:

```bash
docker compose ps
```

Logs prüfen:

```bash
docker compose logs --tail 100 app
```

### 4.8 Post-Deploy-Verifikation

Administrationsoberfläche direkt prüfen:

```text
http://192.168.2.x:81
```

Administrationsoberfläche über den lokalen Hostnamen prüfen:

```text
npm.home
```

Mindestens einen Proxy Host prüfen:

```text
uptime.home
```

Erwartung:

- Container läuft
- Administrationsoberfläche ist erreichbar
- Anmeldung funktioniert
- lokale Hostnamen werden aufgelöst
- Proxy Hosts leiten Anfragen an die vorgesehenen Backend-Services weiter

### 4.9 Manueller Fallback

Der manuelle Fallback wird nur verwendet, wenn das Git-Repository nicht verfügbar ist.

Verzeichnis erstellen:

```bash
mkdir -p ~/homelab/services/nginx-proxy-manager
cd ~/homelab/services/nginx-proxy-manager
```

Docker-Compose-Datei anlegen:

```bash
nano docker-compose.yml
```

Konfiguration prüfen und Service starten:

```bash
docker compose config
docker compose up -d
```

Die manuell erstellte Datei muss später mit dem Git-Repository abgeglichen werden.

> **Hinweis:** Änderungen an der Container-Konfiguration erfolgen über das Git-Repository. Manuelle Änderungen innerhalb des laufenden Containers sind nicht zulässig und gehen beim nächsten Re-Deployment verloren. Einstellungen aus der Nginx-Proxy-Manager-Weboberfläche werden in den persistenten Datenordnern gespeichert.

---

## 5. Betrieb

Alle Docker-Compose-Befehle werden im Service-Verzeichnis ausgeführt:

```bash
cd ~/homelab/services/nginx-proxy-manager
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
docker compose restart app
```

### 5.4 Status

```bash
docker compose ps
```

### 5.5 Logs

Fortlaufende Logs:

```bash
docker compose logs -f app
```

Letzte 100 Logzeilen:

```bash
docker compose logs --tail 100 app
```

### 5.6 Container-Shell

```bash
docker compose exec app sh
```

---

## 6. Konfiguration

### 6.1 Zugriff und Ersteinrichtung

Die Administrationsoberfläche ist erreichbar unter:

```text
npm.home
```

Für Diagnosezwecke:

```text
http://192.168.2.x:81
```

Beim ersten Login muss das Administrationspasswort gesetzt beziehungsweise geändert werden.

Zugangsdaten dürfen nicht im Runbook oder im Git-Repository gespeichert werden.

### 6.2 Proxy Hosts

Proxy Hosts werden über die Nginx-Proxy-Manager-Weboberfläche verwaltet:

```text
Hosts
→ Proxy Hosts
```

Für einen Proxy Host sind mindestens zu prüfen:

- Domain Names
- Scheme
- Forward Hostname / IP
- Forward Port
- Zugriffseinstellungen
- TLS-Zertifikat, falls HTTPS verwendet wird

Der Pfad einer Anwendung gehört nur dann in die Proxy-Konfiguration, wenn der Backend-Service dies ausdrücklich erfordert.

Beispiel Pi-hole:

```text
Domain Name: pihole.home
Forward Hostname / IP: 192.168.2.x
Forward Port: 8080
```

Der Pfad `/admin` gehört nicht in den Forward Host oder Forward Port.

### 6.3 Eingerichtete Proxy Hosts

| Domain | Forward Host | Forward Port |
|---|---|---:|
| `pihole.home` | `192.168.2.x` | 8080 |
| `uptime.home` | `192.168.2.x` | 3001 |
| `npm.home` | `192.168.2.x` | 81 |
| `wiki.home` | `192.168.2.x` | 3000 |
| `vaultwarden.home` | `192.168.2.x` | 11001 |
| `syncthing.home` | `192.168.2.x` | 8384 |

### 6.4 Selbstsigniertes TLS-Zertifikat für Vaultwarden

Für den internen Proxy Host `vaultwarden.home` wird ein selbstsigniertes TLS-Zertifikat verwendet.

Das Zertifikat besitzt:

```text
Common Name: vaultwarden.home
Subject Alternative Name: DNS:vaultwarden.home
Gültigkeit: 365 Tage
```

Ein reproduzierbarer OpenSSL-Aufruf lautet:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout vaultwarden.key \
  -out vaultwarden.crt \
  -subj "/CN=vaultwarden.home" \
  -addext "subjectAltName=DNS:vaultwarden.home"
```

Erzeugte Dateien:

- `vaultwarden.key` – privater Schlüssel
- `vaultwarden.crt` – selbstsigniertes Zertifikat

Der private Schlüssel darf nicht in das Git-Repository eingecheckt werden.

Das Zertifikat ist in Nginx Proxy Manager als benutzerdefiniertes Zertifikat hinterlegt. Die zugehörigen persistenten Daten befinden sich unter anderem in:

- `data/custom_ssl/`
- `data/database.sqlite`
- `data/keys.json`

Das Zertifikat wurde auf dem iPhone als vertrauenswürdig eingerichtet, damit `vaultwarden.home` intern per HTTPS erreichbar ist.

### 6.5 Persistente Konfiguration

Der persistente Datenordner enthält unter anderem:

```text
data/
├── access/
├── custom_ssl/
├── database.sqlite
├── keys.json
├── letsencrypt-acme-challenge/
├── logs/
└── nginx/
```

Die Dateien und Verzeichnisse innerhalb von `data/` müssen zusammen gesichert und wiederhergestellt werden.

### 6.6 Konfigurationsverantwortung

| Konfiguration | Speicherort |
|---|---|
| Containerdefinition | Git-Repository |
| Ports, Volumes und Zeitzone | `docker-compose.yml` |
| Proxy Hosts und Access Lists | Persistenter Datenordner `data/` |
| SQLite-Datenbank | `data/database.sqlite` |
| Schlüsseldatei | `data/keys.json` |
| Benutzerdefinierte Zertifikate | `data/custom_ssl/` |
| Separat eingebundene ACME-Daten | `letsencrypt/` |
| Lokale DNS-Einträge | Pi-hole |

---

## 7. Health Checks

### 7.1 Containerstatus

```bash
cd ~/homelab/services/nginx-proxy-manager
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

### 7.2 Administrationsoberfläche

Direkter Aufruf:

```text
http://192.168.2.x:81
```

Regulärer interner Aufruf:

```text
npm.home
```

Erwartung:

- Administrationsoberfläche ist erreichbar
- Anmeldung funktioniert
- eingerichtete Proxy Hosts werden angezeigt

### 7.3 Proxy-Host-Funktion

Beispiel:

```bash
curl -I http://uptime.home
```

Erwartung:

- der Hostname wird aufgelöst
- Nginx Proxy Manager beantwortet die Anfrage
- keine Nginx-Proxy-Manager-Fehlerseite wird angezeigt

Je nach Backend können Statuscodes wie `200`, `301`, `302` oder eine Authentifizierungsantwort normal sein.

### 7.4 Backend-Erreichbarkeit

Das Backend muss unabhängig vom Proxy erreichbar sein.

Beispiel Uptime Kuma:

```bash
curl -I http://192.168.2.x:3001
```

Beispiel Pi-hole:

```bash
curl -I http://192.168.2.x:8080
```

Ein erfolgreicher Backend-Test bestätigt noch nicht die Funktion des Proxy Hosts. Backend und Proxy-Zugriff müssen getrennt geprüft werden.

### 7.5 Logprüfung

```bash
cd ~/homelab/services/nginx-proxy-manager
docker compose logs --tail 100 app
```

Erwartete Startmeldungen:

```text
Starting nginx
Starting backend
```

Zusätzlich prüfen:

- keine wiederholten Startfehler
- keine Port-Konflikte
- keine Datenbankfehler
- keine Restart-Schleife

---

## 8. Backup und Restore

### 8.1 Backup-Strategie

Der aktuelle automatische Backupweg sichert den vollständigen persistenten Datenordner:

```text
~/homelab/services/nginx-proxy-manager/data/
```

nach:

```text
/mnt/backup/DATUM/npm-data/
```

Der aktuelle Backup-Befehl lautet:

```bash
rsync -av --ignore-errors \
  ~/homelab/services/nginx-proxy-manager/data/ \
  "$BACKUP_DIR/npm-data/"
```

Das Backup enthält unter anderem:

- Proxy-Host-Konfigurationen
- `database.sqlite`
- `keys.json`
- benutzerdefinierte Zertifikate unter `custom_ssl/`
- generierte Nginx-Konfigurationen
- Access-Konfigurationen
- Logs

```text
TODO: Prüfen, ob der persistente Ordner
`~/homelab/services/nginx-proxy-manager/letsencrypt/`
Inhalte enthält und zusätzlich in das Backup aufgenommen werden muss.
```

### 8.2 Kontrolliertes Backup erstellen

Für ein kontrolliertes Dateibackup wird der Service vor dem Kopiervorgang gestoppt.

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/nginx-proxy-manager
```

Service stoppen:

```bash
docker compose down
```

Backup-Verzeichnis erstellen:

```bash
mkdir -p /mnt/backup/DATUM/npm-data
```

Persistente Daten sichern:

```bash
sudo rsync -a \
  ~/homelab/services/nginx-proxy-manager/data/ \
  /mnt/backup/DATUM/npm-data/
```

Service wieder starten:

```bash
docker compose up -d
```

### 8.3 Backup-Verifikation

Backup-Inhalt prüfen:

```bash
ls -la /mnt/backup/DATUM/npm-data/
```

Mindestens prüfen:

```text
custom_ssl/
database.sqlite
keys.json
nginx/
```

Servicezustand prüfen:

```bash
cd ~/homelab/services/nginx-proxy-manager
docker compose ps
```

Mindestens einen Proxy Host funktional prüfen:

```bash
curl -I http://uptime.home
```

### 8.4 Restore

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/nginx-proxy-manager
```

Service stoppen:

```bash
docker compose down
```

Vorhandene Daten als Sicherheitskopie verschieben:

```bash
sudo mv data "data.before-restore-$(date +%Y%m%d-%H%M%S)"
sudo mkdir -p data
```

Backup wiederherstellen:

```bash
sudo rsync -a \
  /mnt/backup/DATUM/npm-data/ \
  ~/homelab/services/nginx-proxy-manager/data/
```

Service starten:

```bash
docker compose up -d
```

### 8.5 Restore-Verifikation

Containerstatus prüfen:

```bash
docker compose ps
```

Logs prüfen:

```bash
docker compose logs --tail 100 app
```

Zusätzlich prüfen:

- Administrationsoberfläche ist erreichbar
- Anmeldung funktioniert
- Proxy Hosts sind vorhanden
- Access Lists sind vorhanden
- `vaultwarden.home` verwendet das selbstsignierte Zertifikat
- `vaultwarden.home` ist auf dem iPhone per HTTPS erreichbar
- mindestens ein HTTP-Proxy-Host funktioniert
- Backend-Services sind direkt erreichbar
- keine Datenbank- oder Zertifikatsfehler erscheinen in den Logs

Ein erfolgreich kopierter Datenordner garantiert noch keinen erfolgreichen Restore. Der Restore muss immer funktional geprüft werden.

---

## 9. Update und Wartung

### 9.1 Voraussetzungen

Vor einem Update:

- aktueller Health Check ist erfolgreich
- aktuelles Backup von `data/` ist vorhanden
- Backup-Inhalt wurde geprüft
- ausreichend freier Speicherplatz ist vorhanden
- keine bekannte Proxy-Störung liegt vor

### 9.2 Update durchführen

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/nginx-proxy-manager
```

Neues Image herunterladen:

```bash
docker compose pull
```

Container aktualisieren:

```bash
docker compose up -d
```

Logs prüfen:

```bash
docker compose logs --tail 100 app
```

### 9.3 Update-Verifikation

Containerstatus prüfen:

```bash
docker compose ps
```

Administrationsoberfläche prüfen:

```text
npm.home
```

Proxy Hosts prüfen:

```text
pihole.home
uptime.home
wiki.home
vaultwarden.home
syncthing.home
```

Zusätzlich prüfen:

- Anmeldung funktioniert
- Proxy Hosts sind vorhanden
- HTTP- und HTTPS-Weiterleitungen funktionieren
- selbstsigniertes Vaultwarden-Zertifikat ist weiterhin vorhanden
- keine Datenbank- oder Zertifikatsfehler erscheinen in den Logs

---

## 10. Bekannte Störungen und Troublelogs

Das Runbook beschreibt den regulären Betrieb und die grundlegende Diagnose von Nginx Proxy Manager.

Ausführliche Fehleranalysen, Ursachen, durchgeführte Maßnahmen und Lessons Learned werden in separaten Troublelogs dokumentiert.

### 10.1 Schnellübersicht

| Störung                                                      | Erste Prüfung                                                                        | Troublelog                                                                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| NPM meldet `Internal Error` beim Anfordern eines Zertifikats | NPM-Logs, Zertifikatskonfiguration und Erreichbarkeit des Zertifikatsdienstes prüfen | [2026-06-24 – NPM meldet „Internal Error“ beim Anfordern eines Zertifikats](../../troubleshooting/log.md) |
| Pi-hole liefert HTTP 403 über Nginx Proxy Manager            | Forward Port, Backend-Pfad und Pi-hole-Proxy-Konfiguration prüfen                    | [2026-06-29 – Pi-hole 403 über Nginx Proxy Manager – Permanente Lösung](../../troubleshooting/log.md)     |


### 10.2 Basisdiagnose

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/nginx-proxy-manager
```

Compose-Konfiguration prüfen:

```bash
docker compose config
```

Containerstatus prüfen:

```bash
docker compose ps
```

Logs prüfen:

```bash
docker compose logs --tail 100 app
```

Belegte Ports prüfen:

```bash
sudo ss -tlnp | grep -E ':(80|81|443)\b'
```

Administrationsoberfläche lokal prüfen:

```bash
curl -I http://localhost:81
```

### 10.3 Proxy-Host-Diagnose

Proxy Host in der Weboberfläche prüfen:

```text
Hosts
→ Proxy Hosts
→ Edit
```

Prüfen:

- Domain Name ist korrekt
- Scheme ist korrekt
- Forward Hostname / IP ist korrekt
- Forward Port ist korrekt
- Access List blockiert den Zugriff nicht
- TLS-Zertifikat ist korrekt zugewiesen

Backend direkt prüfen:

```bash
curl -I http://192.168.2.x:BACKEND-PORT
```

Proxy Host prüfen:

```bash
curl -I http://HOSTNAME.home
```

Bei einem HTTPS-Proxy-Host:

```bash
curl -I https://HOSTNAME.home
```

### 10.4 Einordnung typischer HTTP-Fehler

| Fehler | Typische Bedeutung | Erste Prüfung |
|---:|---|---|
| 403 | Zugriff wird durch NPM oder den Backend-Service verweigert | Access List, Backend-Pfad und Berechtigungen |
| 502 | NPM erreicht das Backend nicht oder erhält keine gültige Antwort | IP-Adresse, Port, Scheme und Backend-Status |
| 504 | Backend antwortet nicht innerhalb des erwarteten Zeitraums | Backend-Auslastung, Firewall und Netzwerkverbindung |

Ein einzelner HTTP-Statuscode beweist die Ursache nicht. Die Diagnose muss Backend und Proxy Host getrennt prüfen.

### 10.5 Eskalation

Falls eine Störung durch die Basisdiagnose nicht behoben werden kann:

1. Keine unkontrollierten Änderungen an mehreren Proxy Hosts gleichzeitig durchführen.
2. Symptome, betroffene Domain, Zeitstempel und relevante Logs sichern.
3. Backend direkt prüfen.
4. Proxy-Host-Konfiguration dokumentieren.
5. Vorhandene Troublelogs prüfen.
6. Einen neuen Troublelog anlegen.
7. Nach erfolgreicher Lösung den Troublelog mit diesem Runbook verknüpfen.

---

## 11. Verweise

### 11.1 Interne Dokumentation

- [`docker-compose.yml`](docker-compose.yml)
- [Pi-hole-Service-Runbook](../pihole/README.md)
- [DNS-Dokumentation](../../infrastructure/network/dns.md)
- [Netzwerkübersicht](../../infrastructure/network/network-overview.md)
- [Backup- und Restore-Runbook](../../runbooks/backup-restore.md)
- [Zentrales Störungs- und Troublelog](../../troubleshooting/log.md)

### 11.2 Troublelogs

```text
TODO: Zugehörige Troublelogs manuell verlinken.
```

### 11.3 Externe Dokumentation

```text
TODO: Offizielle Nginx-Proxy-Manager-Dokumentation verlinken.
TODO: Offizielle Dokumentation des Nginx-Proxy-Manager-Docker-Images verlinken.
TODO: OpenSSL-Dokumentation für selbstsignierte Zertifikate verlinken.
```

---

## 12. Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 2026-07-29 | Runbook in die einheitliche Referenzstruktur überführt |
