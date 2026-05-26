# Serive Runbook: Pi-hole (DNS & ADblocker)

Netzwerkweiter Werbeblocker und lokaler DNS-Server.
Blockiert Werbung und Tracking auf Netzwerkebene für alle Geräte.

## 1. System-Übersicht
 - Dienst: Pi-hole (Werbeblocker & locker DNS)
 - Host-System: Raspberry Pi 5
 - IP-Adresse: 192.168.2.xx
 - Web-Interrface http://192.168.2.XX/admin
 - Installationsart: Docker Compose

## 2 Standard-Befehle (Betrieb)
 Alle Befehle müssen im Verzeichnis der docker-compose.yml ausgeführt werden. 
 - Starten: docker compose up -d
 - Stoppen: docker compose down
 - Neu Starten: docker compose restart pihole
 - Logs anschauen: docker logs pihole
 - Passwort ändern: docker exec pihole pihole setpassword NEUESPASSWORT

## 3 Update & Wartung
Um Pi-Hole auf den neusten Version zu aktualisieren, folgende Befehle nacheinander ausführen
 - docker compose pull
   docker compose down
   docker compose up -d
## Bekannte Probleme
 - Passwort funktioniert nicht nach erstem Start 
  → docker exec pihole pihole setpassword PASSWORT
  
 - DNS antwortet nicht: dnsmasq ignoring query from non-local network
  → FTLCONF_dns_listeningMode: all in docker-compose.yml setzen

 - Easybox verteilt DNS nicht per DHCP
  → DNS manuell auf Endgeräten eintragen: 192.168.2.x

Weitere Details: troubleshooting/log.md 
