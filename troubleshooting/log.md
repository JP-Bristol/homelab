# Troubleshooting-Log

## Troubleshoot Vorlage
## YYYY-MM-DD - [System/Software]: [Kurztitel des Problems] 

**Symptom:** *Was hast du gesehen? Fehlermeldung, unerwartetes Verhalten – immer aus Benutzerperspektive.
**Ursache:** *Warum ist es passiert? Die technische Erklärung für den Fehler.
**Fix:** 
	-**Wo:** *(In welcher App, Datei, GUI oder welchem Menü?)*
	-**Was:** *(Welche Änderung, welcher Befehl, welcher Schieberegler?)*
	-**Hinweis/Prävention:** *(Optional: Was hilft in Zukunft? z.B. Doku ergänzt, PW-Manager empfohlen)*

## 2026-05-22 - Pi started nicht

**Symptom:** Pi bootet nicht, keine Netzwerkverbindung.

**Ursache:** SD-KArte nicht eingesteckt.

**Fix:** SD-Karte eingesteckt.

## 2026-05-22 - SSH Login funktioniert nicht

**Symptom:** Permission denied beim ersten SSH-Login.
 
**Ursache:** Sonderzeichen im Passwort, Tastaurlayout-Problem.

**Fix:** Neu geflasht, Passwort ohne Sonderzeichen gesetzt.

## 2026-05-22 - Git Push schlägt fehl

**Symptom:** Authentication failed, dann 403, dann rejected.

**Ursache:** GitHub Token fehlte, dann Scope, dann lokaler 
und remote Stand nicht synchron.

**Fix:** Token mit repo-Scope erstellt, 
git pull --allow-unreleated-histories  --rebase, 
dann push erfolgreich

## 2026-05-23 - SSH Key nicht gefunden in CMD

**Symptome:** cat und ssh-copy-id nicht erkannt in CMD.

**Ursachen:** CMD kennt diese Befehle nicht, falsche Shell.

**Fix:** PowerShell verwenden, ab jetzt immer PowerShell.

## 2026-05-26 - Pihole Login funktioniert nicht

**Symptom:** Fehlermeldung: Wrong password

**Ursache:** Container wurde zuerst ohne Passwort gestartet.
Pihole setzt Passwort nur beim ersten Start aus der .env

**Fix:** Passwort setzen über - docker exec pihole pihole setpassword DEINPASSWORT

## 2026-05-26 - dig nicht installiert

**Symptom:** Fehlermeldung: dig command not found

**Ursache:** Das Werkzeug dig ist standardmäßig nicht installiert.

**Fix:** sudo apt install -y dnsutils


## 2026-05-26 - Easybox 803 verteil DNS nicht an Geräte

**Symptom:** Fehlermeldung „Server nicht gefunden“ (Website lässt sich nicht laden)

**Ursache:** Die Easybox 803 verteilt fehlerhafte DNS-Server-Daten per DHCP.

**Fix:** DNS-Server auf den Endgeräten manuell eingetragen, DNS=IP des Pi -> 192.168.2.x

## 2026-05-26 - Pi-hole kennt das lokale Netz nicht

**Symptom:** Fehlermeldung in den Pi-hole/FTL-Logs: dnsmasq: ignoring query from non-local network 192.168.2.x

**Ursache:** Pi-hole (ab v6) blockiert standardmäßig Anfragen, die über Docker-Subnetze oder andere Schnittstellen reinkommen, da es sie als „nicht-lokal“ einstuft.

**Fix:** In der docker-compose.yml unter environment: den Listening-Modus auf all umstellen. 
FTLCONF_dns_listeningMode: all

## 2026-05-26 — git add schlägt fehl wegen Pihole data-Verzeichnis

**Symptom:** Permission denied beim git add

**Ursache:** Docker-Verzeichnis data/ gehört root, Git hat keine Rechte

**Fix:** services/pihole/data/ in .gitignore eingetragen

## 2026-05-27 — Uptime Kuma Pihole Monitor zeigt 403

**Symptom:** Fehlermeldung "Request failed with status code 403"

**Ursache:** pi-hole antwortet, verweigert jedoch den zugriff

**Fix:** in Uptime Kuma -> Pihole monitor -> Edit -> Url ändern auf "http://192.168.2.x:8080/admin/login" -> save

## 2026-05-28 - Uptime Kuma: Discord-Benachrichtigung fehlt

**Symptom:** Uptime Kuma sendet keine Benachrichtigungen an Discord.

**Ursache:** Die Benachrichtigungsgruppe war dem Pi-hole-Monitor nicht zugewiesen.

