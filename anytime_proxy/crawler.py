import logging
import aiohttp
import asyncio
import anytime_proxy as ap
import xml.etree.ElementTree as ElementTree
import re
from random import randrange


class BaseCrawler:
    """Fetches the list of proxies from external sources and parses 
       them into BaseProxy objects.
    
    Attributes:
        _url: The URL of the web page to be fetched.
        _forward_proxy: The proxy used to fetch the web page.
    """

    def __init__(self, url, forward_proxy):
        """Init BaseCrawler with _url attribute."""

        self._url = url
        self._forward_proxy = forward_proxy

    def run(self, callback):
        """Asynchronously runs the fetch tasks.
        
        Args:
            callback: The callback function after succeessfully parsing the proxy list.
        """

        asyncio.run(self.bulk_get_proxy(self._url, callback))

    async def bulk_get_proxy(self, url: set, callback, timeout=15):
        """Gathers the fetch tasks.
        
        Args:
            url: The list of urls to be tested.
            callback: The callback function after succeessfully parsing the proxy list.
            timeout: The timeout limit of the fetch task.
        """

        tasks = []
        for task_url_protocol in url:
            task_url = task_url_protocol[0]
            task_protocol = task_url_protocol[1]
            tasks.append(self.get_proxy(task_url, callback, default_protocol=task_protocol, timeout=timeout))
        await asyncio.gather(*tasks)

    async def get_proxy(self, url: str, callback, default_protocol=None, timeout=15):
        """Performs individual fetch task.
        
        Args:
            url: The list of urls to be tested.
            callback: The callback function after succeessfully parsing the proxy list.
            default_protocol: The default protocol of the proxy list.
            timeout: The timeout limit of the fetch task.
        """

        async with aiohttp.ClientSession() as session:
            try:
                for _ in range(3):
                    async with session.get(url, timeout=timeout, proxy=self._forward_proxy) as resp:
                        print(resp.status, url)
                        if resp.status == 200:
                            resp_text = await resp.text()
                            callback(await self.parse_response(resp_text, default_protocol))
                            break
                        else:
                            await asyncio.sleep(randrange(5))
                            continue
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
                raise exc
            except Exception as exc:
                logging.error(
                    "Non-aiohttp exception occured: {}".format(
                        getattr(exc, "__dict__", {})
                    )
                )
                raise exc

    async def parse_response(self, resp, default_protocol):
        """Parses response of the fetch task. To be implemented by each instance class.

        Args:
            resp: The response text of the fetch task.
            default_protocol: The default protocol of the proxy list.

        Returns:
            A list of BaseProxy objects.
        """

        return None


class HideMyName(BaseCrawler):
    def __init__(self, forward_proxy=None):
        super().__init__({("http://hidemy.name/en/proxy-list/", None)}, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = []
        current = ElementTree.fromstring(resp)
        elements = (
            ('body', None),
            ('div', 'wrap'),
            ('div', 'services_proxylist services'),
            ('div', 'inner'),
            ('div', 'table_block'),
            ('table', None),
            ('tbody', None)
        )
        anonymity_level = {
            "High": 2,
            "Average": 1,
            "Low": 1,
            "no": 0
        }

        for tag_name, class_name in elements:
            if class_name:
                for i in current.findall(tag_name):
                    if i.attrib['class'] == class_name:
                        current = i
            else:
                current = current.find(tag_name)

        for proxy in current.findall('tr'):
            host = proxy[0].text()
            port = proxy[1].text()
            geo_info = {
                "region_code": "",
                "region_name": proxy[2].find('div').findall('span')[0].text(),
                "city_name": proxy[2].find('div').findall('span')[1].text(),
            }
            _speed = proxy[3].find('div').find('p').text()
            protocol = proxy[4].text().lower()
            anonymity = anonymity_level.get(proxy[5].text(), 0)
            proxies.append(
                ap.BaseProxy.from_dict(
                    {
                        "geo_info": geo_info,
                        "protocol": protocol,
                        "host": host,
                        "port": port,
                        "anonymity": anonymity,
                        "relay": False,
                        "average_latency": 0.0,
                        "test_times": 0,
                        "validity": 100
                    }
                )
            )


class FreeProxyList(BaseCrawler):
    def __init__(self, forward_proxy=None):
        super().__init__({("http://free-proxy-list.net/", None)}, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = []


class SocksProxy(BaseCrawler):
    def __init__(self, forward_proxy=None):
        super().__init__({("http://www.socks-proxy.net/", None)}, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = []


class ProxyScrape(BaseCrawler):
    def __init__(self, forward_proxy=None):
        url = "http://api.proxyscrape.com/" \
              "?request=getproxies&proxytype={}&timeout=10000&country=all&ssl={}&anonymity=all"
        urls = {
            (url.format('http', 'no'), 'http'),
            (url.format('http', 'yes'), 'https'),
            (url.format('socks4', 'all'), 'socks4'),
            (url.format('socks5', 'all'), 'socks5'),
        }
        super().__init__(urls, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = []
        print(resp)


class IP3366(BaseCrawler):
    def __init__(self, forward_proxy=None):
        urls = set()
        for i in range(1, 5):
            urls.add(("http://www.ip3366.net/free/?stype=1&page={}".format(i), None))
        super().__init__(urls, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = re.findall(
            r"<tr>\s*<td>(.*?)</td>\s*<td>(\d*?)</td>\s*<td>.*?</td>\s*<td>(.*?)</td>",
            resp
        )
        return [(address, port, protocol.lower()) for address, port, protocol in proxies]


class KuaiDaiLi(BaseCrawler):
    def __init__(self, forward_proxy=None):
        urls = set()
        for i in range(1, 5):
            urls.add(("http://www.kuaidaili.com/free/inha/{}/".format(i), None))
        super().__init__(urls, forward_proxy)

    async def parse_response(self, resp, default_protocol):
        proxies = re.findall(
            r"<td data-title=\"IP\">(.+)</td>\s*<td data-title=\"PORT\">(\d+)</td>\s*<.*>\s*<td data-title=\"类型\">(.+)</td?",
            resp
        )
        return [(address, port, protocol.lower()) for address, port, protocol in proxies]
