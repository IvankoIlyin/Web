import csv
import datetime
import logging
import os
import json
from twisted.internet import reactor
from multiprocessing import Process, Manager

from scrapy.crawler import CrawlerRunner

from generic_spider import create_spider_class
import multiple as multiple_spider
import generic_custom_spiders as custom_spiders


def get_spider_data(clean_rss, csv_reader):
    for spider in csv_reader:
        if spider['clean_rss'] == clean_rss:
            return spider


def get_spider(clean_rss, message, generic_spider_configs):
    spider = None
    if clean_rss in generic_spider_configs:
        spider = create_spider_class(clean_rss, generic_spider_configs[clean_rss], message)
    elif hasattr(custom_spiders, clean_rss):
        spider = getattr(custom_spiders, clean_rss)
    else:
        logging.error("Failed to retrieve spider {}, doesn't exist".format(clean_rss))
    return spider


items = []
# this fields are overwrite in pipeline based on message
ignore_fields = ['clean_rss', 'clean_url', 'topic', 'country', 'flag', 'gn_mode', 'type']


class DataStorePipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        global items
        items = self.items


def get_crawled_data(spider, message, settings):
    item_list = Manager().list()

    def inner_crawl(spider, message, settings, item_list):
        runner = CrawlerRunner(settings)
        runner.crawl(spider,
                     clean_url=message['clean_url'],
                     clean_rss=message['clean_rss'],
                     start_urls=message['base_url'].split(','),
                     topic=message['topic'], flag=message['flag'],
                     gn_mode=message['gn_mode'],
                     type=message['type'],
                     country=message['country'])
        deferred = runner.join()
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        item_list.extend(items)

    p = Process(target=inner_crawl, args=(spider, message, settings, item_list))
    p.start()
    p.join()
    return item_list


def compare_data(multiple_py_out, generic_spider_out):
    def replace_na(value):
        if value == 'na':
            return None
        return value

    def get_clean_crawl_dictionary(items):
        def get_item_hash(item):
            item_hash = item.get('link', '')
            if not item_hash:
                item_hash = item.get('pdf_url', '')
            item_hash = item_hash.strip().strip('/').replace('https://', '').replace('http://', '').replace(' ', '%20')
            return item_hash

        def get_clean_item(item):
            # remove published_date, parse_date if it's now
            for date_field in {'published_date', 'parse_date'}:
                if item.get(date_field) and item[date_field] not in {'na'}:
                    try:
                        date_value = datetime.datetime.strptime(item[date_field], '%Y-%m-%d %H:%M:%S')
                        if datetime.datetime.now() > date_value > datetime.datetime.now() + datetime.timedelta(
                                minutes=30):
                            item.pop(date_field)
                    except Exception as e:
                        pass
            for ignore_field in ignore_fields:
                if ignore_field in item:
                    item.pop(ignore_field)
            for field in {'title', 'base_url'}:
                if field in item and item[field]:
                    item[field] = item[field].strip()
            item['base_url'] = item['base_url'].strip('/')
            return item

        final_item_dict = {}
        for item in items:
            key = get_item_hash(item)
            if key not in final_item_dict:
                final_item_dict[key] = []
            final_item_dict[key].append(json.dumps(item))
        return {i: get_clean_item(json.loads(max(final_item_dict[i]))) for i in final_item_dict}

    is_any_mismatch_found = False
    multiple_py_dict = get_clean_crawl_dictionary(multiple_py_out)
    generic_spider_dict = get_clean_crawl_dictionary(generic_spider_out)

    not_present_in_multiple = 0
    for i in generic_spider_dict:
        if i not in multiple_py_dict:
            if not_present_in_multiple == 0:
                print('=' * 50)
                print(('#' * 5) + "Items present in generic spider but not in multiple(regular)" + ('#' * 5))
            not_present_in_multiple += 1
            if not_present_in_multiple > 10:
                continue
            is_any_mismatch_found = True
            print('   ' + i)
    if not_present_in_multiple > 10:
        print('  .... found %s more' % not_present_in_multiple)

    not_present_in_generic = 0
    for i in multiple_py_dict:
        if i not in generic_spider_dict:
            if not_present_in_generic == 0:
                print('=' * 50)
                print(('#' * 5) + "Items present in multiple(regular) but not in generic spider " + ('#' * 5))
            not_present_in_generic += 1
            if not_present_in_generic > 10:
                continue
            is_any_mismatch_found = True
            print('   ' + i)
    if not_present_in_generic > 10:
        print('  .... found %s more' % not_present_in_generic)

    item_data_diff_count = 0
    more_key_count = 0
    print('=' * 50)
    print(('#' * 5) + "Items data different" + ('#' * 5))
    non_matching_fields = set()
    for item_hash in multiple_py_dict:
        if item_hash not in generic_spider_dict:
            continue
        multiple_item = multiple_py_dict[item_hash]
        generic_item = generic_spider_dict[item_hash]
        flag = False
        for field in multiple_item:
            if field in {'link', 'pdf_url'}:
                continue
            if replace_na(multiple_item.get(field)) != replace_na(generic_item.get(field)):
                is_any_mismatch_found = True
                item_data_diff_count += 1
                if item_data_diff_count > 15:
                    continue
                if not flag:
                    print('  -mismatch found in item ' + json.dumps(multiple_item))
                    flag = True
                non_matching_fields.add(field)
                print('   field =>', field)
                print('    multiple_py_out =>', multiple_item.get(field))
                print('    generic_py_out =>', generic_item.get(field))
        multiple_item_keys = sorted([i for i in items if multiple_item[i] not in {'na', None}])
        generic_item_keys = sorted([i for i in items if generic_item[i] not in {'na', None}])
        if multiple_item_keys != generic_item_keys:
            more_key_count += 1
            if more_key_count > 10:
                continue
            print('  -new key found in generic spider output that not present in multiple ' + json.dumps(
                multiple_py_dict[item_hash]))
            for field in generic_item_keys:
                if field not in multiple_item_keys:
                    is_any_mismatch_found = True
                    print('   new field found: %s value=>%s' % (field, generic_item[field]))

    print('=' * 50)
    if is_any_mismatch_found:
        is_issue_with_trailling_slash = False
        print('  SOMETHING IS WRONG, PLEASE CHECK ABOVE DATA TO FIX CRAWLER')
        print("  present in generic but not present in multiple: %s" % not_present_in_multiple)
        print("  present in multiple but not present in generic: %s" % not_present_in_generic)
        print("  item data diff count: %s" % item_data_diff_count)
        print("  more key present in generic spider count: %s" % more_key_count)
        return False, len(multiple_py_out), is_issue_with_trailling_slash
    else:
        print('ALL DATA ARE SAME, READY TO GO :)')
        return True, len(multiple_py_out), False


if __name__ == '__main__':
    clean_rss = 'AbpliveSpider'

    csv_reader = csv.DictReader(open('axis_dev.csv'))
    generic_spider_configs = json.loads(open('generic_spiders.json').read())
    message = get_spider_data(clean_rss, csv_reader)

    settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.80 Safari/537.36",
        "ITEM_PIPELINES": {'__main__.DataStorePipeline': 400}
    }
    # multiple.py spider run
    print('running multiple spider..')
    multiple_py_out = get_crawled_data(getattr(multiple_spider, clean_rss), message, settings)
    # run generic spider
    print('-' * 100)
    print('running generic spider..')
    spider = get_spider(message['clean_rss'], message, generic_spider_configs)
    generic_spider_out = get_crawled_data(spider, message, settings)
    # compare those data
    compare_data(multiple_py_out, generic_spider_out)
