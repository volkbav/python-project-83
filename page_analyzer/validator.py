from urllib.parse import urlparse


# приведение url к нормальному виду
def normilize_url(url):
    parsed_url = urlparse(url)
    scheme_url = parsed_url.scheme
    netloc_url = parsed_url.netloc
    
    return f'{scheme_url}://{netloc_url}'


# проверка url
def url_validate(url):
    parsed_url = urlparse(url)

    # проверка на длину url
    if not url:
        return {'name': 'URL пустой'}
    elif len(url) > 255:
        return {'name': 'URL слишком длинный'}
    
    # проверка типа соединения
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        return {'name': 'Некорректный URL'}
    
    return {}
