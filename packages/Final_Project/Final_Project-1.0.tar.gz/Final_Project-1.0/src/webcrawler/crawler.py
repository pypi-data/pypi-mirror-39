#!/usr/bin/python
"""
Python script to download the house information of Elizabeth City from Zillow and save it to
a csv file. Each record should contain address, year, size, price.
The csv file should contain at least 100 records.
"""
__author__ = "Disaiah Bennett"
__version__ = 1.0

class WebCrawler:
    """Web Crawler
    """
    def __init__(self, url=None, header=None, data=None, page=None):
        """Web Crawler
            url: string - the url.
            header: dict - the header
            data: object - the page data.
            page: object - the url page.
            links: list - the property home link.
            prop_address: list - the property address.
            prop_price: list - the property price.
            prop_year: list - the property year built.
            prop_size: list - the property size.
            clean: bool - places csv in the correct directory.
        """
        self.url = url
        self.req_headers = header

        self.data = data
        self.page = page

        self.links = None

        self.prop_address = []
        self.prop_price = []
        self.prop_year = []
        self.prop_size = []

    def get_header(self):
        """Return the header
            Returns:
                req_headers: dict - the header.
            Example:
                >>> req_headers = crawler.get_header()
        """
        self.req_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        return self.req_headers

    def get_url(self):
        """Return the url
            Returns:
                url: string - the url.
            Example:
                url = crawler.get_url()
        """
        return self.url

    def get_data(self):
        """Return the the url page data.
            Returns:
                data: object - the data of the current url page that is being read.
            Example:
                >>> data = crawler.get_data()
        """
        self.data = self.page.content
        return self.data

    def data_clear(self):
        """Clear the data stored in the web crawler
            Example:
                >>> crawler.data_clear()
        """
        if self.prop_address:
            try:
                del self.prop_address[:]
            except IndexError:
                pass

        if self.prop_price:
            try:
                del self.prop_price[:]
            except IndexError:
                pass

        if self.prop_year:
            try:
                del self.prop_address[:]
            except IndexError:
                pass

        if self.prop_size:
            try:
                del self.prop_size[:]
            except IndexError:
                pass

    def get_page(self):
        """
            Returns:
                page: object - the current page being read from the selected url.
            Example:
                >>> page = crawler.get_page()
        """
        return self.page

    def get_links(self):
        """
            Returns:
                links: list - current list of the properties links.
            Example:
                >>> links = crawler.get_links()
        """
        return self.links

    def address(self, address):
        """
            Returns:
                prop_address: list - updated list of the properties address.
            Example:
                >>> prop_address = crawler.address(address)
        """
        self.prop_address.append(address)
        return self.prop_address

    def get_addresses(self):
        """
            Returns:
                address: list - current list of the properties addresses.
            Example:
                >>> address = crawler.get_addresses()
        """
        return self.prop_address

    def year(self, year):
        """
            Returns:
                prop_year: list - updated list of the properties years.
            Example:
                >>> prop_year = crawler.year(year)
        """
        self.prop_year.append(year)
        return self.prop_year

    def get_years(self):
        """
            Returns:
                year: list - current list of the properties years.
            Example:
                >>> year = crawler.get_years()
        """
        return self.prop_year

    def size(self, size):
        """
            Returns:
                prop_size: list - updated list of the properties sizes.
            Example:
                >>> prop_size = crawler.size(size)
        """
        self.prop_size.append(size)
        return self.prop_size

    def get_sizes(self):
        """
            Returns:
                size: list - current list of the properties sizes.
            Example:
                >>> size = crawler.get_sizes()
        """
        return self.prop_size

    def price(self, price):
        """
            Returns:
                prop_price: list - updated list of the properties prices.
            Example:
                >>> prop_price = crawler.price(price)
        """
        self.prop_price.append(price)
        return self.prop_price

    def get_prices(self):
        """
            Returns:
                price: list - current list of properties prices.
            Example:
                >>> price = crawler.get_prices()
        """
        return self.prop_price
