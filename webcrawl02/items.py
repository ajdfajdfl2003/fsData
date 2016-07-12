# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class fsData(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    timestamp = scrapy.Field()
    category  = scrapy.Field()
    type      = scrapy.Field()
    address   = scrapy.Field()
    assignUnit = scrapy.Field()
    status    = scrapy.Field()
    allData = scrapy.Field()
