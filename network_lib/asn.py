import requests

def get_asn_info(asn, raw=False, timeout=10):
    try:
        resp = requests.get('https://api.bgpview.io/asn/{}'.format(asn), timeout=timeout)
        resp_json = resp.json()
        if resp_json.get('status') == 'ok':
            return resp_json.get('data')
        else:
            return
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
