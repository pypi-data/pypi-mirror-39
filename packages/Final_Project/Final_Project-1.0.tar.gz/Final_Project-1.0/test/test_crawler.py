#!usr/bin/python
"""Unittest for Web Crawler.
"""
import unittest
import requests
from webcrawler.crawler import WebCrawler

__author__ = "Disaiah Bennett"
__version__ = "0.1"

CRAWLER = WebCrawler()
CRAWLER.url = "https://www.zillow.com/homes/for_sale/"

class TestFileConverts(unittest.TestCase):
    """WebCrawler Unittest
    """
    #    def __init__(self, url=None, data=None, addr=None, size=None, year=None, pric=None):
    #    self.url = url
    #    self.data = data
    #    self.addresses = addr
    #    self.sizes = size
    #    self.years = year
    #    self.prices = pric

    def test_get_header_001(self):
        """get_header unittest
        """
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.assertEqual(header, CRAWLER.get_header())
            #            return True
        #else:
        #    return False

    def test_get_url_002(self):
        """get_url unittest
        """
        url = CRAWLER.url
        self.assertEqual(url, CRAWLER.get_url())
            #    return True
        #else:
        #    return False

    def test_get_data_003(self):
        """get_data unittest
        """
        with requests.Session() as session:
            CRAWLER.page = session.get(CRAWLER.get_url(), headers=CRAWLER.get_header())
            _ = CRAWLER.get_data()
#            if data:
#                return True
#            else:
#                return False

    def test_data_clear_004(self):
        """data_clear unittest
        """
        with requests.Session() as session:
            CRAWLER.page = session.get(CRAWLER.get_url(), headers=CRAWLER.get_header())
            _ = CRAWLER.get_data()
            try:
                CRAWLER.data_clear()
#                return True
            except OSError:
                pass

    def test_get_page_005(self):
        """get_page unittest
        """
        with requests.session() as session:
            CRAWLER.page = session.get(CRAWLER.get_url(), headers=CRAWLER.get_header())
            CRAWLER.get_page()
                #    return True
           # else:
           #     return False

    def test_get_links_006(self):
        """get_links unittest
        """
        try:
            CRAWLER.get_links()
        except OSError:
            pass

    def test_address_007(self):
        """address unittest
        """
        try:
            addresses = ["Sample.st", "Sample2.st"]
            CRAWLER.address(addresses)
        except OSError:
            pass

    def test_get_addresses_008(self):
        """get_addresses unittest
        """
        try:
            addresses = ["Sample.st", "Sample2.st"]
            CRAWLER.address(addresses)
            CRAWLER.get_addresses()
                #    return True
           # else:
           #     return False
        except OSError:
            pass

    def test_year_009(self):
        """year unittest
        """
        try:
            years = [i for i in range(2000, 2011)]
            CRAWLER.year(years)
        except OSError:
            pass

    def test_get_years_010(self):
        """get_years unittest
        """
        try:
            years = [i for i in range(2000, 2011)]
            CRAWLER.year(years)
            CRAWLER.get_years()
                #     return True
           # else:
                #   return False
        except OSError:
            pass

    def test_size_011(self):
        """size unittest
        """
        try:
            sizes = [i for i in range(1000, 2000)]
            CRAWLER.size(sizes)
        except OSError:
            pass

    def test_get_sizes_012(self):
        """get_sizes unittest
        """
        try:
            sizes = [i for i in range(1000, 2000)]
            CRAWLER.size(sizes)
            CRAWLER.get_sizes()
            #    return True
            #else:
                #    return False
        except OSError:
            pass

    def test_price_013(self):
        """price unittest
        """
        try:
            prices = [i for i in range(200000, 201100)]
            CRAWLER.price(prices)
        except OSError:
            pass

    def test_get_prices_014(self):
        """get_prices unittest
        """
        try:
            prices = [i for i in range(200000, 201100)]
            CRAWLER.price(prices)
            CRAWLER.get_prices()
#                return True
           # else:
                #    return False
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
