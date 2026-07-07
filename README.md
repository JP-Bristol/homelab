## Homelab
Mein Homelab – Lernprojekt gestartet im Mai 2026.

Ziel: Aufbau einer selbstverwalteten Home-Infrastructure mit Fokus auf Docker, Networking und DevOps-Grundlagen.

## Ziel des Projekts
-   Docker & Container-Management lernen
-   Netzwerkverständnis aufbauen (DNS, Reverse Proxy)
-   Infrastruktur wie in Production-Systemen strukturieren
-   Automatisierung & Backups implementieren

## Infrastruktur

Die Infrastruktur basiert auf einer Docker-Umgebung auf einem Raspberry Pi 5 und wird kontinuierlich erweitert. Ziel ist ein möglichst praxisnaher Aufbau mit Fokus auf Betrieb, Dokumentation und Automatisierung.

### Container & Virtualisierung

-   Docker
-   Docker Compose

### Netzwerk

-   Pi-hole (DNS & lokales Namensmanagement)
-   Nginx Proxy Manager (Reverse Proxy)

### Monitoring

-   Uptime Kuma
-   Zukünftig: Zabbix

### Dokumentation & Wissensmanagement

-   Wiki.js
-   Runbooks
-   Troubleshooting-Log

### Sicherheit

-   UFW (Firewall)
-   Fail2ban

### Daten & Synchronisation

-   Syncthing
-   Backup-System (Cron + USB/NVMe)

### Automatisierung

-   Python-Skripte
-   Bash-Skripte
-   Runbook Agent (in Planung)

## Dokumentation  
  
Die Infrastruktur wird vollständig dokumentiert und über Runbooks, Service-Dokumentationen und Troubleshooting-Protokolle gepflegt.  
  
### Services  
- Pi-hole  
- Uptime Kuma  
- Nginx Proxy Manager  
- Wiki.js  
- Vaultwarden  
- Syncthing  
  
### Runbooks  
- First Boot  
- Backup & Restore  
- SSD Migration  
  
### Infrastruktur  
- DNS  
- Netzwerkübersicht  
- Firewall  
- Security Hardening  
- Infrastrukturplanung  
  
### Troubleshooting  
- Zentrales Fehler- und Lösungsprotokoll  
  
### Automatisierung  
- Python-Skripte inkl. Changelog und Dokumentation


## Services

| Service | Kategorie | Port | Status | Dokumentation |  
|---|---|---:|---|---|  
| Pi-hole | DNS | 53 / 80 | ✅ Aktiv | `services/pihole/` |  
| Uptime Kuma | Monitoring | 3001 | ✅ Aktiv | `services/uptime-kuma/` |  
| Nginx Proxy Manager | Reverse Proxy | 81 | ✅ Aktiv | `services/nginx-proxy-manager/` |  
| Wiki.js | Dokumentation | 3000 | ✅ Aktiv | `services/wikijs/` |  
| Vaultwarden | Security | 11001 | ✅ Aktiv | `services/vaultwarden/` |  
| Syncthing | Sync | 8384 | ✅ Aktiv | `services/syncthing/` |

Jeder produktive Service besitzt eine eigene Dokumentation, einschließlich Konfiguration, Backup-Hinweisen, Troubleshooting und relevanten Runbooks.

## Hardware
| Gerät | Funktion | Details | Seit |
| - | - | - | - |
| Raspberry Pi 5 | Host-System | 8 GB RAM | 2026-05 |
| microSD-Karte | Boot-Medium | Raspberry Pi OS | 2026-05 |
| NVMe SSD | Primärer Speicher | Verbatim Vi3000 256 GB | 2026-06 |
| USB-Stick | Backup-Ziel | 32 GB | 2026-06 |


## Projektstatus  
  
🟢 Aktiv  
  
**Aktuelle Schwerpunkte**  
  
- Dokumentation & Runbooks  
- Python-Automatisierung  
- Monitoring  
- Repository-Optimierung  
  
**Nächster Meilenstein**  
  
- `add_service.py v0.2.0`


## 🚀 Roadmap

### Aktueller Fokus

-   Repository aufräumen und Dokumentation vereinheitlichen
-   Python-Automatisierung für das Homelab weiterentwickeln
-   `add_service.py` bis zur produktiven Version ausbauen
-   Wiki.js als zentrale Wissensbasis erweitern

----------

### Kurzfristig

-   `add_service.py`
    -   v0.2 – Uptime Kuma API (Monitor automatisch anlegen)
    -   v0.3 – Pi-hole DNS-Eintrag automatisch erstellen
    -   v0.4 – Nginx Proxy Manager Proxy Host erstellen
    -   v0.5 – UFW-Port automatisch freigeben
    -   v1.0 – Vollständige Service-Automatisierung
-   Zabbix in das Monitoring integrieren
-   `ufw-setup.sh` entwickeln
-   Syncthing auf dem iPhone einrichten

----------

### Mittelfristig

-   VPN einrichten
-   Zweiten Raspberry Pi integrieren
-   Dedizierte Server (Proxmox, Windows Server, KI-Workspace)
-   Troublelog-Generator mit Claude API entwickeln
-   Weboberfläche für den Troublelog-Generator (FastAPI)

----------

### Langfristig

-   Touch Dashboard für den Homelab-Betrieb
-   Self-hosted KI-Workspace
-   Nextcloud
-   Lokale GPU für KI-Anwendungen
-   Runbook Agent zur automatischen Erstellung und Pflege von Betriebsdokumentation

## Repo-Struktur
``` 
homelab/
├── README.md
├── hardware/
│   └── inventory.md
├── infrastructure/
│   ├── network/
│   ├── security/
│   ├── maintenance.md
│   └── planning.md
├── runbooks/
│   ├── backup-restore.md
│   ├── first-boot.md
│   └── ssd-migration.md
├── scripts/
│   ├── backup.sh
│   └── python/
│       ├── README.md
│       ├── add_service.py
│       ├── backup_log.py
│       ├── requirements.txt
│       └── uptime_api.py
├── services/
│   ├── nginx-proxy-manager/
│   ├── pihole/
│   ├── syncthing/
│   ├── uptime-kuma/
│   ├── vaultwarden/
│   └── wikijs/
└── troubleshooting/
    └── log.md

```
