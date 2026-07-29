# Service Runbook: Pi-hole

| Metadatum | Wert |
|---|---|
| Dokumentstatus | `AKTIV` |
| Service-Status | Produktiv |
| Service-Typ | DNS-Server und Netzwerkfilter |
| Verantwortlich | `TODO` |
| Letzte technische Prüfung | `TODO – nach vollständiger Prüfung setzen` |
| Runbook-Version | `1.0` |

---

## 0. Systemübersicht

| Eigenschaft | Wert |
|---|---|
| Host | Raspberry Pi 5 |
| Host-IP | `192.168.2.x` |
| Containername | `pihole` |
| Service-Pfad | `~/homelab/services/pihole/` |
| Weboberfläche | `pihole.home` |
| Reverse Proxy | Nginx Proxy Manager |
| Internes Proxy-Ziel | `192.168.2.x:8080` |
| DNS-Port | `53/TCP` und `53/UDP` |
| Web-Host-Port | `8080/TCP` |
| Web-Container-Port | `80/TCP` |
| Upstream-DNS | Quad9 |
| Persistente Daten | `~/homelab/services/pihole/data/etc-pihole/` |
| Backup-Ziel | `/mnt/backup/DATUM/pihole-data/` |
| Restart Policy | `unless-stopped` |

---

## 1. Service-Übersicht

### 1.1 Zweck

Pi-hole ist ein netzwerkweiter, DNS-basierter Werbe- und Tracking-Blocker.

DNS-Anfragen aus dem Heimnetz werden zentral durch Pi-hole verarbeitet. Domains, die in den konfigurierten Blocklisten enthalten sind, werden gefiltert.

Pi-hole übernimmt zusätzlich die Verwaltung lokaler DNS-Namen für interne Homelab-Services.

### 1.2 Ziele

- Netzwerkweites Blockieren von Werbung und Tracking-Domains
- Zentrale DNS-Auflösung im Homelab
- Verwaltung lokaler DNS-Einträge
- Einheitlicher Zugriff auf interne Services über Hostnamen
- Transparenz über DNS-Anfragen und verwendete Clients
- Reduzierung manueller Einträge in lokalen `hosts`-Dateien

### 1.3 Besonderheiten

- DHCP wird weiterhin durch den Router bereitgestellt.
- Pi-hole übernimmt DNS-Auflösung, DNS-Filterung und lokale DNS-Einträge.
- Quad9 wird als Upstream-DNS verwendet.
- Die Weboberfläche wird über Nginx Proxy Manager bereitgestellt.
- Der reguläre Zugriff erfolgt über `pihole.home`.
- Ein Port oder der Pfad `/admin` muss beim normalen Zugriff nicht angegeben werden.
- Pi-hole leitet den Aufruf der Hauptseite auf die Administrationsoberfläche weiter.
- Der direkte Zugriff über IP-Adresse und Port `8080` ist nur für Diagnosezwecke vorgesehen.
- Die verwendete EasyBox verteilt Pi-hole nicht zuverlässig als DNS-Server. Auf betroffenen Geräten muss Pi-hole daher manuell als DNS-Server eingetragen werden.

---

## 2. Architektur

### 2.1 Architekturübersicht

```text
DNS-Clients im Heimnetz
          │
          │ DNS über Port 53 TCP/UDP
          ▼
       Pi-hole
          │
          ├── DNS-Filterung
          ├── Blocklisten
          ├── lokale DNS-Einträge
          └── DNS-Weiterleitung
                    │
                    ▼
                  Quad9


Browser
   │
   │ pihole.home
   ▼
Nginx Proxy Manager
   │
   │ internes HTTP
   ▼
192.168.2.x:8080
   │
   ▼
Pi-hole Webserver
   │
   ▼
Weiterleitung auf /admin
```

### 2.2 Komponenten und Abhängigkeiten

