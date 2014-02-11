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
        nameCountRegex = re.compile(ur"[^0-9A-Za-z]+",re.UNICODE)
        lastNameRegex = re.compile(ur"\w+[\s']\w+",re.UNICODE)
        firstNameRegex = re.compile(ur"\w+[\s']\w+[\s']",re.UNICODE)

        sel = Selector(response)
        nombresProfesores = sel.xpath('//html/body/table/tr/td/table/tr/td/table/tr/td/table/tr/td/font/font/text()')
        # Si está en la página principal omita el ciclo de parsing
        if not sel.xpath('//html/body/table/tr/td/table/tr/td/span/text()'):
            return
        departamento = sel.xpath('//html/body/table/tr/td/table/tr/td/span/text()').extract()[1].strip()
        profesores = set()
        for nombre in nombresProfesores:
            nombre = nombre.extract().strip()
            if not nombre:
                continue
            splitName = nameCountRegex.split(nombre)
            if len(splitName) <= 2:
                nombres = splitName[1]
                apellidos = splitName[0]
            else:
                apellidos = lastNameRegex.findall(nombre)[0].strip()
                try:
                    nombres = firstNameRegex.split(nombre)[1].strip()
                except IndexError:
                    print ("ERRORHORRIBLE\t" + nombre + "\t" + str(len(splitName))).encode('utf-8')
            profesor = ProfesorItem()
            profesor['nombres'] = nombres
            profesor['apellidos'] = apellidos
            profesor['departamento'] = departamento
            profesores.add(profesor)
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return profesores
