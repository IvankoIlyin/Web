import time
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import datetime

datetime.datetime.utcnow()
datetime.datetime(2022, 6, 24, 9, 42, 26, 135766)
datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


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

class wionewsComSpider(scrapy.Spider):
    name = "wionewsComSpider"
    allowed_domains = ["wionews.com"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.wionews.com/business-economy','https://www.wionews.com/sports','https://www.wionews.com/science','https://www.wionews.com/entertainment','https://www.wionews.com/india-news','https://www.wionews.com/world']
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
                data = response.css("a.list-more")

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
                                       "link": "https://www.wionews.com" + link.css("a").attrib["href"]
                                       }

                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_article_links += 1

class iflscienceComSpider(scrapy.Spider):
    name = "iflscienceComSpider"
    allowed_domains = ["iflscience.com"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.iflscience.com/latest','https://www.iflscience.com/trending','https://www.iflscience.com/health-and-medicine','https://www.iflscience.com/space-and-physics','https://www.iflscience.com/technology']
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
                data = response.css(".card-content--body--title a")

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
                                       "link": "https://www.iflscience.com" + link.css("a").attrib["href"]
                                       }

                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_article_links += 1

class spaceComSpider(scrapy.Spider):
    name = "spaceComSpider"
    allowed_domains = ["space.com"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.space.com/news','https://www.space.com/search-for-life','https://www.space.com/tech-robots','https://www.space.com/entertainment']
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
                data = response.css("a.article-link")

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
                                       "link": "https://www.space.com" + link.css("a").attrib["href"]
                                       }

                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_article_links += 1

#head = {"USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
process = CrawlerProcess(settings={
                'FEED_URI': 'Newlink_1.json',
                'FEED_FORMAT': 'json',
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
            })

process.crawl(spaceComSpider)

st = time.time()
process.start()
process.stop()
print(f"this is total time {time.time()-st}")
