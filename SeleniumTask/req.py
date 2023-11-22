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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36")
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage') 

datetime.datetime.utcnow()
datetime.datetime(2022, 6, 24, 9, 42, 26, 135766)
datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') 





class McinetGovSSpider(scrapy.Spider):
    name = "McinetGovSSpider"
    allowed_domains = ['mcinet.gov.ma']
    start_urls = ['https://www.msn.com/en-us/lifestyle?cvid=f43c8956dd604d86b2869aa2fb63ad84']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("SeleniumTask/WebDriver/",
                                      chrome_options=chrome_options)
            driver.get(url)

            time.sleep(15)

            links = driver.find_elements_by_css_selector('.contentCard_heading-DS-card1-2')

            for link in links:
                try:
                    if 'http' in str(link.find_element_by_tag_name('a').get_attribute('href')):
                        yield {"clean_url": self.allowed_domains[0],
                               "base_url": url,
                               "pdf_url": link.find_element_by_tag_name('a').get_attribute('href')
                               }
                    else:
                        yield {"clean_url": self.allowed_domains[0],
                               "base_url": url,
                               "pdf_url": "https://www.mcinet.gov.ma" + link.find_element_by_tag_name('a').get_attribute('href')
                               }

                except:
                    pass
            del links
            gc.collect()
            time.sleep(5)
#do not delete this spider
# (INSERT INTO ALL_SOURCES.SCRAPY_SELENIUM_REFERENCIAL
# (base_url, clean_rss, clean_url, flag, gn_mode, topic, `type`, country)
# VALUES('https://www.dubaitourism.gov.ae/en/legislative-news', 'DubaitourismSeSpider', 'dubaitourism.gov.ae', 1, 4, 'news', 'reg_article', 'United Arab Emirates');
# )
class DubaitourismSeSpider(scrapy.Spider):
    name = "DubaitourismSeSpider"
    allowed_domains = ['dubaitourism.gov.ae']
    start_urls = ['https://www.dubaitourism.gov.ae/en/legislative-news']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",chrome_options=chrome_options)
            driver.get(url)

            time.sleep(10)

            links = driver.find_elements_by_css_selector('.news__info-container')

            for link in links:
                try:
                    if 'http' in str(link.find_element_by_tag_name('a').get_attribute('href')):
                        yield{"clean_url": self.allowed_domains[0],
                            "base_url": url,
                            "link": link.find_element_by_tag_name('a').get_attribute('href')
                        }
                    else:
                        yield{"clean_url": self.allowed_domains[0],
                            "base_url": url,
                            "link": "https://added.gov.ae"+link.find_element_by_tag_name('a').get_attribute('href')
                        }
                    
    
                except:
                    pass
            del links
            gc.collect()
            time.sleep(5)



class bundestageSpider(scrapy.Spider):
    name = "ResbankSeSpider"
    allowed_domains = ['bundestag.de']
    start_urls = ['https://www.bundestag.de/drucksachen']
    not_allowed_keyword = ['/btd/']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",chrome_options=chrome_options)
            driver.get(url)

            time.sleep(10)
            # driver.find_elements_by_css_selector('#group0')[-1].click()
            # time.sleep(2)

            links = driver.find_elements_by_css_selector('.bt-linkliste li')

            for link in links:
                try:
                    if any(n in str(link.find_element_by_tag_name('a').get_attribute('href')) for n in self.not_allowed_keyword):
                        if 'http' in str(link.find_element_by_tag_name('a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                "base_url": self.start_urls[0],
                                "title": 'na',
                                "excerpt": 'na',
                                "published_date":'na',
                                "pdf_url": link.find_element_by_tag_name('a').get_attribute('href')
                                }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                "base_url": url,
                                "title":'na',
                                "excerpt": 'na',
                                "published_date": 'na',
                                "pdf_url": "https://www.bundestag.de" + link.find_element_by_tag_name('a').get_attribute(
                                    'href')
                                }

                    else:
                        pass
                except:
                    pass
            del links
            gc.collect()
            time.sleep(5)



