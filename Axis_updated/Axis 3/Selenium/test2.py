import time
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import gc

import logging

logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

timeout = 30

from selenium import webdriver
def handle_error(failure):
    pass

cat_timeout = 300
logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.INFO)  # or any variant from ERROR, CRITICAL or NOTSET
# Headless Chrome is a way to run the Chrome browser in a headless environment.
# Essentially, running Chrome without chrome! It brings all modern web platform features provided
# by Chromium and the Blink rendering engine to the command line.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')

datetime.datetime.utcnow()
datetime.datetime(2022, 6, 24, 9, 42, 26, 135766)
datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


class TaxSpider(scrapy.Spider):
    name = "TaxSpider"
    allowed_domains = ['tax.gov.ae']
    start_urls = ['https://tax.gov.ae/en/legislation.aspx']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)


    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("Users\Denys\Desktop\Webdriver\chromedriver", chrome_options=chrome_options)
            driver.get(url)

            time.sleep(10)
            category_links = self.start_urls
            links = driver.find_elements(By.CSS_SELECTOR, 'PageLi')

            for link in links:
                try:
                    if 'http' in str(link.find_element(By.TAG_NAME,'a').get_attribute('href')):
                        category_links.append(link.find_element(By.TAG_NAME,'a').get_attribute('href'))
                    else:
                         category_links.append("" + link.find_element(By.TAG_NAME,'a').get_attribute('href'))
                except:
                    pass
            del links
            gc.collect()
            time.sleep(5)

        for i in set(category_links):
            base_url = response.meta.get('base_url')
            try:

                if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                    yield {"clean_url": self.allowed_domains[0],
                           "base_url": base_url,
                           "pdf_url": link.css("a").attrib["href"], }
                else:
                    yield {"clean_url": self.allowed_domains[0],
                           "base_url": base_url,
                           "pdf_url": "" + link.css("a").attrib["href"], }

            except:
                pass

    def article_links(self, response):
        driver = webdriver.Chrome("Users\Denys\Desktop\Webdriver\chromedriver", chrome_options=chrome_options)

        base_url = response.meta.get('base_url')
        data = driver.find_elements(By.CSS_SELECTOR, 'd-flex flex-row downloadlinks')
        for link in data:
            try:
                if "https://" in str(link.css(".download-doc-link").attrib["href"]):
                    yield {"clean_url": self.allowed_domains[0],
                           "base_url": base_url,
                           "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href')}
                else:
                    yield {"clean_url": self.allowed_domains[0],
                           "base_url": base_url,
                           "pdf_url":"" + link.find_element(By.TAG_NAME, 'a').get_attribute('href')}

            except:
                pass



process = CrawlerProcess(settings={
    "FEED_URI": f"Newlink_12.json",
    "FEED_FORMAT": "json",
    "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
})

process.crawl(TaxSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time() - st}")
