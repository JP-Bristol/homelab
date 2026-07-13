# Homelab Scripts
Kurze Übersicht aller eigenen Automatisierungs- und Monitoring-Skripte im Homelab.
## 1. Übersicht
| Script | Zweck | Ausführung | Status |  
|---|---|---|---|  
| `uptime_kuma.py` | Service-Status aus Uptime Kuma anzeigen | `python3 uptime_kuma.py` | ✅ v0.1 |  
| `backup_log.py` | Backup-Log auswerten | `python3 backup_log.py` | ✅ v0.1 |  
| `add_service/` | Neuen Service vorbereiten | `python3 add_service/main.py` | ✅ v0.4.0 |

### 1.1 Ablageort
```bash  
~/homelab/scripts/
```
## 2. Voraussetzungen

-   Python 3
-   `.env` Datei vorhanden
-   benötigte Python-Pakete installiert

### 2.1 Python installieren  
  
```bash  
sudo apt update  
sudo apt install python3 python3-pip python3-venv  
```

### 2.2 Python-Abhängigkeiten installieren  
  
```bash  
pip3 install -r requirements.txt --break-system-packages
```

Aktuell verwendete Pakete:  
  
- `python-dotenv`  
- `uptime-kuma-api`


### 2.3 Ausführung
Skripte werden aktuell manuell über das Terminal ausgeführt

## 3. Skripte

### 3.1 uptime_kuma.py
| Feld | Wert |
| - | - |
| Sprache | Python |
| Version | v0.1 |
| Status | ✅ Aktiv|
| Kategorie | Monitoring |

#### 3.1.1 Zweck
Überwacht alle Uptime-Kuma-Monitore und gibt den aktuellen Status inklusive Uptime und letztem Heartbeat aus.
#### 3.1.2 Voraussetzungen
- Python 3  
- `.env`  
- Uptime Kuma API erreichbar

**Abhängigkeiten**
- uptime-kuma-api  
- python-dotenv

#### 3.1.3 Ausführung
```bash  
cd ~/homelab/scripts/python  
python3 uptime_kuma.py
```
#### 3.1.4 Benötigte Umgebungsvariablen
```env 
HOMELAB_IP=  
USER_KUMA=  
PASSWORD_KUMA=
```

#### 3.1.5 Ausgabe
-   Service-Name
-   24h-Uptime
-   Status UP/DOWN
-   letzter Heartbeat

#### 3.1.6 Hinweise

Der aktuelle Status wird über `heartbeat.status` ermittelt, nicht über `monitor.active`.
`monitor.active` zeigt nur ob der Monitor aktiviert ist — nicht ob der Service läuft. Der tatsächliche Status wird über `heartbeat.status` ermittelt. Siehe: `troubleshooting/log.md` → 2026-07-04


### 3.2 backup_log.py
| Feld | Wert |
| - | - |
| Sprache | Python |
| Version | v0.1 |
| Status | ✅ Aktiv|
| Kategorie | Backup |

#### 3.2.1 Zweck
Analysiert das Backup-Log und erkennt Fehler.
#### 3.2.2 Voraussetzungen
- Python 3  
- `.env`  
- Backup-Log vorhanden 


**Abhängigkeiten**
- python-dotenv


#### 3.2.3 Ausführung
```bash  
cd ~/homelab/scripts/python  
python3 backup_log.py
```
#### 3.2.4 Benötigte Umgebungsvariablen

```env 
PFAD= 
BACKUP_PFAD=
```

#### 3.2.5 Ausgabe
- Datum des letzten Backups  
- Backup erfolgreich / fehlgeschlagen  
- Gesicherte Services  
- Bekannte Permission-Fehler  
- Unbekannte Permission-Fehler  
- Anzahl Backup-Verzeichnisse


#### 3.2.6 Hinweise
Bekannte Permission-Fehler (z. B. `logrotate` oder `letsencrypt`) werden separat behandelt und nicht als unbekannte Fehler gewertet.

### 3.2 backup_log.py
| Feld | Wert |
| - | - |
| Sprache | Python |
| Version | v0.1 |
| Status | ✅ Aktiv|
| Kategorie | Backup |

#### 3.2.1 Zweck
Analysiert das Backup-Log und erkennt Fehler.
#### 3.2.2 Voraussetzungen
- Python 3  
- `.env`  
- Backup-Log vorhanden 


**Abhängigkeiten**
- python-dotenv


