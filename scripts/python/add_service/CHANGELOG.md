# Changelog — add_service

Alle nennenswerten Änderungen an `add_service.py` werden hier dokumentiert, neueste Version zuerst.

---

### v0.7.0
**Datum:** 2026-07-16

#### Neu
- Neues Modul `firewall.py` für die Anbindung an UFW (Uncomplicated Firewall) eingeführt.
- `open_service_port()` implementiert:
  - Öffnet einen TCP-Port über `subprocess.run(["sudo", "ufw", "allow", ...])`.
  - Prüft den `returncode` des Befehls (`0` = Erfolg, sonst Fehler).
  - Fehlerdetails aus `result.stderr` werden in die Fehlermeldung übernommen.
  - Fehlerbehandlung für `FileNotFoundError` (falls `ufw` oder `sudo` nicht verfügbar sind) sowie generischer `Exception`-Fallback.
- `sudoers`-Konfiguration eingerichtet (`NOPASSWD` ausschließlich für `/usr/sbin/ufw`), damit `add_service.py` Portfreigaben ohne interaktive Passworteingabe automatisieren kann.

#### Architektur
- Firewall-Funktionen bewusst in einem eigenen Modul gekapselt und damit in die bestehende Integrationsarchitektur eingeordnet.
- UFW stellt keine HTTP-API bereit; die Kommunikation erfolgt bewusst über `subprocess.run()` mit Rückgabecode-Auswertung anstelle einer Netzwerkbibliothek.

#### Hinweis
- Modul bewusst `firewall.py` statt `ufw.py` genannt, da letzteres mit dem bereits installierten Systempaket (`/usr/lib/python3/dist-packages/ufw/`) kollidierte und zu einem `ImportError` führte.
- `ufw allow` ist idempotent. Mehrfaches Ausführen mit demselben Port erzeugt weder einen Fehler noch doppelte Regeln.
- Ein expliziter Port-Duplikatcheck ist daher nicht erforderlich. Portkonflikte zwischen Services werden bereits durch `validate_uptime_monitor()` erkannt, da dort IP und Port gemeinsam geprüft werden.
- Geschützte Ports (z. B. SSH) sowie die Integration in `main.py` inklusive Dry-Run folgen in den nächsten Versionen (`v0.7.1`, `v0.7.2`).

#### Verifikation
- `open_service_port()` isoliert in der Sandbox erfolgreich getestet.
- Ergebnis mit `sudo ufw status` auf Betriebssystemebene verifiziert (IPv4- und IPv6-Regel korrekt angelegt).
- Test-Port nach erfolgreicher Verifikation wieder entfernt (`sudo ufw delete allow ...`).

### v0.6.4
**Datum:** 2026-07-16

#### Neu
- `add_proxy_host_record()` implementiert:
  - Erstellt einen neuen Proxy Host über `POST /api/nginx/proxy-hosts`.
  - Nutzt den von `build_proxy_host_payload()` erzeugten Request-Body.
  - Vollständige, differenzierte Fehlerbehandlung (`HTTPError` mit `get_http_error_message()`, `ConnectionError`, `Timeout`, generischer Fallback), analog zu den übrigen API-Funktionen.
- NPM-Erstellung in den Programmablauf (`main.py`) integriert (Phase 5), inklusive Dry-Run-Unterstützung.
- Erstellung läuft weiterhin sequenziell (Kuma → Pi-hole → NPM, jeweils nur bei Erfolg des vorherigen Schritts), um inkonsistente Zwischenzustände über alle drei Systeme hinweg zu vermeiden.
- `runbook_message` um NPM-Daten erweitert (`domain_name`, `destination`) — der Service-Log-Eintrag enthält jetzt vollständige Informationen zu allen drei Integrationen.

#### Hinweis
- NPM erwartet `forward_scheme` als Pflichtfeld; ein Test mit unvollständiger Payload (ohne `forward_scheme`) schlug mit HTTP 400 fehl und bestätigte, dass `build_proxy_host_payload()` bereits korrekt aufgebaut ist.
- Ein separater v0.6.5-Schritt für die Runbook-Log-Erweiterung entfällt, da diese direkt in v0.6.4 mit umgesetzt wurde.

