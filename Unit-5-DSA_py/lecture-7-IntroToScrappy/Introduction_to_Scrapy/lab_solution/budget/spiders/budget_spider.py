from scrapy import Spider
from budget.items import BudgetItem


class BudgetSpider(Spider):
    name = "budget_spider"
    allowed_urls = ['https://www.the-numbers.com/']
    start_urls = ['https://www.the-numbers.com/movie/budgets/all/' + str(100*i+1) for i in range(56)]

    def parse(self, response):
        rows = response.xpath('//*[@id="page_filling_chart"]/center/table//tr')
        for row in rows[1:]:
            RDate = row.xpath('./td[2]/a/text()').extract_first()
            Title = row.xpath('./td[3]/b/a/text()').extract_first()
            PBudget = row.xpath('./td[4]/text()').extract_first()
            DomesticG = row.xpath('./td[5]/text()').extract_first()
            WorldwideG = row.xpath('./td[6]/text()').extract_first()

            item = BudgetItem()
            item['RDate'] = RDate
            item['Title'] = Title
            item['PBudget'] = PBudget
            item['DomesticG'] = DomesticG
            item['WorldwideG'] = WorldwideG

            yield item
