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
        self._relay = False
        self._anonymity = 0
        self._test_times = 0
        self._average_latency = 0.0
        self._validity = 100

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "[{protocol}://{host}:{port}, Region:{geo_code}, Anonymity:{anonymity}]".format(
            protocol=self._protocol,
            host=self._host,
            port=self._port,
            geo_code=self._geo_info['code'],
            anonymity=self._anonymity_level[self._anonymity]
        )

    @classmethod
    def from_dict(cls, d):
        df = {'_' + k: v for k, v in d.items()}
        return cls(**df)

    def to_dict(self):
        return {
            "geo_info": self._geo_info,
            "protocol": self._protocol,
            "host": self._host,
            "port": self._port,
            "relay": self.relay,
            "anonymity": self.anonymity_level,
            "average_latency": self._average_latency,
            "test_times": self._test_times,
            "validity": self._validity
        }

    @property
    def host(self):
        return self._host

    @property
    def relay(self):
        return self._relay

    @relay.setter
    def relay(self, is_relay):
        if isinstance(is_relay, bool):
            self._relay = is_relay

    @property
    def anonymity_level(self):
        return self._anonymity_level

    @anonymity_level.setter
    def anonymity_level(self, level):
        if not level == 1 or level == 2:
            level = 0
        self._anonymity_level = level
