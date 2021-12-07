import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    pre_url = 'https://leroymerlin.ru/'

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}&suggest=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@data-qa-pagination-item, 'right')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("///a[contains(@data-qa, 'product-image')]//@href").getall()
        for link in links:
            link = self.pre_url + link
            yield response.follow(link, callback=self.parse_items)

    def parse_items(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', "//h1//text()")
        loader.add_xpath('price', "//span[@slot='price']//text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']//@srcset")
        loader.add_value('url', response.url)
        yield loader.load_item()



        # name = response.xpath("//h1//text()").get()
        # url = response.url
        # price = response.xpath("//span[@slot='price']//text()").get()
        # photos = response.xpath("//source[@media=' only screen and (min-width: 1024px)']//@srcset").getall()
        # yield JobparserItem(name=name, url=url, price=price, photos=photos)
        # print()
