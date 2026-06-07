# First Boot - Raspberry Pi 5

## 1. OS flashen
 - Raspberry Pi Imager -> OS Lite 64-bit
 - SSH aktiviere, Hostname: arasaka, Benutzername: arasaka
 - Kein Sonderzeichen im Passwort - Tastaturlayout-Problem

## 2. Erster Login
 - ssh arasaka@192.168.1.x 
 - IP im Router unter verbunden Geräte nachschauen
 - Beim Ersten Mal Fingerprint mit yes bestätigen

## 3. System uodaten
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl vim

## 4. Git konfigurieren
git config --global user.email "deine@email.com"2
git config --global user.name "arasaka"

## 5. SSH-Key einrichten
- Auf dem eigenen Rechner (PowerShell):
ssh-keygen -t ed25519 -C "homelab"
cat $env:USERPROFILE=)(/&%cat $env:USERPROFILE\.ssh\id_ed25519.pub
- Key Kopieren, dann auf dem Pi:
mkdir -p ~/.ssh
nanao ~/.ssh/authoried_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

## 6. Passwort-Login deaktivieren
sudo nano /etc/ssh/sshd_config 
-> PasswordAuthentication no
sudo systemctl restart ssh

## 7. Statische IP am Router servieren
- Router-Oberfläche aujfrufen 192.168.x.x
- Einstellungen -> IPv4 -> Statisches DHCP - Heimnetwerk -> MAC-Adresse des Pi eintragen
- IP festlegen 192.168.x.x
- MAC-Adresse des Pi: op addr -> ether Zeile

## 8. Git SSH-Key für Github eingerichten
- SSH-Key auf dem Pi erstellt
- Public Key auf Github hinterlegt unter Settings -> SSH Keys
- Remote auf SSH unmgestellt:
  git remote set-ur origin git@github.com:DEIN-USERNAME/homelab.git

## 9 Docker Installation auf Raspberry pi
- Installationskript von Docker ausführen:
curl -fsSL https://get.docker.com | sh
- Bentzer zur Docker Gruppe hinzufügen:
sudo usermod -aG docker $USER
- Neu einloggen: 
exit
- Testen ob docker läuft:
docker run hello-world

## 10. DNS auf Pihole setzen (Pi selbst)
sudo nmcli con mod "Wired connection 1" ipv4.dns "192.168.x.x"
sudo nmcli con up "Wired connection 1"

## 11. Nützliche Tools installieren
sudo apt install -y traceroute

## 12. Services starten
# Pihole zuerst - DNS muss als erstes laufen
cd ~/homelab/services/pihole
cd ~/homelab/services/pihole
cp .env.example .env
nano .env  # Passwort setzen
docker compose up -d

# Uptime Kuma
cd ~/homelab/services/uptime-kuma
docker compose up -d

# Nginx Proxy Manager
cd ~/homelab/services/nginx-proxy-manager
docker compose up -d


## 13. Backup-Einrichtung (Ersteinrichtung)

Diese Schritte sind nur einmalig notwendig, um das Backup-System auf einem neuen Raspberry Pi einzurichten.

### Schritt 1: USB-Stick dauerhaft mounten
1. Mount-Verzeichnis erstellen:
   ```bash
   sudo mkdir -p /mnt/backup
   ```
2. UUID des USB-Sticks herausfinden (z. B. von `/dev/sda1` ablesen):
   ```bash
   sudo blkid
   ```
3. Die `/etc/fstab` mit Root-Rechten öffnen:
   ```bash
   sudo nano /etc/fstab
   ```
4. Folgende Zeile am Ende hinzufügen (ersetzen Sie `DEINE-UUID-HIER` mit der echten UUID):
   ```text
   UUID=DEINE-UUID-HIER /mnt/backup ext4 defaults,nofail 0 2
   ```
   *(Hinweis: `nofail` sorgt dafür, dass der Pi auch startet, wenn der USB-Stick mal nicht eingesteckt ist).*

5. System-Dienste neu laden und Stick mounten:
   ```bash
   sudo systemctl daemon-reload
   sudo mount -a
   ```

### Schritt 2: Berechtigungen anpassen
Der Benutzer `arasaka` muss Schreibrechte auf dem Stick haben:
```bash
sudo chown -R arasaka:arasaka /mnt/backup
```

### Schritt 3: Skript aktivieren & automatisieren
1. Das Backup-Skript ausführbar machen:
   ```bash
   chmod 700 ~/homelab/runbooks/backup.sh
   ```
2. Den Cron-Editor für den aktuellen Benutzer öffnen:
   ```bash
   crontab -e
   ```
3. Ganz unten die folgende Zeile einfügen, damit das Skript täglich um 03:00 Uhr läuft:
   ```text
   0 3 * * * /bin/bash ~/homelab/runbooks/backup.sh >> /var/log/backup.log 2>&1
   ```
