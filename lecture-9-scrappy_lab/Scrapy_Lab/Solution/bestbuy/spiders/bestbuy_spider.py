from scrapy import Spider, Request
from bestbuy.items import BestbuyItem
import re

class BestBuySpider(Spider):
	name = 'bestbuy_spider'
	allowed_urls = ['https://www.bestbuy.com/']
	start_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?id=pcmcat247400050000']

	def parse(self, response):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		text = response.xpath('//div[@class="left-side"]/span/text()').extract_first()
		_, per_page, total = map(lambda x: int(x), re.findall('\d+', text))
		number_pages = total // per_page

		# List comprehension to construct all the urls
		result_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?cp={}&id=pcmcat247400050000'.format(x) for x in range(1,number_pages+1)]

		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in result_urls[:1]:
			yield Request(url=url, callback=self.parse_result_page)


	def parse_result_page(self, response):
		# This fucntion parses the search result page.
		
		# We are looking for url of the detail page.
		detail_urls = response.xpath('//div[@class="sku-title"]/h4/a/@href').extract()

		# Yield the requests to the details pages, 
		# using parse_detail_page function to parse the response.
		for url in detail_urls:
			yield Request(url='https://www.bestbuy.com/' + url, callback=self.parse_detail_page)


	def parse_detail_page(self, response):
		# This fucntion parses the product detail page.

		# The first 8 reviews are on the product details page so we have to
		# carry them to the review pages.
		first_reviews = response.xpath('//li[@class="review-item"]')

		# Number of questions for each product
		try:
			question = response.xpath('//div[@class="ugc-qna-stats ugc-stat"]/a/text()').extract_first()
			question = re.findall('\d+', question)[0]
		except:
			question = 0

		if len(first_reviews) == 0:
			# If the product does not have any reviews, we just return.	
			return
		elif len(first_reviews) < 8:
		# If there are less than 8 reviews, we just scrape/yield all of them and call it a day.
		# Extract each field from the review tag
			product = response.xpath('//h1[@class="heading-5 v-fw-regular"]/text()').extract_first()
			for review in first_reviews:
				user = review.xpath('.//div[@class="undefined ugc-author v-fw-medium body-copy-lg"]/text()').extract_first()
				rating = review.xpath('.//span[@class="c-review-average"]/text()').extract_first()
				title = review.xpath('.//h3[@class="ugc-review-title c-section-title heading-5 v-fw-medium  "]/text()').extract_first()
				text = review.xpath('.//p[@class="pre-white-space"]/text()').extract_first()
				try:
					helpful = review.xpath('.//button[@data-track="Helpful"]/text()').extract()[1]
				except IndexError:
					helpful = ""
				try:
					unhelpful = review.xpath('.//button[@data-track="Unhelpful"]/text()').extract()[1]
				except IndexError:
					unhelpful = ""

				item = BestbuyItem()
				item['user'] = user
				item['rating'] = rating
				item['title'] = title
				item['text'] = text
				item['helpful'] = helpful
				item['unhelpful'] = unhelpful
				item['product'] = product
				item['question'] = question

				yield item

		else:
			# Total number of reviews
			num_reviews = response.xpath('//span[@class="c-total-reviews"]/text()').extract()[1]
			num_reviews = int(''.join(num_reviews.split(',')))
			# The link to the first page of reviews.
			first_review_page = response.xpath('//div[@class="see-all-reviews-button-container"]/a/@href').extract_first()
			# If the product has more than 8 reviews, we have to define another function to parse all the review pages
			# If there are some fields of data that you have to piggyback to the next level, you can pass them as a dictionary
			# as the meta parameter of the Request method.


			review_urls = [first_review_page + '?page={}'.format(i) for i in range(1, num_reviews//20+1)]
			for url in review_urls:
				yield Request(url='https://www.bestbuy.com/' + url, meta={'question': question}, 
						callback=self.parse_review_page)


	def parse_review_page(self, response):
		# Retrieve the first reviews from meta
		question = response.meta['question']

		# Find all the review tags
		reviews = response.xpath('//li[@class="review-item"]')
		product = response.xpath("//a[@data-track = 'Product Description']/text()").extract_first()

		# Extract each field from the review tag
		for review in reviews:
			user = review.xpath('.//div[@class="undefined ugc-author v-fw-medium body-copy-lg"]/text()').extract_first()
			rating = review.xpath('.//span[@class="c-review-average"]/text()').extract_first()
			title = review.xpath('.//h3[@class="ugc-review-title c-section-title heading-5 v-fw-medium  "]/text()').extract_first()
			text = review.xpath('.//p[@class="pre-white-space"]/text()').extract_first()
			try:
				helpful = review.xpath('.//button[@data-track="Helpful"]/text()').extract()[1]
			except IndexError:
				helpful = ""
			try:
				unhelpful = review.xpath('.//button[@data-track="Unhelpful"]/text()').extract()[1]
			except IndexError:
				unhelpful = ""

			item = BestbuyItem()
			item['user'] = user
			item['rating'] = rating
			item['title'] = title
			item['text'] = text
			item['helpful'] = helpful
			item['unhelpful'] = unhelpful
			item['product'] = product
			item['question'] = question

			yield item
