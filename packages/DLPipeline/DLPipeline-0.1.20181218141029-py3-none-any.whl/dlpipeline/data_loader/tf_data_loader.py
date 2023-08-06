#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
from warg import NamedOrderedDictionary as NOD

from dlpipeline.data_loader.dlp_data_loader import DLPDataLoader

__author__ = 'cnheider'


class TFDataLoader(DLPDataLoader):
  def _entry_point(self,
                   data_iterator,
                   sess):
    if sess:
      return sess.run(self.resized_image_node, feed_dict={self.jpeg_placeholder:data_iterator})

    return self.items()

  def _build(self,
             *,
               height,
               width,
               depth,
               **kwargs):

    (self.jpeg_placeholder, self.resized_image_node) = self.add_jpeg_decoding_resize(height,
                                                                                     width,
                                                                                     depth).as_list()

  @staticmethod
  def add_jpeg_decoding_resize(input_height, input_width, input_depth):
    '''
    Adds operations that perform JPEG decoding and resizing to the graph..

    Args:
      module_spec: The hub.ModuleSpec for the image module being used.

    Returns:
      Tensors for the node to feed JPEG data into, and the output of the
        preprocessing steps.
    '''

    jpeg_placeholder = tf.placeholder(tf.string, name='jpeg_placeholder')
    decoded_image = tf.image.decode_jpeg(jpeg_placeholder, channels=input_depth)

    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image, tf.float32)
    # Convert from full range of uint8 to range [0,1] of float32.

    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    resize_shape = tf.stack([input_height, input_width])
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image_node = tf.image.resize_bilinear(decoded_image_4d, resize_shape_as_int)

    return NOD(jpeg_placeholder=jpeg_placeholder, resized_image_node=resized_image_node)
