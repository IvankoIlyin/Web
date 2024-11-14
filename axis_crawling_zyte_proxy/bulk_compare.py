import json
import csv
import os
import io
import sys


from compare_test import get_spider_data, get_crawled_data, get_spider, compare_data
import multiple as multiple_spider


def get_compare_test(clean_rss, csv_reader, generic_spider_configs):
    message = get_spider_data(clean_rss, csv_reader)
    settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.80 Safari/537.36",
        "ITEM_PIPELINES": {'__main__.DataStorePipeline': 400}
    }
    # multiple.py spider run
    multiple_py_out = get_crawled_data(getattr(multiple_spider, clean_rss), message, settings)
    # run generic spider
    spider = get_spider(message['clean_rss'], message, generic_spider_configs)
    generic_spider_out = get_crawled_data(spider, message, settings)
    # compare those data
    out = io.StringIO()
    sys.stdout = out
    result, item_crawl_count, is_issue_with_trailling_slash = compare_data(multiple_py_out, generic_spider_out)
    sys.stdout = sys.__stdout__
    compare_log = out.getvalue()
    return result, item_crawl_count, compare_log, is_issue_with_trailling_slash


if __name__ == '__main__':
    if not os.path.exists('compare_log'):
        os.mkdir('compare_log')

    generic_spider_configs = json.loads(open('generic_spiders_US_Dept_multi_countries_Ivan_0611.json').read())
    try:
        tested_spiders = json.loads(open('compare_log/00_tested_spiders.json').read())
    except:
        tested_spiders = {}

    clean_rss_list = list(generic_spider_configs.keys())
    spider_stats = []
    count = 0
    for clean_rss in clean_rss_list:
        if clean_rss in tested_spiders:
            print('already tested: %s' % clean_rss)
            continue
        csv_reader = csv.DictReader(open('axis_dev_US_Dept_multi_countries_Ivan_0611.csv'))
        print('%s ==> %s' % (clean_rss, count))
        count += 1
        try:
            result, item_crawl_count, compare_log, is_issue_with_trailling_slash = get_compare_test(clean_rss, csv_reader, generic_spider_configs)
        except Exception as e:
            print(e)
            continue
        if is_issue_with_trailling_slash and not result:
            spider_stats.append({'spider': clean_rss, 'item_crawled': item_crawl_count, 'is_same': result,
                                 'is_issue_with_trailling_slash': is_issue_with_trailling_slash})
        else:
            spider_stats.append({'spider': clean_rss, 'item_crawled': item_crawl_count, 'is_same': result})
        if not result:
            if compare_log:
                with open('compare_log/%s.log' % clean_rss, 'w') as fout:
                    fout.write(compare_log)
        tested_spiders[clean_rss] = {'count': item_crawl_count, 'is_same': result}
        if is_issue_with_trailling_slash and not result:
            tested_spiders[clean_rss]['is_issue_with_trailling_slash_or_http'] = is_issue_with_trailling_slash
        with open('compare_log/00_tested_spiders.json', 'w') as fout:
            fout.write(json.dumps(tested_spiders))

