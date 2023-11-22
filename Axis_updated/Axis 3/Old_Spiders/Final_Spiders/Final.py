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
#1
class Nbb1PdfSpider(scrapy.Spider):
    name = "Nbb1PdfSpider"
    allowed_domains = ["nbb.be"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-20','https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-21','https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-22','https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/nbb-prudential-supervision-publications','https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/other-publications-national-bank-belgium','https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette/othe-0']
    for i in range(1,5): start_urls.append("https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-20?page=0%2C0%2C"+str(i))
    start_urls.append("https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-21?page=0%2C0%2C1")
    for i in range(1,16): start_urls.append("https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/publications-belgian-official-gazette-22?page=0%2C0%2C"+str(i))
    start_urls.append("https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/nbb-prudential-supervision-publications?page=0%2C0%2C1")
    start_urls.append("https://www.nbb.be/en/financial-oversight/prudential-supervision/publications/nbb-prudential-supervision-publications?page=0%2C0%2C2")
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

    def parse(self, response, **kwargs):
        if str(response.status) == "200":
            if response.css("body"):
                categories_links = []
                res = response.css('.list-unstyled a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.nbb.be"+ r.css("a").attrib["href"])

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
                data = response.css('.content a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],

                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('a::text').get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.nbb.be" + link.css("a").attrib["href"],}

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#2
class EnvironnementWalloniePdfSpider(scrapy.Spider):
    name = "EnvironnementWalloniePdfSpider"
    allowed_domains = ["environnement.wallonie.be"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['http://environnement.wallonie.be/cgi/dgrne/aerw/pe/droitinfo/li_difiche.idc']

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
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
                res = response.css('.lienbleu')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("http://environnement.wallonie.be/cgi/dgrne/aerw/pe/droitinfo/"+ r.css("a").attrib["href"])

                    except:
                        pass

                for i in set(categories_links):
                    try:
                        print(i)
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
                data = response.css('tr td p a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],

                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('a::text').get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "http://environnement.wallonie.be/cgi/dgrne/aerw/pe/droitinfo/" + link.css("a").attrib["href"],}

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#3
class HealthBelgiumPdfSpider(scrapy.Spider):
    name = "HealthBelgiumPdfSpider"
    allowed_domains = ["health.belgium.be"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.health.belgium.be/fr/vers-un-cadre-legal-pour-la-qualite-de-lair-interieur']

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
                res = response.css('p:nth-child(1) a')

                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.health.belgium.be" + r.css("a").attrib["href"])

                    except:
                        pass
                for i in set(categories_links):
                    try:
                        print(i)
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
                data = response.css('.file a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('a::text').get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],

                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css('a::text').get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "" + link.css("a").attrib["href"],}

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

process.crawl(EnvironnementWalloniePdfSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")