import ip_request


# http_proxy = ip_request.proxy.create('http://202.57.132.77/4145')
# http_proxy.test()
# http_proxy.test('https://www.google.com', timeout=5)
# http_proxy.get_anonymity()

# ip_request.proxy.get_anonymity('http://202.57.132.77/4145')


def create(proxy_string):
    return ip_request.proxy.BaseProxy.from_string(proxy_string)


def get_anonymity(proxy_string):
    proxy_object = create(proxy_string)
    proxy_object.test()
    return proxy_object.get_anonymity()
