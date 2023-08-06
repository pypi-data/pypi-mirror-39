# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys
import re
import logging
import json
import six
from functools import wraps
from datetime import datetime, date, time, timedelta
from dateutil import parser
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from scrapy.loader.processors import Compose, SelectJmes, MergeDict
from zhon.hanzi import punctuation, non_stops, stops
from nimbus_utils.urlparse import urlparse, urljoin, parse_qs, parse_qsl
from nimbus_utils.encoding import smart_text, smart_bytes, smart_str, force_str


__all__ = [
    "filter_price",
    "filter_trim",
    "filter_int",
    "filter_datetime",
    "filter_punctuation",
    "urlparse",
    "urljoin",
    "parse_qs",
    "parse_qsl",
]

INT = re.compile(r'\d')


def filter_price(value):
    if value.isdigit():
        return value


def filter_trim(value):
    if isinstance(value, (tuple, list)) and len(value) > 0:
        return value[0].strip()
    elif isinstance(value, six.string_types):
        return value.strip()
    return value


def filter_int(value):
    if isinstance(value, six.string_types):
        value = INT.findall(value)
        return value
    return value


def filter_datetime(value):
    if isinstance(value, (datetime, date, time)):
        return value
    elif isinstance(value, six.string_types):
        value = value.replace('[', '').replace(']', '')
        value = value.strip()
        value = parser.parse(value)
        return value
    return value


def filter_punctuation(value, repl=""):
    if isinstance(value, six.string_types):
        value = re.sub(r"[{}]+".format(punctuation), repl, value)
        return value
    return value



