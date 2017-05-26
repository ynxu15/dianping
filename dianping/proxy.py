#!/usr/bin/python
#-*-coding:utf-8-*-

import random
import scrapy
import requests
import ujson

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class RandomProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_ip=''):
        self.proxy_ip = proxy_ip
        r = requests.get("http://192.168.1.84:8000/?types=0&count=200&country=%E5%9B%BD%E5%86%85", timeout=10)
        r1 = ujson.decode(r.text)
        for record in r1:
            self.proxy_list.append("http://"+record[0]+":"+str(record[1]))

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        if ip:
            print ip
            request.meta['proxy']= ip

    #turns out only several ip works here
    '''proxy_list = [  "http://206.109.4.94:8080",
                    "http://202.103.215.199:80",
                    "http://171.35.242.139:80",
                    "http://52.76.170.159:80",
                    "http://54.183.234.224:8080",
                    "http://124.193.9.6:3128",
                    "http://54.183.214.25:8083",
                    "http://41.215.240.161:3128",
                    "http://221.211.117.140:3128",
                    "http://190.131.215.52:80"]'''

    proxy_list = ['http://111.56.7.9:80', 'http://60.211.182.76:8080', 'http://117.135.198.11:80', 'http://1.82.132.75:8080', 'http://1.30.130.60:8080', 'http://220.182.51.123:8081', 'http://113.58.232.193:808', 'http://221.14.7.241:8080', 'http://111.23.10.172:80', 'http://36.249.26.17:808', 'http://183.32.88.116:808', 'http://124.47.7.45:80', 'http://60.169.5.68:8080', 'http://116.199.115.85:80', 'http://111.23.10.46:80', 'http://111.23.10.51:80']


    
            