# Homelab Scripts
Kurze Übersicht aller eigenen Automatisierungs- und Monitoring-Skripte im Homelab.
## 1. Übersicht
| Script | Zweck | Ausführung | Status |  
|---|---|---|---|  
| `uptime_kuma.py` | Service-Status aus Uptime Kuma anzeigen | `python3 uptime_kuma.py` | ✅ v0.1 |  
| `backup_log.py` | Backup-Log auswerten | `python3 backup_log.py` | ✅ v0.1 |  
| `add_service.py` | Neuen Service vorbereiten | `python3 add_service.py` | 🔲 geplant |

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
| Version | v0.1.0 |  
| Status |  ✅ Aktiv|  
| Kategorie | Automatisierung |

#### 3.3.1 Zweck
Unterstützt beim automatisierten Einrichten neuer Homelab-Services.

#### 3.3.2 Geplante Funktionen
- Uptime Kuma Monitor hinzufügen  
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