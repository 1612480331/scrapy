# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BmwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 图片的类型
    # imagesPipeline 底层会自动从 image_urls 字段获取图片请求链接
    image_urls = scrapy.Field()
    images = scrapy.Field()
