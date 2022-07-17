import scrapy
from config import *
import logging

logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

proxy = "https://{}:{}@{}".format(proxy_user, proxy_password, proxy_base_url)

def handle_error(failure):
    pass


# When You have a website with topics and categories links
# Example 1

class ChooseAName(scrapy.Spider):
    name = "" # Put unique name for a class
    allowed_domains = [""] # put allowed domains like cbsnews.com
    start_urls = "" # put start url
    check_ip_category = 0 # Use this when doing proxies
    check_ip_article_links = 0 # Use this when doing proxies

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
        if str(response.status) == "200": # If  not 200 meaning you need to use Proxies
            if response.css("body"): # Find Categorical Links
                categories_links = [] # Fill them in
                """
                scraping job
                """
                # Now you go on each link and look for article URLS
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

    def article_links(self, response): # To find Article links for a ccategorical link
        if str(response.status) == "200":

            article_links = []
            """
            scraping magic
            """
            for i in article_links:
                print(i)
        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1


# When you do not have a categoties and you need to extract article urls from the main website
class ChooseAUniqueName(scrapy.Spider):
    name = ""
    allowed_domains = [""]
    start_urls = ""
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
            article_links = []
            """
            scraping magic
            """
            for i in article_links:
                print(article_links)
        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1