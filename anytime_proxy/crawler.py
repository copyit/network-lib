import aiohttp
import asyncio
import anytime_proxy as ap
import xml.etree.ElementTree as ElementTree


class BaseCrawler:
    def __init__(self, url):
        self._url = url

    def run(self, callback):
        asyncio.run(self.bulk_get_proxy(self._url, callback))

    async def bulk_get_proxy(self, urls: set, callback, timeout=15):
        tasks = []
        for task_url_protocol in urls:
            task_url = task_url_protocol[0]
            task_protocol = task_url_protocol[1]
            tasks.append(self.get_proxy(task_url, callback, default_protocol=task_protocol, timeout=timeout))
        await asyncio.gather(*tasks)

    async def get_proxy(self, url: str, callback, default_protocol=None, timeout=15):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as resp:
                resp = await resp.text()
                callback(await self.parse_response(resp, default_protocol))

    async def parse_response(self, resp, default_protocol):
        return None


class HideMyName(BaseCrawler):
    def __init__(self):
        super().__init__({("https://hidemy.name/en/proxy-list/", None)})

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
        def __init__(self):
            super().__init__({("https://free-proxy-list.net/", None)})

        async def parse_response(self, resp, default_protocol):
            proxies = []

    class SocksProxy(BaseCrawler):
        def __init__(self):
            super().__init__({("https://www.socks-proxy.net/", None)})

        async def parse_response(self, resp, default_protocol):
            proxies = []

    class ProxyScrape(BaseCrawler):
        def __init__(self):
            url = "https://api.proxyscrape.com/" \
                  "?request=getproxies&proxytype={}&timeout=10000&country=all&ssl={}&anonymity=all"
            urls = {
                (url.format('http', 'no'), 'http'),
                (url.format('http', 'yes'), 'https'),
                (url.format('socks4', 'all'), 'socks4'),
                (url.format('socks5', 'all'), 'socks5'),
            }
            super().__init__(urls)

        async def parse_response(self, resp, default_protocol):
            proxies = []
