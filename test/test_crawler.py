import unittest
import anytime_proxy as ap


class TestCrawler(unittest.TestCase):
    def test_hide_my_name(self):
        hide_my_name_crawler = ap.crawler.HideMyName()
        hide_my_name_crawler.run(print)

    def test_proxy_scrape(self):
        proxy_scrape_crawler = ap.crawler.ProxyScrape()
        proxy_scrape_crawler.run(print)

    def test_ip_3366(self):
        ip_3366_crawler = ap.crawler.IP3366()
        ip_3366_crawler.run(print)

    def test_kuai_dai_li(self):
        kuai_dai_li_crawler = ap.crawler.KuaiDaiLi()
        kuai_dai_li_crawler.run(print)


if __name__ == '__main__':
    unittest.main()