| Komponente | Aufgabe |
|---|---|
| Raspberry Pi 5 | Docker-Host |
| Docker | Container-Laufzeit |
| Docker Compose | Deployment und Container-Konfiguration |
| Pi-hole | DNS-Auflösung, DNS-Filterung und lokale DNS-Verwaltung |
| Quad9 | Externe DNS-Auflösung |
| Nginx Proxy Manager | Zugriff auf die Weboberfläche über `pihole.home` |
| Router/EasyBox | DHCP und Netzwerk-Gateway |
| Persistenter Datenordner | Speicherung der Pi-hole-Konfiguration |
| Git-Repository | Versionierung der Deployment-Konfiguration |

### 2.3 Rollenverteilung

| Funktion | Zuständiges System |
|---|---|
| DHCP | Router/EasyBox |
| Netzwerk-Gateway | Router/EasyBox |
| DNS-Auflösung | Pi-hole |
| DNS-Filterung | Pi-hole |
| Lokale DNS-Einträge | Pi-hole |
| Externe DNS-Auflösung | Quad9 |
| Webzugriff | Nginx Proxy Manager |
| Deployment-Konfiguration | Git-Repository |
| Laufzeitdaten | Persistenter `data/`-Ordner |

---

## 3. Netzwerk und Ports

### 3.1 Portübersicht

| Host-Port | Container-Port | Protokoll | Zweck |
|---:|---:|---|---|
| 53 | 53 | TCP | DNS-Anfragen über TCP |
| 53 | 53 | UDP | DNS-Anfragen über UDP |
| 8080 | 80 | TCP | Internes Ziel für Nginx Proxy Manager |

Port `8080` wird nicht als reguläre Benutzeradresse verwendet.

### 3.2 Webzugriff

Der reguläre Zugriff erfolgt über:

```text
pihole.home
```

Nginx Proxy Manager leitet die Anfrage intern an den Pi-hole-Webserver weiter:

```text
pihole.home
→ Nginx Proxy Manager
→ 192.168.2.x:8080
→ Pi-hole
→ /admin
```

Ein Port oder der Pfad `/admin` muss nicht manuell eingegeben werden.

> **Diagnosehinweis:** Falls `pihole.home` nicht erreichbar ist, kann geprüft werden, ob Pi-hole intern über `192.168.2.x:8080` erreichbar ist. Dieser Zugriffsweg ist nicht für den regulären Betrieb vorgesehen.

### 3.3 Lokale DNS-Verwaltung

Lokale Hostnamen werden in Pi-hole als **Local DNS Records** verwaltet.

Beispiele:

- `pihole.home`
- `uptime.home`
- `npm.home`
- `wiki.home`
- `vaultwarden.home`

Verwaltung:

```text
Pi-hole Web UI
→ Local DNS
→ DNS Records
```

Dadurch können interne Services über einheitliche Hostnamen erreicht werden. Manuelle Einträge in den lokalen `hosts`-Dateien der Clients sind nicht erforderlich.

Weitere Informationen:

```text
infrastructure/network/dns.md
```

### 3.4 DNS-Konfiguration der Clients

Clients müssen die Pi-hole-IP als DNS-Server verwenden:

```text
192.168.2.x
```

Prüfung auf einem Client:

```bash
dig google.com
```

Erwartete Ausgabe:

```text
;; SERVER: 192.168.2.x#53
```

Wird stattdessen die Router-IP angezeigt, verwendet der Client nicht Pi-hole als DNS-Server.

---

## 4. Deployment

### 4.1 Deployment-Prinzip

Die Docker-Compose-Datei und die grundlegende Service-Konfiguration werden im Git-Repository versioniert.

Das Git-Repository ist die Quelle der Wahrheit für:

- Containerdefinition
- Portfreigaben
- Volume-Mounts
- Umgebungsvariablen-Struktur
- Deployment-Ablauf

