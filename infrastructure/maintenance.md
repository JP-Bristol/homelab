## 1. Ziel

Regelmäßige Wartung und Überprüfung des Homelabs zur Sicherstellung eines stabilen und sicheren Betriebs.

Service-spezifische Wartungsarbeiten sind in den jeweiligen Service-Runbooks dokumentiert.

## 2. Tägliche Prüfung
### 2.1 Speicherplatz
```bash
df -h
```

Prüfen:

-   Genügend freier Speicherplatz vorhanden
----------
### 2.2 Arbeitsspeicher
```bash
free -h
```

Prüfen:

-   Keine ungewöhnlich hohe RAM-Auslastung
----------
### 2.3 Docker Services

```
docker ps
```

Prüfen:

-   Alle Container laufen

----------

### 2.4 Backup

```
tail -20 ~/homelab/logs/backup.log
```

Prüfen:

-   Letztes Backup erfolgreich abgeschlossen

----------

### 2.5 Systemfehler

```
journalctl -p err --since "24 hours ago"
```

Prüfen:

-   Keine neuen kritischen Fehler

----------

### 2.6 Security

```
sudo fail2ban-client status sshd
```

Prüfen:

-   Aktive Sperren
-   Auffällige Login-Versuche

## 3. Wöchentliche Wartung

### 3.1 System aktualisieren

```
sudo apt update
sudo apt upgrade -y
```

----------

### 3.2 Docker Images aktualisieren

Für jeden Service:

```
docker compose pull
```


Anschließend den jeweiligen Service gemäß dessen Runbook aktualisieren.

**Details:**

-   `services/pihole/README.md` → **Update & Maintenance**
-   `services/uptime-kuma/README.md` → **Update & Maintenance**
-   `services/nginx-proxy-manager/README.md` → **Update & Maintenance**
-   `services/wikijs/README.md` → **Update & Maintenance**
-   `services/vaultwarden/README.md` → **Update & Maintenance**
-   `services/syncthing/README.md` → **Update & Maintenance**

----------

### 3.3 Backup prüfen

```
ls -lah /mnt/backup/
```

Prüfen:

-   Aktuelles Backup vorhanden
-   Größe plausibel

----------

## 4. Monatliche Wartung

### 4.1 Firewall prüfen

```
sudo ufw status verbose
```

----------

### 4.2 Offene Netzwerkports prüfen

```
sudo ss -tulpn
```

----------

### 4.3 Docker Images bereinigen

```
docker image prune
```

----------

### 4.4 Dokumentation aktualisieren

Prüfen:

-   Neue Services dokumentiert
-   Neue Trouble Logs ergänzt
-   Runbooks aktuell

----------

## 5. Verifikation

Nach der Wartung prüfen:

-   Alle Docker Container laufen
-   Backup erfolgreich
-   Weboberflächen erreichbar
-   Uptime Kuma zeigt keine Fehler
-   Keine neuen Systemfehler im Journal
