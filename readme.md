# python3.8 安装scrapy及其使用 ，爬取糗事百科小案例
> **yls**  *2020/5/27*
## 安装scrapy之前，先安装 twisted，否则会报错

1. 在 https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted 中下载与python对应版本的 Twisted   
,cp38对应py3.8，自行选择32 or 64位。
2. 找到下载好后的Twisted文件地址，在cmd运行命令 pip install 文件位置  
例如：pip install C:\Users\name\Downloads\Twisted-18.7.0-cp37-cp37m-win_amd64.whl   
若安装时报错如下：
D:\python>pip3 install Twisted-20.3.0-cp38-cp38-win_amd64.whl
ERROR: Twisted-20.3.0-cp38-cp38-win_amd64.whl is not a supported wheel on this platform.    
则 修改文件名为 Twisted-20.3.0-cp38-cp38-win32.whl 后，重新安装



## 安装 scrapy
```
# pip默认国外的源文件 http://mirrors.aliyun.com/pypi/simple/ 使用国内源
1. pip3 --default-timeout=100 install Scrapy -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

## 创建项目实例
```
scrapy startproject [项目的名字]

例如：scrapy startproject tencent
```
## 创建爬虫
```
进入项目根目录 cd tencent
创建爬虫  scrapy genspider [爬虫的名字] [爬虫的域名]
例如：scrapy genspider example example.com
注意：爬虫的名字不能和项目的名字相同
```
## 运行一个爬虫
```
1. 直接在命令行运行
scrapy crawl [爬虫名]
2. 写一个py脚本，直接运行脚本即可
from scrapy import cmdline

cmdline.execute(["scrapy", "crawl", "爬虫名"])
```
## 运行爬虫前，一般需要在 settings.py 中设置 USER_AGENT 和 Obey robots.txt rules
```
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

ROBOTSTXT_OBEY = False
```
## 使用日志
```python
import logging

logger=logging.getLogger(__name__)  #可以使日志打印时，显示当前所在文件名

logger.warning(item)  #示例
```

## 爬虫中打印日志的方式，在settings.py中设置日志级别和日志文件
```python
LOG_LEVEL="WARNING"
LOG_FILE="./log.log" #日志保存文件，设置以后，终端不会显示日志记录
```

## 在settings.py中开启管道
```python
ITEM_PIPELINES = {
   'tutorial.pipelines.TutorialPipeline': 300,    #300表示优先级，数字越小越优先

   'tutorial.pipelines.TutorialPipeline1': 301,  # 300表示优先级，数字越小越优先

}
```

## scrapy案例一
> 爬取糗事百科网站中的段子   
> 数据包括：作者，段子内容，发布的时间   
> 根据上面的介绍创建爬虫即可
### 1. 定义 items.py
```python
import scrapy

"""
定义要爬取的数据字段,就可以不使用字典了
"""


class QsbkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapylearn.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()

```
### 2. 在settings.py中添加配置
```python
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 激活通道
ITEM_PIPELINES = {
   'qsbk.pipelines.QsbkPipeline': 300,
}
```
### 3. 编辑 piplines.py ,保存爬取数据结果到json文件中，有三种方式
```python
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
使用 JsonLinesItemExporter,一行一行的添加，和 方式一效果 一样
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

```

### 4. 编辑爬虫逻辑
```python
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

```

## 5. [代码托管地址：https://github.com/1612480331/scrapy/tree/master/qsbk](https://github.com/1612480331/scrapy/tree/master/qsbk)