import aiohttp
import asyncio
import anytime_proxy as ap
import logger



class Validator:
    # 
    def __init__(self, proxy_list):
        test_urls = {
            'https://httpbin.org/get?show_env'
        }
        asyncio.run(
            self.test_bulk(
                proxy_list, 
                test_urls
            )
        )

    async def test_bulk(self, proxy_list: list, test_urls: set) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for proxy in proxy_list:
                for url in test_urls:
                    tasks.append(
                        self.fetch_html(proxy, url)
                    )
            await asyncio.gather(*tasks)

    async def fetch_html(self, proxy: ap.BaseProxy, url: str, session: aiohttp.ClientSession) -> None:
        found = set()
        try:
            async with session.get('http://httpbin.org/get', proxy=proxy, params=params) as resp:
                logger.info("Got response [%s] for URL: %s", resp.status, url)
                resp.raise_for_status()
                resp_json = await resp.json()
        except (
            aiohttp.ClientError,
            aiohttp.ClientConnectorError,
            aiohttp.http_exceptions.HttpProcessingError,
            TimeoutError, 
            AttributeError
        ) as exc:
            logger.error(
                "aiohttp exception for {} [{}]: {}".format(
                    url,
                    getattr(exc, "status", None),
                    getattr(exc, "message", None)
                ),
            )
        except Exception as e:
            logger.exception(
                "Non-aiohttp exception occured:  {}".format(
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
            logger.info("Vaild Proxy: {}".format(proxy))
        finally:
            await session.close()
