from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawl_registro.items import CrawlRegistroItem
from crawl_registro.items import ProfesorItem

class CursosCrawlSpider(CrawlSpider):
    name = 'cursos_crawl'
    allowed_domains = ['registroapps2.uniandes.edu.co']
    start_urls = ['http://registroapps2.uniandes.edu.co/scripts/adm_con_horario_joomla.php']


    rules = (
        Rule(SgmlLinkExtractor(allow=r''), callback='parse_departamento', follow=True),
    )

    def parse_departamento(self, response):
        sel = Selector(response)
        nombresProfesores = sel.xpath('//html/body/table/tr/td/table/tr/td/table/tr/td/table/tr/td/font/font/text()')
        departamento = sel.xpath('//html/body/table/tr/td/table/tr/td/span/text()').extract()[1].strip()
        profesores = []
        for nombre in nombresProfesores:
            print nombre.extract().strip()
            profesor = ProfesorItem()
            profesor['nombre'] = nombre.extract().strip()
            profesor['departamento'] = departamento
            profesores.append(profesor)
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return profesores