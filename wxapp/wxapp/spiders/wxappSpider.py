# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapylearn.wxapp.wxapp.items import WxappItem


class WxappspiderSpider(CrawlSpider):
    name = 'wxappSpider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    """
    allow=r'Items/': 满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配。
    callback="": 指定规则解析器解析数据的规则（回调函数）
    follow：是一个布尔值(boolean),制定了根据该规则从response提取的链接是否需要跟进。
           若为True:需要在当前规则提取的链接请求后，返回的response中继续提取链接
           若为False：不需要在当前规则提取的链接请求后，返回的response中继续提取链接
           如果callback为None，follow默认设置为True，否则默认为Flase
    """
    rules = (
        # 该规则只负责提取链接，需要跟进，不负责解析数据，所以不需要callback
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d+'), follow=True),
        # 该规则中 \. 是将正则中的 . 进行转义，原样匹配
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").get().strip()
        author_p = response.xpath("//p[@class='authors']")
        author = author_p.xpath("./a/text()").get().strip()
        time = author_p.xpath("./span/text()").get().strip()
        content = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(content).strip()
        item = WxappItem(title=title, author=author, time=time, content=content)
        yield item

    # 默认生成的，没使用到
    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
