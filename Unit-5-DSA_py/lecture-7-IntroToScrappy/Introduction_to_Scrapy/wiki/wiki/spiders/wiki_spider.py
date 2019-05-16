# -*- coding: utf-8 -*-
from scrapy import Spider
from wiki.items import WikiItem


class WikiSpider(Spider):
	name = 'wiki_spider'
	allowed_urls = ['https://en.wikipedia.org']
	start_urls = ['https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films']

	def parse(self, response):
		# Find all the table rows
		rows = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')
		
		# The movie title could be of different styles so we need to provide all the possibilities.
		patterns = ['./td[1]/i/a/text()', './td[1]/i/b/a/text()', './td[1]/i/span[2]//text()', './td[1]/i/b/span/text()']
		for row in rows:
			# extract() will return a Python list, extract_first() will return the first element in the list
			# If you know the first element is what you want, you can use extract_first()
			for pattern in patterns:
				film = row.xpath(pattern).extract_first()
				if film:
					break
			# If the movie title is missing, then we just skip it.
			if not film:
				continue
			# Relative xpath for all the other columns
			year = row.xpath('./td[2]/a/text()').extract_first()
			awards = row.xpath('./td[3]/text()').extract_first()
			nominations = row.xpath('./td[4]/text()').extract_first().strip()

			# Initialize a new WikiItem instance for each movie.
			item = WikiItem()
			item['film'] = film
			item['year'] = year
			item['awards'] = awards
			item['nominations'] = nominations
			yield item