#### 3.2.3 Ausführung
```bash  
cd ~/homelab/scripts/python  
python3 backup_log.py
```
#### 3.2.4 Benötigte Umgebungsvariablen

```env 
PFAD= 
BACKUP_PFAD=
```

#### 3.2.5 Ausgabe
- Datum des letzten Backups  
- Backup erfolgreich / fehlgeschlagen  
- Gesicherte Services  
- Bekannte Permission-Fehler  
- Unbekannte Permission-Fehler  
- Anzahl Backup-Verzeichnisse


#### 3.2.6 Hinweise
Bekannte Permission-Fehler (z. B. `logrotate` oder `letsencrypt`) werden separat behandelt und nicht als unbekannte Fehler gewertet.

### 3.3 add_service.py
| Feld | Wert |  
| - | - |  
| Sprache | Python |  
| Version | v0.4.0 |  
| Status |  ✅ Aktiv|  
| Kategorie | Automatisierung |

#### 3.3.1 Zweck
Unterstützt beim automatisierten Einrichten neuer Homelab-Services.

#### 3.2.2 Voraussetzungen

- Python 3
- `.env` mit den benötigten Variablen
- Uptime Kuma API erreichbar

**Abhängigkeiten:**
- uptime-kuma-api-v2
- python-dotenv
- requests

