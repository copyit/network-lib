import anytime_proxy as ap


class ProxyAPI:
    def __init__(self):
        pass

    def find(self):
        pass

    def save(self):
        pass

    def test_list(self, proxy_list):
        validator = ap.Validator()
        validator.run(proxy_list, print)

    def gather(self):
        pass
