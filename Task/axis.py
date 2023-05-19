import time
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import datetime

datetime.datetime.utcnow()
datetime.datetime(2022, 6, 24, 9, 42, 26, 135766)
datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
import re
import requests as rq
from bs4 import BeautifulSoup
import gc



logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)
username = "kizy"
password = "dd5220-4902e5-ca7c78-712cbd-c377de"

PROXY_RACK_DNS = "usa.rotating.proxyrack.net:9000"
proxy = "http://cdfcd4e233464959ac5f1f8d45a9c05f:@proxy.crawlera.com:8011/"
timeout = 60
cat_timeout = 20

def handle_error(failure):
    pass




# Type 1 article

class AlittihadSpider(scrapy.Spider):
    name = "AlittihadSpider"
    allowed_domains = ["alittihad.ae"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.alittihad.ae/category/%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA']
    links=[]


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
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                data = response.css(".most-read-text,.innerdesc , .mb0")

                for link in data:
                    try:
                        if str(link.css("a").attrib["href"]) not in self.links:
                            if "http" in str(link.css("a").attrib["href"]):
                                self.links.append(str(link.css("a").attrib["href"]))
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": link.css("a").attrib["href"]
                                       }
                            else:
                                self.links.append(str(link.css("a").attrib["href"]))
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": "https://www.alittihad.ae" + link.css("a").attrib["href"]
                                       }

                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_article_links += 1


# Type 2 reg_article

class OxfordBusinessGroupSpider(scrapy.Spider):
    name = "OxfordBusinessGroupSpider"
    allowed_domains = ["oxfordbusinessgroup.com"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://oxfordbusinessgroup.com/search-results?sector=all&country=54046&keywords='
    ,'https://oxfordbusinessgroup.com/search-results?sector=52390&country=54052&keywords=',
    'https://oxfordbusinessgroup.com/search-results?sector=52392&country=54052&keywords=',
    'https://oxfordbusinessgroup.com/search-results?sector=52394&country=54057&keywords=']

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
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                data = response.css('.white')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": link.css("a").attrib["href"],
                                       }

                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": "https://oxfordbusinessgroup.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1

class SfSpider(scrapy.Spider):
    name = "SfdaCircularSpider"
    allowed_domains = ["sfda.gov.sa"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.sfda.gov.sa/ar/circulars?tags=All']
    links =[]

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
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                categories_links = []
                res = response.css('.download-doc-link')
                for r in res:
                    try:
                        if any(n in str(r.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if str(r.css("a").attrib["href"]) not in categories_links:
                                if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                                    categories_links.append(r.css("a").attrib["href"])
                                else:
                                    categories_links.append(
                                        "https://www.sfda.gov.sa" + r.css("a").attrib["href"]
                                    )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout,"base_url": response.url},
                            errback=handle_error,
                        )


                    except:
                        pass
        self.links.clear()

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                base_url = response.meta.get('base_url')
                data = response.css('.warning-item,.sing-date')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if link.css("a").attrib["href"] not in self.links:
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                    self.links.append( link.css("a").attrib["href"])
                                    yield {"clean_url": self.allowed_domains[0],
                                           "base_url": base_url,
                                           "link": link.css("a").attrib["href"],

                                           }
                                else:
                                    self.links.append(link.css("a").attrib["href"])
                                    yield {"clean_url": self.allowed_domains[0],
                                           "base_url": base_url,
                                           "link": "https://www.sfda.gov.sa" + link.css("a").attrib["href"],

                                           }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1



# Type 3 PDF spiders One Page

class TejarahSpider(scrapy.Spider):
    name = "TejarahSpider"
    allowed_domains = ["tejarah.gov.om"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://tejarah.gov.om/rules']


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
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                data = response.css('.explore-projects-content')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "title": link.css('.item.d-flex.align-items-center span::text').get().strip() if link.css('.item.d-flex.align-items-center span') else 'na',
                                       "excerpt": link.css('h3::text').get().strip() if link.css('h3') else 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"].replace('..','')
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "title": link.css('.item.d-flex.align-items-center span::text').get().strip() if link.css('.item.d-flex.align-items-center span') else 'na',
                                       "excerpt": link.css('h3::text').get().strip() if link.css('h3') else 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://tejarah.gov.om" + link.css("a").attrib["href"].replace('..','')
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1



# Type 4 PDF spider More Pages

class SfdaCircularSpider(scrapy.Spider):
    name = "SfdaCircularSpider"
    allowed_domains = ["sfda.gov.sa"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.sfda.gov.sa/en/circulars?tags=All','https://www.sfda.gov.sa/ar/circulars?tags=All']

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
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                categories_links = []
                res = response.css('.download-doc-link')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.sfda.gov.sa"
                                + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout,"base_url": response.url},
                            errback=handle_error,
                        )


                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                base_url = response.meta.get('base_url')
                data = response.css('.warning-item,.sing-date')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('.m-c-title::text').get().strip(),
                                       "excerpt": 'na',
                                       "published_date": response.css('.sing-date::text').get().strip() if response.css(
                                           '.sing-date::text').get().strip() else 'na',
                                       "pdf_url": link.css(".download-doc-link").attrib["href"],

                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('.m-c-title::text').get().strip(),
                                       "excerpt": 'na',
                                       "published_date": response.css('.sing-date::text').get().strip() if response.css(
                                           '.sing-date::text').get().strip() else 'na',
                                       "pdf_url": "https://www.sfda.gov.sa" + link.css(".download-doc-link").attrib[
                                           "href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1







process = CrawlerProcess(settings={
                "FEED_URI" : f"Newlink_1.json",
                "FEED_FORMAT" : "json",
                "USER_AGENT" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(AlittihadSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")