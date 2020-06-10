class BaseProxy:
    """The template of a proxy.
    
    Attributes:
        _anonymity_level: The valid anonymity levels.
        _geo_info: The geolocation info of  the proxy.
        _valid_protocols: The valid protocols. (http, https, socks4, socks5)
        _protocol: The protocol of the proxy.
        _host: The hostname or IP address of the proxy.
        _port: The port of the proxy.
        _relay: Whether the proxy is a relay. 
                Without relay: Cilent-> Proxy -> Destination
                With relay: Cilent-> Proxy (Relay) -> Another Proxy -> Destination
        _anonymity: The anonymity level of the proxy.
        _validity: The validity of the proxy.
    """

    def __init__(self, protocol, host, port):
        """Inits BaseProxy with default attributes."""

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
        self._geo_info = {
            "region_code": "N/A",
            "region_name": "N/A",
            "state": "N/A",
            "city": "N/A",
            "postal": "N/A",
            "latitude": "N/A",
            "longitude": "N/A",
            "organization": "N/A",
            "asn": "N/A",
            "isp": "N/A",
            "asn_organization": "N/A",
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
        return "[{protocol}://{host}:{port} Region:{geo_code} Anonymity:{anonymity}]".format(
            protocol=self._protocol,
            host=self._host,
            port=self._port,
            geo_code=self._geo_info['region_code'],
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
            "anonymity": self._anonymity,
            "validity": self._validity
        }

    def to_list(self):
        return [
            self._protocol,
            self._host,
            self._port,
            self._anonymity,
            self._validity
        ]

    def to_proxy_string(self):
        return "{}://{}:{}".format(self._protocol, self._host, self._port)

    def to_request_proxy(self):
        return {
            'http': self.to_proxy_string(),
            'https': self.to_proxy_string()
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
    def anonymity(self):
        return self._anonymity

    @anonymity.setter
    def anonymity(self, level):
        if not level == 1 or level == 2:
            level = 0
        self._anonymity = level
