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

class BbcSpider(scrapy.Spider):
    name = 'indiatv'
    allowed_domains = ['indiatvnews.com']
    start_urls = ['https://www.indiatvnews.com/']

    def parse(self, response):
        res = response.css('li.dropdown')
        for r in res:
            category_link=r.css('a').attrib['href']
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('h3.title')
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

class BbcSpider(scrapy.Spider):
    name = 'asiaone'
    allowed_domains = ['asiaone.com']
    start_urls = ['https://www.asiaone.com/']

    def parse(self, response):
        res = response.css('li.ant-menu-item')
        for r in res:
            category_link='https://www.asiaone.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('button.btn-read-more')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
            print(link.css('a').attrib['href'])

class BbcSpider(scrapy.Spider):
    name = 'chicago'
    allowed_domains = ['chicagotribune.com']
    start_urls = ['https://www.chicagotribune.com/']

    def parse(self, response):
        res = response.css('li.link-list')
        for r in res:
            category_link='https://www.chicagotribune.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('div.crd--cnt')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }
            print(link.css('a::attr(href)').get())

class BbcSpider(scrapy.Spider):
    name = 'standardmedia'
    allowed_domains = ['standardmedia.co.ke']
    start_urls = ['https://www.standardmedia.co.ke/']

    def parse(self, response):
        res = response.css('li.nav-item')
        for r in res:
            category_link=r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('div.card')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
            print(link.css('a').attrib['href'])