#### Verifikation
- Vollständiger Programmablauf (Dry-Run) mit allen drei Integrationen erfolgreich getestet.
- Vollständiger, normaler Programmablauf (kein Dry-Run) erfolgreich getestet: Uptime-Kuma-Monitor, Pi-hole-DNS-Eintrag und NPM-Proxy-Host wurden korrekt erstellt.
- `runbook_message` mit vollständigen Daten aus allen drei Systemen in `logs/service_events.log` verifiziert.

### v0.6.3
**Datum:** 2026-07-15

#### Neu
- `build_proxy_host_payload()` implementiert:
  - Baut den vollständigen Request-Body für das Erstellen eines NPM-Proxy-Hosts.
  - Nimmt nur die drei variablen Werte (`domain_name`, `forward_host`, `forward_port`) als Parameter entgegen.
  - Restliche Payload-Felder (`forward_scheme`) als sinnvoller Default im Funktionskörper.
  - `domain_name` wird korrekt in eine Liste (`domain_names`) verpackt, `forward_port` bleibt als Ganzzahl (`int`), entsprechend der von NPM erwarteten Struktur.

#### Architektur
- Trennung zwischen variablen und statischen Payload-Daten eingeführt:
  - Variablen werden über Funktionsparameter übergeben.
  - Statische Standardwerte werden zentral innerhalb der Funktion definiert.
- Neue Payload-Optionen können künftig ergänzt werden, ohne bestehende Aufrufer (`main.py`) anzupassen.

#### Hinweis
- Payload-Struktur wurde über den Browser-Network-Tab beim manuellen Anlegen eines Proxy Hosts in der NPM-UI ermittelt.
- Bewusst nur die minimal notwendigen Felder übernommen, statt aller 17 Felder aus der UI-Payload (YAGNI-Prinzip). Weitere Optionen werden erst ergänzt, wenn sie im Homelab tatsächlich benötigt werden.

#### Verifikation
- Erster eigener Unit-Test (`pytest`) für `build_proxy_host_payload()` geschrieben und erfolgreich ausgeführt:
  - Prüft korrekten Feldnamen (`domain_names` statt `domain_name`).
  - Prüft korrekten Wert für `forward_host`.
  - Prüft korrekten Wert für `forward_port`.
  - Prüft explizit den Datentyp von `forward_port` (`int` statt `str`).
- Test lebt aktuell noch im Verzeichnis `sandbox/` und wird beim Aufbau der Test-Infrastruktur (nach v1.0) in einen eigenen `tests/`-Ordner überführt.

### v0.6.2
**Datum:** 2026-07-15

#### Neu
- `validate_npm_proxy_hosts()` implementiert:
  - Prüft, ob eine Domain bereits als NPM-Proxy-Host vorhanden ist.
  - Der Vergleich erfolgt unabhängig von Groß- und Kleinschreibung.
  - Die NPM-Duplikatprüfung wurde in den Programmablauf (`main.py`, Phase 4: Duplikate prüfen) integriert.

#### Geändert
- `build_dns_hostname()` aus `pihole.py` entfernt und durch die gemeinsame Funktion `build_hostname()` in `config.py` ersetzt.
  - Wird jetzt sowohl für Pi-hole-Hostnamen als auch für NPM-Domain-Namen verwendet.
  - Identische `.home`-Konvention wird dadurch zentral verwaltet; doppelte Logik entfällt.
- `main.py` verwendet jetzt durchgängig die zentrale Variable `hostname` anstelle separater Variablen wie `pihole_hostname`.

#### Architektur
- Zentrale `build_hostname()` in `config.py` verhindert künftige Duplikation, falls weitere Services (z. B. UFW) dieselbe `.home`-Konvention benötigen.
- NPM folgt jetzt derselben Validierungspipeline wie Uptime Kuma und Pi-hole:

```
build → validate
```

#### Hinweis
- NPM verhindert das Anlegen doppelter Domains bereits serverseitig (durch manuellen Test bestätigt).
- Die zusätzliche Validierung sorgt für eine kontrollierte und konsistente Fehlermeldung, bevor der serverseitige Fehler auftritt – analog zum Verhalten bei Uptime Kuma und Pi-hole.
- Der Dry-Run-Hinweis für NPM (`[INFO] Würde NPM Proxy Host erstellen`) wird bewusst erst zusammen mit der eigentlichen Erstellungsfunktion in v0.6.4 ergänzt, um das bisherige Vorgehen bei den anderen Integrationen beizubehalten.

