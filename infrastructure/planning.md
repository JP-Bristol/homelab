# Homelab Infrastruktur Planung

## Zielzustand

Beschreibung der geplanten Homelab Architektur. 

---
## 1. Hardware

| Gerät | Codename | Status | Rolle |  
|-|-|-|-|  
| Raspberry Pi 5 | Arasaka | vorhanden | Core Services |  
| Raspberry Pi 5| Trauma Team | geplant | Monitoring |  
| Raspberry Pi 5| Militech | geplant | Dokumentation & Files |  
| Raspberry Pi 5| Netrunner | geplant | Experimente & Dev|  
| OptiPlex Mini-PC | Mikoshi | geplant | Virtualisierung & AI |  
| PoE Switch | Afterlife | geplant | Netzwerk |  
| Touch Display | Delamain | geplant | Dashboard |
| NAS (später) | Crystal Palace  | geplant | Storage |


## 2. Service Verteilung:

### 2.1 Pi 1 - Arasaka (Aktiv)

| Service | Zweck | Status |
|-|-|-|
|Pi-hole| DNS & Adblocker|✅ läuft|
|Nginx Proxy Manager| Reverse Proxy|✅ läuft|
|Vaultwarden| Passwortmanager|✅ läuft|
|Uptime Kuma| Monitoring|✅ läuft|
|UFW| Firewall|✅ aktiv|
|fail2ban| Brute-Force-Schutz|✅ aktiv|

### 2.2 Pi 2 — Trauma Team (Geplant)

| Service | Zweck | Status |
|-|-|-|
| Uptime Kuma | Monitoring | 🔲 Migration von Arasaka |
| Zabbix | Monitoring | 🔲 geplant |
| Grafana | Dashboards | 🔲 geplant |
| Touch Dashboard | Eigenes Monitoring Display | 🔲 geplant |

### 2.3 Pi 3 - Militech (Geplant)

| Service | Zweck | Status |
|-|-|-|
| Wiki.js | Knowledge Management | 🔲 Migration von Arasaka |
| Paperless-ngx | Dokumenten-Management | 🔲 geplant |
| Nextcloud | Self-hosted Storage | 🔲 geplant |

### 2.4 Pi 4 - (Name TBD) (Geplant)
| Service | Zweck | Status |
|-|-|-|
| Gitea | Self-hosted Git | 🔲 geplant |
| n8n | Automatisierung | 🔲 geplant |
| Testumgebungen | Experimente & Dev| 🔲 geplant |

### 2.5 Optiplex - (Name TBD)  (Geplant) 
| Workload | Zweck | Status |
|-|-|-|
| Windows Server VM | Active Directory, GPO | 🔲 geplant |
| Linux VM | Experimente | 🔲 geplant |
| KI-Workspace | Lokale LLMs & Automatisierung | 🔲 geplant |


## 3. Netzwerk Zielstuand

### 3.1 Geplante Komponenten 
```text  
	 Internet  
		|  
	  Router  
		|  
	PoE Switch  
		|  
+-----------------+  
| 4x Raspberry Pi |  
+-----------------+   
		|  
		|  
	OptiPlex
```

### 3.2 Dienste

-   Lokaler DNS über Pi-hole
-   Reverse Proxy über Nginx Proxy Manager
-   VPN Zugriff über WireGuard (langfristig)

## 4. Migrationsplan

### 4.1 Phase 1 - Basis Homelab

Status:  
Aktiv

-   Raspberry Pi 5
-   Docker
-   Backup-System
-   Pi-hole
-   Monitoring Basis

### 4.2 Phase 2 - Erweiterung

Status:  
Geplant

-   Zweiter Raspberry Pi
-   Monitoring Stack
-   Netzwerksegmentierung

### 4.3 Phase 3 - Server Integration

Status:  
Geplant

-   OptiPlex
-   Proxmox
-   AI Services
