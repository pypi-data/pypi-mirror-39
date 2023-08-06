#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from dlpipeline.data_loader.image_sets import ACCEPTED_FORMATS, test_validation_split

__author__ = 'cnheider'

import tensorflow as tf


def build_first_level_image_list(image_directory,
                                 *,
                                 testing_percentage=15,
                                 validation_percentage=15,
                                 **kwargs):
  '''
  Builds a list of training images from the file system.

  Analyzes the sub folders in the image directory, splits them into stable
  training, testing, and validation sets, and returns a data structure
  describing the lists of images for each label and their paths.

  Args:
    image_directory: String path to a folder containing subfolders of images.
    testing_percentage: Integer percentage of the images to reserve for tests.
    validation_percentage: Integer percentage of images reserved for validation.

  Returns:
    An OrderedDict containing an entry for each label subfolder, with images
    split into training, testing, and validation sets within each label.
    The order of items defines the class indices.
  '''

  if not tf.gfile.Exists(image_directory):
    dir_err = f"Image directory {image_directory} not found."
    tf.logging.error(dir_err)
    print(dir_err)
    return None

  class_directories = next(tf.gfile.Walk(image_directory))[1]

  classes = {label:[] for label in class_directories}

  for class_directory in classes:
    a = [x[0] for x in tf.gfile.Walk(os.path.join(image_directory, class_directory))]
    sub_directories = sorted(a)

    for sub_directory in sub_directories:
      tf.logging.info(f"Looking for images in {sub_directory}")

      file_extensions = sorted(set(os.path.normcase(ext)
                                   for ext in ACCEPTED_FORMATS))

      for extension in file_extensions:
        file_glob = os.path.join(sub_directory, '*.' + extension)
        this_glob = tf.gfile.Glob(file_glob)
        classes[class_directory].extend(this_glob)

  result = test_validation_split(classes,
                                 testing_percentage=testing_percentage,
                                 validation_percentage=validation_percentage)

  return result
