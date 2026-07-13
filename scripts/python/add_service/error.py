HTTP_STATUS_MESSAGES = {
    400: "Ungültige Anfrage",
    401: "Authentifizierung fehlgeschlagen",
    403: "Zugriff verweigert",
    404: "Ressource nicht gefunden",
    500: "Interner Serverfehler",
}

def get_http_error_message(status_code):
    """Übersetzt einen HTTP-Status-Code in eine verständliche Meldung."""
    return HTTP_STATUS_MESSAGES.get(status_code, ...)