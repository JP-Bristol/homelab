# Homelab-Infrastrukturplanung

| Metadatum | Wert |
|---|---|
| Dokumentstatus | `AKTIV` |
| Planungshorizont | Langfristig |
| Letzte Aktualisierung | `2026-07-28` |
| Verantwortlich | `TODO` |

---

## 1. Ziel und aktueller Stand

### 1.1 Ziel

Dieses Dokument beschreibt den geplanten Ausbau des Homelabs, die vorgesehene Rollenverteilung der Hosts sowie die schrittweise Migration bestehender Services.

Ziel ist eine nachvollziehbare Trennung zwischen produktiven Basisdiensten, Monitoring, Dokumentation, Dateidiensten, Entwicklungsumgebungen, Virtualisierung und zentralem Storage.

### 1.2 Aktueller Stand

Aktuell laufen die produktiven Homelab-Services überwiegend auf dem Raspberry Pi 5 `Arasaka`.

Der geplante Ausbau verteilt die Services schrittweise auf spezialisierte Hosts. Migrationen erfolgen erst, nachdem der jeweilige Zielhost eingerichtet, abgesichert und in das Backup-Konzept eingebunden wurde.

---

## 2. Geplante Hardware

| Gerät | Codename | Status | Vorgesehene Rolle |
|---|---|---|---|
| Raspberry Pi 5 | Arasaka | Vorhanden | DNS, Reverse Proxy und zentrale Basisdienste |
| Raspberry Pi 5 | Trauma Team | Geplant | Monitoring und Visualisierung |
| Raspberry Pi 5 | Militech | Geplant | Dokumentation und Dateidienste |
| Raspberry Pi 5 | Netrunner | Geplant | Entwicklung, Automatisierung und Tests |
| OptiPlex Mini-PC | Mikoshi | Geplant | Virtualisierung, Lab-Infrastruktur und KI |
| PoE-Switch | Afterlife | Geplant | Switching und PoE-Versorgung |
| Touch-Display | Delamain | Geplant | Monitoring-Anzeige |
| NAS | Crystal Palace | Langfristig geplant | Zentraler Speicher und Backup-Ziel |

---

## 3. Service-Verteilung

### 3.1 Arasaka – Raspberry Pi 1

**Status:** Aktiv

| Service | Zweck | Status |
|---|---|---|
| Pi-hole | DNS und Adblocker | ✅ Läuft |
| Nginx Proxy Manager | Reverse Proxy | ✅ Läuft |
| Vaultwarden | Passwortmanager | ✅ Läuft |
| Uptime Kuma | Monitoring | ✅ Läuft |
| Wiki.js | Dokumentation | ✅ Läuft |
| Syncthing | Datei-Synchronisation | ✅ Läuft |
| UFW | Firewall | ✅ Aktiv |
| fail2ban | Brute-Force-Schutz | ✅ Aktiv |

Arasaka bleibt zunächst der zentrale produktive Host. Uptime Kuma und Wiki.js sollen später auf spezialisierte Systeme migriert werden.

### 3.2 Trauma Team – Raspberry Pi 2

**Status:** Geplant

| Service | Zweck | Status |
|---|---|---|
| Uptime Kuma | Verfügbarkeitsmonitoring | 🔲 Migration von Arasaka geplant |
| Zabbix | Infrastrukturmonitoring | 🔲 Zielhost noch festzulegen |
| Grafana | Dashboards und Visualisierung | 🔲 Zielhost noch festzulegen |
| Touch-Dashboard | Eigenes Monitoring-Display | 🔲 Geplant |

Trauma Team soll mindestens Uptime Kuma und die Anbindung des Touch-Displays übernehmen.

Ob Grafana und Zabbix dauerhaft auf Trauma Team oder später auf Mikoshi betrieben werden, ist noch zu entscheiden.

### 3.3 Militech – Raspberry Pi 3

**Status:** Geplant

| Service | Zweck | Status |
|---|---|---|
| Wiki.js | Wissens- und Homelab-Dokumentation | 🔲 Migration von Arasaka geplant |
| Paperless-ngx | Dokumentenmanagement | 🔲 Geplant |
| Nextcloud | Self-hosted Storage und Dateizugriff | 🔲 Geplant |

Vor der Inbetriebnahme von Paperless-ngx oder Nextcloud muss ein Storage- und Backup-Konzept festgelegt werden.

### 3.4 Netrunner – Raspberry Pi 4

**Status:** Geplant

| Service | Zweck | Status |
|---|---|---|
| Gitea | Self-hosted Git | 🔲 Geplant |
| n8n | Automatisierung | 🔲 Geplant |
| Testumgebungen | Experimente und Entwicklung | 🔲 Geplant |

Netrunner ist nicht für kritische produktive Basisdienste vorgesehen. Experimente und Tests dürfen den Betrieb der übrigen Hosts nicht beeinträchtigen.

### 3.5 Mikoshi – OptiPlex

**Status:** Geplant

