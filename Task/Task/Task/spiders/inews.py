import scrapy


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

class businessinsiderSpider(scrapy.Spider):
    name = 'businessinsider'
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
