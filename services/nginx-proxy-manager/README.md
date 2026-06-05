# Service Runbook: Nginx Proxy Manager
Nginx Proxy Manager Der Nginx Proxy Manager ist eine Anwendung, 
die es ermöglicht, Web-Anfragen aus dem Internet über eine grafische Oberfläche 
sicher an verschiedene Server oder Dienste im Heimnetzwerk weiterzuleiten 
und dabei automatisch kostenlose SSL-Zertifikate (HTTPS) zu verwalten

## 1. System-Übersicht
 - Dienst: Service Runbook: Nginx Proxy Manager
 - Host-System: Raspberry Pi 5
 - IP-Adresse: 192.168.2.xx
 - Web-Interrface http://192.168.2.xx:81
 - Installationsart: Docker Compose

## 2. Standard-Befehle (Betrieb)
Alle Befehle müssen im Verzeichnis der docker-compose.yml ausgeführt werden.

Starten: docker compose up -d
Stoppen: docker compose down
Neu Starten: docker compose restart nginx-proxy-manager
Logs anschauen: docker logs nginx-proxy-manager

## 3.  Update & Wartung
Um Nginx Proxy Manager auf den neusten Version zu aktualisieren, folgende Befehle nacheinander ausführen

docker compose pull
docker compose down
docker compose up -d

## 4. Eingerichtete Proxy Hosts
| Domain | Ziel | Port |
|--------|------|------|
| pihole.home | 192.168.2.x | 8080 |
| uptime.home | 192.168.2.x | 3001 |
| npm.home | 192.168.2.x | 81 |

## 5. Bekannte Probleme
- Pihole v6 blockt Root-Pfad → 403 Error
  Fix: Custom Location in NPM anlegen, Forward Path auf /admin setzen
  Weitere Details: troubleshooting/log.md
