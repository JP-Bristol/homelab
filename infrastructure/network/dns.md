# DNS-Konfiguration

| Metadatum | Wert |
|---|---|
| Dokumentstatus | `AKTIV` |
| Infrastrukturkomponente | DNS |
| Primärer DNS-Dienst | Pi-hole |
| Aktiver Upstream-Resolver | Quad9 |
| Verantwortlich | `TODO` |
| Letzte technische Prüfung | `TODO – nach vollständiger Prüfung setzen` |

---

## 1. Zweck

Dieses Dokument beschreibt die DNS-Infrastruktur des Homelabs.

Ziel ist es, den primären DNS-Dienst, den verwendeten Upstream-Resolver, die DNS-Verteilung an Clients sowie die lokalen Namensauflösungen nachvollziehbar zu dokumentieren.

---

## 2. DNS-Architektur

```text
Clients
   |
   v
Pi-hole
192.168.2.x:53
   |
   v
Quad9
9.9.9.9
```

Pi-hole dient als zentraler DNS-Filter und DNS-Forwarder für das lokale Netzwerk.

DNS-Anfragen der Clients werden zunächst an Pi-hole gesendet. Externe Anfragen, die nicht lokal beantwortet werden können, leitet Pi-hole an Quad9 weiter.

---

## 3. Primärer DNS-Server

| Eigenschaft | Wert |
|---|---|
| Dienst | Pi-hole |
| Host | Raspberry Pi 5 `Arasaka` |
| IP-Adresse | `192.168.2.x` |
| Port | `53/TCP` und `53/UDP` |
| Rolle | Lokaler DNS-Filter und DNS-Forwarder |
| Service-Pfad | `~/homelab/services/pihole/` |

---

## 4. Upstream-DNS-Server

Pi-hole leitet externe DNS-Anfragen an folgenden Upstream-Resolver weiter:

| Anbieter | DNS-Server | Status |
|---|---|---|
| Quad9 | `9.9.9.9` | Aktiv |

Cloudflare und Google DNS werden aktuell nicht als Upstream-Resolver verwendet.

---

## 5. DNS-Clients

| Gerätetyp | DNS-Server |
|---|---|
| Raspberry Pis | Pi-hole |
| Desktop-PC | Pi-hole |
| Laptop | Pi-hole |
| Smartphone | Pi-hole |
| Tablet | Pi-hole |

Die DNS-Konfiguration wird aktuell auf den einzelnen Clients manuell vorgenommen.

Eine zentrale Verteilung der Pi-hole-Adresse als DNS-Server über DHCP ist mit der eingesetzten EasyBox derzeit nicht möglich beziehungsweise funktioniert in der vorhandenen Konfiguration nicht zuverlässig.

Voraussetzung für die lokale Namensauflösung und DNS-Filterung ist daher, dass Pi-hole auf jedem Client manuell als DNS-Server eingetragen wird.

```text
TODO: DNS-Verteilung erneut prüfen, falls der Router ersetzt oder ein eigener DHCP-Server eingerichtet wird.
```

---

## 6. Lokale DNS-Einträge

### 6.1 Host-Records

| Hostname | IP-Adresse |
|---|---|
| `pihole.home` | `192.168.2.x` |
| `uptime.home` | `192.168.2.x` |
| `npm.home` | `192.168.2.x` |
| `wiki.home` | `192.168.2.x` |
| `vaultwarden.home` | `192.168.2.x` |
| `syncthing.home` | `192.168.2.x` |

Die Hostnamen sind als Local DNS Records in Pi-hole hinterlegt.

Eine manuelle Konfiguration der lokalen `hosts`-Datei auf den Clients ist dadurch nicht erforderlich.

### 6.2 Zusammenspiel mit Nginx Proxy Manager

Die Local DNS Records in Pi-hole lösen die Hostnamen auf die IP-Adresse des Reverse-Proxy-Hosts auf.

Nginx Proxy Manager wertet anschließend den Hostnamen der HTTP- oder HTTPS-Anfrage aus und leitet die Anfrage an den jeweiligen internen Service weiter.

```text
Client
   |
   | DNS-Anfrage: vaultwarden.home
   v
Pi-hole
   |
   | Antwort: 192.168.2.x
   v
Nginx Proxy Manager
   |
   | Weiterleitung anhand des Hostnamens
   v
Vaultwarden
```

DNS übernimmt dabei ausschließlich die Namensauflösung. Die Weiterleitung an den jeweiligen internen Service erfolgt durch Nginx Proxy Manager.

---

## 7. Verifikation

### 7.1 Verwendeten DNS-Server prüfen

Auf einem Client prüfen, welcher DNS-Server verwendet wird.

Linux:

```bash
resolvectl status
```

Windows:

```powershell
ipconfig /all
```

Erwartung:

```text
DNS-Server: 192.168.2.x
```

### 7.2 Pi-hole direkt abfragen

```bash
dig @192.168.2.x vaultwarden.home
```

Alternativ:

