import logging
import datetime
import requests as rq
import re
import json
import gc

import scrapy
import tldextract


from constants import *



class GenericSpider(scrapy.Spider):
    allowed_domains = []

    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    check_ip_category_limit = 2
    check_ip_article_links_limit = 2

    dont_retry = True
    dont_filter = True

    scope_selector = None
    extractors = {}
    categories_links = None
    process_items_in_category_page = False

    pagination = None
    categories_pagination = None

    initial_proxy = False
    initial_meta = None
    headers = {}

    def handle_error(self, failure):
        pass

    def handle_retry(self, response, is_article=False):
        if is_article:
            while self.check_ip_article_links < self.check_ip_article_links_limit:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_article_links += 1
        else:
            while self.check_ip_category < self.check_ip_category_limit:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1

    def start_requests(self):
        self.initial_meta = {}
        if self.zyte_proxy:
            self.initial_meta['zyte_proxy'] = True
        callback_function = self.parse
        if self.categories_links:
            callback_function = self.parse_categories
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=callback_function,
                dont_filter=self.dont_filter,
                meta={**self.initial_meta, **{"dont_retry": self.dont_retry, "download_timeout": timeout}},
                headers=self.headers,
                errback=self.handle_error,
            )
            logging.info({"initial_meta":self.initial_meta})
            if self.process_items_in_category_page:
                category_page_item_scope = self.scope_selector
                if self.process_items_in_category_page != True:
                    category_page_item_scope = self.process_items_in_category_page

                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    meta={**self.initial_meta, **{"dont_retry": self.dont_retry, "download_timeout": cat_timeout,
                                                  "base_url": self.start_urls[0],
                                                  "scope_selector": category_page_item_scope}},
                    headers=self.headers,
                    errback=self.handle_error,
                )

    def start_requests_ip(self, arg):
        for url in self.start_urls:
            res_ip = scrapy.Request(
                url,
                meta={"proxy": zyte_proxy, "dont_retry": self.dont_retry, "download_timeout": timeout},
                headers=self.headers,
                callback=self.parse,
                dont_filter=self.dont_filter,
                errback=self.handle_error,
            )
            yield res_ip
            logging.info({"proxy": "1", "clean_url": self.allowed_domains[0], "link": url})

    def parse(self, response, **kwargs):
        base_url = response.meta.get('base_url') if response.meta.get('base_url') else response.url
        scope_selector = response.meta.get('scope_selector') if response.meta.get(
            'scope_selector') else self.scope_selector
        if str(response.status) == "200":
            if response.css("body"):
                scopes = self.process_scope_extractor(scope_selector, response)
                for scope in scopes:
                    try:
                        item = {
                            "clean_url": self.allowed_domains[0],
                            "base_url": base_url
                        }
                        for field in self.extractors:
                            extractor = self.extractors[field]
                            extractor_value = self.process_extractor(field, extractor, scope, item)
                            extractor_value = self.post_process_extractor(field, extractor_value, item, response)
                            item[field] = extractor_value
                        item = self.handle_edge_cases(item)
                        if self.is_not_allowed_keyword_present(item):
                            continue
                        if not self.is_valid_item(item):
                            continue
                        yield item
                    except Exception as e:
                        pass
            if self.pagination:
                next_pages = self.process_pagination_extractor(self.pagination, response)
                if next_pages:
                    for next_page in next_pages:
                        full_link_next_page = self.process_link(next_page, {}, response)
                        if not full_link_next_page:
                            continue
                        yield scrapy.Request(
                            full_link_next_page,
                            callback=self.parse,
                            meta={**self.initial_meta,
                                  **{"dont_retry": self.dont_retry, "download_timeout": cat_timeout, "base_url": base_url}},
                            headers=self.headers,
                            errback=self.handle_error)

        else:
            self.handle_retry(response)

    def parse_categories(self, response, **kwargs):
        base_url = response.meta.get('base_url') if response.meta.get('base_url') else response.url
        if str(response.status) == "200":
            if response.css("body"):
                category_links = self.process_categories_link_extractor(self.categories_links, response)
                for category_link in category_links:
                    full_link = self.process_link(category_link, {}, response)
                    if not full_link:
                        continue
                    try:
                        yield scrapy.Request(full_link, callback=self.parse,
                                             meta={**self.initial_meta,
                                                   **{"dont_retry": self.dont_retry, "download_timeout": cat_timeout,
                                                      "base_url": base_url}},
                                             headers=self.headers,
                                             errback=self.handle_error,
                                             )
                    except Exception as e:
                        logging.error(e)

                if self.categories_pagination:
                    next_pages = self.process_pagination_extractor(self.categories_pagination)
                    if next_pages:
                        for next_page in next_pages:
                            full_link_next_page = self.process_link(next_page, {}, response)
                            yield scrapy.Request(
                                full_link_next_page,
                                callback=self.parse_categories,
                                meta={**self.initial_meta,
                                      **{"dont_retry": self.dont_retry, "download_timeout": cat_timeout,
                                         "base_url": base_url}},
                                headers=self.headers,
                                errback=self.handle_error)
        else:
            self.handle_retry(response, is_article=True)

    def process_extractor(self, field, extractor, scope, item):
        extracted_value = None
        if isinstance(extractor, str):
            extractor_method = "css"
            extractor_selector = extractor
        else:
            extractor_method = extractor.get("method", "css")
            extractor_selector = extractor.get("selector")

        if extractor_method == "css":
            extracted_value = scope.css(extractor_selector).get()
        elif extractor_method == "xpath":
            extracted_value = scope.xpath(extractor_selector).get()
        elif extractor_method == "set_value":
            extracted_value = extractor_selector
        elif extractor_method == "script":
            try:
                exec(extractor_selector)
                extracted_value = item.get(field)
            except Exception as e:
                logging.error("error while executing script")
                logging.error(e)
        else:
            raise NotImplementedError(extractor_method)
        return extracted_value

    def process_scope_extractor(self, extractor, response):
        extracted_value = []
        if isinstance(extractor, str):
            extractor_method = "css"
            extractor_selector = extractor
        else:
            extractor_method = extractor.get("method", "css")
            extractor_selector = extractor.get("selector")

        if extractor_method == "css":
            extracted_value = response.css(extractor_selector)
        elif extractor_method == "xpath":
            extracted_value = response.xpath(extractor_selector)
        elif extractor_method == "script":
            try:
                exec(extractor_selector)
                if 'scopes' in locals():
                    extracted_value = locals()['scopes']
                else:
                    extracted_value = []
            except Exception as e:
                logging.error("error while executing script")
                logging.error(e)
        else:
            raise NotImplementedError(extractor_method)
        return extracted_value

    def process_pagination_extractor(self, extractor, response):
        extracted_value = []
        if isinstance(extractor, str):
            extractor_method = "css"
            extractor_selector = extractor
        else:
            extractor_method = extractor.get("method", "css")
            extractor_selector = extractor.get("selector")

        if extractor_method == "css":
            extracted_value = response.css(extractor_selector).extract()
        elif extractor_method == "xpath":
            extracted_value = response.xpath(extractor_selector).extract()
        elif extractor_method == "script":
            try:
                exec(extractor_selector)
                if 'next_pages' in locals():
                    extracted_value = locals()['next_pages']
                else:
                    extracted_value = []
            except Exception as e:
                logging.error("error while executing script")
                logging.error(e)
        else:
            raise NotImplementedError(extractor_method)
        return extracted_value

    def process_categories_link_extractor(self, extractor, response):
        return self.process_pagination_extractor(extractor, response)

    def post_process_extractor(self, field, value, item, response):
        if field in ["link", "pdf_url"]:
            value = self.process_link(value, item, response)
        if field in ["title", "published_date", "excerpt"]:
            value = value.strip() if value else None
        return value

    def process_link(self, value, item, response):
        if not value:
            return value
        value = value.strip()
        value = response.urljoin(value)
        return value

    def is_not_allowed_keyword_present(self, item):
        link = ''
        if 'link' in item and item['link']:
            link = item['link']
        if 'pdf_url' in item and item['pdf_url']:
            link = item['pdf_url']
        if any(n in str(link) for n in self.not_allowed_keyword):
            return True
        return False

    def is_valid_item(self, item):
        if not any([item.get(mandatory_field) for mandatory_field in ["link", "pdf_url"]]):
            return False
        return True

    def handle_edge_cases(self, item):
        if item['base_url'].endswith('/'):
            item['base_url'] = item['base_url'][:-1]
        return item


