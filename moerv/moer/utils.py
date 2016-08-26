# -*- coding: utf-8 -*-

from scrapy.utils.log import logger
from urlparse import urljoin
from urllib2 import urlopen, Request
from urllib import urlencode
import json
import re
from os import path

request_type = {
    'follower': 'http://moer.jiemian.com/wapcommon_findMyFansCount.json',
    'concern': 'http://moer.jiemian.com/wapcommon_findMyAttentionsCount.json'
}


def complete_url(start_url, extracted_url):
    return urljoin(start_url, extracted_url)


def simple_post(req_type, user_id):
    url = request_type[req_type]
    post_data = {
        'userId': user_id,
    }
    post_data = urlencode(post_data)
    req = Request(url, post_data)
    html = urlopen(req).read()
    return int(json.loads(html)['data']['count'])


def calculate_page(num):
    if num < 0:
        return None
    else:
        remainder = num % 10
        base_num = num / 10
        if remainder > 0:
            return base_num + 1
        else:
            return base_num


def fetch_profit(article_id):
    url = 'http://moer.jiemian.com/findArticleStockInfo.htm?articleId=%d' % article_id
    try:
        response = urlopen(url).read()
    except Exception as e:
        logger.debug(str(e))
        return '0'

    pattern = re.compile(r"-?[0-9]*(\.*\d*)%")
    match = pattern.search(response)
    if match:
        return match.group(0)
    else:
        return '0'


def fetch_article_id(url):
    pattern = re.compile(r"[0-9]\d*")
    match = pattern.search(url)
    return int(match.group(0))


def import_history(history_set):
    if path.exists('history.txt'):
        with open('history.txt', 'r') as f:
            for each_line in f:
                lists = each_line.split('\t\t')
                history_set.add(lists[1])


if __name__ == '__main__':
    test_set = set()
    import_history(test_set)
    print test_set
