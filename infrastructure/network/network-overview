## Network Overview
**Zweck**
Dieses Dokument beschreibt die grundlegende Netzwerktopologie des Homelabs.

Ziel ist es, IP-Adressierung, Netzwerkgeräte und wichtige DHCP-Reservierungen nachvollziehbar zu dokumentieren.

### 1. Netzwerkübersicht

```
Internet
    │
    ▼
Router
192.168.2.1
    │
    ▼
Raspberry Pi 5
192.168.2.x
    │
    ├── Pi-hole
    ├── Uptime Kuma
    └── Nginx Proxy Manager
```

### 2. Netzwerk-Konfiguration
| Eigenschaft | Wert |
| - | - |
| Netzwerk | 192.168.2.0/24 |
| Subnetzmaske | 255.255.255.0 |
| Gateway | 192.168.2.1 |
| DHCP Server | Router |
| DNS Server | Pi-hole |

### 3. Router

| Eigenschaft | Wert |
| - | - |
| Gerät | EasyBox |
| IP-Adresse | 192.168.2.1 |
| Rolle | Gateway / DHCP |

### 4. DHCP Bereich 

| Einstellung | Wert |
| - | - |
| DHCP Start| 192.168.2.50 |
| DHCP Ende | 192.168.2.199 |

Gültigkeit der IP-Adresszuordnung: 2 Wochen

### 5. DHCP Reservierungen

| Gerät | IP-Adresse |
| - | - |
| Raspberry Pi 5| 192.168.2.x |
| EPSON Drucker | 192.168.2.x |

Hinweis:

Die Zuordnung erfolgt über die MAC-Adresse im Router.

### 6. Wichtige Systeme

| System | IP-Adresse | Zweck |
| - | - | - |
| Raspberry Pi 5| 192.168.2.x | Docker Host |
| Pi-hole | 192.168.2.x:8080 | DNS |
| Uptime Kuma | 192.168.2.x:3001 | Monitoring |
| Nginx Proxy Manager | 192.168.2.x:81 | Reverse Proxy |

### 7. Verifikation

#### 7.1 Gateway erreichbar:

```
ping -c 4 192.168.2.1
```

#### 7.2 Internet erreichbar:

```
ping -c 4 1.1.1.1
```

#### 7.3 DNS funktioniert:

```
nslookup google.com
```
