#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dlpipeline.utilities import DLPDataIterator
from dlpipeline.data_loader.image_sets import build_deep_level_image_list
from dlpipeline.data_loader.image_sets.first_level_label import build_first_level_image_list
from dlpipeline.utilities.path_utilities.directory_exists import ensure_directory_exists

__author__ = 'cnheider'

import tensorflow as tf


class DataLoader(DLPDataIterator):
  def __init__(self, C=None, first_level_categories=True):
    super().__init__()

    self._first_level = first_level_categories

    if C:
      self.load(C)

  def load(self, C):
    if not C.image_directory:
      tf.logging.error('Must set flag --image_directory.')
      return -1

    # Set up the directory we'll write summaries to for TensorBoard
    if tf.gfile.Exists(C.summaries_directory):
      pass
      # tf.gfile.DeleteRecursively(summaries_directory)
    else:
      tf.gfile.MakeDirs(C.summaries_directory)

    if C.intermediate_store_frequency > 0:
      ensure_directory_exists(C.intermediate_output_graphs_directory)

    if self._first_level:
      self._data_iterator = build_first_level_image_list(**vars(C))
    else:
      self._data_iterator = build_deep_level_image_list(**vars(C))

    if not self._data_iterator:
      raise EnvironmentError

    self._class_count = len(self._data_iterator.keys())
    if self._class_count == 0:
      tf.logging.error(f'No valid folders of images found at {C.image_directory}')
      return -1
    if self._class_count == 1:
      tf.logging.error(
          f'Only one valid folder of images found at {C.image_directory} - multiple classes are '
          f'needed for classification.')
      return -1

    for label, sets in self._data_iterator.items():
      for set, instances in sets.items():
        print(f'Class {label}, {set} has {len(instances)} instances')

    return self

  @property
  def image_list(self):
    return self._data_iterator

  @property
  def class_count(self):
    return self._class_count

  def keys(self):
    return self._data_iterator.keys()

  def __iter__(self):
    return self.items().__iter__()

  def items(self):
    return self._data_iterator.items()

  def __getitem__(self, item):
    return self._data_iterator.get(item)

  def __len__(self):
    return len(self.items())

  def __contains__(self, item):
    return self._data_iterator[item] is not None
