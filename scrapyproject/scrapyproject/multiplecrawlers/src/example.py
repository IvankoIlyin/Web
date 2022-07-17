import scrapy
from scrapy.crawler import CrawlerProcess
from config import *
import logging

logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

proxy = "http://{}:{}@{}".format(proxy_user,proxy_pass, proxy_ip)

def handle_error(failure):
    pass


class CbsNewsSpider(scrapy.Spider):
    name = "CbsNewsSpider"
    allowed_domains = ["cbsnews.com"]
    not_allowed_keyword = []
    start_urls = "https://www.cbsnews.com/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"dont_retry": True, "download_timeout": timeout},
            errback=handle_error,
        )
        yield res

    def start_requests_ip(self, arg):
        res_ip = scrapy.Request(
            self.start_urls,
            meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
            callback=self.parse,
            dont_filter=True,
            errback=handle_error,
        )
        logging.info(
            {
                "proxy": "1",
                "clean_url": self.allowed_domains[0],
                "link": self.start_urls,
            }
        )
        yield res_ip

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                categories_links = []
                res = response.css(".site-nav__item--news").css("ul.site-nav").css("li.site-nav__item").css("ul.site-nav__section").css("li")[:12]

                for r in res:
                    categories_links.append(
                        "https://www.cbsnews.com" + r.css("a").attrib["href"]
                    )

                for i in categories_links:
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )

                        self.start_urls = i

                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css("article.item")
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            yield {"link": link.css("a").attrib["href"]}

                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1


process = CrawlerProcess(settings={
                "FEED_URI": f"/Users/aakashsaini/Desktop/scraping code/scrapyproject/multiplecrawlers/src/Newlink_1.json",
                "FEED_FORMAT": "json",
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(CbsNewsSpider)
process.start()
