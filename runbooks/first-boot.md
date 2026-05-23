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
