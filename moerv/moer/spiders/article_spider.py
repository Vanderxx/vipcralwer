# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector as html_selector
from scrapy.http import Request

from moer.items import ArticleItem
from moer.utils import complete_url, calculate_page, fetch_profit, fetch_article_id


class ArticleSpider(Spider):
    name = 'article'

    def __init__(self, dict_data):
        super(ArticleSpider, self).__init__()
        self.base_url = dict_data['url']
        self.page_num = calculate_page(dict_data['article_num'])
        self.author_id = dict_data['user_id']

    def start_requests(self):
        return [Request(url=self.base_url, callback=self.parse)]

    def parse(self, response):
        selector = html_selector(response)

        article_links = selector.xpath(u'//a[contains(@href, "articleDetails")]/@href').extract()
        for article_link in article_links:
            article_link = complete_url(self.base_url, article_link.encode('utf-8').strip())
            yield Request(url=article_link, callback=self.parse_article)

        for page_index in range(2, self.page_num + 1):
            article_list_url = 'http://moer.jiemian.com/findArticlePageList.htm?theId=%d&returnAuPage=&page=%d&' \
                               'collectType=0' % (self.author_id, page_index)
            yield Request(url=article_list_url, callback=self.parse)

    def parse_article(self, response):
        selector = html_selector(response)
        article_item = ArticleItem()

        article_item['article_id'] = fetch_article_id(response.url)
        article_item['author_id'] = self.author_id
        article_item['article_title'] = selector.select(u'//h2[@class="article-title"]/text()').extract()[0].encode(
            'utf-8').strip()

        purchases = selector.xpath(u'//i[@class="red"]/text()')
        if len(purchases) > 0:
            article_item['purchases'] = int(purchases.extract()[0].encode('utf-8').strip())
        else:
            article_item['purchases'] = 0

        price = selector.xpath('//span[@class="red moerb-icon"/strong/text()')
        if len(price) > 0:
            article_item['article_price'] = price.extract()[0].encode('utf-8')
        else:
            article_item['article_price'] = '0'

        article_item['profit'] = fetch_profit(article_item['article_id'])

        article_item['article_url'] = response.url

        article_item['viewed_num'] = selector.xpath(u'//p[@class="summary-footer"]/span/i[1]/text()').extract()[
            0].encode('utf-8').strip()

        article_item['released_time'] = selector.xpath(u'//p[@class="summary-footer"]/span/i[2]/text()').extract()[
            0].encode('utf-8').strip()

        article_item['praised_num'] = selector.xpath(u'//div[@class="article-handler-box clearfix"]/a/b/text()'
                                                     ).extract()[0].encode('utf-8').strip()

        yield article_item


# if __name__ == '__main__':
    # from twisted.internet import reactor
    #
    # from scrapy.crawler import CrawlerRunner
    # from scrapy.utils.project import get_project_settings
    # from scrapy.utils.log import configure_logging, logger
    #
    # settings = get_project_settings()
    # configure_logging(settings)
    #
    # runner = CrawlerRunner()
    #
    # test_dict = {
    #     'url': 'http://moer.jiemian.com/authorHome.htm?theId=108829243',
    #     'article_num': 182,
    #     'user_id': 108829243
    # }
    # runner.crawl(ArticleSpider, test_dict)
    #
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    #
    # reactor.run()
    # logger.info('All tasks have been finished!')
    # from twisted.internet import reactor
    # from scrapy.crawler import Crawler
    # from scrapy import log, signals
    # from scrapy.utils.project import get_project_settings
    #
    # test_dict = {
    #     'url': 'http://moer.jiemian.com/authorHome.htm?theId=108829243',
    #     'article_num': 182,
    #     'user_id': 108829243
    # }
    # spider = ArticleSpider(test_dict)
    # settings = get_project_settings()
    #
    # crawler = Crawler(settings)
    # crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    # crawler.configure()
    # crawler.crawl(spider)
    # crawler.start()
    # log.start()
    # reactor.run()
