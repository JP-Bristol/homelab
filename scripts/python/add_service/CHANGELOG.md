# Changelog — add_service

Alle nennenswerten Änderungen an `add_service.py` werden hier dokumentiert, neueste Version zuerst.

---

### v0.4.3
**Datum:** 2026-07-13

#### Neu
- Ausgabe-Helper in `output.py` eingeführt:
  - `print_ok()`
  - `print_info()`
  - `print_warning()`
  - `print_error()`
  - `print_debug()`
- Einheitliches Ausgabeformat für die Konsole eingeführt:
  - `[OK]`
  - `[INFO]`
  - `[WARNING]`
  - `[ERROR]`
  - `[DEBUG]`

#### Geändert
- `main.py` verwendet jetzt ausschließlich die neuen Ausgabe-Helper anstelle direkter `print()`-Aufrufe.
- Debug-Ausgaben auf `print_debug()` umgestellt.
- Erfolgs-, Informations-, Warn- und Fehlermeldungen im Hauptprogramm vereinheitlicht.
- Redundante Präfixe im Meldungstext entfernt (z. B. `"Fehler: ..."`, `[DEBUG]`, `[DRY-RUN]`), da die neuen Ausgabe-Helper das Präfix automatisch ergänzen.

#### Behoben
- Warnmeldungen bei nicht sauber getrennten Verbindungen (`disconnect_uptime_kuma()` / `disconnect_from_pihole()`) waren seit dem `try/finally`-Umbau in v0.4.0 verloren gegangen (Rückgabewerte wurden nicht mehr geprüft); jetzt wiederhergestellt und über `print_warning()` ausgegeben.
- `finally`-Block um `None`-Prüfungen ergänzt (`if api is not None:` / `if session is not None:`), sodass Disconnect-Funktionen nur bei tatsächlich aufgebauten Verbindungen aufgerufen werden.

#### Verifikation
- Erfolgreichen Programmablauf mit den neuen Ausgabe-Helpern getestet.
- Dry-Run mit der vereinheitlichten Konsolenausgabe getestet.
- Fehler- und Warnmeldungen im Hauptprogramm erfolgreich über die neuen Ausgabe-Helper ausgegeben.
- Kritischer Fehlerfall (Uptime-Kuma-Verbindung schlägt fehl) erneut mit neuen Ausgabe-Helpern bestätigt.

#### Bekannt / Offen
- Business-Logik in `pihole.py`, `uptime_kuma.py` und `validation.py` nutzt weiterhin eigene `print()`-Aufrufe statt der neuen Ausgabe-Helper — vollständige Trennung von Ausgabe und Logik folgt in einem späteren Schritt.

## v0.4.2
**Datum:** 2026-07-13

**Neu**
- `parse_monitor_record()` implementiert:
  - Wandelt einen von der Uptime-Kuma-API zurückgegebenen Monitor in eine schlanke interne Datenstruktur um.
- `build_monitor_records()` implementiert:
  - Erstellt aus allen unterstützten Uptime-Kuma-Monitoren eine strukturierte Liste.
  - Filtert ausschließlich HTTP(s)-Monitore (`type == "http"`); andere Monitortypen (z. B. Ping) werden ausgeschlossen.
- Einheitliche interne Datenstruktur für Uptime-Kuma-Monitore eingeführt:

```python
[
    {
        "id": 1,
        "name": "Pihole",
        "url": "http://192.168.2.x:8080/admin/login"
    }
]
```

**Geändert**
- `main.py`: Das Ergebnis von `get_uptime_monitors()` wird jetzt über `build_monitor_records()` in die interne Datenstruktur überführt, bevor es an `validate_uptime_monitor()` übergeben wird.
- `validate_uptime_monitor()` selbst bleibt unverändert und arbeitet dank identischer Feldnamen (`name`, `url`) transparent mit der neuen Datenstruktur.
- Die Datenverarbeitung für Uptime Kuma folgt jetzt derselben Architektur wie Pi-hole:
  - `fetch → build → validate → add`

