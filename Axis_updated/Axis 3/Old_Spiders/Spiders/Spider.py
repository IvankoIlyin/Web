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



class NcaPdfSpider(scrapy.Spider):
    name = "NcaPdfSpider"
    allowed_domains = ["nca.gov.sa"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://nca.gov.sa/en/legislation']

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                data = response.css(".Heading_teaser-title__Fcglm a")
                for r in data:
                    try:
                        categories_links.append("https://www.hrsd.gov.sa" + r.css('a').attrib['href'])
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
                data = response.css('.File_rowWrapper__yr8cl.col-lg-4.col-md-6.col-sm-12 a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": "na",
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css(".download-doc-link").attrib["href"],

                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": "na",
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "" + link.css(".download-doc-link").attrib["href"],

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

process.crawl(NcaPdfSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")