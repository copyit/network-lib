import unittest
import anytime_proxy as ap


class TestValidator(unittest.TestCase):
    def test_fetch(self):
        proxy_list = [
            ap.BaseProxy('http', '80.187.140.26', '8080')
        ]
        validator = ap.Validator()
        validator.run(proxy_list)
        for proxy in proxy_list:
            print(proxy.to_dict())

    def test_bulk(self):
        proxy_list = [
            ap.BaseProxy('http', '3.211.17.212', '80'),
            ap.BaseProxy('http', '80.187.140.26', '8080'),
            ap.BaseProxy('http', '202.57.132.77', '4145')
        ]
        validator = ap.Validator()
        validator.run(proxy_list)
        for proxy in proxy_list:
            print(proxy.to_dict())


if __name__ == '__main__':
    unittest.main()
