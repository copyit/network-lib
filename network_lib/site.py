import requests


def full_url(url):
    full = requests.head(url)
    return full.headers.get('Location')


def unu(url, keyword=""):
    api_url = "https://u.nu/api.php"
    data = {
        "action": 'shorturl',
        "format": 'simple',
        "url": url,
        "keyword": keyword
    }
    short_url = requests.get(api_url, params=data)
    return short_url.text


def tinyurl(url):
    api_url = 'https://tinyurl.com/api-create.php?url={}'
    short_url = requests.get(api_url.format(url))
    return short_url.text


def gitio(url, keyword=''):
    api_url = 'https://git.io/{}'
    data = {
            'url': url, 
            'code': keyword
        }
    if url.startswith('https://github.com'):
        short_url = requests.post(api_url.format(url), data=data)
        return short_url.headers.get('Location')