**Behoben**
- `get_uptime_monitors()` verfügt jetzt über eine eigene Fehlerbehandlung (`try/except`) und gibt bei API-Fehlern konsistent `None` zurück.
- `main.py` prüft analog zu Pi-hole (`raw_dns_records`), ob `get_uptime_monitors()` `None` liefert, bevor `build_monitor_records()` aufgerufen wird.

**Verifikation**
- Erfolgreichen Erstell-Durchlauf (Uptime-Kuma-Monitor + Pi-hole Local-DNS-Eintrag) mit der neuen Datenstruktur getestet.
- Duplikat-Erkennung für Monitorname und Monitor-URL mit der neuen Datenstruktur erfolgreich bestätigt.
- Erfolgreichen Dry-Run mit der neuen Monitor-Datenstruktur getestet.
- Fehlerfall beim Abrufen der Uptime-Kuma-Monitore erfolgreich getestet.

---

## v0.4.1
**Datum:** 2026-07-13

**Neu**
- Neues Modul `config.py` eingeführt.
- `load_env_config()` implementiert:
  - Lädt alle benötigten Umgebungsvariablen.
  - Erstellt eine strukturierte Konfiguration für:
    - Uptime Kuma
    - Pi-hole
    - Netzwerk

**Geändert**
- `main.py` verwendet jetzt ausschließlich die zentrale Konfiguration aus `config.py`.
- Alle direkten `os.getenv()`-Aufrufe aus `main.py` entfernt.
- `validate_env()` auf die neue Konfigurationsstruktur umgestellt.
- `load_dotenv()` nach `config.py` verschoben, sodass das Laden der Konfiguration vollständig gekapselt ist.

**Verifikation**
- Erfolgreichen Programmablauf mit der neuen Konfigurationsstruktur getestet.
- Dry-Run erfolgreich ausgeführt.
- Erstellung von Uptime-Kuma-Monitor und Pi-hole Local-DNS-Eintrag mit zentral geladener Konfiguration erfolgreich getestet.

---

## v0.4.0
**Datum:** 2026-07-13

**Neu**
- `try/finally` für zentrales Ressourcenmanagement in `main.py` eingeführt.
  - Verbindungsaufbau, Prüfung und der gesamte Programmablauf laufen jetzt innerhalb eines `try`-Blocks.
  - Beide Verbindungen (Uptime Kuma, Pi-hole) werden im `finally`-Block garantiert getrennt – unabhängig davon, an welcher Stelle das Programm beendet wird.

**Geändert**
- Wiederholte `disconnect_uptime_kuma()`- und `disconnect_from_pihole()`-Aufrufe an den einzelnen `return`-Stellen entfernt; das Cleanup erfolgt jetzt zentral im `finally`.
- `disconnect_uptime_kuma()` um eine `None`-Prüfung ergänzt (analog zu `disconnect_from_pihole()`), damit die Funktion auch dann sicher ausgeführt werden kann, wenn die Verbindung nie erfolgreich aufgebaut wurde.

**Verifikation**
- Erfolgreichen Programmablauf mit beiden API-Verbindungen getestet.
- Kritischen Fehlerfall getestet: Uptime-Kuma-Verbindung schlägt fehl (falsches Passwort), Pi-hole-Verbindung wurde bereits erfolgreich aufgebaut → beide Ressourcen werden trotzdem sauber freigegeben, kein Absturz.

---

## v0.3.3
**Datum:** 2026-07-12

**Neu**
- `add_local_dns_record()` implementiert:
  - Erstellt Local-DNS-Einträge über die Pi-hole REST-API.
  - Verwendet den HTTP-Endpunkt `PUT /config/dns/hosts/{record}`.
  - Prüft den erwarteten Status `201 Created`.
- Pi-hole-DNS-Erstellung in den Programmablauf integriert.
- Dry-Run um die geplante Erstellung des Pi-hole-DNS-Eintrags erweitert.

**Geändert**
- `TARGET_IP` enthält nur noch die reine IP-Adresse.
- `build_monitor_url()` ergänzt das URL-Schema für Uptime-Kuma-Monitore.
- Erfolgs- und Dry-Run-Ausgaben für Uptime Kuma und Pi-hole getrennt dargestellt.
- Erstellung läuft sequenziell (erst Uptime Kuma, dann Pi-hole), um bei Fehlern
  inkonsistente Zwischenzustände zu vermeiden.

