## Runbook: SSD Migration

### 1. Zweck
Migration eines bestehenden Raspberry-Pi-Systems von SD-Karte auf SSD/NVMe.

Ziel:
-   Höhere Performance
-   Höhere Zuverlässigkeit
-   Größere Speicherkapazität
-   Reduzierter Verschleiß der SD-Karte

## 2. Voraussetzungen

-   Raspberry Pi 5
-   Funktionierendes System auf SD-Karte
-   SSD/NVMe angeschlossen
-   Aktuelles Backup vorhanden
-   SSH-Zugriff verfügbar

## 3. Zielgerät identifizieren
Vor der Migration prüfen:
```Bash
lsblk
```
 Beispiel:
```Bash
mmcblk0     179:0    0  29.7G  0 disk SD Karte (Quelle)
├─mmcblk0p1 179:1    0   512M  0 part 
└─mmcblk0p2 179:2    0  29.2G  0 part
zram0       254:0    0     2G  0 disk [SWAP]
nvme0n1     259:0    0 238.5G  0 disk SSD (Ziel)
├─nvme0n1p1 259:1    0   512M  0 part /boot/firmware
```
Hinweis:
Gerätebezeichnungen sorgfältig prüfen.

## 4. Backup erstellen
Vor jeder Migration vollständiges Backup durchführen.

Siehe:
- runbooks/backup-restore.md

## 5. SSD klonen
```Bash
sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress conv=fsync
```
Wartezeit abhängig von Datenträgergröße und Geschwindigkeit.

## 6. Boot-Reihenfolge prüfen
Raspberry Pi ausschalten.

Optional:
-   SD-Karte entfernen
-   SSD angeschlossen lassen
Danach System starten.

## 7. Verifikation

### 7.1 System läuft
```Bash
hostnamectl
```

### 7.2 SSH erreichbar
```Bash
ssh USER@IP
```

### 7.3 Datenträger prüfen
```Bash
lsblk
```

Erwartung:

```
Root-Dateisystem befindet sich auf nvme0n1
```

### 7.4 Freien Speicher Prüfen
```Bash
df -h /
```
Erwartung:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  235G   11G  215G   5% /
```
Die verfügbare Größe entspricht der SSD-Kapazität.

## 8. Partition erweitern (falls erforderlich!)
Freien Speicher prüfen:
```Bash
df -h
```
Prüfen ob notwendige Pakete installiert sind:
```Bash
sudo apt install -y cloud-guest-utils
```
Falls die Größe der ursprünglichen SD-Karte übernommen wurde:
```Bash
sudo growpart /dev/nvme0n1 2
```
Falls notwendig, zuerst Filesystem-Check:
```bash 
sudo e2fsck -f /dev/nvme0n1p2 
```
Dann, Dateisystem auf die neue Partitionsgröße anpassen:
```Bash
sudo resize2fs /dev/nvme0n1p2
```
Danach:
```Bash
sudo reboot
```
## 9.  Service-Verifikation

Prüfen:
```Bash
docker ps  --format  "table {{.Names}}\t{{.Status}}"
```
Folgende Services müssen laufen (Stand Juni 2026):
-   Pi-hole → Up
-   Uptime Kuma → Up
-   Nginx Proxy Manager → Up
-   Wiki.js → Up

## 10. Rollback
Falls die Migration fehlschlägt:
1.  Raspberry Pi ausschalten
2.  SSD entfernen
3.  Von der ursprünglichen SD-Karte booten
4.  Fehleranalyse durchführen

Das ursprüngliche System bleibt unverändert erhalten.

## 11. Bekannte Probleme

### 11.1 rpi-clone schlägt bei NVMe fehl
Details siehe:  
`troubleshooting/log.md `
  
Eintrag:  
`2026-06-16 – rpi-clone schlägt bei NVMe fehl`







