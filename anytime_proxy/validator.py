import aiohttp
import asyncio
import anytime_proxy as ap
import logging


class Validator:
    def __init__(self, proxy_list):
        test_urls = {
            'https://httpbin.org/get?show_env'
        }
        self.real_ip = "127.0.0.1"
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
        async with aiohttp.ClientSession() as session:
            tasks = []
            for proxy in proxy_list:
                for url in test_urls:
                    tasks.append(
                        self.fetch_html(proxy, url, session)
                    )
            await asyncio.gather(*tasks)

    async def fetch_html(self, proxy: ap.BaseProxy, url: str, session: aiohttp.ClientSession) -> None:
        try:
            async with session.get(url, proxy=proxy, timeout=15) as resp:
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
