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

class solSpider(scrapy.Spider):
    name = "solSpider"
    allowed_domains = ["sol.no"]
    not_allowed_keyword = ["/www.dagbladet.no"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://sol.no/']
    links =[]

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"proxy": proxy, "download_timeout": timeout},
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
                res = response.css('.noLeftArrow a')
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
                                        "https:" + r.css("a").attrib["href"]
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
        time.sleep(3)
        if str(response.status) == "200":
            if response.css("body"):
                base_url = response.meta.get('base_url')
                data = response.css('.wl-tile a')
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
                                           "link": "https://www.trouw.nl" + link.css("a").attrib["href"],

                                           }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1



#head = {"USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
process = CrawlerProcess(settings={
                'FEED_URI': 'Newlink_1.json',
                'FEED_FORMAT': 'json',
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
            })

process.crawl(solSpider)

st = time.time()
process.start()
process.stop()
print(f"this is total time {time.time()-st}")
