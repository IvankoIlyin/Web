import scrapy

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