**Hinweis:** Es wird der Fork [`uptime-kuma-api-v2`](https://github.com/exaland/uptime-kuma-api-v2) verwendet — das Original-Paket `uptime-kuma-api` ist nicht vollständig kompatibel mit Uptime Kuma 2.x (siehe `troubleshooting/log.md`, 2026-07-08). Der Python-Import bleibt unverändert: `from uptime_kuma_api import UptimeKumaApi, MonitorType`.

#### 3.3.3 Ausführung
```bash
cd ~/homelab/scripts/python/add_service
python3 main.py --service <name> --port <port> [--dry-run]
```

#### 3.3.4 Benötigte Umgebungsvariablen
```env
KUMA_URL=
TARGET_IP=
KUMA_USERNAME=
KUMA_PASSWORD=

PIHOLE_API_URL= 
PIHOLE_PASSWORD= 
```
#### 3.3.5 Aktuell umgesetzt
- Uptime Kuma Monitor hinzufügen
- Duplikat-Prüfung (Name & URL)
- `--dry-run`-Modus

#### 3.3.6 Geplante Funktionen
- Pi-hole DNS-Eintrag anlegen  
- Nginx Proxy Manager Proxy Host erstellen  
- UFW-Port freigeben  
- Service-Log schreiben

## 4. Changelog

### 4.1 uptime_kuma.py
### 4.2 backup_log.py
### 4.3 add_service.py

#### 4.3.1 v0.1.0  
  
**Datum:** 2026-07-07  
  
- CLI mit `argparse` erstellt  
- Eingabevalidierung für Service-Name und Port  
- Simulation der Einrichtungsschritte  
- Einheitliche Konsolenausgabe  
- Erste Version veröffentlicht


#### 4.3.2  v0.2.0 
**Datum:** 2026-07-08 

**Neu** 
- Uptime-Kuma-API-Anbindung ergänzt
- Verbindung und Login zu Uptime Kuma umgesetzt 
- Monitor-Erstellung über `uptime-kuma-api-v2` integriert 

**Geändert**
- API-Bibliothek aufgrund eines Kompatibilitätsproblems mit Uptime Kuma 2.4.0 von `uptime-kuma-api` auf `uptime-kuma-api-v2` umgestellt.

**Details:** 
`troubleshooting/log.md` → `2026-07-08 Python: add_service.py kann keinen Uptime-Kuma-Monitor erstellen`

#### 4.3.3 v0.2.1
**Datum:** 2026-07-09

**Neu**
- Funktion zum Erstellen der Monitor-URL ergänzt.
- Abrufen vorhandener Uptime-Kuma-Monitore integriert.
- Prüfung auf bereits vorhandene Monitor-Namen und Monitor-URLs ergänzt.
- Validierung der benötigten Umgebungsvariablen (`.env`) ergänzt.

**Geändert**
- Monitor-Erstellung auf getrennte Parameter (`monitor_name`, `monitor_url`) umgestellt.
- Funktionen durch Docstrings ergänzt.
- Programmablauf für bessere Wartbarkeit überarbeitet.

**Verbessert**
- Doppelte Monitor-Erstellung wird verhindert.
- Service-Namen werden bei der Prüfung unabhängig von Groß- und Kleinschreibung verglichen.
- Fehlerbehandlung und Ablaufsteuerung weiter vereinheitlicht.


#### 4.3.4 v0.2.2
**Datum:** 2026-07-09

**Refactoring**
- Umstrukturierung von `add_service.py` in das Modul-Verzeichnis `add_service/`.
- Aufgeteilt in `main.py`, `parser.py`, `validation.py`, `output.py` und `uptime_kuma.py`.
- `validate_uptime_monitor` nach `validation.py` verschoben (reine Prüflogik ohne API-Kommunikation).
- Veralteten Hinweis „Simulation beendet“ aus `print_status()` entfernt.
- Funktionalität unverändert – erfolgreicher Testlauf einschließlich Duplikat-Erkennung durchgeführt.


#### 4.3.4 v0.2.3
**Datum:** 2026-07-09

**Neu**
- `--dry-run`-Modus ergänzt.
- Simuliert die Monitor-Erstellung, ohne Änderungen an Uptime Kuma vorzunehmen.
- Verbindung zu Uptime Kuma sowie Duplikat-Prüfung werden auch im Dry-Run vollständig ausgeführt.

**Geändert**
- `main.py` um den Dry-Run-Ablauf erweitert.
- Monitor-Erstellung wird nur außerhalb des Dry-Run-Modus ausgeführt.
- `print_status()` zeigt den aktiven Dry-Run-Modus an.
- Veraltete Liste der geplanten Schritte aus `print_status()` entfernt.
- `get_uptime_monitor` zu `get_uptime_monitors` umbenannt (Plural, da alle Monitore zurückgegeben werden).

**Behoben**
- Erfolgsmeldung „Monitor erfolgreich erstellt“ wurde im Dry-Run-Modus fälschlicherweise ausgegeben.


#### 4.3.5 v0.3.0
**Datum:** 2026-07-10

**Neu**
- Pi-hole REST-API in `add_service` integriert.
- `connect_to_pihole()` implementiert:
  - HTTP-Session (`requests.Session`) erstellt.
  - Authentifizierung über Pi-hole API.
  - HTTP-Status und Session-ID (SID) werden geprüft.
  - Authentifizierte Session wird für weitere API-Aufrufe bereitgestellt.
- `disconnect_from_pihole()` implementiert:
  - Pi-hole-Session wird serverseitig beendet.
  - HTTP-Status des Logout-Endpunkts wird geprüft.
  - Lokale HTTP-Session wird zuverlässig geschlossen.

**Geändert**
- `main.py` um Pi-hole-Verbindungsaufbau und Session-Management erweitert.
- `.env`-Validierung um Pi-hole-Konfigurationsvariablen ergänzt.
- Ressourcenverwaltung erweitert, sodass Uptime Kuma- und Pi-hole-Verbindungen beim Programmende oder Fehlerfall sauber beendet werden.

**Behoben**
- `disconnect_from_pihole()` konnte mit `AttributeError` abbrechen, wenn `session` `None` war (z. B. nach fehlgeschlagenem Verbindungsaufbau); Prüfung auf `None` am Funktionsanfang ergänzt.
- Fehlende `disconnect`-Aufrufe an mehreren `return`-Stellen in `main.py` ergänzt, damit bei Verbindungsfehlern bereits aufgebaute Verbindungen zu Uptime Kuma und Pi-hole sauber beendet werden.
- Logout auf den korrekten HTTP-Status `204 No Content` angepasst; erfolgreiche Sitzungsbeendigung wurde zuvor fälschlich als Fehler erkannt.

#### 4.3.6 v0.3.1
**Datum:** 2026-07-10

**Neu**
- `fetch_dns_records()` implementiert:
  - Local-DNS-Einträge über die Pi-hole REST-API abrufen.
  - HTTP-Status prüfen und DNS-Einträge zurückgeben.
- `parse_dns_record()` implementiert:
  - Pi-hole-DNS-Einträge in eine interne Datenstruktur (`dict`) umwandeln.
- `build_dns_records()` implementiert:
  - Aus allen Pi-hole-DNS-Einträgen eine strukturierte Liste (`list[dict]`) erstellen.
- Interne Datenstruktur für DNS-Einträge eingeführt:
  ```python
  {
      "ip": "192.168.2.x",
      "hostname": "pihole.home"
  }
  ```

**Geändert**
- `main.py` erweitert:
  - DNS-Einträge von Pi-hole abrufen.
  - API-Daten in das interne Datenmodell überführen.
- Pi-hole API-URL vereinfacht:
  - `.env` enthält jetzt die Basis-URL (`/api`).
  - API-Endpunkte werden direkt in den Funktionen ergänzt.

**Behoben**
- Reihenfolge der Pi-hole-Verarbeitung korrigiert:
  - DNS-Einträge werden nun vor dem Logout der Session abgerufen.
- API-Endpunkte vereinheitlicht und an die neue Basis-URL angepasst.
- Rückgabewert von `disconnect_uptime_kuma()` wird jetzt geprüft (war zuvor 
  inkonsistent zu `disconnect_from_pihole()`, wo dies bereits der Fall war).

#### 4.3.7 v0.3.2
**Datum:** 2026-07-12

**Neu**
- `validate_pihole_dns_records()` implementiert:
  - Prüft, ob ein Hostname bereits als Local-DNS-Eintrag in Pi-hole vorhanden ist.
  - Vergleich erfolgt unabhängig von Groß- und Kleinschreibung.
  - Verhindert das Anlegen doppelter Local-DNS-Einträge.
- `build_dns_hostname()` implementiert:
  - Erstellt aus einem Servicenamen den vollständigen DNS-Hostnamen.
- DNS-Validierung in den Programmablauf (`main.py`) integriert.

**Geändert**
- `validate_env()` um die Pi-hole-Konfigurationsvariablen erweitert:
  - `PIHOLE_API_URL`
  - `PIHOLE_PASSWORD`
- Einheitliche Erstellung von DNS-Hostnamen über `build_dns_hostname()`.
- Dry-Run berücksichtigt nun die erfolgreiche DNS-Validierung.
- Dry-Run-Meldung präzisiert: zeigt jetzt explizit „Uptime-Kuma Monitor" an.


#### 4.3.8 v0.3.3
**Datum:** 2026-07-12

**Neu**
- `add_local_dns_record()` implementiert:
  - Erstellt Local-DNS-Einträge über die Pi-hole REST-API.
  - Verwendet den HTTP-Endpunkt `PUT /config/dns/hosts/{record}`.
  - Prüft den erwarteten Status `201 Created`.
- Pi-hole-DNS-Erstellung in den Programmablauf integriert.
- Dry-Run um die geplante Erstellung des Pi-hole-DNS-Eintrags erweitert.

**Geändert**
- `TARGET_IP` enthält nur noch die reine IP-Adresse.
- `build_monitor_url()` ergänzt das URL-Schema für Uptime-Kuma-Monitore.
- Erfolgs- und Dry-Run-Ausgaben für Uptime Kuma und Pi-hole getrennt dargestellt.
- Erstellung läuft sequenziell (erst Uptime Kuma, dann Pi-hole), um bei Fehlern 
  inkonsistente Zwischenzustände zu vermeiden.

**Verifikation**
- Uptime-Kuma-Monitor erfolgreich erstellt.
- Pi-hole-Local-DNS-Eintrag erfolgreich angelegt.
- Beide API-Verbindungen anschließend sauber beendet.


#### 4.3.9 v0.4.0
**Datum:** 2026-07-13

**Neu**
- `try/finally` für zentrales Ressourcenmanagement in `main.py` eingeführt.
  - Verbindungsaufbau, Prüfung und der gesamte Programmablauf laufen jetzt innerhalb eines `try`-Blocks.
  - Beide Verbindungen (Uptime Kuma, Pi-hole) werden im `finally`-Block garantiert getrennt – unabhängig davon, an welcher Stelle das Programm beendet wird.

**Geändert**
- Wiederholte `disconnect_uptime_kuma()`- und `disconnect_from_pihole()`-Aufrufe an den einzelnen `return`-Stellen entfernt; das Cleanup erfolgt jetzt zentral im `finally`.
- `disconnect_uptime_kuma()` um eine `None`-Prüfung ergänzt (analog zu `disconnect_from_pihole()`), damit die Funktion auch dann sicher ausgeführt werden kann, wenn die Verbindung nie erfolgreich aufgebaut wurde.

**Verifikation**
- Erfolgreichen Programmablauf mit beiden API-Verbindungen getestet.
- Kritischen Fehlerfall getestet: Uptime-Kuma-Verbindung schlägt fehl (falsches Passwort), Pi-hole-Verbindung wurde bereits erfolgreich aufgebaut → beide Ressourcen werden trotzdem sauber freigegeben, kein Absturz.