class HandelsblattSpider(scrapy.Spider):
    name = 'HandelsblattSpider'
    allowed_domains = ['handelsblatt.com']
    start_urls = ['https://www.handelsblatt.com/?navi=HOME']

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)


    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",chrome_options=chrome_options)
            driver.get(url)
            time.sleep(5)

            for i in range(3):
                try:
                    target_iframe = driver.find_element_by_xpath("/html/body/div[12]/iframe")
                    driver.switch_to.frame(target_iframe)
                except:
                    logging.info("[HandelsblattSpider] No IFrame found")
            for i in range(2):
                try:
                    accept_button = driver.find_element(by= By.XPATH, value='//*[@id="notice"]/div[3]/div/div[1]/button[2]')
                    accept_button.click()
                    break
                except:
                    time.sleep(1)
                    logging.info("[HandelsblattSpider] No button found")
            
            time.sleep(5)
            

            nav_links = driver.find_elements(by= By.CLASS_NAME, value="vhb-c-nav__item")
            for nav_link in nav_links:
                try:
                    a_href = nav_link.find_element_by_tag_name("a").get_attribute("href")
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(a_href)
                    time.sleep(5)
                    page_links = driver.find_elements_by_css_selector('.o-teasers__item,.vhb-teaser-link,.vhb-teaser--wrapper')
                    for link in page_links[:40]:
                        if link.get_attribute('href') != None and str(link.get_attribute('href')).__contains__('handelsblatt.com') and str(link.get_attribute('href')).count('/') > 4:
                            yield({"link":link.get_attribute('href'),
                            "html": driver.page_source})
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except Exception as e:
                    logging.info("[HandelsblattSpider] Failed to get links from nav link : {} due to ".format(a_href) + str(e))
                    break
            









class ParliamentSeSpider(scrapy.Spider):
    name = "ParliamentSeSpider"
    allowed_domains = ['parliament.gov.za']
    start_urls = ['https://www.nuprc.gov.ng/acts-and-regulations']
    not_allowed_keyword = ['/ContactInformation.aspx','mediareleases.aspx','_layouts/listfeed']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",chrome_options=chrome_options)
            driver.get(url)

            time.sleep(10)
            # driver.find_elements_by_css_selector('#group0')[-1].click()
            # time.sleep(2)

            links = driver.find_elements_by_css_selector('.column-2 a')

            for link in links:
                try:
                    if any(n in str(link.find_element_by_tag_name('a').get_attribute('href')) for n in self.not_allowed_keyword):
                            pass
                    else:
                        if 'http' in str(link.find_element_by_tag_name('a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                "base_url": url,
                                # "title": link.find_element_by_tag_name('a').text if link.find_element_by_tag_name('a').text else 'na',
                                "excerpt": 'na',
                                "published_date":'na',
                                "pdf_url": link.find_element_by_tag_name('a').get_attribute('href')
                                }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                "base_url": url,
                                # "title":link.find_element_by_tag_name('a').text if link.find_element_by_tag_name('a').text else 'na',
                                "excerpt": 'na',
                                "published_date": 'na',
                                "pdf_url": "https://www.parliament.gov.za" + link.find_element_by_tag_name('a').get_attribute(
                                    'href')
                                }

                except:
                    pass
            del links
            gc.collect()
            time.sleep(5)

class BmasPdfSeSpider(scrapy.Spider):
    name = "BmasPdfSeSpider"
    allowed_domains = ['bmas.de']
    not_allowed_keyword = ['/ContactInformation.aspx', 'mediareleases.aspx', '_layouts/listfeed']
    start_urls = ['https://www.moj.gov.ae/en/laws-and-legislation/court-judgments.aspx#page=1']


    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",chrome_options=chrome_options)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)

            time.sleep(10)

            links = driver.find_elements_by_css_selector('.file--application-pdf a')
            driver.find_element_by_css_selector('#edit-field-parliament-value').click()


            for link in links:
                print(link)
                try:
                    if any(n in str(link.get_attribute('href')) for n in
                           self.not_allowed_keyword):
                        pass
                    else:
                        if 'http' in str(link.get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": self.start_urls[0],
                                #    "title": link.find_element_by_tag_name('a').text if link.find_element_by_tag_name(
                                    #    'a').text else 'na',
                                   "excerpt": 'na',
                                   "published_date": 'na',
                                   "pdf_url": link.get_attribute('href')
                                   }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": self.start_urls[0],
                                #    "title": link.find_element_by_tag_name('a').text if link.find_element_by_tag_name(
                                #        'a').text else 'na',
                                   "excerpt": 'na',
                                   "published_date": 'na',
                                   "pdf_url": "https://www.bmas.de" + link.get_attribute('href')
                                   }

                except:
                    pass
            driver.close()

            del links
            gc.collect()
            time.sleep(5)

