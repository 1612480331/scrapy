# -*- coding: utf-8 -*-
import scrapy


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.usst.edu.cn']

    def parse(self, response):
        i=1
        i = i + 1
        input(i)
        # print(response.body)


        li_list = response.xpath("//ul[@class='wp-menu clearfix'][1]/li/a/text()").extract()
        for li in li_list:

            item = {}
            item['url']=response.url
            item['name'] = li
            yield item

        next_url=response.xpath("//ul[@class='wp-menu clearfix']/li[@class='menu-item i3']/a/@href").extract_first()
        next_url='http://www.usst.edu.cn'+next_url
        print (next_url)
        yield scrapy.Request(next_url,callback=self.parse1)
    def parse1(self, response):
        i=1
        i = i + 1
        input(i)
        # print(response.body)


        li_list = response.xpath("//ul[@class='wp-menu clearfix'][1]/li/a/text()").extract()
        for li in li_list:

            item = {}
            item['url']=response.url
            item['name'] = li
            yield item