```bash
nslookup vaultwarden.home 192.168.2.x
```

Erwartete Antwort:

```text
vaultwarden.home. IN A 192.168.2.x
```

Der antwortende DNS-Server muss die IP-Adresse von Pi-hole sein.

### 7.3 Reguläre Namensauflösung prüfen

```bash
dig vaultwarden.home
```

Erwartung:

- der verwendete DNS-Server ist Pi-hole
- `vaultwarden.home` wird auf `192.168.2.x` aufgelöst

### 7.4 Externe DNS-Auflösung prüfen

```bash
dig @192.168.2.x example.com
```

Erwartung:

- Pi-hole beantwortet die Anfrage
- externe Domains werden über Quad9 aufgelöst

### 7.5 Weboberflächen und Reverse Proxy prüfen

Im Browser öffnen:

```text
http://pihole.home/admin
http://uptime.home
http://npm.home
http://wiki.home
http://vaultwarden.home
http://syncthing.home
```

Erwartung:

- alle Hostnamen werden erfolgreich aufgelöst
- die jeweiligen Weboberflächen sind erreichbar
- die HTTP- oder HTTPS-Weiterleitung erfolgt über Nginx Proxy Manager

Ein erfolgreicher DNS-Test bestätigt nur die Namensauflösung. Die Erreichbarkeit der Weboberfläche hängt zusätzlich von Nginx Proxy Manager und dem jeweiligen Zielservice ab.

---

## 8. Bekannte Störungen und Diagnose

### 8.1 Schnellübersicht

| Störung | Erste Prüfung | Troublelog |
|---|---|---|
| Lokale Domain wird nicht aufgelöst | verwendeten DNS-Server und Local DNS Record prüfen | [2026-06-06 – Fehler Domainauflösung in Uptime Kuma](../../troubleshooting/log.md) |
| Container kann externe Domains nicht auflösen | DNS-Konfiguration und Erreichbarkeit von Quad9 prüfen | [2026-05-28 – Uptime Kuma: Keine Discord-Benachrichtigung (DNS-Fehler)](../../troubleshooting/log.md) |
| Raspberry Pi verwendet die EasyBox statt Pi-hole als DNS-Server | aktiven DNS-Server und NetworkManager-Verbindung prüfen | [2026-06-06 – Raspberry Pi nutzt noch den DNS-Server der EasyBox](../../troubleshooting/log.md) |
| EasyBox verteilt Pi-hole nicht zuverlässig per DHCP | DHCP- und DNS-Konfiguration des Routers sowie den DNS-Server des Clients prüfen | [2026-05-26 – EasyBox 803 verteilt DNS nicht an Geräte](../../troubleshooting/log.md) |

### 8.2 Basisdiagnose

In das Pi-hole-Serviceverzeichnis wechseln:

```bash
cd ~/homelab/services/pihole
```

Containerstatus prüfen:

```bash
docker compose ps
```

Logs prüfen:

```bash
docker compose logs --tail 100 pihole
```

Pi-hole-Status prüfen:

```bash
docker compose exec pihole pihole status
```

Port 53 prüfen:

```bash
sudo ss -tulpn | grep :53
```

Quad9 direkt testen:

```bash
dig @9.9.9.9 example.com
```

Pi-hole lokal testen:

```bash
dig @127.0.0.1 example.com
```

### 8.3 Häufige Ursachen

- Pi-hole-Container läuft nicht
- Port `53/TCP` oder `53/UDP` ist nicht verfügbar
- Client verwendet nicht Pi-hole als DNS-Server
- Router verteilt einen falschen DNS-Server
- Local DNS Record fehlt oder enthält eine falsche IP-Adresse
- Quad9 ist nicht erreichbar
- Firewall blockiert DNS-Anfragen
- Container verwendet eine fehlerhafte DNS-Konfiguration

Ausführliche Ursachen, Maßnahmen und Lessons Learned werden im zentralen Troublelog dokumentiert.

---

## 9. Verweise

### 9.1 Interne Dokumentation

- [Pi-hole-Service-Runbook](../../services/pihole/README.md)
- [Nginx-Proxy-Manager-Service-Runbook](../../services/nginx-proxy-manager/README.md)
- [Netzwerkübersicht](network-overview.md)
- [Zentrales Störungs- und Troublelog](../../troubleshooting/log.md)
- [Firewall-Dokumentation](../security/firewall.md)

### 9.2 Externe Dokumentation

TODO: Offizielle Pi-hole-Dokumentation verlinken.

TODO: Offizielle Quad9-Dokumentation verlinken.

---

## 10. Änderungsverlauf

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 2026-06 | Initiale Erstellung |
| 1.1 | 2026-06-27 | Lokale DNS-Einträge in Pi-hole eingerichtet; lokale `hosts`-Dateien sind nicht mehr erforderlich |
| 1.2 | 2026-07-29 | DNS-Architektur, Verifikation, Diagnose und manuelle DNS-Konfiguration der Clients dokumentiert |
