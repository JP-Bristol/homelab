# Contributing

Dieses Dokument beschreibt die Konventionen, die in diesem Repository verwendet werden — vor allem für Commit-Messages. Es dient primär der eigenen Nachvollziehbarkeit über die Projektlaufzeit hinweg.

## Commit-Präfixe

| Präfix | Bedeutung |
|---|---|
| `feat:` | Neue oder erweiterte Funktionalität |
| `fix:` | Bugfix |
| `doku:` | Dokumentation |
| `services:` | Neuer Service deployed |
| `scripts:` | Python/Bash Scripts (kleinere Änderungen) |
| `config:` | Konfiguration |
| `cleanup:` | Aufräumen / Entfernen bestehender Struktur |
| `chore:` | Housekeeping / Infrastruktur-Pflege (z. B. `.gitignore`) |
| `security:` | Security-Änderungen |
| `backup:` | Backup-bezogen |
| `refactor:` | Code-Umbau ohne Verhaltensänderung |

## Abgrenzung `cleanup:` vs. `chore:`

- `cleanup:` — etwas wird aktiv entfernt oder umstrukturiert (z. B. alte Dateien löschen, Ordner umbauen)
- `chore:` — etwas wird gepflegt/ergänzt, ohne bestehende Struktur zu verändern (z. B. neue `.gitignore`-Zeile)

## Format

```
<präfix>: <kurze beschreibung>
```

Beispiel:
```
feat: add_service v0.3.3 pihole dns eintrag erstellen implementiert
```

## Versionierung (Python-Scripts)

Scripts wie `add_service.py` werden inkrementell versioniert (v0.1, v0.2, ...), mit einem Changelog pro Script in `scripts/python/README.md`. Jede Version ist einzeln testbar und wird vor dem nächsten Schritt verifiziert.