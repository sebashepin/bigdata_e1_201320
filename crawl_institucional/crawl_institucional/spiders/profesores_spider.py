# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from crawl_institucional.items import ProfesorItem
from scrapy.http import Request

class ProfesoresSpider(Spider):
    name = "profesores"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = ["http://uniandes.edu.co/"]

    def parse(self, response):
        sel = Selector(response)
	sitios = sel.xpath("//div[@id='facultad']//li[@class='submenu2']/ul/li/a")
	enlaces = []
	for sitio in sitios:
	    titulo = sitio.xpath('text()').extract()
	    enlaces.append(sitio.xpath('@href')[0].extract())
	enlacesVisitados = []
	for enlace in enlaces:
	    enlacesVisitados.append(enlace)
	    print enlace
	    #yield Request(enlace, self.parse_departamento)

    def parse_departamento(self, response):
        sel = Selector(response)
	enlanceProfesores = sel.xpath("//a/text()='Profesores de planta'")
	print enlanceProfesores
