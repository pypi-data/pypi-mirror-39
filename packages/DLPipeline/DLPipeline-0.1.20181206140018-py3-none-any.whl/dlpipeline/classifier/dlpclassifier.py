#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.utilities.transformation.data_iterator import DLPDataIterator

__author__ = 'cnheider'


class DLPClassifier(DLPDataIterator):
  def __init__(self, dataset: iter, *, C):
    super().__init__(dataset)

  def learn(self, dataset: iter, *, C=None, **kwargs):
    raise NotImplementedError

  def predict(self, param: iter):
    raise NotImplementedError

  def summary(self):
    raise NotImplementedError

  def save(self, dataset, *, C):
    raise NotImplementedError

  def test(self, dataset, *, C):
    raise NotImplementedError
