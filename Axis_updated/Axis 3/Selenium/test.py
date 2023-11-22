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


class RegulationsPdfSpider(scrapy.Spider):
    name = 'RegulationsPdfSpider'
    allowed_domains = ['regulations.citc.gov.sa']
    start_urls = ["https://regulations.citc.gov.sa/en/pages/public-consultations.aspx#/PublishedPublicConsultations"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(15)

            driver.switch_to.window(driver.window_handles[0])

            for i in range(2, 5):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.legislation-card .legislation-card-footer')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://regulations.citc.gov.sa/en/pages/public-consultations.aspx#/PublishedPublicConsultations",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date":  "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://regulations.citc.gov.sa/en/pages/public-consultations.aspx#/PublishedPublicConsultations",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '') }

                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, ".see-more a").click()
                    driver.implicitly_wait(4)


                except:
                    break
                time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)

process = CrawlerProcess(settings={
    "FEED_URI": f"Newlink_12.json",
    "FEED_FORMAT": "json",
    "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
})

process.crawl(RegulationsPdfSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time() - st}")