#### Verifikation
- Duplikat-Fall (Domain bereits vorhanden) erfolgreich getestet: korrekter Programmabbruch mit verständlicher Fehlermeldung.
- Neu-Fall (Domain noch nicht vorhanden) erfolgreich getestet: Ablauf läuft bis zum Ende des Dry-Runs ohne Fehler durch.
- Vollständiger Programmablauf (kein Dry-Run) mit der zentralen `build_hostname()`-Funktion erfolgreich getestet: Uptime-Kuma-Monitor und Pi-hole-DNS-Eintrag werden weiterhin korrekt erstellt.


### v0.6.1
**Datum:** 2026-07-15

#### Neu
- `fetch_proxy_hosts()` implementiert:
  - Ruft alle Proxy-Host-Einträge über `GET /api/nginx/proxy-hosts` ab.
  - Gibt die Response direkt als Liste zurück (im Gegensatz zu Pi-hole keine verschachtelte Struktur, kein zusätzliches Auslesen von Unter-Keys nötig).
- `parse_proxy_host_record()` implementiert:
  - Wandelt einen rohen NPM-Proxy-Host in eine schlanke interne Struktur um (`id`, `domain_name`, `forward_host`, `forward_port`).
  - Nimmt nur die erste Domain aus `domain_names` (Liste), da pro Service aktuell nur eine Domain vorgesehen ist.
- `build_proxy_host_records()` implementiert:
  - Erstellt aus allen Proxy-Host-Einträgen eine strukturierte Liste, analog zu `build_dns_records()` und `build_monitor_records()`.
- `main.py` um Abruf und Aufbereitung der NPM-Proxy-Hosts erweitert (Phase 3: Daten abrufen).

#### Geändert
- Interne Datenstruktur für NPM-Proxy-Hosts eingeführt:
  ```python
  {
      "id": 1,
      "domain_name": "zabbix.home",
      "forward_host": "192.168.2.x",
      "forward_port": 8080
  }
  ```
- NPM folgt jetzt derselben Datenpipeline wie Uptime Kuma und Pi-hole:
  ```
  fetch → parse → build
  ```

#### Verifikation
- Vollständiger Programmablauf (Dry-Run) mit allen drei Datenquellen (Uptime-Kuma-Monitore, Pi-hole-DNS-Einträge, NPM-Proxy-Hosts) erfolgreich getestet.
- `[DEBUG]`-Ausgabe bestätigt die korrekte Anzahl geladener Proxy-Host-Einträge.
- Interne Proxy-Host-Datenstruktur mit mehreren vorhandenen Proxy-Hosts erfolgreich verifiziert.

### v0.6.0
**Datum:** 2026-07-15

#### Neu
- Neues Modul `npm.py` für die Anbindung an Nginx Proxy Manager eingeführt.
- `connect_to_npm()` implementiert:
  - Authentifizierung über `POST /api/tokens` mit `identity`/`secret` (JWT-basiert, im Gegensatz zu Pi-holes Session-ID).
  - Token wird aus der Response extrahiert und als `Authorization: Bearer <token>`-Header für alle weiteren Requests gesetzt.
  - Vollständige, differenzierte Fehlerbehandlung (`HTTPError` mit `get_http_error_message()`, `ConnectionError`, `Timeout`, generischer Fallback), analog zu Pi-hole.
- `disconnect_from_npm()` implementiert:
  - Beendet die Session über `DELETE`-Request (im Network-Tab verifiziert, Status 200 bestätigt).
- `config.py` um NPM-Konfiguration erweitert (`api_url`, `identity`, `secret`).
- `main.py` um NPM-Verbindungsaufbau, -Prüfung und -Trennung erweitert (Phase 1, 2, 6).

#### Geändert
- `validate_env()` refaktoriert:
  - Prüfung der Umgebungsvariablen erfolgt jetzt über eine verschachtelte Schleife statt über einzelne `if`-Blöcke.
  - Neue Services können durch Erweiterung der Konfiguration eingebunden werden, ohne die Validierungslogik anzupassen.

