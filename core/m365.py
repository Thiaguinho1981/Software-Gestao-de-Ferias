import requests
from config import settings


def get_token():
    url = f"https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/token"

    data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }

    r = requests.post(url, data=data, timeout=15)
    r.raise_for_status()
    return r.json()["access_token"]


def bloquear_usuario_m365(email: str):
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "accountEnabled": False
    }

    url = f"https://graph.microsoft.com/v1.0/users/{email}"
    r = requests.patch(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()


def desbloquear_usuario_m365(email: str):
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "accountEnabled": True
    }

    url = f"https://graph.microsoft.com/v1.0/users/{email}"
    r = requests.patch(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()