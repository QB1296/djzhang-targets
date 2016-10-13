# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    title = scrapy.Field()
    oldPrice = scrapy.Field()
    newPrice = scrapy.Field()
    pictures = scrapy.Field()

    color = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
