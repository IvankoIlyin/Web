import json
import logging
from bs4 import BeautifulSoup
import requests
import re

from scrappey_API import make_scrappey, make_scrapingbee

logging.basicConfig(
    level='INFO',
    format='[%(levelname)-5s] %(asctime)s\t-\t%(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)



class IrishmirrorIe:
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = ['READ MORE:','Sign up to']

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            content1= []
            content_divs = self.res.find_all('div',attrs={'class':'article-body'})
            for div in content_divs:
                for p in div.find_all(['p']):
                    if p.select('b a'):
                        continue
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        if str(p.text) not in str(content1):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta', attrs={'property':'article:published_time'})["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class HeadtopicsCom:#scrappey
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = []

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            remove_elem=self.res.find_all(attrs={'class':['News-Part','Tag']})
            for i in remove_elem:
                i.clear()
            content1= []
            content_divs = self.res.find_all('div',attrs={'class':'ArticleContentBlock--text'})
            for div in content_divs:
                for p in div.find_all(['p']):
                    if p.select('b a'):
                        continue
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        if str(p.text) not in str(content1):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta', attrs={'property':'article:published_time'})["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class TahlequahdailypressCom:
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = []

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            content1= []
            content_divs = self.res.find_all('div',attrs={'id':'article-body'})
            for div in content_divs:
                for p in div.find_all(['p','h4']):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        if str(p.text) not in str(content1):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('time', attrs={'class':'tnt-date'})["datetime"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class SlateCom:
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = []

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            content1= []
            content_divs = self.res.find_all('div',attrs={'class':['article__content','podcast-episode__main-bottom']})
            for div in content_divs:
                for p in div.find_all(['p','h4']):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        if str(p.text) not in str(content1):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('time')["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class AlCom:
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = ['Privacy Policy','Read more']

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            content1= []
            content_divs = self.res.find_all('div',attrs={'class':['entry-content']})
            for div in content_divs:
                for p in div.find_all('p',attrs={'class':['article__paragraph']}):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta',attrs={'property':'article:published_time'})["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'trackonomics.author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}




url='https://www.al.com/sports/2024/11/alcom-college-football-staff-picks-for-week-11-of-2024.html'
response = requests.get(url)
print(response.status_code)
res = BeautifulSoup(response.content,'html.parser')


#res = make_scrappey(url)


test = AlCom(url,res)
data_test = test.url_response()
title = data_test['title']
author=data_test['author']
date=data_test['date']
content=data_test['content']

print(str(title)+'\n')
print(str(author)+'\n')
print(str(date)+'\n')
print(str(content)+'\n')