## 安装 scrapy
```python
1. pip3 --default-timeout=100 install Scrapy
```

## 创建项目实例
```angular2
scrapy startproject tencent
```
## 创建爬虫
```angular2
    cd tencent
    scrapy genspider example example.com

```
## 运行一个爬虫
```
scrapy crawl [爬虫名]
```

## 使用日志
```python
import logging

logger=logging.getLogger(__name__)  #可以使日志打印时，显示当前所在文件名

logger.warning(item)  #示例
```

## 在settings.py中设置日志级别和日志文件
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