import requests

def get_asn_info(asn, raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}'.format(asn), timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            return resp_json.get('data')
    except Exception:
        raise


def get_asn_name(asn, timeout=10):
    asn_info = get_asn_info(asn, timeout=timeout)
    if asn_info:
        return (
            asn_info.get('asn'), 
            asn_info.get('name'), 
            asn_info.get('description_short')
        )

def get_asn_contact(asn, timeout=10):
    asn_info = get_asn_info(asn, timeout=timeout)
    if asn_info:
        return (
            asn_info.get('email_contacts'), 
            asn_info.get('abuse_contacts'), 
            asn_info.get('website'), 
            asn_info.get('owner_address')
        )

def get_rir_allocation(asn, timeout=10):
    asn_info = get_asn_info(asn, timeout=timeout)
    if asn_info:
        rir_info = asn_info.get('rir_allocation')
        if rir_info:
            return (
                rir_info.get('rir_name'), 
                rir_info.get('country_code'), 
                rir_info.get('date_allocated')
            )

def get_asn_prefix(asn, protocol='', raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/prefixes'.format(asn), timeout=timeout)
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

def get_asn_prefix_list(asn, protocol='', timeout=10):
    asn_prefix = get_asn_prefix(asn, protocol=protocol, timeout=timeout)
    if asn_prefix:
        return [prefix.get('prefix') for prefix in asn_prefix]

def get_asn_prefix_ip(asn, protocol='', timeout=10):
    asn_prefix = get_asn_prefix(asn, protocol=protocol, timeout=timeout)
    if asn_prefix:
        return [prefix.get('ip') for prefix in asn_prefix]

def get_asn_peers(asn, protocol='', raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/peers'.format(asn), timeout=timeout)
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

def get_asn_peers_list(asn, protocol='', timeout=10):
    asn_prefix = get_asn_prefix(asn, protocol=protocol, timeout=timeout)
    if asn_prefix:
        return [prefix.get('asn') for prefix in asn_prefix]

def get_asn_peers_name(asn, protocol='', timeout=10):
    asn_prefix = get_asn_prefix(asn, protocol=protocol, timeout=timeout)
    if asn_prefix:
        return [prefix.get('name') for prefix in asn_prefix]

def get_asn_upstreams(asn, protocol='', raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/upstreams'.format(asn), timeout=timeout)
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

def get_asn_upstreams_list(asn, protocol='', timeout=10):
    asn_upstreams = get_asn_upstreams(asn, protocol=protocol, timeout=timeout)
    if asn_upstreams:
        return [upstream.get('asn') for upstream in asn_upstreams]

def get_asn_upstreams_name(asn, protocol='', timeout=10):
    asn_upstreams = get_asn_upstreams(asn, protocol=protocol, timeout=timeout)
    if asn_upstreams:
        return [upstream.get('name') for upstream in asn_upstreams]

def get_asn_downstreams(asn, protocol='', raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/downstreams'.format(asn), timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            if protocol in ('4', 'v4', 'ipv4'):
                return resp_json.get('data').get('ipv4_downstreams', [])
            elif protocol in ('6', 'v6', 'ipv6'):
                return resp_json.get('data').get('ipv6_downstreams', [])
            else:
                return resp_json.get('data').get('ipv4_downstreams', []) + resp_json.get('data').get('ipv6_downstreams', [])
    except Exception:
        raise
        
def get_asn_downstreams_list(asn, protocol='', timeout=10):
    asn_downstreams = get_asn_downstreams(asn, protocol=protocol, timeout=timeout)
    if asn_downstreams:
        return [downstream.get('asn') for downstream in asn_downstreams]

def get_asn_downstreams_name(asn, protocol='', timeout=10):
    asn_downstreams = get_asn_downstreams(asn, protocol=protocol, timeout=timeout)
    if asn_downstreams:
        return [downstream.get('name') for downstream in asn_downstreams]


def get_asn_ixs(asn, raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}/ixs'.format(asn), timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            return resp_json.get('data')
    except Exception:
        raise

def get_asn_ixs_list(asn, timeout=10):
    asn_ixs = get_asn_ixs(asn, timeout=timeout)
    if asn_ixs:
        return [ix.get('ix_id') for ix in asn_ixs]

def get_asn_ixs_name(asn, timeout=10):
    asn_ixs = get_asn_ixs(asn, timeout=timeout)
    if asn_ixs:
        return [ix.get('name') for ix in asn_ixs]
