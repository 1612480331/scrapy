# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
定义要爬取的数据字段,就可以不使用字典了
"""


class QsbkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapylearn.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
