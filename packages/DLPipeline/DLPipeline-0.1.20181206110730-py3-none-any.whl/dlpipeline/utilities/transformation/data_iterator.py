#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'cnheider'

from abc import abstractmethod
from collections import Iterable
from typing import Iterator


class DLPDataIterator(object):
  def __init__(self, data_iterator: iter = None):
    self._data_iterator = data_iterator

  def __iter__(self) -> Iterator:
    return self.entry_point(self._data_iterator).__iter__()

  @abstractmethod
  def entry_point(self, data_iterator) -> Iterable:
    pass

  def keys(self):
    return self._data_iterator.keys()

  def class_count(self):
    return len(self._data_iterator.keys())
