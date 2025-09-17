import requests
from bs4 import BeautifulSoup

ERROR_CODE = 500


def parse_content(url, url_id):
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return {
            'url_id': url_id,
            'status_code': response.status_code,
            'h1': None,
            'title': None,
            'description': None
        }
    soup = BeautifulSoup(response.text, "html.parser")

    h1 = soup.h1.get_text(strip=True) if soup.h1 else None
    title = soup.title.get_text(strip=True) if soup.title else None
    description_tag = soup.find("meta", attrs={"name": "description"})
    
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



