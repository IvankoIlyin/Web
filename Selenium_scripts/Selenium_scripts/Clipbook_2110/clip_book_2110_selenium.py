import time

from selenium.webdriver.common.by import By
from selenium import webdriver


class McknightshomecareComSpider:
    start_urls = ["https://www.mcknightshomecare.com/"]

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--ignore-ssl-errors")
        self.chrome_options.add_argument("--ignore-gpu-blacklist")
        self.chrome_options.add_argument("--use-gl")
        self.chrome_options.add_argument("--disable-cookies")
        self.chrome_options.add_argument("--disable-web-security")
        #self.chrome_options.add_argument("--headless")

    def parse(self):
        for url in self.start_urls:
            try:
                driver = webdriver.Chrome(options=self.chrome_options)
                driver.get(url)
                time.sleep(2)
                categories = driver.find_elements(By.CSS_SELECTOR, ".sub-menu li a")
                category_links = [cat.get_attribute('href') for cat in categories]
                for cat_link in category_links:
                    driver.get(cat_link)
                    time.sleep(2)
                    links = []
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, ".card-title a")
                        for link in elements:
                            l = link.get_attribute('href')
                            if 'http' in str(l):
                                links.append(str(l))
                            else:
                                links.append("https://www.realclearenergy.org" + str(l))

                    except Exception as inner_e:
                        print(f"Error processing category link: {inner_e}")
                    for url_link in list(set(links)):
                        print("parent_url:" +cat_link+ " link:" +url_link)


            except Exception as outer_e:
                print(f"Error processing start URL {url}: {outer_e}")

            finally:
                time.sleep(1)
                driver.quit()
                driver.close()


test = McknightshomecareComSpider()
test.parse()