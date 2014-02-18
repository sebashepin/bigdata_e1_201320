# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from crawl_institucional.items import ProfesorItem
from scrapy.http import Request
import re

class ProfesoresSpider(Spider):
    name = "profesores"
    allowed_domains = ["uniandes.edu.co"]
    start_urls = ["http://uniandes.edu.co/"]

    def parse(self, response):
        sel = Selector(response)
        sitios = sel.xpath("//div[@id='facultad']//li[@class='submenu2']/ul/li/a")
        for sitio in sitios:
            enlace = sitio.xpath("@href")[0].extract()
            departamento = sitio.xpath("text()")[0].extract()
            yield Request(enlace, self.parse_departamento, meta={'departamento': departamento})

    def parse_departamento(self, response):
        #print response.meta['departamento']
        sel = Selector(response)
        ruta = sel.xpath("//a/span[contains(., 'Planta')]/../@href").extract()
        if ruta:
            ruta = ruta[0]
            if ruta.startswith("http"):
                enlaceCompleto = ruta
            elif ruta.startswith("/"):
                enlaceCompleto = response.url + ruta[1:]
            else:
                enlaceCompleto = response.url + ruta
            print enlaceCompleto
            yield Request(enlaceCompleto, self.parse_planta, meta={'departamento': response.meta['departamento'], 'urlprincipal': response.url})
        else:
            ruta = sel.xpath("//a[re:test(., 'lanta|rofesores|Faculty')]/@href").extract()
            if ruta:
                ruta = ruta[0]
                if ruta.startswith("http"):
                    enlaceCompleto = ruta
                elif ruta.startswith("/"):
                    enlaceCompleto = response.url + ruta[1:]
                else:
                    enlaceCompleto = response.url + ruta
                print enlaceCompleto
                yield Request(enlaceCompleto, self.parse_planta, meta={'departamento': response.meta['departamento'], 'urlprincipal': response.url})
            else:
                print "No encontró la página de profesores de " + response.url

    def parse_planta(self, response):
        sel = Selector(response)
        profesores = sel.xpath("//p[re:test(., '[Ee][Xx][Tt]\w*\W+[0-9]{4}\D')]/../..").extract()
        if profesores:
            items = dict()
            for profesor in profesores:
                item = ProfesorItem()
                nombres = ""
                extension = ""
                email = ""
                try:
                    nombres = re.search('(([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,} ?){2,})', profesor).group(0)
                except:
                    pass
                try:
                    extension = re.search('([1-3][\d]{3})', profesor).group(0)
                except:
                    pass
                try:
                    email = re.search('([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})', profesor).group(0)
                except:
                    pass
                departamento = response.meta['departamento']
                sitioweb = response.meta['urlprincipal']
                if nombres:
                    item['nombres'] = nombres
                if extension:
                    item['extension'] = extension
                if email:
                    item['email'] = email
                if departamento:
                    item['departamento'] = departamento
                if sitioweb:
                    item['sitioWeb'] = sitioweb
                print "Profesor ******************************************************************"
                print "Nombre: " + nombres
                print "Departamento: " + departamento
                print "Extension: " + extension
                print "Email: " + email
                print "Sitio web: " + sitioweb
                print "***************************************************************************\n"
                items[(nombres+departamento+extension+email+sitioweb).encode('UTF-8')] = item
            return list(items.values())

