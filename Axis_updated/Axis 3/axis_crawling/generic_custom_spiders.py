from generic_spider import GenericSpider


class AbpliveSpider(GenericSpider):
    name = 'AbpliveSpider'
    allowed_domains = ['news.abplive.com']
    scope_selector = ".news_featured,.home-hero-news,a.other_news,.el-hero-news,.el-subnews,a.news_content," \
                     ".first-news-item,div.news_content a, div.other_news a"
    extractors = {"link": "::attr(href)"}

    def process_link(self, value, item, response):
        if not value:
            return value
        value = value.strip()
        print(value)
        if value.count('/') < 1:
            print(value)
            return None
        value = response.urljoin(value)
        return value
