# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapylearn.qsbk.qsbk.items import QsbkItem


class QsbkspiderSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'qsbkSpider'
    # 爬虫允许的域名，限制爬虫的范围，不属于该域名的网址，就不会去爬取
    allowed_domains = ['qiushibaike.com']
    # 开始爬虫的网址
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    # 自定义变量，为爬取多页面提供url的前一部分
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        # print("=" * 40)
        # # 打印出response的类型
        # print(type(response))
        # print("=" * 40)
        duanzidivs = response.xpath("//div[@class='col1 old-style-col1']/div")
        for duanzi in duanzidivs:
            author = duanzi.xpath(".//h2/text()").extract_first().strip()  # extract = getall ，extract_first = get
            content = duanzi.xpath(".//div[@class='content']/span/text()").getall()
            # 使用items代替字典
            # item = {"author": author, "content": content}
            item = QsbkItem(author=author, content=content)
            infoUrl = self.base_domain + duanzi.xpath("./a[1]/@href").get()
            # 可以将已经解析好的数据传递到下一个解析，使用深拷贝，否则下一个for循环中的值会改变上一个item的值
            yield scrapy.Request(infoUrl, callback=self.parseTime, meta={"item": deepcopy(item)})

        # 下一页标签中的 url
        nextUrl = self.base_domain + response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not nextUrl:
            return
        else:
            yield scrapy.Request(nextUrl, callback=self.parse)

    # 在段子的全部信息页面解析该段子发布的时间
    def parseTime(self, response):
        # 接收上一个解析函数传递的数据
        item = response.meta["item"]
        time = response.xpath("//span[@class='stats-time']/text()").get().strip()
        item["time"] = time
        # yield 是将item一个一个的返回，也可以将item 存储到一个列表[]中，最后使用return 全部返回
        yield item
