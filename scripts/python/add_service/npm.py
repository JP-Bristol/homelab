import requests
import logging 

from output import print_ok, print_error
from error import get_http_error_message

logger = logging.getLogger(__name__)

def connect_to_npm(npm_api_url,npm_identity, npm_secret):

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
