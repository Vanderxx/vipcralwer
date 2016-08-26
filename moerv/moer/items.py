# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MoerItem(Item):
    id = Field()
    name = Field()
    type = Field()
    article_num = Field()
    concern_num = Field()
    followers_num = Field()


class ArticleItem(Item):
    author_id = Field()
    article_title = Field()
    article_id = Field()
    purchases = Field()
    profit = Field()
    viewed_num = Field()
    praised_num = Field()
    released_time = Field()
    article_url = Field()
    article_price = Field()
