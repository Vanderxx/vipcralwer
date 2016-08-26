# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector as html_selector
from scrapy.http import Request

from moer.items import MoerItem
from moer.utils import simple_post
from article_spider import ArticleSpider


class VipCommentSpider(Spider):
    name = 'vip_comment'

    def __init__(self, runner, user_set):
        super(VipCommentSpider, self).__init__()
        self.base_url = 'http://moer.jiemian.com/dp/ajax/briefList.htm?from=1'
        self.runner = runner
        self.user_set = user_set
        self.min_index = 999999

    def start_requests(self):
        return [Request(url=self.base_url, callback=self.parse)]

    def parse(self, response):
        selector = html_selector(response)
        user_list = selector.xpath('//li[@class="clearfix"]')

        for user in user_list:
            # yield request for crawling the user info
            user_home_link = user.xpath('div/a/@href').extract()[0].encode('utf-8')
            user_id = user_home_link[-9:]
            if user_id not in self.user_set:
                self.user_set.add(user_id)
                yield Request(url=user_home_link, callback=self.parse_person)

            # yield request for next page
            data_id = int(user.xpath('@data-id').extract()[0].encode('utf-8'))
            if data_id < self.min_index:
                self.min_index = data_id

        # if min index is less than 5600, the response would be null
        if self.min_index > 5600:
            next_page_link = 'http://moer.jiemian.com/dp/ajax/briefList.htm?start=%d&from=1&' \
                             'long_short=0' % self.min_index
            yield Request(url=next_page_link, callback=self.parse)

    def parse_person(self, response):
        person_item = MoerItem()
        selector = html_selector(response)

        person_item['name'] = selector.xpath('//div[@class="author-msg"]/h4/span/text()').extract()[0].encode(
            'utf-8').strip()
        person_item['id'] = int(response.url[-9:])

        if len(selector.xpath('//i[@class="moerv-red"]').extract()) > 0:
            person_item['type'] = 1
        else:
            person_item['type'] = 0

        person_item['concern_num'] = simple_post('concern', person_item['id'])
        person_item['followers_num'] = simple_post('follower', person_item['id'])

        extracted_article_num = selector.xpath(u'//input[@id="totalNum"]/@value').extract()[0]
        person_item['article_num'] = int(extracted_article_num.encode('utf-8').strip())

        data_dict = {
            'url': response.url,
            'article_num': person_item['article_num'],
            'user_id': person_item['id']
        }
        self.runner.crawl(ArticleSpider, data_dict)

        yield person_item

# if __name__ == '__main__':
#     from twisted.internet import reactor
#
#     from scrapy.crawler import CrawlerProcess
#     from scrapy.utils.project import get_project_settings
#     from scrapy.utils.log import configure_logging, logger
#
#     from moer_spider import MoerSpider
#
#     from moer.utils import import_history
#
#     session_explaination = object()
#     vip_comment = object()
#
#     entry_type = {
#         session_explaination: MoerSpider,
#         vip_comment: VipCommentSpider
#     }
#
#     settings = get_project_settings()
#     configure_logging(settings)
#
#     user_set = set()
#     import_history(user_set)
#
#     runner = CrawlerProcess()
#     special_spider = entry_type[vip_comment]
#     runner.crawl(special_spider, runner, user_set)
#
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#
#     reactor.run()
#     logger.info('All tasks have been finished!')