Operative Pi-hole-Daten werden persistent unter `data/` gespeichert. Änderungen, die über die Pi-hole-Weboberfläche vorgenommen werden, befinden sich daher nicht vollständig im Git-Repository.

### 4.2 Voraussetzungen

- Raspberry Pi ist über SSH erreichbar
- Docker ist installiert
- Docker Compose ist installiert
- Homelab-Git-Repository ist vorhanden
- Host besitzt eine feste IP-Adresse oder DHCP-Reservierung
- Port `53/TCP` ist frei
- Port `53/UDP` ist frei
- Port `8080/TCP` ist frei
- `.env`-Datei ist vorhanden
- Nginx Proxy Manager ist erreichbar
- DNS-Eintrag für `pihole.home` ist vorhanden

### 4.3 Verzeichnisstruktur

```text
~/homelab/services/pihole/
├── docker-compose.yml
├── .env
├── .env.example
└── data/
    └── etc-pihole/
```

| Pfad | Zweck |
|---|---|
| `docker-compose.yml` | Definition des Pi-hole-Containers |
| `.env` | Lokale Zugangsdaten und Umgebungsvariablen |
| `.env.example` | Vorlage ohne echte Zugangsdaten |
| `data/etc-pihole/` | Persistente Pi-hole-Konfiguration und Daten |

### 4.4 Environment konfigurieren

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/pihole
```

Environment-Datei aus der Vorlage erstellen:

```bash
cp .env.example .env
nano .env
```

Aktuelle Variable:

```env
FTLCONF_webserver_api_password=secure-password
```

Die `.env`-Datei darf nicht in das Git-Repository eingecheckt werden.

### 4.5 Docker-Compose-Konfiguration

```yaml
services:
  pihole:
    image: pihole/pihole:latest
    container_name: pihole

    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80"

    environment:
      TZ: Europe/Berlin
      WEBPASSWORD: ${FTLCONF_webserver_api_password}
      FTLCONF_dns_listeningMode: all

    volumes:
      - ./data/etc-pihole:/etc/pihole

    restart: unless-stopped
