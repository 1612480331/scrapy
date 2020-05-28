# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapylearn.bmw.bmw.items import BmwItem


class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    rules = (
        # 若规则中的allow 模式能匹配到 start_urls中的url，那么start_urls中的url也会满足该规则，就也会回调 callback='parse_page'
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/65-.+',
                           deny=r'https://car.autohome.com.cn/pic/series-t.+'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        # print(response.url)
        title = response.xpath("//div[@class='uibox']/div[1]/text()").get().strip()
        urls = response.xpath("//div[@class='uibox']/div[2]/ul/li//img/@src").getall()

        new_urls = []
        # 过滤掉不正确的 url
        for url in urls:
            if url.find("/cardfs/product/") > 0:
                """
                        x.replace("240x180_0_q95_c42_", "") 获取缩略图对应的高清图url
                        response.urljoin() 补全url

                """
                url = response.urljoin(url.replace("240x180_0_q95_c42_", ""))
                new_urls.append(url)

        yield BmwItem(title=title, image_urls=new_urls)

    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
