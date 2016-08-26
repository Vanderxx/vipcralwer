# -*- coding: utf-8 -*-

import os


class MoerStorePipeline(object):
    """
    Store moer user
    """

    def __init__(self):
        if not os.path.exists('MoerV.txt'):
            os.mknod('MoerV.txt')
        self.fd = open('MoerV.txt', 'a+')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.fd.close()

    def process_item(self, item, spider):
        if spider.name == 'moer'or spider.name == 'vip_comment':
            self.fd.write(item['name'] + '\t\t')
            self.fd.write(str(item['id']) + '\t\t')
            self.fd.write(str(item['type']) + '\t\t')
            self.fd.write(str(item['concern_num']) + '\t\t')
            self.fd.write(str(item['followers_num']) + '\t\t')
            self.fd.write(str(item['article_num']))
            self.fd.write('\n')
        return item


class ArticleStorePipeline(object):
    """
    Store article info
    """

    def __init__(self):
        if not os.path.exists('ArticleInfo.txt'):
            os.mknod('ArticleInfo.txt')

        self.fd = open('ArticleInfo.txt', 'a+')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.fd.close()

    def process_item(self, item, spider):
        if spider.name == 'article':
            self.fd.write(str(item['author_id']) + '\t\t')
            self.fd.write(str(item['article_id']) + '\t\t')
            self.fd.write(str(item['article_title']) + '\t\t')
            self.fd.write(str(item['purchases']) + '\t\t')
            self.fd.write(str(item['profit']) + '\t\t')
            self.fd.write(str(item['viewed_num']) + '\t\t')
            self.fd.write(str(item['released_time']) + '\t\t')
            self.fd.write(str(item['praised_num']) + '\t\t')
            self.fd.write(str(item['article_url']) + '\t\t')
            self.fd.write(item['article_price'])
            self.fd.write('\n')
        return item
