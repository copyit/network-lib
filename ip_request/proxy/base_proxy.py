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
            "socks4",
            "socks5"
        }

        self._protocol = protocol
        self._host = host
        self._port = port
        self._relay = False
        self._anonymity = 0
        self._validity = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "[{protocol}://{host}:{port}]".format(
            protocol=self._protocol,
            host=self._host,
            port=self._port,
            anonymity=self._anonymity_level[self._anonymity]
        )

    @classmethod
    def from_dict(cls, d):
        df = {'_' + k: v for k, v in d.items()}
        return cls(**df)

    @classmethod
    def from_string(cls, proxy_string):
        proxy_string = proxy_string.split(':')
        return cls(**proxy_string)

    def to_dict(self):
        return {
            "protocol": self._protocol,
            "host": self._host,
            "port": self._port,
            "relay": self._relay,
            "anonymity": self._anonymity,
            "validity": self._validity
        }

    def to_string(self):
        return "{}://{}:{}".format(self._protocol, self._host, self._port)

    def to_requests(self):
        return {
            'http': self.to_string(),
            'https': self.to_string()
        }

    def get_anonymity(self, raw=False):
        if raw:
            return self._anonymity
        else:
            return self._anonymity_level[self._anonymity]

    def test(self, url='http://httpbin.org/get'):
        pass
