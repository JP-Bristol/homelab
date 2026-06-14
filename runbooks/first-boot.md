## 1. Grundsystem
### 1.1 OS Flashen
**Ziel**
Ein sicherer, automatisierter Headless-Start des Raspberry Pi, vorbereitet für die spätere Verwaltung im Konfigurationsmanagement

#### 1.1.1 OS-Vorbereitung (Raspberry Pi Imager)
Die Installation erfolgt mit dem Raspberry Pi Imager. Während der Einrichtung sind insbesondere die **Erweiterten Einstellungen (Customisation)** relevant.

**Betriebssystem auswählen**

-   **Choose OS:**  
    `Raspberry Pi OS (other) → Raspberry Pi OS Lite (64-bit)`

Empfohlen für Headless-Server ohne Desktop-Umgebung.

**Zielmedium auswählen**
- Select Storage:  
Das korrekte Laufwerk sorgfältig prüfen (Datenverlustgefahr!)

**Systemkonfiguration (Customisation)**
- **Hostname:**  
z. B. `pi-homelab` (eindeutig und aussagekräftig)

- **Benutzerkonto:**
Benutzername z. B. `jp`  
Passwort nach eigenen Sicherheitsrichtlinien setzen  
Hinweis: Auf korrektes Tastaturlayout achten (Sonderzeichen!)

- **WLAN:**  
Nicht erforderlich bei Ethernet-Nutzung (empfohlen für stabile Homelab-Setups)

- **SSH aktivieren:**

	-   Enable SSH aktivieren
	-   Authentication: **Password authentication**

Hinweis: Unsicherer als Key-Based Auth, aber für Initial Setup akzeptabel

- **Raspberry Pi Connect:**  
Empfohlen: **deaktivieren**

#### 1.1.2 Funktion prüfen (Erster Boot)
Nach dem Flashen und Start des Raspberry Pi erfolgt der erste SSH-Test:
```Bash
ssh jp@<ip>
```
**Hinweis**

SSH-Problem: alter Host-Key
Falls das Gerät unter derselben IP bereits einmal bekannt war, kann es zu einer Warnung kommen.
Alten Key entfernen in PowerShell:
```Bash
ssh-keygen -R  192.168.2.x
```
Dadurch wird der alte gespeicherte SSH-Fingerprint aus `known_hosts` entfernt.

---

### 1.2. Erster Login per SSH

#### 1.2.1 Verbindung herstellen
```bash 
ssh jp@192.168.2.x
```

#### 1.2.2 IP Herausfinden 
Falls die IP nicht bekannt ist:

- Im Router unter „Verbundene Geräte“ nachsehen
- Oder per DHCP-Liste / Geräteliste im Router-Menü

#### 1.2.3 Beim ersten Verbindungsaufbau
Beim ersten Login erscheint eine Sicherheitsabfrage (Host Key / Fingerprint):
```bash
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Mit yes Bestäigen

---

### 1.3 System aktualisieren
Nach dem ersten Login sollte das System auf den neuesten Stand gebracht werden, um Sicherheitsupdates und Paketverbesserungen zu installieren.

#### 1.3.1 Paketlisten aktulisieren  

```bash
sudo apt update && sudo apt upgrade -y
```

Führt beide Schritte direkt hintereinander aus:
1. Aktualisierung der Paketlisten
2. Installation verfügbarer Updates

#### 1.3.2 Hinweis

Nach größeren Systemupdates kann ein Neustart erforderlich sein:
```bash
sudo reboot now
```
---

### 1.4. Nützliche Werkzeuge installieren
**Ziel**
Installation grundlegender Werkzeuge für Administration, Netzwerkdiagnose und Versionsverwaltung.
**Pakete installieren**
```Bash
sudo apt install -y  git  curl  vim traceroute dnsutils nmap tcpdump
```
**Enthaltene Werkzeuge**
| Paket | Zweck | 
|----------|----------|
| git | Versionsverwaltung und Arbeit mit GitHub-Repositories | 
| curl | HTTP-/API-Anfragen und Downloads über die Kommandozeile | 
| vim |Texteditor für Konfigurationsdateien | 
| traceroute| Analyse von Netzwerkpfaden | 
| dnsutils | DNS-Diagnosewerkzeuge wie `dig` und `nslookup` | 
| nmap | Port- und Netzwerk-Scans |
| tcpdump | Netzwerkverkehr analysieren |

**Installation prüfen**
```Bash
git  --version  
curl  --version  
vim  --version  
traceroute --version  
dig -v
nmap --version
tcpdump --version

