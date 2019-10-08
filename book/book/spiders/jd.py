# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import urllib


class JdSpider(scrapy.Spider):
    i = 1
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']/dl/dt")[1:2]
        for dt in dt_list:
            item = {}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:
                item["s_href"] = "https:" + em.xpath("./a/@href").extract_first()
                item["s_name"] = em.xpath("./a/text()").extract_first()
                if item["s_href"] is not None:
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):  # 解析列表页

        item = response.meta["item"]
        li_list = response.xpath("//div[@id='plist']/ul/li")

        for li in li_list:
            # print(li.extract())
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_img"] = "https:" + item["book_img"]
            yield item

        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )
