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