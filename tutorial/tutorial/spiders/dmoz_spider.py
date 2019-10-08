import scrapy
import logging

logger=logging.getLogger(__name__)  #可以使日志打印时，显示当前所在文件名

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.xinhuanet.com/politics/leaders/2019-10/07/c_1125075561.htm"
    ]

    def parse(self, response):
        i = response.xpath("//div[@class='nav']").xpath("//li/text()").extract()
        print(i)

        item = {}
        # from scrapy.tutorial.tutorial.items import DmozItem
        # item = DmozItem()
        # item['title'] = "faf"
        logger.warning(item)
        yield item  #yield 将item发送到pipelines管道
#
# i=response.xpath("//div[@class='nav']").xpath("//li/text()").extract()
# print(i)
# filename = response.url.split("/")[-2] + '.html'
# with open(filename, 'wb') as f:
#     f.write(response.body)