# /html/body/main/section[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/ul/li[3]
# /html/body/main/section[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/ul/li[2]

class AdafsaSe2Spider(scrapy.Spider):
    name = "AdafsaSe2Spider"
    allowed_domains = ['adafsa.gov.ae']
    not_allowed_keyword = []
    start_urls = [
        'https://www.moccae.gov.ae/ar/legislations.aspx']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome("/Users/aakashsaini/Desktop/webdriver/chromedriver",
                                      chrome_options=chrome_options)
            driver.get(url)
            time.sleep(2)

            
            for page in range(1,17):
                next_page = f'https://www.moccae.gov.ae/ar/legislations.aspx#page={page}'
                driver.get(next_page)
                time.sleep(4)
                links = driver.find_elements(By.CSS_SELECTOR, '.item')


                for link in links:
                    try:
                        if any(n in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')) for n in
                                self.not_allowed_keyword):
                            pass
                        else:

                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": url,
                                    "title": link.find_element(By.CSS_SELECTOR, '.item-title').text,
                                    "excerpt": 'na',
                                    "published_date": "01-01-"+link.find_element(By.CSS_SELECTOR, '.date').text,
                                    "pdf_url": response.urljoin(
                                        link.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                                    }
                    except Exception as e:
                        pass
                    except:
                        links = []
                        pass

            del links
            gc.collect()
            time.sleep(5)

