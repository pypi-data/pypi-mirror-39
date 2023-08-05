#!/usr/bin/python
"""Extracting Data from Zillow, and storing into a csv file to be graphed.
"""
import os
import re as regex
from bs4 import BeautifulSoup
import requests
import unicodecsv as csv
from crawler import WebCrawler

__author__ = "Disaiah Bennett"
__version__ = 1.0

def main():
    """Extracting housing information from zillow by utilizing the web-crawler.
    """
    url = "https://www.zillow.com/homes/for_sale/" # THE URL
    head = "https://www.zillow.com/" # THE HEAD OF THE URL
    tail = "_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy"

    zipcode = "27909" # ZIP CODES
    total = 0 # NUMBER OF URL
    page_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    crawler = WebCrawler()
    csv_file = csv.writer(open("zillow_homes_%s.csv" % zipcode, "wb"))

    with requests.Session() as session:
        for i, _ in enumerate(page_num):
            crawler.url = "%s%s/%d_p/%s" % (url, zipcode, page_num[i],tail)

            print crawler.url

            crawler.page = session.get(crawler.get_url(), headers=crawler.get_header())
            soup = BeautifulSoup(crawler.get_data(), 'html.parser')

            prop_links = soup.findAll('a', {"class": "zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"})
            crawler.links = [link.get('href') for _, link in enumerate(prop_links)]

            print "Zip Code: %s\n" % zipcode, \
            "----------------------------------------------------------------------------------"
            for i, link in enumerate(crawler.get_links()):
                crawler.sub_url = "%s%s" % (head, link)

                if crawler.sub_url:
                    total += 1
                    print "%d %s" % (total, crawler.sub_url)

                crawler.page = session.get(crawler.sub_url, headers=crawler.get_header())
                soup = BeautifulSoup(crawler.get_data(), 'html.parser')

                house_years = regex.findall(r'<div class="fact-value">Built in (.*?)<', str(soup))
                house_address = soup.findAll('div', {"class": "zsg-h1 hdp-home-header-st-addr"})
                house_address = soup.findAll('div', {"class": "zsg-h1 hdp-home-header-st-addr"})
                house_cost = soup.findAll('div', {"class": "price"})
                house_size = soup.findAll('h3', {"class": "edit-facts-light"})

                for _, address in enumerate(house_address):
                    if address:
                        print address.text
                        crawler.address(address.text)
                        break

                for _, year in enumerate(house_years):
                    if year:
                        print year
                        crawler.year(int(year))
                        break

                for _, cost in enumerate(house_cost):
                    if cost:
                        print cost.text.replace("and up", "").replace("from", "")
                        crawler.price(float(cost.text.replace("and up", "").replace("from", "").replace("$", "").replace(",", "").replace("From:", "")))
                        break

                for _, size in enumerate(house_size):
                    if size:
                        if "baths" in size.text:
                            try:
                                print size.text.replace("--", "N/A").split("baths")[1]
                                crawler.size(size.text.replace("--", "0").replace("sqft", "").replace(",", "").split("baths")[1])
                            except IndexError:
                                pass

                        elif "bath" in size.text:
                            try:
                                print size.text.replace("--", "N/A").split("bath")[1]
                                crawler.size(size.text.replace("--", "0").replace("sqft", "").replace(",", "").split("bath")[1])
                            except IndexError:
                                pass
                        else:
                            print size.text
                            crawler.size(size.text)
                print "\n"
                if house_address and house_cost and house_size and house_years:
                    try:
                        crawler.prop_size[i] = crawler.prop_size[i].replace("sqft", "").replace("acres", "").replace("--", "").replace(",", "")
                        csv_file.writerow([crawler.prop_address[i], crawler.prop_year[i], float(crawler.prop_size[i]), crawler.prop_price[i]])
                    except IndexError:
                        pass
                elif house_address and house_cost and house_size:
                    try:
                        crawler.prop_size[i] = crawler.prop_size[i].replace("sqft", "").replace("acres", "").replace("--", "0").replace(",", "")
                        csv_file.writerow([crawler.prop_address[i], "N/A", float(crawler.prop_size[i]), crawler.prop_price[i]])
                    except IndexError:
                        pass
                elif house_address and house_size and house_years:
                    try:
                        crawler.prop_size[i] = crawler.prop_size[i].replace("sqft", "").replace("acres", "").replace("--", "0").replace(",", "")
                        csv_file.writerow([crawler.prop_address[i], crawler.prop_year[i], float(crawler.prop_size[i]), 0.0])
                    except IndexError:
                        pass

            crawler.data_clear()

#        os.system(". move_csv.sh")
        os.system("python analyze.py")

if __name__ == "__main__":
    main()