#### Hinweis
- Für Nginx Proxy Manager existiert keine offizielle API-Dokumentation.
- Die verwendeten Endpunkte wurden anhand einer Community-Postman-Dokumentation sowie über die Browser-Entwicklertools (Network-Tab) beim manuellen Login und Logout analysiert und verifiziert.

#### Verifikation
- Vollständiger Programmablauf (Dry-Run) mit allen drei Verbindungen (Kuma, Pi-hole, NPM) erfolgreich getestet.
- Erfolgreicher Login-Test mit echtem JWT-Token bestätigt.
- Erfolgreicher Logout-Test (Status 200) bestätigt.
- `validate_env()`-Schleife mit fehlender Umgebungsvariable getestet, korrekte Fehlermeldung (`service.feld ist nicht gesetzt`) bestätigt.


### v0.5.2
**Datum:** 2026-07-14

#### Neu
- Separater `runbook_logger` (`logging.getLogger("runbook_data")`) eingeführt:
  - Eigener `FileHandler` für `logs/service_events.log`.
  - `propagate = False`, damit Einträge ausschließlich in dieser Datei landen, nicht zusätzlich in `logs/service.log` oder der Konsole.
- Strukturiertes `key=value`-Format (logfmt-Stil) für erfolgreich angelegte Services:

```
service=zabbix | monitor_url=http://192.168.2.90:123 port=123 | dns_hostname=zabbix.home ip=192.168.2.90
```

  - Dient als maschinenlesbare Datenquelle für den späteren Runbook Agent.
  - Flaches Format (ohne Gruppierung) gewählt, um das Parsen zu vereinfachen — ein Parser muss nur nach `key=value`-Mustern suchen, ohne verschachtelte Struktur zu berücksichtigen.
- Log-Eintrag wird ausschließlich bei tatsächlicher, erfolgreicher Erstellung geschrieben (nicht im Dry-Run-Modus).

#### Architektur
- Technisches Logging (`service.log`) und fachliche Ereignisprotokollierung (`service_events.log`) vollständig voneinander getrennt.
- Das Runbook-Log enthält ausschließlich strukturierte Informationen über erfolgreich angelegte Services und dient als Grundlage für die spätere Runbook-Generierung.

#### Verifikation
- Vollständiger Programmablauf (normale Ausführung) getestet: `service.log` enthält alle Schritte, `service_events.log` enthält ausschließlich den strukturierten Event-Eintrag.
- Bestätigt: `service_events.log` bleibt bei Dry-Run-Läufen leer.
- Trennung zwischen beiden Log-Dateien (kein Vermischen) erfolgreich bestätigt.

### v0.5.1
**Datum:** 2026-07-14

#### Geändert
- `output.py`: Die Ausgabe-Helper (`print_ok()`, `print_error()`, `print_warning()`, `print_info()`, `print_debug()`) erwarten jetzt einen `logger` als ersten Parameter und nutzen intern das Python-`logging`-Modul anstelle von `print()`.
- `print_status()` bleibt bewusst unverändert und verwendet weiterhin `print()`, da die Funktion ausschließlich der visuellen Konsolenausgabe (Header, Rahmen) dient und nicht Bestandteil des strukturierten Loggings ist.
- Alle Aufrufer (`main.py`, `pihole.py`, `uptime_kuma.py`) übergeben jetzt ihren modulspezifischen Logger (`logging.getLogger(__name__)`) an die Ausgabe-Helper.
- Log-Formatierung um feste Spaltenbreiten ergänzt (`%(levelname)-7s`, `%(name)-12s`) für bessere Lesbarkeit beim Überfliegen der Log-Datei.

#### Architektur
- Trennung zwischen visueller Konsolenausgabe und strukturiertem Logging weiter ausgebaut:
  - Status-Header bleiben reine CLI-Ausgabe.
  - Fachliche Informationen, Warnungen, Fehler und Debug-Ausgaben werden über das Logging-System verarbeitet.
- Durch die Verwendung von `logging.getLogger(__name__)` enthält jede Log-Nachricht automatisch den Namen des erzeugenden Moduls.

