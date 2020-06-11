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

def get_external(protocol='', bypass_proxy=True, timeout=10):
    try:
        if protocol in ('', 'default'):
            api_url='https://api.ip.sb/ip'
        elif protocol in ('4', 'v4', 'ipv4'):
            api_url='https://api-ipv4.ip.sb/ip'
        elif protocol in ('6', 'v6', 'ipv6'):
            api_url='https://api-ipv6.ip.sb/ip'
    
        with requests.Session() as session:
            if bypass_proxy:
                session.trust_env = False
            resp = requests.get(api_url, timeout=timeout)
            return resp.text
    except Exception:
        pass

def get_external_ipv4(timeout=10):
    return get_external(protocol='ipv4', timeout=timeout)

def get_external_ipv6(timeout=10):
    return get_external(protocol='ipv6', timeout=timeout)

def get_geo_info(ip_address='', raw=False, bypass_proxy=True, timeout=10):
    try:
        with requests.Session() as session:
            if bypass_proxy:
                session.trust_env = False
            resp = requests.get('https://api.ip.sb/geoip/{}'.format(ip_address), timeout=timeout)
            if resp.status_code == 400:
                return None
            else:
                return resp.json()
    except Exception:
        raise

def get_asn(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('asn'), geo_info.get('asn_organization'), geo_info.get('organization')

def get_timezone(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('timezone')

def get_isp(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('isp')

def get_region(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('region'), geo_info.get('region_code')

def get_city(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('city')

def get_country(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('country'), geo_info.get('country_code')

def get_coordinate(ip_address='', bypass_proxy=True, timeout=10):
    geo_info = get_geo_info(ip_address=ip_address, bypass_proxy=bypass_proxy, timeout=timeout)
    if geo_info:
        return geo_info.get('longitude'), geo_info.get('latitude')

def get_rir_allocation(ip_address='', bypass_proxy=True, timeout=10):
    try:
        if not ip_address:
            ip_address = get_external(bypass_proxy=bypass_proxy, timeout=timeout)
        with requests.Session() as session:
            if bypass_proxy:
                session.trust_env = False
            resp = requests.get('https://api.bgpview.io/ip/{}'.format(ip_address), timeout=timeout)
            if resp_json.get('status') == 'ok':
                return resp_json.get('data').get('rir_allocation')
    except Exception:
        raise