import scrapy
import logging
import datetime
import requests as rq
import re
from bs4 import BeautifulSoup
import json
import tldextract
import gc
from constants import *


def handle_error(failure):
    pass

#1
class tiecSpider(scrapy.Spider):
    name = "tiecSpider"
    allowed_domains = ["tiec.gov.eg"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"dont_retry": True, "download_timeout": timeout},
                errback=handle_error,
            )
            yield res

    def start_requests_ip(self, arg):
        for i in self.start_urls:
            res_ip = scrapy.Request(
                i,
                meta={"change_proxies": True, "dont_retry": True, "download_timeout": timeout},
                callback=self.parse,
                dont_filter=True,
                errback=handle_error,
            )
            yield res_ip

        logging.info(
            {
                "proxy": "1",
                "clean_url": self.allowed_domains[0],
                "link": self.start_urls,
            }
        )

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.listingHeader a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": link.css("a").attrib["href"]
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": "https://tiec.gov.eg/English/MediaCenter/PressReleases" + str(
                                           link.css("a").attrib["href"])[2:],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1



class zatcaPdfSpider(scrapy.Spider):
    name = "zatcaPdfSpider"
    allowed_domains = ["zatca.gov.sa"]
    not_allowed_keyword = ["fatca-services-login"]
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"zyte_proxy": True, "dont_retry": True, "download_timeout": timeout},
                errback=handle_error,
            )
            yield res

    def start_requests_ip(self, arg):
        for i in self.start_urls:
            res_ip = scrapy.Request(
                i,
                meta={"change_proxies": True, "dont_retry": True, "download_timeout": timeout},
                callback=self.parse,
                dont_filter=True,
                errback=handle_error,
            )
            yield res_ip

            logging.info(
                {
                    "proxy": "1",
                    "clean_url": self.allowed_domains[0],
                    "link": i,
                }
            )

    def parse(self, response):

        if str(response.status) == "200":
            if response.css("body"):

                # Parse Zakat, Customs, and Tax Regulations
                regulations_links = []
                regulations_data = response.css("div.iconLinkTiles__items a")

                for link in regulations_data:
                    try:
                        if any(n in str(link.css('a').attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif link.css("a").attrib["href"] not in regulations_links:
                            regulations_links.append(response.urljoin(link.css("a").attrib["href"]))
                    except:
                        pass

                for link in regulations_links:
                    yield scrapy.Request(
                        link,
                        callback=self.parse_regulations,
                        dont_filter=True,
                        meta={"zyte_proxy": True,"dont_retry": True, "download_timeout": timeout, "origin_url": response.url},
                        errback=handle_error,
                    )

                # Parse Tax and Customs Agreements
                agreements_links = []
                agreements_data = response.css("div#agreementsData a")
                for link in agreements_data:
                    try:
                        if any(n in str(link.css('a').attrib["data-link"]) for n in self.not_allowed_keyword):
                            pass
                        elif link.css("a").attrib["data-link"] not in agreements_links:
                            agreements_links.append(response.urljoin(link.css("a").attrib["data-link"]))
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": response.meta['origin_url'] if 'origin_url' in response.meta else response.url,
                                   "title": str(link.css("a").attrib["data-title"]) if 'data-title' in link.css("a").attrib else 'na',
                                   "excerpt": 'na',
                                   "published_date": 'na',
                                   "pdf_url": response.urljoin(link.css("a").attrib["data-link"]),
                                   }
                    except:
                        pass

    def parse_regulations(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                service_links = []
                service_data = response.css("div.boxService")

                for link in service_data:
                    try:
                        if any(n in str(link.css('a').attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif link.css("a").attrib["href"] not in service_links:
                            service_links.append(response.urljoin(link.css("a").attrib["href"]))
                    except:
                        pass

                for link in service_links:
                    yield scrapy.Request(
                        link,
                        callback=self.parse_service,
                        dont_filter=True,
                        meta={"zyte_proxy": True,"dont_retry": True, "download_timeout": timeout, "origin_url": response.meta["origin_url"]},
                        errback=handle_error,
                    )

    def parse_service(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                try:
                    data = response.css("div.textSection__inner")
                    if len(data) > 0 and len(data.css('a')) > 0:
                        yield {"clean_url": self.allowed_domains[0],
                               "base_url": response.meta['origin_url'] if 'origin_url' in response.meta else response.url,
                               "title": str(data.css("h3::text").get()) if len(data.css("h3").get()) > 0 else 'na',
                               "excerpt": str(data.css('table.ms-rteTable-default td.ms-rteTable-default::text').get()) if (
                                       data.css('table.ms-rteTable-default td.ms-rteTable-default').get() and len(
                                   data.css('table.ms-rteTable-default td.ms-rteTable-default').get()) > 0) else 'na',
                               "published_date": 'na',
                               "pdf_url": response.urljoin(data.css('a').attrib['href']) if len(data.css('a')) > 0 else 'na',
                               }
                except:
                    pass