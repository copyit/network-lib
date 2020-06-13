import requests
import network_lib


def validate(proxy, url='http://httpbin.org/get', timeout=5):
    requests_proxy = {
        'http': proxy,
        'https': proxy
    }

    resp = requests.get(url, proxies=requests_proxy, timeout=timeout)
    return resp.status_code == 200


def anonymity(proxy, timeout=5):
    url = 'http://httpbin.org/get'
    real_ip = network_lib.ip.get_external()
    requests_proxy = {
        'http': proxy,
        'https': proxy
    }

    resp = requests.get(url, proxies=requests_proxy, timeout=timeout)
    resp_json = resp.json()
    x_forwarded_for = resp_json.get("headers", dict()).get("X-Forwarded-For", None)

    if real_ip in x_forwarded_for:
        proxy.anonymity = 0
    elif not x_forwarded_for:
        proxy.anonymity = 2
    else:
        proxy.anonymity = 1
