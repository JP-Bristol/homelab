## DNS Configuration
**Zweck**
Dieses Dokument beschreibt die DNS-Infrastruktur des Homelabs.

Ziel ist es, die verwendeten DNS-Server, Upstream-Resolver und lokalen Namensauflösungen nachvollziehbar zu dokumentieren.


### 1. DNS Architektur
```
Clients
    │
    ▼
Pi-hole
(192.168.2.x)
    │
    ▼
Upstream DNS
(Quad9)
```
### 2. Primärer DNS-Server

| Eigenschaften | Wert |
|-|-|
| Dienst | Pi-hole |
| Host | Raspberry Pi 5 |
| IP-Adresse | 192.168.2.x |
| Port | 53 TCP/UDP |
| Rolle | Lokaler DNS Resolver & Ad Blocker |

### 3. Upstream DNS Server
Pi-hole leitet DNS-Anfragen an folgende Upstream Resolver weiter:

| Anbieter | DNS Server |
|-|-|
| Quad9 | 9.9.9.9 |
| Cloudflare | 1.1.1.1 |
| Google DNS| 8.8.8.8 |

Aktiv verwendet:
```
Quad9 (9.9.9.9)
```
### 4. DNS Clients

| Gerät | DNS Server |
|-|-|
| Raspberry Pi | Pi-hole |
| Desktop PC | Pi-hole |
| Laptop| Pi-hole |
| Smartphone| Pi-hole |
| Tablet | Pi-hole |
DNS wird über DHCP bzw. manuelle Konfiguration verteilt.

### 5. Lokale DNS Einträge
#### 5.1 Host Records
| Hostname| IP-Adresse|
|-|-|
| pihole.home | 192.168.2.x:8080 |
| uptime.home | 192.168.2.x:3001 |
| npm.home| 192.168.2.x:81 |
**Hinweis:** Diese Domains sind in der hosts-Datei der Clients eingetragen und werden über Nginx Proxy Manager weitergeleitet:

### 6. Verifikation
DNS-Auflösung testen:

```
dig @192.168.2.xx google.com
```

Lokale Einträge testen:

```
nslookup pihole.home 192.168.2.x
```
**Hinweis:** NXDOMAIN erwartet, da pihole.home nicht in Pi-hole sondern nur in der hosts-Datei eingetragen ist.

### 7. Failure Scenarios

#### 7.1 DNS antwortet nicht
Prüfen:

```
docker logs pihole
```

```
docker exec pihole pihole status
```

Mögliche Ursachen:

-   Pi-hole Container gestoppt
-   Port 53 blockiert
-   Router verteilt falschen DNS
-   Upstream DNS nicht erreichbar

### 8. Änderungen
| Datum | Änderung |
|-|-|
| 2026-06 | Initiale Erstellung |

