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
