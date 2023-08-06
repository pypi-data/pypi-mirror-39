# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys


ITEM_PIPELINES = {
    'nimbus_scrapy.pipelines.NimbusPipeline': 300,
}

SPIDER_MIDDLEWARES = {
    'nimbus_scrapy.middlewares.DeltaFetch': 100,
}


def update_settings(settings=None):
    if settings is None:
        settings = {}
    item_pipelines = settings.get("ITEM_PIPELINES", {})
    item_pipelines.update(ITEM_PIPELINES)
    spider_middlewares = settings.get("SPIDER_MIDDLEWARES", {})
    spider_middlewares.update(SPIDER_MIDDLEWARES)
    settings["ITEM_PIPELINES"] = item_pipelines
    settings["SPIDER_MIDDLEWARES"] = spider_middlewares
    return settings
