# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import json
import time
import signal
from collections import OrderedDict
from pydispatch import dispatcher
from twisted.internet import reactor, defer
from scrapy import signals
from scrapy.spiders import Spider
from scrapy.resolver import CachingThreadedResolver
from multiprocessing import Process, Lock, Queue, current_process
from multiprocessing import Pool, Manager
import multiprocessing as mp
from .crawler import CrawlerRunner, CrawlerProcess
from ..settings import update_settings

__all__ = [
    "BaseWorker",
    "CrawlerRunnerWorker",
    "CrawlerProcessWorker",
    "CrawlerCallback",
    "start_spider_by_process",
    "start_spider_by_runner",
    "stop_spider",
]


def _process_init():
    try:
        import psutil
        ps = psutil.Process(os.getpid())
        if not psutil.WINDOWS:
            ps.nice(19)
        else:
            ps.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception as e:
        pass


class BaseWorker(Process):

    def __init__(self, group=None, target=None, name=None, daemon=False):
        super(BaseWorker, self).__init__(group=group, target=target, name=name)
        self.daemon = daemon
        self.spider = None
        self.settings = {}
        self.args = None
        self.kwargs = None
        self.callback = None
        self.stop_after_crawl = True

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

    def start(self, spider=None, callback=None, settings=None, stop_after_crawl=True, *args, **kwargs):
        self.spider = spider
        self.settings = update_settings(settings)
        self.stop_after_crawl = stop_after_crawl
        self.args = args
        self.kwargs = kwargs
        self.callback = callback if callback and isinstance(callback, CrawlerCallback) else CrawlerCallback()
        dispatcher.connect(self._item_passed, signals.item_passed)
        dispatcher.connect(self._spider_closed, signals.spider_closed)
        super(BaseWorker, self).start()

    def run(self, *args, **kwargs):
        _process_init()
        self.callback.process_start(info=self.info)
        crawler = self.get_crawler()
        crawler.crawl(self.spider, *self.args, **self.kwargs)
        crawler.start(self.stop_after_crawl)
        crawler.stop()
        self.callback.process_done(info=self.info)
        self.clean()

    def clean(self):
        self.spider = None
        self.settings = {}
        self.args = None
        self.kwargs = None
        self.callback = None

    def _item_passed(self, item, spider=None):
        self.callback.process_item(item=item, spider=spider)

    def _spider_closed(self, *args, **kwargs):
        try:
            reactor.stop()
        except RuntimeError:
            pass
        
    def get_crawler(self):
        raise NotImplementedError


class CrawlerRunnerWorker(BaseWorker):

    def get_crawler(self):
        return CrawlerRunner(self.settings)


class CrawlerProcessWorker(BaseWorker):

    def get_crawler(self):
        return CrawlerProcess(self.settings)


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

    def release(self):
        self.lock.release()

    def callback_start(self, info=None, *args, **kwargs):
        pass

    def callback_item(self, item, spider, *args, **kwargs):
        pass

    def callback_end(self, items, info=None, *args, **kwargs):
        pass


def start_spider_by_process(spider, callback=None, settings=None, stop_after_crawl=True, *args, **kwargs):
    callback = callback if callback and isinstance(callback, CrawlerCallback) else CrawlerCallback()

    def _item_passed(item, spider=None):
        callback.process_item(item=item, spider=spider)

    def _spider_closed(*args, **kwargs):
        try:
            callback.release()
            reactor.stop()
        except RuntimeError:
            pass

    def _get_info():
        return {
            "name": spider.name,
            "cpus": mp.cpu_count(),
            "ppid": os.getppid(),
            "pid": os.getpid(),
        }

    _process_init()
    dispatcher.connect(_item_passed, signals.item_passed)
    dispatcher.connect(_spider_closed, signals.spider_closed)
    dfs = list()
    settings = update_settings(settings)
    info = _get_info()
    callback.process_start(info=info)
    crawler = CrawlerProcess(settings)
    d = crawler.crawl(spider, *args, **kwargs)
    dfs.append(d)
    defer.DeferredList(dfs).addBoth(lambda _: _spider_closed())
    crawler.start(stop_after_crawl=stop_after_crawl)
    crawler.stop()
    callback.process_done(info=info)


def start_spider_by_runner(spider, callback=None, settings=None, stop_after_crawl=True, *args, **kwargs):
    callback = callback if callback and isinstance(callback, CrawlerCallback) else CrawlerCallback()

    def _item_passed(item, spider=None):
        callback.process_item(item=item, spider=spider)

    def _spider_closed(*args, **kwargs):
        try:
            callback.release()
            reactor.stop()
        except RuntimeError:
            pass

    def _get_info():
        return {
            "name": spider.name,
            "cpus": mp.cpu_count(),
            "ppid": os.getppid(),
            "pid": os.getpid(),
        }

    _process_init()
    dfs = list()
    dispatcher.connect(_item_passed, signals.item_passed)
    dispatcher.connect(_spider_closed, signals.spider_closed)
    settings = update_settings(settings)
    info = _get_info()
    callback.process_start(info=info)
    crawler = CrawlerRunner(settings)
    d = crawler.crawl(spider, *args, **kwargs)
    dfs.append(d)
    defer.DeferredList(dfs).addBoth(lambda _: _spider_closed())
    crawler.start(stop_after_crawl=stop_after_crawl)
    crawler.stop()
    callback.process_done(info=info)


def stop_spider(pid=1):
    try:
        os.killpg(pid, signal.SIGKILL)
        if os.waitpid(pid, os.WNOHANG) == (0, 0):
            return True
    except OSError as e:
        pass
    return False
