import json
import os
import requests

def fetch_source(url: str, save_path: str) -> str:
    """Fetch raw text/JSON from URL and save locally."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return save_path


def load_local(path: str):
    """Load local file as JSON or text."""
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return txt

