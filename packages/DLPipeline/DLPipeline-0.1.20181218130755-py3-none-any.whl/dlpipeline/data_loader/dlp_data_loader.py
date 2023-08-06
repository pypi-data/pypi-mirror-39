#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
from warg import NamedOrderedDictionary as NOD
from dlpipeline.data_loader.image_sets import build_deep_level_image_list
from dlpipeline.data_loader.image_sets.first_level_label import build_first_level_image_list
from dlpipeline.utilities.path_utilities.directory_exists import ensure_directory_exists
from nisse import DataIterator

__author__ = 'cnheider'


class DLPDataLoader(DataIterator):
  def _entry_point(self, data_iterator):
    return self.items()

  def __init__(self,
               C=None,
               first_level_categories=True):
    super().__init__()

    self._first_level = first_level_categories

    if C:
      self.load(C.image_directory, C)

  def load(self, image_directory='', C=None):
    if not image_directory:
      tf.logging.error('Must set flag --image_directory.')
      return -1

    if self._first_level:
      self._iterable = build_first_level_image_list(**vars(C))
    else:
      self._iterable = build_deep_level_image_list(**vars(C))

    if not self._iterable:
      raise EnvironmentError

    self.satellite_data.class_count = len(self._iterable.keys())
    if self.satellite_data.class_count == 0:
      tf.logging.error(f'No valid folders of images found at {image_directory}')
      return -1
    if self.satellite_data.class_count == 1:
      tf.logging.error(
          f'Only one valid folder of images found at {image_directory} - multiple classes are '
          f'needed for classification.')
      return -1

    for label, sets in self._iterable.items():
      for set, instances in sets.items():
        print(f'Class {label}, {set} has {len(instances)} instances')

  @property
  def image_list(self):
    return self._iterable.items()

  @property
  def class_count(self):
    return self.satellite_data.class_count

  def keys(self):
    return self._iterable.keys()

  def __iter__(self):
    return self.items().__iter__()

  def items(self):
    return self._iterable.items()

  def __getitem__(self, item):
    return self._iterable.get(item)

  def __len__(self):
    return len(self.items())

  def __contains__(self, item):
    return item in self._iterable


def get_image_path(*,
                   dataset,
                   label_name,
                   index,
                   set):
  '''
  Returns a path to an image for a label at the given index.

  Args:
    dataset: OrderedDict of images for each label.
    label_name: Label string we want to get an image for.
    index: Int offset of the image we want. This will be moduloed by the
    available number of images for the label, so it can be arbitrarily large.
    image_directory: Root folder string of the subfolders containing the training
    images.
    set: Name string of set to pull images from - training, testing, or
    validation.

  Returns:
    File system path string to an image that meets the requested parameters.

  '''
  if label_name not in dataset:
    tf.logging.fatal(f'Label does not exist {label_name}.')
  label_lists = dataset[label_name]

  if set not in label_lists:
    tf.logging.fatal(f'Set does not exist {set}')
  set_a = label_lists[set]

  l = len(set_a)

  if not set_a or l == 0:
    tf.logging.fatal(f'Label {label_name} has no images in the category {set}.')
    return None

  mod_index = index % l
  base_name = set_a[mod_index]

  return base_name
