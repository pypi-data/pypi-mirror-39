#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nisse import DataIterator

__author__ = 'cnheider'


class DLPClassifier(DataIterator):
  def __init__(self, dataset: iter, *, C):
    super().__init__(dataset)

  def learn(self,
            dataset: iter,
            *,
            C=None,
            **kwargs):
    raise NotImplementedError

  def predict(self, param: iter):
    raise NotImplementedError

  def save(self, dataset, *, C):
    raise NotImplementedError

  def test(self, dataset, *, C):
    raise NotImplementedError
