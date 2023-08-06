#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warg import NamedOrderedDictionary

from dlpipeline.utilities.transformation import add_jpeg_decoding
from dlpipeline.utilities.transformation.data_iterator import DLPDataIterator

__author__ = 'cnheider'

import tensorflow as tf


class TFAugmentor(DLPDataIterator):
  def __init__(self, data_iterator, *, C,
               input_size,
               depth_size,
               ):
    super().__init__(data_iterator)

    self._will_preprocess = (C.flip_left_right or
                             (C.random_crop != 0) or
                             (C.random_scale != 0) or
                             (C.random_brightness != 0)) if C else False

    self.build(
        input_size=input_size,
        depth=depth_size,
        C=C)

  @property
  def will_preprocess(self):
    return self._will_preprocess

  def build(self,
            *,
            input_size,
            depth,

            C):
    self.tf_config = tf.ConfigProto()
    self.tf_config.gpu_options.allow_growth = True
    self.tf_config.allow_soft_placement = True

    with tf.Session(config=self.tf_config) as sess:
      sess.run(tf.global_variables_initializer())

      (jpeg_data_node, decoded_image_node) = add_jpeg_decoding(input_size, depth=depth).as_list()

      (distorted_jpeg_data_node, distorted_image_node) = self.add_input_augmentation(input_size,
                                                                                     depth,
                                                                                     **vars(C)).as_list()

    self.jpeg_node=jpeg_data_node,
    self.decoded_image_node=decoded_image_node
    self.distorted_jpeg_node=distorted_jpeg_data_node
    self.distorted_image_node=distorted_image_node

  @staticmethod
  def add_input_augmentation(
      input_size,
      depth_size,
      *,
      flip_left_right,
      random_crop,
      random_scale,
      random_brightness,
      **kwargs):
    '''Creates the operations to apply the specified distortions.

    During training it can help to improve the results if we run the images
    through simple distortions like crops, scales, and flips. These reflect the
    kind of variations we expect in the real world, and so can help train the
    classifier to cope with natural data more effectively. Here we take the supplied
    parameters and construct a network of operations to apply them to an image.

    Cropping
    ~~~~~~~~

    Cropping is done by placing a bounding box at a random position in the full
    image. The cropping parameter controls the size of that box relative to the
    input image. If it's zero, then the box is the same size as the input and no
    cropping is performed. If the value is 50%, then the crop box will be half the
    width and height of the input. In a diagram it looks like this:

    <       width         >
    +---------------------+
    |                     |
    |   width - crop%     |
    |    <      >         |
    |    +------+         |
    |    |      |         |
    |    |      |         |
    |    |      |         |
    |    +------+         |
    |                     |
    |                     |
    +---------------------+

    Scaling
    ~~~~~~~

    Scaling is a lot like cropping, except that the bounding box is always
    centered and its size varies randomly within the given range. For example if
    the scale percentage is zero, then the bounding box is the same size as the
    input and no scaling is applied. If it's 50%, then the bounding box will be in
    a random range between half the width and height and full size.

    Args:
      flip_left_right: Boolean whether to randomly mirror images horizontally.
      random_crop: Integer percentage setting the total margin used around the
      crop box.
      random_scale: Integer percentage of how much to vary the scale by.
      random_brightness: Integer range to randomly multiply the pixel values by.
      graph.
      input_size: The hub.ModuleSpec for the image module being used.

    Returns:
      The jpeg input layer and the distorted result tensor.
    '''

    input_height, input_width = input_size
    input_depth = depth_size

    jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    # Convert from full range of uint8 to range [0,1] of float32.
    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image,
                                                          tf.float32)

    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    margin_scale = 1.0 + (random_crop / 100.0)
    resize_scale = 1.0 + (random_scale / 100.0)
    margin_scale_value = tf.constant(margin_scale)
    resize_scale_value = tf.random_uniform(shape=[],
                                           minval=1.0,
                                           maxval=resize_scale)

    scale_value = tf.multiply(margin_scale_value, resize_scale_value)
    precrop_width = tf.multiply(scale_value, input_width)
    precrop_height = tf.multiply(scale_value, input_height)
    precrop_shape = tf.stack([precrop_height, precrop_width])
    precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
    precropped_image = tf.image.resize_bilinear(decoded_image_4d,
                                                precrop_shape_as_int)

    precropped_image_3d = tf.squeeze(precropped_image, axis=[0])
    cropped_image = tf.random_crop(precropped_image_3d,
                                   [input_height, input_width, input_depth])
    if flip_left_right:
      flipped_image = tf.image.random_flip_left_right(cropped_image)
    else:
      flipped_image = cropped_image
    brightness_min = 1.0 - (random_brightness / 100.0)
    brightness_max = 1.0 + (random_brightness / 100.0)
    brightness_value = tf.random_uniform(shape=[],
                                         minval=brightness_min,
                                         maxval=brightness_max)
    brightened_image = tf.multiply(flipped_image, brightness_value)
    distort_result = tf.expand_dims(brightened_image, 0, name='DistortResult')
    return NamedOrderedDictionary(jpeg_data, distort_result)