#### Verifikation
- Vollständigen Programmablauf (Dry-Run und Duplikat-Fall) mit angebundenem Logging erfolgreich getestet.
- `logs/service.log` enthält strukturierte Einträge mit Zeitstempel, Log-Level und passendem Modulnamen (`pihole`, `uptime_kuma`, `__main__`).
- `DEBUG`-Nachrichten erscheinen wie vorgesehen ausschließlich auf der Konsole und werden nicht in die Logdatei geschrieben.

### v0.5.0
**Datum:** 2026-07-14

#### Neu
- `logging_config.py` eingeführt:
  - `setup_logging()` konfiguriert den Python-Root-Logger zentral mit zwei Handlern:
    - `StreamHandler` (Konsole), Level `DEBUG`
    - `FileHandler` (`logs/service.log`), Level `INFO`
  - Formatter für die Log-Datei: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
  - Absicherung gegen doppelte Handler bei mehrfachem Aufruf (`if logger.handlers: return logger`)
  - Log-Level von Drittanbieter-Bibliotheken (`requests`, `urllib3`) auf `WARNING` gedämpft, um deren interne HTTP-Debug-Ausgaben aus Konsole und Datei fernzuhalten.
- Jedes Modul (`main.py`, `pihole.py`, `uptime_kuma.py`) holt sich über `logging.getLogger(__name__)` einen eigenen, automatisch benannten Logger.
  - Durch die Root-Logger-Konfiguration erben alle Modul-Logger automatisch dieselben Handler, ohne eigene Konfiguration.
- `datefmt="%Y-%m-%d %H:%M:%S"` ergänzt, um Millisekunden aus dem Zeitstempel zu entfernen.

#### Geändert
- `setup_logging()` wird einmalig zentral in `main.py` aufgerufen (nicht in den einzelnen Modulen).

#### Verifikation
- Grundfunktion isoliert in der Sandbox getestet (Logger-Vererbung über Root-Logger, Level-Filterung DEBUG nur Konsole).
- Vollständiger Programmablauf (Dry-Run) in der echten Struktur getestet: Konsolen-Ausgabe unverändert zu vorher, `logs/service.log` erhält strukturierte Einträge mit Zeitstempel und korrektem Modulnamen.
- Drittanbieter-Log-Rauschen (`requests`/`urllib3` HTTP-Debug-Meldungen) erfolgreich unterdrückt.

#### Bekannt / Offen
- `output.py`s Ausgabe-Helper (`print_ok()`, `print_error()`, etc.) nutzen noch `print()`, nicht die neuen Logger — Anbindung folgt in v0.5.1.

### v0.4.5
**Datum:** 2026-07-14

#### Geändert
- Kommentar-Struktur in `main.py` vereinheitlicht:
  - `# 1. Verbindungen herstellen`, `# 2. Verbindungen prüfen`, `# 3. Daten abrufen`,
    `# 4. Duplikate prüfen`, `# 5. Ressourcen erstellen`, `# 6. Verbindungen trennen`
- Variablennamen vereinheitlicht:
  - `api` → `session_uptime_kuma`
  - `session` → `session_pihole`
  - `parsed_records` → `dns_records` (nach `build_*()` entstehen fertige Datenobjekte, keine "geparsten" Daten mehr)
- Funktionsparameter korrigiert:
  - `parse_monitor_record(monitors)` → `parse_monitor_record(monitor)` (Parser erhält immer ein einzelnes Objekt, nicht die Liste)
- Schreibweisen projektweit vereinheitlicht:
  - **Pi-hole** (durchgehend mit Bindestrich, statt „Pihole“/„Pi-Hole“)
  - **Uptime Kuma** (mit Leerzeichen als Basisform)
  - **Uptime-Kuma-Monitor(e)**, **Uptime-Kuma-Session**, **Uptime-Kuma-Verbindung** (durchgekoppelt als zusammengesetzte Begriffe)
  - **Pi-hole DNS-Eintrag/-Einträge**
- Alle verbliebenen rohen `print()`-Aufrufe (in `validation.py`, `output.py`) auf die Ausgabe-Helper aus v0.4.3 umgestellt.
- Meldungstexte durchgängig überarbeitet: vollständige, kontextbezogene Aussagen statt Textfragmenten (z. B. „Uptime Kuma Monitors“ → „Uptime-Kuma-Monitore konnten nicht abgerufen werden“).
- Doppelte Präfixe entfernt (z. B. „Fehler: “ im Text, wo `print_error()` das Präfix bereits automatisch ergänzt).

