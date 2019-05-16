from scrapy import Spider
from Wiki_practice.items import WikiPracticeItem

class WikiPracticeSpider(Spider):
    name = 'wiki_practice_spider'
    allowed_urls = ['https://en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films']

    def parse(self, response):
        # Find all the table rows
        rows = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')
        patterns = ['./td[1]/i/a/text()', './td[1]/i/b/a/text()',\
                    './td[1]/i/span[2]//text()', './td[1]/i/b/span/text()']
        
        for row in rows:            
            for pattern in patterns:
                film = row.xpath(pattern).extract_first()
                if film:
                    break
            if not film:
                continue
          
            year = row.xpath('./td[2]/a/text()').extract_first()
            award = row.xpath('./td[3]/text()').extract_first()
            nomination = row.xpath('./td[4]/text()').extract_first().strip()

            item = WikiPracticeItem()
            item['film']=film
            item['year']=year
            item['awards']=award
            item['nominations']=nomination

            yield item
