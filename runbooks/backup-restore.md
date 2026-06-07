# Runbook: Backup & Restore

## 1. System-Übersicht
- Host-System: Raspberry Pi 5
- IP-Adresse: 192.168.2.xx

## 2. Backup Prozess (Automatisiert)
Die automatisierten Backups laufen täglich um 3:00 Uhr nachts via Cronjob.


# Runbook: Backup & Restore

## 1. System-Übersicht
- **Host-System:** Raspberry Pi 5
- **IP-Adresse:** 192.168.2.xx

## 2. Backup-Prozess (Automatisiert)
Die automatisierten Backups laufen täglich um 3:00 Uhr nachts via Cronjob.

## 3. Wo liegen die Backups?
* **Externer Speicherort (USB-Stick):** `/mnt/backup/`
* **Aufbewahrungsfrist:** Backups, die älter als 7 Tage sind, werden automatisch gelöscht.

## 4. Was wird gesichert?
Es werden die Konfigurationen des Homelabs, die Dokumentation sowie die Live-Daten der Services gesichert.

1. **Configs und Dokumentation:**
   * Pfad: `~/homelab/`
2. **Daten der Services:**
   * **Pi-hole:** DNS-Listen und Einstellungen
   * **Uptime Kuma:** Monitoring-Datenbank
   * **Nginx Proxy Manager:** Proxy-Konfigurationen und SSL-Zertifikate

---

## 5. Restore (Wiederherstellung)

⚠️ *Hinweis: Ersetzen Sie `DATUM` in den Befehlen immer durch den echten Ordnernamen des Backups (z. B. `2026-06-07`).*

### Service wiederherstellen: Pi-hole
1. In den Service-Ordner wechseln und Container stoppen:
   ```bash
   cd ~/homelab/services/pihole/
   docker compose down
   ```
2. Daten aus Backup zurückkopieren:
   ```bash
   rsync -av /mnt/backup/DATUM/pihole-data/ ~/homelab/services/pihole/data/
   ```
3. Service wieder starten:
   ```bash
   docker compose up -d
   ```
4. Testen, ob die Pi-hole Weboberfläche erreichbar ist und DNS funktioniert.

### Service wiederherstellen: Uptime Kuma
1. In den Service-Ordner wechseln und Container stoppen:
   ```bash
   cd ~/homelab/services/uptime-kuma/
   docker compose down
   ```
2. Daten aus Backup zurückkopieren:
   ```bash
   rsync -av /mnt/backup/DATUM/uptime-kuma-data/ ~/homelab/services/uptime-kuma/data/
   ```
3. Service wieder starten:
   ```bash
   docker compose up -d
   ```
4. Testen, ob das Dashboard alle Monitore korrekt anzeigt.

### Service wiederherstellen: Nginx Proxy Manager
1. In den Service-Ordner wechseln und Container stoppen:
   ```bash
   cd ~/homelab/services/nginx-proxy-manage/
   docker compose down
   ```
2. Daten aus Backup zurückkopieren:
   ```bash
   rsync -av /mnt/backup/DATUM/nginx-proxy-manage-data/ ~/homelab/services/nginx-proxy-manage/data/
   ```
3. Service wieder starten:
   ```bash
   docker compose up -d
   ```
4. Testen, ob die Proxy-Weiterleitungen und SSL-Zertifikate wieder aktiv sind.




