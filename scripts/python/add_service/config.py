import os
from dotenv import load_dotenv

load_dotenv()

def load_env_config():
    """Lädt alle benötigten Umgebungsvariablen als strukturiertes Dict."""
    return {
        "kuma": {
            "url": os.getenv("KUMA_URL"),
            "username": os.getenv("KUMA_USERNAME"),
            "password": os.getenv("KUMA_PASSWORD")
        },
        "pihole": {
            "api_url": os.getenv("PIHOLE_API_URL"),
            "password": os.getenv("PIHOLE_PASSWORD")
        },
        "network": {
            "target_ip": os.getenv("TARGET_IP")
        }
    }