```

### 4.6 Compose-Konfiguration prüfen

Vor dem Deployment:

```bash
cd ~/homelab/services/pihole
docker compose config
```

Erwartung:

- keine YAML-Fehler
- Environment-Variable wird aufgelöst
- Volume-Pfad ist korrekt
- Ports sind korrekt definiert

### 4.7 Deployment starten

```bash
cd ~/homelab/services/pihole
docker compose up -d
```

Containerstatus prüfen:

```bash
docker compose ps
```

Logs prüfen:

```bash
docker logs pihole --tail 100
```

### 4.8 Post-Deploy-Verifikation

Pi-hole-Status prüfen:

```bash
docker exec pihole pihole status
```

DNS-Auflösung prüfen:

```bash
dig @192.168.2.x google.com
```

Lokale DNS-Auflösung prüfen:

```bash
dig @192.168.2.x pihole.home
```

Weboberfläche öffnen:

```text
pihole.home
```

Erwartung:

- Container läuft
- Pi-hole-Blocking ist aktiviert
- öffentliche Domains werden aufgelöst
- `pihole.home` wird aufgelöst
- Nginx Proxy Manager leitet die Anfrage an Pi-hole weiter
- die Administrationsoberfläche wird ohne manuelle Eingabe von `/admin` geöffnet

### 4.9 Manueller Fallback

Der manuelle Fallback wird nur verwendet, wenn das Git-Repository nicht verfügbar ist.

Verzeichnis erstellen:

```bash
mkdir -p ~/homelab/services/pihole
cd ~/homelab/services/pihole
```

Benötigte Dateien manuell anlegen:

```bash
nano docker-compose.yml
nano .env
```

Konfiguration prüfen und Service starten:

```bash
docker compose config
docker compose up -d
```

Die manuell erstellten Dateien müssen später mit dem Git-Repository abgeglichen werden.

---

## 5. Betrieb

Alle Befehle werden im Service-Verzeichnis ausgeführt:

```bash
cd ~/homelab/services/pihole
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
docker compose restart pihole
```

### 5.4 Status

```bash
docker compose ps
```

### 5.5 Logs

Fortlaufende Logs:

```bash
docker logs -f pihole
```

Letzte 100 Logzeilen:

```bash
docker logs pihole --tail 100
```

### 5.6 Container-Shell

```bash
docker exec -it pihole bash
```

---

## 6. Konfiguration

### 6.1 Administrationspasswort ändern

Passwort interaktiv ändern:

```bash
docker exec pihole pihole setpassword
```

Das Passwort darf nicht im Runbook oder im Git-Repository gespeichert werden.

Nach einer Passwortänderung muss geprüft werden, ob die Anmeldung über `pihole.home` weiterhin funktioniert.

### 6.2 Upstream-DNS

Pi-hole verwendet Quad9 als Upstream-DNS.

Die Einstellung wird über die Pi-hole-Weboberfläche verwaltet.

Nach Änderungen muss geprüft werden, ob externe Domains weiterhin aufgelöst werden:

```bash
dig @192.168.2.x google.com
```

### 6.3 Lokale DNS-Einträge

Verwaltung:

```text
Pi-hole Web UI
→ Local DNS
→ DNS Records
```

Nach einer Änderung:

```bash
dig @192.168.2.x HOSTNAME.home
```

Erwartung:

- Status `NOERROR`
- korrekte interne IP-Adresse wird zurückgegeben

### 6.4 Blocklisten

Blocklisten werden über die Pi-hole-Weboberfläche verwaltet.

Nach Änderungen muss geprüft werden:

- Listen wurden erfolgreich aktualisiert
- DNS-Auflösung funktioniert weiterhin
- gewünschte Domains werden blockiert
- erforderliche Domains werden nicht versehentlich blockiert

### 6.5 Listening Mode

In der Compose-Datei ist gesetzt:

```yaml
FTLCONF_dns_listeningMode: all
```

Dadurch akzeptiert Pi-hole DNS-Anfragen über die verfügbaren Container-Netzwerkschnittstellen.

### 6.6 Nginx Proxy Manager

Für die Weboberfläche existiert in Nginx Proxy Manager ein Proxy Host für:

```text
pihole.home
```

Das interne Ziel ist:

```text
192.168.2.x:8080
```

Nach Änderungen an der Proxy-Konfiguration muss der Zugriff über `pihole.home` geprüft werden.

### 6.7 Konfigurationsverantwortung

| Konfiguration | Speicherort |
|---|---|
| Containerdefinition | Git-Repository |
| Ports und Volumes | `docker-compose.yml` |
| Zugangsdaten | `.env` |
| Pi-hole-Konfiguration | `data/etc-pihole/` |
| Lokale DNS-Einträge | Persistente Pi-hole-Daten |
| Blocklisten | Persistente Pi-hole-Daten |
| Reverse Proxy | Nginx Proxy Manager |
| Upstream-DNS | Pi-hole-Konfiguration |

---

## 7. Health Checks

### 7.1 Containerstatus

```bash
cd ~/homelab/services/pihole
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

### 7.2 Pi-hole-Status

```bash
docker exec pihole pihole status
```

Erwartung:

```text
Pi-hole blocking is enabled
```

### 7.3 DNS-Auflösung

```bash
dig @192.168.2.x google.com
```

Erwartung:

```text
status: NOERROR
```

### 7.4 Verwendeter DNS-Server

Prüfung auf einem Client:

```bash
dig google.com
```

Erwartung:

```text
;; SERVER: 192.168.2.x#53
```

### 7.5 Lokale DNS-Auflösung

```bash
dig @192.168.2.x pihole.home
```

Erwartung:

- Status `NOERROR`
- korrekte interne IP-Adresse wird zurückgegeben

