"""
1. нет проверки, что данный сайт уже в БД

"""
from urllib.parse import urlparse


def normilize_url(url):
    parsed_url = urlparse(url)
    scheme_url = parsed_url.scheme
    netloc_url = parsed_url.netloc
    
    return f'{scheme_url}://{netloc_url}'


def url_validate(url):
    parsed_url = urlparse(url)

    if not url:
        return {'name': 'URL пустой'}
    elif len(url) > 255:
        return {'name': 'URL слишком длинный'}
    
    if not parsed_url.scheme or not parsed_url.netloc:
        return {'name': 'Некорректный URL'}
    
    return {}
