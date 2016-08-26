#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging, logger

from spiders.moer_spider import MoerSpider
from spiders.vip_comment_spider import VipCommentSpider

from utils import import_history

session_explaination = object()
vip_comment = object()

entry_type = {
    session_explaination: MoerSpider,
    vip_comment: VipCommentSpider
}

if __name__ == '__main__':

    # configure logger
    settings = get_project_settings()
    configure_logging(settings)

    # filter duplicated moerv users
    # if the crawling history exists, import them
    user_set = set()
    import_history(user_set)

    # generate a crawler process to manager spiders with default settings
    # customize some settings
    runner = CrawlerProcess()
    runner.settings.set(
        'ITEM_PIPELINES', {'moer.pipelines.MoerStorePipeline': 200,
                           'moer.pipelines.ArticleStorePipeline': 300}
    )

    # choose special spider from different crawl entries
    special_spider = entry_type[vip_comment]
    runner.crawl(special_spider, runner, user_set)

    # generate a deffer as all crawling tasks have been finished
    # trigger a signal to notice reactor for stop
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
    logger.info('All tasks have been finished!')
