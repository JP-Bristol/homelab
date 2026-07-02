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
| pihole.home | 192.168.2.x |
| uptime.home | 192.168.2.x |
| npm.home | 192.168.2.x |
| wiki.home | 192.168.2.x |
| vaultwarden.home | 192.168.2.x |
| syncthing.home | 192.168.2.x |

**Hinweis:** 
Die Hostnamen sind als Local DNS Records in Pi-hole hinterlegt.

Voraussetzung ist, dass die Clients Pi-hole als DNS-Server verwenden. Eine manuelle Konfiguration der hosts-Datei auf den Clients ist dadurch nicht erforderlich.

Der Zugriff erfolgt über den jeweiligen Hostnamen. Die Weiterleitung auf den entsprechenden Service übernimmt der Nginx Proxy Manager.Domains sind als lokale DNS-Einträge direkt in Pi-hole hinterlegt.
Erreichbar automatisch von allen Geräten im Netzwerk — keine manuelle hosts-Datei Konfiguration nötig.
Ports werden über Nginx Proxy Manager weitergeleitet.

### 6. Verifikation

#### 6.1 DNS-Auflösung testen

```Bash
dig vaultwarden.home 
```

Erwartung:

```
;; SERVER: 192.168.2.x#53
```

```
;; ANSWER SECTION: 
vaultwarden.home. IN A 192.168.2.x
```

Der verwendete DNS-Server muss die Pi-hole-IP sein.

**Hinweis:**

Früher waren die Hostnamen ausschließlich in der Windows-hosts-Datei eingetragen.

Jetzt werden sie über die Local DNS Records in Pi-hole aufgelöst und stehen damit allen Geräten im Netzwerk zur Verfügung, sofern diese Pi-hole als DNS-Server verwenden.

#### 6.2 Ereichbarkeit pürfen

Im Browser öffnen:

`http://pihole.home/admin`
`http://uptime.home`
`http://npm.home`
`http://wiki.home`
`http://vaultwarden.home`
`http://syncthing.home`
Erwartung:

- Alle Hostnamen werden erfolgreich aufgelöst.
- Die jeweiligen Weboberflächen sind erreichbar.
- Die Weiterleitung erfolgt über den Nginx Proxy Manager.


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
| 2026-06-27 | Lokale DNS-Einträge in Pi-hole eingerichtet — hosts-Datei nicht mehr nötig |

