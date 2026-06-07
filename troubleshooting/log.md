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
**Ursache** SD-KArte nicht eingestekck.
**Fix** SD-Karte eingesteck

## 2026-05-22 - SSH Login funktioniert nicht

**Symptom** Permission denied beim ersten SSH-Login. 
**Ursache** Sonderzeichen im Passwort, Tastaurlayout-Problem
**Fix** Neu geflasht, Passwort ohne Sonderzeichen gesetzt.

## 2026-05-22 Git Push schlägt fehl

**Symptom** Authentication failed, dann 403, dann rejected.
**Ursache** GitHub Token fehlte, dann Scope, dann lokaler 
und remote Stand nicht synchron.
**Fix** Token mit repo-Scope erstellt, git pull --allow-unreleated-histories 
--rebase, dann push erfolgreich

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
  2. Den DNS-Server der Verbindung manuell auf die Pi-hole IP (z. B.     192.168.x.x) umstellen: sudo nmcli con mod "Wired connection 1" ipv4.dns     "192.168.x.x"
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
**Fix:** IP-Adresse und Port direkt in Uptime Kuma verwenden (z. B. http://192.168.x.x:8080/admin/login) statt Domainnamen.
Langfristige Lösung: Lokale DNS-Einträge in Pihole pflegen damit Container die Domain auflösen können. (TODO)

## 2026-06-07 Fehler Erstellen von Dateien/Ordnern auf externem Datenträger

**Symptom:** Erstellen von Dateien/Ordnern auf externem Datenträger schlägt fehl.
 - Befehl: mkdir -p /mnt/backup/2026-06-07/homelab
 - Fehler: failed: No such file or directory (oder Permission denied)
**Ursache:** Das Verzeichnis /mnt/backup gehörte root, weshalb mein Standard-User keine Schreibrechte hat.
**Fix:** 
 - Besitzer des Mount-Points auf meinen User ändern:
sudo chown arasaka:arasaka /mnt/backup
