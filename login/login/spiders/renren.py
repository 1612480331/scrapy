# -*- coding: utf-8 -*-
import scrapy
import re


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/972426506/profile']

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
        print(re.findall("杨露生", response.body.decode()))
        yield scrapy.Request(
            "http://www.renren.com/972426506/profile?v=info_timeline",
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        print(re.findall("杨露生", response.body.decode()))