### 7.6 Weboberfläche und Reverse Proxy

Aufruf:

```text
pihole.home
```

Erwartung:

- DNS-Name wird aufgelöst
- Nginx Proxy Manager ist erreichbar
- Weiterleitung zu Pi-hole funktioniert
- Administrationsoberfläche wird geöffnet
- Anmeldung funktioniert
- DNS-Anfragen werden im Dashboard angezeigt

### 7.7 Logprüfung

```bash
docker logs pihole --tail 100
```

Erwartung:

- keine wiederholten Startfehler
- keine Port-Konflikte
- keine Datenbankfehler
- keine Restart-Schleife

---

## 8. Backup und Restore

### 8.1 Backup-Strategie

Gesichert wird der vollständige persistente Datenordner:

```text
~/homelab/services/pihole/data/
```

Dieser enthält unter anderem:

- Pi-hole-Konfiguration
- lokale DNS-Einträge
- Blocklisten und zugehörige Einstellungen
- weitere persistente Pi-hole-Daten

Für ein konsistentes Dateibackup wird der Container vor dem Kopiervorgang gestoppt.

Die `.env`-Datei enthält Zugangsdaten und muss separat in einem sicheren beziehungsweise verschlüsselten Backup gespeichert werden.

### 8.2 Backup erstellen

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/pihole
```

Service stoppen:

```bash
docker compose down
```

Backup-Verzeichnis erstellen:

```bash
mkdir -p /mnt/backup/DATUM/pihole-data
```

Persistente Daten sichern:

```bash
sudo rsync -a \
  ~/homelab/services/pihole/data/ \
  /mnt/backup/DATUM/pihole-data/
```

Service wieder starten:

```bash
docker compose up -d
```

### 8.3 Backup-Verifikation

Backup-Inhalt prüfen:

```bash
ls -la /mnt/backup/DATUM/pihole-data/
```

Erwarteter Inhalt:

```text
etc-pihole/
```

Servicezustand prüfen:

```bash
docker compose ps
docker exec pihole pihole status
dig @192.168.2.x google.com
```

### 8.4 Restore

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/pihole
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
  /mnt/backup/DATUM/pihole-data/ \
  ~/homelab/services/pihole/data/
```

Service starten:

```bash
docker compose up -d
```

### 8.5 Restore-Verifikation

Containerstatus:

```bash
docker compose ps
```

Pi-hole-Status:

```bash
docker exec pihole pihole status
```

DNS-Auflösung:

```bash
dig @192.168.2.x google.com
```

Lokale DNS-Auflösung:

```bash
dig @192.168.2.x pihole.home
```

Zusätzlich prüfen:

- `pihole.home` ist erreichbar
- Anmeldung funktioniert
- lokale DNS-Einträge sind vorhanden
- Quad9 ist als Upstream-DNS konfiguriert
- Blocklisten sind vorhanden
- DNS-Anfragen erscheinen im Dashboard
- Blockierungen werden gezählt

Ein erfolgreich kopierter Datenordner garantiert noch keinen erfolgreichen Restore. Der Restore muss immer funktional geprüft werden.

---

## 9. Update und Wartung

### 9.1 Voraussetzungen

Vor einem Update:

- aktueller Health Check ist erfolgreich
- aktuelles Backup ist vorhanden
- ausreichend freier Speicherplatz ist vorhanden
- keine bekannte DNS-Störung liegt vor

### 9.2 Update durchführen

In das Service-Verzeichnis wechseln:

```bash
cd ~/homelab/services/pihole
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
docker logs pihole --tail 100
```

### 9.3 Update-Verifikation

```bash
docker compose ps
docker exec pihole pihole status
dig @192.168.2.x google.com
dig @192.168.2.x pihole.home
```

Zusätzlich prüfen:

