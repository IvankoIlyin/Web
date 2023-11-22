import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

browser = webdriver.Chrome()
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://www.youtube.com/")
videos = driver.find_element(ById = "video-title")
print(videos)
