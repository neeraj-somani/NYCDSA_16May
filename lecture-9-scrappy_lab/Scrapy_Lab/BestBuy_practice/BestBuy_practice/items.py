# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestbuyPracticeItem(scrapy.Item):
    # define the fields for your item here like:
    Pname = scrapy.Field()
    Uname = scrapy.Field()
    RRating = scrapy.Field()
    RText = scrapy.Field()
    RTitle = scrapy.Field()
    NumberOfHelpful = scrapy.Field()
    NumberOfUnhelpful = scrapy.Field()
