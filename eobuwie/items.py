# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def clean(value):
    value = value.replace('\n',' ').strip()
    value = value.replace('  ',' ').strip()
    return value.replace('zł','').strip()

class EobuwieItem(scrapy.Item):
    name = scrapy.Field(input_processor = MapCompose(remove_tags, clean), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags, clean), output_processor = TakeFirst())
    rating_count = scrapy.Field(input_processor = MapCompose(remove_tags, clean), output_processor = TakeFirst())
    
