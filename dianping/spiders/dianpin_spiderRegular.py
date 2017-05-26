# -*- coding:utf-8 -*-
from scrapy.spider import BaseSpider
from urlparse import urlparse
from scrapy.http import Request 
import urllib
import sys
import time
import scrapy
import time
import re
from dianping.items import ShopItem


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

#from scrapy import optional_features
#optional_features.remove('boto')

reload(sys)
sys.setdefaultencoding('utf-8') 

#from dianping.items import *

def match(reU, s):
    if re.match(reU, s):
        return True
    else:
        return False


class DianpingSpiderR(BaseSpider):
    name = "dianpingR"
    allowed_domains = ["dianping.com"]

    
    start_urls = [
        "http://www.dianping.com/shanghai",
        "http://www.dianping.com/shanghai/life",
        "http://www.dianping.com/shanghai/wedding",
        "http://www.dianping.com/shanghai/food",
        "http://www.dianping.com/shanghai/movie",
        "http://www.dianping.com/shanghai/hotel", 
        "http://www.dianping.com/shanghai/beauty",
        "http://www.dianping.com/shanghai/sports",
          ]

    '''rules = [
        Rule(sle(allow=("http://www.dianping.com/search/category/1/30/g135*")), callback='parse', follow=True),
        #Rule(sle(allow=("/topsites/category/Top$", )), callback='parse_category_top', follow=True),
    ]'''

    
    
    def start_requests(self):
        self.base_url = "http://www.dianping.com"
        self.shop_base_url = "http://www.dianping.com"
        self.urlUProcessed = {}
        self.urlProcessed = {}
        self.url_can = {}
        self.shop_rule = "/shop/[0-9]+$"
        #self.region_rule = "/search/category/1/*"
        self.region_rule = "/search/category/1/[0-9]+/r[0-9]+$"
        self.region_rule1 = "/search/category/1/[0-9]+/r[0-9]+p"
        self.category_rule = "/shanghai/[a-z]+$"
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_region)
        '''while(len(self.urlUProcessed)>0):
            for url in self.urlProcessed:
                yield scrapy.Request(url=url, callback=self.parse) 
            time.sleep(120)'''
        

    def parse_region(self, response):
        #print 'parsessssssssssssssssssssssssssssssssssssssssssssssss'  
        #self.urlProcessed[response.url] = 1
        #self.urlUProcessed.pop(response.url)
        self.url_can[response.url] = 1
        newurls = response.xpath('//a/@href').extract()
        #print newurls
        for url in newurls:
        	if match(self.shop_rule,url):
        		if not self.url_can.has_key(self.base_url+url):
        			yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop1) 
        	if match(self.category_rule,url):
        		if not self.url_can.has_key(self.base_url+url):
        			yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
        	if match(self.region_rule,url) or match(self.region_rule1,url):
				if not self.url_can.has_key(self.base_url+url):
					#time.sleep(0.5)
					#self.url_can[url] = 1
					yield scrapy.Request(url=self.base_url+url, callback=self.parse_region)  
               

    def parse_shop(self, response):
        name = response.xpath('//*[@id="basic-info"]/h1/text()').extract()
        rating = response.xpath('//*[@id="basic-info"]/div[1]/span[1]/@title').extract()
        kouwei = response.xpath('//*[@id="comment_score"]/span[1]/text()').extract()
        huanjing = response.xpath('//*[@id="comment_score"]/span[2]/text()').extract()
        fuwu = response.xpath('//*[@id="comment_score"]/span[3]/text()').extract()
        price = response.xpath('//*[@id="avgPriceTitle"]/text()').extract()
        tag = response.xpath('//*[@id="body"]/div[2]/div[1]/a[3]/text()').extract()
        comNum = response.xpath('//*[@id="reviewCount"]/text()').extract() 
        address =  response.xpath('//*[@id="basic-info"]/div[2]/span[2]/text()').extract()    # address
        tel = response.xpath('//*[@id="basic-info"]/p/span[2]/text()').extract()
        des = response.xpath('//*[@id="shop-tabs"]/div[5]/div[2]/p[2]/text()').extract()
        lonlat = response.xpath('//*[@id="map"]/img/@src').extract()
        #lonlat = response.xpath('//*[@id="aside-bottom"]/div[1]/div').extract()
        #print (response.body)
        #print('name', name)

        outPage = open('shopPage/'+response.url.split('/')[-1],'w')
        outPage.write(response.body)
        outPage.close()

        script  = response.xpath('//script/text()').extract()
        #print script
        for s in script:
            if "window.shop_config" in s:
                shopInfo = open('shopLoc/'+response.url.split('/')[-1],'w')
                shopInfo.write(s)

        out = open('test123.txt','a+')
        i=0
        out.write(name[i].strip())        
        out.write(',')
        out.write(tag[i].strip())
        out.write(',')             
        out.write(rating[i])
        out.write(',')
        out.write(comNum[i])
        out.write(',')
        out.write(price[i])
        out.write(',')
        out.write(kouwei[i])
        out.write(',')
        out.write(huanjing[i])
        out.write(',')
        out.write(fuwu[i])
        out.write(',')
        out.write(str(tel[i]))
        out.write(',')
        out.write(address[i].replace('\n',''))
        #out.write(',')
        #out.write(str(len(lonlat)))
        #out.write(',')
        #out.write(str(len(des)))
        out.write('\n')
        out.close()
        if(len(lonlat)>0):
            desOut = open('./des/'+name[0].strip()+'.txt','w')
            desOut.write(lonlat[0])
            desOut.write('\n\n')
            desOut.write(des[0])
            desOut.close()


    def parse_shop1(self, response):
        name = response.xpath('//*[@id="basic-info"]/h1/text()').extract()
        rating = response.xpath('//*[@id="basic-info"]/div[1]/span[1]/@title').extract()
        taste = response.xpath('//*[@id="comment_score"]/span[1]/text()').extract()
        environment = response.xpath('//*[@id="comment_score"]/span[2]/text()').extract()
        service = response.xpath('//*[@id="comment_score"]/span[3]/text()').extract()
        price = response.xpath('//*[@id="avgPriceTitle"]/text()').extract()
        tag = response.xpath('//*[@id="body"]/div[2]/div[1]/a[3]/text()').extract()
        comNum = response.xpath('//*[@id="reviewCount"]/text()').extract() 
        address =  response.xpath('//*[@id="basic-info"]/div[2]/span[2]/text()').extract()    # address
        tel = response.xpath('//*[@id="basic-info"]/p/span[2]/text()').extract()
        #des = response.xpath('//*[@id="shop-tabs"]/div[5]/div[2]/p[2]/text()').extract()
        #lonlat = response.xpath('//*[@id="map"]/img/@src').extract()
        script  = response.xpath('//script/text()').extract()

        shopPage = open('shopPage/'+response.url.split('/')[-1],'w')
        shopPage.write(response.body)

        # shop location Information
        for s in script:
            if "window.shop_config" in s:
                shopInfo = open('shopLoc/'+response.url.split('/')[-1],'w')
                shopInfo.write(s)
        # shop information
        item = ShopItem();
        item['shopId'] = response.url.split('/')[-1]
        if len(name)>0:
            item['shopName'] = name[0].strip()
        else:
            item['shopName'] = 'NULL'
        if len(rating)>0:
            item['rating'] = rating[0]
        else:
            item['rating'] = 'NULL'
        if len(taste)>0:
            item['taste'] = taste[0]
        else:
            item['taste']  = 'NULL'
        if len(environment)>0:
            item['environment'] = environment[0]
        else:
            item['environment'] = 'NULL'
        if len(service)>0:
            item['service'] = service[0]
        else:
            item['service'] = 'NULL'
        if len(tag)>0:
            item['tag'] = tag[0].replace('\\n','').strip ()
        else:
            item['tag'] = 'NULL'
        if len(comNum)>0:
            item['comNum'] = comNum[0]
        else:
            item['comNum'] = 'NULL'
        if len(address)>0:
            item['address'] = address[0].replace('\\n','').strip ()
        else:
            item['address'] = 'NULL'
        if len(tel)>0:
            item['tel'] = tel[0]
        else:
            item['tel'] = 'NULL'
        
        yield item
