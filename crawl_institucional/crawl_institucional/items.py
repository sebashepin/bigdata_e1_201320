# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProfesorItem(Item):
    nombres = Field()
    apellidos = Field()
    departamento = Field()
    extension = Field()
    tipo = Field()
    email = Field()
    sitioWeb = Field()
