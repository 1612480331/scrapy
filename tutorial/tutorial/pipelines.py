# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# 使用pipelines,首先要在settings中配置开启
# 进入管道的item，会按照优先级经过每一个管道

class TutorialPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        item['a'] = "fadf"
        return item       # 必须有return 才能把值传入下一个管道


class TutorialPipeline1(object):
    def process_item(self, item, spider):
        print(item)
        return item
