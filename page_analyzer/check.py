import requests


def get_response(url):
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()

        return {
            'status_code': response.status_code,
            'is_ok': True
        }

    except requests.exceptions.RequestException:
        return {
            'status_code': None,
            'is_ok': False
        }
    
