import aiohttp
import asyncio
import anytime_proxy as ap
import logging


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
        """Inits Validator with default real_ip attribute."""

        test_urls = {
            'https://httpbin.org/get?show_env'
        }
        self.real_ip = "127.0.0.1"


    def run(proxy_list: list) -> None:
        """Asynchronously obtains the real IPv4 address and validates the proxies.

        Args:
            proxy_list: A list of proxies (instances of anytime_proxy.BaseProxy) 
                        to be validated.
        """

        asyncio.run(
            self.get_real_ip()
        )
        asyncio.run(
            self.test_bulk(
                proxy_list,
                test_urls
            )
        )

    async def get_real_ip(self) -> None:
        """Fetches the webpage ('https://httpbin.org/get') to find the real IP address."""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://httpbin.org/get', timeout=15) as resp:
                    resp_json = await resp.json()
        except (
                aiohttp.ClientError,
                aiohttp.ClientConnectorError,
                TimeoutError,
                AttributeError
        ) as exc:
            logging.error(
                "aiohttp exception for {} [{}]: {}".format(
                    'https://httpbin.org/get',
                    getattr(exc, "status", None),
                    getattr(exc, "message", None)
                ),
            )
        else:
            self.real_ip = resp_json.get("origin", self.real_ip)

    async def test_bulk(self, proxy_list: list, test_urls: set) -> None:
        """Gathers the fetch tasks and asynchronously runs them.
        
        This method creates fetch tasks for different URLs for each proxy to
        determine whether both the proxy could be connected and the proxy is
        not banned by specific websites based on user's preferences.

        Args:
            proxy_list: A list of proxies (instances of anytime_proxy.BaseProxy) 
                        to be validated.
            test_urls: A set of URLs to be tested.
        """

        async with aiohttp.ClientSession() as session:
            tasks = []
            for proxy in proxy_list:
                for url in test_urls:
                    tasks.append(
                        self.fetch_html(proxy, url, session)
                    )
            await asyncio.gather(*tasks)

    async def fetch_html(self, proxy: ap.BaseProxy, url: str, session: aiohttp.ClientSession) -> None:
        """Fetches the text of webpage with the proxy and check its anonymity level.

        Args:
            proxy: An instance of anytime_proxy.BaseProxy.
            url: The URL of the webpage to be fetched.
            session: An instance of aiohttp.ClientSession created by self.test_bulk().
        """
        try:
            async with session.get(url, proxy=proxy.to_proxy_string(), timeout=15) as resp:
                logging.info("Got response [%s] for URL: %s", resp.status, url)
                resp.raise_for_status()
                resp_json = await resp.json()
        except (
                aiohttp.ClientError,
                aiohttp.ClientConnectorError,
                TimeoutError,
                AttributeError
        ) as exc:
            logging.error(
                "aiohttp exception for {} [{}]: {}".format(
                    url,
                    getattr(exc, "status", None),
                    getattr(exc, "message", None)
                ),
            )
        except Exception as e:
            logging.error(
                "Non-aiohttp exception occured: {}".format(
                    getattr(e, "__dict__", {})
                )
            )
        else:
            x_forwarded_for = resp_json.get("headers", dict()).get("X-Forwarded-For", None)
            origin = resp_json.get("origin")

            if origin != proxy.host:
                proxy.relay = True
            else:
                proxy.relay = False

            if self.real_ip in x_forwarded_for:
                proxy.anonymity_level = 0
            elif not x_forwarded_for:
                proxy.anonymity_level = 2
            else:
                proxy.anonymity_level = 1
            logging.info("Valid Proxy: {}".format(proxy))
        finally:
            await session.close()
