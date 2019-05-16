# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WikiItem(scrapy.Item):
	film = scrapy.Field()
	year = scrapy.Field()
	awards = scrapy.Field()
	nominations = scrapy.Field()
