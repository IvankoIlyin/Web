import scrapy
from scrapy.crawler import CrawlerProcess
import logging

timeout = 30
proxy_user = 'abcdefgh12'
proxy_pass = 'uo5hv5r25so2'
proxy_ip = '45.142.28.83:8094'
cat_timeout = 5


logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

proxy = "http://{}:{}@{}".format(proxy_user,proxy_pass, proxy_ip)

def handle_error(failure):
    pass

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.treasuryandrisk.com']
    start_urls = ['https://www.treasuryandrisk.com/']

    def parse(self, response):
        topic_links = response.css("#topics a")
        for link in topic_links:
            categories_links = "https://www.treasuryandrisk.com" + link.attrib['href']
            yield response.follow(categories_links, callback=self.news_links)

    def news_links(self, response):
        result = response.css(".cr2 .brief")
        for r in result:
            yield {
                "News_links": "https://www.treasuryandrisk.com/" + r.css('a')[1].attrib['href'],
                # "Title":r.css('a::text')[1].get().strip(),

            }


class PenSpider(scrapy.Spider):
    name = 'pen'
    allowed_domains = ['www.penews.com']
    start_urls = ['https://www.penews.com/news-topics?filter_by_topic']

    def parse(self, response):
        result = response.css('.PENTheme--topic--dWcMgVWf a')
        for r in result:
            '''yield{
                "Cat":'https://www.penews.com'+r.attrib['href']
            }'''
            category_link = 'https://www.penews.com' + r.attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('a.PENTheme--headline-link--3tkfvFGB')
        for link in data:
            try:
                yield {
                    "News_links": link.attrib['href']
                }
            except:
                yield {
                    "News_links": 'Na'
                }


class LegalSpider(scrapy.Spider):
    name = 'legal'
    allowed_domains = ['www.legalitprofessionals.com']
    start_urls = ['https://www.legalitprofessionals.com/legal-it-news/']

    def parse(self, response):
        result = response.css(".items-leading .gradient")
        for r in result:
            try:
                yield {
                    "News_links": "https://www.legalitprofessionals.com" + r.css(".readmore-link").attrib['href'],
                    # "Title":r.css('h2::text').get().strip(),
                    # "Country":r.i.css("div.mbNewsFlagHolder::text").extract(),
                }
            except:
                yield {
                    "News links": "Na",
                    "Title": 'Na',
                }

        next_page = 'https://www.legalitprofessionals.com' + response.css(".pagination-next .pagenav").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class NewsSpider_consultancy(scrapy.Spider):
    name = 'consult'
    allowed_domains = ['www.consultancy.uk']
    start_urls = ['https://www.consultancy.uk/news/']

    def parse(self, response):
        result = response.css('.index1')
        for r in result:
            try:
                yield {
                    "News_links": 'https://www.consultancy.uk' + r.css('a').attrib['href']

                }
            except:
                yield {
                    "News_links": 'Na'

                }

        next_page = 'https://www.consultancy.uk' + response.css('.active+ li .a-paging').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse)


class bangkokpostSpider(scrapy.Spider):
    name = 'bangkokpost'
    allowed_domains = ['bangkokpost.com']
    start_urls = ['https://www.bangkokpost.com/']

    def parse(self, response):
        res=response.css('.divNav--row').css('li')
        for r in range(0,32):
            category_link='https://www.bangkokpost.com/'+res[r].css('a').attrib['href']
            print('Res: ',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.list-detail, .listnews-text').css('h3,h2')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.bangkokpost.com/'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#20.02.2022
class indiatvSpider(scrapy.Spider):
    name = 'indiatv'
    allowed_domains = ['indiatvnews.com']
    start_urls = ['https://www.indiatvnews.com/']

    def parse(self, response):
        res2=response.css('ul.menu_link').css('li')
        res1 = response.css('#li-trending a , #li-health a , #li-photos a , #li-technology a , #li-entertainment a , #li-sports a , #li-world a , #li-india a , .link_elections_2022 a , #li-astrology a , #li-video a')
        for r in res1:
            category_link=r.css('a').attrib['href']
            yield response.follow(category_link,callback=self.article_links)
        for r in res2:
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
        res = response.css('#trending-topics-wrapper .tag-solid')
        for r in res:
            category_link='https://www.chicagotribune.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('div.crd--cnt, .clln-it-bdr-btm , .ntv-ad-text , .crd--tle , .river')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.chicagotribune.com'+ link.css('a::attr(href)').get()
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
        res = response.css('.nav-item:nth-child(2) .nav-link , .nav-item:nth-child(3) .nav-link , .nav-item:nth-child(4) .nav-link , .nav-item:nth-child(5) .nav-link , .nav-item:nth-child(6) .nav-link , .nav-item:nth-child(7) .nav-link , .nav-item:nth-child(8) .nav-link , .nav-item:nth-child(9) .nav-link , .nav-item:nth-child(10) .nav-link , .w-15 .nav-link , .nav-item:nth-child(1) .nav-link')
        for r in range(0,10):
            category_link=res[r].css('a').attrib['href']
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
#21.02.2022
class cbsnewsSpider(scrapy.Spider):
    name = 'cbsnews'
    allowed_domains = ['cbsnews.com']
    start_urls = ['https://www.cbsnews.com/']

    def parse(self, response):
        res = response.css('li.site-nav__item--first').css('ul').css('li.site-nav__item--level-2')
        for r in range(0,12):
            category_link='https://www.cbsnews.com'+res[r].css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.item__anchor , #component-topic-world .lazyloaded')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class nsnewsSpider(scrapy.Spider):
    name = 'nsnews'
    allowed_domains = ['nsnews.com']
    start_urls = ['https://www.nsnews.com/']

    def parse(self, response):
        res=response.css('#nav-home+ .theme-blue .navitem')
        for r in res:
            category_link='https://www.nsnews.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('#category-items,.section-items').css('a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.nsnews.com'+link.attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ibtimesSpider(scrapy.Spider):
    name = 'ibtimes'
    allowed_domains = ['ibtimes.com']
    start_urls = ['https://www.ibtimes.com/']

    def parse(self, response):
        res = response.css('#block-ibtimes-footer-ibtimes-footer .leaf')
        for r in res:
            category_link='https://www.ibtimes.com'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.item-link , .title , .clearfix,article ')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.ibtimes.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thehindubusinesslineSpider(scrapy.Spider):
    name = 'thehindubusinessline'
    allowed_domains = ['thehindubusinessline.com']
    start_urls = ['https://www.thehindubusinessline.com/']

    def parse(self, response):
        res = response.css('.News+ .dropdown-menu .nav-link')
        for r in res:
            category_link=r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('article')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#24.02.2022

class thesundailySpider(scrapy.Spider):
    name = 'thesundaily'
    allowed_domains = ['thesundaily.my']
    start_urls = ['https://www.thesundaily.my/']

    def parse(self, response):
        res = response.css('li.tabnav')
        for r in range(0,10):
            category_link='https://www.thesundaily.my'+res[r].css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.trc_excludable,div.headline')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.thesundaily.my'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thisdayliveSpider(scrapy.Spider):
    name = 'thisdaylive'
    allowed_domains = ['thisdaylive.com']
    start_urls = ['https://www.thisdaylive.com/']

    def parse(self, response):
        res = response.css('#menu-mr-solomon-arase-1 a')
        for r in range(0,9):
            category_link=res[r].css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.td-module-title,.td-block-span6,.td-animation-stack,.item-details')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class washingtonexaminerSpider(scrapy.Spider):
    name = 'washingtonexaminer'
    allowed_domains = ['washingtonexaminer.com']
    start_urls = ['https://www.washingtonexaminer.com/']

    def parse(self, response):
        res = response.css('li.NavigationItem-items-item')
        for r in range(0,8):
            category_link=res[r].css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.Link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class peopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['people.com']
    start_urls = ['https://people.com/']

    def parse(self, response):
        res = response.css('.open-channel-page:nth-child(1) .elementFont__subtitle--navigation')
        for r in res:
            category_link=r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.category-page-item-content,.category-page-videos__listItem,.carouselNav__listItem,.heading')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class businessliveSpider(scrapy.Spider):
    name = 'businesslive'
    allowed_domains = ['businesslive.co.za']
    start_urls = ['https://www.businesslive.co.za/']

    def parse(self, response):
        res = response.css('.section:nth-child(2) h3 a , .mobile-hide .col-12 h3')
        for r in res:
            category_link='https://www.businesslive.co.za'+r.css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.title , .article-title')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.businesslive.co.za/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class albawabaSpider(scrapy.Spider):
    name = 'albawaba'
    allowed_domains = ['albawaba.com']
    start_urls = ['https://www.albawaba.com/']

    def parse(self, response):
        res = response.css('#block-abn-main-menu li:nth-child(8) a , #block-abn-main-menu li:nth-child(7) a , #block-abn-main-menu li:nth-child(6) a , li:nth-child(5) a , #block-abn-main-menu li:nth-child(4) a , #block-abn-main-menu li:nth-child(3) a , #block-abn-main-menu .first+ li a , .is-active')
        for r in range(0,8):
            category_link='https://www.albawaba.com'+res[r].css('a').attrib['href']
            print('Result:',category_link)
            yield response.follow(category_link,callback=self.article_links)


    def article_links(self,response):
        data=response.css('.field--name-node-title, .press_release')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.albawaba.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#02.03.2022

class InewsSpider(scrapy.Spider):
    name = 'inews'
    allowed_domains = ['inews.co.uk']
    start_urls = ['http://inews.co.uk/']

    def parse(self, response):
        res = response.css('.inews-menu-item-has-children:nth-child(1) a')
        for r in res:
            category_link = r.css('a').attrib['href']
            print('Result:', category_link)
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.inews__post-puff__content-headline a , .inews__post-teaser__content__headline a , .inews__post-jot__content-headline a , .inews__post-hero__headline')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class lawSpider(scrapy.Spider):
    name = 'law'
    allowed_domains = ['law.com']
    start_urls = ['https://www.law.com/topics/']

    def parse(self, response):
        res = response.css('.dl-astyle')
        for r in res:
            category_link = 'https://www.law.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('#trending a , .my-3 a , .brief')
        for link in data:
            try:
                yield {
                    "News_links": 'https://www.law.com'+link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }

class cityamSpider(scrapy.Spider):
    name = 'cityam'
    allowed_domains = ['cityam.com']
    start_urls = ['https://www.cityam.com/']

    def parse(self, response):
        res = response.css('li.menu-item-type-taxonomy')
        for r in res:
            category_link =r.css('a::attr(href)').get()
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('li.content-listing__content-item')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }
#cityamSpider dont work
class cityamSpider(scrapy.Spider):
    name = 'investorplace'
    allowed_domains = ['investorplace.com']
    start_urls = ['https://investorplace.com/']

    def parse(self, response):
        res = response.css('#primary-menu a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.headline-c , .ipm_content_type-article')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }

class theedgemarketsSpider(scrapy.Spider):
    name = 'theedgemarkets'
    allowed_domains = ['theedgemarkets.com']
    start_urls = ['https://www.theedgemarkets.com/']

    def parse(self, response):
        res = response.css('#tb-megamenu-column-1 .mega')
        for r in res:
            category_link ='https://www.theedgemarkets.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.post-title, views-field')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.theedgemarkets.com'+link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }

