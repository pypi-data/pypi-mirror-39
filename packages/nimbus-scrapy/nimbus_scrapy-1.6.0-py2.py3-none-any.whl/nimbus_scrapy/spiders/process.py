# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import json
import time
from collections import OrderedDict
from pydispatch import dispatcher
from scrapy import signals
from scrapy.resolver import CachingThreadedResolver
from multiprocessing import Process, Lock, Queue, current_process
from multiprocessing import Pool, Manager
import multiprocessing as mp
from .crawler import CrawlerRunner, CrawlerProcess

__all__ = [
    "BaseWorker",
    "CrawlerRunnerWorker",
    "CrawlerProcessWorker",
]


class BaseWorker(Process):

    def __init__(self, spider, callback=None, group=None, target=None, name=None, *args, **kwargs):
        super(BaseWorker, self).__init__(group=group, target=target, name=name)
        self.spider = spider
        self.args = args
        self.kwargs = kwargs
        self.callback = callback if callback and isinstance(callback, CrawlerCallback) else CrawlerCallback()
        dispatcher.connect(self._item_passed, signals.item_passed)

    @staticmethod
    def init():
        try:
            import psutil
            ps = psutil.Process(os.getpid())
            if not psutil.WINDOWS:
                ps.nice(19)
            else:
                ps.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except Exception as e:
            pass

    @property
    def info(self):
        return {
            "name": self.spider.name,
            "cpus": mp.cpu_count(),
            "ppid": os.getppid(),
            "pid": os.getpid(),
        }

    def _item_passed(self, item, spider=None):
        self.callback.process_item(item=item, spider=spider)


class CrawlerRunnerWorker(BaseWorker):

    def __init__(self, spider, callback=None, settings=None, group=None, target=None, name=None, *args, **kwargs):
        super(CrawlerRunnerWorker, self).__init__(
            spider, callback=callback, group=group, target=target, name=name, *args, **kwargs)
        self.crawler = CrawlerRunner(settings)

    def run(self, *args, **kwargs):
        self.init()
        self.callback.process_start(info=self.info)
        self.crawler.crawl(self.spider, *self.args, **self.kwargs)
        self.crawler.start()
        self.crawler.stop()
        self.callback.process_done(info=self.info)


class CrawlerProcessWorker(BaseWorker):

    def __init__(self, spider, callback=None, settings=None, group=None, target=None, name=None, *args, **kwargs):
        super(CrawlerProcessWorker, self).__init__(
            spider, callback=callback, group=group, target=target, name=name, *args, **kwargs)
        self.crawler = CrawlerProcess(settings)

    def run(self, *args, **kwargs):
        self.init()
        self.callback.process_start(info=self.info)
        self.crawler.crawl(self.spider, *self.args, **self.kwargs)
        self.crawler.start()
        self.crawler.stop()
        self.callback.process_done(info=self.info)


class CrawlerCallback(object):

    def __init__(self, lock=None):
        self.items = []
        self.lock = lock if lock is not None else Lock()
        self.time_st = 0
        self.time_end = 0
        self.delta = 0

    def get_time_delta(self, end=None):
        end = end or time.time()
        return end - self.time_st

    def process_start(self, info):
        self.lock.acquire()
        try:
            self.time_st = time.time()
            self.callback_start(info=info, time=self.time_st)
        finally:
            self.lock.release()

    def process_item(self, item, spider=None):
        self.lock.acquire()
        try:
            delta = self.get_time_delta()
            self.items.append(item)
            self.callback_item(item, spider=spider, delta=delta)
        finally:
            self.lock.release()

    def process_done(self, info):
        self.lock.acquire()
        try:
            self.time_end = time.time()
            self.delta = self.get_time_delta(self.time_end)
            self.callback_end(self.items, info=info, time_st=self.time_st, time_end=self.time_end, delta=self.delta)
        finally:
            self.lock.release()

    def callback_start(self, info=None, *args, **kwargs):
        pass

    def callback_item(self, item, spider, *args, **kwargs):
        pass

    def callback_end(self, items, info=None, *args, **kwargs):
        pass
