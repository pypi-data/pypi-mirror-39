# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import json
from collections import OrderedDict
from scrapy import signals
from scrapy.conf import settings as default_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing import Process, Lock, Queue, current_process
from multiprocessing import Pool, Manager
import multiprocessing as mp


class CrawlerWorker(Process):

    def __init__(self, spider, callback=None, settings=None, *args, **kwargs):
        super(Process, self).__init__()
        _settings = settings or default_settings
        self.crawler = CrawlerProcess(_settings)
        self.spider = spider
        self.callback = callback if callback and isinstance(callback, CrawlerCallback) else CrawlerCallback()
        self.info = {}
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _info(self):
        return {
            "name": self.spider.name,
            "cpus": mp.cpu_count(),
            "ppid": os.getppid(),
            "pid": os.getpid(),
        }

    def _item_passed(self, item, spider=None):
        self.callback.process_item(item=item, spider=spider)

    def run(self, *args, **kwargs):
        self.info = self._info()
        self.callback.process_info(info=self.info)
        self.crawler.crawl(self.spider)
        self.crawler.start(stop_after_crawl=True)
        self.crawler.stop()
        self.callback.process_done()


class CrawlerCallback(object):

    def __init__(self, lock=None):
        self.items = []
        self.lock = lock if lock is not None else Lock()

    def process_info(self, info):
        self.lock.acquire()
        try:
            self.callback_info(info=info)
        finally:
            self.lock.release()

    def process_item(self, item, spider=None):
        self.lock.acquire()
        try:
            self.items.append(item)
            self.callback_item(item, spider=spider)
        finally:
            self.lock.release()

    def process_done(self):
        self.lock.acquire()
        try:
            self.callback_items(self.items)
        finally:
            self.lock.release()

    def callback_info(self, info):
        raise NotImplementedError

    def callback_item(self, item, spider):
        raise NotImplementedError

    def callback_items(self, items):
        raise NotImplementedError
