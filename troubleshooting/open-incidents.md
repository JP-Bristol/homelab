# Open Incidents

Aktuell bekannte, noch nicht vollständig analysierte oder gelöste Probleme.

Nach erfolgreicher Ursachenanalyse und Verifikation wird der Eintrag nach
`log.md` übernommen.

---

## 2026-07-13 — Uptime Kuma: Sporadischer Verbindungsfehler beim ersten Skriptstart

**Status:** 🟡 Offen

**Betroffen:**
- `add_service.py`
- Uptime Kuma API

### Symptom
Beim ersten Ausführen von `add_service.py` an einem Tag tritt gelegentlich ein
Verbindungsfehler zur Uptime Kuma API auf. Das Skript bricht den Verbindungsaufbau ab.
Ein erneuter Aufruf des Skripts funktioniert anschließend meist ohne Probleme.

### Beobachtungen
- Bisher nur beim ersten Skriptstart des Tages beobachtet.
- Nicht zuverlässig reproduzierbar.
- Nach einem erneuten Skriptstart funktioniert die Verbindung in der Regel.
- Das Uptime-Kuma-Webinterface ist währenddessen erreichbar.

### Aktuelle Fehlerbehandlung
Der Fehler wird durch den generischen `Exception`-Handler in `connect_to_uptime_kuma()`
abgefangen (siehe `add_service.py` v0.4.4). Folgende Informationen werden protokolliert:

- Exception-Typ (`type(err).__name__`)
- Fehlermeldung (`{err}`)

### Aktuelle Vermutungen
- Socket.IO-Verbindung ist beim ersten Verbindungsaufbau noch nicht vollständig initialisiert.
- Session-Initialisierung der verwendeten Python-Bibliothek (`uptime-kuma-api-v2`).
- Kurzzeitige Netzwerk- oder DNS-Verzögerung.
- Fehler oder Inkompatibilität der verwendeten Bibliothek.
- Uptime-Kuma-Dienst war unmittelbar zuvor noch nicht vollständig bereit (z. B. nach
  Container-Neustart über Nacht).

### Workaround
Das Skript erneut ausführen. In den bisherigen Tests konnte die Verbindung anschließend
erfolgreich hergestellt werden.

### Geplanter Fix
Nach erfolgreicher Ursachenanalyse einen Retry-Mechanismus für den Verbindungsaufbau
evaluieren (2–3 Versuche, mit kurzer Pause dazwischen). Der Retry soll ausschließlich bei
temporären Verbindungsfehlern greifen und keine Konfigurations- oder
Authentifizierungsfehler (z. B. falsches Passwort) verdecken.

### Nächste Analyse
Beim nächsten Auftreten kurz notieren (aus der bestehenden Konsolen-Ausgabe, kein Zusatzaufwand):

- [x] Exception-Typ: `TimeoutError` (Pythons eingebaute Klasse, NICHT `uptime_kuma_api.Timeout`)
- [x] Fehlermeldung: (leer/keine Nachricht)
- [x] Uhrzeit: 2026-07-13, 19:57

### Abschlusskriterien
Der Eintrag wird ins reguläre `log.md` übernommen, sobald:

- die Root Cause eindeutig identifiziert wurde,
- ein reproduzierbarer Fix vorliegt,
- und der Fix erfolgreich verifiziert wurde.

---