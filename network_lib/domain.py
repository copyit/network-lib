import re

import requests


def punycode(domain, encode=True):
    if encode:
        return domain.encode("idna")
    else:
        return domain.decode("idna")


def check_cdn_provider(domain, location='global', proxy=None, timeout=5):
    location_encode = {
        'global': 'GO',
        'asia': 'AS',
        'china': 'CN',
        'north america': 'NA'
    }
    location = location_encode.get(location, location)
    api_url = 'https://www.whatsmycdn.com/?uri={}&location={}'.format(domain, location)
    resp = requests.get(api_url, proxies=proxy, timeout=timeout)
    resp_text = resp.text
    location = re.findall(
        r'<div class="six columns" style="word-wrap:break-word;">(.+)</div>',
        resp_text
    )
    provider = re.findall(
        r'<div class="six columns" style="margin-left: 2px; word-wrap:break-word;">(.+)</div>',
        resp_text
    )
    return dict(zip(location, provider))