class Dziennikurzedowy2SeSpider(scrapy.Spider):
    name = "Dziennikurzedowy2SeSpider"
    allowed_domains = ['dziennikurzedowy.knf.gov.pl']
    not_allowed_keyword = []
    start_urls = ['https://dziennikurzedowy.knf.gov.pl/actbymonths']

    def start_requests(self):
        yield scrapy.Request(url="https://books.toscrape.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)

            time.sleep(5)

            links = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')

            for link in links:
                try:
                    if any(n in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')) for n in
                           self.not_allowed_keyword):
                        pass
                    else:

                        yield {"clean_url": self.allowed_domains[0],
                               "base_url": url,
                               "title": link.find_element(By.TAG_NAME, 'a').text,
                               "excerpt": 'na',
                               "published_date": link.find_element(By.TAG_NAME, 'data-act-date-splite').text,
                               "pdf_url": response.urljoin(
                                   link.find_element(By.TAG_NAME, 'a').get_attribute('href')).replace('legalact',
                                                                                                      'DU_KNF') + "/akt.pdf" if not link.find_element(
                                   By.TAG_NAME, 'a').get_attribute('href').endswith('/') else + "akt.pdf"
                               }
                except Exception as e:
                    pass
            for i in range(2, 13):
                driver.find_element(By.XPATH, f'//*[@id="year"]/option[{i}]').click()
                time.sleep(2)
                links = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')

                for link in links:
                    try:
                        if any(n in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')) for n in
                               self.not_allowed_keyword):
                            pass
                        else:

                            yield {"clean_url": self.allowed_domains[0],
                                   "base_url": url,
                                   "title": link.find_element(By.TAG_NAME, 'a').text,
                                   "excerpt": 'na',
                                   "published_date": link.find_element(By.TAG_NAME, 'data-act-date-splite').text,
                                   "pdf_url": response.urljoin(
                                       link.find_element(By.TAG_NAME, 'a').get_attribute('href')).replace('legalact',
                                                                                                          'DU_KNF') + "/akt.pdf" if not link.find_element(
                                       By.TAG_NAME, 'a').get_attribute('href').endswith('/') else + "akt.pdf"
                                   }
                    except Exception as e:
                        pass
            del links
            gc.collect()
            time.sleep(5)


class MoiatPdfSpider(scrapy.Spider):
    name = "MoiatPdfSpider"
    allowed_domains = ["moiat.gov.ae"]
    start_urls = ["https://moiat.gov.ae/en/about-us/laws-and-legislation"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                print(e)
            time.sleep(5)

            
            driver.switch_to.window(driver.window_handles[0])

            for i in range(1,13):
                try:
                    driver.get(f"https://moiat.gov.ae/en/about-us/laws-and-legislation?page={i}")
                    time.sleep(20)
                    pdf_div = driver.find_elements(By.CSS_SELECTOR,'tr.legislation-row-wrap')
                    for link in pdf_div:
                        if link.find_element(By.CSS_SELECTOR,'div.downloads').find_element(By.TAG_NAME,'a').get_attribute('href') != None :
                            if "http" in str(link.find_element(By.TAG_NAME,'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                "base_url": "https://moiat.gov.ae/en/about-us/laws-and-legislation",
                                "title": link.find_element(By.CSS_SELECTOR,'div.legislation-title p').text.strip(),
                                "excerpt": "na",
                                "published_date": "na",
                                "pdf_url": link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')
                                }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                "base_url": "https://moiat.gov.ae/en/about-us/laws-and-legislation",
                                "title": link.find_element(By.CSS_SELECTOR,'div.legislation-title p').text.strip(),
                                "excerpt": "na",
                                "published_date": "na",
                                "pdf_url": "https://moiat.gov.ae" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')
                                }
                    
                except:
                    break  
                time.sleep(2)
            del pdf_div


            ####################### [END] Find the Links #######################
            
            time.sleep(5)
                
            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)



class DohGovSe3Spider(scrapy.Spider):
    name = "DohGovSe3Spider"
    allowed_domains = ['doh.gov.ae']
    not_allowed_keyword = []
    start_urls = ["https://www.doh.gov.ae/en/about/law-and-legislations"]

    def start_requests(self):
        yield scrapy.Request(url="https://newscatcherapi.com/", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)

            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)

                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                except:
                    break

            links = driver.find_elements(By.CSS_SELECTOR, '.law-reg-box.animate.fadeInUp.animated')

            for link in links:
                try:
                    if any(n in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')) for n in
                           self.not_allowed_keyword):
                        pass
                    else:

                        yield {"clean_url": self.allowed_domains[0],
                               "base_url": url,
                               "title": link.find_element(By.TAG_NAME, 'h4').text,
                               "excerpt": 'na',
                               "published_date": 'na',
                               "pdf_url": response.urljoin(
                                   link.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                               }
                except Exception as e:
                    pass
                except:
                    links = []
                    pass

            del links
            gc.collect()
            time.sleep(5)


class fahrCabinetResolutionsSpider(scrapy.Spider):
    name = 'fahrCabinetResolutionsSpider'
    allowed_domains = ['fahr.gov.ae']
    start_urls = ["https://www.fahr.gov.ae/Portal/en/legislations-and-guides/the-cabinet-resolutions/cabinet-resolutions.aspx"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            time.sleep(5)

            driver.switch_to.window(driver.window_handles[0])

            for i in range(1, 4):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, 'tr.data')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls[0],
                                       "title": link.find_element(By.CSS_SELECTOR, 'td.auto').text.strip(),
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                           '..', '')
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": self.start_urls[0],
                                       "title": link.find_element(By.CSS_SELECTOR, 'td.auto').text.strip(),
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "https://www.fahr.gov.ae/Portal/" + link.find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                                           'href').replace('..', '')
                                       }

                    time.sleep(3)
                    del pdf_div

                    show_more_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                    show_more_button.click()

                except:
                    break
                time.sleep(5)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(5)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)



class SdtpsPdfSpider(scrapy.Spider):
    name = 'SdtpsPdfSpider'
    allowed_domains = ["sdtps.gov.ae"]
    start_urls = ["https://www.sdtps.gov.ae/webcenter/portal/dtps/RulesList"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            time.sleep(8)

            driver.switch_to.window(driver.window_handles[0])

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, 'div.item-inner')
                for link in pdf_div:
                    try:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": "https://www.sdtps.gov.ae/webcenter/portal/dtps/RulesList",
                                        "title": link.find_element(By.TAG_NAME, 'a').text.strip(),
                                        "excerpt": "na",
                                        "published_date": "na",
                                        "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')
                                        }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": "https://www.sdtps.gov.ae/webcenter/portal/dtps/RulesList",
                                        "title": link.find_element(By.TAG_NAME, 'a').text.strip(),
                                        "excerpt": "na",
                                        "published_date": "na",
                                        "pdf_url": "https://www.sdtps.gov.ae" + link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace('..', '')
                                        }
                    except:
                        pass

                time.sleep(3)
                del pdf_div

            except:
                pass
                time.sleep(3)

            gc.collect()

            ####################### [END] Find the Links #######################

            time.sleep(3)

            driver.quit()
            time.sleep(1)
        except Exception as e:
            logging.error(e)


