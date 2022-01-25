import json
import requests
from bs4 import BeautifulSoup

def Write(htmlList):
 list=[]
 for i in range(len(htmlList)):
  text=htmlList[i].text
  list.append(text)
 return list

def WriteUrl(htmlList):
 list=[]
 for i in range(len(htmlList)):
  url=htmlList[i].get('src')
  list.append(url)
 return list

urlNews='https://www.reuters.com/world/blinken-arrives-berlin-ukraine-talks-with-european-allies-2022-01-20/'
htmlNews = requests.get(urlNews)
textHtmlNews=htmlNews.text
fhtml=open("html.html","w")
fhtml.write(textHtmlNews)
fhtml.close
with open("html.html") as fp:
 newsSoup=BeautifulSoup(fp,'html5lib')
title=Write(newsSoup.find_all('title'))#check
ptime=Write(newsSoup.find_all('span', class_='DateLine__date___12trWy'))#check
articleSoup=(newsSoup.find('article'))#check
articleText=Write(list(articleSoup.find_all('p')))#check
UrlImg=WriteUrl(newsSoup.find_all('img'))#check
author=Write(newsSoup.find_all('a',class_='AuthorName__author___1tcHiY'))#check
newsData = {
 "title" : title,
 "published_time" : ptime,
 "author" : author,
 "article_text" : articleText,
 "URL_of_the_image" : UrlImg
}
jsonNewsData=json.dumps(newsData)
with open('News.json','w') as fj:
 fj.write(jsonNewsData)

