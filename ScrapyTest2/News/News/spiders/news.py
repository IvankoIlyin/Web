import scrapy
import requests
from bs4 import BeautifulSoup
import json

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com/']

    def parse(self, response):
        htmlNews = requests.get(response.url)
        newsSoup = htmlNews.text
        title=newsSoup.find_all('p')
        newsData={
            title: title
        }
        jsonNewsData = json.dumps(newsData)
        with open('News.json', 'a') as fj:
            fj.write(jsonNewsData)
