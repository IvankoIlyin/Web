import json
import logging
from bs4 import BeautifulSoup
import requests
import re
logging.basicConfig(
    level='INFO',
    format='[%(levelname)-5s] %(asctime)s\t-\t%(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)



class LenationalOrg:
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
            remove_elem = self.res.find('strong')
            for i in remove_elem:
                i.clear()
            content1= []
            content_divs = self.res.find_all('div',attrs={'class':'td-post-content tagdiv-type'})
            for div in content_divs:
                for p in div.find_all(['p']):
                    if not any(keyword in p.text for keyword in self.not_allowed_keyword):
                        if str(p.text) not in str(content1):
                            content1.append(p.text)
            content = "\n".join(content1)
            content = content.replace("\xa0", " ").replace("\n\n", "")

        except:
            content = None

        ## Pub_date
        try:
            date = self.res.find('time', attrs={'class':'entry-date'})["datetime"]
        except:
            date = None




        try:
            author = self.res.find('div',
                                   attrs={'class':'td-post-author-name'}).text.replace('Écrit par : ','').replace(',','')
        except:
            author = None

        return {"title": title, "date": date, "content": content, 'author': author}



url='https://lenational.org/post_article.php?spo=1277'
response = requests.get(url)
print(response.status_code)
res = BeautifulSoup(response.content,'html.parser')

test = LenationalOrg(url,res)
data_test = test.url_response()
title = data_test['title']
author=data_test['author']
date=data_test['date']
content=data_test['content']

print(str(title)+'\n')
print(str(author)+'\n')
print(str(date)+'\n')
print(str(content)+'\n')