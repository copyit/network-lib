import requests
import socket


def get_hostname():
    return socket.gethostname()


def get_internal():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        raise
    finally:
        if s:
            s.close()


def get_external(protocol='', proxy=None, timeout=10):
    try:
        if protocol in ('', 'default'):
            api_url = 'https://api.ip.sb/ip'
        elif protocol in ('4', 'v4', 'ipv4'):
            api_url = 'https://api-ipv4.ip.sb/ip'
        elif protocol in ('6', 'v6', 'ipv6'):
            api_url = 'https://api-ipv6.ip.sb/ip'
        else:
            return

        resp = requests.get(api_url, proxies=proxy, timeout=timeout)
        return resp.text

    except Exception:
        raise


def get_geo_info(ip_address='', items='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.ip.sb/geoip/{}'.format(ip_address), proxies=proxy, timeout=timeout)
        resp_json = resp.json()

        if resp.status_code == 400:
            return None
        elif not items:
            return resp_json
        elif hasattr(items, "__iter__"):
            return (resp_json.get(_) for _ in items)
        else:
            return resp_json.get(items)
    except Exception:
        raise


def get_rir_allocation(ip_address, proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/ip/{}'.format(ip_address), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            return resp_json.get('data').get('rir_allocation')
    except Exception:
        raise