#### Verifikation
- Vollständiger Programmablauf (normale Ausführung, kein Dry-Run) nach allen Umbenennungen erfolgreich getestet.
- Alle Konsolen-Meldungen auf durchgängige `[OK]`/`[INFO]`/`[ERROR]`-Formatierung und einheitliche Schreibweisen geprüft.

#### Bekannt / Offen
- Parameter-Namen `session`/`api` in `pihole.py`/`uptime_kuma.py` bewusst NICHT umbenannt: 
  Dateikontext macht die Zugehörigkeit bereits eindeutig.
- `validate_env()` nutzt weiterhin sechs einzelne `if`-Blöcke statt einer Schleife.

### v0.4.4
**Datum:** 2026-07-13

#### Neu
- `errors.py` eingeführt:
  - `HTTP_STATUS_MESSAGES` — Lookup-Tabelle für verständliche HTTP-Status-Meldungen (400, 401, 403, 404, 500).
  - `get_http_error_message()` — übersetzt einen HTTP-Status-Code in eine lesbare Meldung, mit Fallback für unbekannte Codes.
- Differenzierte Fehlerbehandlung in allen API-Funktionen eingeführt, statt eines generischen `except Exception`:
  - **Pi-hole** (`connect_to_pihole()`, `disconnect_from_pihole()`, `fetch_dns_records()`, `add_local_dns_record()`):
    - `requests.exceptions.HTTPError` (mit `get_http_error_message()`)
    - `requests.exceptions.ConnectionError`
    - `requests.exceptions.Timeout`
    - `KeyError` (nur bei `fetch_dns_records()`, für unerwartetes Antwortformat)
    - generischer `Exception`-Fallback
  - **Uptime Kuma** (`connect_to_uptime_kuma()`, `get_uptime_monitors()`, `add_uptime_monitor()`, `disconnect_uptime_kuma()`):
    - `Timeout` (Unterklasse von `UptimeKumaException`)
    - `UptimeKumaException`
    - generischer `Exception`-Fallback
- `response.raise_for_status()` ersetzt die bisherige manuelle Status-Code-Prüfung (`if response.status_code != 200`) in allen Pi-hole-Funktionen.

#### Geändert
- Alle acht API-Funktionen (vier Pi-hole, vier Kuma) geben jetzt konsistent `None` (bei datenliefernden Funktionen) bzw. `False` (bei aktionsausführenden Funktionen) zurück.
- Fehlermeldungen sind jetzt kontextspezifisch pro Funktion formuliert (z. B. „Monitor konnte nicht erstellt werden“ statt einer generischen Meldung für alle Kuma-Funktionen).
- Verbleibende rohe `print()`-Aufrufe in `pihole.py` und `uptime_kuma.py` auf die Ausgabe-Helper aus v0.4.3 umgestellt.

#### Verifikation
- Vollständiger Ablauf (Dry-Run) mit allen acht überarbeiteten Funktionen erfolgreich getestet.
- `HTTPError`-Fall (falsches Pi-hole-Passwort, 401) erfolgreich mit verständlicher Meldung bestätigt.
- `KeyError`-Fall (künstlich fehlerhafte JSON-Struktur) erfolgreich getestet.
- `UptimeKumaException`-Fall (falsches Kuma-Passwort) erfolgreich mit Bibliotheks-Fehlermeldung bestätigt.

#### Bekannt / Offen
- Vereinzelt (nicht reproduzierbar) tritt beim ersten Skriptstart des Tages ein Verbindungsfehler zu Uptime Kuma auf, der aktuell nur vom generischen `Exception`-Block aufgefangen wird. `connect_to_uptime_kuma()` protokolliert versuchsweise den Exception-Typnamen (`type(err).__name__`), um die genaue Ursache beim nächsten Auftreten zu identifizieren.
- Retry-Mechanismus für `connect_to_uptime_kuma()` als möglicher Fix vorgemerkt (noch nicht umgesetzt).


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