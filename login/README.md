# Scrapy 实现需要登录简单网站的爬取（以登录人人网为例）
> 有些网站登录时需要验证码等操作，登录思想都差不多，知识逻辑复杂一些
* [scrapy的基本使用参考](https://www.cnblogs.com/yloved/p/12974294.html)
## scrapy 实现人人网登录两种思路
### 1. 使用 Post请求 + 登录需要的数据（用户名、密码等），代码如下
```python
import scrapy

"""
实现登录 方式一
登录信息+post
"""
class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/']

    # 添加账号，密码，模拟post请求,
    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"
        # 账号和密码自己注册
        data = {"email": "人人网登录的账号", "password": "密码"}
        request = scrapy.FormRequest(url, formdata=data, callback=self.parse)
        yield request

    def parse(self, response):
        # 打印出登陆成功后，返回的页面，证明登录成功
        print(response.text)
```

### 2. 手动在浏览器登录好，然后按F12打开开发者控制台，在Network中找到请求中的 cookie字段，
使用 cookie + Get的方式实现登录，代码如下：
```python
import scrapy
import re

"""
实现登录 方式二
手动登录之后返回的cookie+get
"""
class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/972426506/profile']

    # 先收到在浏览器登录，然后将cookie保存下来
    # 添加cookie,自己发送请求,后面的请求会将第一次的cookie传过去
    def start_requests(self):
        cookies = "_r01_=1; ick=673bdfcb-80a0-4abd-9b67-772625ac07e1; anonymid=k1h7k08l-tgsrnq; depovince=SH; JSESSIONID=abcl41_lXglCFcpuViP2w; ick_login=e3f85082-2211-4af0-bce6-9e2a0feded88; t=bc0c3ef07a15e08a88d637fb983f9fcd6; societyguester=bc0c3ef07a15e08a88d637fb983f9fcd6; id=972426506; xnsid=56db8b2b; XNESSESSIONID=55ae25fcfd6a; ver=7.0; loginfrom=null; springskin=set; jebe_key=f2498e28-ac92-4a1c-b4e6-f010cca7ba03%7Cda7cc9f64d73986a7d77b37defa339cc%7C1570500946458%7C1%7C1570500950799; jebe_key=f2498e28-ac92-4a1c-b4e6-f010cca7ba03%7Cda7cc9f64d73986a7d77b37defa339cc%7C1570500946458%7C1%7C1570500950803; vip=1; wp_fold=0; jebecookies=336a9dc0-7ca0-4704-b75d-e0985b5ea448|||||"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        print(response.text)
        # 自动添加第一次请求的cookie
        yield scrapy.Request(
            "http://www.renren.com/972426506/profile?v=info_timeline",
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        print(response.text)

```

## [代码托管地址](https://github.com/1612480331/scrapy/tree/master/login)