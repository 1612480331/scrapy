# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json, os


class BookPipeline(object):
    i = 1

    def process_item(self, item, spider):
        base_dir = os.getcwd()

        filename = base_dir + '/news.json'
        # 打开json文件，向里面以dumps的方式吸入数据
        # 注意需要有一个参数ensure_ascii=False ，不然数据会直接为utf编码的方式存入比如
        # :“/xe15”

        with open(filename, 'a',encoding='utf-8') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'

            f.write(line)

        return item
