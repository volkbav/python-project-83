import requests


def get_response(url):
    try:
        response = requests.get(url, timeout=1)
    except requests.exceptions.ReadTimeout:
        result = {
            'is_ok': None
        }
    else:
        result = {
            'status_code': response.status_code,
            'is_ok': response.ok
        }

    return result