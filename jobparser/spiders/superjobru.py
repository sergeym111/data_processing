import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, '_6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow('https://russia.superjob.ru' + link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//a[contains(@class, '_6AfZ9')]//text()").get()
        salary = response.xpath("//span[contains(@class, 'ZON4b')]//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)

