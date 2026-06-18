## Firewall Management

### 1. Ziel
Verwaltung der Host-Firewall des Raspberry Pi.  
Die Firewall reduziert die Angriffsfläche, indem nur benötigte Netzwerkzugriffe erlaubt werden.

### 2. Technologie
Firewall:
- UFW (Uncomplicated Firewall)
Prinzip:
- Default Deny Incoming  
- Default Allow Outgoing

### 3. Aktuelle Regeln
| Port | Service | Zweck |  
|-|-|-|  
|22/tcp|SSH|Administration|  
|53/tcp|Pi-hole|DNS|  
|53/udp|Pi-hole|DNS|  
|81/tcp|Nginx Proxy Manager|Management UI|  
|80/tcp|Nginx Proxy Manager|HTTP Reverse Proxy|  
|443/tcp|Nginx Proxy Manager|HTTPS Reverse Proxy|  
|3000/tcp|Wiki.js|Dokumentation|  
|3001/tcp|Uptime Kuma|Monitoring|  
|8080/tcp|Pi-hole|Web UI|

### 4. Firewall Regeln setzen
#### 4.1. SSH Administration
```bash 
sudo ufw allow ssh
```
#### 4.2. Pi-hole DNS  
```bash 
sudo ufw allow 53/tcp  
sudo ufw allow 53/udp  
```
#### 4.3. Pi-hole Web UI  
```bash 
sudo ufw allow 8080/tcp  
``` 
#### 4.4. Wiki.js 
```bash 
sudo ufw allow 3000/tcp  
```
#### 4.5. Uptime Kuma  
```bash 
sudo ufw allow 3001/tcp  
```  
#### 4.6. Nginx Proxy Manager  
```bash 
sudo ufw allow 81/tcp  
sudo ufw allow 80/tcp  
sudo ufw allow 443/tcp
```
**Hinweis:**
`Die Ports 80/443 werden nur benötigt, wenn Nginx Proxy Manager als Reverse Proxy verwendet wird. Für die reine Weboberfläche ist nur Port 81 notwendig.`


### 5. Status prüfen 
```bash  
sudo ufw status verbose
```

### 6. Port hinzufügen
Beispiel:
```bash  
sudo ufw allow 9000/tcp comment "Neuer Service"
```

### 7. Port entfernen
Beispiel:
```bash  
sudo ufw delete allow 9000/tcp
```

## 8. Aktive Verbindungen prüfen
```bash  
sudo ss -tulpn
```

## 9. Externe Prüfung
Von einem anderen Gerät im LAN:
```bash  
nmap 192.168.2.x
```
