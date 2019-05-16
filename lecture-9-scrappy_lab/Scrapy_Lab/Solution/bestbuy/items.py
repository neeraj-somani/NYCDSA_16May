# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestbuyItem(scrapy.Item):
    # define the fields for your item here like:
    user = scrapy.Field()
    rating = scrapy.Field()
    text = scrapy.Field()
    title = scrapy.Field()
    helpful = scrapy.Field()
    unhelpful = scrapy.Field()
    product = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()