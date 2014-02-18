# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawl_registro.items import ProfesorItem
import re

class CursosCrawlSpider(CrawlSpider):
    name = 'cursos_crawl'
    allowed_domains = ['registroapps2.uniandes.edu.co']
    start_urls = ['http://registroapps2.uniandes.edu.co/scripts/adm_con_horario_joomla.php']
    rules = (
        Rule(SgmlLinkExtractor(allow=r''), callback='parse_departamento', follow=True),
    )

    def parse_departamento(self, response):
        # Regex compilation
        nameCountRegex = re.compile(ur"\s",re.UNICODE)
        splitNameRegex = re.compile(ur"([^\s]+\s[^\s]+\s)",re.UNICODE)

        sel = Selector(response)
        nombresProfesores = sel.xpath('//html/body/table/tr/td/table/tr/td/table/tr/td/table/tr/td/font/font/text()')
        # Si está en la página principal omita el ciclo de parsing
        if not sel.xpath('//html/body/table/tr/td/table/tr/td/span/text()'):
            return
        departamento = sel.xpath('//html/body/table/tr/td/table/tr/td/span/text()').extract()[1].strip()
        profesores = dict()
        for nombre in nombresProfesores:
            nombre = nombre.extract().strip()
            if not nombre:
                continue
            splitName = nameCountRegex.split(nombre)
            if len(splitName) <= 2:
                nombres = splitName[1]
                apellidos = splitName[0]
            else:
                apellidos = splitNameRegex.findall(nombre)[0].strip()
                nombres = splitNameRegex.split(nombre)[2].strip()  
            profesor = ProfesorItem()
            profesor['nombres'] = nombres
            profesor['apellidos'] = apellidos
            profesor['departamento'] = departamento
            profesores[(nombres+apellidos+departamento).encode('UTF-8')] = profesor
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return list(profesores.values())