**Verifikation**
- Uptime-Kuma-Monitor erfolgreich erstellt.
- Pi-hole-Local-DNS-Eintrag erfolgreich angelegt.
- Beide API-Verbindungen anschließend sauber beendet.

---

## v0.3.2
**Datum:** 2026-07-12

**Neu**
- `validate_pihole_dns_records()` implementiert:
  - Prüft, ob ein Hostname bereits als Local-DNS-Eintrag in Pi-hole vorhanden ist.
  - Vergleich erfolgt unabhängig von Groß- und Kleinschreibung.
  - Verhindert das Anlegen doppelter Local-DNS-Einträge.
- `build_dns_hostname()` implementiert:
  - Erstellt aus einem Servicenamen den vollständigen DNS-Hostnamen.
- DNS-Validierung in den Programmablauf (`main.py`) integriert.

**Geändert**
- `validate_env()` um die Pi-hole-Konfigurationsvariablen erweitert:
  - `PIHOLE_API_URL`
  - `PIHOLE_PASSWORD`
- Einheitliche Erstellung von DNS-Hostnamen über `build_dns_hostname()`.
- Dry-Run berücksichtigt nun die erfolgreiche DNS-Validierung.
- Dry-Run-Meldung präzisiert: zeigt jetzt explizit „Uptime-Kuma Monitor" an.

---

## v0.3.1
**Datum:** 2026-07-10

**Neu**
- `fetch_dns_records()` implementiert:
  - Local-DNS-Einträge über die Pi-hole REST-API abrufen.
  - HTTP-Status prüfen und DNS-Einträge zurückgeben.
- `parse_dns_record()` implementiert:
  - Pi-hole-DNS-Einträge in eine interne Datenstruktur (`dict`) umwandeln.
- `build_dns_records()` implementiert:
  - Aus allen Pi-hole-DNS-Einträgen eine strukturierte Liste (`list[dict]`) erstellen.
- Interne Datenstruktur für DNS-Einträge eingeführt:
  ```python
  {
      "ip": "192.168.2.x",
      "hostname": "pihole.home"
  }
  ```

**Geändert**
- `main.py` erweitert:
  - DNS-Einträge von Pi-hole abrufen.
  - API-Daten in das interne Datenmodell überführen.
- Pi-hole API-URL vereinfacht:
  - `.env` enthält jetzt die Basis-URL (`/api`).
  - API-Endpunkte werden direkt in den Funktionen ergänzt.

**Behoben**
- Reihenfolge der Pi-hole-Verarbeitung korrigiert:
  - DNS-Einträge werden nun vor dem Logout der Session abgerufen.
- API-Endpunkte vereinheitlicht und an die neue Basis-URL angepasst.
- Rückgabewert von `disconnect_uptime_kuma()` wird jetzt geprüft (war zuvor
  inkonsistent zu `disconnect_from_pihole()`, wo dies bereits der Fall war).

---

## v0.3.0
**Datum:** 2026-07-10

**Neu**
- Pi-hole REST-API in `add_service` integriert.
- `connect_to_pihole()` implementiert:
  - HTTP-Session (`requests.Session`) erstellt.
  - Authentifizierung über Pi-hole API.
  - HTTP-Status und Session-ID (SID) werden geprüft.
  - Authentifizierte Session wird für weitere API-Aufrufe bereitgestellt.
- `disconnect_from_pihole()` implementiert:
  - Pi-hole-Session wird serverseitig beendet.
  - HTTP-Status des Logout-Endpunkts wird geprüft.
  - Lokale HTTP-Session wird zuverlässig geschlossen.

**Geändert**
- `main.py` um Pi-hole-Verbindungsaufbau und Session-Management erweitert.
- `.env`-Validierung um Pi-hole-Konfigurationsvariablen ergänzt.
- Ressourcenverwaltung erweitert, sodass Uptime Kuma- und Pi-hole-Verbindungen beim Programmende oder Fehlerfall sauber beendet werden.