class EcShjAePdfSpider(scrapy.Spider):
    name = 'EcShjAePdfSpider'
    allowed_domains = ['ec.shj.ae']
    start_urls = ["https://ec.shj.ae/legislations/"]

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

            for i in range(2, 122):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, 'div.item_')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://ec.shj.ae/legislations/",
                                       "title": link.find_elements(By.TAG_NAME, "span")[1].text.strip() if link.find_elements(By.TAG_NAME, "span")[1] else "na",
                                       "excerpt": link.find_element(By.TAG_NAME, "span").text.strip() if link.find_element(By.TAG_NAME, "span") else "na",
                                       "published_date": link.find_elements(By.TAG_NAME, "strong")[1].text.strip() if link.find_elements(By.TAG_NAME, "strong")[1] else "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                           '..', '')
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://ec.shj.ae/legislations/",
                                       "title": link.find_elements(By.TAG_NAME, "span")[1].text.strip() if link.find_elements(By.TAG_NAME, "span")[1] else "na",
                                       "excerpt": link.find_element(By.TAG_NAME, "span").text.strip() if link.find_element(By.TAG_NAME, "span") else "na",
                                       "published_date": link.find_elements(By.TAG_NAME, "strong")[1].text.strip() if link.find_elements(By.TAG_NAME, "strong")[1] else "na",
                                       "pdf_url": "https://ec.shj.ae" + link.find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                                           'href').replace('..', '')
                                       }

                    del pdf_div

                    driver.find_element(By.LINK_TEXT, str(i)).click()
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


class SssdShjAePdfSpider(scrapy.Spider):
    name = 'SssdShjAePdfSpider'
    allowed_domains = ['sssd.shj.ae']
    start_urls = ["https://sssd.shj.ae/decisions_legislation/"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(7)

            driver.switch_to.window(driver.window_handles[0])

            try:
                close_modal = driver.find_element(By.XPATH, '/html/div[3]/div/div[1]/a')
                close_modal.click()
            except:
                pass

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, 'table.table-striped tbody tr')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://sssd.shj.ae/decisions_legislation",
                                    "title": link.find_element(By.TAG_NAME, "label").text.strip() if link.find_element(By.TAG_NAME, "label") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://sssd.shj.ae/decisions_legislation",
                                    "title": link.find_element(By.TAG_NAME, "label").text.strip() if link.find_element(By.TAG_NAME, "label") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": "https://sssd.shj.ae" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

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


class ItcGovAePdfSpider(scrapy.Spider):
    name = 'ItcGovAePdfSpider'
    allowed_domains = ['itc.gov.ae']
    start_urls = ["https://www.itc.gov.ae/en/Media/Publications/"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(10)

            driver.switch_to.window(driver.window_handles[0])

            for i in range(10, 30, 10):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, 'div.details-top')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.itc.gov.ae/en/Media/Publications",
                                       "title": link.find_element(By.CSS_SELECTOR, "span.title").text.strip() if link.find_element(By.CSS_SELECTOR, "span.title") else "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                           '..', '')
                                       }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": "https://www.itc.gov.ae/en/Media/Publications",
                                       "title": link.find_element(By.CSS_SELECTOR, "span.title").text.strip() if link.find_element(By.CSS_SELECTOR, "span.title") else "na",
                                       "excerpt": "na",
                                       "published_date": "na",
                                       "pdf_url": "https://www.itc.gov.ae" + link.find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                                           'href').replace('..', '')
                                       }

                    del pdf_div

                    driver.get(f"https://www.itc.gov.ae/en/Media/Publications#publications_e={i}")
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



