# Troubleshooting-Log

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
**Fix:** DNS-Server auf den Endgeräten manuell eingetragen, DNS=IP des Pi -> 192.168.x.x

## 2026-05-26 - Pi-hole kennt das lokale Netz nicht
**Symptom:** Fehlermeldung in den Pi-hole/FTL-Logs: dnsmasq: ignoring query from non-local network 192.168.2.90
**Ursache:** Pi-hole (ab v6) blockiert standardmäßig Anfragen, die über Docker-Subnetze oder andere Schnittstellen reinkommen, da es sie als „nicht-lokal“ einstuft.
**Fix:** In der docker-compose.yml unter environment: den Listening-Modus auf all umstellen. 
FTLCONF_dns_listeningMode: all

## 2026-05-26 — git add schlägt fehl wegen Pihole data-Verzeichnis

**Symptom:** Permission denied beim git add
**Ursache:** Docker-Verzeichnis data/ gehört root, Git hat keine Rechte
**Fix:** services/pihole/data/ in .gitignore eingetragen
