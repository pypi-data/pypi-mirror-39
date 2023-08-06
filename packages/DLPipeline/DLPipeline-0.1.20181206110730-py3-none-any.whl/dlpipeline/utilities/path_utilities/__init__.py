#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import tensorflow as tf

__author__ = 'cnheider'


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


