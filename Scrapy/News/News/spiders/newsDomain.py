import scrapy
import requests
from bs4 import BeautifulSoup
import json


def Write(htmlList):
    list = []
    for i in range(len(htmlList)):
        text = htmlList[i].text
        list.append(text)
    return list


def WriteUrl(htmlList):
    list = []
    for i in range(len(htmlList)):
        url = htmlList[i].get('src')
        list.append(url)
    return list




class NewsdomainSpider(scrapy.Spider):
    name = 'newsDomain'
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com/']

    def parse(self, response):
        htmlNews = requests.get(response.url)
        newsSoup= htmlNews.text
        print(response)
        title = Write(newsSoup.find_all('title'))  # check
        ptime = Write(newsSoup.find_all('span', class_='DateLine__date___12trWy'))  # check
        articleSoup = (newsSoup.find('article'))  # check
        articleText = Write(list(articleSoup.find_all('p')))  # check
        UrlImg = WriteUrl(newsSoup.find_all('img'))  # check
        author = Write(newsSoup.find_all('a', class_='AuthorName__author___1tcHiY'))  # check
        newsData = {
            "title": title,
            "published_time":ptime,
            "author": author,
            "article_text":articleText,
            "URL_of_the_image":UrlImg
        }
        jsonNewsData = json.dumps(newsData)
        with open('News.json', 'a') as fj:
            fj.write(jsonNewsData)

