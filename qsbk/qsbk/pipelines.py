# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
若要激活 pipline ,需要在settings.py中设置 ITEM_PIPELINES
示例如下：
ITEM_PIPELINES = {
   'qsbk.pipelines.QsbkPipeline': 300,
}
"""

"""
将数据保存到json文件中，方式一 
使用 json
"""
# import json
#
#
# class QsbkPipeline:
#     # 当爬虫被打开的时候会调用
#     def open_spider(self, spider):
#         print("爬虫开始执行。。。")
#
#     # 当爬虫有item传过来的时候会调用
#     def process_item(self, item, spider):
#         """
#          对item进行处理操作,例如保存到json文件：
#          with open(filename, 'a',encoding='utf-8') as f:
#             line = json.dumps(dict(item), ensure_ascii=False) + '\n'
#             f.write(line)
#         """
#         fileName = "duanzi.json"
#         # 将item转换为json格式
#         duanzi = json.dumps(dict(item), ensure_ascii=False)
#         with open(fileName, 'a', encoding='utf-8') as f:
#             f.write(duanzi + "\n")
#         return item
#
#     # 当爬虫关闭的时候会调用
#     def close_spider(self, spider):
#         print("爬虫执行结束")
"""
将数据保存到json文件中，方式二
使用 JsonItemExporter,保存结果是满足json格式的列表
缺点是数据量如果太大，会占用内存，因为爬虫执行完之前数据都保存在内存中，最后统一写入到磁盘
"""
# from scrapy.exporters import JsonItemExporter
#
#
# class QsbkPipeline:
#     # 当爬虫被打开的时候会调用
#     def open_spider(self, spider):
#         print("爬虫开始执行。。。")
#         fileName = "duanzi2.json"
#         self.fp = open(fileName, "wb")  # 必须以二进制的形式打开文件
#         self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding="utf-8")
#         self.exporter.start_exporting()
#
#     # 当爬虫有item传过来的时候会调用
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     # 当爬虫关闭的时候会调用
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         print("爬虫执行结束")
"""
将数据保存到json文件中，方式三
使用 JsonLinesItemExporter,一行一行的添加，和 方式一 一样
"""
from scrapy.exporters import JsonLinesItemExporter


class QsbkPipeline:
    # 当爬虫被打开的时候会调用
    def open_spider(self, spider):
        print("爬虫开始执行。。。")
        fileName = "duanzi3.json"
        self.fp = open(fileName, "wb")  # 必须以二进制的形式打开文件
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding="utf-8")

    # 当爬虫有item传过来的时候会调用
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # 当爬虫关闭的时候会调用
    def close_spider(self, spider):
        print("爬虫执行结束")
