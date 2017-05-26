#!/usr/bin/env python2.7
# -*- coding utf-8 -*-


import scrapy
import re
from scrapy import Selector
from dianping.items import ShopItem

class HuaweiAppSpider(scrapy.Spider):
    name = "HuaweiAppSpider"
    allowed_domains = ["appstore.huawei.com"]
    start_urls = [
        "http://appstore.huawei.com/more/all/1",
        "http://appstore.huawei.com/more/soft/1",
        "http://appstore.huawei.com/more/recommend/1",
        "http://appstore.huawei.com/more/game/1",
        "http://appstore.huawei.com/more/newPo/1",
        "http://appstore.huawei.com/more/newUp/1",
        "http://appstore.huawei.com/search/0/1",
        "http://appstore.huawei.com/search/1/1",
        "http://appstore.huawei.com/search/2/1",
        "http://appstore.huawei.com/search/3/1",
        "http://appstore.huawei.com/search/4/1",
        "http://appstore.huawei.com/search/5/1",
        "http://appstore.huawei.com/search/6/1",
        "http://appstore.huawei.com/search/7/1",
        "http://appstore.huawei.com/search/8/1",
        "http://appstore.huawei.com/search/9/1",
        "http://appstore.huawei.com/search/app/1",
        "http://appstore.huawei.com/search/software/1",
    ]

    def parse(self, response):
        hrefs = response.selector.xpath('.//h4[@class="title"]/a/@href')

        for href in hrefs:
            yield scrapy.Request(href.extract(),callback = self.parse_recommended)
        #next page 
        next_page = self.find_next_page(response.url)
        if next_page:
            url = next_page
            yield scrapy.Request(self.find_next_page(response.url),self.parse)
    
    def find_next_page(self,url):
        try:
            page_num_str = url.split('/')[-1]
            page_num = int(page_num_str) +1;
            url = url[:-len(page_num_str)] + str(page_num)
            return url
        except ValueError:
            print "### page cannot be handled"
            print url
            return "http://google.com"

    '''def parse_recommended(self,respone):
        item = AppstoreItem();

        page = Selector(respone)

        item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
        item['url'] = respone.url
        appid = re.match(r'http://.*/(.*)',item['url']).group(1)
        item['appid'] = appid
        #item['intro'] = page.xpath('//div[@class="content"]/div[@id="app_strdesc"]/text()').extract_first().encode('utf-8')
        #item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
        item['thumbnail'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first();
        divs = page.xpath('//div[@class="open-info"]')

        recommens = ""
        for div in divs:
            url = div.xpath('./p[@class="name"]/a/@href').extract_first().encode('utf-8')
            recommenAppId = re.match(r'http://.*/(.*)',url).group(1)
            recommenTitle = div.xpath('./p[@class="name"]/a/@title').extract_first().encode('utf-8')
            recommens += "{0}:{1},".format(recommenAppId,recommenTitle)

        item['recommended'] = recommens

        yield item'''