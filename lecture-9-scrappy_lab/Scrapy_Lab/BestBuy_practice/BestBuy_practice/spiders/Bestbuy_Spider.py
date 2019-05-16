from scrapy import Spider
from BestBuy_practice.items import BestbuyPracticeItem

class BestbuyPracticeSpider(Spider):
	name = 'BestbuyPracticeSpider'
	allowed_urls = ['https://www.bestbuy.com/']
    start_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?id=pcmcat247400050000']


	def parse(self, response):
	    # Find the total number of pages in the result so that we can decide how many urls to scrape next
	    text = response.xpath('//div[@class="left-side"]/span/text()').extract_first()
	    _, per_page, total = map(lambda x: int(x), re.findall('\d+', text))
	    number_pages = total // per_page + 1
	    # List comprehension to construct all the urls
	    result_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?cp={}&id=pcmcat247400050000'.format(x) for x in range(1,number_pages+1)]
    	for url in result_urls:
    		return Request(url=url, call_back=self.parse_result_page)

    def parse_result_page(self, response):
	    # This fucntion parses the search result page.
	    # We are looking for url of the detail page.
	    detail_urls = response.xpath('//div[@class="sku-title"]/h4/a/@href').extract()
	    print(len(detail_urls))