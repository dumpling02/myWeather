# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyweatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_url = scrapy.Field()
    area_name = scrapy.Field()
    weather = scrapy.Field()
    pass
