class BaseProxy:
    def __init__(self, protocol, host, port):
        self._anonymity_level = {
            0: "Transparent",
            1: "Anonymous",
            2: "High Anonymous"
        }
        self._valid_protocols = {
            "http", 
            "https", 
            "socks5", 
            "socks4"
        }
        self._geo_info = {
            "code": "",
            "name": "",
            "region_code": "",
            "region_name": "",
            "city_name": ""
        }
        self._protocol = protocol
        self._host = host
        self._port = port
        self._anonymity = 0
        self._test_times = 0
        self._average_latency = 0.0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "[{protocol}://{host}:{port}, Region:{geo_code}, Anonymity:{anonymity}]".format(
            protocol=self._protocol,
            host=self._host,
            port=self._port,
            geo_code=self._geo_code
            anonymty=self._anonymity_level[self._anonymity]
        )
    