| Virtuelle Maschine | Zweck | Status |
|---|---|---|
| VM 1 – Windows Server | Active Directory, GPO und DNS | 🔲 Geplant |
| VM 2 – Windows 11 | Client und Testing | 🔲 Geplant |
| VM 3 – Linux-Testsystem | Experimente | 🔲 Geplant |
| VM 4 – Docker-Produktion | Möglicher Zielhost für Grafana und Zabbix | 🔲 Zielarchitektur offen |
| VM 5 – Docker-KI | Qdrant, Runbook-Agent und KI-Workspace | 🔲 Geplant |

Mikoshi soll als Virtualisierungshost mit Proxmox betrieben werden.

Produktive und experimentelle Workloads werden in getrennten virtuellen Maschinen ausgeführt.

### 3.6 Afterlife – PoE-Switch

**Status:** Geplant

Vorgesehene Aufgaben:

- zentrale Netzwerkanbindung der Raspberry Pis
- PoE-Versorgung geeigneter Geräte
- Vorbereitung einer späteren Netzwerksegmentierung
- Anbindung von Mikoshi, Delamain und Crystal Palace

### 3.7 Delamain – Touch-Display

**Status:** Geplant

Delamain dient als dauerhaft sichtbare Monitoring-Anzeige.

Vorgesehene Inhalte:

- Erreichbarkeit zentraler Services
- Hoststatus
- aktuelle Störungen
- zusammengefasste Monitoring-Metriken

Die Daten sollen von Trauma Team beziehungsweise dem später festgelegten zentralen Monitoring-System bereitgestellt werden.

### 3.8 Crystal Palace – NAS

**Status:** Langfristig geplant

Vorgesehene Aufgaben:

- zentraler Netzwerkspeicher
- mögliches Backup-Ziel
- Bereitstellung größerer Datenbestände
- Storage für Dokumenten- und Dateidienste

Die konkrete NAS-Lösung wird erst festgelegt, wenn Speicherbedarf, Redundanzanforderungen und Backup-Strategie definiert sind.

---

## 4. Netzwerk-Zielzustand

### 4.1 Geplante Komponenten

```text
Internet
   |
Router
   |
Afterlife – PoE-Switch
   |
   +-- Arasaka
   +-- Trauma Team
   +-- Militech
   +-- Netrunner
   +-- Mikoshi
   +-- Delamain
   +-- Crystal Palace
```

### 4.2 Zentrale Netzwerkdienste

- lokaler DNS über Pi-hole
- Reverse Proxy über Nginx Proxy Manager
- Host-Firewall über UFW
- Brute-Force-Schutz über fail2ban
- langfristiger VPN-Zugriff über WireGuard
- langfristige Netzwerksegmentierung über VLANs

### 4.3 Geplante Netzwerksegmentierung

Eine spätere Segmentierung soll mindestens folgende Bereiche prüfen:

- produktive Server
- Management
- Clients
- Test- und Entwicklungsumgebungen
- Monitoring
- Storage
- IoT- und Dashboard-Geräte

```text
TODO: VLAN- und IP-Adresskonzept erstellen.
```

---

## 5. Abhängigkeiten

### 5.1 Trauma Team

Vor der Migration von Uptime Kuma müssen folgende Voraussetzungen erfüllt sein:

- Betriebssystem installiert und abgesichert
- Docker und Docker Compose eingerichtet
- Netzwerkverbindung und DNS-Auflösung geprüft
- Backup-Ziel angebunden
- Backup und Restore getestet
- Monitoring während der Migration weiterhin verfügbar

### 5.2 Militech

Vor der Migration von Wiki.js und der Installation weiterer Dateidienste müssen folgende Voraussetzungen erfüllt sein:

- Storage-Konzept festgelegt
- Backup- und Restore-Konzept vorhanden
- Zugriffs- und Berechtigungskonzept erstellt
- ausreichende Speicherkapazität geprüft

### 5.3 Mikoshi

Vor dem produktiven Einsatz müssen folgende Voraussetzungen erfüllt sein:

- Proxmox installiert und abgesichert
- VM- und Netzwerkstruktur definiert
- Backup-Ziel festgelegt
- Ressourcen für virtuelle Maschinen geplant
- Trennung zwischen produktiven und experimentellen Workloads umgesetzt

### 5.4 Crystal Palace

Vor der Beschaffung oder Einrichtung müssen folgende Punkte geklärt sein:

- benötigte Speicherkapazität
- gewünschte Redundanz
- Backup-Ziele und Aufbewahrungsfristen
- Netzwerkgeschwindigkeit
- Energieverbrauch
- Wiederherstellungsanforderungen

---

## 6. Migrationsplan

### 6.1 Phase 1 – Bestehendes Homelab stabilisieren

**Status:** Aktiv

**Ziel:**

Der aktuelle Betrieb auf Arasaka ist dokumentiert, abgesichert und wiederherstellbar.

**Umfang:**

- Raspberry Pi 5 `Arasaka`
- Docker und Docker Compose
- Backup-System
- Pi-hole
- Nginx Proxy Manager
- Vaultwarden
- Uptime Kuma
- Wiki.js
- UFW
- fail2ban
- Service-Runbooks
- getestete Restore-Verfahren

