from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawl_institucional.items import ProfesorItem

class DependencyspiderSpider(CrawlSpider):
    name = 'DependencySpider'
    allowed_domains = ['uniandes.edu.co']
    start_urls = []

    rules = (
        Rule(SgmlLinkExtractor(allow=r'.*planta.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print response.url
        sel = Selector(response)
        i = CrawlInstitucionalItem()
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
