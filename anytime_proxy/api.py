import anytime_proxy as ap


class ProxyAPI:
    def __init__(self):
        pass

    @staticmethod
    def find():
        pass

    @staticmethod
    def save():
        pass

    @staticmethod
    def test_list(proxy_list):
        validator = ap.Validator()
        validator.run(proxy_list)
