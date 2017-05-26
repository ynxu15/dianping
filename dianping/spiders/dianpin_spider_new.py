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


class DianpingSpiderNew(BaseSpider):
    name = "dianpingnew"
    allowed_domains = ["dianping.com"]
    
    start_urls = [
        "http://www.dianping.com/shanghai",
        "http://www.dianping.com/shanghai/life",
        "http://www.dianping.com/shanghai/wedding"
    ]

    rules = [
        Rule(sle(allow=("http://www.dianping.com/search/category/1/30/g135*")), callback='parse', follow=True),
        #Rule(sle(allow=("/topsites/category/Top$", )), callback='parse_category_top', follow=True),
    ]

    
    
    def start_requests(self):
    	#print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
        self.base_url = "http://www.dianping.com"
        self.shop_base_url = "http://www.dianping.com"
        self.url_can = []
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': "your agent string"}, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            }) 

    def parse(self, response):
    	#print 'parsessssssssssssssssssssssssssssssssssssssssssssssss'  
    	newurls = response.xpath('//a/@href').extract()
    	#print newurls
    	urlRule = "/search/category/1/30/*"
    	#print response.xpath('//*[@id="index-nav"]/li[2]/div/div/div/a[1]')
    	for url in newurls:
    		if match(urlRule,url):
    			time.sleep(1)
    			#print url
    			if not url in self.url_can:
    				self.url_can.append(url)
    				yield scrapy.Request(url=self.base_url+url, callback=self.parse1, headers={'User-Agent': "your agent string"}, meta={
				    'splash': {
				    'endpoint': 'render.html',
				    'args': {'wait': 0.5}
				    }
				}) 
				for p in range(2,51):
					time.sleep(1)
					yield scrapy.Request(url=self.base_url+url+'p'+str(p), callback=self.parse1, headers={'User-Agent': "your agent string"}, meta={
				        'splash': {
				        'endpoint': 'render.html',
                        		'args': {'wait': 0.5}
                        		}                    		
				    })          

                    
    def parse11(self, response):
        urls = response.xpath('//*[@id="J_nc_business"]/div[2]/div[1]/dl/dd/ul/li/a/@href').extract() 
        
        for url in urls:
            time.sleep(1)
            yield scrapy.Request(url=self.base_url+url, callback=self.parse1, headers={'User-Agent': "your agent string"}, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            }) 
        for url in urls:
            time.sleep(1)
            for p in range(2,51):
                yield scrapy.Request(url=self.base_url+url+'p'+str(p), callback=self.parse1, headers={'User-Agent': "your agent string"}, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': 0.5}
                    }
                })                 
        

    def parse1(self, response):
        shop_urls = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href').extract()
        for url in shop_urls:
            time.sleep(0.1)
            yield scrapy.Request(url=self.base_url+url, callback=self.parse3, headers={'User-Agent': "your agent"},meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })


       
    
    def parse2(self, response):
        time.sleep(2)
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
        print (response.body)
        #print('name', name)
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
        out.write(',')
        out.write(str(len(lonlat)))
        out.write(',')
        out.write(str(len(des)))
        out.write('\n')
        out.close()
        if(len(lonlat)>0):
            desOut = open('./des/'+name[0].strip()+'.txt','w')
            desOut.write(lonlat[0])
            desOut.write('\n\n')
            desOut.write(des[0])
            desOut.close()
        
                
        
    def parse3(self, response):
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
        
        #print 'parse2'
        #print lonlat
        
        out = open('test123.txt','a+')
        #for i in range(len(name)):
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
        out.write(',')
        out.write(str(len(lonlat)))
        out.write(',')
        out.write(str(len(des)))
        out.write(',')
        if(len(lonlat)>0):
        	out.write(lonlat[0].split('|')[-1])
        else:
        	out.write('NULL')
        out.write('\n')
        out.close()
        if(len(lonlat)>0):
            desOut = open('./des/'+name[0].strip()+'.txt','w')
            desOut.write(lonlat[0])
            desOut.write('\n\n')
            desOut.write(des[0])
            desOut.close()

        