**Fix:** 
  1. In Uptime Kuma den **Pi-hole Monitor** aufrufen und auf **Bearbeiten** (*Edit*) klicken.
  2. Zum Bereich **Benachrichtigungen** (*Notifications*) scrollen.
  3. Den Schieberegler bei `My Discord Alert` auf **Aktiviert** (*ON*) stellen.

## 2026-05-28 - Uptime Kuma: Keine Discord-Benachrichtigung (DNS-Fehler)

**Symptom:** Uptime Kuma sendet trotz Monitor-Ausfall keine Benachrichtigungen an Discord.

**Ursache:** Lokaler DNS-Ausfall (z. B. Pi-hole war down). Uptime Kuma konnte die Domain `discord.com` für den Webhook nicht auflösen.

**Fix:**  Im uptime-kuma Docker-Container docker-compose.yml einen sekundären, externen DNS-Server (`9.9.9.9`) fest eintragen. 


## 2026-06-06 - Raspberry Pi nutzt noch den DNS-Server der Easybox (Router)

**Symptom:** Der Raspberry Pi nutzt noch den DNS-Server der Easybox (Router) statt den eigenen Pi-hole DNS.

**Ursache:** Die Easybox verteilt den Pi-hole DNS nicht zuverlässig per DHCP an die Geräte im Netzwerk (siehe separaten Log-Eintrag vom 2026-05-26 - Easybox 803 verteil DNS nicht an Geräte).

**Fix:**
  1. Namen der aktiven Netzwerkverbindung über den NetworkManager ermitteln: sudo nmcli con show (Ergebnis hier: "Wired connection 1")
  2. Den DNS-Server der Verbindung manuell auf die Pi-hole IP (z. B.     192.168.2.x) umstellen: sudo nmcli con mod "Wired connection 1" ipv4.dns     "192.168.2.x"
  3. Die Verbindung neu laden, um die Änderungen zu aktivieren: sudo nmcli con up "Wired connection 1" 


## 2026-06-06 Fehler beim aurufen von http://pihole.home.

**Symptom:** Beim Aufrufen von http://pihole.home erscheint die Fehlermeldung "403 - Oops! Access denied.".

**Ursache:** Mit dem Update auf Pi-hole v6 hat sich die Webserver-Struktur geändert. Der direkte Zugriff auf den Root-Pfad (/) ohne das Anhängen von /admin führt zu einem Rechtefehler (Access Denied).

**Fix:**
1. Im Nginx Proxy Manager die Proxy-Weiterleitung für pihole.home bearbeiten (Edit)
2. Reiter **Custom Locations** → Add Location
3. Werte eintragen:
   - Location: `/`
   - Scheme: `http`
   - Forward Hostname: `192.168.2.x`
   - Forward Port: `8080`
4. Save klicken und Seite neu laden

## 2026-06-06 Fehler Domainauflösung in Uptime Kuma

