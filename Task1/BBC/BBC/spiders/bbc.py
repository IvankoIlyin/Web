import scrapy
import requests
from bs4 import BeautifulSoup

class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bangkokpost.com']
    start_urls = ['https://www.bangkokpost.com/']

    def parse(self, response):
        result = response.css('div.menu-panel')
        res=result.css('a::attr(href)').getall()
        for r in res:
            category_link='https://www.bangkokpost.com/'+r
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('h3')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
        print('https://www.bangkokpost.com/'+link.css('a').attrib['href'])
