# Crawl Spider 汽车之家中宝马5系全部图片
> **yls**  *2020/5/28*
需要使用 `LinkExtractor` `Rule`来决定爬虫的具体走向

* [Crawl Spider介绍](http://www.imooc.com/article/37268)
## scrapy 爬取文件或者图片简介
### *. 为什么选择使用scrapy内置的下载文件的方法：
```
1. 避免重新下载最近已经下载过的数据
2. 可以方便的指定问及那存储的路径
3. 可以将下载的图片转换为通用的格式，比如png或jpg
4. 可以方便的生成缩略图
5. 可以方便的检测图片的宽高，确保他们的满足最小限制
6. 一部下载，效率高
```
### *. 下载文件的 Files Pipline：
```
使用 Files Pipeline 下载文件时，按以下步骤完成
1. 定义好一个 Item,在这个Item中定义两个属性，分别为 file_urls和files。file_urls用来存储需要下载的文件的链接，需要给一个链表
2. 文件下载完成后，会把下载的相关信息存储到item的files属性中。比如下载路径，下载的url和文件的校验码等
3. 在settings.py中配置FILES_STORE,这个配置用来设置文件下载后在本地存储的路径
4. 启动pipeline:在ITEM_PIPELINES中设置scrapy.pipeline.files.FilesPipeline:1。若根据自身业务可以重写 FilesPipeline
重写时也要在ITEM_PIPELINES中设置激活
```
### *. 下载文件的 Images Pipline：
```
使用 Images Pipeline 下载文件时，按以下步骤完成
1. 定义好一个 Item,在这个Item中定义两个属性，分别为 image_urls和images。
image_urls用来存储需要下载的图片的链接，需要给一个链表
2. 文件下载完成后，会把下载的相关信息存储到item的images属性中。
比如下载路径，下载的url和图片的校验码等
3. 在settings.py中配置IMAGEAS_STORE,这个配置用来设置图片下载后在本地存储的路径
4. 启动pipeline:在ITEM_PIPELINES中设置scrapy.pipeline.images.ImagesPipeline:1。若根据自身业务可以重写 FilesPipeline
重写时也要在ITEM_PIPELINES中设置激活
```

## 1. 创建项目
```
scrapy startproject bmw
```
## 2. 创建爬虫
```
cd bmw
scrapy genspider bmw5 -t crawl "car.autohome.com.cn"
```
## 3. 编辑需要爬取的数据字段 items.py
```python
import scrapy


class BmwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 图片的类型
    # imagesPipeline 底层会自动从 image_urls 字段获取图片请求链接
    image_urls = scrapy.Field()
    images = scrapy.Field()
```

## 4. 根据图片分类业务，重写 ImagesPipeline 类
```python
import os

from scrapy.pipelines.images import ImagesPipeline
from scrapylearn.bmw.bmw import settings

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
```
## 5. 在settings.py中激活管道,添加图片存储路径
```
ITEM_PIPELINES = {
    # 'bmw.pipelines.BmwPipeline': 300,
    'bmw.pipelines.BmwImagePipeline': 300,
}
# 图片下载的路径，供images pipeline 使用
IMAGES_STORE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
```

## 6. 编写爬虫 bmw5.py
```python
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
```

## 7. 在项目根目录下，运行爬虫
```
#scrapy crawl [爬虫名]
scrapy crawl bmw5
```

## 8. [代码托管地址:https://github.com/1612480331/scrapy/tree/master/bmw](https://github.com/1612480331/scrapy/tree/master/bmw)
