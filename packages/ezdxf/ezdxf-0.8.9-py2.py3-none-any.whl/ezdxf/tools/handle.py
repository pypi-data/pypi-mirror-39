# Purpose: handle module
# Created: 11.03.2011
# Copyright (c) 2011-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals


class HandleGenerator(object):
    def __init__(self, start_value='1'):
        self._handle = int(start_value, 16)
    reset = __init__

    def __str__(self):
        return "%X" % self._handle

    def next(self):
        next_handle = self.__str__()
        self._handle += 1
        return next_handle
    __next__ = next


class ImageKeyGenerator(HandleGenerator):
    def __str__(self):
        return "Image%05d" % self._handle


class UnderlayKeyGenerator(HandleGenerator):
    def __str__(self):
        return "Underlay%05d" % self._handle
