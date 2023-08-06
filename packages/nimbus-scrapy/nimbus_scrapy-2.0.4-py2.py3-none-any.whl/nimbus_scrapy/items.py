# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from scrapy.loader.processors import Compose, SelectJmes, MergeDict
from scrapy.loader import ItemLoader


class CrawledItem(scrapy.Item):
    url = scrapy.Field()


class ScrapItem(scrapy.Item):
    url = scrapy.Field()


