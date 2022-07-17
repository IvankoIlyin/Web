# Scrapy spider


##What this spider do
These spiders are created to scrape news article links from all category of the website.
Each website will have each unique spider

##Directory Description
* In scrapyproject there is on main directory multiplecrawlers which contain 3 sub-directory.
  * No.1 examples which contain multiples_example.py in multiples_example.py there are three example names as 'Example number 1','Example number 2','Example number 3' these examples were there for you reference and further described under "Template description".
  * No.2 final_job which contain multiples_final.py this is the final file where you will save the final spiders.
  * No.3 src which contains 7 files.
    * config.py used for the configuration used in scrapy (don't change it).
    * example.py which can be used to see if this spider is running on you machine or not and also for the reference how to structure a spider.
    * multiple.py.
    * Newlink_1.json its a json file contain all the scraped article link this file is used to see if we are able to scrape links or not.
    * settings.py used for scrapy settings(don't change it).
    * template.py contains 3 templates you have to choose which template to use for which website further described under 'Template description'
    * to_test.py used to write a spider and test it there.

## Type of website
There are three types of website we will deal with in this project.
* Number 1 websites which have category links and no subcategory links.
  * Ex: https://www.boston.com in this website all category links are on the home page so we have to get the category links from the home page and scrape all the articles links from that categories.
* Number 2 websites which don't have any category links.
  * Ex : https://www.consultancy.uk/ this website has category but that categories are of no use for us because categories are like job, service,ranking so in that case we have to find if there is any category like news or latest then we have to use that link as our start url not 'https://www.consultancy.uk/'
  * In above case start url should be https://www.consultancy.uk/news not https://www.consultancy.uk 
  * In this case we will use template number 2.



## Naming of spider and class :
Examples:
* Website : https://www.cbsnews.com/ 
    * spider name : CbsNewsSpider.
    * Class name : CbsNewsSpider(scrapy.Spider)
* Website : https://www.treasuryandrisk.com
    * spider name : TreasuryAndRiskSpider
    * Class name : TreasuryAndRiskSpider(scrapy.Spider)
  
In short make every first letter of the website name capital and add Spider in the end.

## Not to do :
1. Do not make any changes in config.py,settings.py else spider will not run.
2. Do not change the variables name or any function name for example:

```
name = ""
allowed_domains = ["abc.com"]
not_allowed_keyword = ['video','picture','contact us']
start_urls = "https://www.abc.com"
check_ip_category = 0
check_ip_article_links = 0

def parse(self, response):
def article_links(self, response):
def start_requests_ip(self, arg):
def start_requests(self):
def sub_category(self, response):
```


##How to run example.py:
* Make sure you have installed python.
* Make sure you have installed pycharm or any IDE.
* Make sure you have installed requirements.txt.
  * To install requirements.txt use ```cd /path to requirement.txt directory``` then run ```pip install -r requirements.txt``` in the terminal.
  * Or open pycharm setting click on python interpreter and click on the plus sign and search for all libraries in requirements.txt one by one and install it from there.
  * <img width="995" alt="Screenshot 2022-06-03 at 4 18 24 PM" src="https://user-images.githubusercontent.com/99249497/171840281-0d0dac1f-cee1-48e2-963e-e36945eec533.png">

* After all the installation is done open example.py right click on it make click on run.
* Or use this ```scrapy runspider example.py``` on you terminal.

## Which template to choose
* Step1 : See if its a news website or not sometime somewebsite are ecommerce website.
* Step2 : If a news website see if there is any category like sport,latest,bussiness,covid-19 etc.
* Step3 : If there is category then open those category links and see there any more category in each category links for example: website has a category sports when we sport the sport link there is some more new category like football,cricket,basketball etc.
* Step4 : If there step3 is true then choose tempelate number 1, if step2 is true and step 3 is false choose template 2.
* Step5 : If step3 and step3 both are false but you that there is only one category which contains news then use template 3.

## How to write a spider 


## How to save time with scrapy shell and check response from the website
* Video link googledrive/abc.mp4
* Write scrapy shell in your pycharm terminal 
* Now you are on scrapy shell write commaand ```fetch https://abcnews.com```
* Type ```response``` if response is 200 then its ok we can continue with this website.

## How to do final test with example.py


## where to save
