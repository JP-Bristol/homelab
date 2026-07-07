## Homelab
Mein Homelab – Lernprojekt gestartet im Mai 2026.

Ziel: Aufbau einer selbstverwalteten Home-Infrastructure mit Fokus auf Docker, Networking und DevOps-Grundlagen.

## Ziel des Projekts
-   Docker & Container-Management lernen
-   Netzwerkverständnis aufbauen (DNS, Reverse Proxy)
-   Infrastruktur wie in Production-Systemen strukturieren
-   Automatisierung & Backups implementieren

## Hardware 
| Gerät | Details | Seit |
|  --------  |  -------  | --------  | 
| Raspberry Pi 5 | 8 GB RAM |2026-05 |
| Storage | SD-Karte | 2026-05 |
| USB-Stick | 32 GB Backup-Speicher | 2026-06 |
| NVMe SSD | Verbatim Vi3000 256GB | 2026-06 |

## Services

| Service | Port | Status | Beschreibung |
|  --------  |  -------  | --------  |  -------  |
| Pi-hole | 53 / 80 |✅ läuft | DNS & Adblocker |
| Uptime Kuma | 3001 |✅ läuft | Monitoring & Alerts |
| Nginx Proxy Manager | 81 |✅ läuft | Reverse Proxy |
| Wiki.js | 3000 |✅ läuft | Dokumentation & Wissensmanagement |
| Vaultwarden | 11001 | ✅ läuft | Passwortmanager |
| Syncthing | 8384 | ✅ läuft | Datei-Synchronisation |

##  Infrastruktur Stack
-   Docker
-   Docker Compose
-   DNS (Pi-hole)
-   Reverse Proxy
-   Monitoring
-   Wiki.js
-   Vaultwarden
-   Security Hardening (ufw, fail2ban)
-   Syncthing 

## Status
-   Woche 1 - 6: abgeschlossen 
-   Nächste Schritte: Python Grundlagen, Zabbix, Repo-Aufräum-Tag, VPN

## Aktuell aktiv

- Pi-hole (DNS & Adblocker)
- Uptime Kuma (Monitoring)
- Nginx Proxy Manager (Reverse Proxy)
- Backup-System (USB + Cron)
- Wiki / Dokumentation
- Vaultwarden (Passwortmanager)
- Security Hardening (ufw, fail2ban) 
- NVMe SSD Migration
- Lokale DNS-Einträge
- Syncthing (Datei-Synchronisation)
- Obsidian (Notizen via Syncthing) 

## Geplant

**Kurzfristig**
- Repo-Aufräum-Tag
- Syncthing iPhone einrichten
- Automatisierungs-Script (DNS + NPM + Uptime Kuma)
- Zabbix (Monitoring)
- Python - Grundlagen + Homelab-Scripts
- Security Script (ufw-setup.sh)
- Wiki befüllen
- Automatisierungs-Script (DNS + NPM + Uptime Kuma)

**Mittelfristig (mit Hardware)**
- Dedizierte Server (Proxmox, Windows Server, KI-Workspace)
- Zweiter Pi
- VPN
- Troublelog-Generator (Claude API + Few-Shot Prompting)
- Troublelog-Generator Web GUI (FastAPI + HTML)

**Langfristig**
- Touch Dashboard
- Self-hosted KI-Workspace
- Nextcloud
- GPU für lokale KI
- Runbook-Generator Agent (Wiki.js + Claude API + Chroma)

## Dokumentation
-   `services/pihole/README.md`
-   `services/uptime-kuma/README.md`
-   `services/nginx-proxy-manager/README.md`
-   `services/wikijs/README.md`
-   `services/vaultwarden/README.md`
-   `services/syncthing/README.md`
-   `runbooks/first-boot.md`
-   `runbooks/backup-restore.md`
-   `runbooks/ssd-migration.md`
-   `infrastructure/network/dns.md`
-   `infrastructure/network/network-overview.md`
-   `infrastructure/security/hardening.md`
-   `infrastructure/security/firewall.md`
-   `infrastructure/planning.md`

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
