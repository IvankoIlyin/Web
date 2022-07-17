# Example number 1
# Website with categories
# class TreasuryAndRiskSpider(scrapy.Spider):
#     name = "TreasuryAndRiskSpider"
#     allowed_domains = ["treasuryandrisk.com"]
#     start_urls = "https://www.treasuryandrisk.com/"
#     check_ip_category = 0
#     check_ip_article_links = 0
#
#     def start_requests(self):
#         res = scrapy.Request(
#             self.start_urls,
#             callback=self.parse,
#             dont_filter=True,
#             meta={"dont_retry": True, "download_timeout": timeout},
#             errback=handle_error,
#         )
#         yield res
#
#     def start_requests_ip(self, arg):
#         res_ip = scrapy.Request(
#             self.start_urls,
#             meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
#             callback=self.parse,
#             dont_filter=True,
#             errback=handle_error,
#         )
#         logging.info(
#             {
#                 "proxy": "1",
#                 "clean_url": self.allowed_domains[0],
#                 "link": self.start_urls,
#             }
#         )
#         yield res_ip
#
#     def parse(self, response):
#         if str(response.status) == "200":
#             if response.css("body"):
#                 categories_links = []
#                 topic_links = response.css("#topics a")
#                 for link in topic_links:
#                     categories_links.append(
#                         "https://www.treasuryandrisk.com" + link.attrib["href"]
#                     )
#
#                 for i in categories_links:
#                     try:
#                         yield scrapy.Request(
#                             i,
#                             callback=self.article_links,
#                             meta={"dont_retry": True, "download_timeout": cat_timeout},
#                             errback=handle_error,
#                         )
#                         self.start_urls = i
#                     except:
#                         pass
#         else:
#             while self.check_ip_category < 2:
#                 yield response.follow(self.start_urls, callback=self.start_requests_ip)
#                 self.check_ip_category += 1
#
#     def article_links(self, response):
#         if str(response.status) == "200":
#             if response.css("body"):
#                 result = response.css(".cr2 .brief")
#                 for r in result:
#                     try:
#                         print ({
#                             "link": "https://www.treasuryandrisk.com/"
#                             + r.css("a")[1].attrib["href"],
#                         })
#                     except:
#                         pass
#         else:
#             while self.check_ip_article_links < 2:
#                 self.start_urls = response.url
#                 yield response.follow(self.start_urls, callback=self.start_requests_ip)
#                 self.check_ip_article_links += 1
class BostonSpider(scrapy.Spider):
    name = "BostonSpider"
    allowed_domains = ["boston.com"]
    start_urls = "https://www.boston.com/"
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
                res = response.css("#panel-primary-nav a")
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.boston.com"
                                + r.css("a").attrib["href"]
                            )

                    except:
                        pass

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
                data = response.css(
                    ".m-article-list-feature__headline , .m-numbered-post-list__title , .a-article__title")
                for link in data:
                    try:
                        if "https" in str(link.css("a").attrib["href"]):
                            yield {"link": link.css("a").attrib["href"]}
                        else:
                            yield {
                                "link": "https://www.boston.com"
                                        + link.css("a").attrib["href"]
                            }
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css(
                    '.m-numbered-post-list__title , .m-article-list-feature__headline , .m-article-list__link')
                for link in data:
                    try:
                        if "https" in str(link.css("a").attrib["href"]):
                            yield {"link": link.css("a").attrib["href"]}
                        else:
                            yield {
                                "link": "https://www.boston.com"
                                        + link.css("a").attrib["href"]
                            }

                    except:
                        pass
        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1


# Example number 2
# Website with pages without categories
class ConsultancyUKSpider(scrapy.Spider):
    name = "ConsultancyUKSpider"
    allowed_domains = ["consultancy.uk"]
    start_urls = "https://www.consultancy.uk/news/"
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
                result = response.css(".index1")
                for r in result:
                    try:
                        yield {
                            "link": "https://www.consultancy.uk"
                            + r.css("a").attrib["href"]
                        }
                    except:
                        pass
                for i in range(2, 14):
                    next_page = f"https://www.consultancy.uk/news/page/{str(i)}"
                    self.start_urls = next_page
                    try:
                        yield scrapy.Request(
                            next_page,
                            callback=self.parse,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )
                    except:
                        pass

        else:
            while self.check_ip_article_links < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1


# Example number 3
# Website with categories and subcategories
class ChicagoTribuneSpider(scrapy.Spider):
    name = "ChicagoTribuneSpider"
    allowed_domains = ["chicagotribune.com"]
    start_urls = "https://www.chicagotribune.com/"
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
                res = response.css("li.link-list")
                for r in res:
                    categories_links.append(
                        "https://www.chicagotribune.com" + r.css("a").attrib["href"]
                    )

                for i in categories_links:
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.sub_category,
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

    def sub_category(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                sub_category = []
                sub_res = response.css("#trending-topics-wrapper .tag-solid")
                for s in sub_res:
                    sub_category.append(
                        "https://www.chicagotribune.com" + s.css("a").attrib["href"]
                    )
                for i in sub_category:
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
                data = response.css(".no-u")
                for link in data:
                    try:
                        yield {
                            "link": "https://www.chicagotribune.com/"
                            + link.css("a::attr(href)").get()
                        }
                    except:
                        pass
        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1