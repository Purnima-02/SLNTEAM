# utils.py
import requests

def get_api_count(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return len(response.json())
    except requests.RequestException:
        return 0
