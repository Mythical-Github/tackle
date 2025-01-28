import os
import sys
import hashlib
from pathlib import Path

import requests


SCRIPT_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def download_file(url: str, destination: str) -> bool:
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return True
    except requests.exceptions.RequestException:
        return False


def calculate_sha256(file_path) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {e}"
