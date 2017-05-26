# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shopId = scrapy.Field();
    shopName = scrapy.Field();
    rating = scrapy.Field();
    taste = scrapy.Field();
    environment = scrapy.Field();
    service = scrapy.Field();
    tag = scrapy.Field();
    comNum = scrapy.Field();
    address = scrapy.Field();
    tel = scrapy.Field();
