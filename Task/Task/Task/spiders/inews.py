import tldextract
import time
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import datetime

datetime.datetime.utcnow()
datetime.datetime(2022, 6, 24, 9, 42, 26, 135766)
datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
import urllib.parse
import re
import requests as rq
from bs4 import BeautifulSoup

logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)
username = "kizy"
password = "dd5220-4902e5-ca7c78-712cbd-c377de"
PROXY_RACK_DNS = "usa.rotating.proxyrack.net:9000"
proxy = "https://{}:{}@{}".format(username, password, PROXY_RACK_DNS)
timeout = 60
cat_timeout = 20
def handle_error(failure):
    pass

class statesmanSpider(scrapy.Spider):
    name = "statesmanSpider"
    allowed_domains = ["statesman.com"]
    not_allowed_keyword = []
    start_urls = "https://www.statesman.com/news/"
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
                res = response.css('.gnt_sn_a_w, .gnt_sn_dd_a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.statesman.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('.gnt_m_flm_a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.statesman.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.gnt_m_flm_a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.statesman.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class foolSpider(scrapy.Spider):
    name = "foolSpider"
    allowed_domains = ["fool.com"]
    not_allowed_keyword = []
    start_urls = "https://www.fool.com/investing-news/"
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
                data = response.css('.py-12px.text-gray-1100')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"]
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.fool.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class thedailymealSpider(scrapy.Spider):
    name = "thedailymealSpider"
    allowed_domains = ["thedailymeal.com"]
    not_allowed_keyword = []
    start_urls = "https://www.thedailymeal.com/category/news/"
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
                res = response.css('.subcategories li+ li a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.thedailymeal.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('.article-description')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.thedailymeal.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.article-description')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.thedailymeal.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class thatgrapejuiceSpider(scrapy.Spider):
    name = "thatgrapejuiceSpider"
    allowed_domains = ["thatgrapejuice.net"]
    not_allowed_keyword = []
    start_urls = "https://thatgrapejuice.net/category/feature-article/"
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
                data = response.css('.title a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"]
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://thatgrapejuice.net" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class nypostSpider(scrapy.Spider):
    name = "nypostSpider"
    allowed_domains = ["nypost.com"]
    not_allowed_keyword = []
    start_urls = "https://nypost.com/news/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                data = response.css('.headline a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"]
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://nypost.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class aarpSpider(scrapy.Spider):
    name = "aarpSpider"
    allowed_domains = ["aarp.org"]
    not_allowed_keyword = []
    start_urls = "https://www.aarp.org/"
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
                res = response.css('.aarpe-accordion~ li a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.aarp.org" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('.topic-heading a , .link')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {None}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.aarp.org" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.topic-heading a , .link')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {None}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.aarp.org" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class southernlivingSpider(scrapy.Spider):
    name = "southernlivingSpider"
    allowed_domains = ["southernliving.com"]
    not_allowed_keyword = []
    start_urls = "https://www.southernliving.com/news"
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
                res = response.css('.header-nav__list-item:nth-child(8) .header-nav__sublist-item:nth-child(2) a , .header-nav__list-item:nth-child(8) .header-nav__sublist-item:nth-child(1) a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.southernliving.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('.card--no-image')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.southernliving.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.card--no-image')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.southernliving.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class expaSpider(scrapy.Spider):
    name = "expaSpider"
    allowed_domains = ["expa.com"]
    not_allowed_keyword = []
    start_urls = "https://www.expa.com/news"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                data = response.css('a.title')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {None
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.expa.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class cbsnewsSpider(scrapy.Spider):
    name = "cbsnewsSpider"
    allowed_domains = ["cbsnews.com"]
    not_allowed_keyword = []
    start_urls = "https://www.cbsnews.com/cbslocal/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                data = response.css('a.item__anchor')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"]
                                       }


                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.cbsnews.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class moreSpider(scrapy.Spider):
    name = "moreSpider"
    allowed_domains = ["more.com"]
    not_allowed_keyword = []
    start_urls = "https://www.more.com/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                res = response.css('#primary-menu a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.more.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('.block')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.more.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.block')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.more.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class designmilkSpider(scrapy.Spider):
    name = "designmilkSpider"
    allowed_domains = ["design-milk.com"]
    not_allowed_keyword = []
    start_urls = "https://design-milk.com/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                res = response.css('.column-topics a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://design-milk.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('a.post-title')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://design-milk.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('a.post-title')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://design-milk.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

class onepmSpider(scrapy.Spider):
    name = "onepmSpider"
    allowed_domains = ["one37pm.com"]
    not_allowed_keyword = []
    start_urls = "https://www.one37pm.com/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"proxy": proxy, "download_timeout": timeout},
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
                res = response.css('.popular-culture , .music , .style , .sports , .gaming , .nft')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.one37pm.com" + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

                data = response.css('a.article-card')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.one37pm.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('a.article-card')

                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": link.css("a").attrib["href"],
                                       "type": 'article'}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "link": "https://www.one37pm.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1


#head = {"USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
process = CrawlerProcess(settings={
                'FEED_URI': f'Newlink_1.json',
                'FEED_FORMAT': 'json',
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
            })

process.crawl(foolSpider)
process.start()
