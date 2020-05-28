# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os

from scrapy.pipelines.images import ImagesPipeline
from scrapylearn.bmw.bmw import settings


class BmwPipeline:
    def process_item(self, item, spider):
        return item


"""
由于默认的imagepipeline会将所有图片放到一个文件夹，源码如下：
    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s.jpg' % (image_guid)
我们需要类型不同的文件对应不同的文件夹
所以需要重写imagepipeline
"""


class BmwImagePipeline(ImagesPipeline):
    """
    该方法在发送下载请求之前调用
    其实这个方法本身就是去下载请求
    该方法有参数 item ，通过重写该方法，可以将item中的字段数据添加到 request中进行传递
    """

    def get_media_requests(self, item, info):
        request_objs = super().get_media_requests(item, info)
        # 重写时，在父类方法返回的Requeset列表中的每一个Request中加入item,以便传递数据信息
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs
        # return [Request(x) for x in item.get(self.images_urls_field, [])]

    """
    该方法在图片将要被存储的时候调用，来获取这个图片存储的路径
    """

    def file_path(self, request, response=None, info=None):
        path = super().file_path(request, response, info)
        # 重写 get_media_requests 方法对request添加了 item,所以这里可以从request中体取title数据
        title = request.item["title"]
        # 获取图片存储的总文件夹
        image_store = settings.IMAGES_STORE
        # 根据title获取当前分类图片存储的子文件夹
        title_path = os.path.join(image_store, title)
        # 不存在则创建
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        # 将父类ImagesPipeline默认的全部文件的存储文件夹full删掉
        image_path = os.path.join(title_path, path.replace("full/", ""))
        print(image_path)
        return image_path

        # image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        # return 'full/%s.jpg' % (image_guid)
