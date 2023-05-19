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


# Case 1 : Article links from the start_urls no need to find any category link just grab the links of the article

class TamimiJudgmentsSpider(scrapy.Spider):
    name = "TamimiJudgmentsSpider"
    allowed_domains = ["tamimi.com"]
    not_allowed_keyword = []
    start_urls = "https://www.tamimi.com/judgments/"
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
                data = response.css('.h-thumb-content')
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
                                       "link": "https://www.tamimi.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1


# Case 2 : Pdf links from the start_urls no need to find any category link just grab the links of the pdf
class SfdaRegulationSpider(scrapy.Spider):
    name = "SfdaRegulationSpider"
    allowed_domains = ["sfda.gov.sa"]
    not_allowed_keyword = []
    start_urls = "https://www.sfda.gov.sa/en/regulations?keys=&regulation_type=All&date%5Bmin%5D=&date%5Bmax%5D=&tags=All"
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
                data = response.css('.warning-item')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "title": link.css('.m-c-title::text').get().strip(),
                                       "excerpt": 'na',
                                       "published_date": link.css('.news-date::text').get().strip() if link.css(
                                           '.news-date::text').get().strip() else 'na',
                                       "pdf_url": link.css(".download-doc-link").attrib["href"],
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "title": link.css('.m-c-title::text').get().strip(),
                                       "excerpt": 'na',
                                       "published_date": link.css('.news-date::text').get().strip() if link.css(
                                           '.news-date::text').get().strip() else 'na',
                                       "pdf_url": "https://www.sfda.gov.sa" + link.css(".download-doc-link").attrib[
                                           "href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

# Case 3 : When are two links for the pdf use this structure to grab the links of the pdf_url_eng and pdf_url_original
class TobaccoControllawsUaeSpider(scrapy.Spider):
    name = "TobaccoControllawsUaeSpider"
    allowed_domains = ["tobaccocontrollaws.org"]
    not_allowed_keyword = []
    start_urls = "https://www.tobaccocontrollaws.org/legislation/country/united-arab-emirates/laws"
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
                try:
                    data = response.css('.law-row')
                except:
                    data = []
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "title": link.css('h3::text').get().strip(),
                                       "excerpt": link.css('.comment.pull-left').css('p::text').get().strip(),
                                       "published_date": link.css(
                                           '.col-4.col-md-3.pt-1.px-1.law_date.text-left::text').get() if link.css(
                                           '.col-4.col-md-3.pt-1.px-1.law_date.text-left::text').get() else 'na',
                                       "pdf_url_eng": link.css('.btn.btn-sm.btn-success').attrib['href'] if link.css('.btn.btn-sm.btn-success').attrib['href']
                                       else 'na',
                                       "pdf_url_original": link.css('.btn.btn-sm.btn-primary').attrib['href'] if
                                       link.css('.btn.btn-sm.btn-primary').attrib['href'] else 'na',
                                       
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "title": link.css('h3::text').get().strip(),
                                       "excerpt": link.css('.comment.pull-left').css('p::text').get().strip(),
                                       "published_date": link.css(
                                           '.col-4.col-md-3.pt-1.px-1.law_date.text-left::text').get() if link.css(
                                           '.col-4.col-md-3.pt-1.px-1.law_date.text-left::text').get() else 'na',
                                      "pdf_url_eng": link.css('.btn.btn-sm.btn-success').attrib['href'] if link.css('.btn.btn-sm.btn-success').attrib['href']
                                       else 'na',
                                       "pdf_url_original": "https://www.tobaccocontrollaws.org" +
                                                           link.css('.btn.btn-sm.btn-primary').attrib['href'] if
                                       link.css('.btn.btn-sm.btn-primary').attrib['href'] else 'na',
                                       }
                    except:
                        pass
        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1




# Case 4 : Pdf links are not in the start_urls so have to use this structre to first find category_link and then grab the links of the pdf

class SfdaCircularSpider(scrapy.Spider):
    name = "SfdaCircularSpider"
    allowed_domains = ["sfda.gov.sa"]
    not_allowed_keyword = []
    start_urls = "https://www.sfda.gov.sa/en/circulars?tags=All"
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
                res = response.css('.download-doc-link')
                for r in res:
                    try:
                        if "http" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
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
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )


                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.warning-item,.sing-date')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
                                       "title": link.css('.m-c-title::text').get().strip(),
                                       "excerpt": 'na',
                                       "published_date": response.css('.sing-date::text').get().strip() if response.css(
                                           '.sing-date::text').get().strip() else 'na',
                                       "pdf_url": link.css(".download-doc-link").attrib["href"],
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls,
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
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1



class TamimiLawSpider(scrapy.Spider):
    name = "TamimiLawSpider"
    allowed_domains = ["tamimi.com"]
    not_allowed_keyword = []
    start_urls = "https://www.tamimi.com/our-knowledge/law-update/"
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
                res = response.css('.lawyer-thumb-img')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.tamimi.com" + r.css("a").attrib["href"]
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
                
                data = response.css('.sec-btn')
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
                                       "link": "https://www.tamimi.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass


    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.h-thumb-img-wrap')
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
                                       "link": "https://www.tamimi.com" + link.css("a").attrib["href"],
                                       "type": 'article'}
                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1



process = CrawlerProcess(settings={
                "FEED_URI": f"Newlink_1.json",
                "FEED_FORMAT": "json",
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(TamimiLawSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")