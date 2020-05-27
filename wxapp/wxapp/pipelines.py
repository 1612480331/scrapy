# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter


class WxappPipeline:
    # 当爬虫被打开的时候会调用
    def open_spider(self, spider):
        print("爬虫开始执行。。。")
        fileName = "article.json"
        self.fp = open(fileName, "wb")  # 必须以二进制的形式打开文件
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding="utf-8")

    # 当爬虫有item传过来的时候会调用
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # 当爬虫关闭的时候会调用
    def close_spider(self, spider):
        print("爬虫执行结束")