class DfsaenThomsonreutersConsultationPapersPdfSpider(scrapy.Spider):
    name = 'DfsaenThomsonreutersConsultationPapersPdfSpider'
    allowed_domains = ["dfsaen.thomsonreuters.com"]
    start_urls = ["https://dfsaen.thomsonreuters.com/rulebook/consultation-papers/"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                pass
            driver.implicitly_wait(5)

            driver.switch_to.window(driver.window_handles[0])

            ## For Current papers
            try:
                driver.get("https://dfsaen.thomsonreuters.com/rulebook/current-papers")
                driver.implicitly_wait(5)
                data1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/aside/div/div/nav/ul/li/ul/li[8]/ul/li[1]')
                data2 = data1.find_elements(By.CSS_SELECTOR, 'ul.menu li.menu-item')
                for link in data2:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Current Papers",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Current Papers",
                                    "published_date": "na",
                                    "pdf_url": "https://dfsaen.thomsonreuters.com" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

                del data1
                del data2
                

            except:
                pass
            time.sleep(3)


            ## For Current papers
            try:
                driver.get("https://dfsaen.thomsonreuters.com/rulebook/current-papers")
                driver.implicitly_wait(5)
                data1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/aside/div/div/nav/ul/li/ul/li[8]/ul/li[1]')
                data2 = data1.find_elements(By.CSS_SELECTOR, 'ul.menu li.menu-item')
                for link in data2:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Current Papers",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Current Papers",
                                    "published_date": "na",
                                    "pdf_url": "https://dfsaen.thomsonreuters.com" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

                del data1
                del data2
                

            except:
                pass
            time.sleep(3)## For Past papers
            try:
                driver.get("https://dfsaen.thomsonreuters.com/rulebook/past-papers")
                driver.implicitly_wait(5)
                data1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/aside/div/div/nav/ul/li/ul/li[8]/ul/li[2]')
                data2 = data1.find_elements(By.CSS_SELECTOR, 'ul.menu li.menu-item')
                for link in data2:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Past Papers",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://dfsaen.thomsonreuters.com/rulebook/consultation-papers",
                                    "title": link.find_element(By.TAG_NAME, "a").text.strip() if link.find_element(By.TAG_NAME, "a") else "na",
                                    "excerpt": "Past Papers",
                                    "published_date": "na",
                                    "pdf_url": "https://dfsaen.thomsonreuters.com" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

                del data1
                del data2
                

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


class ScaGovAePdfSpider(scrapy.Spider):
    name = 'ScaGovAePdfSpider'
    allowed_domains = ['sca.gov.ae']
    start_urls = ["https://www.sca.gov.ae/en/regulations/regulations-listing.aspx#page=1"]

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
                pdf_div = driver.find_elements(By.CSS_SELECTOR, 'div.data-item')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://www.sca.gov.ae/en/regulations/regulations-listing.aspx#page=1",
                                    "title": link.find_element(By.TAG_NAME, "h4").text.strip() if link.find_element(By.TAG_NAME, "h4") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://www.sca.gov.ae/en/regulations/regulations-listing.aspx#page=1",
                                    "title": link.find_element(By.TAG_NAME, "h4").text.strip() if link.find_element(By.TAG_NAME, "h4") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": "https://www.sca.gov.ae" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

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




class DoeGovAePdfSpider(scrapy.Spider):
    name = "DoeGovAePdfSpider"
    allowed_domains = ['doe.gov.ae']
    start_urls = ["https://www.doe.gov.ae/Publications#publication-listing_categoryname=Codes%20of%20Practice", "https://www.doe.gov.ae/Publications#publication-listing_categoryname=Codes",
                  'https://www.doe.gov.ae/Publications#publication-listing_categoryname=Guidance', 'https://www.doe.gov.ae/Publications#publication-listing_categoryname=Laws',
                  'https://www.doe.gov.ae/Publications#publication-listing_categoryname=Regulations','https://www.doe.gov.ae/Publications#publication-listing_categoryname=Resolutions']

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        for url in self.start_urls:
            try:
                driver = webdriver.Chrome(chrome_options=chrome_options)
                try:
                    driver.get(url)
                except Exception as e:
                    pass
                driver.implicitly_wait(6)
                driver.switch_to.window(driver.window_handles[0])

                try:
                    accept_cookies_btn = driver.find_element(By.CSS_SELECTOR, ".submit > a:nth-child(1)")
                    accept_cookies_btn.click()
                    time.sleep(1)
                except:
                    pass

                while True:
                    try:
                        show_more_button = driver.find_element(By.CSS_SELECTOR, ".load-more > div:nth-child(1) > input:nth-child(1)")
                        show_more_button.click()
                    except Exception as e:
                        break

                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR, 'ul.search-result-list li')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                            if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": url,
                                        "title": link.find_element(By.CSS_SELECTOR, "p.field-title").text.strip(),
                                        "excerpt": link.find_element(By.CSS_SELECTOR, "span.field-title").text.strip(),
                                        "published_date": "na",
                                        "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                            '..', '')
                                        }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                        "base_url": url,
                                        "title": link.find_element(By.CSS_SELECTOR, "p.field-title").text.strip(),
                                        "excerpt": link.find_element(By.CSS_SELECTOR, "span.field-title").text.strip(),
                                        "published_date": "na",
                                        "pdf_url": "https://www.doe.gov.ae" + link.find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                                            'href').replace('..', '')
                                        }

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


