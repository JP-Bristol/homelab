# Homelab Scripts
Kurze Übersicht aller eigenen Automatisierungs- und Monitoring-Skripte im Homelab.
## 1. Übersicht
| Script | Zweck | Ausführung | Status |  
|---|---|---|---|  
| `uptime_kuma.py` | Service-Status aus Uptime Kuma anzeigen | `python3 uptime_kuma.py` | ✅ v0.1 |  
| `backup_log.py` | Backup-Log auswerten | `python3 backup_log.py` | ✅ v0.1 |  
| `add_service/` | Neuen Service vorbereiten | `python3 add_service/main.py` | ✅ v0.6.3 |

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
| Version | v0.6.3 |  
| Status |  ✅ Aktiv|  
| Kategorie | Automatisierung |

**Vollständiger Changelog:** siehe [`add_service/CHANGELOG.md`](add_service/CHANGELOG.md)

#### 3.3.1 Zweck
Unterstützt beim automatisierten Einrichten neuer Homelab-Services.

#### 3.3.2 Voraussetzungen

- Python 3
- `.env` mit den benötigten Variablen
- Uptime Kuma API erreichbar

**Abhängigkeiten:**
- uptime-kuma-api-v2
- python-dotenv
- requests


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
- Pi-hole DNS-Eintrag anlegen (inkl. Duplikat-Prüfung)
- Duplikat-Prüfung (Name & URL / Hostname)
- `--dry-run`-Modus
- Zentrales Ressourcen-Management (`try/finally`)
- Strukturierte Konfiguration (`config.py`)
- Einheitliche Datenstrukturen für Kuma-Monitore und Pi-hole-DNS-Einträge
- Ausgabe-Helper & Business-Logik entkoppeln (v0.4.3)
- Fehlerbehandlung verfeinern (v0.4.4)

#### 3.3.6 Geplante Funktionen
- Namenskonventionen vereinheitlichen (v0.4.5)
- Service-Log implementieren (v0.5.0)
- Nginx Proxy Manager Proxy Host erstellen (v0.6.x)
- UFW-Port freigeben (v0.7.x)

#### 3.3.7 Hinweis
Es wird der Fork [`uptime-kuma-api-v2`](https://github.com/exaland/uptime-kuma-api-v2) verwendet — das Original-Paket `uptime-kuma-api` ist nicht vollständig kompatibel mit Uptime Kuma 2.x (siehe `troubleshooting/log.md`, 2026-07-08). Der Python-Import bleibt unverändert: `from uptime_kuma_api import UptimeKumaApi, MonitorType`.