import unittest
import network_lib


class TestPing(unittest.TestCase):
    def test_ping_tcp(self):
        ping_result = network_lib.ping.tcp('www.cloudflare.com', 443, count=5)
        print(ping_result)
        self.assertTrue(ping_result)

    def test_ping_scan(self):
        scan_result = network_lib.ping.scan('github.com', (80, 443))
        print(scan_result)
        self.assertTrue(scan_result)

    def test_speed_test(self):
        speed_test_result = network_lib.ping.speed_test('https://github.com/', method='GET')
        print(speed_test_result)
        self.assertTrue(speed_test_result)


if __name__ == '__main__':
    unittest.main()
