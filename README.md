# Homelab

Dieses Repository dokumentiert meinen praktischen Einstieg in die IT — aufgebaut auf einem Raspberry Pi 5, gewachsen durch echte Probleme und deren Lösungen.

## Projektbeschreibung

Das Homelab dient als persönliche Lern- und Entwicklungsumgebung mit Fokus auf Linux, Docker, Netzwerktechnik, Automatisierung und technischer Dokumentation.

Es ist ein langfristiges Projekt, mit dem ich praktische Erfahrungen beim Aufbau, Betrieb und der Automatisierung einer Self-Hosted-Infrastruktur sammle. Neben dem aktuellen Stand der Infrastruktur dokumentiert dieses Repository auch technische Entscheidungen, Änderungen und die kontinuierliche Weiterentwicklung der Umgebung.

## Kernziele & Kompetenzentwicklung

###  Infrastruktur & Systemarchitektur

-   **Linux & Docker:** Planung, Aufbau und Betrieb einer selbst verwalteten Docker-Umgebung mit Fokus auf Stabilität und Wartbarkeit.
    
-   **DevOps-Grundlagen:** Schrittweiser Aufbau von Kenntnissen in den Bereichen Monitoring, Backup-Strategien, Security-Hardening und Infrastruktur-Automatisierung.
    

### Automatisierung & Tool-Entwicklung

-   **Skripting:** Entwicklung von Python- und Shell-Skripten, um wiederkehrende administrative Aufgaben zu automatisieren.
    
-   **Eigene Werkzeuge:** Entwicklung eigener Tools – beispielsweise des Runbook Agents – zur Unterstützung von Betrieb und technischer Dokumentation.
    

### Dokumentation & Wissensmanagement

-   **Struktur:** Aufbau einer zentralen Wissensbasis mit Service-Dokumentationen, Runbooks und Troubleshooting-Guides.
    
-   **Nachvollziehbarkeit:** Technische Entscheidungen und Probleme (inkl. Lösungen) so zu dokumentieren, dass Konfigurationen, Entscheidungen und Arbeitsabläufe auch nach längerer Zeit nachvollzogen und reproduziert werden können.

## Infrastruktur

Die Infrastruktur basiert auf einer Docker-Umgebung auf einem Raspberry Pi 5 und wird kontinuierlich erweitert. Ziel ist ein möglichst praxisnaher Aufbau mit Fokus auf Betrieb, Dokumentation und Automatisierung.

### Container & Virtualisierung

-   Docker
-   Docker Compose

### Netzwerk

-   Pi-hole  (DNS, Adblocking & lokale Namensauflösung)
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
  
- `add_service.py v0.4.2` – Uptime-Kuma-Datenstruktur vereinheitlichen


## 🚀 Roadmap

### Aktueller Fokus

-   Repository aufräumen und Dokumentation vereinheitlichen
-   Python-Automatisierung für das Homelab weiterentwickeln
-   `add_service.py` bis zur produktiven Version ausbauen
-   Wiki.js als zentrale Wissensbasis erweitern

----------

### Kurzfristig

-   `add_service.py`
    -   (abgeschlossen) v0.2 – Uptime Kuma API (Monitor automatisch anlegen)
    -   (abgeschlossen) v0.3 – Pi-hole DNS-Eintrag automatisch erstellen
    -   (abgeschlossen) v0.4.0 – Ressourcenverwaltung (try/finally)
    -   (abgeschlossen) v0.4.1 – Konfiguration (load_env_config)
    -   v0.4.x – Datenstruktur, Ausgabe & Fehlerbehandlung vereinheitlichen
    -   v0.5.0 – Service-Log (Pipe-Format, Konsole + Log parallel, Basis für späteren Runbook-Agent-Parser)
    -   v0.6.x – Nginx Proxy Manager Proxy Host erstellen
    -   v0.7.x – UFW-Port automatisch freigeben
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
    -   `uptime_api.py` → eigenes Modul (Umbenennung + Modul-Ordner, sobald Dashboard-Anbindung startet)
    -   `backup_log.py` → eigenes Modul (analog)
    -   Architektur: getrennte Module pro Datenquelle, Dashboard bündelt nur die Daten, keine eigene API-Anbindung
-   Runbook Agent (eigenes Projekt-Repo, RAG mit Qdrant)
    -   Start: nach `add_service.py` v1.0
    -   Nutzt `service_log.txt` aus `add_service.py` als zusätzliche strukturierte Datenquelle
-   Self-hosted KI-Workspace
-   Nextcloud
-   Lokale GPU für KI-Anwendungen

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
│       ├── add_service/
│       │   ├── main.py
│       │   ├── parser.py
│       │   ├── output.py
│       │   ├── requirements.txt
│       │   ├── uptime_kuma.py
│       │   └── validation.py
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
