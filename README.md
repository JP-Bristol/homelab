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


## Services

| Service | Port | Status | Beschreibung |
|  --------  |  -------  | --------  |  -------  |
| Pi-hole | 53 / 80 |✅ läuft | DNS & Adblocker |
| Uptime Kuma | 3001 |✅ läuft | Monitoring & Alerts |
| Nginx Proxy Manager | 81 |✅ läuft | Reverse Proxy |
| Wiki.js | 3000 |✅ läuft | Dokumentation & Wissensmanagement |
| Vaultwarden | 11001 | ✅ läuft | Passwortmanager |

##  Infrastruktur Stack
-   Docker
-   Docker Compose
-   DNS (Pi-hole)
-   Reverse Proxy
-   Monitoring


## Status
-   Woche 1 & 2: abgeschlossen 
-   Nächste Schritte: Security Hardening,Security Hardening, VPN

## Aktuell aktiv

- Pi-hole (DNS & Adblocker)
- Uptime Kuma (Monitoring)
- Nginx Proxy Manager (Reverse Proxy)
- Backup-System (USB + Cron)
- Wiki / Dokumentation
- Vaultwarden (Passwortmanager)

## Geplant
-   Monitoring Erweiterung
-   Security Hardening
-   Dedizierter Server (Virtualisierung, Windows Server, KI-Workspace)
-   Zweiter Pi
-   VPN

## Dokumentation
-   `services/pihole/README.md`
-   `services/uptime-kuma/README.md`
-   `services/nginx-proxy-manager/README.md`
-   `services/wikijs/README.md`
-   `runbooks/first-boot.md`
-   `runbooks/backup-restore.md`
-   `runbooks/ssd-migration.md`
-   `infrastructure/network/dns.md`
-   `infrastructure/network/network-overview.md`

## Repo-Struktur
``` 
homelab/
├── README.md
├── services/
│   ├── pihole/
│   ├── uptime-kuma/
│   └── nginx-proxy-manager/
│   └── wikijs/
├── runbooks/
│   ├── first-boot.md
│   └── backup-restore.md
├── scripts/
│   └── backup.sh
├── hardware/
│   └── inventory.md
├── infrastructure/
│   └── network/
│       ├── dns.md
│       └── network-overview.md
└── troubleshooting/
    └── log.md
```
