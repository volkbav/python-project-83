import requests
from bs4 import BeautifulSoup

TIMEOUT_CODE = 504


# парсер запроса
def parse_content(url, url_id):
    # пробуем получить данные запроса по принятому url
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return {
            'url_id': url_id,
            'status_code': TIMEOUT_CODE,
            'h1': None,
            'title': None,
            'description': None
        }
    # обрабатываем данные запроса
    # только текст
    soup = BeautifulSoup(response.text, "html.parser")

    # парсим заголовки 1 уровня
    h1 = soup.h1.get_text(strip=True) if soup.h1 else None
    # парсим названия
    title = soup.title.get_text(strip=True) if soup.title else None
    # ищем теги с описаниями
    description_tag = soup.find("meta", attrs={"name": "description"})
    # собираем данные из описания
    if description_tag and description_tag.has_attr("content"):
        description = description_tag["content"].strip()
    else:
        description = None
    
    return {
        'url_id': url_id,
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description
        }



