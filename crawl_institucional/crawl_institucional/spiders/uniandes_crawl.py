from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawl_institucional.items import ProfesorItem
from scrapy.http import Request
from DependencySpider import DependencyspiderSpider
class UniandesCrawlSpider(CrawlSpider):
    name = 'uniandes_crawl'
    allowed_domains = ['uniandes.edu.co']
    start_urls = ['http://www.uniandes.edu.co/']

    rules = (
        Rule(SgmlLinkExtractor(allow='',deny='.*/institucional/facultades/*',restrict_xpaths='//*[@id="facultad"]/ul/li/div/div/div/div/ul'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = CrawlInstitucionalItem()
        print str(sel.xpath('//title/text()').extract()) + "\t\t" + response.url
        myRequest = Request("https://mecanica.uniandes.edu.co",callback=self.parse_item)
        return myRequest
        currentDependency = DependencyspiderSpider()
        currentDependency.start_urls = ["https://mecanica.uniandes.edu.co"]
        currentDependency.start_requests()
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
