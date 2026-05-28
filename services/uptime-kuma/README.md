# Service Runbook: Uptime Kuma (self-hosted monitoring tool)
Uptime Kuma ist ein selbstgehostetes, einfach zu bedienendes Überwachungswerkzeug (Monitoring-Tool), das die Erreichbarkeit und Performance von Websites, Servern und Diensten in Echtzeit überprüft und bei Ausfällen Benachrichtigungen versendet.

## 1. System-Übersicht
 - Dienst: Service Runbook: Uptime Kuma (self-hosted monitoring tool)
 - Host-System: Raspberry Pi 5
 - IP-Adresse: 192.168.2.xx
 - Web-Interrface http://192.168.2.xx:3001
 - Installationsart: Docker Compose

## 2. Standard-Befehle (Betrieb)
Alle Befehle müssen im Verzeichnis der docker-compose.yml ausgeführt werden.

 - Starten: docker compose up -d
 - Stoppen: docker compose down
 - Neu Starten: docker compose restart uptime-kuma
 - Logs anschauen: docker logs uptime-kuma

## 3. Update & Wartung
Um Uptime Kuma auf den neusten Version zu aktualisieren, folgende Befehle nacheinander ausführen

 - docker compose pull 
 - docker compose down 
 - docker compose up -d

## 5. Anpassung in der `docker-compose.yml`

### Externer DNS
In der docker-compose.yml ist ein externer DNS-Server (9.9.9.9) eingetragen.
Grund: Wenn Pihole ausfällt kann Uptime Kuma sonst keine Discord-Benachrichtigungen schicken.
Ohne diesen Eintrag ist Uptime Kuma vom selben DNS abhängig den es überwacht. 

## 4. ## Bekannte Probleme

- Monitor zeigt 403 → URL auf /admin/login ändern
  Weitere Details: troubleshooting/log.md
- Wenn lokaler DNS-Server (z.B. Pi-hole) ausfällt, kann uptime Kuma keine Benachrichtung schicken.
  Weitere Detail: troubleshooting/log.md


