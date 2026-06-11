## Hardware Inventory
**Zweck**
Dieses Dokument beschreibt die physische Infrastruktur des Homelabs.

Ziel ist es, einer anderen Person die Übernahme, Wartung oder Erweiterung der Umgebung zu ermöglichen

### 1. Primärer Host

| Eigenschaften| Wert|
|-|-|
| Gerät |Raspberry Pi 5 |
| RAM | 8 GB |
| SD-Karte | 32 GB |
| Rolle | Docker Host |
| Hostname | arasaka |
| IP Adresse | statisch via DHCP-Reservierung |
| MAC-Adresse | xx:xx:xx:xx:xx |
| Standort|  |
| In Betrieb seit | 2026-05|

### 2. Netzwerk

| Eigenschaften| Wert|
|-|-|
| Verbindung |Ethernet |
| DHCP Reservation | Ja |
| IP-Adresse | 192.168.2.x |
| MAC-Adresse | xx:xx:xx:xx:xx |

Hinweis:
Die feste IP wird über den Router mittels DHCP Reservation vergeben.

### 3. Storage

#### 3.1 **Systemlaufwerk**
| Eigenschaften| Wert|
|-|-|
| Typ | microSD |
| Kapazität | 32 GB |
| Zweck | Betriebssystem |

#### 3.2 Backup-Laufwerk

| Eigenschaften| Wert|
|-|-|
| Typ |USB-Stick |
| Kapazität | 32 GB |
| Dateisystem | ext4 |
| Mount-Pfad | /mnt/backup |
| Zweck | Tägliche Backups |
| In Betrieb seit | 2026-06|

### 4 Angeschlossene Geräte

| Eigenschaften| Wert|
|-|-|
| Typ |USB-Stick |
| USB-Stick | Backup Storage |
| Ethernet | Netzwerkverbindung |

### 5. Abhängigkeiten
Für den Betrieb erforderlich:
-   Stromversorgung Raspberry Pi
-   Ethernet-Verbindung
-   Router mit DHCP Reservation
-   Backup USB-Stick

### 6. Kapazitätsüberischt
Aktuelle Nutzung regelmäßig prüfen:
```bash
df -h
```
Besonders relevant:
-   SD-Karte
-   USB Backup Storage

### 7. Austausch im Fehlerfall
#### 7.1 Raspberry Pi defekt
Wiederherstellung:
1.  Raspberry Pi OS neu installieren
2.  First-Boot Guide durchführen
3.  Repository klonen
4.  Backup USB-Stick anschließen
5.  Services aus Backup wiederherstellen

Siehe:

-   first-boot.md
-   backup-restore.md

### 8. Änderungsverlauf
| Datum| Änderung|
|-|-|
| 2026-06 |Initiale Erstellung |
