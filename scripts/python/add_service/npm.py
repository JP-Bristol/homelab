import requests
import logging 

from output import print_ok, print_error, print_debug
from error import get_http_error_message

logger = logging.getLogger(__name__)

def connect_to_npm(npm_api_url,npm_identity, npm_secret):

    """Stellt eine Verbindung zur NPM-API her, authentifiziert den Benutzer und gibt eine vorbereitete HTTP-Session zurück"""

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    try:
        login_json = {
            "identity": npm_identity,
            "secret": npm_secret
        }
        response = session.post(f"{npm_api_url}/tokens", json=login_json)
        response.raise_for_status()


        data = response.json()
        token = data.get("token")

        if token is None:
            print_error(logger,"Kein gültiger Token erhalten")
            return None
        
        session.headers.update({"Authorization": f"Bearer {token}"})
        print_ok(logger,"Verbindung zu NPM erfolgreich")
       
        return session

    except requests.exceptions.HTTPError as err:
        session.close() 
        message = get_http_error_message(err.response.status_code)
        print_error(logger,f"NPM: {message} (HTTP {err.response.status_code})")
        return None

    except requests.exceptions.ConnectionError as err:
        session.close() 
        print_error(logger,f"Verbindung zu NPM fehlgeschlagen: {err}")
        return None  
    
    except requests.exceptions.Timeout as err:
        session.close() 
        print_error(logger,f"Zeitüberschreitung bei der Verbindung zu NPM: {err}")
        return None      

    except Exception as err:
        session.close()
        print_error(logger,f"Unbekannter Fehler: {err}")
        return None
    
def disconnect_from_npm(npm_api_url,session):

    """ Beendet die NPM-Session über die API und schließt die lokale HTTP-Session. """

    if session is None:
        return False
    
    try:
        response = session.delete(f"{npm_api_url}")
        response.raise_for_status()

        print_ok(logger,"Verbindung zu NPM getrennt")
        return True

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(logger,f"NPM: {message} (HTTP {err.response.status_code})")
        return False

    except requests.exceptions.ConnectionError as err:
        print_error(logger,f"Verbindung vom NPM konnte nicht getrennt werden: {err}")
        return False
        
    except requests.exceptions.Timeout as err:
        print_error(logger,f"Zeitüberschreitung bei der Trennung vom NPM: {err}")
        return False     

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return False

    finally:
        session.close()

def fetch_proxy_hosts(npm_api_url, session):

    """ Ruft alle Proxy-Hosts-Einträge von der NPM-API ab und gibt sie als Liste zurück. """

    try:
        response = session.get(f"{npm_api_url}/nginx/proxy-hosts")
        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(logger,f"NPM: {message} (HTTP {err.response.status_code})")
        return None

    except requests.exceptions.ConnectionError as err:
        print_error(logger,f"Verbindung zu NPM fehlgeschlagen: {err}")
        return None

    except requests.exceptions.Timeout as err:
        print_error(logger,f"Zeitüberschreitung beim Abrufen der Proxy-Host-Einträge: {err}")
        return None

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return None


def parse_proxy_host_record(proxy_host):

    """ Wandelt einen NPM-Proxy-Host-Eintrag in ein Dictionary mit id, domain_name, forward_host und forward_port um. """

    return {
        "id": proxy_host["id"],
        "domain_name": proxy_host["domain_names"][0],
        "forward_host": proxy_host["forward_host"],
        "forward_port": proxy_host["forward_port"]
    }

def build_proxy_host_records(records):

    """ Erstellt aus allen NPM-Proxy-Host-Einträgen eine strukturierte Liste von Dictionaries. """

    proxy_host_records = [parse_proxy_host_record(record) for record in records]
    return proxy_host_records

def build_proxy_host_payload(domain_name, forward_host, forward_port):
    
    """Baut den Request-Body für das Erstellen eines NPM-Proxy-Hosts."""

    return {
        "domain_names": [domain_name],
        "forward_scheme": "http",
        "forward_host": str(forward_host),
        "forward_port": forward_port 
    }

def add_proxy_host_record(session, npm_api_url, payload):

    """ Erstellt einen NPM-Proxy-Host-Eintrag über die NPM REST-API."""

    try:
        response = session.post(f"{npm_api_url}/nginx/proxy-hosts", 
                                json=payload)
        response.raise_for_status()
        return True

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(logger,f"NPM: {message} (HTTP {err.response.status_code})")
        return False

    except requests.exceptions.ConnectionError as err:
        print_error(logger,f"Datenübertragung zu NPM fehlgeschlagen: {err}")
        return False

    except requests.exceptions.Timeout as err:
        print_error(logger,f"Zeitüberschreitung beim Übertragen des NPM-Proxy-Host-Eintrags: {err}")
        return False

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return False