- `pihole.home` ist erreichbar
- Anmeldung funktioniert
- lokale DNS-Einträge sind vorhanden
- Quad9 ist als Upstream-DNS konfiguriert
- Blocklisten sind vorhanden
- DNS-Anfragen werden verarbeitet
- Blocking ist aktiviert

---

## 10. Bekannte Störungen und Troublelogs

Das Runbook beschreibt den regulären Betrieb und die grundlegende Diagnose von Pi-hole.

Ausführliche Fehleranalysen, Ursachen, durchgeführte Maßnahmen und Lessons Learned werden in separaten Troublelogs dokumentiert.

### 10.1 Schnellübersicht

| Störung | Erste Prüfung | Troublelog |
|---|---|---|
| Anmeldung an der Weboberfläche schlägt fehl | Containerstatus, Logs und Passwort prüfen | `TODO` |
| Container startet nicht | Compose-Konfiguration, Logs und belegte Ports prüfen | `TODO` |
| Clients umgehen Pi-hole | Verwendeten DNS-Server auf dem Client prüfen | `TODO` |
| `pihole.home` ist nicht erreichbar | Lokale DNS-Auflösung und NPM-Proxy-Host prüfen | `TODO` |
| DNS-Auflösung funktioniert nicht | Pi-hole-Status und Erreichbarkeit von Port 53 prüfen | `TODO` |

### 10.2 Basisdiagnose

Containerstatus:

```bash
cd ~/homelab/services/pihole
docker compose ps
```

Containerlogs:

```bash
docker logs pihole --tail 100
```

Compose-Konfiguration:

```bash
docker compose config
```

Pi-hole-Status:

```bash
docker exec pihole pihole status
```

DNS-Auflösung über Pi-hole:

```bash
dig @192.168.2.x google.com
```

Lokale DNS-Auflösung:

```bash
dig @192.168.2.x pihole.home
```

Vom Client verwendeten DNS-Server prüfen:

```bash
dig google.com
```

Erwartung:

```text
;; SERVER: 192.168.2.x#53
```

### 10.3 Diagnose des Webzugriffs

Funktioniert `pihole.home` nicht, sind folgende Komponenten zu prüfen:

1. Lokaler DNS-Eintrag für `pihole.home`
2. Erreichbarkeit von Nginx Proxy Manager
3. Proxy-Host-Konfiguration in Nginx Proxy Manager
4. Erreichbarkeit des internen Ziels `192.168.2.x:8080`
5. Status des Pi-hole-Containers

### 10.4 Eskalation

Falls eine Störung durch die Basisdiagnose nicht behoben werden kann:

1. Keine unkontrollierten Konfigurationsänderungen durchführen.
2. Symptome, Zeitstempel und relevante Logs sichern.
3. Vorhandene Troublelogs prüfen.
4. Einen neuen Troublelog anlegen.
5. Durchgeführte Prüfungen und Maßnahmen dokumentieren.
6. Nach erfolgreicher Lösung den Troublelog mit diesem Runbook verknüpfen.

---

## 11. Verweise

### 11.1 Interne Dokumentation

- `infrastructure/network/dns.md`
- `docker-compose.yml`
- `.env.example`

### 11.2 Troublelogs

```text
TODO: Zugehörige Troublelogs manuell verlinken.
```

### 11.3 Externe Dokumentation

```text
TODO: Offizielle Pi-hole-Dokumentation verlinken.
TODO: Offizielle Dokumentation des Pi-hole-Docker-Images verlinken.
TODO: Quad9-Dokumentation verlinken.
```

---

## 12. Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 2026-07-16 | Runbook in die einheitliche Referenzstruktur überführt |
| 1.0 | 2026-07-16 | Nginx Proxy Manager und Zugriff über `pihole.home` dokumentiert |
| 1.0 | 2026-07-16 | Leeren DNSMasq-Volume-Mount entfernt |
| 1.0 | 2026-07-16 | Ausführliche Fehlerszenarien durch kompakte Troublelog-Übersicht ersetzt |