**Abschlusskriterien:**

- zentrale Services sind dokumentiert
- Backups laufen regelmäßig
- Restore-Verfahren sind dokumentiert
- Health Checks sind definiert
- bekannte Störungen sind in Troublelogs erfasst

### 6.2 Phase 2 – Monitoring auslagern

**Status:** Geplant

**Ziel:**

Trauma Team übernimmt das zentrale Verfügbarkeitsmonitoring.

**Umfang:**

- zweiten Raspberry Pi bereitstellen
- Betriebssystem und Docker einrichten
- Uptime Kuma von Arasaka migrieren
- Backup und Restore testen
- Delamain anbinden
- Standort von Grafana und Zabbix festlegen

**Abschlusskriterien:**

- Uptime Kuma läuft auf Trauma Team
- alle Monitore wurden übernommen
- Benachrichtigungen funktionieren
- Monitoring bleibt während der Migration verfügbar
- Backup und Restore wurden erfolgreich getestet

### 6.3 Phase 3 – Dokumentation und Dateidienste auslagern

**Status:** Geplant

**Ziel:**

Militech übernimmt Dokumentation und ausgewählte Dateidienste.

**Umfang:**

- Militech bereitstellen und absichern
- Wiki.js von Arasaka migrieren
- Storage-Konzept umsetzen
- Paperless-ngx prüfen und gegebenenfalls installieren
- Nextcloud prüfen und gegebenenfalls installieren

**Abschlusskriterien:**

- Wiki.js läuft auf Militech
- Dokumentationsdaten wurden vollständig übernommen
- Backup und Restore wurden getestet
- Berechtigungen und Datenpfade sind dokumentiert

### 6.4 Phase 4 – Virtualisierungsserver integrieren

**Status:** Geplant

**Ziel:**

Mikoshi stellt getrennte virtuelle Umgebungen für Server-, Client-, Docker- und KI-Workloads bereit.

**Umfang:**

- OptiPlex beschaffen und vorbereiten
- Proxmox installieren
- Netzwerk- und Storage-Anbindung einrichten
- geplante virtuelle Maschinen anlegen
- Backup-Konzept für virtuelle Maschinen umsetzen
- langfristigen Standort von Grafana und Zabbix festlegen

**Abschlusskriterien:**

- Proxmox läuft stabil
- produktive und experimentelle VMs sind getrennt
- Backups der VMs sind eingerichtet
- Wiederherstellung einer Test-VM wurde geprüft

### 6.5 Phase 5 – Entwicklungs- und Automatisierungsumgebung aufbauen

**Status:** Geplant

**Ziel:**

Netrunner übernimmt Test-, Entwicklungs- und Automatisierungsaufgaben.

**Umfang:**

- Netrunner bereitstellen
- Gitea installieren
- n8n installieren
- isolierte Testumgebungen einrichten
- Zugriffs- und Backup-Konzept dokumentieren

**Abschlusskriterien:**

- Experimente sind von produktiven Services getrennt
- Repositories und Automatisierungen werden gesichert
- Testumgebungen können reproduzierbar erstellt werden

### 6.6 Phase 6 – Netzwerk segmentieren

**Status:** Langfristig geplant

**Ziel:**

Produktive Systeme, Management, Clients, Experimente und Storage werden logisch voneinander getrennt.

**Umfang:**

- Afterlife bereitstellen
- VLAN-Konzept erstellen
- Firewall-Regeln definieren
- Management-Zugänge absichern
- Services schrittweise in die vorgesehenen Segmente migrieren

**Abschlusskriterien:**

- Netzwerksegmente sind dokumentiert
- notwendige Kommunikation ist freigegeben
- unerwünschte Kommunikation ist blockiert
- Management-Zugänge wurden getestet

### 6.7 Phase 7 – Zentrales Storage integrieren

**Status:** Langfristig geplant

**Ziel:**

Crystal Palace stellt zentralen Speicher für geeignete Services und Backups bereit.

**Umfang:**

- Anforderungen an Speicher und Redundanz festlegen
- NAS-Lösung auswählen
- Netzwerk- und Berechtigungskonzept umsetzen
- Backup-Ziele migrieren
- Wiederherstellungsverfahren testen

**Abschlusskriterien:**

- Storage ist redundant und dokumentiert
- Berechtigungen wurden geprüft
- Backups werden erfolgreich gespeichert
- Wiederherstellung wurde getestet

---

## 7. Offene Entscheidungen

- langfristiger Standort von Grafana und Zabbix
- Umfang des Monitorings auf Trauma Team
- Storage-Lösung für Militech
- Backup-Ziel für Mikoshi
- konkrete NAS-Lösung für Crystal Palace
- VLAN- und IP-Adresskonzept
- Notwendigkeit und Zeitpunkt des vierten Raspberry Pi
- Rolle von Syncthing im zukünftigen Zielzustand
- Zeitpunkt der Migration von Uptime Kuma
- Zeitpunkt der Migration von Wiki.js
- Auswahl der Services für Delamain
- Reihenfolge der Phasen nach der Monitoring-Migration
