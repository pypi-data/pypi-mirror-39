# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
from twisted.internet import reactor, defer
from scrapy.resolver import CachingThreadedResolver
from scrapy.crawler import CrawlerProcess as ScrapyCrawlerProcess
from scrapy.crawler import CrawlerRunner as ScrapyCrawlerRunner

__all__ = [
    "CrawlerProcess",
    "CrawlerRunner",
]


class CrawlerProcess(ScrapyCrawlerProcess):

    def __init__(self, settings=None, install_root_handler=True):
        super(CrawlerProcess, self).__init__(settings, install_root_handler)


class CrawlerRunner(ScrapyCrawlerRunner):

    def __init__(self, settings=None):
        super(CrawlerRunner, self).__init__(settings)

    def start(self, stop_after_crawl=True):
        if stop_after_crawl:
            d = self.join()
            # Don't start the reactor if the deferreds are already fired
            if d.called:
                return
            d.addBoth(self._graceful_stop_reactor)
        reactor.installResolver(self._get_dns_resolver())
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call

    def _get_dns_resolver(self):
        if self.settings.getbool('DNSCACHE_ENABLED'):
            cache_size = self.settings.getint('DNSCACHE_SIZE')
        else:
            cache_size = 0
        return CachingThreadedResolver(
            reactor=reactor,
            cache_size=cache_size,
            timeout=self.settings.getfloat('DNS_TIMEOUT')
        )

    def _graceful_stop_reactor(self, *args, **kwargs):
        d = self.stop()
        d.addBoth(self._stop_reactor)
        return d

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError:  # raised if already stopped or in shutdown stage
            pass
