import csv
import os
import time
from scrapy.crawler import CrawlerProcess
import logging
from multiple import *

logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)


def get_spider_data(clean_rss):
    csv_reader = csv.DictReader(open('axis_dev.csv'))
    for spider in csv_reader:
        if spider['clean_rss'] == clean_rss:
            return spider


if __name__ == '__main__':
    clean_rss = 'AbpliveSpider'
    message = get_spider_data(clean_rss)
    if os.path.exists('multiple_run.json'):
        os.remove('multiple_run.json')

    process = CrawlerProcess(settings={
        "FEED_URI": f"multiple_run.json",
        "FEED_FORMAT": "json",
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.80 Safari/537.36"
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