def create_spider_class(spider_name, config, message):
    if "allowed_domains" not in config:
        start_urls = message["base_url"].split(",")
        temp_allowed_domains = ['.'.join([i for i in list(tldextract.extract(i)) if i]) for i in start_urls]
        replace_top_sub_domains = {'www.', 'www2.'}
        allowed_domains = []
        for allowed_domain in temp_allowed_domains:
            for replace_top_sub_domain in replace_top_sub_domains:
                if allowed_domain.startswith(replace_top_sub_domain):
                    allowed_domain = allowed_domain[len(replace_top_sub_domain):]
            allowed_domains.append(allowed_domain)
        allowed_domains = list(set(allowed_domains))
    else:
        allowed_domains = config["allowed_domains"]

    class_dict = {
        "name": spider_name,
        "allowed_domains": allowed_domains,
        "not_allowed_keyword": config.get("not_allowed_keyword", []),

        "scope_selector": config["scope_selector"],
        "extractors": config["extractors"],

        "categories_links": config.get("categories_links", None),
        "process_items_in_category_page": config.get("process_items_in_category_page", False),

        "categories_pagination": config.get("categories_pagination", None),
        "pagination": config.get("pagination", None),

        "check_ip_category_limit": config.get("check_ip_category_limit", 2),
        "check_ip_article_links_limit": config.get("check_ip_article_links_limit", 2),
        "dont_retry": config.get("dont_retry", True),
        "dont_filter": config.get("dont_filter", True),

        "initial_proxy": config.get("initial_proxy", False),
        "zyte_proxy": config.get("zyte_proxy", False),
        "headers": config.get("headers", None)
    }
    return type(spider_name, (GenericSpider,), class_dict)