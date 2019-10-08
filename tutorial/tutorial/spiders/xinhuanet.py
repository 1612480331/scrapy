# -*- coding: utf-8 -*-
import scrapy


class XinhuanetSpider(scrapy.Spider):
    name = 'xinhuanet'
    allowed_domains = ['xinhuanet.com']
    start_urls = ['http://xinhuanet.com/']

    def parse(self, response):
        pass
