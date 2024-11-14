import logging
from bs4 import BeautifulSoup
import requests
import re
logging.basicConfig(
    level='INFO',
    format='[%(levelname)-5s] %(asctime)s\t-\t%(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)



class archynewsyComUniqueClass():
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
            content_divs = self.res.find_all('div',attrs={'class':'entry-content'})
            for div in content_divs:
                for p in div.find_all(['p']):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ")
        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta',attrs={'property':'article:published_time'})["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class newsyTodayComUniqueClass():
    def __init__(self, url,res) -> None:
        self.url = url
        self.res = res
        self.not_allowed_keyword = ["Scene-setting","Subtitle:","!:","End of Article","Sources:"]

    def url_response(self):

        ## Title
        try:
            title = self.res.find('meta', attrs={'property':'og:title'})["content"]
        except:
            title = None

        ## Content
        try:
            remove_elem = res.find_all('div',attrs={'class':'jp-relatedposts'})
            for i in remove_elem:
                i.clear()
            content1= []
            content_divs = self.res.find('div',attrs={'data-editable':'content'})
            if not content_divs:
                content_divs =self.res.find('div',attrs={'data-widget_type':'theme-post-content.default'})
            for p in content_divs.find_all(['p']):
                if 'Read the full story:' in p.text:
                    break
                if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                    content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ")
        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta',attrs={'property':'article:published_time'})["content"]
        except:
            date = None

        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

class sfreporterСomUniqueClass():
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
            remove_elem = res.find_all(attrs={'class':'media-carousel'})
            for i in remove_elem:
                i.clear()
            content1= []
            content_divs = self.res.find_all('div',attrs={'id':'content'})
            for div in content_divs:
                for p in div.find_all(['p']):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ")
        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('meta',attrs={'property':'article:published_time'})["content"]
        except:
            date = None




        try:
            author = self.res.find('meta',attrs={'name':'author'})["content"]
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}

url='https://www.newsy-today.com/i-am-keen-on-extensions-as-a-result-of-theyre-lovely-3/'
response = requests.get(url)
print(response.status_code)
res = BeautifulSoup(response.content,'html.parser')

test = newsyTodayComUniqueClass(url,res)
data_test = test.url_response()
title = data_test['title']
author=data_test['author']
date=data_test['date']
content=data_test['content']

print(str(title)+'\n')
print(str(author)+'\n')
print(str(date)+'\n')
print(str(content)+'\n')