**Behoben**
- `disconnect_from_pihole()` konnte mit `AttributeError` abbrechen, wenn `session` `None` war (z. B. nach fehlgeschlagenem Verbindungsaufbau); Prüfung auf `None` am Funktionsanfang ergänzt.
- Fehlende `disconnect`-Aufrufe an mehreren `return`-Stellen in `main.py` ergänzt, damit bei Verbindungsfehlern bereits aufgebaute Verbindungen zu Uptime Kuma und Pi-hole sauber beendet werden.
- Logout auf den korrekten HTTP-Status `204 No Content` angepasst; erfolgreiche Sitzungsbeendigung wurde zuvor fälschlich als Fehler erkannt.

---

## v0.2.3
**Datum:** 2026-07-09

**Neu**
- `--dry-run`-Modus ergänzt.
- Simuliert die Monitor-Erstellung, ohne Änderungen an Uptime Kuma vorzunehmen.
- Verbindung zu Uptime Kuma sowie Duplikat-Prüfung werden auch im Dry-Run vollständig ausgeführt.

**Geändert**
- `main.py` um den Dry-Run-Ablauf erweitert.
- Monitor-Erstellung wird nur außerhalb des Dry-Run-Modus ausgeführt.
- `print_status()` zeigt den aktiven Dry-Run-Modus an.
- Veraltete Liste der geplanten Schritte aus `print_status()` entfernt.
- `get_uptime_monitor` zu `get_uptime_monitors` umbenannt (Plural, da alle Monitore zurückgegeben werden).

**Behoben**
- Erfolgsmeldung „Monitor erfolgreich erstellt" wurde im Dry-Run-Modus fälschlicherweise ausgegeben.

---

## v0.2.2
**Datum:** 2026-07-09

**Refactoring**
- Umstrukturierung von `add_service.py` in das Modul-Verzeichnis `add_service/`.
- Aufgeteilt in `main.py`, `parser.py`, `validation.py`, `output.py` und `uptime_kuma.py`.
- `validate_uptime_monitor` nach `validation.py` verschoben (reine Prüflogik ohne API-Kommunikation).
- Veralteten Hinweis „Simulation beendet" aus `print_status()` entfernt.
- Funktionalität unverändert – erfolgreicher Testlauf einschließlich Duplikat-Erkennung durchgeführt.

---

## v0.2.1
**Datum:** 2026-07-09

**Neu**
- Funktion zum Erstellen der Monitor-URL ergänzt.
- Abrufen vorhandener Uptime-Kuma-Monitore integriert.
- Prüfung auf bereits vorhandene Monitor-Namen und Monitor-URLs ergänzt.
- Validierung der benötigten Umgebungsvariablen (`.env`) ergänzt.

**Geändert**
- Monitor-Erstellung auf getrennte Parameter (`monitor_name`, `monitor_url`) umgestellt.
- Funktionen durch Docstrings ergänzt.
- Programmablauf für bessere Wartbarkeit überarbeitet.

**Verbessert**
- Doppelte Monitor-Erstellung wird verhindert.
- Service-Namen werden bei der Prüfung unabhängig von Groß- und Kleinschreibung verglichen.
- Fehlerbehandlung und Ablaufsteuerung weiter vereinheitlicht.

---

## v0.2.0
**Datum:** 2026-07-08

**Neu**
- Uptime-Kuma-API-Anbindung ergänzt
- Verbindung und Login zu Uptime Kuma umgesetzt
- Monitor-Erstellung über `uptime-kuma-api-v2` integriert

**Geändert**
- API-Bibliothek aufgrund eines Kompatibilitätsproblems mit Uptime Kuma 2.4.0 von `uptime-kuma-api` auf `uptime-kuma-api-v2` umgestellt.

**Details:**
`troubleshooting/log.md` → `2026-07-08 Python: add_service.py kann keinen Uptime-Kuma-Monitor erstellen`

---

## v0.1.0
**Datum:** 2026-07-07

- CLI mit `argparse` erstellt
- Eingabevalidierung für Service-Name und Port
- Simulation der Einrichtungsschritte
- Einheitliche Konsolenausgabe
- Erste Version veröffentlicht