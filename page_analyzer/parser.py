import requests

ERROR_CODE = 500


def get_response(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # to delete
        print(f'responce \n{response}')
        print(f'content \n{response.content}')
        # --
        return {
            'status_code': response.status_code,
            'content': response.content
        }

    except requests.exceptions.RequestException:
        # to delete
        print(f'responce \n{response}')
        print(f'content \n{response.content}')
        # --
        return {
            'status_code': response.status_code,
            'content': response.content
        }


# ??? for what?
"""По идее, сначала надо получить запрос и данные по нему,
а уже после их проверять"""


def is_server_error(response):
    status_code = response['status_code']

    if status_code >= ERROR_CODE:
        return False
    else:
        return True
    # ???


def parse_content(url, id):
    response = get_response(url)
    status_code = response['status_code']
    """тут планирую обработать запрос
Не забудь снять комментарий!"""
    #    content = response['content']

    data = {
        'url_id': id,
        'status_code': status_code,
        'h1': None,
        'title': None,
        'description': None}

    return data