```
**Beispiele**
DNS-Auflösung testen:
```Bash
dig github.com
```
Netwerkpfad analysieren:
```Bash
traceroute github.com
```
HTTP-Header abrufen:
```Bash
curl  -I https://github.com
```
---

### 1.5 Docker installieren
**Ziel**
Installation der Docker Engine und des Docker Compose Plugins zur Bereitstellung containerisierter Services.

#### 1.5.1 Installation
```bash  
curl -fsSL https://get.docker.com | sh
```
#### 1.5.2 Benutzer zur docker Gruppe hinzufügen
Damit Docker ohne `sudo` verwendet werden kann:
```bash  
sudo usermod -aG docker $USER
```
#### 1.5.3 Neue Gruppenrechte laden
Abmelden und erneut anmelden oder eine neue SSH-Session öffnen
```bash  
exit
ssh jp@<ip>
```
#### x.4 Funktion prüfen
```bash  
docker run hello-world
```
**Erwartetes Ergebnis**
Docker lädt das Test-Image herunter und gibt eine Erfolgsmeldung aus:
```  
Hello from Docker!
```
**Hinweis**
Das offizielle Installationsskript installiert:

-   Docker Engine
-   Docker Compose Plugin (`docker compose`)

Eine separate Docker-Compose-Installation ist nicht erforderlich.


### 1.6. SSH-KEy einrichten (empfohlen)
Ziel ist eine passwortlose und sichere Anmeldung per SSH-Key.

#### 1.6.1 Key auf dem lokalen Rechner erstellen (Bsp. Windows / PowerShell)
In PowerShell
```bash
ssh-keygen -t ed25519 -C "homelab"
```

- Speicherort bestätigen (Standard: C:\Users\<User>\.ssh\id_ed25519)
- Optional: Passphrase setzen (empfohlen)

#### 1.6.2 Public Key anzeigen und kopieren
In PowerShell
```bash
cat $env:USERPROFILE\.ssh\id_ed25519.pub
```
Den kompletten Output kopieren (beginnt mit ssh-ed25519)

#### 1.6.3 Key auf dem Raspberry Pi hinterlegen
Per SSH auf den Pi einloggen:
```bash
ssh jp@<ip>
```

Dann auf dem Pi:

.ssh Verzeichnis erstellen
```bash
mkdir -p ~/.ssh
```
Key in authorized_keys einfügen
```bash
nano ~/.ssh/authorized_keys
```
Den kopierten Public Key dort einfügen und speichern

#### 1.6.4 Berechtigungen setzen (wichtig!)
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
Bedeutung:
- 700 → nur du darfst das Verzeichnis nutzen
- 600 → nur du darfst die Datei lesen/schreiben

#### 1.6.5 Verbindung testen
Zurück auf dem lokalen Rechner:
```bash
ssh jp@<ip>
```

---

### 1.7. Passwort-Login deaktivieren (SSH Hardening)
Ziel: Nach erfolgreicher Einrichtung von SSH-Keys wird der Passwort-Login deaktiviert, um den Server gegen Brute-Force-Angriffe abzusichern.

#### 1.7.1 SSH-Konfiguration öffnen
```bash
sudo nano /etc/ssh/sshd_config
```

#### 1.7.2 Einstellung anpassen
Im Editor folgende Parameter suchen und setzen:
```bash
PasswordAuthentication no
```

Wichtig:
- Falls ein # davor steht, muss es entfernt werden
- Der Wert muss explizit auf no gesetzt werden

#### 1.7.3 SSH-Dienst neu starten
Damit die Änderungen aktiv werden:
```bash
sudo systemctl restart ssh
```

#### 1.7.4 Test vor Logout (wichtig!)
Bevor die aktuelle Sitzung geschlossen wird:
- Neue SSH-Verbindung in separatem Terminal testen:
```bash
ssh jp@<ip>
```
Hinweis
Nur wenn der Login per Key funktioniert, sollte die alte Session beendet werden.

---
### 1.8. GitHub SSH-Key einrichten
Ziel: Einrichtung eines SSH-Keys für GitHub, um Repositories sicher und ohne Passwortabfrage nutzen zu können.

#### 1.8.1 SSH-Key erstellen
Auf dem Raspberry Pi (oder lokalem Rechner):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Hinweis:

- -t ed25519 = modernes, sicheres Key-Verfahren
- -C = Kommentar (meist E-Mail zur Zuordnung)
- Speicherort kann standardmäßig übernommen werden: ~/.ssh/id_ed25519

#### 1.8.2 Public Key anzeigen  
```bash
cat ~/.ssh/id_ed25519.pub
```
DEn kompletten Putput kopieren (beginnt mit ssh-ed25519)

#### 1.8.3 Key in GitHub hinterlegen
In Github: 
- Settings → SSH and GPG keys → New SSH Key
- Titel vergeben (z. B. homelab-pi)
- Public Key einfügen und speichern

#### 1.8.4 Alten Key entfernen (falls vorhanden)
Falls bereits ein alter Key existiert:
- In GitHub unter SSH Keys
- alten Key löschen

---
### 1.9. Git-Repository einrichten
**Ziel**
Ein lokales Repository wird erstellt und mit GitHub verbunden, um Konfigurationen und Skripte versioniert zu verwalten (Grundlage für „Homelab as Code“).

#### 1.9.1 Projektverzeichnis erstellen
```Bash
mkdir  -p ~/homelab  
cd ~/homelab
```
Erstellt ein zentrales Verzeichnis für alle Homelab-Konfigurationen und wechselt in dieses Verzeichnis.

#### 1.9.2 Git-Repository klonen
```Bash
git clone git@github.com:DEIN-USERNAME/homelab.git .
```
Wichtig: Der Punkt `.` bedeutet, dass das Repository in das **aktuelle Verzeichnis** geklont wird.

Das macht automatisch:
- Herunterladen des Repositories
- Einrichten des `.git`-Verzeichnisses
- Konfiguration des Remote (`origin`)

#### 1.9.3 Verbindung prüfen
```Bash
git remote -v
```
Zeigt, ob das Remote korrekt eingebunden wurde.


**Hinweis (wichtig für Verständnis)**

Dieses Repository ist die Grundlage für:

-   Konfigurationsmanagement
-   Infrastructure-as-Code (IaC)
-   Backup deiner Setup-Schritte
-   spätere Automatisierung (z. B. mit Ansible oder Scripts)

---
### 1.10. Git konfigurieren
**Ziel**
Git wird auf dem Raspberry Pi einmalig konfiguriert, damit Commits korrekt zugeordnet werden können.

#### 1.10.1  Benutzerinformationen setzen

```Bash
git config --global user.name "Dein Name"  
git config --global user.email "deine.mail@example.com"
```
Diese Daten werden bei jedem Commit gespeichert und in GitHub angezeigt.

**Hinweis**
Vor ersten Push Branch auf main setzen:
```bash
git branch -M main
git push -u origin main
```

#### 1.10.2 Konfiguration prüfen
```Bash
git config --list
```
Zeigt alle aktuell gesetzten Git-Konfigurationen an, z. B.:
```Bash
user.name=Dein Name  
user.email=deine.mail@example.com
```
**Hinweis**
Diese Konfiguration muss nur einmal pro System durchgeführt werden.  
Sie gilt global für alle Git-Repositories auf diesem Gerät (`--global`).

---
### 1.11. Statische IP-Adresse per DHCP-Reservierung
**Ziel**
Der Raspberry Pi erhält vom Router immer dieselbe IP-Adresse. Dadurch bleiben SSH-Zugriffe, Automatisierungen und Dienste dauerhaft unter derselben Adresse erreichbar.

#### 1.11.1 MAC-Adresse des Raspberry Pi ermitteln
Auf dem Raspberry Pi
```Bash
ip addr
```
Die MAC-Adresse befindet sich in der Zeile `link/ether` der verwendeten Netzwerkschnittstelle.
Beispiel:
```Bash
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>  
link/ether dc:a6:32:xx:xx:xx
```
Die Adresse hinter `link/ether` notieren.

#### 1.11.2 Router-Oberfläche öffnen
Im Browser die Verwaltungsoberfläche des Routers aufrufen, z. B.:
```Bash
http://192.168.2.x
```
#### 1.11.3 DHCP-Reservierung anlegen
**Router**
Menüpfad (allgemein):
`Router-Oberfläche öffnen → DHCP-Einstellungen → Statische IP / DHCP-Reservierung → MAC-Adresse + IP eintragen`

Dort:
1. MAC-Adresse des Raspberry Pi eintragen
  2. Gewünschte IP-Adresse festlegen (z. B. `192.168.2.x`)
3. Konfiguration speichern

#### 1.11.4 Funktion prüfen
Neue IP-Adresse testen:
```Bash
ping  192.168.2.x
```
SSH-Verbindung prüfen:
```Bash
ssh jp@192.168.2.x
```
**Hinweis**
Die gewählte IP-Adresse sollte:

-   innerhalb des lokalen Netzwerks liegen
-   nicht bereits von einem anderen Gerät verwendet werden
-   möglichst außerhalb häufig genutzter DHCP-Bereiche liegen

Beispiel:
```Bash
Router: 192.168.1.1  
Raspberry Pi: 192.168.1.10  
PC: 192.168.1.20
```
---

## 2. Storage & Backup
**Ziel:**
Bereitstellung eines lokalen Backup-Speichers auf einem USB-Datenträger sowie automatisierte tägliche Sicherungen wichtiger Konfigurationen und Daten.


### 2.1 Architektur
```
Raspberry Pi  
│  
├── Services  
│ 		├── Pihole  
│ 		├── uptime-kuma  
│ 		└── ...  
│  
▼  
Backup Script  
│  
▼  
/mnt/backup  
│  
▼  
USB SSD / USB Stick
```

### 2.2 USB-Speicher einrichten
**Ziel**
Der Backup-Datenträger wird dauerhaft unter `/mnt/backup` eingebunden.

**Mount-Verzeichnis erstellen**
```Bash
sudo  mkdir  -p /mnt/backup
```
**UUID ermitteln**
```Bash
sudo blkid
```
Beispiel:
```
/dev/sda1: UUID="1234-ABCD" TYPE="ext4"
```
**fstab konfigurieren**
```Bash
sudo nano /etc/fstab
```
Eintrag ergänzen:
```Bash
UUID=1234-ABCD /mnt/backup ext4 defaults,nofail 0 2
```
**Mount testen**
```Bash
sudo systemctl daemon-reload  
sudo mount -a
```
Prüfen:
```Bash
df -h
```
### 2.3 Berechtigungen
Der Benutzer `jp` benötigt Schreibrechte auf dem Backup-Datenträger.
```Bash
sudo  chown  -R jp:jp /mnt/backup
```
Prüfen:
```Bash
ls  -ld /mnt/backup
```

### 2.4 Backup-Script
**Speicherort der Backups:**
```Bash
/mnt/backup
```
**Script-Pfad**
```Bash
~/homelab/scripts/backup.sh
```
**Berechtigungen setzen**
```Bash
chmod  700 ~/homelab/scripts/backup.sh
```
**Manueller Testlauf**
```Bash
~/homelab/scripts/backup.sh
```
**Prüfen:**
```Bash
ls  -lah /mnt/backup
```
### 2.5 Automatisierung (Cron)
**Cronjob anlegen:**
```Bash
crontab -e
```
Eintrag hinzufügen:
```Bash
0 3 * * * /bin/bash ~/homelab/scripts/backup.sh >> ~/homelab/logs/backup.log 2>&1
```
**Bedeutung**
| Wert | Bedeutung |
|  --------  |  -------  |
| 0 | Minute |
| 3 | Stunde |
| * | Tag |
| * | Monat |
| * | Wochentag |
→ tägliche Ausführung um **03:00 Uhr**

### 2.6 Verifikation
**Cronjob anlegen**
```Bash
crontab -l
```
**Log prüfen**
```Bash
tail -f ~/homelab/logs/backup.log
```
**Backup-Dateien prüfen**
```Bash
ls  -lah /mnt/backup
```
### 2.7 Recovery
**Verfügbare Backups anzeigen:**
```Bash
ls  -lah /mnt/backup
```
Für die vollständige Wiederherstellung einzelner Services: → Siehe `runbooks/backup-restore.md`

### 2.8 Troubleshooting
**USB-Stick wird nicht gemountet**
Prüfen:
```Bash
sudo blkid
```
```Bash
sudo mount -a
```
```Bash
journalctl -xe
```
**Backup wird nicht ausgeführt**
Prüfen:
```Bash
crontab -l
```
```Bash
tail -100 ~/homelab/logs/backup.log
```
**Keine Schreibrechte auf USB-Stick**
```Bash
sudo  chown  -R jp:jp /mnt/backup
```
---
## 3. Services 
Nach Abschluss des Basis-Setups können die ersten Homelab-Dienste bereitgestellt werden.
### 3.1 Pi-Hole einrichten
**Ziel**
Pi-hole als zentralen DNS-Filter und Werbeblocker im Homelab bereitstellen.

**Environment konfigurieren** 
```bash
cd ~/homelab/services/pihole  
cp .env.example .env 
nano .env # Passwort setzen 
```
**Deployment**
```Bash
cd ~/homelab/services/pihole 
docker compose up -d
```
**Funktion prüfen**
Webinterface aufrufen:
```Bash
http://192.168.2.x:8080/admin
```
DNS-Auflösung testen:
```Bash
dig @192.168.2.x google.com
```
**Weiterführende Dokumentation**
Details zu Betrieb, Updates, Backup und Troubleshooting befinden sich im Service-Runbook:
```
services/pihole/README.md
```
### 3.2 Uptime Kuma
**Ziel** 
Monitoring und Verfügbarkeitsprüfung für Homelab-Dienste bereitstellen.

**Deployment**
```Bash
cd ~/homelab/services/uptime-kuma 
docker compose up -d
```
**Funktion prüfen**
Webinterface aufrufen:
```Bash
http://192.168.2.x:3001
```
**Weiterführende Dokumentation**
Details zu Betrieb, Updates, Backup und Troubleshooting befinden sich im Service-Runbook:
```
services/uptime-kuma/README.md
```

### 3.3 Nginx Proxy Manager
**Ziel**
Zentralen Reverse Proxy für interne Webanwendungen bereitstellen.
**Deployment**
```Bash
cd ~/homelab/services/nginx-proxy-manager
docker compose up -d
```
**Funktion prüfen**
Webinterface aufrufen:
```Bash
http://192.168.2.x:81
```
**Weiterführende Dokumentation**
Details zu Betrieb, Updates, Backup und Troubleshooting befinden sich im Service-Runbook:
```
services/nginx-proxy-manager/README.md
```
**Hinweis**
Nach dem Start müssen die Proxy Hosts manuell in der Web-UI angelegt werden. Details → `services/nginx-proxy-manager/README.md`

### 3.x Recovery
Nach erfolgreichem Setup alle Services aus Backup wiederherstellen:
→ Siehe `runbooks/backup-restore.md`
