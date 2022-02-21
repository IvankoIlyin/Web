import scrapy
import requests
from bs4 import BeautifulSoup

class bangkokpostSpider(scrapy.Spider):
    name = 'bangkokpost'
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

class indiatvSpider(scrapy.Spider):
    name = 'indiatv'
    allowed_domains = ['indiatvnews.com']
    start_urls = ['https://www.indiatvnews.com/']

    def parse(self, response):
        res = response.css('li.dropdown')
        for r in res:
            category_link=r.css('a').attrib['href']
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.text_box a , .p_news:nth-child(2) a , li:nth-child(1) a , .trc_ellipsis, .title')
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

class asiaoneSpider(scrapy.Spider):
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

class chicagoSpider(scrapy.Spider):
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

class standardmediaSpider(scrapy.Spider):
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

class cbsnewsSpider(scrapy.Spider):
    name = 'cbsnews'
    allowed_domains = ['cbsnews.com']
    start_urls = ['https://www.cbsnews.com/']

    def parse(self, response):
        res = response.css('.site-nav__item,.site-nav__item--level-2')
        for r in res:
            category_link='https://www.cbsnews.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('article.item')
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

class nsnewsSpider(scrapy.Spider):
    name = 'nsnews'
    allowed_domains = ['nsnews.com']
    start_urls = ['https://www.nsnews.com/']

    def parse(self, response):
        res = response.css('li.nav-1')
        for r in res:
            category_link='https://www.nsnews.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.nsnews.com'+link.attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
