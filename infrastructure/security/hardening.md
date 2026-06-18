## Security Hardening

### 1. Ziel
Absicherung des Raspberry Pi Homelab Hosts gegen typische Angriffe.

Maßnahmen:
- SSH-Brute-Force-Schutz
- Firewall-Regeln
- Minimierung offener Netzwerkdienste
- Regelmäßige Überprüfung der Systemkonfiguration

### 2. Security Architektur
#### 2.1 Netzwerkmodell
Das Homelab befindet sich hinter dem Heimrouter und ist aktuell nicht direkt aus dem Internet erreichbar.

Aktuelle Sicherheitsstrategie:
- Eingehender Traffic (Inbound): Standardmäßig blockiert
- Ausgehender Traffic (Outbound): Erlaubt
- Zugriff auf Services erfolgt nur aus dem lokalen Netzwerk
- Keine Portfreigaben am Router vorhanden

Ziel:
Minimierung der Angriffsfläche durch Verzicht auf öffentliche Erreichbarkeit.

### 3. SSH Hardening
**Zweck**
Die Angriffsfläche des administrativen Zugangs zum System zu reduzieren.
#### 3.1 Key-Based Authentication

Status:
- SSH Login über Public Key
- Password-Login deaktiviert

Verifikation:
```Bash
sudo sshd -T | grep passwordauthentication
```
Erwartung:
```text
passwordauthentication no
```

#### 3.2 Root Login deaktivieren
**Zweck**
Direkte SSH-Anmeldung als Root verhindern. Administrative Aktionen erfolgen über einen normalen Benutzer mit `sudo`.
##### 3.2.1 Verifikation:
```bash sudo sshd -T |  grep permitrootlogin ```
Erwartung:
```permitrootlogin no ```
Falls nicht gesetzt, Datei bearbeiten:
```sudo nano /etc/ssh/sshd_config ```
Eintragen:
```permitrootlogin no ```

#### 3.2.2 SSH Dienst neu starten:
```sudo systemctl restart  ssh ```


### 4. fail2ban
**Zweck**
fail2ban überwacht Login-Versuche und blockiert IP-Adressen nach mehrfachen fehlversuchen

#### 4.1. Installation
```Bash
sudo apt install -y fail2ban
```

#### 4.2. Service aktivieren
```Bash
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
```

#### 4.3 Status Prüfen
```Bash
sudo fail2ban-client status sshd
```
Erwartung:
```Bash
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  |- Total failed:     0
|  `- Journal matches:  _SYSTEMD_UNIT=ssh.service + _COMM=sshd
`- Actions
   |- Currently banned: 0
   |- Total banned:     0
   `- Banned IP list:
```

### 5. UFW Firewall 
Die Host-Firewall wird über UFW verwaltet.

**Ziel:**
- Standardmäßig alle eingehenden Verbindungen blockieren
-  Nur benötigte Ports explizit freigeben
- Ausgehende Verbindungen erlauben

Ausnahme:  
Explizit freigegebene LAN-Zugriffe auf notwendige Services.

Detaillierte Verwaltung:  
Siehe:  
infrastructure/security/firewall.md

### 6. Netzwerküberprüfung
#### 6.1 Prüfung aus dem Netzwerk
```Bash
sudo ss -tulpn
```
#### 6.2 Prüfung von einem anderen Gerät im Lan:
```Bash
nmap 192.168.2.x
```
Zeigt alle lauschenden TCP-Ports und welcher Prozess sie nutzt.


### 7. Wartung
Regelmäßig prüfen:
```Bash
sudo fail2ban-client status  
sudo ufw status  
sudo apt update  
sudo apt upgrade
```

### 8. Service Erreichbarkeit
Aktuell sind Services nur intern erreichbar:
- Pi-hole:  
`http://192.168.2.x:8080`  
  
- Uptime Kuma:  
`http://192.168.2.x:3001`  
  
- Wiki.js:  
`http://192.168.2.x:3000`

Eine externe Erreichbarkeit ist aktuell nicht vorgesehen.

### 9. Zukünftige Erweiterungen
Falls externe Erreichbarkeit notwendig wird:
- VPN bevorzugt (z. B. WireGuard)  
- Alternativ Reverse Proxy mit TLS  
- Keine direkten Portfreigaben auf einzelne Services

