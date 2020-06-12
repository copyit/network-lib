import unittest
import network_lib


class TestIP(unittest.TestCase):
    def test_internal(self):
        internal_ip = network_lib.ip.get_internal()
        print('Internal IP Address:', internal_ip)
        self.assertTrue(isinstance(internal_ip, str))

    def test_external(self):
        external_ipv4 = network_lib.ip.get_external(protocol='v4')
        external_ipv6 = network_lib.ip.get_external(protocol='v6')
        print('External IPv4 Address:', external_ipv4)
        print('External IPv6 Address:', external_ipv6)


if __name__ == '__main__':
    unittest.main()
