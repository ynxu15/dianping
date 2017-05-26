# -*- coding:utf-8 -*-
from scrapy.spider import BaseSpider
from urlparse import urlparse
from scrapy.http import Request 
import urllib
import sys
import time
import scrapy

#from scrapy import optional_features
#optional_features.remove('boto')

reload(sys)
sys.setdefaultencoding('utf-8') 

#from dianping.items import *


class DianpingSpider2(BaseSpider):
    name = "dianping2"
    allowed_domains = ["dianping.com"]
    
    
    start_urls = [
        #"http://www.dianping.com/search/category/1/10/r835"
        #"http://www.dianping.com/shanghai/food"
    ]
    #"http://www.dianping.com/shanghai/food"
    def start_requests(self):
        self.base_url = "http://www.dianping.com/search/category/1/10/r"
        self.shop_base_url = "http://www.dianping.com"
        ids = []
        ids += range(835,839)
        ids += range(8865,874)
        ids += [24031]
        ids += range(811,815)
        ids += range(839,846)
        ids += range(846,854)
        ids += [2528,8597,8928,70507,982,67276,8446,8929,9179,12029,22947,22948,24017,24018,24020,24024,24141,70265,70326,70531,67275,2865,2866,9177,12038,2864,12026,22949,22950,22951,22946,8445,831,833]
        ids += [834,2527,9178,11374,24019,26146,70277, 67354,5962,24021,24022,27830,65166, 5949,24023,30340, 70209,9172,9173,24025,66319,66320,9174,65207,66226,8848]
        ids += range(22952,22959)
        ids += range(801,8011)
        ids += range(2867,2870)
        ids += range(5946,5949)
        ids += range(859,865)
        ids += range(815,820)
        ids += range(827,831)
        ids += range(820, 827)
        ids += range(854, 859)  
        ids += range(8440, 8445)  
        ids += range(9169, 9172) 
        ids += range(5940, 5944)  
        ids += range(22979, 22988)  
        ids += range(5944, 5947)  
        ids += range(22988, 22993)  
        ids += range(22993, 22996)  
        ids += range(22959, 22966)  
        ids += range(22966, 22976)  
        ids += range(64597, 64615)   
        #for url in self.start_urls:
            #yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': "your agent string"}) 
        #yield scrapy.Request(url=self.base_url+str(ids[1]), callback=self.parse1, headers={'User-Agent': "your agent string"}) 
        for id in ids:
            time.sleep(1)
            yield scrapy.Request(url=self.base_url+str(id), callback=self.parse1) 
        for id in ids:
            time.sleep(1)
            for pageN in range(2,51):
                yield scrapy.Request(url=self.base_url+str(id)+'p'+str(pageN), callback=self.parse1)         
                    
    def parse(self, response):
        #print response.body
        #print ('xpath')
        #print response.xpath('//body/div[@class="main"]')
        #print response.xpath('//div[@class="block nav_box"]/ul/li[@id="J_nc_business"]/div[@data-target="#J_nc_business"]')
        #print response.xpath('//*[@id="J_nc_business"]/div')
        #print response.xpath('//div[@class="fpp_business"]')
        #filename = response.url.split("/")[-2]
        #open('test12.txt', 'wa').write(response.xpath('//*[@id="J_nc_business"]/div[2]'))
        #print (response.body)
        #print response.xpath('//*[@id="shop-all-list"]/ul/li[3]/div[2]/div[1]')
        #print response.xpath('//*[@id="shop-all-list"]/ul/li[2]/div[2]/div[1]/a[1]/h4/text()').extract()
        #print response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/h4/text()').extract()   # name
        #print response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/a[1]/b/text()').extract()     # number of customer
        #print response.xpath('//*[@id="shop-all-list"]/ul/li[3]/div[2]/div[3]/span/text()').extract()    # address
        name = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/h4/text()').extract()
        rating = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/span/@title').extract()
        kouwei = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/span/span[1]/b/text()').extract()
        huanjing = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/span/span[2]/b/text()').extract()
        fuwu = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/span/span[3]/b/text()').extract()
        price = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/a[2]/b/text()').extract()
        tag = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[3]/a[1]/span/text()').extract()
        comNum = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/a[1]/b/text()').extract() 
        address =  response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[3]/span/text()').extract()    # address
        
        #print 'rating'
        #print rating
        
        #out = open('test123.txt','a+')
        #out.write('rating')
        #out.write(str(len(rating)))
        #out.write('\n')
        
        out = open('test123.txt','a+')
        for i in range(len(name)):
            out.write(name[i])
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
            out.write(tag[i])
            out.write(',')
            out.write(address[i])
            out.write('\n')
        
        items = []
        for i in range(len(name)):
            item = DianpingItem()
            item['shopName'] = name[i]
            item['shopAdd'] = address[i]
            item['comNum'] = comNum[i]
            items.append(item) 
        return items
        
        
        #open('test.txt', 'wb').write(response.body)
    def parse1(self, response):
        urls = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href').extract()
        for url in urls:
            time.sleep(0.2)
            yield scrapy.Request(url=self.shop_base_url+url, callback=self.parse2)      
    
    def parse2(self, response):
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
        script  = response.xpath('//script/text()').extract()
        #print script
        for s in script:
        	if "window.shop_config" in s:
        		shopInfo = open('shopLoc/'+response.url.split('/')[-1],'w')
        		shopInfo.write(s)
        		#print s
        #lonlat = response.xpath('//*[@id="aside-bottom"]/div[1]/div').extract()
        
        #print 'parse2'
        #print lonlat
        
        out = open('test123.txt','a+')
        #for i in range(len(name)):
        i=0
        out.write(name[i].strip())        
        out.write(',')
        out.write(str(len(script)))
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
        #out1 = open('shop/'+response.url.split('/')[-1],'w')
        #out1.write(response.body)
        if(len(lonlat)>0):
            desOut = open('./des/'+name[0].strip()+'.txt','w')
            desOut.write(lonlat[0])
            desOut.write('\n\n')
            desOut.write(des[0])
            desOut.close()
        
                
        
        

        
