# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class roomItem(scrapy.Item):

    source = scrapy.Field()
    cate = scrapy.Field()
    room = scrapy.Field()
    nickname = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    viewers_num = scrapy.Field()
    parent_cate_name = scrapy.Field()
