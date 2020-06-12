import requests


def get_asn_info(asn, items='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') != 'ok':
            return None
        elif not items:
            return resp_json.get('data')
        elif hasattr(items, "__iter__"):
            return (resp_json.get(_) for _ in items)
        else:
            return resp_json.get(items)
    except Exception:
        raise


def get_asn_prefix(asn, protocol='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/prefixes'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            if protocol in ('4', 'v4', 'ipv4'):
                return resp_json.get('data').get('ipv4_prefixes', [])
            elif protocol in ('6', 'v6', 'ipv6'):
                return resp_json.get('data').get('ipv6_prefixes', [])
            else:
                return resp_json.get('data').get('ipv4_prefixes', []) + resp_json.get('data').get('ipv6_prefixes', [])
    except Exception:
        raise


def get_asn_peers(asn, protocol='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/peers'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            if protocol in ('4', 'v4', 'ipv4'):
                return resp_json.get('data').get('ipv4_peers', [])
            elif protocol in ('6', 'v6', 'ipv6'):
                return resp_json.get('data').get('ipv6_peers', [])
            else:
                return resp_json.get('data').get('ipv4_peers', []) + resp_json.get('data').get('ipv6_peers', [])
    except Exception:
        raise


def get_asn_upstreams(asn, protocol='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/upstreams'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            if protocol in ('4', 'v4', 'ipv4'):
                return resp_json.get('data').get('ipv4_upstreams', [])
            elif protocol in ('6', 'v6', 'ipv6'):
                return resp_json.get('data').get('ipv6_upstreams', [])
            else:
                return resp_json.get('data').get('ipv4_upstreams', []) + resp_json.get('data').get('ipv6_upstreams', [])
    except Exception:
        raise


def get_asn_downstreams(asn, protocol='', proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/downstreams'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            if protocol in ('4', 'v4', 'ipv4'):
                return resp_json.get('data').get('ipv4_downstreams', [])
            elif protocol in ('6', 'v6', 'ipv6'):
                return resp_json.get('data').get('ipv6_downstreams', [])
            else:
                return resp_json.get('data').get('ipv4_downstreams', []) + resp_json.get('data').get('ipv6_downstreams',
                                                                                                     [])
    except Exception:
        raise


def get_asn_ixs(asn, proxy=None, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/ixs'.format(asn), proxies=proxy, timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            return resp_json.get('data')
    except Exception:
        raise
