import scrapy
import requests
from bs4 import BeautifulSoup

class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bangkokpost.com']
    start_urls = ['https://www.bangkokpost.com/']

    def parse(self, response):
        result = response.css('.menu-list a')
        for r in result:
            category_link='https://www.bangkokpost.com/'+r.attrib['href']
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.xpath('a.chanel')
        print("RESULT")
        print(data)
        for link in data:
            try:
                yield {
                    "News_links": link.attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }