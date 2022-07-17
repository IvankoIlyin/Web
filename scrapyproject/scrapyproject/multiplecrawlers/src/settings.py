import logging

custom_scrapy_logs = logging.ERROR
logging.getLogger('scrapy').setLevel(custom_scrapy_logs)  # disable all logs of scrapy apart from error logs

BOT_NAME = 'multiplecrawler'

SPIDER_MODULES = ['multiplecrawler.src']
NEWSPIDER_MODULE = 'multiplecrawler.src'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False


CONCURRENT_REQUESTS = 16