class AdxAePdfSpider(scrapy.Spider):
    name = 'AdxAePdfSpider'
    allowed_domains = ['adx.ae']
    start_urls = ["https://www.adx.ae/English/pages/regulations/marketrules.aspx"]

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

            try:
                pdf_div = driver.find_elements(By.CSS_SELECTOR, 'div.rules-box div.col-sm-6')
                for link in pdf_div:
                    if link.find_element(By.TAG_NAME, 'a').get_attribute('href') != None:
                        if "http" in str(link.find_element(By.TAG_NAME, 'a').get_attribute('href')):
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://www.adx.ae/English/pages/regulations/marketrules.aspx",
                                    "title": link.find_element(By.TAG_NAME, "span").text.strip() if link.find_element(By.TAG_NAME, "span") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": link.find_element(By.TAG_NAME, 'a').get_attribute('href').replace(
                                        '..', '')
                                    }
                        else:
                            yield {"clean_url": self.allowed_domains[0],
                                    "base_url": "https://www.adx.ae/English/pages/regulations/marketrules.aspx",
                                    "title": link.find_element(By.TAG_NAME, "span").text.strip() if link.find_element(By.TAG_NAME, "span") else "na",
                                    "excerpt": "na",
                                    "published_date": "na",
                                    "pdf_url": "https://www.adx.ae" + link.find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                                        'href').replace('..', '')
                                    }

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


class DubaitourismGovAeSpider(scrapy.Spider):
    name = 'DubaitourismGovAeSpider'
    allowed_domains = ['dubaitourism.gov.ae']
    start_urls = ["https://www.dubaitourism.gov.ae/en/legislative-news"]

    def start_requests(self):
        yield scrapy.Request(url="https://google.com", callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            try:
                driver.get(self.start_urls[0])
            except Exception as e:
                print(e)
            time.sleep(5)
            
            driver.switch_to.window(driver.window_handles[0])
            
            
            for i in range(1,10):
                try:
                    pdf_div = driver.find_elements(By.CSS_SELECTOR,'div.news__info-container')
                    for link in pdf_div:
                        if link.find_element(By.TAG_NAME,'a').get_attribute('href') != None :
                            if "http" in str(link.find_element(By.TAG_NAME,'a').get_attribute('href')):
                                yield {"clean_url": self.allowed_domains[0],
                                "base_url": "https://www.dubaitourism.gov.ae/en/legislative-news",
                                "title": link.find_element(By.TAG_NAME,'a').text.strip(),
                                "excerpt": link.find_element(By.CSS_SELECTOR,'p.news_pageintro').text.strip(),
                                "published_date": "na",
                                "pdf_url": link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')
                                }
                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                "base_url": "https://www.dubaitourism.gov.ae/en/legislative-news",
                                "title": link.find_element(By.TAG_NAME,'a').text.strip(),
                                "excerpt": link.find_element(By.CSS_SELECTOR,'p.news_pageintro').text.strip(),
                                "published_date": "na",
                                "pdf_url": "https://www.dubaitourism.gov.ae" + link.find_element(By.TAG_NAME,'a').get_attribute('href').replace('..', '')
                                }
                    
                    time.sleep(2)
                    try:
                        show_more_button = driver.find_element(By.CSS_SELECTOR, "button.load-more__btn")
                        show_more_button.click()
                    except Exception as e:
                        print(e)
                        logging.error(e)
                    time.sleep(6)

                except Exception as e:
                    break  

            del pdf_div
            gc.collect()
                
            driver.quit()
            time.sleep(3)
        except Exception as e:
            logging.error(e)

        
        
        # //*[@id="onetrust-accept-btn-handler"]

# //*[@id="leftMenuItems"]/li[2]/a
# //*[@id="year"]/option[12]
# //*[@id="year"]/option[11]
# //*[@id="year"]/option[2]
process = CrawlerProcess(settings={
                "FEED_URI": f"Newlink_12.json",
                "FEED_FORMAT": "json",
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(DubaitourismGovAeSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")
