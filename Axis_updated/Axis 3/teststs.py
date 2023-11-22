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

proxy = "http://{}:{}@{}".format(proxy_user, proxy_pass, proxy_ip)


def handle_error(failure):
    pass


#1
class SicurezzanazionalePdfSpider(scrapy.Spider):
    name = "SicurezzanazionalePdfSpider"
    allowed_domains = ["sicurezzanazionale.gov.it"]
    not_allowed_keyword = []
    start_urls = ["https://www.sicurezzanazionale.gov.it/sisr.nsf/documentazione/normativa-di-riferimento.html"]
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
                res = response.css('.entry a')

                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.sicurezzanazionale.gov.it" + r.css("a").attrib["href"])
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
                data = response.css('.entry a')

                for link in data:

                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif ".pdf" in link.css("a").attrib["href"]:
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
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date":  'na',
                                       "pdf_url": "https://www.sicurezzanazionale.gov.it" + link.css("a").attrib["href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#2
class PoliticheagricolePdfSpider(scrapy.Spider):
    name = "PoliticheagricolePdfSpider"
    allowed_domains = ["politicheagricole.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/59",
                  "https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/10483",
                  "https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/6174",
                  "https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/12348",
                  "https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/89",
                  "https://www.politicheagricole.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/156"]


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
                res = response.css(".u-textClean")

                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.politicheagricole.it" + r.css("a").attrib["href"])
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
                data = response.css('.viewLink.viewLinkIMG')

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
                                       "published_date":  'na',
                                       "pdf_url": "https://www.sicurezzanazionale.gov.it" + link.css("a").attrib["href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#3
class AadePdfSpider(scrapy.Spider):
    name = "AadePdfSpider"
    allowed_domains = ["aade.gr"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.aade.gr/egkyklioi-kai-apofaseis"]
    all_urls = ["https://www.aade.gr/egkyklioi-kai-apofaseis?page=" + str(i) for i in range(1, 212)]
    start_urls += all_urls

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
                res = response.css('.field-content a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.aade.gr" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout,"base_url": response.url},
                            errback=handle_error,)

                    except:
                        pass

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                base_url = response.meta.get('base_url')
                data = response.css('a.pdf-file')

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
                                       "pdf_url": link.css("a").attrib["href"],}

                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.aade.gr" + link.css("a").attrib["href"], }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#4
class NormattivaPdfSpider(scrapy.Spider):
    name = "NormattivaPdfSpider"
    allowed_domains = ["normattiva.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://www.normattiva.it/ricerca/elencoPerData/anno/2023?tabID=0.8047822093619303&title=lbl.risultatoRicerca',
                  'https://www.normattiva.it/ricerca/elencoPerData/1?tabID=0.8047822093619303&title=Dettaglio&bloccoAggiornamentoBreadCrumb=true']

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
                res = response.css('p a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.normattiva.it" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                            errback=handle_error, )
                    except:
                        pass

    llinks = []
    def article_links(self, response, llinks =[]):
        if str(response.status) == "200":
            if response.css("body"):

                base_url = response.meta.get('base_url')
                data = response.css('.link_gazzetta a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.normattiva.it" + link.css("a").attrib["href"], }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#5
class Consob1PdfSpider(scrapy.Spider):
    name = "Consob1PdfSpider"
    allowed_domains = ["consob.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.consob.it/web/consob-and-its-activities/laws-and-regulations"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css("a.listLink")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                   "base_url": response.url if response.url else "na",
                                   "title": 'na',
                                   "excerpt": 'na',
                                   "published_date": 'na',
                                   "pdf_url": link.css("a").attrib["href"], }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                   "base_url": response.url if response.url else "na",
                                   "title": 'na',
                                   "excerpt": 'na',
                                   "published_date": 'na',
                                   "pdf_url":link.css("a").attrib["href"].replace("javascript:liferayLinkHook('", "https://www.consob.it/o/PubblicazioniPortlet/DownloadFile?filename=").replace("');", "") }
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#6
class Consob2PdfSpider(scrapy.Spider):
    name = "Consob2PdfSpider"
    allowed_domains = ["consob.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.consob.it/web/area-pubblica/determinazioni-dirigenziali"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css("li a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if ".pdf" in str(link.css("a").attrib["href"]):
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                    yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if  response.url else 'na',
                                       "title": link.css('a::text').get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                                else:
                                    yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if  response.url else 'na',
                                        "title": link.css('a::text').get(),
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://www.consob.it" + link.css("a").attrib["href"]}
                    except:
                        print("a")
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#7
class EneaPdfSpider(scrapy.Spider):
    name = "EneaPdfSpider"
    allowed_domains = ["enea.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.enea.it/it/enea/Riferimenti-normativi"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css("p a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "index" in str(link.css("a").attrib["href"]) or "component" in str(link.css("a").attrib["href"]):
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                    yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else 'na',
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                                else:
                                    yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else 'na',
                                        "title": link.css("a::text").get(),
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://www.enea.it" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#8
class MasePdfSpider(scrapy.Spider):
    name = "MasePdfSpider"
    allowed_domains = ["mase.gov.it"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.mase.gov.it/archivio-normative?title=&tid_1=All&tid_direzioni-normative=All&year%5Bvalue%5D%5Bdate%5D=&year_month%5Bvalue%5D%5Bdate%5D="]
    all_urls = ["https://www.mase.gov.it/archivio-normative?title=&tid_1=All&tid_direzioni-normative=All&year%5Bvalue%5D%5Bdate%5D=&year_month%5Bvalue%5D%5Bdate%5D=&page=" + str(i) for i in range(1, 19)]
    start_urls += all_urls
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
                res = response.css('.views-field.views-field-title a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.mase.gov.it" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                            errback=handle_error, )
                    except:
                        pass

    llinks = []
    def article_links(self, response, llinks =[]):
        if str(response.status) == "200":
            if response.css("body"):

                base_url = response.meta.get('base_url')
                data = response.css('.file a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "" + link.css("a").attrib["href"], }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#9
class MinistryofjusticePdfSpider(scrapy.Spider):
    name = "MinistryofjusticePdfSpider"
    allowed_domains = ["ministryofjustice.gr"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://ministryofjustice.gr/?page_id=3576"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css("li a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in  llinks and ".pdf" in str(link.css("a").attrib["href"]):
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url":response.url if response.url else 'na',
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else 'na',
                                        "title": 'na',
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://ministryofjustice.gr" + link.css("a").attrib["href"].replace("./wp-content","/wp-content")}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#10
class UokikPdfSpider(scrapy.Spider):
    name = "UokikPdfSpider"
    allowed_domains = ["uokik.gov.pl"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://uokik.gov.pl/wyjasnienia_i_wytyczne.php"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css(".file-list li a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in  llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else 'na',
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url":response.url if response.url else 'na' ,
                                        "title": link.css("a::text").get(),
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://uokik.gov.pl/" + link.css("a").attrib["href"].replace("./wp-content","/wp-content")}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#11
class BtePdfSpider(scrapy.Spider):
    name = "BtePdfSpider"
    allowed_domains = ["bte.gep.msess.gov.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["http://bte.gep.msess.gov.pt/"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css(".capa a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in  llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else "na",
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else "na",
                                        "title": 'na',
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "bte.gep.msess.gov.pt" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#12
class ParlamentoPdfSpider(scrapy.Spider):
    name = "ParlamentoPdfSpider"
    allowed_domains = ["parlamento.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.parlamento.pt/DAR/Paginas/DAR2Serie.aspx",
                  "https://www.parlamento.pt/DAR/Paginas/DAR1Serie.aspx"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []
                data = response.css("a.TextoRegular")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in  llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url":response.url if response.url else "na",
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else "na",
                                        "title": 'na',
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://www.parlamento.pt/" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#13
class AnacomPdfSpider(scrapy.Spider):
    name = "AnacomPdfSpider"
    allowed_domains = ["anacom.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.anacom.pt/render.jsp?categoryId=377595",
                  "https://www.anacom.pt/render.jsp?categoryId=1644",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=1",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=2",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=3",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=4",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=5",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=6",
                  "https://www.anacom.pt/render.jsp?categoryId=377595&tab=&year=2023&month=&pag=7"]

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
                res = response.css('h3 a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.anacom.pt" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:

                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                            errback=handle_error, )
                    except:
                        pass

    llinks = []
    def article_links(self, response, llinks =[]):
        if str(response.status) == "200":
            if response.css("body"):

                base_url = response.meta.get('base_url')
                data = response.css('.pdf a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.anacom.pt" + link.css("a").attrib["href"], }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#14
class Infarmed1PdfSpider(scrapy.Spider):
    name = "Infarmed1PdfSpider"
    allowed_domains = ["infarmed.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.infarmed.pt/web/infarmed/legislacao-farmaceutica-compilada"]

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
                res = response.css('p a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.infarmed.pt" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:

                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                            errback=handle_error, )
                    except:
                        pass

    llinks = []
    def article_links(self, response, llinks =[]):
        if str(response.status) == "200":
            if response.css("body"):

                base_url = response.meta.get('base_url')
                data = response.css('p a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif str(link.css("a").attrib["href"]) not in llinks and ".pdf" in str(link.css("a").attrib["href"]) :
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.infarmed.pt" + link.css("a").attrib["href"], }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#--
class Infarmed2PdfSpider(scrapy.Spider):
    name = "Infarmed2PdfSpider"
    allowed_domains = ["infarmed.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.infarmed.pt/web/infarmed/legislacao/legislacao-publicada"]

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
                llinks = []

                base_url = response.meta.get('base_url')
                data = response.css(".cell-button a")

                for link in data:
                    try:
                        if str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(
                                    link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https://www.infarmed.pt" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#15
class Bportugal1PdfSpider(scrapy.Spider):
    name = "Bportugal1PdfSpider"
    allowed_domains = ["bportugal.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.bportugal.pt/en/page/legislation-and-regulations-cards",
                  "https://www.bportugal.pt/en/page/legislation-and-regulations-cheques",
                  "https://www.bportugal.pt/en/page/legislation-and-regulations-prohibition-use-cheques",
                  "https://www.bportugal.pt/en/page/legislation-and-regulations-transfers"]

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
                res = response.css('p a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("" + r.css("a").attrib["href"])
                    except:
                        pass

                for i in set(categories_links):
                    try:

                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                            errback=handle_error, )
                    except:
                        pass

    llinks = []
    def article_links(self, response, llinks =[]):
        if str(response.status) == "200":
            if response.css("body"):

                base_url = response.meta.get('base_url')
                data = response.css(".filename-legislation-file a")
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css("span::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"],}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": base_url,
                                       "title": link.css("span::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": "https:" + link.css("a").attrib["href"], }
                    except:
                        pass

        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#16
class Bportugal2PdfSpider(scrapy.Spider):
    name = "Bportugal2PdfSpider"
    allowed_domains = ["bportugal.pt"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.bportugal.pt/en/page/legislation-and-regulations-direct-debits",
                  "https://www.bportugal.pt/en/page/legislation-and-regulations-psd2"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []


                data = response.css("p a")

                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else 'na',
                                       "title": link.css("strong::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else 'na',
                                        "title": link.css("strong::text").get(),
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#17
class Bportugal3PdfSpider(scrapy.Spider):
    name = "Bportugal3PdfSpider"
    allowed_domains = ["bportugal.pt"]
    not_allowed_keyword = ["/en/search/node/Prevention"]
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.bportugal.pt/en/page/legislation-and-rules?mlid=1149"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []
                data = response.css("#block-system-main a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else 'na',
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else 'na',
                                        "title": link.css("a::text").get(),
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#18
class Sn1PdfSpider(scrapy.Spider):
    name = "Sn1PdfSpider"
    allowed_domains = ["sn.pl"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Odpowiedzialnosci",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Kontroli",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Kontroli&Rok=2021",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Kontroli&Rok=2020",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Kontroli&Rok=2019",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2022",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2021",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2020",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2019",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2018",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2017",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2016",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2015",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2014",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2012",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Pracy&Rok=2013"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []
                data = response.css(".Label_body")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else 'na',
                                       "title": link.css("a::text").get(),
                                       "excerpt": 'na',
                                       "published_date": link.css(".Date::text").get(),
                                       "pdf_url": link.css("a").attrib["href"].replace("/sprawy/http://", "http://")}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else 'na',
                                        "title": link.css("a::text").get(),
                                        "excerpt": 'na',
                                        "published_date": link.css(".Date::text").get(),
                                        "pdf_url": "https://www.sn.pl" + link.css("a").attrib["href"].replace("/sprawy/http://", "http://")}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#19
class Sn2ArticleSpider(scrapy.Spider):
    name = "Sn2ArticleSpider"
    allowed_domains = ["sn.pl"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Karna",
                  "https://www.sn.pl/orzecznictwo/SitePages/Najnowsze_orzeczeniaIOZ.aspx?Izba=Cywilna"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []

                data = response.css(".Items")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else "na",
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date": link.css(".Date::text").get(),
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url":response.url if response.url else "na",
                                        "title": 'na',
                                        "excerpt": 'na',
                                        "published_date": link.css(".Date::text").get(),
                                        "pdf_url": "https://www.sn.pl" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#20
class MindigitalPdfSpider(scrapy.Spider):
    name = "MindigitalPdfSpider"
    allowed_domains = ["mindigital.gr"]
    not_allowed_keyword = []
    start_urls = ["https://mindigital.gr/archives/539#"]
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

                data = response.css("#recent-posts-2 a")
                data += response.css(".wp-block-file a:nth-child(1)")
                for r in data:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append("https://www.politicheagricole.it" + r.css("a").attrib["href"])
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
                data = response.css('.wp-block-file a')

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
                                       "published_date":  'na',
                                       "pdf_url": "https://www.sicurezzanazionale.gov.it" + link.css("a").attrib["href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#21
class Uokik1PdfSpider(scrapy.Spider):
    name = "Uokik1PdfSpider"
    allowed_domains = ["isap.sejm.gov.pl"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://uokik.gov.pl/ochrona_konsumentow_.php",
                  "https://uokik.gov.pl/ochrona_konkurencji_.php"]

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
                res = response.css('.file-list a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(""+ r.css("a").attrib["href"])
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
                data = response.css('.icon-after.doc-link')
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
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date":  'na',
                                       "pdf_url": "https://isap.sejm.gov.pl" + link.css("a").attrib["href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#22
class Uokik2PdfSpider(scrapy.Spider):
    name = "Uokik2PdfSpider"
    allowed_domains = ["isap.sejm.gov.pl"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://uokik.gov.pl/znak_ce_.php",
                  "https://uokik.gov.pl/ogolne_bezpieczenstwo_produktow_.php",
                  "https://uokik.gov.pl/jakosc_paliw_.php"]

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
                res = response.css('#text a')
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(""+ r.css("a").attrib["href"])
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
                data = response.css('.icon-after.doc-link')
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
                                       "title": 'na',
                                       "excerpt": 'na',
                                       "published_date":  'na',
                                       "pdf_url": "https://isap.sejm.gov.pl" + link.css("a").attrib["href"],

                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#23
class YpergasiasPdfSpider(scrapy.Spider):
    name = "YpergasiasPdfSpider"
    allowed_domains = ["ypergasias.gov.gr"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ["https://ypergasias.gov.gr/ergasiakes-scheseis/ygeia-kai-asfaleia-stin-ergasia/nomothesia-gia-tin-yae/"]

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
                meta={"proxy": proxy,"dont_retry": True, "download_timeout": timeout},
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
                llinks = []
                data = response.css(".elementor-widget-theme-post-content a")
                for link in data:
                    try:
                        if  str(link.css("a").attrib["href"]) not in llinks:
                            llinks.append(str(link.css("a").attrib["href"]))
                            if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url if response.url else "na",
                                       "title": link.css("a::text").get() if link.css("a::text").get() else 'na',
                                       "excerpt": 'na',
                                       "published_date": 'na',
                                       "pdf_url": link.css("a").attrib["href"]}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": response.url if response.url else "na",
                                        "title": link.css("a::text").get() if link.css("a::text").get() else 'na',
                                        "excerpt": 'na',
                                        "published_date": 'na',
                                        "pdf_url": "https://ypergasias.gov.gr" + link.css("a").attrib["href"]}
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1
#24
class YpergasiasArticleSpider(scrapy.Spider):
    name = "YpergasiasArticleSpider"
    allowed_domains = ["ypergasias.gov.gr"]
    not_allowed_keyword = []
    start_urls = ["https://ypergasias.gov.gr/ergasiakes-scheseis/atomikes-ergasiakes-sxeseis/kanonismoi-ergasias-prosopikou/"]
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
                llinks = []
                data = response.css("#recent-posts-4 a")
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        elif link.css("a").attrib["href"] not in llinks:
                            llinks.append(link.css("a").attrib["href"])
                            if "http" in str(link.css("a").attrib["href"]):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": link.css("a").attrib["href"],
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": "https://ypergasias.gov.gr" + link.css("a").attrib["href"],
                                       }
                    except:
                        pass

        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1

process = CrawlerProcess(settings={
                "FEED_URI": f"Newlink_0.json",
                "FEED_FORMAT": "json",
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })
process.crawl(SicurezzanazionalePdfSpider)
process.start()