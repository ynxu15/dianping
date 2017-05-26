# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
import time
import scrapy
from dianping.items import ShopItem
reload(sys)
sys.setdefaultencoding('utf-8') 


class DianpingSpider11(CrawlSpider):
    name = "dianping11"
    allowed_domains = ["dianping.com"]
    
    start_urls = [
        #"http://www.dianping.com/shanghai/food",
        #"http://www.dianping.com/search/category/1/10/r1",
        #"http://www.dianping.com/search/category/1/10/r2",
        #"http://www.dianping.com/search/category/1/10/r3"
        "http://www.dianping.com/shop/75661045",
        "http://www.dianping.com/shop/69608275",
        "http://www.dianping.com/shop/21585481",
        "http://www.dianping.com/shop/58039287",
        "http://www.dianping.com/shop/65747721",
        "http://www.dianping.com/shop/5238394"
    ]

    rules = [
        #Rule(LinkExtractor(allow=('www.dianping.com/search/category/1/10/r*',)), callback='parse_region'),
        #Rule(LinkExtractor(allow=('/search/category/1/10/r*',)), callback='parse_region'),
        Rule(LinkExtractor(allow=('/shop/[0-9]+/review_more*',)), callback='parse_comment'),
        #Rule(LinkExtractor(allow=('/shop/[0-9]+$',)), callback='parse_shop'),
        #Rule(LinkExtractor(allow=('www.dianping.com/shop/[0-9]+$',)), callback='parse_shop'),
        #Rule(LinkExtractor(allow=('/search/category/*',)), callback='parse_region'),

    ]
    
  	#Do not over write this function
    #def parse(self, response):
    #	pass
    def parse_region(self, response):
    	pass
        
    def parse_shop(self, response):
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
        item['shopName'] = name[0].strip()
        item['rating'] = rating[0]
        item['taste'] = taste[0]
        item['environment'] = environment[0]
        item['service'] = service[0]
        item['tag'] = tag[0].replace('\\n','').strip ()
        item['comNum'] = comNum[0]
        item['address'] = address[0].replace('\\n','').strip ()
        item['tel'] = tel[0]

        yield item

    def parse_comment(self, response):
    	''' folder
    	shopComment
    		shopId
    			comment
    			pic
    				user
    	'''
    	shopId = response.url.split('/')[-2]	
    	userId = response.xpath('//li/div[class="pic"]/a[1]/@user-id').extract()
    	#userName = response.xpath('//div[@class="comment-list"]/li/div[@class="pic"]/p[@class="name"]/a/text()').extract()
    	#userContribution = response.xpath('//div[@class="comment-list"]/li//div[@class="pic"]/p[@class="contribution"]/span/text()').extract()
    	#commentId = response.xpath('//div[@class="comment-list"]/li/@data-id').extract()
    	#commentStar = response.xpath('//div[@class="comment-list"]/li//div[@class="content"]/div[class="user-info"]/span[@title]/@title').extract()
    	#commPer =  response.xpath('//div[@class="comment-list"]/li//div[@class="content"]/div[class="user-info"]/span[@class="comm-per"]/text()').extract()
    	#commentRst = response.xpath('//div[@class="comment-list"]/li//div[@class="content"]/div[class="user-info"]/div[@class="comment-rst"]/span[1]/text()').extract()
    	#commentTxt = response.xpath('//div[@class="comment-list"]/li//div[@class="content"]/div[class="comment-txt"]/div[1]/text()').extract()
    	#commentTime = response.xpath('//li[@id]/span[@class="time"]/text()').extract()
    	#shopPhoto 
    	#agreeNum
    	#responseNum
    	#collectionNum 
    	outfile = open('shopRecom/'+shopId,'w')
    	for user in userId:
    		outfile.write(userId)
    		outfile.write('\n')




