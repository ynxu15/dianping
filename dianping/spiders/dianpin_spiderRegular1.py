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
import os

#from scrapy import optional_features
#optional_features.remove('boto')

reload(sys)
sys.setdefaultencoding('utf-8') 

def match(reU, s):
    if re.match(reU, s):
        return True
    else:
        return False


class DianpingSpiderR(BaseSpider):
    name = "dianpingR1"
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
        #"http://www.dianping.com/search/category/1/10/r1",
        #"http://www.dianping.com/search/category/1/10/r2",
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
        self.review_rule = "/shop/[0-9]+/review_more"
        self.user_rule = "/member/[0-9]+$"
        self.user_review_rule = "/member/[0-9]+/"
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_region)
        '''while(len(self.urlUProcessed)>0):
            for url in self.urlProcessed:
                yield scrapy.Request(url=url, callback=self.parse) 
            time.sleep(120)'''
        

    def parse_region(self, response):
        self.url_can[response.url] = 1
        newurls = response.xpath('//a/@href').extract()
        for url in newurls:
            if match(self.shop_rule,url):
                if not self.url_can.has_key(self.base_url+url):
                    yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop2) 
            if match(self.review_rule,url):
                if not self.url_can.has_key(self.base_url+url):
                    yield scrapy.Request(url=self.base_url+url, callback=self.parse_review) 
	    if match(self.user_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user) 
	    if match(self.user_review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user_review) 
            if match(self.category_rule,url):
                if not self.url_can.has_key(self.base_url+url):
                    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
            if match(self.region_rule,url) or match(self.region_rule1,url):
                if not self.url_can.has_key(self.base_url+url):
                    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
                

    def parse_shop2(self, response):
	'''shop information'''
        self.url_can[response.url] = 1
	destinationPath = 'shopPage'
	if not os.path.exists(destinationPath):
	    os.makedirs(destinationPath)	
        outPage = open('shopPage/'+response.url.split('/')[-1],'w')
        outPage.write(response.body)
        outPage.close()

	newurls = response.xpath('//a/@href').extract()
	for url in newurls:
	    if match(self.shop_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop2) 
	    if match(self.review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_review) 
	    if match(self.user_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user) 
	    if match(self.user_review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user_review) 
	    if match(self.category_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
	    if match(self.region_rule,url) or match(self.region_rule1,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 

    def parse_review(self, response):
	'''review information of shops'''
        self.url_can[response.url] = 1
        shopId = response.url.split('/')[-2]
        page = response.url.split('/')[-1]
	destinationPath = 'shopRecom'
	if not os.path.exists(destinationPath):
	    os.makedirs(destinationPath)	
        mypath = 'shopRecom/'+shopId
        if not os.path.exists(mypath):
            os.makedirs(mypath)
        out = open(mypath+'/'+page,'w')
        out.write(response.body)
        out.close()

	newurls = response.xpath('//a/@href').extract()
	for url in newurls:
	    if match(self.shop_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop2) 
	    if match(self.review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_review) 
	    if match(self.user_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user)
	    if match(self.user_review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user_review) 
	    if match(self.category_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
	    if match(self.region_rule,url) or match(self.region_rule1,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 

    def parse_user(self, response):
	'''user information'''
        self.url_can[response.url] = 1
       	userId = response.url.split('/')[-1]
	destinationPath = 'user'
	if not os.path.exists(destinationPath):
	    os.makedirs(destinationPath)	
        mypath = 'user/'+userId
        out = open(mypath,'w')
        out.write(response.body)
        out.close()

	newurls = response.xpath('//a/@href').extract()
	for url in newurls:
	    if match(self.shop_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop2) 
	    if match(self.review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_review) 
	    if match(self.user_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user)
	    if match(self.user_review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user_review) 
	    if match(self.category_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
	    if match(self.region_rule,url) or match(self.region_rule1,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
    
    def parse_user_review(self, response):
	'''user review information'''
        self.url_can[response.url] = 1
       	userId = response.url.split('/')[-2]
        page = response.url.split('/')[-1]
	destinationPath = 'userReview'
	if not os.path.exists(destinationPath):
	    os.makedirs(destinationPath)	
        mypath = 'userReview/'+userId
        if not os.path.exists(mypath):
            os.makedirs(mypath)
        out = open(mypath+'/'+page,'w')
        out.write(response.body)
        out.close()

	newurls = response.xpath('//a/@href').extract()
	for url in newurls:
	    if match(self.shop_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_shop2) 
	    if match(self.review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_review) 
	    if match(self.user_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user) 
	    if match(self.user_review_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_user_review) 	    
	    if match(self.category_rule,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 
	    if match(self.region_rule,url) or match(self.region_rule1,url):
		if not self.url_can.has_key(self.base_url+url):
		    yield scrapy.Request(url=self.base_url+url, callback=self.parse_region) 

