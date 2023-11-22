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

#1
class CpaPdfSpider(scrapy.Spider):
    name = 'CpaPdfSpider'
    allowed_domains = ['cpa.org.sa']
    start_urls = ["https://cpa.org.sa/page/93/"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.card-body')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://cpa.org.sa/page/93/",
                                   "title": link.find_element(By.CSS_SELECTOR, ".card-text strong").text.strip(),
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://cpa.org.sa/page/93/",
                                   "title": "na",
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#2
class MtPdfSpider(scrapy.Spider):
    name = 'MtPdfSpider'
    allowed_domains = ['mt.gov.sa']
    start_urls = ["https://mt.gov.sa/policies-regulations/tourism-regulaitons"]

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

            for i in range(2, 7):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.h-Eserv.d-flex.flex-column.flex-md-row.align-items-center')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://mt.gov.sa/policies-regulations/tourism-regulaitons",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://mt.gov.sa/policies-regulations/tourism-regulaitons",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "https://cdn.mt.gov.sa" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, str(".row.nav div:nth-child(" + str(i) + ")")).click()
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
#3
class McPdfSpider(scrapy.Spider):
    name = 'McPdfSpider'
    allowed_domains = ['mc.gov.sa']
    start_urls = ["https://mc.gov.sa/en/Regulations/Pages/default.aspx"]

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

            for i in range(3, 6):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.col-sm-5.card-actions')
                    for link in pdf_div:
                        if link.find_element(By.CSS_SELECTOR, 'a.icon-attach').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.CSS_SELECTOR, 'a.icon-attach').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://mt.gov.sa/policies-regulations/tourism-regulaitons",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.CSS_SELECTOR, 'a.icon-attach').get_attribute('href').replace(';', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://mt.gov.sa/policies-regulations/tourism-regulaitons",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "https://mc.gov.sa/" + link.find_element(By.CSS_SELECTOR, 'a.icon-attach').get_attribute('href').replace(';', '')}
                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, str(".pagination li:nth-child(" + str(i) + ") a")).click()
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
#4
class MoePdfSpider(scrapy.Spider):
    name = 'MoePdfSpider'
    allowed_domains = ['moe.gov.sa']
    start_urls = ["https://www.moe.gov.sa/en/aboutus/nationaltransformation/Pages/rpr.aspx"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.blog-info.text-right')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://www.moe.gov.sa/en/aboutus/nationaltransformation/Pages/rpr.aspx",
                                   "title": link.find_element(By.TAG_NAME, "h3").text.strip(),
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://www.moe.gov.sa/en/aboutus/nationaltransformation/Pages/rpr.aspx",
                                   "title": link.find_element(By.TAG_NAME, "h3").text.strip(),
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#5
class MewaPdfSpider(scrapy.Spider):
    name = 'MewaPdfSpider'
    allowed_domains = ['mewa.gov.sa']
    start_urls = ["https://www.mewa.gov.sa/en/InformationCenter/DocsCenter/RulesLibrary/Pages/default.aspx"]

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

            for i in range(1, 5):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.table.table-bordered.Grid')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.mewa.gov.sa/en/InformationCenter/DocsCenter/RulesLibrary/Pages/default.aspx",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.mewa.gov.sa/en/InformationCenter/DocsCenter/RulesLibrary/Pages/default.aspx",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, str(".GridFooterPager a:nth-child(8)")).click()
                    driver.implicitly_wait(4)
                    time.sleep(3)

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
#6
class MomrahPdfSpider(scrapy.Spider):
    name = 'MomrahPdfSpider'
    allowed_domains = ['momrah.gov.sa']
    start_urls = ["https://momrah.gov.sa/ar/regulations?pageNumber=1"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.reg-set-box')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://momrah.gov.sa/ar/regulations?pageNumber=1",
                                   "title": link.find_element(By.TAG_NAME, "p").text.strip(),
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://momrah.gov.sa/ar/regulations?pageNumber=1",
                                   "title": link.find_element(By.TAG_NAME, "p").text.strip(),
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#7
class SaipPdfSpider(scrapy.Spider):
    name = 'SaipPdfSpider'
    allowed_domains = ['saip.gov.sa']
    start_urls = ["https://saip.gov.sa/en/privacy-legislation/#regulations_and_regulations"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.service-item')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/privacy-legislation/#regulations_and_regulations",
                                   "title": link.find_element(By.CSS_SELECTOR, ".service-item__title.my-4").text.strip(),
                                   "excerpt": "na",
                                   "published_date": link.find_element(By.CSS_SELECTOR, ".service-item-data+ .service-item-data .service-item-data__subtitle").text.strip(),
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/privacy-legislation/#regulations_and_regulations",
                                   "title": link.find_element(By.CSS_SELECTOR, ".service-item__title.my-4").text.strip(),
                                   "excerpt": "na",
                                   "published_date": link.find_element(By.CSS_SELECTOR, ".service-item-data+ .service-item-data .service-item-data__subtitle").text.strip(),
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#8
class Saip1PdfSpider(scrapy.Spider):
    name = 'Saip1PdfSpider'
    allowed_domains = ['saip.gov.sa']
    start_urls = ["https://saip.gov.sa/en/privacy-legislation/#guiding_policies"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.col-md-5')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/privacy-legislation/#guiding_policies",
                                   "title": "na",
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/privacy-legislation/#guiding_policies",
                                   "title": "na",
                                   "excerpt": "na",
                                   "published_date": "na",
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#9
class Saip2PdfSpider(scrapy.Spider):
    name = 'Saip2PdfSpider'
    allowed_domains = ['saip.gov.sa']
    start_urls = ["https://saip.gov.sa/en/ip-domains/239/#publications"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(45)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, '.g-0.row')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/ip-domains/239/#publications",
                                   "title": link.find_element(By.CSS_SELECTOR, ".main-color").text.strip(),
                                   "excerpt": "na",
                                   "published_date": link.find_element(By.CSS_SELECTOR, ".font-75").text.strip(),
                                   "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": "https://saip.gov.sa/en/ip-domains/239/#publications",
                                   "title": link.find_element(By.CSS_SELECTOR, ".main-color").text.strip(),
                                   "excerpt": "na",
                                   "published_date": link.find_element(By.CSS_SELECTOR, ".font-75").text.strip(),
                                   "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                del pdf_div


            except:
                pass
            time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(2)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)
#10
class Saso1PdfSpider(scrapy.Spider):
    name = 'Saso1PdfSpider'
    allowed_domains = ['saso.gov.sa']
    start_urls = ["https://www.saso.gov.sa/en/Laws-And-Regulations/guidelines/Pages/default.aspx"]

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

            for i in range(4, 6):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.col-md-3.col-sm-6.col-12')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.saso.gov.sa/en/Laws-And-Regulations/guidelines/Pages/default.aspx",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.saso.gov.sa/en/Laws-And-Regulations/guidelines/Pages/default.aspx",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, ".pagination span a:nth-child(" + str(i) + ")").click()
                    driver.implicitly_wait(4)
                    time.sleep(2)

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
#11
class SasoPdfSpider(scrapy.Spider):
    name = 'SasoPdfSpider'
    allowed_domains = ['saso.gov.sa']
    start_urls = ["https://www.saso.gov.sa/en/Laws-And-Regulations/technical_regulations/Pages/default.aspx"]

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

            for i in range(1, 6):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, '.col-md-3.col-sm-6.col-12')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.saso.gov.sa/en/Laws-And-Regulations/technical_regulations/Pages/default.aspx",
                                       "title":  "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')}
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.saso.gov.sa/en/Laws-And-Regulations/technical_regulations/Pages/default.aspx",
                                       "title": "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')}
                    del pdf_div

                    driver.find_element(By.CSS_SELECTOR, str("a.Next")).click()
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
                "FEED_URI": f"Newlink_15.json",
                "FEED_FORMAT": "json",
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(SasoPdfSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")