**Symptom:** Uptime Kuma kann eine über den Nginx Proxy Manager (NPM) eingerichtete Domain (z. B. http://pihole.home) nicht auflösen. Fehlermeldung: getaddrinfo ENOTFOUND pihole.home.

**Ursache:** Uptime Kuma läuft in einem isolierten Docker-Container. Lokale DNS-Einträge oder Einträge in der hosts-Datei des Windows-Clients sind innerhalb des Docker-Netzwerks nicht bekannt.

**Fix:** IP-Adresse und Port direkt in Uptime Kuma verwenden (z. B. http://192.168.2.x:8080/admin/login) statt Domainnamen.
Langfristige Lösung: Lokale DNS-Einträge in Pihole pflegen damit Container die Domain auflösen können. (TODO)

## 2026-06-07 Fehler Erstellen von Dateien/Ordnern auf externem Datenträger

**Symptom:** Erstellen von Dateien/Ordnern auf externem Datenträger schlägt fehl.
 - Befehl: mkdir -p /mnt/backup/2026-06-07/homelab
 - Fehler: failed: No such file or directory (oder Permission denied)

**Ursache:** Das Verzeichnis /mnt/backup gehörte root, weshalb mein Standard-User keine Schreibrechte hat.

**Fix:** 
 - Besitzer des Mount-Points auf meinen User ändern:
```Bash
sudo chown jp:jp /mnt/backup
```

## 2026-06-08 Cron führt das Backup-Skript nicht aus.

**Symptom:** Kein automatisches Backup, keine Log-Datei. Manueller Test ergab: Permission denied beim Schreiben nach /var/log/backup.log.

**Ursache:** Das Verzeichnis /var/log/ gehört root. Der Benutzer, unter dem der Cron-Job läuft, hat keine Schreibberechtigung.

**Fix:** Log-Pfad in das Home-Verzeichnis verschoben (~/homelab/logs/backup.log). Anpassung der Crontab auf absolute Pfade, um Umgebungskonflikte zu vermeiden.

## 2026-06-08 rsync-Fehler während des Backups

**Symptom:** Während des Backups treten Fehler in der Log-Datei auf (z. B. "file has vanished" oder Datei-Zugriffsfehler), da sich Dateien ändern, während rsync sie kopiert.

**Ursache:** rsync versucht Dateien zu kopieren, die während des Kopiervorgangs von laufenden Diensten verändert oder neu geschrieben werden.

**Fix:**
1. --ignore-errors hinzugefügt, damit das Backup bei einzelnen Datei-Fehlern nicht vollständig abbricht.
2. --exclude='logs/' hinzugefügt, damit die Log-Datei des Backup-Prozesses nicht während des Schreibens erneut gesichert wird.
3. `--exclude='.git/'` hinzugefügt um Git-Objekte nicht zu sichern.

Aktueller Stand der Backup-Befehle:
```bash
rsync -av --ignore-errors --exclude='logs/' ~/homelab/ $BACKUP_DIR/homelab/
rsync -av --ignore-errors ~/homelab/services/pihole/data/ $BACKUP_DIR/pihole-data/
rsync -av --ignore-errors ~/homelab/services/uptime-kuma/data/ $BACKUP_DIR/uptime-kuma-data/
rsync -av --ignore-errors ~/homelab/services/nginx-proxy-manager/data/ $BACKUP_DIR/npm-data/
```

TODO: Strategie für konsistente Docker-Volume-Backups (z. B. docker pause oder Datenbank-Dumps) implementieren

## 2026-06-09 - git push schlägt fehl: kein upstream Branch

**Symptom:** `fatal: The current branch master has no upstream branch`

**Ursache:** Lokaler Branch heißt `master`, GitHub erwartet `main`.

**Fix:**
1. Branch umbenennen: `git branch -M main`
2. Push mit upstream setzen: `git push -u origin main`

## 2026-06-10 - Backup Restore schlägt fehl (Permission denied)

**Symptom:** Fehler beim Wiederherstellen von Service-Backups.
Beispiel:
```text
rsync: failed: Permission denied
```

**Ursache:** Das data-Verzeichnis des betroffenen Services gehört dem Benutzer root und kann vom Restore-Prozess nicht beschrieben werden.

**Fix:** Eigentümer des Verzeichnisses korrigieren:
```Bash
sudo chown -R USER:USER ~/homelab/services/<service>/data/
```

Beispiel:
```Bash
sudo chown -R jp:jp ~/homelab/services/pihole/data/
```

**Verifikation:**

Eigentümer prüfen:
```Bash
ls -ld ~/homelab/services/<service>/data/
```
Anschließend den Restore erneut ausführen.

```Bash
docker compose up -d
docker ps
```
Prüfen, ob der Service erfolgreich startet und die Konfigurationen wieder vorhanden sind.


## 2026-06-10 - Restore schlägt fehl (Docker-Permission)

**Symptom:** Fehler beim Wiederherstellen von Service-Backups.
Beispiel:
```text
rsync: [generator] failed to set times on "/home/jp/homelab/services/pihole/data/.": Operation not permitted 
```

**Ursache:** Der aktuelle Benutzer besitzt Schreibrechte auf die Dateien, darf jedoch bestimmte Dateiattribute (Gruppeninformationen oder Zeitstempel) nicht setzen. Dies tritt häufig bei Docker-Volumes oder gemounteten Verzeichnissen auf.

**Fix:** rsync ohne Übernahme von Gruppeninformationen und Zeitstempeln ausführen:
```Bash
rsync -av --no-group --no-times /mnt/backup/DATUM/SERVICE-data/ ~/homelab/services/SERVICE/data/
```
Beispiel:
```Bash
rsync -av --no-group --no-times /mnt/backup/2026-06-10/pihole-data/ ~/homelab/services/pihole/data/
```

**Verifikation:**
Restore erneut ausführen.

```Bash
docker compose up -d
docker ps
```
Prüfen, ob der Service erfolgreich startet und die Konfigurationen wieder vorhanden sind.

## 2026-06-11 - Backup Cronjob schlägt fehl (Script nicht gefunden)

**Symptom:** Backup-Cronjob läuft nicht erfolgreich.
Fehlermeldung in `backup.log`:
```text
/bin/bash: /home/jp/homelab/scripts/backup.sh: No such file or directory
```

**Ursache:** Der Cronjob verweist auf einen falschen Pfad.
Aktueller Speicherort des Scripts:
```text
~/homelab/scripts/backup.sh
```

**Fix:** Crontab Eintrag korrigieren:
```Bash
0 3 * * * /bin/bash ~/homelab/scripts/backup.sh >> ~/homelab/logs/backup.log 2>&1
```

**Hinweis (TODO)**
backup.sh sollte langfristig aus dem Runbooks-Verzeichnis in einen dedizierten Scripts-Ordner verschoben werden:
```Bash
~/homelab/scripts/backup.sh
```

**Verifikation:**
1. Script manuell ausführen
```Bash
 /bin/bash ~/homelab/scripts/backup.sh >> ~/homelab/logs/backup.log 2>&1
```

2. Logs Prüfen
```Bash
cat ~/homelab/logs/backup.log
```
Erwartung:
```Bash
Backup fertig: /mnt/backup/2026-06-11
```

3. Backup-Verzeichnis prüfen
```Bash
ls -l /mnt/backup/
```
Erwartung:
```Bash
2026-06-11
```
**Zusatzprüfung (Zeitverhalten)**
Cron-Ausführung prüfen:
```Bash
ls -l /mnt/backup/
```
Erwartung: täglich neuer Ordner um 03:00 Uhr


## 2026-06-16 - rpi-clone schlägt bei NVMe-Ziel fehl

**Symptom:**
Klonvorgang mit `rpi-clone` bricht ab.

Fehlermeldung:
```text
...
mount: /mnt/clone: fsconfig() failed: /dev/nvme0n12: Can't lookup blockdev. dmesg(1) may have more information after failed mount system call. Mount failure of /dev/nvme0n12 on /mnt/clone. Aborting!
```

**Ursache:**
`rpi-clone` erzeugt bei bestimmten NVMe-Geräten fehlerhafte Partitionspfade.

Statt: 
`/dev/nvme0n1p2`
wird fälschlicherweise:
`/dev/nvme0n12`
verwendet.

Dadurch können die Zielpartitionen nicht gemountet werden und der Klonvorgang schlägt fehl.

**Fix:**
Für NVMe-Medien kein `rpi-clone` verwenden.
Stattdessen das Laufwerk mit `dd` klonen:
```Bash
sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress conv=fsync
```
Gerätebezeichnungen vor Ausführung sorgfältig prüfen.

**Hinweis:**
Das Problem tritt nur bei bestimmten NVMe-Geräten auf.
Für SD-Karten und klassische USB-Laufwerke kann `rpi-clone` weiterhin funktionieren

.Nach dem Klonen entspricht die Partitionsgröße zunächst der Größe des Quellmediums.  
  
Wird beispielsweise eine 32-GB-SD-Karte auf eine 500-GB-SSD geklont, bleiben große Teile des Speicherplatzes zunächst ungenutzt.  
  
Freien Speicher prüfen:  
  
```bash  
lsblk
```
```bash 
df -h
```

Falls erforderlich, Partition erweitern:
```bash 
sudo growpart /dev/nvme0n1 2
```

Falls erforderlich, Dateisystem auf die neue Partitionsgröße anpassen:
```bash 
sudo resize2fs /dev/nvme0n1p2
```

Erwartung:
```
resize2fs 1.47.2 (1-Jan-2025) 
Resizing the filesystem on /dev/nvme0n1p2 to 62381648 (4k) blocks. 
The filesystem on /dev/nvme0n1p2 is now 62381648 (4k) blocks long.
```
Anschließend Neustart durchführen:
```bash 
sudo reboot
```
Verifikation:
```bash  
df -h /
```
Erwartung:

Die Root-Partition nutzt die vollständige Kapazität der SSD.
Beispiel:
``` 
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  235G   11G  215G   5% /
```
**Verifikation**

Partitionen prüfen:
```bash 
lsblk
```
Erwartung:

-   Zielmedium enthält die gleichen Partitionen wie das Quellmedium.

Optional:
```bash 
sudo fdisk -l /dev/nvme0n1
```
Nach dem Klonen Test-Boot durchführen:

-   SD-Karte entfernen (falls gewünscht)
-   Von NVMe starten
-   SSH Login erfolgreich
-   Docker Services starten fehlerfrei

Erwartung:
Das System bootet vollständig vom geklonten NVMe-Laufwerk und alle Services sind funktionsfähig


## 2026-06-18 - SSH Passwort-Login nicht deaktiviert 

**Symptom:** Bei der Überprüfung, mit ```Bash sudo sshd -T | grep passwordauthenticationob``` Password-Login deaktiviert ist festgestellt, dass der Passwort-Login noch aktiv ist. 

```text
passwordauthentication Yes
```


**Ursache:** Die SSH-Konfiguration wurde durch eine Datei im Verzeichnis `/etc/ssh/sshd_config.d/` überschrieben.

In der Datei:
```text
/etc/ssh/sshd_config.d/50-cloud-init.conf
```
```text
PasswordAuthentication yes
```


Obwohl in der Hauptkonfigurationsdatei:
 `/etc/ssh/sshd_config `

bereits
```text
PasswordAuthentication no
```
eingetragen war.

Die Konfiguration aus sshd_config.d hatte Vorrang und aktivierte den Passwort-Login wieder.


**Fix:** Passwort-Login in der Cloud-Init SSH-Konfiguration deaktivieren:
```Bash
sudo nano /etc/ssh/sshd_config.d/50-cloud-init.conf
```

Ändern:
`PasswordAuthentication yes` → `PasswordAuthentication no`

SSH-Dienst neu starten:
```Bash
sudo systemctl restart ssh
```


Hinweis:
Vor Änderungen an der SSH-Konfiguration sicherstellen:

- Aktuelle SSH-Verbindung geöffnet lassen
- Zweite SSH-Verbindung testen
- Nicht die bestehende Sitzung schließen, bevor der neue Login erfolgreich funktioniert

Bei falscher SSH-Konfiguration kann der SSH-Zugriff verloren gehen.
Lokaler Zugriff über Bildschirm/Tastatur oder ein Backup der Konfiguration ist dann erforderlich.

**Verifikation:**

SSH-Konfiguration prüfen:
```Bash
sudo sshd -T | grep passwordauthentication
```

Erwartung:
`passwordauthentication no`

Neue SSH-Verbindung testen:
```powershell
ssh USER@192.168.2.x
```

Erwartung:
- Login funktioniert ohne Passwortabfrage
- Public-Key-Authentifizierung wird verwendet


## 2026-06-24 - Vaultwarden Dashboard meldet "secure context required"

**Symptom:** 
Beim Aufrufen des Vaultwarden Dashboards erscheint:
```
You are not using a secure context which is required for the subtle crypto api.
You need to enable https.
```
**Ursache:**
Vaultwarden benötigt für bestimmte kryptographische Funktionen die Browser Web Crypto API.

Diese API ist nur in einem sicheren Kontext verfügbar:

-   HTTPS-Verbindung
-   oder spezielle Ausnahmefälle wie localhost

Eine lokale HTTP-Verbindung über:
```
http://vaultwarden.home
```
wird vom Browser als unsicher behandelt.

Ein Let's Encrypt Zertifikat ist für eine lokale `.home` Domain nicht möglich, da keine öffentliche Domain-Verifikation durchgeführt werden kann.

**Fix:**
Ein selbstsigniertes TLS-Zertifikat erstellen und über Nginx Proxy Manager bereitstellen.
Zertifikat erstellen:
```Bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \ -keyout vaultwarden.key \ -out vaultwarden.crt \ -subj "/CN=vaultwarden.home"
```

Danach:

1.  Zertifikat in Nginx Proxy Manager unter **SSL Certificates → Add Certificate → Custom Certificate** importieren.
2.  Zertifikat dem Proxy Host `vaultwarden.home` zuweisen.
3.  Zugriff über HTTPS testen: `https://vaultwarden.home`

**Verifikation**
Erwartung:

-   Keine Secure-Context Fehlermeldung mehr
-   Vaultwarden Login funktioniert
-   Browser verwendet HTTPS

**Hinweis**
Der Proxy Host bleibt intern auf HTTP:
- HTTPS wird nur zwischen Browser und Nginx Proxy Manager verwendet.

## 2026-06-24 - NPM meldet "Internal Error" beim Anfordern eines Zertifikats

**Symptom**

Beim Versuch ein SSL-Zertifikat über Nginx Proxy Manager anzufordern erscheint:

```
Internal Error
```

**Ursache**

Nginx Proxy Manager versucht ein Let's Encrypt Zertifikat auszustellen.

Let's Encrypt benötigt eine öffentlich erreichbare Domain, die über das öffentliche DNS aufgelöst und verifiziert werden kann.

Die verwendete lokale Domain:

```
vaultwarden.home
```

existiert nur im lokalen Netzwerk und kann nicht durch Let's Encrypt validiert werden.

**Fix**

Für lokale Services kein Let's Encrypt Zertifikat verwenden.

Stattdessen ein selbstsigniertes Zertifikat erstellen und in Nginx Proxy Manager als Custom Certificate hinterlegen.

Siehe:

```
2026-06-24 Vaultwarden Dashboard meldet "secure context required"
```

**Verifikation**

Prüfen:

-   Custom Certificate ist in Nginx Proxy Manager vorhanden
-   Zertifikat ist dem Proxy Host `vaultwarden.home` zugewiesen
-   Zugriff funktioniert über:

```
https://vaultwarden.home
```

Erwartung:

-   HTTPS Verbindung erfolgreich
-   Vaultwarden Dashboard erreichbar
-   Keine Secure-Context Fehlermeldung


## 2026-06-25 USB-Stick nicht gemountet – Backup schlägt fehl
**Symptom:**

Automatische Backups werden nicht erstellt.

Fehlermeldung:

cannot create directory '/mnt/backup/2026-06-25': Permission denied
**Ursache:**

Der Backup-USB-Stick ist nicht gemountet.

Raspberry Pi OS Lite wird headless betrieben und mountet USB-Geräte nicht automatisch wie eine Desktop-Umgebung.

Dadurch zeigt /mnt/backup lediglich auf das lokale Verzeichnis des Raspberry Pi statt auf den USB-Stick.

**Fix:**

Mount-Status prüfen:
```Bash
mount | grep backup
```
USB-Stick manuell mounten:
```Bash
sudo mount -a
```
oder:
```Bash
sudo mount /dev/sda1 /mnt/backup
```
Verifikation

Prüfen:
```Bash
mount | grep backup
```
Erwartung:
```
/dev/sda1 on /mnt/backup type ext4 (rw,relatime)
```
Zusätzlich:
```Bash
ls -l /mnt/backup
```
Erwartung:

- Vorhandene Backup-Verzeichnisse sichtbar
- Neues Backup kann erfolgreich erstellt werden

## 2026-06-29 Pi-hole 403 über Nginx Proxy Manager – Permanente Lösung

Ersetzt den bisherigen Workaround vom 06.06.2026 (Fehler beim aurufen von http://pihole.home).

**Symptom:**

Beim Aufrufen von `http://pihole.home` erscheint die Fehlermeldung: **403 Forbidden** oder die Weiterleitung auf 

`http://pihole.home/admin `

funktioniert trotz entsprechender Konfiguration im Nginx Proxy Manager nicht.

**Ursache:**

Pi-hole benötigt den konfigurierten Hostnamen für die korrekte Verarbeitung der Weboberfläche.

Ist `webserver.domain` nicht gesetzt, kann die Weiterleitung zum Admin-Dashboard (`/admin`) über einen Reverse Proxy fehlschlagen.

**Fix:**

In der Pi-Hole Weboberfläche:

1. Oben rechts von **Basic** auf **Expert** umschalten.
2. **All settings** öffnen unter Settings - Menü links
3. Webserver and API auswählen.
4. Den Eintrag **webserver.domain** auf den gewünschten Hostnamen setzen: `pihole.home`
5. Änderungen speichern.

**Hinweis:** 

Der bisherige Workaround über NPM Custom Location funktionierte nicht zuverlässig nach Updates oder Container-Neustarts. Diese Lösung ist stabiler da sie direkt in Pi-hole konfiguriert wird.


**Verifikation:**

Browser öffnen:
`http://pihole.home`
Erwartung:

-   Automatische Weiterleitung auf `http://pihole.home/admin/`
-   Pi-hole Dashboard wird ohne 403-Fehler angezeigt.

## 2026-06-30 - Bitwarden iOS App kann keine Verbindung zu Vaultwarden herstellen

**Symptom:**
Die Bitwarden-App auf dem iPhone kann sich nicht mit dem selbst gehosteten Vaultwarden-Server verbinden.

Nach Eingabe des Master-Passworts erscheint die Fehlermeldung:
```
Es ist ein Fehler aufgetreten.
```
Der Zugriff über den Webbrowser funktioniert hingegen.

**Ursache:**
Das verwendete selbstsignierte Zertifikat enthielt keinen **Subject Alternative Name (SAN)**.

Moderne TLS-Clients – insbesondere iOS bzw. Apple App Transport Security (ATS) – akzeptieren Zertifikate ohne SAN nicht. Dadurch schlägt die TLS-Verbindung der Bitwarden-App fehl.

**Fix:**
1. Neues Zertifikat mit SAN erstellen
```bash
cd ~/homelab/services/vaultwarden/data
```
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout vaultwarden.key \ 
-out vaultwarden.crt \ 
-subj "/CN=vaultwarden.home" \ 
-addext "subjectAltName=DNS:vaultwarden.home,IP:192.168.2.x"
```

2. Zertifikat in Nginx Proxy Manager austauschen
	1. SSL Certificates → Custom Certificate 
	2. Altes Zertifikat löschen.
	3. Neues Zertifikat importieren (`.crt` und `.key`).
	4. Unter: `Proxy Hosts` → `vaultwarden.home` → `Edit` → `SSL`
	5. Neues Zertifikat auswählen.
	6. `Force SSL` aktivieren.

3. Zertifikat auf dem iPhone installieren
	1. `vaultwarden.crt` per AirDrop, iCloud Drive oder E-Mail auf das iPhone übertragen.
	2. Zertifikat öffnen und installieren.
	3. Anschließend öffnen: `Einstellungen` →`Allgemein` → `VPN und Geräteverwaltung` → `Konfigurationsprofil` → Installation abschließen.
	4. Danach: `Einstellungen` →`Allgemein` → `Info` → `Zertifikatsvertrauenseinstellungen` → `Volles Vertrauen für Root-Zertifikate` für das installierte Zertifikat aktivieren.

**Hinweise:**
-   Der Proxy Host im Nginx Proxy Manager bleibt weiterhin auf **HTTP** konfiguriert.
-   HTTPS wird ausschließlich zwischen Client (Browser bzw. Bitwarden-App) und Nginx Proxy Manager verwendet.
-   Das selbstsignierte Zertifikat muss auf jedem iOS-Gerät einmalig installiert und als vertrauenswürdig aktiviert werden.

**Verifikation:**

1. Server:
-   Browser öffnet `https://vaultwarden.home`
-   Keine Meldung bezüglich eines fehlenden Secure Contexts
-   Vaultwarden Login funktioniert
-   Force SSL ist aktiviert

2. iPhone:
-   Zertifikat ist installiert und als vertrauenswürdig markiert.
-   Login über die Bitwarden-App funktioniert.
-   Tresore werden erfolgreich synchronisiert.
	
## 2026-07-02 - Syncthing: Ordner wird nicht synchronisiert wegen Docker Volume Mapping

**Symptom:**

Der Obsidian-Ordner wird nicht synchronisiert.

In der Syncthing Web UI wird kein Fehler angezeigt. Der Ordnerstatus steht auf:

```
Up to Date
```

Trotzdem erscheinen die erwarteten Dateien nicht auf den anderen Geräten.

**Ursache:**

Der Obsidian-Ordner wurde auf dem Raspberry Pi außerhalb des in den Container eingebundenen Volume-Bereichs angelegt.

Dadurch konnte der Syncthing-Container den Ordner nicht sehen.

Wichtig:

Der **Folder Path** in Syncthing muss immer aus Sicht des Containers angegeben werden, nicht aus Sicht des Hosts.

**Fix:**

**Fix 1 (empfohlen) — Folder Path anpassen:**
In der Syncthing Web UI den Folder Path direkt auf den Container-Pfad setzen:
```
/var/syncthing/obsidian
```
Grund: Kein Neustart nötig — Änderung wird sofort übernommen.

**Fix 2 (alternativ) — Eigenes Volume hinzufügen:**

Eigenes Volume für den Obsidian-Ordner in der `docker-compose.yml` hinzufügen:

```
volumes:
  - ./data:/var/syncthing
  - ~/homelab/data/obsidian:/var/syncthing/obsidian
```

Danach Container neu starten:

```
docker compose down
docker compose up -d
```

In der Syncthing Web UI den Folder Path setzen auf:

```
/var/syncthing/obsidian
```

**Hinweis:**

Bei zusätzlichen Volume-Mappings muss das Backup-Konzept angepasst werden.

Der Host-Pfad:

```
~/homelab/data/obsidian/
```

muss separat gesichert werden, falls er nicht im normalen Syncthing-Backup enthalten ist.


**Verifikation:**

1.  Testdatei im synchronisierten Host-Ordner erstellen:

```
touch ~/homelab/data/obsidian/test.txt
```

2.  Syncthing Web UI beobachten.

Erwartung:

-   Ordnerstatus wechselt kurz auf **Syncing**
-   Anschließend wieder auf **Up to Date**

3.  Auf dem gekoppelten Gerät prüfen.

Erwartung:

-   `test.txt` erscheint im synchronisierten Ordner.

4.  Testdatei wieder löschen.

Erwartung:

-   Die Löschung wird ebenfalls auf das gekoppelte Gerät synchronisiert.


## 2026-07-04 - Python: Falsche Statusauswertung mit der Uptime Kuma API

**Symptom:**

Das eigene Python-Skript zeigte einen Service immer als **UP** an, obwohl dieser in Uptime Kuma als **DOWN** markiert war.

Die Statusausgabe des Skripts stimmte nicht mit dem Uptime-Kuma-Dashboard überein.

**Ursache:**
Für die Statusauswertung wurde zunächst ein ungeeigneter Wert verwendet.

`monitor.active` beschreibt lediglich, ob der Monitor in Uptime Kuma aktiviert ist. Dieser Wert sagt **nicht** aus, ob der überwachte Service aktuell erreichbar ist.

Der tatsächliche Laufzeitstatus wird über den letzten Heartbeat bereitgestellt.

Zusätzlich musste der Heartbeat-Status korrekt als boolescher Wert ausgewertet werden.

**Fix:**

Den Status aus dem letzten Heartbeat lesen und anschließend in einen booleschen Status umwandeln.

```
beat_status = latest_beat.get("status")
is_up = beat_status.value == 1
```

Die Statusanzeige anschließend über `is_up` erzeugen:

```
"status": "✅ UP" if is_up else "❌ DOWN"
```

Hinweis:
Beim Arbeiten mit APIs sollte geprüft werden, welche Bedeutung ein Feld tatsächlich besitzt.

In der Uptime Kuma API gilt:

-   `monitor.active` → Monitor ist aktiviert.
-   `heartbeat.status` → Tatsächlicher Status des überwachten Services.

Beide Werte dürfen nicht miteinander verwechselt werden.


**Verifikation:**

1.  Einen überwachten Service stoppen.
2.  Warten, bis Uptime Kuma den Status aktualisiert (Standard-Polling-Intervall: 60 Sekunden).
3.  Python-Skript erneut ausführen.

**Erwartung:**

-   Uptime Kuma zeigt den Service als **❌ DOWN**.
-   Das Python-Skript zeigt den Service ebenfalls als **❌ DOWN**.

4.  Den Service wieder starten.
5.  Erneut ca. 60 Sekunden warten.
6.  Python-Skript erneut ausführen.

**Erwartung:**

-   Uptime Kuma zeigt den Service wieder als **✅ UP**.
-   Das Python-Skript zeigt den Service ebenfalls als **✅ UP**.

## 2026-07-08 - Python: `add_service.py` kann keinen Uptime-Kuma-Monitor erstellen

**Symptom:**

Beim Erstellen eines Monitors über `add_service.py` trat folgender Fehler auf:

```text
SQLITE_CONSTRAINT: NOT NULL constraint failed: monitor.conditions
```

Der Monitor wurde nicht in Uptime Kuma angelegt.

----------

**Ursache:**

Die verwendete Python-Bibliothek `uptime-kuma-api` ist nicht vollständig mit Uptime Kuma **2.4.0** kompatibel.

Beim Erstellen eines Monitors wird das in Uptime Kuma 2.x erforderliche Feld `monitor.conditions` nicht gesetzt. Dadurch schlägt das Anlegen des Monitors aufgrund einer Datenbank-Constraint fehl.

----------


**Fix:**

Die nicht kompatible Bibliothek `uptime-kuma-api` deinstallieren:

```bash
pip3 uninstall uptime-kuma-api
```

Anschließend die kompatible Bibliothek `uptime-kuma-api-v2` installieren:

```bash
pip3 install uptime-kuma-api-v2
```

**Hinweis:**

Der Import im Python-Code bleibt unverändert:

```python
from uptime_kuma_api import UptimeKumaApi, MonitorType
```

Es sind keine weiteren Codeänderungen am Import erforderlich.

Anschließend das Skript erneut ausführen.

----------

**Hinweis:**

Vor der Verwendung einer Python-Bibliothek sollte geprüft werden, ob sie mit der eingesetzten Version der Zielanwendung kompatibel ist.

In diesem Fall unterstützt `uptime-kuma-api-v2` die Änderungen von Uptime Kuma 2.x.

----------

**Verifikation:**

1.  Neue Bibliothek installieren.
    
2.  `add_service.py` erneut ausführen.
    

**Erwartung:**
-   Der Monitor wird ohne Fehlermeldung erstellt.
-   Es tritt kein `SQLITE_CONSTRAINT`-Fehler mehr auf.
-   Der neue Monitor erscheint im Uptime-Kuma-Dashboard.
-   Die Statusüberwachung startet erfolgreich.