class insidermonkeySpider(scrapy.Spider):
    name = 'insidermonkey'
    allowed_domains = ['insidermonkey.com']
    start_urls = ['https://www.insidermonkey.com/']

    def parse(self, response):
        res = response.css('.dropdown:nth-child(5) .dropdown-toggle , .dropdown:nth-child(4) .dropdown-toggle , .dropdown:nth-child(3) .dropdown-toggle , .dropdown:nth-child(2) .dropdown-toggle , .dropdown:nth-child(1) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.tracked-link , .title , .post-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#05.03.2022
class digitaltrendsSpider(scrapy.Spider):
    name = 'digitaltrends'
    allowed_domains = ['digitaltrends.com']
    start_urls = ['https://www.digitaltrends.com/']

    def parse(self, response):
        res = response.css('li.b-nav__item-2')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.b-snippet__hot, .b-meta__title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#
class cointelegraphSpider(scrapy.Spider):
    name = 'cointelegraph'
    allowed_domains = ['cointelegraph.com']
    start_urls = ['https://cointelegraph.com/']

    def parse(self, response):
        res = response.css('li.menu-desktop-sub__item')
        for r in res:
            category_link ='https://cointelegraph.com/'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.editors-choice-widget__item , .post-card-inline__title-link')
        for link in data:
            try:
                yield {
                    "News_links":'https://cointelegraph.com/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class techstorySpider(scrapy.Spider):
    name = 'techstory'
    allowed_domains = ['techstory.in']
    start_urls = ['https://techstory.in/']

    def parse(self, response):
        res = response.css('#cb-nav-bar a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.cb-post-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class tomsguideSpider(scrapy.Spider):
    name = 'tomsguide'
    allowed_domains = ['tomsguide.com']
    start_urls = ['https://www.tomsguide.com/']

    def parse(self, response):
        res = response.css('.menu-level-1 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.listingResult, .popular-box__article-list__heading')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thewrapSpider(scrapy.Spider):
    name = 'thewrap'
    allowed_domains = ['thewrap.com']
    start_urls = ['https://www.thewrap.com/']

    def parse(self, response):
        res = response.css('#primary-menu > .menu-item a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.title, .heading-sm')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class digitaljournalSpider(scrapy.Spider):
    name = 'digitaljournal'
    allowed_domains = ['digitaljournal.com']
    start_urls = ['https://www.digitaljournal.com/']

    def parse(self, response):
        res = response.css('#menu-main-menu-1 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.zox-art-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class wallstSpider(scrapy.Spider):
    name = '247wallst'
    allowed_domains = ['247wallst.com']
    start_urls = ['https://247wallst.com/']

    def parse(self, response):
        res = response.css('#wallst-nav-menu > .navbar-start .is-mega~ .is-mega+ .is-mega .navbar-link , #wallst-nav-menu > .navbar-start .is-mega:nth-child(1) .navbar-link')
        for r in res:
            category_link =r.attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.media-content')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class charlotteobserverSpider(scrapy.Spider):
    name = 'charlotteobserver'
    allowed_domains = ['charlotteobserver.com']
    start_urls = ['https://www.charlotteobserver.com/']

    def parse(self, response):
        res = response.css('#flag .caps')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.package')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#13.03.2022

class econotimesSpider(scrapy.Spider):
    name = 'econotimes'
    allowed_domains = ['econotimes.com']
    start_urls = ['http://econotimes.com/']

    def parse(self, response):
        res = response.css('.subNav a')
        for r in res:
            category_link ='http://econotimes.com/'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.mostPopularList p , #archivePage .title')
        for link in data:
            try:
                yield {
                    "News_links":'http://econotimes.com/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class venturebeatSpider(scrapy.Spider):
    name = 'venturebeat'
    allowed_domains = ['venturebeat.com']
    start_urls = ['https://venturebeat.com/']

    def parse(self, response):
        res = response.css('.Nav__section--active li a')
        for r in res:
            category_link ='https://venturebeat.com/'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.ArticleListing__title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class finextraSpider(scrapy.Spider):
    name = 'finextra'
    allowed_domains = ['finextra.com']
    start_urls = ['https://www.finextra.com/']

    def parse(self, response):
        res = response.css('.nav--toplevel-item:nth-child(1) .nav--link')
        for r in res:
            category_link ='https://www.finextra.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('#premierSectionChild h4 a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.finextra.com/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ftSpider(scrapy.Spider):
    name = 'ft'
    allowed_domains = ['ft.com']
    start_urls = ['https://www.ft.com/']

    def parse(self, response):
        res = response.css('#o-header-link-9 , #o-header-link-8 , #o-header-link-7 , #o-header-link-6 , #o-header-link-5 , #o-header-link-2 , #o-header-link-3 , #o-header-link-4 , .o-header__mega-column--subsections .o-header__mega-link , #o-header-link-0 , #o-header-link-1')
        for r in res:
            category_link ='https://www.ft.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.o-teaser__heading')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.ft.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class androidheadlinesSpider(scrapy.Spider):
    name = 'androidheadlines'
    allowed_domains = ['androidheadlines.com']
    start_urls = ['https://www.androidheadlines.com/']

    def parse(self, response):
        res = response.css('#slideout-menu .menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.post-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a::attr(href)').get()
                }
            except:
                yield {
                    "News_links": None
                }

class timeSpider(scrapy.Spider):
    name = 'time'
    allowed_domains = ['time.com']
    start_urls = ['https://time.com/']

    def parse(self, response):
        res = response.css('.menu-section a')
        for r in range(0,15):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('div.taxonomy-tout')
        for link in data:
            try:
                yield {
                    "News_links":'https://time.com/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class neowinSpider(scrapy.Spider):
    name = 'neowin'
    allowed_domains = ['neowin.net']
    start_urls = ['https://www.neowin.net/']

    def parse(self, response):
        res = response.css('#news-nav a')
        for r in res:
            category_link ='https://www.neowin.net/'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.trending-item , .news-item-title')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.neowin.net'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class finsmesSpider(scrapy.Spider):
    name = 'finsmes'
    allowed_domains = ['finsmes.com']
    start_urls = ['https://www.finsmes.com/']

    def parse(self, response):
        res = response.css('#menu-categories a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.entry-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class itwebSpider(scrapy.Spider):
    name = 'itweb'
    allowed_domains = ['itweb.co.za']
    start_urls = ['https://www.itweb.co.za/']

    def parse(self, response):
        res = response.css('div.v-list-group__items')
        for r in range(0,11):
            category_link ='https://www.itweb.co.za'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.mb-5')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.itweb.co.za'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#itwebSpider can't find article link

class steelguruSpider(scrapy.Spider):
    name = 'steelguru'
    allowed_domains = ['steelguru.com']
    start_urls = ['https://www.steelguru.com/']

    def parse(self, response):
        res = response.css('.menu-m__menu-item__Zj0zc:nth-child(9) a , .menu-m__menu-item__Zj0zc:nth-child(8) a , .menu-m__menu-item__Zj0zc:nth-child(7) a , .menu-m__menu-item__Zj0zc:nth-child(6) a , .menu-m__menu-item__Zj0zc:nth-child(5) a , .menu-m__menu-item__Zj0zc:nth-child(4) a , .menu-m__menu-item__Zj0zc:nth-child(3) a , .menu-m__menu-item__Zj0zc:nth-child(2) a , .menu-m__menu-item__Zj0zc:nth-child(1) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.mb-5')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.itweb.co.za'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#steelguruSpider can't find news link

class energyvoiceSpider(scrapy.Spider):
    name = 'energyvoice'
    allowed_domains = ['energyvoice.com']
    start_urls = ['https://www.energyvoice.com/']

    def parse(self, response):
        res = response.css('.menu-item-343009 a , .menu-item-205697 a , .menu-item-195967 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('#sidebar a , .title--sm a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#15.03.2022
class indiantelevisionSpider(scrapy.Spider):
    name = 'indiantelevision'
    allowed_domains = ['indiantelevision.com']
    start_urls = ['https://indiantelevision.com/']

    def parse(self, response):
        res = response.css('.expanded:nth-child(10) a , .expanded:nth-child(9) a , .expanded:nth-child(8) a , .expanded:nth-child(7) a , .expanded:nth-child(6) a , .expanded:nth-child(5) a , .expanded:nth-child(4) a , .expanded:nth-child(3) a , .first+ .expanded a , .first a')
        for r in res:
            category_link ='https://indiantelevision.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.col-sm-offset-0 a , .no-top a , .col-lg-5 a , .col-xs-6 h5 a')
        for link in data:
            try:
                yield {
                    "News_links":'https://indiantelevision.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coindeskSpider(scrapy.Spider):
    name = 'coindesk'
    allowed_domains = ['coindesk.com']
    start_urls = ['https://www.coindesk.com/']

    def parse(self, response):
        res = response.css('.fJiUlX:nth-child(4) a , .fJiUlX:nth-child(3) a , .fJiUlX:nth-child(2) a , .fJiUlX:nth-child(1) a')
        for r in res:
            category_link ='https://www.coindesk.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.headline')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.coindesk.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class financemagnatesSpider(scrapy.Spider):
    name = 'financemagnates'
    allowed_domains = ['financemagnates.com']
    start_urls = ['https://www.financemagnates.com/']

    def parse(self, response):
        res = response.css('.header-menu__parent-item:nth-child(1) .header-menu__submenu-text')
        for r in res:
            category_link ='https://www.financemagnates.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('.most-viewed__item-text , .news-item__title')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.financemagnates.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class advanced_televisionSpider(scrapy.Spider):
    name = 'advanced-television'
    allowed_domains = ['advanced-television.com']
    start_urls = ['https://advanced-television.com/']

    def parse(self, response):
        res = response.css('#submenu a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

    def article_links(self, response):
        data = response.css('#advancedrecentposts-3 a , .entry-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class adaderanaSpider(scrapy.Spider):
    name = 'adaderana'
    allowed_domains = ['adaderana.lk']
    start_urls = ['http://adaderana.lk/']

    def parse(self, response):
        res = response.css('.navbar-left li:nth-child(6) a , .navbar-left li:nth-child(5) a , .navbar-left li:nth-child(4) a , .navbar-left li:nth-child(2) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.wr-news-line a , .hidden-xs a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class whattheythinkSpider(scrapy.Spider):
    name = 'whattheythink'
    allowed_domains = ['whattheythink.com']
    start_urls = ['https://whattheythink.com/']

    def parse(self, response):
        res = response.css('.nav-textiles li:nth-child(1) a , .nav-home li:nth-child(1) a , .nav-finishing li:nth-child(1) a , .nav-software li:nth-child(1) a , .nav-packaging li:nth-child(1) a , .nav-wideformat li:nth-child(1) a , .nav-textiles+ .nav-industrial li:nth-child(1) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.news-list a, .px-0 a, #wideformat-news a, .mt-4 a')
        for link in data:
            try:
                yield {
                    "News_links":'https://whattheythink.com/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#17.03.2022
class fnarenaSpider(scrapy.Spider):
    name = 'fnarena'
    allowed_domains = ['fnarena.com']
    start_urls = ['https://www.fnarena.com/']

    def parse(self, response):
        res = response.css('#menu-item-80 a , .menu-item-esg-focus a , #menu-item-78 a , #menu-item-75 a , #menu-item-38 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.marbot-5 a , .s16 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class dailybusinessgroupSpider(scrapy.Spider):
    name = 'dailybusinessgroup'
    allowed_domains = ['dailybusinessgroup.co.uk']
    start_urls = ['https://dailybusinessgroup.co.uk/']

    def parse(self, response):
        res = response.css('.menu-item-580 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.subhnewssp')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class itproSpider(scrapy.Spider):
    name = 'itpro'
    allowed_domains = ['itpro.co.uk']
    start_urls = ['https://www.itpro.co.uk/']

    def parse(self, response):
        res1 = response.css('li.polaris__navigation--item')
        res = response.css('ul.-sub-menu-list').css('li')
        for r in range(0,8):
            category_link ='https://www.itpro.co.uk'+res1[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        for r in res:
            category_link ='https://www.itpro.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.polaris__article-card--link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.itpro.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class itnewsSpider(scrapy.Spider):
    name = 'itnews'
    allowed_domains = ['itnews.com.au']
    start_urls = ['https://www.itnews.com.au/']

    def parse(self, response):
        res = response.css('.mobile-nav-dropdown .mobile-nav-item')
        for r in range(0,15):
            category_link ='https://www.itnews.com.au'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.columns .collapse,.featured-article-body')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.itnews.com.au'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class techrepublicSpider(scrapy.Spider):
    name = 'techrepublic'
    allowed_domains = ['techrepublic.com']
    start_urls = ['https://www.techrepublic.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#primary .headline a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class globalcapitalSpider(scrapy.Spider):
    name = 'globalcapital'
    allowed_domains = ['globalcapital.com']
    start_urls = ['https://www.globalcapital.com/']

    def parse(self, response):
        res = response.css('li.NavigationItem-items-item')
        for r in range(0,11):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.PromoB-title .Link , .PromoA-title .Link , .PromoC-title .Link , .PromoLede-title .Link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class totalteleSpider(scrapy.Spider):
    name = 'totaltele'
    allowed_domains = ['totaltele.com']
    start_urls = ['https://www.totaltele.com/']

    def parse(self, response):
        res = response.css('#MainMenu li:nth-child(1) a , .has-child:nth-child(3) a , .has-child:nth-child(4) a , .has-child:nth-child(2) a')
        for r in range(0,15):
            category_link ='https://www.totaltele.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#HeaderListing h3')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.totaltele.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class onmsftSpider(scrapy.Spider):
    name = 'onmsft'
    allowed_domains = ['onmsft.com']
    start_urls = ['https://www.onmsft.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-post_tag a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class crnSpider(scrapy.Spider):
    name = 'crn'
    allowed_domains = ['crn.com']
    start_urls = ['https://www.crn.com/']

    def parse(self, response):
        res = response.css('#newsDrop a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.story-list p , #single-col-stories .border-bottom')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.crn.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class investmentnewsSpider(scrapy.Spider):
    name = 'investmentnews'
    allowed_domains = ['investmentnews.com']
    start_urls = ['https://www.investmentnews.com/']

    def parse(self, response):
        res = response.css('.menu-item-has-children:nth-child(1) .menu-item')
        for r in range(2,7):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('h3 a,h4 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class abladvisorSpider(scrapy.Spider):
    name = 'abladvisor'
    allowed_domains = ['abladvisor.com']
    start_urls = ['https://www.abladvisor.com/industry-news-latest']

    def parse(self, response):
        res = response.css('.newsMenu a')
        for r in res:
            category_link ='https://www.abladvisor.com/'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ipeSpider(scrapy.Spider):
    name = 'ipe'
    allowed_domains = ['ipe.com']
    start_urls = ['https://www.ipe.com/']

    def parse(self, response):
        res=response.css('.parentNav~ li a')
        for r in range(0,16):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        newslink='https://www.ipe.com/news'
        yield response.follow(newslink, callback=self.article_links())


    def article_links(self, response):
        data = response.css('.subSleeve a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#18.03.2022
class finewsSpider(scrapy.Spider):
    name = 'finews'
    allowed_domains = ['finews.com']
    start_urls = ['https://www.finews.com/news/english-news']

    def parse(self, response):
        res=response.css('.item-1070 a , .item-1474 a , .item-1071 a , .item-1069 a')
        for r in range(0,4):
            category_link ='https://www.finews.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.teaser-element, .topstory-container')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.finews.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class hackneygazetteSpider(scrapy.Spider):
    name = 'hackneygazette'
    allowed_domains = ['hackneygazette.co.uk']
    start_urls = ['https://www.hackneygazette.co.uk/']

    def parse(self, response):
        res=response.css('div.mdc-list__item-primary')
        for r in range(0,12):
            category_link ='https://www.hackneygazette.co.uk'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.mdc-card')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.hackneygazette.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class itnewsafricaSpider(scrapy.Spider):
    name = 'itnewsafrica'
    allowed_domains = ['itnewsafrica.com']
    start_urls = ['https://www.itnewsafrica.com/']

    def parse(self, response):
        res=response.css('.sub-menu a')
        for r in range(0,24):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ftadviserSpider(scrapy.Spider):
    name = 'ftadviser'
    allowed_domains = ['ftadviser.com']
    start_urls = ['https://www.ftadviser.com/']

    def parse(self, response):
        res = response.css('#Tax~ .children a , #Regulation~ .children a , #Protection~ .children a , #Mortgages~ .children a , #Investments~ .children a , #Pensions~ .children a')
        for r in res:
            category_link ='https://www.ftadviser.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('a.card__link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.ftadviser.com'+link.attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class globalbankingandfinanceSpider(scrapy.Spider):
    name = 'globalbankingandfinance'
    allowed_domains = ['globalbankingandfinance.com']
    start_urls = ['https://www.globalbankingandfinance.com/']

    def parse(self, response):
        res=response.css('.menu-item-262625 a , .menu-item-262628 a , .menu-item-262627 a , .menu-item-262626 a , .menu-item-262624 a , .menu-item-262623 a , .menu-item-262630 a , .menu-item-262622 a')
        for r in range(0,8):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('li.infinite-post,section.relative')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class diginomicaSpider(scrapy.Spider):
    name = 'diginomica'
    allowed_domains = ['diginomica.com']
    start_urls = ['https://diginomica.com/']

    def parse(self, response):
        res = response.css('.menu-item:nth-child(7) a , .menu-item--expanded:nth-child(4) a , .menu-item--expanded:nth-child(3) a , #block-mainnavigation .menu-item--expanded:nth-child(2) a , .menu-item--expanded:nth-child(1) a')
        for r in res:
            category_link ='https://diginomica.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry__title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://diginomica.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#22.03.2022
class channelwebSpider(scrapy.Spider):
    name = 'channelweb'
    allowed_domains = ['channelweb.co.uk']
    start_urls = ['https://www.channelweb.co.uk/']

    def parse(self, response):
        res = response.css('.active:nth-child(4) .nav-link , .arrowfixed+ .active .nav-link , .active:nth-child(1) .nav-link, .sub-part-nav a')
        for r in res:
            category_link ='https://www.channelweb.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.row div div div div div:nth-child(2) a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.channelweb.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class altfiSpider(scrapy.Spider):
    name = 'altfi'
    allowed_domains = ['altfi.com']
    start_urls = ['https://www.altfi.com/']

    def parse(self, response):
        res = response.css('.dropdown-item')
        for r in range(0,6):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.pane')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thetradenewsSpider(scrapy.Spider):
    name = 'thetradenews'
    allowed_domains = ['thetradenews.com']
    start_urls = ['https://www.thetradenews.com/']

    def parse(self, response):
        res = response.css('.menu-item-55312 a , .menu-item-55313 a , .menu-item-55316 a , .menu-item-55314 a , .menu-item-55311 a , .menu-item-55308 a , .menu-item-55310 a , .menu-item-55248 a , .menu-item-55309 a , .menu-item-55246')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.wpp-list h4 a , .list-item')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class industryleadersmagazineSpider(scrapy.Spider):
    name = 'industryleadersmagazine'
    allowed_domains = ['industryleadersmagazine.com']
    start_urls = ['https://www.industryleadersmagazine.com/']

    def parse(self, response):
        res = response.css('.menu-item-8248 a , .menu-item-8240 a , .menu-item-309 a')
        for r in range(0,26):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#ajax-posts .readmore')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class sdtimesSpider(scrapy.Spider):
    name = 'sdtimes'
    allowed_domains = ['sdtimes.com']
    start_urls = ['https://sdtimes.com/']

    def parse(self, response):
        res = response.css('#menu-topic-navigation-1 a')
        for r in res:
            category_link ='https://sdtimes.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.col-md-9')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class dqindiaSpider(scrapy.Spider):
    name = 'dqindia'
    allowed_domains = ['dqindia.com']
    start_urls = ['https://www.dqindia.com/']

    def parse(self, response):
        res = response.css('.mega-menu-item-69467 .mega-menu-link , .mega-menu-item-621 .mega-menu-link , .mega-menu-item-615 .mega-menu-link , .mega-menu-item-614 .mega-menu-link , .mega-menu-item-609 .mega-menu-link , .mega-menu-item-594 .mega-menu-link , .mega-menu-item-605 .mega-menu-link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.more-link a , .post-right')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class investorschronicleSpider(scrapy.Spider):
    name = 'investorschronicle'
    allowed_domains = ['investorschronicle.co.uk']
    start_urls = ['https://www.investorschronicle.co.uk/']

    def parse(self, response):
        res = response.css('.ic__footer--menu-vertical:nth-child(3) a , .ic__footer--menu-vertical:nth-child(2) a , .ic__footer--menu-vertical:nth-child(1) a')
        for r in res:
            category_link ='https://www.investorschronicle.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.specialist__card__article--link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#24.03.2022
class sharesmagazineSpider(scrapy.Spider):
    name = 'sharesmagazine'
    allowed_domains = ['sharesmagazine.co.uk']
    start_urls = ['https://www.sharesmagazine.co.uk/']

    def parse(self, response):
        res = response.css('.span_5_of_12 .secondaryNavLink')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#maincontent .brdr-under-sh5, td~ td+ td a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class channelfuturesSpider(scrapy.Spider):
    name = 'channelfutures'
    allowed_domains = ['channelfutures.com']
    start_urls = ['https://www.channelfutures.com/']

    def parse(self, response):
        res = response.css('#menu-item-208766 a , #menu-item-140809 a , #menu-item-123588 a , #menu-item-123563 a , .active+ .has-dropdown a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.cat-list-container')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class fierceelectronicsSpider(scrapy.Spider):
    name = 'fierceelectronics'
    allowed_domains = ['fierceelectronics.com']
    start_urls = ['https://www.fierceelectronics.com/']

    def parse(self, response):
        res = response.css('.header-link-group.col .nav-link')
        for r in range(0,5):
            category_link ='https://www.fierceelectronics.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.element-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#dont work article links
class legalitprofessionalsSpider(scrapy.Spider):
    name = 'legalitprofessionals'
    allowed_domains = ['legalitprofessionals.com']
    start_urls = ['https://www.legalitprofessionals.com/']

    def parse(self, response):
        res = response.css('.item7 a , .item39 a , .item155 a')
        for r in res:
            category_link ='https://www.legalitprofessionals.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.readmore-link, .readmore a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.legalitprofessionals.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class treasuryandriskSpider(scrapy.Spider):
    name = 'treasuryandrisk'
    allowed_domains = ['treasuryandrisk.com']
    start_urls = ['https://www.treasuryandrisk.com/']

    def parse(self, response):
        res = response.css('#li-dropdown-careers a , #li-dropdown-technology a , #li-dropdown-global-markets a , #li-dropdown-operational-risk a , #li-dropdown-financial-risk a , #li-dropdown-corporate-finance a , #li-dropdown-working-capital a , #li-dropdown-cash-management a')
        for r in res:
            category_link ='https://www.treasuryandrisk.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.treasuryandrisk.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class indiatimesSpider(scrapy.Spider):
    name = 'indiatimes'
    allowed_domains = ['indiatimes.com']
    start_urls = ['https://www.indiatimes.com/']

    def parse(self, response):
        res = response.css('li.dropdown,.menu-icon')
        for r in res:
            category_link ='https://www.indiatimes.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.mt-10 , .card-title')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.indiatimes.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class openprSpider(scrapy.Spider):
    name = 'openpr'
    allowed_domains = ['openpr.com']
    start_urls = ['https://www.openpr.com/news/categories']

    def parse(self, response):
        res = response.css('.category-title a')
        for r in res:
            category_link ='https://www.openpr.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.pm-box').css('h2')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.openpr.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#28.03.2022
class apnewsSpider(scrapy.Spider):
    name = 'apnews'
    allowed_domains = ['apnews.com']
    start_urls = ['https://apnews.com/']

    def parse(self, response):
        res = response.css('.header-navigation-item:nth-child(11) .topic-link , .header-navigation-item:nth-child(10) .topic-link , .header-navigation-item:nth-child(9) .topic-link , .header-navigation-item:nth-child(8) .topic-link , .header-navigation-item:nth-child(7) .topic-link , .header-navigation-item:nth-child(6) .topic-link , .header-navigation-item:nth-child(5) .topic-link , .header-navigation-item:nth-child(4) .topic-link , .header-navigation-item:nth-child(3) .topic-link , .header-navigation-item:nth-child(2) .topic-link , .header-navigation-item:nth-child(1) .topic-link')
        for r in res:
            category_link ='https://apnews.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.storyHeadlines-0-2-101 , .CardHeadline')
        for link in data:
            try:
                yield {
                    "News_links":'https://apnews.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class businesswireSpider(scrapy.Spider):
    name = 'businesswire'
    allowed_domains = ['businesswire.com']
    start_urls = ['https://www.businesswire.com/portal/site/home/']

    def parse(self, response):
        res = response.css('.bw-has-submenu:nth-child(3) li a')
        for r in res:
            category_link ='https://www.businesswire.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#headlines li')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.businesswire.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class menafnSpider(scrapy.Spider):
    name = 'menafn'
    allowed_domains = ['menafn.com']
    start_urls = ['https://menafn.com/']

    def parse(self, response):
        res = response.css('.has-child:nth-child(2) > .dropdown-inner li:nth-child(1) > a , .has-child:nth-child(2) li+ .has-child a')
        for r in range(0,8):
            category_link ='https://menafn.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class hindustantimesSpider(scrapy.Spider):
    name = 'hindustantimes'
    allowed_domains = ['hindustantimes.com']
    start_urls = ['https://www.hindustantimes.com/']

    def parse(self, response):
        res = response.css('.leftFixedNav li:nth-child(10) a , .leftFixedNav li:nth-child(9) a , .leftFixedNav li:nth-child(8) a , .leftFixedNav li:nth-child(7) a , .leftFixedNav li:nth-child(6) a , .leftFixedNav li:nth-child(5) a , .leftFixedNav li:nth-child(4) a , .leftFixedNav li:nth-child(3) a , .active+ li a , .active a')
        for r in range(0,10):
            category_link ='https://www.hindustantimes.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.hdg3 a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.hindustantimes.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class republicworldSpider(scrapy.Spider):
    name = 'republicworld'
    allowed_domains = ['republicworld.com']
    start_urls = ['https://www.republicworld.com/']

    def parse(self, response):
        res = response.css('div:nth-child(7) .ham-sub-title a , div:nth-child(6) .ham-sub-title a , #quick-links div:nth-child(5) .ham-sub-title a , div:nth-child(4) .ham-sub-title a , #quick-links div:nth-child(3) .ham-sub-title a , .ham-menu div:nth-child(2) .ham-sub-title a , .ham-menu div:nth-child(1) .ham-sub-title a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.hover-effect')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thehinduSpider(scrapy.Spider):
    name = 'thehindu'
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/']

    def parse(self, response):
        res = response.css('.main-menu #main-menu a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.story1-3x100-heading , h3 a , .story-card-news h2 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class business_standardSpider(scrapy.Spider):
    name = 'business-standard'
    allowed_domains = ['business-standard.com']
    start_urls = ['https://www.business-standard.com/']

    def parse(self, response):
        res=response.css('#horiz-menu a')
        for r in res:
            category_link ='https://www.business-standard.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#nifty-tab3 a , .listing-txt h2 a,.aticle-list h2,.aticle-txt h2 a , .top-section h2 , .webexclu1 , .webexclu0,.size16 span , #bs-new-top-story-listing-ajax-block a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.business-standard.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#31.03.2022
class benzingaSpider(scrapy.Spider):
    name = 'benzinga'
    allowed_domains = ['benzinga.com']
    start_urls = ['https://www.benzinga.com/']

    def parse(self, response):
        res=response.css('li:nth-child(2) .fNjuVS a , li:nth-child(4) .bAvjQq div:nth-child(1) .menu-items a , li:nth-child(1) .fNjuVS a , li:nth-child(3) .fNjuVS a , li:nth-child(5) .initial , li:nth-child(4) .initial , li:nth-child(3) .initial , li:nth-child(2) .initial , .sub-group-wrapper > .menu-items .fNjuVS:nth-child(1) a , li:nth-child(1) .initial')
        for r in res:
            category_link ='https://www.benzinga.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.bz3-post-card, a.newsfeed-card,a.bz3-featured-article-link, .read-more a')
        for link in data:
            try:
                yield {
                    "News_links": link.attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class indianexpressSpider(scrapy.Spider):
    name = 'indianexpress'
    allowed_domains = ['indianexpress.com']
    start_urls = ['https://indianexpress.com/']

    def parse(self, response):
        res=response.css('#navbar li:nth-child(12) a , #navbar li:nth-child(10) a , #navbar li:nth-child(9) a , #navbar li:nth-child(8) a , #navbar li:nth-child(7) a , #navbar li:nth-child(6) a , #navbar li:nth-child(5) a , #navbar li:nth-child(4) a , .active-el+ li a , .active-el a , #navbar li:nth-child(1) a')
        for r in res:
            category_link ='https://indianexpress.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#IE_RHS_Best_of_Express , #IE_RHS_Latest_News , .second-story a , .title a')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class usinessinsiderSpider(scrapy.Spider):
    name = 'usinessinsider'
    allowed_domains = ['businessinsider.com']
    start_urls = ['https://www.businessinsider.com/']

    def parse(self, response):
        res=response.css('.subnav-link')
        for r in res:
            category_link ='https://www.businessinsider.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.tout-title-link')
        for link in data:
            try:
                yield {
                    "News_links": 'https://www.businessinsider.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#new age 07.04.2022
class brecorderSpider(scrapy.Spider):
    name = 'brecorder'
    allowed_domains = ['brecorder.com']
    start_urls = ['https://www.brecorder.com/']

    def parse(self, response):
        res=response.css('.ml-0')
        for r in res:
            category_link ='https://www.brecorder.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.story__link')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class mbSpider(scrapy.Spider):
    name = 'mb'
    allowed_domains = ['mb.com']
    start_urls = ['https://mb.com.ph/']

    def parse(self, response):
        res=response.css('li.menu-item')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('li.article')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class financialitSpider(scrapy.Spider):
    name = 'financialit'
    allowed_domains = ['financialit.net']
    start_urls = ['https://financialit.net/']

    def parse(self, response):
        res=response.css('.dropdown:nth-child(3) .waves-light')
        for r in res:
            category_link ='https://financialit.net'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.post-info-2 .title')
        for link in data:
            try:
                yield {
                    "News_links":'https://financialit.net'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class tradersmagazineSpider(scrapy.Spider):
    name = 'tradersmagazine'
    allowed_domains = ['tradersmagazine.com']
    start_urls = ['https://www.tradersmagazine.com/']

    def parse(self, response):
        res=response.css('.block-mega-child-cats , .menu-item-30081 a , .mega-menu-sub-cat-td_uid_1_6266f366b8220+ .mega-menu-sub-cat-td_uid_1_6266f366b8220 , .cur-sub-cat+ .mega-menu-sub-cat-td_uid_1_6266f366b8220')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#13.04.2022
class nzheraldSpider(scrapy.Spider):
    name = 'nzherald'
    allowed_domains = ['nzherald.co.nz']
    start_urls = ['https://www.nzherald.co.nz/']

    def parse(self, response):
        res=response.css('.navigation__item-link-color')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.story-card__heading__link')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bloombergquintSpider(scrapy.Spider):
    name = 'bloombergquint'
    allowed_domains = ['bloombergquint.com']
    start_urls = ['https://www.bloombergquint.com/']

    def parse(self, response):
        res=response.css('.menu-item-m__menu-item__2xi2Z')
        for r in res:
            category_link ='https://www.bloombergquint.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.sub-story-list__link,.cardHeadlineAuthorVertical-m__wrapper__esCCA,.card-with-time card-with-time-m__wrapper__3dNaB,.headline-wrapper,.stories-seven-two-row-m__story__22vMl')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.bloombergquint.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thetimesSpider(scrapy.Spider):
    name = 'thetimes'
    allowed_domains = ['thetimes.co.uk']
    start_urls = ['https://www.thetimes.co.uk/']

    def parse(self, response):
        res=response.css('.js-channelsDropdownToggle font , .is-active font , #todays-sections-menu-desktop .js-tracking')
        for r in res:
            category_link ='https://www.thetimes.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#section-register .Headline--s .js-tracking , #section-times2 .Headline--s .js-tracking , #section-sport .Headline--s .js-tracking , .Headline--m .js-tracking , #section-news .Headline--s .js-tracking')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.thetimes.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bnnbloombergSpider(scrapy.Spider):
    name = 'bnnbloomberg'
    allowed_domains = ['bnnbloomberg.ca']
    start_urls = ['https://www.bnnbloomberg.ca/']

    def parse(self, response):
        res=response.css('.sports-nav-dropdown li > a')
        for r in res:
            category_link ='https://www.bnnbloomberg.ca'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-content')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.bnnbloomberg.ca'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class independentSpider(scrapy.Spider):
    name = 'independent'
    allowed_domains = ['independent.ie']
    start_urls = ['https://www.independent.ie/']

    def parse(self, response):
        res=response.css('.-c\:opinion a , .-c\:travel a , .-c\:entertainment a , .-c\:style a , .-c\:life a , .-c\:sport a , .-c\:business a , .-c\:news a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.-as\:1')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class foxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    start_urls = ['https://www.foxnews.com/']

    def parse(self, response):
        res=response.css('.menu-nation a , .menu-fox-weather a , .menu-lifestyle a , .menu-sports a , .menu-entertainment a , .menu-business a , .menu-opinion a , .menu-media a , .menu-politics a , .menu-news a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-list, .title a,.main-content')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.foxnews.com'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#16.04.2022
class timesnownewsSpider(scrapy.Spider):
    name = 'timesnownews'
    allowed_domains = ['timesnownews.com']
    start_urls = ['https://www.timesnownews.com/']

    def parse(self, response):
        res=response.css('ul.undefined').css('li')
        for r in res:
            category_link ='https://www.timesnownews.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.ArticleList-tnn__h-list-1W5s9, .Story-tnn__h-list-2LXp3')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.timesnownews.com'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class zawyaSpider(scrapy.Spider):
    name = 'zawya'
    allowed_domains = ['zawya.com']
    start_urls = ['https://www.zawya.com/en/mena']

    def parse(self, response):
        res=response.css('.inline-navigation-list a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.teaser-title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.zawya.com'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class theguardianSpider(scrapy.Spider):
    name = 'theguardian'
    allowed_domains = ['theguardian.com']
    start_urls = ['https://www.theguardian.com/']

    def parse(self, response):
        res=response.css('#bannerandheader .pillars__item .pillar-link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.fc-item__content')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class indiatodaySpider(scrapy.Spider):
    name = 'indiatoday'
    allowed_domains = ['indiatoday.in']
    start_urls = ['https://www.indiatoday.in/']

    def parse(self, response):
        res=response.css('.second-level-child-0 , .url-type-internal')
        for r in res:
            category_link ='https://www.indiatoday.in'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.detail,#itg-block-14 a , #itg-block-13 a , .story a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.zawya.com'+ link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class marketwatchSpider(scrapy.Spider):
    name = 'marketwatch'
    allowed_domains = ['marketwatch.com']
    start_urls = ['https://www.marketwatch.com/']

    def parse(self, response):
        res=response.css('#nav__menu a')
        for r in range(0,7):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article__headline a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class freepressjournalSpider(scrapy.Spider):
    name = 'freepressjournal'
    allowed_domains = ['freepressjournal.in']
    start_urls = ['https://www.freepressjournal.in/']

    def parse(self, response):
        res=response.css('.fpj_nav a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#storyList').css('li')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#21.04.2022
class thestarSpider(scrapy.Spider):
    name = 'thestar'
    allowed_domains = ['thestar.com.my']
    start_urls = ['https://www.thestar.com.my/']

    def parse(self, response):
        res=response.css('.mega-nav__col:nth-child(4) a , .mega-nav__col:nth-child(3) a , .mega-nav__col:nth-child(2) a , .mega-nav__inner:nth-child(3) .mega-nav__list a , .mega-nav__col:nth-child(1) .mega-nav__title')
        for r in res:
            category_link ='https://www.thestar.com.my'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.f18 a,.thumb__title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ndtvSpider(scrapy.Spider):
    name = 'ndtv'
    allowed_domains = ['ndtv.com']
    start_urls = ['https://www.ndtv.com/']

    def parse(self, response):
        res=response.css('#subnav a:nth-child(8) , #subnav a:nth-child(6) , a a:nth-child(3) , #subnav a:nth-child(1) , #header2 a:nth-child(10) , #header2 a:nth-child(9) , #header2 a:nth-child(8) , #header2 a:nth-child(7) , .topnav_cont a:nth-child(5) , #header2 .topnav_cont a:nth-child(4) , .topnav_cont a:nth-child(3) , .topnav_cont a:nth-child(2)')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.newsHdng a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class miragenewsSpider(scrapy.Spider):
    name = 'miragenews'
    allowed_domains = ['miragenews.com']
    start_urls = ['https://www.miragenews.com/']

    def parse(self, response):
        res=response.css('.menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.ul-sec a , .post-right a, #wtab1-content a , #tab1-content a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class consultancySpider(scrapy.Spider):
    name = 'consultancy'
    allowed_domains = ['consultancy.uk']
    start_urls = ['https://www.consultancy.uk/']

    def parse(self, response):
        res=response.css('#newsMenuItem a')
        for r in res:
            category_link ='https://www.consultancy.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.news-item-info')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.consultancy.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cioreviewSpider(scrapy.Spider):
    name = 'cioreview'
    allowed_domains = ['cioreview.com']
    start_urls = ['https://www.cioreview.com/news/']

    def parse(self, response):

        res=response.css('#newsmag_widget_posts_column-1 a')
        for r in res:
            category_link ='https://www.consultancy.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.news-item-info')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.consultancy.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#don't work^

#25.04.2022

class govconwireSpider(scrapy.Spider):
    name = 'govconwire'
    allowed_domains = ['govconwire.com']
    start_urls = ['https://www.govconwire.com/']

    def parse(self, response):
        res=response.css('.menu-item-86358 .nav-link , .menu-item-73081 .nav-link , .menu-item-239881 .nav-link , .menu-item-286018 .nav-link , .menu-item-192393 .nav-link , .menu-item-51156 .nav-link , .menu-item-51154 .nav-link , .menu-item-51153 .nav-link , .menu-item-73080 .nav-link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.post-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class wealthbriefingSpider(scrapy.Spider):
    name = 'wealthbriefing'
    allowed_domains = ['wealthbriefing.com']
    start_urls = ['https://wealthbriefing.com/html/index.php']

    def parse(self, response):
        res=response.css('#catnav a , #contactnav+ .gen a')
        for r in res:
            category_link ='https://wealthbriefing.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-wrapper').css('a')
        for link in data:
            try:
                yield {
                    "News_links":'https://wealthbriefing.com/html/'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ceiSpider(scrapy.Spider):
    name = 'cei'
    allowed_domains = ['cei.org']
    start_urls = ['https://cei.org/issue-areas/']

    def parse(self, response):
        res=response.css('#site-main .menu-link , .submenu-link , .tertiary-link , .link-item:nth-child(4) .footer-link')

        for r in res:
            category_link = 'https://cei.org' + r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.card-link')
        for link in data:
            try:
                yield {
                    "News_links": link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class infoqSpider(scrapy.Spider):
    name = 'infoq'
    allowed_domains = ['infoq.com']
    start_urls = ['https://www.infoq.com/']

    def parse(self, response):
        res=response.css('.section__heading a')
        for r in res:
            category_link ='https://www.infoq.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.card__title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.infoq.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class resellerSpider(scrapy.Spider):
    name = 'reseller'
    allowed_domains = ['reseller.co.nz']
    start_urls = ['https://www.reseller.co.nz/']

    def parse(self, response):
        res=response.css('.super:nth-child(3) a , .search+ li a')
        for r in res:
            category_link ='https://www.reseller.co.nz'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.lo-article_title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.reseller.co.nz'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class euromoneySpider(scrapy.Spider):
    name = 'euromoney'
    allowed_domains = ['euromoney.com']
    start_urls = ['https://www.euromoney.com/']

    def parse(self, response):
        res=response.css('li.NavigationItem-items-item')
        for r in range(7,22):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.PromoB-title .Link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#26.04.2022

class hlSpider(scrapy.Spider):
    name = 'hl'
    allowed_domains = ['hl.co.uk']
    start_urls = ['https://www.hl.co.uk/']

    def parse(self, response):
        res=response.css('#nav16516,#nav16522')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.spacer-none.large-text-increase-0 , .text-increase-0.spacer-none, .newsCard__anchor')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thinkadvisorSpider(scrapy.Spider):
    name = 'thinkadvisor'
    allowed_domains = ['thinkadvisor.com']
    start_urls = ['https://www.thinkadvisor.com/']

    def parse(self, response):
        res=response.css('#secondary-sidenav a')
        for r in res:
            category_link ='https://www.thinkadvisor.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.art-heading, .card-text a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class businesswireindiaSpider(scrapy.Spider):
    name = 'businesswireindia'
    allowed_domains = ['businesswireindia.com']
    start_urls = ['https://www.businesswireindia.com/']

    def parse(self, response):
        res=response.css('.text-right a')
        for r in res:
            category_link ='https://www.businesswireindia.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('span a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class insidermediaSpider(scrapy.Spider):
    name = 'insidermedia'
    allowed_domains = ['insidermedia.com']
    start_urls = ['https://www.insidermedia.com/']

    def parse(self, response):
        res=response.css('li:nth-child(1) .dropdown , .online .dts-4.level2 h3 , .online .dts-4 li')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.featured_item--sml h4 , .recent_item_title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#not responding to commands
class arnnetSpider(scrapy.Spider):
    name = 'arnnet'
    allowed_domains = ['arnnet.com.au']
    start_urls = ['https://www.arnnet.com.au/']

    def parse(self, response):
        res=response.css('.super:nth-child(3) a , .search+ li a')
        for r in res:
            category_link ='https://www.arnnet.com.au'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.spacer-none.large-text-increase-0 , .text-increase-0.spacer-none, .newsCard__anchor')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.arnnet.com.au'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#redirecting 301

#27.04.2022
class siliconindiaSpider(scrapy.Spider):
    name = 'siliconindia'
    allowed_domains = ['siliconindia.com']
    start_urls = ['https://www.siliconindia.com/']

    def parse(self, response):
        res=response.css('.orange-border')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.indi-col a , .small-post a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class crnSpider(scrapy.Spider):
    name = 'crn'
    allowed_domains = ['crn.com.au']
    start_urls = ['https://www.crn.com.au/']

    def parse(self, response):
        res=response.css('#site-logo , #sticky-nav .has-dropdown:nth-child(1) a')
        for r in res:
            category_link ='https://www.crn.com.au'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-list-content,#most-read-container a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.crn.com.au'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class siliconindiaSpider(scrapy.Spider):
    name = 'emarketer'
    allowed_domains = ['emarketer.com']
    start_urls = ['https://www.emarketer.com/']

    def parse(self, response):
        res=response.css('.sc-htpNat')
        for r in res:
            try:
                yield {
                    "News_links": r.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class electronicsweeklySpider(scrapy.Spider):
    name = 'electronicsweekly'
    allowed_domains = ['electronicsweekly.com']
    start_urls = ['https://www.electronicsweekly.com/']

    def parse(self, response):
        res=response.css('#menu-item-445149 a , #menu-item-445141 a , #menu-item-445193 a , .menu-item-object-custom+ .menu-item-object-category a , .current_page_item+ .menu-item-object-custom a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.post-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class financialstandardSpider(scrapy.Spider):
    name = 'financialstandard'
    allowed_domains = ['financialstandard.com.au']
    start_urls = ['https://www.financialstandard.com.au/']

    def parse(self, response):
        res=response.css('#site-logo , #sticky-nav .has-dropdown:nth-child(1) a')
        for r in res:
            category_link ='https://www.financialstandard.com.au'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.news_heading td , .featured_news_module_news_headline')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#work in shell but not in All

class wealthmanagementSpider(scrapy.Spider):
    name = 'wealthmanagement'
    allowed_domains = ['wealthmanagement.com']
    start_urls = ['https://www.wealthmanagement.com/']

    def parse(self, response):
        res=response.css('.hamburger-menu-nav__item:nth-child(9) a , .hamburger-menu-nav__item:nth-child(8) a , .hamburger-menu-nav__item:nth-child(7) a , .hamburger-menu-nav__item:nth-child(6) a , .hamburger-menu-nav__item:nth-child(5) a , .hamburger-menu-nav__item:nth-child(4) a , .hamburger-menu-nav__item:nth-child(3) a , .hamburger-menu-nav__item:nth-child(2) a , .hamburger-menu-nav__item:nth-child(1) a')
        for r in res:
            category_link ='https://www.wealthmanagement.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.wealthmanagement.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#28.04.2022
class cityindexSpider(scrapy.Spider):
    name = 'cityindex'
    allowed_domains = ['cityindex.co.uk']
    start_urls = ['https://www.cityindex.co.uk/']

    def parse(self, response):
        res=response.css('.primary-nav__item:nth-child(6) a')
        for r in res:
            category_link ='https://www.cityindex.co.uk'+r.css('a').attrib['href']
            print(category_link)
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.research-card__title-link, .hero__media-col a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.wealthmanagement.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class sharecafeSpider(scrapy.Spider):
    name = 'sharecafe'
    allowed_domains = ['sharecafe.com.au']
    start_urls = ['https://www.sharecafe.com.au/']

    def parse(self, response):
        res=response.css('.menu-item-3797 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#posts-lists a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class financialbuzzSpider(scrapy.Spider):
    name = 'financialbuzz'
    allowed_domains = ['financialbuzz.com']
    start_urls = ['https://www.financialbuzz.com/']

    def parse(self, response):
        res=response.css('.menu-item-1439984 a , .menu-item-1750 a , .menu-item-1751 a , .menu-item-1749 a , .menu-item-1752 a , .menu-item-1746 a , .menu-item-1745 a , .menu-item-1741 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class pionlineSpider(scrapy.Spider):
    name = 'pionline'
    allowed_domains = ['pionline.com']
    start_urls = ['https://www.pionline.com/']

    def parse(self, response):
        res=response.css('.open+ .open .openlink , .menu-item:nth-child(1) .omnitrack-hover')
        for r in res:
            category_link ='https://www.pionline.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.middle-article-headline a, .feature-article-headline .omnitrack, .feature-article-headline .omnitrack')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.crn.com.au'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class americanbankerSpider(scrapy.Spider):
    name = 'americanbanker'
    allowed_domains = ['americanbanker.com']
    start_urls = ['https://www.americanbanker.com/']

    def parse(self, response):
        res=response.css('li.DropdownNavigationItem-items-item')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.PromoMediumImageRight-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class reinsuranceneSpider(scrapy.Spider):
    name = 'reinsurancene'
    allowed_domains = ['reinsurancene.ws']
    start_urls = ['https://www.reinsurancene.ws/']

    def parse(self, response):
        res=response.css('.menu-item-object-category+ .menu-item-object-page .nav-link , .menu-item-object-category .nav-link , .has-mega-menu .nav-link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.read-post, .pl-0')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#29.04.2022
class computerweeklySpider(scrapy.Spider):
    name = 'computerweekly'
    allowed_domains = ['computerweekly.com']
    start_urls = ['https://www.computerweekly.com/']

    def parse(self, response):
        res=response.css('#nav-links-Opinion a , #nav-links-Blogs a , #nav-links-InDepth a , #nav-links-News a, li.nav-list-sublist-item')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.infotype-news-title a, h4 a, h3 a,.new-notable-item a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class investmentweekSpider(scrapy.Spider):
    name = 'investmentweek'
    allowed_domains = ['investmentweek.co.uk']
    start_urls = ['https://www.investmentweek.co.uk/']

    def parse(self, response):
        res=response.css('.sub-menu a')
        res2=response.css('.active:nth-child(1) .nav-link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in res2:
            category_link ='https://www.investmentweek.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.infotype-news-title a, h4 a, h3 a,.new-notable-item a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.investmentweek.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class mybigplungeSpider(scrapy.Spider):
    name = 'mybigplunge'
    allowed_domains = ['mybigplunge.com']
    start_urls = ['https://mybigplunge.com/']

    def parse(self, response):
        res=response.css('.menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('div.mvp-main-blog-text, div.mvp-feat2-sub-text, div.mvp-100img-in')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class steelguruSpider(scrapy.Spider):
    name = 'steelguru'
    allowed_domains = ['steelguru.com']
    start_urls = ['https://www.steelguru.com/']

    def parse(self, response):
        res=response.css('#header-default-menu a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.headline-m_dark__en3hW')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#article links res=[]

class appleinsiderSpider(scrapy.Spider):
    name = 'appleinsider'
    allowed_domains = ['appleinsider.com']
    start_urls = ['https://appleinsider.com/']

    def parse(self, response):
        res=response.css('.inl:nth-child(3) a , .inl:nth-child(2) a , .inl:nth-child(1) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.blueHover a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class sharecastSpider(scrapy.Spider):
    name = 'sharecast'
    allowed_domains = ['sharecast.com']
    start_urls = ['https://www.sharecast.com/']

    def parse(self, response):
        res=response.css('.open a , .grid-row-2 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.twi a, #RightAside li a , .dark-xs-news-box a , .caption a , .horizont-card a , .news-item__headline a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#02.05.2022
class sharecastSpider(scrapy.Spider):
    name = 'theverge'
    allowed_domains = ['theverge.com']
    start_urls = ['https://www.theverge.com/']

    def parse(self, response):
        res=response.css('.c-global-header__link:nth-child(4) a , .c-global-header__link:nth-child(2) a , .is-pinned a, .l-wrapper')
        hideres=response.css('.c-nav-list__sub-items').css('li')
        for r in res:
            category_link ='https://www.theverge.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(0,37):
            category_link ='https://www.theverge.com'+hideres[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.c-entry-box--compact__title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class entrepreneurSpider(scrapy.Spider):
    name = 'entrepreneur'
    allowed_domains = ['entrepreneur.com']
    start_urls = ['https://www.entrepreneur.com/']

    def parse(self, response):
        res=response.css('.collapsible-body').css('ul').css('li')
        for r in range(10,19):
            category_link ='https://www.entrepreneur.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.entrepreneur.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.flex-grow .block')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.entrepreneur.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class zdnetSpider(scrapy.Spider):
    name = 'zdnet'
    allowed_domains = ['zdnet.com']
    start_urls = ['https://www.zdnet.com/']

    def parse(self, response):
        res=response.css('.desktop-topic')
        secres=response.css('.secondary')
        for r in range(1,8):
            category_link ='https://www.zdnet.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(14,71):
            category_link =secres[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('#main .col-2 a , h3 a,.odd a , .even a  ')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.zdnet.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class morningstarSpider(scrapy.Spider):
    name = 'morningstar'
    allowed_domains = ['morningstar.com']
    start_urls = ['https://www.morningstar.com/']

    def parse(self, response):
        res=response.css('.mds-list-group__item:nth-child(7) .mds-list-group__link , .mds-list-group__item:nth-child(6) .mds-list-group__link , .mds-list-group__item:nth-child(5) .mds-list-group__link , .mds-list-group__item--sublist .mds-list-group__link , .mds-list-group__item:nth-child(4) .mds-list-group__link')
        for r in range(0,16):
            category_link ='https://www.morningstar.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.morningstar.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.mdc-card__title--clamp , .mdc-grid-item__title--link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.morningstar.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class engadgetSpider(scrapy.Spider):
    name = 'engadget'
    allowed_domains = ['engadget.com']
    start_urls = ['https://www.engadget.com/']

    def parse(self, response):
        res=response.css('li.nav-menu')
        subres=response.css('li.menu-item')
        for r in range(0,8):
            category_link ='https://www.engadget.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(0,65):
            category_link ='https://www.engadget.com'+subres[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.flex-grow .block')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.entrepreneur.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#dont work

#03.05.2022
class nbcnewsSpider(scrapy.Spider):
    name = 'nbcnews'
    allowed_domains = ['nbcnews.com']
    start_urls = ['https://www.nbcnews.com/']

    def parse(self, response):
        res=response.css('.menu-section-main .menu-list-item')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.nbcnews.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.dt-m, .tease-card__title--news,.f5-m , .f8-m , .f6-m a , .styles_headline__ice3t , .styles_teaseTitle__H4OWQ')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class insiderSpider(scrapy.Spider):
    name = 'insider'
    allowed_domains = ['insider.com']
    start_urls = ['https://www.insider.com/']

    def parse(self, response):
        res=response.css('.verticals-listitem+ .verticals-listitem')
        for r in res:
            category_link ='https://www.insider.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.insider.com/', callback=self.article_links)



    def article_links(self, response):
        res=response.css('.subnav-link')
        for r in res:
            catLink='https://www.insider.com'+r.css('a').attrib['href']
            yield response.follow(catLink, callback=self.Secarticle_links)

        data = response.css('.tout-title-link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.insider.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }


    def Secarticle_links(self, response):
        data = response.css('.tout-title-link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.insider.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class metroSpider(scrapy.Spider):
    name = 'metro'
    allowed_domains = ['metro.us']
    start_urls = ['https://www.metro.us/']

    def parse(self, response):
        res=response.css('.nav-menu-pile:nth-child(1) a')
        for r in res:
            category_link ='https://www.metro.us'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class law360Spider(scrapy.Spider):
    name = 'law360'
    allowed_domains = ['law360.com']
    start_urls = ['https://www.law360.com/']

    def parse(self, response):
        res=response.css('.list-group:nth-child(5) .list-group-item , div+ .list-group .list-group-item')
        for r in res:
            category_link ='https://www.law360.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.law360.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry-title, .article a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.law360.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class foxbusinessSpider(scrapy.Spider):
    name = 'foxbusiness'
    allowed_domains = ['foxbusiness.com']
    start_urls = ['https://www.foxbusiness.com/']

    def parse(self, response):
        res=response.css('.nav-item a')
        for r in range(0,46):
            category_link ='https://www.foxbusiness.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.foxbusiness.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.law360.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class hellenicshippingnewsSpider(scrapy.Spider):
    name = 'hellenicshippingnews'
    allowed_domains = ['hellenicshippingnews.com']
    start_urls = ['https://www.hellenicshippingnews.com/']

    def parse(self, response):
        res=response.css('#menu-main a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.hellenicshippingnews.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.post-title a, .post-box-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#04.05.2022
class afrSpider(scrapy.Spider):
    name = 'afr'
    allowed_domains = ['afr.com']
    start_urls = ['https://www.afr.com/']

    def parse(self, response):
        res=response.css('.EzC8j,._22VNd')
        for r in res:
            category_link ='https://www.afr.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('._20-Rx')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.afr.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cnbcSpider(scrapy.Spider):
    name = 'cnbc'
    allowed_domains = ['cnbc.com']
    start_urls = ['https://www.cnbc.com/']

    def parse(self, response):
        res=response.css('.politics .nav-menu-button , .tech .nav-menu-button , .investing .nav-menu-button , .business_news .nav-menu-button , .markets .nav-menu-button')
        subres=response.css('.nav-menu-subLinks').css('li')
        for r in range(0,5):
            category_link ='https://www.cnbc.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(0,43):
            category_link ='https://www.cnbc.com'+subres[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.cnbc.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.Card-titleContainer')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class prnewswireSpider(scrapy.Spider):
    name = 'prnewswire'
    allowed_domains = ['prnewswire.co.uk']
    start_urls = ['https://www.prnewswire.co.uk/']

    def parse(self, response):
        res=response.css('.omniture-subnav')
        for r in res:
            category_link ='https://www.prnewswire.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.prnewswire.co.uk/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.arabiclistingcards')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.prnewswire.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cnbctv18Spider(scrapy.Spider):
    name = 'cnbctv18'
    allowed_domains = ['cnbctv18.com']
    start_urls = ['https://www.cnbctv18.com/']

    def parse(self, response):
        res=response.css('.accordian-item:nth-child(3) .hamburger_menu , .sub-menu .hamburger_menu')
        for r in range(0,17):
            category_link ='https://www.cnbctv18.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.cnbctv18.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('li.jsx-3979883281')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class techradarSpider(scrapy.Spider):
    name = 'techradar'
    allowed_domains = ['techradar.com']
    start_urls = ['https://www.techradar.com/']

    def parse(self, response):
        res=response.css('li.menu-item')
        subres=response.css('ul.sub-menu').css('li')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(0,14):
            category_link = subres[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.techradar.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.listingResult, .feature-block-item-wrapper')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class rteSpider(scrapy.Spider):
    name = 'rte'
    allowed_domains = ['rte.ie']
    start_urls = ['https://www.rte.ie/']

    def parse(self, response):
        res=response.css('.business-nav-item+ li , .business-nav-item , #primary-nav li:nth-child(3) , #primary-nav li:nth-child(2) , #primary-nav li:nth-child(1)')

        for r in range(0,9):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
            print(category_link)

        yield response.follow('https://www.rte.ie/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.article-meta a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.rte.ie'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#05.05.2022
class bostonglobeSpider(scrapy.Spider):
    name = 'bostonglobe'
    allowed_domains = ['bostonglobe.com']
    start_urls = ['https://www.bostonglobe.com/']

    def parse(self, response):
        res=response.css('.pointer:nth-child(15) , .pointer:nth-child(14) , .pointer:nth-child(13) , .pointer:nth-child(12) , .pointer:nth-child(11) , .pointer:nth-child(10) , .pointer:nth-child(9) , .pointer:nth-child(8) , .pointer:nth-child(7) , .pointer:nth-child(6) , .pointer:nth-child(5) , .pointer:nth-child(4) , #primary_nav_links .pointer:nth-child(3) , .pointer:nth-child(2) , #primary_nav_links .pointer:nth-child(1)')

        for r in res:
            category_link ='https://www.bostonglobe.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.bostonglobe.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.margin_bottom')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.bostonglobe.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class fxstreetSpider(scrapy.Spider):
    name = 'fxstreet'
    allowed_domains = ['fxstreet.com']
    start_urls = ['https://www.fxstreet.com/']

    def parse(self, response):
        res=response.css('#CRYPTOS_SECTION+ .fxs_hideElements a , #ECONOMIC_CALENDAR_SECTION+ .fxs_hideElements a , #ANALYSIS_SECTION+ .fxs_hideElements a , #CRYPTOS_SECTION , #ECONOMIC_CALENDAR_SECTION , #ANALYSIS_SECTION , #NEWS_SECTION+ .fxs_hideElements a , #NEWS_SECTION , .fxs_subNav_col_2 a , #RATES_CHARTS_SECTION , #HOME_SECTION')

        for r in res:
            category_link ='https://www.fxstreet.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.fxs_headline_from_medium_to_large a , .fxs_headline_small a , .fxs_entryHeadline a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class gulfnewsSpider(scrapy.Spider):
    name = 'gulfnews'
    allowed_domains = ['gulfnews.com']
    start_urls = ['https://gulfnews.com/']

    def parse(self, response):
        res=response.css('.nav-item:nth-child(8) .nav-link , .nav-item:nth-child(7) .nav-link , .nav-item:nth-child(6) .nav-link , #menu-bar .nav-item:nth-child(5) .nav-link , #menu-bar .nav-item:nth-child(4) .nav-link , #menu-bar .nav-item:nth-child(3) .nav-link , #menu-bar .nav-item:nth-child(2) .nav-link , #menu-bar .nav-item:nth-child(1) .nav-link')
        for r in res:
                category_link ='https://gulfnews.com'+r.css('a').attrib['href']
                if 'videos' not in category_link:
                    yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):

        data = response.css('.card-title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://gulfnews.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class wsjSpider(scrapy.Spider):
    name = 'wsj'
    allowed_domains = ['wsj.com']
    start_urls = ['https://www.wsj.com/']

    def parse(self, response):
        res=response.css('.style--section-link--2rDVp5ht')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.wsj.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.WSJTheme--headline--7VCzo7Ay')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }
#status 403 but work in shell

class moneycontrolSpider(scrapy.Spider):
    name = 'moneycontrol'
    allowed_domains = ['moneycontrol.com']
    start_urls = ['https://www.moneycontrol.com/']

    def parse(self, response):
        res=response.css('.menu_l1:nth-child(3) a , .sub_nav:nth-child(5) a , .active+ .menu_l1 a')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.moneycontrol.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.list_sepbx a , #keynwstb1 a, #cagetory a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class channelnewsasiaSpider(scrapy.Spider):
    name = 'channelnewsasia'
    allowed_domains = ['channelnewsasia.com']
    start_urls = ['https://www.channelnewsasia.com/']

    def parse(self, response):
        res=response.css('.hamburger-menu__item--with-sub+ .hamburger-menu__item:nth-child(2) .hamburger-menu__link , .section-menu.hamburger-menu__link--sub-1 , .hamburger-menu__link--with-sub.main-menu__link--active')

        for r in range(0,9):
            category_link ='https://www.channelnewsasia.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.channelnewsasia.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.list-object__heading-link')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.channelnewsasia.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#06.05.2022
class foolSpider(scrapy.Spider):
    name = 'fool'
    allowed_domains = ['fool.com']
    start_urls = ['https://www.fool.com/']

    def parse(self, response):
        res=response.css('.leading-relaxed li,.gap-16px div , .mb-16px , .flex.text-gray-1100')

        for r in range(0,73):
            category_link=str(res[r])
            if 'https' in category_link:
                yield {
                    "News_links":  res[r].css('a').attrib['href']
                }
            if 'https' not in category_link:
                yield {
                    "News_links":'https://www.fool.com'+res[r].css('a').attrib['href']
                }

class editionSpider(scrapy.Spider):
    name = 'edition'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/']

    def parse(self, response):
        res=response.css('.fDMFSn:nth-child(11) .cgygcP , .fDMFSn:nth-child(12) .cgygcP , .fDMFSn:nth-child(7) .cgygcP , .fDMFSn:nth-child(6) .cgygcP , .fDMFSn:nth-child(5) .cgygcP , .fDMFSn:nth-child(4) .cgygcP , .fDMFSn:nth-child(3) .cgygcP , .fDMFSn:nth-child(2) .cgygcP , .fDMFSn:nth-child(9) .cgygcP , .fDMFSn:nth-child(8) .cgygcP , .fDMFSn:nth-child(1) .cgygcP')

        for r in res:
            checkR=str(r)
            if 'videos' not in checkR:
                category_link ='https://edition.cnn.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://edition.cnn.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.cd__headline a')
        for link in data:
            try:
                yield {
                    "News_links":'https://edition.cnn.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class investingSpider(scrapy.Spider):
    name = 'investing'
    allowed_domains = ['investing.com']
    start_urls = ['https://www.investing.com/']

    def parse(self, response):
        res=response.css('.navMenuUL > li:nth-child(4) a')

        for r in res:
            category_link ='https://www.investing.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.investing.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.textDiv')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.investing.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class startribuneSpider(scrapy.Spider):
    name = 'startribune'
    allowed_domains = ['startribune.com']
    start_urls = ['https://www.startribune.com/']

    def parse(self, response):
        res=response.css('.nav-secondary-shortcut:nth-child(10) .nav-shortcut-link , .nav-secondary-shortcut:nth-child(9) .nav-shortcut-link , .nav-primary-shortcut .nav-shortcut-link')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.startribune.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.tease-headline')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cnet(scrapy.Spider):
    name = 'cnet'
    allowed_domains = ['cnet.com']
    start_urls = ['https://www.cnet.com/']

    def parse(self, response):
        res = response.css('.c-siteMenuPanel_menu').css('li')
        for r in range(0,44):
            category_link ='https://www.cnet.com'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.cnet.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.c-universalLatest_text, .c-storiesHighlightsLead, .c-storiesExpertCardStory')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.cnet.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class tmcnet(scrapy.Spider):
    name = 'tmcnet'
    allowed_domains = ['tmcnet.com']
    start_urls = ['https://www.tmcnet.com/']

    def parse(self, response):
        res = response.css('.widget li+ li:nth-child(2) a , .sub-menu a , .under-menu .load-responsive ul a , .has-ot-mega-menu+ li li a , .widget-menu li:nth-child(1) a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.tmcnet.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('p+ a, #feedBox-content a, .list-space a, #feedbox-title a, .list-space a, h2 a')
        for link in data:
            try:
                if 'https' not in str(link):
                    yield {
                        "News_links":'https://www.tmcnet.com'+link.css('a').attrib['href']
                    }
                if 'https' in str(link):
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
            except:
                yield {
                    "News_links": None
                }

#09.05.2022
class forbesSpider(scrapy.Spider):
    name = 'forbes'
    allowed_domains = ['forbes.com']
    start_urls = ['https://www.forbes.com/']

    def parse(self, response):
        res=response.css('.mouse__enter .section__link , .header__color--statuesque-bronze .section__link , .header__color--capitalist-teal .section__link , .header__color--benjamins-green .section__link , .header__color--fortknox-gold .section__link , .header__color--diamondring-blue .section__link , .header__color--centennial-silver .section__link , .header__color--merlot-burgundy+ .header__hoverable a , .header__color--statuesque-bronze+ .header__hoverable .header__title , .header__color--statuesque-bronze .header__title , .header__color--capitalist-teal .header__title , .header__color--benjamins-green .header__title , .header__color--fortknox-gold .header__title , .header__color--diamondring-blue .header__title , .header__color--centennial-silver .header__title')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.forbes.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.headlink,.no-label--special-feature , .stream-item__title,.EventDescription_descriptionTitle__1RGAC , .LatestNewsItem_latestNewsItemBody__1tzGZ, .brand-voice-name .ng-binding, .more-content-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class reutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com/']

    def parse(self, response):
        res=response.css('.nav-bar__nav-button__2LWkE')

        for r in res:
            category_link ='https://www.reuters.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.reuters.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.media-story-card__heading__eqhp9')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.reuters.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class usatodaySpider(scrapy.Spider):
    name = 'usatoday'
    allowed_domains = ['usatoday.com']
    start_urls = ['https://www.usatoday.com/']

    def parse(self, response):
        res=response.css('nav.gnt_n_mn').css('a')

        for r in res:
            category_link ='https://www.usatoday.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.usatoday.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.gnt_m a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.usatoday.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com/']

    def parse(self, response):
        res=response.css('#orb-header .international a')

        for r in range(0,8):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.media__link, .rectangle-story-item__container, .ssrcss-tq7xfh-PromoContent .e1f5wbog0 ')
        for link in data:
            linkchk=str(link)
            if 'https' not in linkchk:
                try:
                    yield {
                        "News_links":'https://www.bbc.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }
            else:
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class prnewswireSpider(scrapy.Spider):
    name = 'prnewswire'
    allowed_domains = ['prnewswire.com']
    start_urls = ['https://www.prnewswire.com/']

    def parse(self, response):
        res=response.css('.omniture-subnav')

        for r in res:
            check=str(r)
            if 'news' in check:
                category_link ='https://www.prnewswire.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.prnewswire.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.arabiclistingcards, .col-sm-6 .row, .col-sm-8 , .display-outline').css('a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.prnewswire.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class nasdaqSpider(scrapy.Spider):
    name = 'nasdaq'
    allowed_domains = ['nasdaq.com']
    start_urls = ['https://www.nasdaq.com/']

    def parse(self, response):
        res=response.css('li.primary-nav__mega-subnav-item')

        for r in res:
            check=str(r)
            if 'news' in check:
                category_link ='https://www.nasdaq.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.topic-mini-feed__related-item')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.nasdaq.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#10.05.2022
class yahooSpider(scrapy.Spider):
    name = 'yahoo'
    allowed_domains = ['yahoo.com']
    start_urls = ['https://www.yahoo.com/']

    def parse(self, response):
        res=response.css('#root_7 , #root_6 , #root_5 , #root_4 , #root_3 , #root_2')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.yahoo.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('a.js-content-viewer')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.yahoo.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class mrwebSpider(scrapy.Spider):
    name = 'mrweb'
    allowed_domains = ['mrweb.com']
    start_urls = ['https://mrweb.com/']

    def parse(self, response):
        res=response.css('li:nth-child(9) a , #collapsemenu li:nth-child(1) a')

        for r in range(0,2):
            category_link ='https://mrweb.com/'+res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.comms-cover-right a, .col-md-8 .glyphicon-menu-right+ a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ibsintelligenceSpider(scrapy.Spider):
    name = 'ibsintelligence'
    allowed_domains = ['ibsintelligence.com']
    start_urls = ['https://ibsintelligence.com/']

    def parse(self, response):
        res=response.css('#myTab .nav-item:nth-child(2) .nav-link')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        res2=response.css('.col-md-4')
        yield response.follow(res2[0].css('a').attrib['href'], callback=self.article_links)
        yield response.follow('https://ibsintelligence.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.blogHor, .bvrCon, .blogVerBtn')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class computingSpider(scrapy.Spider):
    name = 'computing'
    allowed_domains = ['computing.co.uk']
    start_urls = ['https://www.computing.co.uk/']

    def parse(self, response):
        res=response.css('.active:nth-child(4) .nav-link , .arrowfixed+ .active .nav-link , .active:nth-child(1) .nav-link')
        ressub=response.css('.sub-part-nav a')
        for r in res:
            category_link ='https://www.computing.co.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in range(0,8):
            category_link ='https://www.computing.co.uk'+ressub[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.computing.co.uk/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.list-group-item h4 , .card h4 a, .row div div div div div:nth-child(2) a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.computing.co.uk'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class politicoSpider(scrapy.Spider):
    name = 'politico'
    allowed_domains = ['politico.com']
    start_urls = ['https://www.politico.com/']

    def parse(self, response):
        res=response.css('#js-top-header .js-tealium-tracking')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.politico.com/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('h3 .js-tealium-tracking,')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class govSpider(scrapy.Spider):
    name = 'gov'
    allowed_domains = ['gov.uk']
    start_urls = ['https://www.gov.uk/']

    def parse(self, response):
        res=response.css('.gem-c-layout-super-navigation-header__navigation-second-item-link')
        res2=response.css('.gem-c-image-card__title-link')
        for r in res:
            category_link ='https://www.gov.uk'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.parseSecondary)

        for r in res2:

            if 'https' not in str(r):
                category_link ='https://www.gov.uk'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

            if 'https'  in str(r):
                category_link = r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

    def parseSecondary(self, response):
        res=response.css('ul.browse__list').css('li')
        for r in res:
            category_link = 'https://www.gov.uk' + r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)




    def article_links(self, response):
        data = response.css('.govuk-link, .govspeak .govuk-link, .nhsuk-card__link, .govuk-\!-font-size-24 a')
        for link in data:
            if 'https' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.gov.uk' + link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https'  in str(link):
                try:
                    yield {
                        "News_links":  link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class zacksSpider(scrapy.Spider):
    name = 'zacks'
    allowed_domains = ['zacks.com']
    start_urls = ['https://www.zacks.com/']

    def parse(self, response):
        res=response.css('.selected a , #earnings-dd , #stocks-dd')
        for r in res:
                category_link =r.css('a').attrib['href']
                if '/' == str(category_link)[0]:
                    s = str(category_link).split('//')
                    l = s[1]
                    yield response.follow(l, callback=self.article_links)
                if '/' not in str(category_link)[0]:
                    yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.analytics_tracking')
        for link in data:
            if 'https' not in link.css('a').attrib['href']:
                try:
                    yield {
                        "News_links":'https://www.zacks.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https' in link.css('a').attrib['href']:
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }
# crawld 404

#Top 80 Cryptocurrency News Websites
#16.05.2022
class cointelegraphSpider(scrapy.Spider):
    name = 'cointelegraph'
    allowed_domains = ['cointelegraph.com']
    start_urls = ['https://cointelegraph.com/']

    def parse(self, response):
        res=response.css('.menu-desktop__item~ .menu-desktop__item+ .menu-desktop__item .menu-desktop-sub__link , .menu-desktop__item:nth-child(1) .menu-desktop-sub__link , .menu-desktop-sub__list:nth-child(1) .menu-desktop-sub__item:nth-child(1) .menu-desktop-sub__link')
        for r in res:
            category_link =r.css('a').attrib['href']
            f=str(category_link)
            if 'https' in f:
                yield response.follow(category_link, callback=self.article_links)

            if 'https' not in f:
                yield response.follow('https://cointelegraph.com'+category_link, callback=self.article_links)

            yield response.follow('https://cointelegraph.com/', callback=self.article_links)

    def article_links(self, response):
        data = response.css('.guide-card__title, .post-card__article, .post-card-inline, .post-card-inline__header')
        for link in data:
            if 'https' not in link.css('a').attrib['href']:
                try:
                    yield {
                        "News_links":'https://cointelegraph.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https' in link.css('a').attrib['href']:
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class newsbtcSpider(scrapy.Spider):
    name = 'newsbtc'
    allowed_domains = ['newsbtc.com']
    start_urls = ['https://www.newsbtc.com/']

    def parse(self, response):
        res=response.css('.menu-item-object-category.menu-item-has-children a')

        for r in range(0,20):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.newsbtc.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.format-standard .jeg_post_title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class newsbitcoinSpider(scrapy.Spider):
    name = 'newsbitcoin'
    allowed_domains = ['news.bitcoin.com']
    start_urls = ['https://news.bitcoin.com/']

    def parse(self, response):
        res=response.css('.header__title , .menu-item-52571 a , .menu-item-496724 a')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://news.bitcoin.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.story--medium__info, .story--small__text, .story--medium')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class uSpider(scrapy.Spider):
    name = 'u'
    allowed_domains = ['u.today']
    start_urls = ['https://u.today/']

    def parse(self, response):
        res=response.css('.header__nav-item--arrow:nth-child(4) .header__nav-child-link , .header__nav-item--arrow:nth-child(3) .header__nav-child-link , .header__nav-item--arrow:nth-child(2) .header__nav-child-link , .header__nav-item--arrow:nth-child(1) .header__nav-child-link , .header__nav-item--arrow:nth-child(4) .header__nav-link , .header__nav-item--arrow:nth-child(3) .header__nav-link , .header__nav-item--arrow:nth-child(2) .header__nav-link , .header__nav-item--arrow:nth-child(1) .header__nav-link')

        for r in res:
            category_link ='https://u.today'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://u.today/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.category-item__title-link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptoslateSpider(scrapy.Spider):
    name = 'cryptoslate'
    allowed_domains = ['cryptoslate.com']
    start_urls = ['https://cryptoslate.com/']

    def parse(self, response):
        res=response.css('li.menu-item-object-category')

        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://cryptoslate.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.list-post')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bitcoinmagazineSpider(scrapy.Spider):
    name = 'bitcoinmagazine'
    allowed_domains = ['bitcoinmagazine.com']
    start_urls = ['https://bitcoinmagazine.com/']

    def parse(self, response):
        res=response.css('#offcanvas0-3 .m-accordion--item-heading-link , #offcanvas0-2 .m-accordion--item-heading-link , #offcanvas0-1 .m-accordion--item-heading-link , #offcanvas0-0 .m-accordion--item-heading-link, .m-navbar--link:nth-child(2) , .m-navbar--link:nth-child(1)')

        for r in res:
            category_link ='https://bitcoinmagazine.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://bitcoinmagazine.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.m-card--header')
        for link in data:
            try:
                yield {
                    "News_links":'https://bitcoinmagazine.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#17.05.2022
class nineninebitcoinsSpider(scrapy.Spider):
    name = '99bitcoins'
    allowed_domains = ['99bitcoins.com']
    start_urls = ['https://99bitcoins.com/']

    def parse(self, response):

        yield response.follow('https://99bitcoins.com/', callback=self.article_links)
        yield response.follow('https://99bitcoins.com/category/news/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.read-more')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coinpediaSpider(scrapy.Spider):
    name = 'coinpedia'
    allowed_domains = ['coinpedia.org']
    start_urls = ['https://coinpedia.org/']

    def parse(self, response):
        res = response.css('.main-menu').css('ul.menu').css('li.menu-item')
        for r in range(0,27):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.post-title, .guide-cards, .article-blocks')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class forbesSpider(scrapy.Spider):
    name = 'forbes'
    allowed_domains = ['forbes.com']
    start_urls = ['https://www.forbes.com/']

    def parse(self, response):
        res = response.css('.header__color--capitalist-teal .section__link , .header__color--benjamins-green .section__link , .header__color--statuesque-bronze .section__link , .header__color--fortknox-gold .section__link , .header__color--merlot-burgundy+ .header__hoverable a~ .header__subnav .section__link , .header__color--merlot-burgundy .section__link , .header__color--diamondring-blue .section__link , .header__color--merlot-burgundy+ .header__hoverable a.header__title , .header__color--statuesque-bronze+ .header__hoverable .header__title , .header__color--statuesque-bronze .header__title , .header__color--capitalist-teal .header__title , .header__current .header__title , .header__color--fortknox-gold .header__title , .header__color--diamondring-blue .header__title , .header__color--centennial-silver .header__title , .header__color--centennial-silver .section__link')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.forbes.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.no-label--special-feature , .section-pick__title , .stream-item__title, td.name, .brand-voice-name .ng-binding, .card-wrap')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class ambcryptoSpider(scrapy.Spider):
    name = 'ambcrypto'
    allowed_domains = ['ambcrypto.com']
    start_urls = ['https://ambcrypto.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-category')
        for r in range(0,3):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://ambcrypto.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.infinite-post')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class beincryptoSpider(scrapy.Spider):
    name = 'beincrypto'
    allowed_domains = ['beincrypto.com']
    start_urls = ['https://beincrypto.com/']

    def parse(self, response):
        res = response.css('#menu-fast-links a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://beincrypto.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#18.05.2022
class cryptopotatoSpider(scrapy.Spider):
    name = 'cryptopotato'
    allowed_domains = ['cryptopotato.com']
    start_urls = ['https://cryptopotato.com/']

    def parse(self, response):
        res = response.css('#menu-submenu a , .menu-item-114354 a , .menu-item-28317 .sf-with-ul , .menu-item-2171 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://cryptopotato.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.entry-title a, .media-heading a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptonewsSpider(scrapy.Spider):
    name = 'cryptonews'
    allowed_domains = ['cryptonews.com']
    start_urls = ['https://cryptonews.com/']

    def parse(self, response):
        res = response.css('li:nth-child(3) a , li:nth-child(2) a')
        for r in res:
            category_link ='https://cryptonews.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://cryptonews.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.article__title--choice , .article__title--featured')
        for link in data:
            try:
                yield {
                    "News_links":'https://cryptonews.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptobriefingSpider(scrapy.Spider):
    name = 'cryptobriefing'
    allowed_domains = ['cryptobriefing.com']
    start_urls = ['https://cryptobriefing.com/']

    def parse(self, response):
        res = response.css('#menu-navigation-header-1 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://cryptobriefing.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.project-spotlight-url , .article-url , .main-news-link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class finextraSpider(scrapy.Spider):
    name = 'finextra'
    allowed_domains = ['finextra.com']
    start_urls = ['https://www.finextra.com/']

    def parse(self, response):
        res = response.css('.nav--toplevel-item:nth-child(1) .nav--link , .rake--link')
        for r in res:
            category_link ='https://www.finextra.com'+r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.finextra.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.article__title--choice , .article__title--featured, #premierSectionChild h4 a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.finextra.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class techbullionSpider(scrapy.Spider):
    name = 'techbullion'
    allowed_domains = ['techbullion.com']
    start_urls = ['https://techbullion.com/']

    def parse(self, response):
        res = response.css('.menu-item-3586 a , #menu-item-68 a , #menu-item-70 a , .tog-minus a , .menu-item-25184')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)




    def article_links(self, response):
        data = response.css('#tab-col2 li, .feat-widget-wrap, #mvp_pop_widget-5 li, .infinite-post')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bitcoinistSpider(scrapy.Spider):
    name = 'bitcoinist'
    allowed_domains = ['bitcoinist.com']
    start_urls = ['https://bitcoinist.com/']

    def parse(self, response):
        res = response.css('#footer .menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://bitcoinist.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.jeg_post_title a, .title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#19.05.2022
class cryptonewszSpider(scrapy.Spider):
    name = 'cryptonewsz'
    allowed_domains = ['cryptonewsz.com']
    start_urls = ['https://www.cryptonewsz.com/']

    def parse(self, response):
        res = response.css('.menu-item-68839 a')
        for r in range(0,21):
            category_link ='https://www.cryptonewsz.com/tag'+res[r].css('a').attrib['href']
            print(category_link)
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.cryptonewsz.com/', callback=self.article_links)






    def article_links(self, response):
        data = response.css('#block-17 li , .post-title a')
        for link in data:
            try:
                yield {
                    "News_links":'https://www.cryptonewsz.com'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class zycryptoSpider(scrapy.Spider):
    name = 'zycrypto'
    allowed_domains = ['zycrypto.com']
    start_urls = ['https://zycrypto.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-category a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://zycrypto.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coinquoraSpider(scrapy.Spider):
    name = 'coinquora'
    allowed_domains = ['coinquora.com']
    start_urls = ['https://coinquora.com/']

    def parse(self, response):
        res = response.css('li.menu-item')
        for r in range(0,33):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.col-md-4')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptonewsflashSpider(scrapy.Spider):
    name = 'crypto-news-flash'
    allowed_domains = ['crypto-news-flash.com']
    start_urls = ['https://www.crypto-news-flash.com/']

    def parse(self, response):
        res = response.css('.menu-item-21169 a , .menu-item-21144 a , .menu-item-21139 a , .menu-item-9747 a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.cryptonewsz.com/', callback=self.article_links)






    def article_links(self, response):
        data = response.css('.read-more a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coinjournalSpider(scrapy.Spider):
    name = 'coinjournal'
    allowed_domains = ['coinjournal.net']
    start_urls = ['https://coinjournal.net/']

    def parse(self, response):
        res = response.css('.lg\:mb-0:nth-child(1) .hover\:bg-menu-item-background-hover')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://coinjournal.net/', callback=self.article_links)






    def article_links(self, response):
        data = response.css('.leading-5, .leading-6')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coincentralSpider(scrapy.Spider):
    name = 'coincentral'
    allowed_domains = ['coincentral.com']
    start_urls = ['https://coincentral.com/news/']

    def parse(self, response):
        res = response.css('li.ccToolTip')
        for r in range(1,6):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.pp-content-grid-more-link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }


#20.05.2022
class blockchainSpider(scrapy.Spider):
    name = 'blockchain'
    allowed_domains = ['blockchain.news']
    start_urls = ['https://blockchain.news/']

    def parse(self, response):
        res = response.css('.col a')
        for r in res:

                category_link ='https://blockchain.news'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://blockchain.news/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.col-12.tab-content-title, .post-title')
        for link in data:
            try:
                yield {
                    "News_links":'https://blockchain.news'+link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class dailycoinSpider(scrapy.Spider):
    name = 'dailycoin'
    allowed_domains = ['dailycoin.com']
    start_urls = ['https://dailycoin.com/']

    def parse(self, response):
        res = response.css('.mkd-menu-has-sub a , .menu-item-object-page+ .mkd-menu-narrow a')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://dailycoin.com/', callback=self.article_links)






    def article_links(self, response):
        data = response.css('.mkd-pt-title-link')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptopressSpider(scrapy.Spider):
    name = 'cryptopress'
    allowed_domains = ['cryptopress.network']
    start_urls = ['https://cryptopress.network/']

    def parse(self, response):
        res = response.css('.menu-item-1100 a , .menu-item-1099 a , .menu-item-1114 a , .menu-item-1311 a , .menu-item-1098 a , .menu-item-1096 a , .menu-item-1097 a , .menu-item-1095 a , .menu-item-1094 a , .menu-item-1093 a , .menu-item-1092 a , .sf-with-ul , .menu-item-328 a')
        for r in range(0,12):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)







    def article_links(self, response):
        data = response.css('.jeg_post_title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thenewscryptoSpider(scrapy.Spider):
    name = 'thenewscrypto'
    allowed_domains = ['thenewscrypto.com']
    start_urls = ['https://thenewscrypto.com/']

    def parse(self, response):
        res = response.css('.menu-item-4610 .nav-link , .menu-item-16029 .nav-link , .menu-item-9881 .nav-link , .menu-item-2608 .nav-link')
        subres=response.css('ul.dropdown-menu').css('li')
        for r in res:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in subres:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://thenewscrypto.com/', callback=self.article_links)







    def article_links(self, response):
        data = response.css('.post-title, .sm-header, .p-2')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thecryptobasicSpider(scrapy.Spider):
    name = 'thecryptobasic'
    allowed_domains = ['thecryptobasic.com']
    start_urls = ['https://thecryptobasic.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-category')
        subres=response.css('ul.sub-menu').css('li')
        for r in range(0,7):
            category_link =res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        for r in subres:
            category_link =r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://thecryptobasic.com/', callback=self.article_links)







    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptoninjasSpider(scrapy.Spider):
    name = 'cryptoninjas'
    allowed_domains = ['cryptoninjas.net']
    start_urls = ['https://www.cryptoninjas.net/']

    def parse(self, response):
        res = response.css('.sub-menu a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.cryptoninjas.net/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.jeg_post_title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#23.05.2022
class cryptoemotionsSpider(scrapy.Spider):
    name = 'cryptoemotions'
    allowed_domains = ['cryptoemotions.com']
    start_urls = ['https://www.cryptoemotions.com/']

    def parse(self, response):
        res = response.css('.menu-item-793 a , .menu-item-481 a , .menu-item-482 a , .menu-item-477 a , .menu-item-1134 a , .menu-item-191 a')
        for r in range(0,13):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry__title--small a, .entry__title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class nulltxSpider(scrapy.Spider):
    name = 'nulltx'
    allowed_domains = ['nulltx.com']
    start_urls = ['https://nulltx.com/']

    def parse(self, response):
        res = response.css('#menu-menu-2-1 a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://nulltx.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class protosSpider(scrapy.Spider):
    name = 'protos'
    allowed_domains = ['protos.com']
    start_urls = ['https://protos.com/']

    def parse(self, response):
        res = response.css('.menu-item-12249 a , .menu-item-9733 a , .menu-item-163 a , #menu-item-86 a')
        for r in range(0,4):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://protos.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.u-heading-1 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class bitratesSpider(scrapy.Spider):
    name = 'bitrates'
    allowed_domains = ['bitrates.com']
    start_urls = ['https://www.bitrates.com/news']

    def parse(self, response):
        res = response.css('li.iscroll-item ')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)


    def article_links(self, response):
        data = response.css('.item-wrap')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptoreporterSpider(scrapy.Spider):
    name = 'crypto-reporter'
    allowed_domains = ['crypto-reporter.com']
    start_urls = ['https://www.crypto-reporter.com/']

    def parse(self, response):
        res = response.css('#menu-item-2006').css('ul.sub-menu').css('li')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.crypto-reporter.com/', callback=self.article_links)


    def article_links(self, response):
        data = response.css('.entry-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coincrunchSpider(scrapy.Spider):
    name = 'coincrunch'
    allowed_domains = ['coincrunch.in']
    start_urls = ['https://coincrunch.in/']

    def parse(self, response):
        res = response.css('#menu-primary-items a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.post-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#24.05.2022
class cryptocoinSpider(scrapy.Spider):
    name = 'cryptocoin'
    allowed_domains = ['cryptocoin.news']
    start_urls = ['https://cryptocoin.news/']

    def parse(self, response):
        res = response.css('ul.sub-menu').css('li')
        for r in range(0,9):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://cryptocoin.news/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class coinnounceSpider(scrapy.Spider):
    name = 'coinnounce'
    allowed_domains = ['coinnounce.com']
    start_urls = ['https://coinnounce.com/']

    def parse(self, response):
        res = response.css('.td-module-title a')
        for r in res:
                category_link =r.css('a').attrib['href']
                try:
                    yield {
                        "News_links": category_link
                    }
                except:
                    yield {
                        "News_links": None
                    }

class cryptocointradeSpider(scrapy.Spider):
    name = 'cryptocointrade'
    allowed_domains = ['cryptocointrade.com']
    start_urls = ['https://www.cryptocointrade.com/']

    def parse(self, response):
        yield response.follow('https://www.cryptocointrade.com/crypto-market-trading-news-info/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.elementor-post__title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class dcforecastsSpider(scrapy.Spider):
    name = 'dcforecasts'
    allowed_domains = ['dcforecasts.com']
    start_urls = ['https://www.dcforecasts.com/']

    def parse(self, response):
        res=response.css('ul.sub-menu').css('li.menu-item-type-taxonomy')
        for r in range(0, 47):
            category_link = res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.dcforecasts.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.jeg_post_title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptonewsSpider(scrapy.Spider):
    name = 'crypto-news'
    allowed_domains = ['crypto-news.net']
    start_urls = ['https://www.crypto-news.net/']

    def parse(self, response):
        res = response.css('.mg-tpt-txnlst').css('ul').css('li')
        for r in res:
            category_link = r.css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.crypto-news.net/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.wp-block-post-title, .title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptocurrencyguideSpider(scrapy.Spider):
    name = 'cryptocurrencyguide'
    allowed_domains = ['cryptocurrencyguide.org']
    start_urls = ['https://www.cryptocurrencyguide.org/']

    def parse(self, response):
        res=response.css('ul.sub-menu').css('li')
        for r in range(0,16):
            category_link = res[r].css('a').attrib['href']
            yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.cryptocurrencyguide.org/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.elementor-post__title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#25.05.2022
class latestcryptoSpider(scrapy.Spider):
    name = 'latestcrypto'
    allowed_domains = ['latestcrypto.news']
    start_urls = ['https://latestcrypto.news/']

    def parse(self, response):
        res = response.css('#menu-main-menu-1 a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://latestcrypto.news/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class menaSpider(scrapy.Spider):
    name = 'mena'
    allowed_domains = ['mena.news']
    start_urls = ['https://mena.news/#']

    def parse(self, response):
        res = response.css('#menu-fx-demo-header-menu a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.fx-module-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptofeedsSpider(scrapy.Spider):
    name = 'cryptofeeds'
    allowed_domains = ['cryptofeeds.news']
    start_urls = ['https://cryptofeeds.news/']

    def parse(self, response):
        res = response.css('.menu-item-5836 a , .menu-item-5837 a , .menu-item-621 a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('#main a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class thecryptonewswireSpider(scrapy.Spider):
    name = 'thecryptonewswire'
    allowed_domains = ['thecryptonewswire.com']
    start_urls = ['https://thecryptonewswire.com/']

    def parse(self, response):
        res = response.css('li.menu-item')
        for r in range(0,9):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.article-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptoglobalnewsSpider(scrapy.Spider):
    name = 'cryptoglobalnews'
    allowed_domains = ['cryptoglobalnews.live']
    start_urls = ['https://cryptoglobalnews.live/']

    def parse(self, response):
        res = response.css('li.menu-item')
        for r in range(0,5):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)



    def article_links(self, response):
        data = response.css('.post-title a, .elementor-post__title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptocurrencylatestnewsSpider(scrapy.Spider):
    name = 'cryptocurrencylatestnews'
    allowed_domains = ['cryptocurrencylatestnews.com']
    start_urls = ['https://cryptocurrencylatestnews.com/']

    def parse(self, response):
        res=response.css('ul.sub-menu').css('li')
        for r in range(0,11):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://cryptocurrencylatestnews.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.entry-title, .rpwe-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class decryptSpider(scrapy.Spider):
    name = 'decrypt'
    allowed_domains = ['decrypt.co']
    start_urls = ['https://decrypt.co/news']

    def parse(self, response):
        res = response.css('.pt-4').css('a')
        for r in res:
                category_link ='https://decrypt.co'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://decrypt.co/news', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class visionaryfinanceSpider(scrapy.Spider):
    name = 'visionaryfinance'
    allowed_domains = ['visionary-finance.com']
    start_urls = ['https://visionary-finance.com/']

    def parse(self, response):
        res = response.css('.menu-item-object-category a')
        for r in range(0,9):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://visionary-finance.com/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.post-link, .entry-title a , .entry-more')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#26.05.2022
class atozcryptoSpider(scrapy.Spider):
    name = 'atozcrypto'
    allowed_domains = ['atozcrypto.org']
    start_urls = ['https://atozcrypto.org/']

    def parse(self, response):
        res = response.css('.bd_cats_menu > a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://atozcrypto.org/', callback=self.article_links)



    def article_links(self, response):
        data = response.css('.entry-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class globalcryptopressSpider(scrapy.Spider):
    name = 'globalcryptopress'
    allowed_domains = ['globalcryptopress.com']
    start_urls = ['https://www.globalcryptopress.com/']

    def parse(self, response):
        res=response.css('.nav-header').css('ul').css('li')
        for r in range(0,6):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)




    def article_links(self, response):
        data = response.css('.title-post a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class allcryptocoininfoSpider(scrapy.Spider):
    name = 'allcryptocoininfo'
    allowed_domains = ['allcryptocoininfo.com']
    start_urls = ['https://allcryptocoininfo.com/']

    def parse(self, response):
        res=response.css('.menu-item-568 a , .menu-item-567 a , .menu-item-566 a , .menu-item-565 a , .menu-item-258 a')
        for r in range(0,5):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://allcryptocoininfo.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.entry-title a , #standard_pro-random-5 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptocurrencylatestnewsTodaySpider(scrapy.Spider):
    name = 'cryptocurrencylatestnewsToday'
    allowed_domains = ['cryptocurrencylatestnews.today']
    start_urls = ['https://cryptocurrencylatestnews.today/']

    def parse(self, response):
        res=response.css('#navigation a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://cryptocurrencylatestnews.today/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.title-post a#recent-posts-9 a , .cmsmasters_archive_item_title, #custom-posts-tabs-24 a , #recent-posts-9 a , #middle .entry-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class blockchainchapSpider(scrapy.Spider):
    name = 'blockchainchap'
    allowed_domains = ['blockchainchap.com']
    start_urls = ['https://blockchainchap.com/']

    def parse(self, response):
        res=response.css('ul.hfe-nav-menu').css('li')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://blockchainchap.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.post, .elementor-button-wrapper')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class sandboxlySpider(scrapy.Spider):
    name = 'sandboxly'
    allowed_domains = ['sandboxly.com']
    start_urls = ['https://sandboxly.com/']

    def parse(self, response):
        res=response.css('.menu-item-object-category a')
        for r in range(0,5):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://sandboxly.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.cs-entry__title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

#27.05.2022
class cryptoraderSpider(scrapy.Spider):
    name = 'cryptorader'
    allowed_domains = ['cryptorader.com']
    start_urls = ['https://cryptorader.com/']

    def parse(self, response):
        res=response.css('.menu-item-3174 a , .menu-item-3179 a , .menu-item-3173 a , .menu-item-3168 a , #menu-item-93 a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://cryptorader.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.mh-posts-focus-title-small a , .wp-block-latest-posts__post-title, .mh-custom-posts-small-title a , .mh-posts-list-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptobreakingnewsSpider(scrapy.Spider):
    name = 'cryptobreakingnews'
    allowed_domains = ['crypto.breakingnews.exchange']
    start_urls = ['https://crypto.breakingnews.exchange/']

    def parse(self, response):
        res=response.css('#menu-td-demo-header-menu-1 a')
        for r in range(0,8):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)




    def article_links(self, response):
        data = response.css('.td-module-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class fortunezSpider(scrapy.Spider):
    name = 'fortunez'
    allowed_domains = ['fortunez.com']
    start_urls = ['https://fortunez.com/']

    def parse(self, response):
        res=response.css('.menu-item-1328 a , .menu-item-150 a , .menu-item-3520 a')
        for r in range(0,6):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://fortunez.com/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.cb-post-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class breakingcryptoSpider(scrapy.Spider):
    name = 'breakingcrypto'
    allowed_domains = ['breakingcrypto.news']
    start_urls = ['https://breakingcrypto.news/']

    def parse(self, response):
        res=response.css('ul.menu').css('li.menu-item')
        for r in range(0,7):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://breakingcrypto.news/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('.read-title')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class livecryptoSpider(scrapy.Spider):
    name = 'livecrypto'
    allowed_domains = ['livecrypto.in']
    start_urls = ['https://livecrypto.in/']

    def parse(self, response):
        res=response.css('ul.menu').css('li.menu-item')
        for r in range(0,5):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)





    def article_links(self, response):
        data = response.css('.post-title a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class cryptodailySpider(scrapy.Spider):
    name = 'cryptodaily'
    allowed_domains = ['cryptodaily.co.uk']
    start_urls = ['https://cryptodaily.co.uk/']

    def parse(self, response):
        res=response.css('.position-relative:nth-child(9) .nav-link , .position-relative:nth-child(8) .nav-link , .position-relative:nth-child(7) .nav-link , .position-relative:nth-child(6) .nav-link , .position-relative:nth-child(5) .nav-link , .main-nav .position-relative:nth-child(4) .nav-link , .main-nav .position-relative:nth-child(3) .nav-link , .main-nav .position-relative:nth-child(2) .nav-link , .main-nav .position-relative:nth-child(1) .nav-link')
        for r in res:
                category_link ='https://cryptodaily.co.uk'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://cryptodaily.co.uk/', callback=self.article_links)




    def article_links(self, response):
        data = response.css('h3 a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

# новый шаблон который который я не собираюсь юзать, но пускай полежит тут
# a new class template, wich I'm not going to use, but let it lie here

class BostonSpider(scrapy.Spider):
    name = "BostonSpider"
    allowed_domains = ["boston.com"]
    start_urls = "https://www.boston.com/"
    check_ip_category = 0
    check_ip_article_links = 0

    def start_requests(self):
        res = scrapy.Request(
            self.start_urls,
            callback=self.parse,
            dont_filter=True,
            meta={"dont_retry": True, "download_timeout": timeout},
            errback=handle_error,
        )
        yield res

    def start_requests_ip(self, arg):
        res_ip = scrapy.Request(
            self.start_urls,
            meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
            callback=self.parse,
            dont_filter=True,
            errback=handle_error,
        )
        logging.info(
            {
                "proxy": "1",
                "clean_url": self.allowed_domains[0],
                "link": self.start_urls,
            }
        )
        yield res_ip

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                categories_links = []
                res = response.css("#panel-primary-nav a")
                for r in res:
                    try:
                        if "https://" in str(r.css("a").attrib["href"]):
                            categories_links.append(r.css("a").attrib["href"])
                        else:
                            categories_links.append(
                                "https://www.boston.com"
                                + r.css("a").attrib["href"]
                            )

                    except:
                        pass

                for i in categories_links:
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout},
                            errback=handle_error,
                        )

                        self.start_urls = i

                    except:
                        pass
                data = response.css(
                    ".m-article-list-feature__headline , .m-numbered-post-list__title , .a-article__title")
                for link in data:
                    try:
                        if "https" in str(link.css("a").attrib["href"]):
                            yield {"link": link.css("a").attrib["href"]}
                        else:
                            yield {
                                "link": "https://www.boston.com"
                                        + link.css("a").attrib["href"]
                            }
                    except:
                        pass
        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_category += 1

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css(
                    '.m-numbered-post-list__title , .m-article-list-feature__headline , .m-article-list__link')
                for link in data:
                    try:
                        if "https" in str(link.css("a").attrib["href"]):
                            yield {"link": link.css("a").attrib["href"]}
                        else:
                            yield {
                                "link": "https://www.boston.com"
                                        + link.css("a").attrib["href"]
                            }

                    except:
                        pass
        else:
            while self.check_ip_article_links < 2:
                self.start_urls = response.url
                yield response.follow(self.start_urls, callback=self.start_requests_ip)
                self.check_ip_article_links += 1


#summer 100 links

#06.07.2022

class weatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['weather.gov']
    start_urls = ['https://www.weather.gov/news/']


    def parse(self, response):
        data=response.css('.newsst0101, .newsst010122, .newsst01')
        for link in data:
            if 'weather.gov' in str(link):

                try:
                     yield {
                            "News_links": link.css('a').attrib['href']
                            }
                except:
                    yield {
                            "News_links": None
                            }

class mtvSpider(scrapy.Spider):
    name = 'mtv'
    allowed_domains = ['mtv.com']
    start_urls = ['http://www.mtv.com/news/']


    def parse(self, response):
        data=response.css('.headline')
        for link in data:

                    try:
                        yield {
                            "News_links": link.css('a').attrib['href']
                        }
                    except:
                        yield {
                            "News_links": None
                        }

class rottentomatoesSpider(scrapy.Spider):
    name = 'rottentomatoes'
    allowed_domains = ['editorial.rottentomatoes.com']
    start_urls = ['https://editorial.rottentomatoes.com/news']


    def parse(self, response):
        data=response.css('.newsItem')
        for link in data:

                    try:
                        yield {
                            "News_links": link.css('a').attrib['href']
                        }
                    except:
                        yield {
                            "News_links": None
                        }

class hopkinsmedicineSpider(scrapy.Spider):
    name = 'hopkinsmedicine'
    allowed_domains = ['hopkinsmedicine.org']
    start_urls = ['https://www.hopkinsmedicine.org/news/newsroom']

    def parse(self, response):
        res=response.css('.btn-purple')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)
        yield response.follow('https://www.hopkinsmedicine.org/news/newsroom', callback=self.article_links)




    def article_links(self, response):
        data = response.css('a.article, a.item')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }

class verdictjustiaSpider(scrapy.Spider):
    name = 'verdictjustia'
    allowed_domains = ['verdict.justia.com']
    start_urls = ['https://verdict.justia.com/topics']

    def parse(self, response):
        res=response.css('#main a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)





    def article_links(self, response):
        data = response.css('.read_more_link a')
        for link in data:
            try:
                yield {
                    "News_links":link.css('a').attrib['href']
                }
            except:
                yield {
                    "News_links": None
                }


#08.07.2022
class nbcSpider(scrapy.Spider):
    name = 'nbc'
    allowed_domains = ['nbc.com']
    start_urls = ['https://www.nbc.com/nbc-insider']

    def parse(self, response):
        res=response.css('.nav__secondary a')
        for r in res:
                category_link ='https://www.nbc.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)





    def article_links(self, response):
        data = response.css('.teaser__meta')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.nbc.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class medicinenetSpider(scrapy.Spider):
    name = 'medicinenet'
    allowed_domains = ['medicinenet.com']
    start_urls = ['https://www.medicinenet.com/health_medical_news/article.htm']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.medicinenet.com/health_medical_news/article.htm', callback=self.article_links)





    def article_links(self, response):
        data = response.css('#news_header a')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.medicinenet.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class federalreserveSpider(scrapy.Spider):
    name = 'federalreserve'
    allowed_domains = ['federalreserve.gov']
    start_urls = ['https://www.federalreserve.gov/newsevents/pressreleases.htm']

    def parse(self, response):
        res=response.css('.dropdown--1Col li:nth-child(3) .sr-only-focusable , .dropdown--1Col li:nth-child(2) .sr-only-focusable , .dropdown--1Col li:nth-child(1) .sr-only-focusable')
        for r in res:
                category_link ='https://www.federalreserve.gov'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)





    def article_links(self, response):
        data = response.css('.itemTitle .ng-binding')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.federalreserve.gov'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }
#res=[]

class uwaterlooSpider(scrapy.Spider):
    name = 'uwaterloo'
    allowed_domains = ['uwaterloo.ca']
    start_urls = ['https://uwaterloo.ca/news/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://uwaterloo.ca/news/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.uw_ct_story')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://uwaterloo.ca'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class newssophosSpider(scrapy.Spider):
    name = 'newssophos'
    allowed_domains = ['news.sophos.com']
    start_urls = ['https://news.sophos.com/en-us/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://news.sophos.com/en-us/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.py-6')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://news.sophos.com/en-us'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class nberSpider(scrapy.Spider):
    name = 'nber'
    allowed_domains = ['nber.org']
    start_urls = ['https://www.nber.org/nber-news?page=1&perPage=50']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.nber.org/nber-news?page=1&perPage=50', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.digest-card__title a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.nber.org/news'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class businessinsiderSpider(scrapy.Spider):
    name = 'businessinsider'
    allowed_domains = ['businessinsider.com']
    start_urls = ['https://www.businessinsider.com/']

    def parse(self, response):
        res=response.css('.subnav-item:nth-child(8) .headline-regular')
        for r in res:
                category_link ='https://www.businessinsider.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.businessinsider.com/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.tout-title-link, .graviton a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.businessinsider.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

#17.07.2022
class acluSpider(scrapy.Spider):
    name = 'aclu'
    allowed_domains = ['aclu.org']
    start_urls = ['https://www.aclu.org/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.aclu.org/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('a.hp__top_news_link, a.hp__latest_news_link')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.aclu.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class btSpider(scrapy.Spider):
    name = 'bt'
    allowed_domains = ['bt.com']
    start_urls = ['https://www.bt.com/sport/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.bt.com/sport/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.s4 a')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.bt.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class marthastewartSpider(scrapy.Spider):
    name = 'marthastewart'
    allowed_domains = ['marthastewart.com']
    start_urls = ['https://www.marthastewart.com/1543773/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.marthastewart.com/1543773/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.carouselNav__listItem , .category-page-videos-lead , .category-page-item-content')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.marthastewart.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class ieaSpider(scrapy.Spider):
    name = 'iea'
    allowed_domains = ['iea.org']
    start_urls = ['https://www.iea.org/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.iea.org/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.m-news-listing__link')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.iea.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class mastercardSpider(scrapy.Spider):
    name = 'mastercard'
    allowed_domains = ['mastercard.com']
    start_urls = ['https://www.mastercard.com/news/europe/fr-fr']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.mastercard.com/news/europe/fr-fr', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.accordion-item__separator-heading, .story-tile')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.mastercard.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class unhcrSpider(scrapy.Spider):
    name = 'unhcr'
    allowed_domains = ['unhcr.org']
    start_urls = ['https://www.unhcr.org/news-and-stories.html']

    def parse(self, response):
        res=response.css('.thirdlevel-list a')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.unhcr.org/news-and-stories.html', callback=self.article_links)





    def article_links(self, response):
        data = response.css('a.cta__box, .results li, .cta__info')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.unhcr.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class healthSpider(scrapy.Spider):
    name = 'health'
    allowed_domains = ['health.com']
    start_urls = ['https://www.health.com/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.health.com/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('a.mntl-card-list-items')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.health.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class wtoSpider(scrapy.Spider):
    name = 'wto'
    allowed_domains = ['wto.org']
    start_urls = ['https://www.wto.org/english/news_e/news_e.htm']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.wto.org/english/news_e/news_e.htm', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.paracolourtext')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.wto.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }
#res=[]

class unhcrSpider(scrapy.Spider):
    name = 'unhcr'
    allowed_domains = ['unhcr.org']
    start_urls = ['https://guinnessworldrecords.com/news/latest-news']

    def parse(self, response):
        res=response.css('.dynamic-menu-content .mob-menu-link')
        for r in range(1,4):
                category_link ='https://guinnessworldrecords.com'+res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)






    def article_links(self, response):
        data = response.css('#home-page-news a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://guinnessworldrecords.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }
#res=[]

class geSpider(scrapy.Spider):
    name = 'ge'
    allowed_domains = ['ge.com']
    start_urls = ['https://www.ge.com/news/']

    def parse(self, response):
        res=response.css('.mr-4')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.ge.com/news/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.article--link')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.ge.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class idcSpider(scrapy.Spider):
    name = 'idc'
    allowed_domains = ['idc.com']
    start_urls = ['https://www.idc.com/search/other/perform_.do?page=1&hitsPerPage=25&sortBy=DATE&srchIn=ALLRESEARCH&src=&athrT=10&cg=5_1291&cmpT=10&pgT=10&trid=121110108&siteContext=IDC']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.idc.com/search/other/perform_.do?page=1&hitsPerPage=25&sortBy=DATE&srchIn=ALLRESEARCH&src=&athrT=10&cg=5_1291&cmpT=10&pgT=10&trid=121110108&siteContext=IDC', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.result-title')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://www.idc.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class newsdeltaSpider(scrapy.Spider):
    name = 'newsdelta'
    allowed_domains = ['news.delta.com']
    start_urls = ['https://news.delta.com/']

    def parse(self, response):
        res=response.css('#block-dnh-main-menu .nav-link')
        for r in res:
                category_link ='https://news.delta.com'+r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://news.delta.com/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.views-field-title a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":None
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://news.delta.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }




#18.07.2022
class diabetesSpider(scrapy.Spider):
    name = 'diabetes'
    allowed_domains = ['diabetes.org']
    start_urls = ['https://diabetes.org/newsroom-all']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://diabetes.org/newsroom-all', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.view--newsroom-title')
        for link in data:
            if 'https://' in str(link):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link):
                try:
                    yield {
                        "News_links":'https://diabetes.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class ucalgarySpider(scrapy.Spider):
    name = 'ucalgary'
    allowed_domains = ['ucalgary.ca']
    start_urls = ['https://www.ucalgary.ca/ucalgary-news']

    def parse(self, response):
        res=response.css('.image+ .text .red-back')
        for r in res:
                category_link =r.css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.ucalgary.ca/ucalgary-news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.image+ .text .one-col :nth-child(2), .read-more')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.ucalgary.ca'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class blognationalgeographicSpider(scrapy.Spider):
    name = 'blognationalgeographic'
    allowed_domains = ['blog.nationalgeographic.org']
    start_urls = ['https://blog.nationalgeographic.org/']

    def parse(self, response):
        res=response.css('.ng-text-uppercase')
        for r in range(0,5):
                category_link =res[r].css('a').attrib['href']
                yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://blog.nationalgeographic.org/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.ng-padding-medium-bottom a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://blog.nationalgeographic.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class granicusSpider(scrapy.Spider):
    name = 'granicus'
    allowed_domains = ['granicus.com']
    start_urls = ['https://granicus.com/news-press/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://granicus.com/news-press/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.cover-link')
        for link in data:
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class iataSpider(scrapy.Spider):
    name = 'iata'
    allowed_domains = ['iata.org']
    start_urls = ['https://www.iata.org/en/pressroom/searchresults/?ContentType=85#searchForm']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.iata.org/en/pressroom/searchresults/?ContentType=85#searchForm', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.result-listing-item')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.iata.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class worldwildlifeSpider(scrapy.Spider):
    name = 'worldwildlife'
    allowed_domains = ['worldwildlife.org']
    start_urls = ['https://www.worldwildlife.org/stories']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.worldwildlife.org/stories', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.first-featured , #content .gutter-horiz-in')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.worldwildlife.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class parentsSpider(scrapy.Spider):
    name = 'parents'
    allowed_domains = ['parents.com']
    start_urls = ['https://www.parents.com/news/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.parents.com/news/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('a.mntl-card-list-items')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.parents.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class dpreviewSpider(scrapy.Spider):
    name = 'dpreview'
    allowed_domains = ['dpreview.com']
    start_urls = ['https://www.dpreview.com/features']

    def parse(self, response):
        res=response.css('.articlesCount a')
        for r in res:
                    category_link =r.css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.dpreview.com/features', callback=self.article_links)





    def article_links(self, response):
        data = response.css('#mainContent .title a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.dpreview.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class blSpider(scrapy.Spider):
    name = 'bl'
    allowed_domains = ['bl.uk']
    start_urls = ['https://www.bl.uk/news/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.bl.uk/news/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.pnl-title')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.bl.uk'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class unwomenSpider(scrapy.Spider):
    name = 'unwomen'
    allowed_domains = ['unwomen.org']
    start_urls = ['https://www.unwomen.org/en/news-and-events/stories']

    def parse(self, response):
        res=response.css('.facet-item a')
        for r in res:
                    category_link ='https://www.unwomen.org'+r.css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.unwomen.org/en/news-and-events/stories', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.search-item-title')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.unwomen.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class unwomenSpider(scrapy.Spider):
    name = 'unwomen'
    allowed_domains = ['unwomen.org']
    start_urls = ['https://www.unwomen.org/en/news-and-events/stories']

    def parse(self, response):
        res=response.css('.facet-item a')
        for r in res:
                    category_link ='https://www.unwomen.org'+r.css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.unwomen.org/en/news-and-events/stories', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.search-item-title')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.unwomen.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

#19.07.2022
class pfizerSpider(scrapy.Spider):
    name = 'pfizer'
    allowed_domains = ['pfizer.com']
    start_urls = ['https://www.pfizer.com/news']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.pfizer.com/news', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.lmedium-10 h5')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.pfizer.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class reasonSpider(scrapy.Spider):
    name = 'reason'
    allowed_domains = ['reason.com']
    start_urls = ['https://reason.com/latest/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://reason.com/latest/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('h4 a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://reason.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class newsnicovideoSpider(scrapy.Spider):
    name = 'newsnicovideo'
    allowed_domains = ['news.nicovideo.jp']
    start_urls = ['https://news.nicovideo.jp/?cmnhd_ref=device%3Dpc%26site%3Dniconico%26pos%3Dheader_servicelink%26page%3Dtop']

    def parse(self, response):
        res=response.css('.tabs a')
        for r in res:
                    category_link ='https://news.nicovideo.jp'+r.css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)





    def article_links(self, response):
        data = response.css('.news-article')
        for link in data:
            if '//news.nicovideo.jp' in str(link.css('a').attrib['href']) and 'https:' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https:'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://news.nicovideo.jp' in str(link.css('a').attrib['href']):

                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }


            if '//news.nicovideo.jp' not in str(link.css('a').attrib['href']) and 'https:' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://news.nicovideo.jp'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class swissinfoSpider(scrapy.Spider):
    name = 'swissinfo'
    allowed_domains = ['swissinfo.ch']
    start_urls = ['https://www.swissinfo.ch/eng']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.swissinfo.ch/eng', callback=self.article_links)





    def article_links(self, response):
        data = response.css('a.si-teaser__link')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.swissinfo.ch'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class namiSpider(scrapy.Spider):
    name = 'nami'
    allowed_domains = ['nami.org']
    start_urls = ['https://nami.org/About-NAMI/NAMI-News']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://nami.org/About-NAMI/NAMI-News', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.summary a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://nami.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class reliefwebSpider(scrapy.Spider):
    name = 'reliefweb'
    allowed_domains = ['reliefweb.int']
    start_urls = ['https://reliefweb.int/updates?view=headlines']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://reliefweb.int/updates?view=headlines', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.rw-river-article__title a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://reliefweb.int'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class updatespandaSpider(scrapy.Spider):
    name = 'updatespanda'
    allowed_domains = ['updates.panda.org']
    start_urls = ['https://updates.panda.org/tag/blog']

    def parse(self, response):
        res=response.css('.active-branch+ .hs-menu-depth-2 a , .active a')
        for r in range(0,2):
                    category_link =res[r].css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)







    def article_links(self, response):
        data = response.css('.link, .news-block')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://updates.panda.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class petaSpider(scrapy.Spider):
    name = 'peta'
    allowed_domains = ['peta.org']
    start_urls = ['https://www.peta.org/blog/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.peta.org/blog/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.description').css('h2')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.peta.org'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class euractivSpider(scrapy.Spider):
    name = 'euractiv'
    allowed_domains = ['euractiv.com']
    start_urls = ['https://www.euractiv.com/news/']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.euractiv.com/news/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.caption a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.euractiv.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class syfySpider(scrapy.Spider):
    name = 'syfy'
    allowed_domains = ['syfy.com']
    start_urls = ['https://www.syfy.com/syfy-wire']

    def parse(self, response):
       # res=response.css('.nav__secondary a')
       # for r in res:
         #       category_link =r.css('a').attrib['href']
        #        yield response.follow(category_link, callback=self.article_links)
       yield response.follow('https://www.syfy.com/syfy-wire', callback=self.article_links)





    def article_links(self, response):
        data = response.css('.teaser__meta')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":None
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.syfy.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

class dailysignalSpider(scrapy.Spider):
    name = 'dailysignal'
    allowed_domains = ['dailysignal.com']
    start_urls = ['https://www.dailysignal.com/']

    def parse(self, response):
        res=response.css('.evergreen a')
        for r in res:
                    category_link ='https://www.dailysignal.com'+r.css('a').attrib['href']
                    yield response.follow(category_link, callback=self.article_links)

        yield response.follow('https://www.dailysignal.com/', callback=self.article_links)





    def article_links(self, response):
        data = response.css('h2 a')
        for link in data:
            if 'https://' in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }

            if 'https://' not in str(link.css('a').attrib['href']):
                try:
                    yield {
                        "News_links":'https://www.dailysignal.com'+link.css('a').attrib['href']
                    }
                except:
                    yield {
                        "News_links": None
                    }


#a thing for running a script without a command in the console, I won’t use it either
process = CrawlerProcess(settings={
                'FEED_URI': f'Newlink_1.json',
                'FEED_FORMAT': 'json',
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
            })

process.crawl(dailysignalSpider)
process.start()
