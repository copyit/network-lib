import anytime_proxy as ap
import logging
import json
import requests
import concurrent.futures


class Validator:
    """Checks whether a proxy is valid and its anonymity level.

    There are three levels of anoymity:
        Transparent:    Forward detailed information about you including your IP address 
                        to the target server you are connecting to.

        Anonymous:      Does not reveal your IP address to a server, however the server 
                        will know that the connection was made through a proxy because 
                        of the additional information that is sent with each request.

        High Anonymous: The server you are connecting to has no idea that the connection 
                        was made through a proxy nor does it know your real IP address.

    Attributes:
        real_ip: The real IPv4 address of the device.
    """

    def __init__(self):
        """Inits Validator with default test_urls and real_ip attributes."""

        self.test_url = 'http://httpbin.org/get?show_env'
        self.real_ip = "127.0.0.1"

    def run(self, proxy_list, callback):
        """Asynchronously obtains the real IPv4 address and validates the proxies.

        Args:
            proxy_list: A list of proxies (instances of anytime_proxy.BaseProxy) 
                        to be validated.
        """
        try:
            self.real_ip = self.get_real_ip()
            return self.test_bulk(proxy_list, self.test_url, callback)

        except Exception as exc:
            logging.error(
                "Exception occurred: {}".format(
                    repr(exc)
                ),
            )

    @staticmethod
    def get_real_ip():
        """Fetches the webpage ('https://httpbin.org/get') to find the real IP address."""

        resp = requests.get('http://httpbin.org/get', timeout=5)
        resp_json = resp.json()
        return resp_json.get("origin", '127.0.0.1')

    def test_bulk(self, proxy_list, test_url, callback):
        """Gathers the fetch tasks and asynchronously runs them.
        
        This method creates fetch tasks for different URLs for each proxy to
        determine whether both the proxy could be connected and the proxy is
        not banned by specific websites based on user's preferences.

        Args:
            proxy_list: A list of proxies (instances of anytime_proxy.BaseProxy) 
                        to be validated.
            test_url: The URL to be tested.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        # future_list = {executor.submit(self.fetch_html, proxy, test_url, callback) for proxy in proxy_list}
        # result_list = concurrent.futures.wait(future_list, timeout=10, return_when=concurrent.futures.ALL_COMPLETED)
        # return [future.result() for future in result_list[0]]
        for proxy in proxy_list:
            executor.submit(self.fetch_html, proxy, test_url, callback)

    @staticmethod
    def get_geo_info(ip_address: str) -> dict:
        try:
            url = 'https://api.ip.sb/geoip/{}'
            resp = requests.get(url.format(ip_address), timeout=5)
            logging.info("Got response [%s] for URL: %s", resp.status_code, url)
            resp_json = json.loads(resp.text)
            return {
                "region_code": resp_json.get("country_code"),
                "region_name": resp_json.get("country"),
                "state": resp_json.get("region_code"),
                "city": resp_json.get("city"),
                "postal": resp_json.get("postal"),
                "latitude": resp_json.get("latitude"),
                "longitude": resp_json.get("longitude"),
                "organization": resp_json.get("organization"),
                "asn": resp_json.get("asn"),
                "isp": resp_json.get("isp"),
                "asn_organization": resp_json.get("asn_organization")
            }
        except Exception:
            raise

    def fetch_html(self, proxy: ap.BaseProxy, url: str, callback):
        """Fetches the text of webpage with the proxy and check its anonymity level.

        Args:
            proxy: An instance of anytime_proxy.BaseProxy.
            url: The URL of the webpage to be fetched.
        """
        try:
            resp = requests.get(url, proxies=proxy.to_request_proxy(), timeout=5)
            logging.info("Got response [%s] for URL: %s", resp.status_code, url)
            resp_json = resp.json()
            x_forwarded_for = resp_json.get("headers", dict()).get("X-Forwarded-For", None)
            origin = resp_json.get("origin")
            if proxy.host in origin:
                proxy.relay = False
            else:
                proxy.relay = True

            if self.real_ip in x_forwarded_for:
                proxy.anonymity = 0
            elif not x_forwarded_for:
                proxy.anonymity = 2
            else:
                proxy.anonymity = 1
            logging.info("Valid Proxy: {}".format(proxy))
            proxy._validity = True
            proxy._geo_info = self.get_geo_info(origin)
        except Exception:
            raise

        finally:
            callback(proxy)
