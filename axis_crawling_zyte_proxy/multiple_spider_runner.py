import csv
import os
import time
from scrapy.crawler import CrawlerProcess
import logging
from multiple import *
import random
from constants import *

logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)


class CustomProxyMiddleware(object):

    def process_request(self, request, spider):
        if request.meta.get("change_proxies") == True:
            proxy = self.get_random_proxy(other_proxies_trails)
        elif request.meta.get("zyte_proxy") == True:
            proxy = zyte_proxy
            logging.info({'spider_name': spider.name, 'zyte_proxy': True})
        else:
            proxy = self.get_random_proxy(us_proxies_trails)
            logging.info({'spider_name': spider.name, 'other proxy': True})

        request.meta["proxy"] = proxy

    def get_random_proxy(self, proxy_trails):
        random_proxy_trail = random.choice(proxy_trails)
        random_proxy = f"http://{PROXY_BASE_USERNAME}{random_proxy_trail}:{PROXY_PASSWORD}@{PROXY_ADDRESS}:{PROXY_PORT}"
        return random_proxy



def get_spider_data(clean_rss):
    csv_reader = csv.DictReader(open('axis_dev_US_Dept_multi_countries_Ivan_0611.csv'))
    for spider in csv_reader:
        if spider['clean_rss'] == clean_rss:
            return spider


class CustomProxyMiddleware(object):

    def process_request(self, request, spider):
        if request.meta.get("change_proxies") == True:
            proxy = self.get_random_proxy(other_proxies_trails)
        elif request.meta.get("zyte_proxy") == True:
            proxy = zyte_proxy
            logging.info({'spider_name': spider.name, 'zyte_proxy': True})
        else:
            proxy = self.get_random_proxy(us_proxies_trails)
            logging.info({'spider_name': spider.name, 'other proxy': True})

        request.meta["proxy"] = proxy

    def get_random_proxy(self, proxy_trails):
        random_proxy_trail = random.choice(proxy_trails)
        random_proxy = f"http://{PROXY_BASE_USERNAME}{random_proxy_trail}:{PROXY_PASSWORD}@{PROXY_ADDRESS}:{PROXY_PORT}"
        return random_proxy



if __name__ == '__main__':
    clean_rss = 'zatcaPdfSpider'
    message = get_spider_data(clean_rss)
    if os.path.exists('multiple_run.json'):
        os.remove('multiple_run.json')

    process = CrawlerProcess(settings={
        "FEED_URI": f"multiple_run.json",
        "FEED_FORMAT": "json",
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.80 Safari/537.36",
        'DOWNLOADER_MIDDLEWARES': {
            'generic_spider_runner.CustomProxyMiddleware': 400}
    })

    process.crawl(globals()[clean_rss],
                  clean_url=message['clean_url'],
                  clean_rss=message['clean_rss'],
                  start_urls=message['base_url'].split(','),
                  topic=message['topic'], flag=message['flag'],
                  gn_mode=message['gn_mode'],
                  type=message['type'],
                  country=message['country'])
    st = time.time()
    process.start()
    process.stop()
    print(f"this is total time {time.time() - st}")
