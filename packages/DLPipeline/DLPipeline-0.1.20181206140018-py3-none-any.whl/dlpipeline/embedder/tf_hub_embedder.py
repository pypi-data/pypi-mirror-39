#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import sys
from random import randrange

from warg import NamedOrderedDictionary

from dlpipeline import get_image_path, ensure_directory_exists
from dlpipeline.utilities.transformation.data_iterator import DLPDataIterator
import tensorflow as tf
import numpy as np

__author__ = 'cnheider'

import tensorflow_hub as hub

# A module is understood as instrumented for quantization with TF-Lite
# if it contains any of these ops.
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')


class TFHubEmbedder(DLPDataIterator):

  def __init__(self, data_iterator: iter, *, C):
    super().__init__(data_iterator)
    self.build(C)
    self._C = C

  def build(self, C):
    '''
      flip_left_right: Boolean whether to randomly mirror images horizontally.
      random_crop: Integer percentage setting the total margin used around the
      crop box.
      random_scale: Integer percentage of how much to vary the scale by.
      random_brightness: Integer range to randomly multiply the pixel values by.
    '''

    module_specification = hub.load_module_spec(C.embedding_module)
    height, width = hub.get_expected_image_size(module_specification)
    depth = 3

    self.tf_config = tf.ConfigProto()
    self.tf_config.gpu_options.allow_growth = True
    self.tf_config.allow_soft_placement = True

    with tf.get_default_graph().as_default():
      with tf.Session(config=self.tf_config) as sess:

        self.embedder_input_node = tf.placeholder(tf.float32, [None, height, width, depth], name='embedding_input')
        module = hub.Module(module_specification)
        self.embedding_output_node = module(self.embedder_input_node)
        quantize = any(node.op in FAKE_QUANT_OPS for node in tf.get_default_graph().as_graph_def().node)



    self.module_specification = module_specification
    self.quantize = quantize
    self.input_size = hub.get_expected_image_size(self.module_specification)
    self.depth_size = hub.get_num_image_channels(self.module_specification)
    self.batch_size, self.embedding_size = self.embedding_output_node.get_shape().as_list()

  def fetch_data(self,
                 transformer,
                 dataset,
                 *,
                 batch_size=64,
                 C,
                 sub_set='training'):
    '''
    Get a batch of input embedding values, either calculated fresh every
     time with distortions applied, or from the cache stored on disk.
    '''
    if transformer.will_preprocess:
      (features, label) = self.get_random_distorted_embeddings_online(
          dataset,
          sub_set,
          input_jpeg_tensor=transformer.distorted_image_node,
          distorted_image=transformer.distorted_jpeg_node,
          batch_size=C.batch_size)
    else:
      (features, label, _) = self.get_random_cached_embeddings(
          dataset,
          sub_set,
          jpeg_data_tensor=transformer.jpeg_node,
          decoded_image_tensor=transformer.decoded_image_node,
          batch_size=batch_size)

    return features, label

  def create_embedding_file(self,
                            *,
                            embedding_path,
                            dataset,
                            label_name,
                            index,
                            category,
                            image_date_node,
                            decoded_image_node
                            ):
    '''
    Create a single embedding file.
    '''

    print('Creating embedding at ' + embedding_path)
    image_path = get_image_path(dataset=dataset,
                                label_name=label_name,
                                index=index,
                                set=category)

    if not tf.gfile.Exists(image_path):
      tf.logging.fatal(f'File does not exist {image_path}', )

    image_data = tf.gfile.GFile(image_path, 'rb').read()

    try:
      embedding_values = self.run_embedding_on_image(image_data,
                                                     image_data_node=image_date_node,
                                                     decoded_image_node=decoded_image_node)
    except Exception as e:
      raise RuntimeError(f'Error during processing file {image_path} ({e})')

    embedding_string = ','.join(str(x) for x in embedding_values)

    with open(embedding_path, 'w') as embedding_file:
      embedding_file.write(embedding_string)

  def get_or_create_embedding(self,
                              dataset,
                              *,
                              label_name,
                              index,
                              category,
                              image_data_node,
                              decoded_image_node):
    '''
    Retrieves or calculates embedding values for an image.

    If a cached version of the embedding data exists on-disk, return that,
    otherwise calculate the data and save it to disk for future use.

    Args:
      sess: The current active TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      label_name: Label string we want to get an image for.
      index: Integer offset of the image we want. This will be modulo-ed by the
      available number of images for the label, so it can be arbitrarily large.
      category: Name string of which set to pull images from - training, testing,
      or validation.
      embedding_directory: Folder string holding cached files of embedding values.
      image_data_node: The tensor to feed loaded jpeg data into.
      decoded_image_node: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The output tensor for the embedding values.
      embedding_module: The name of the image module being used.

    Returns:
      Numpy array of values produced by the embedding layer for the image.
    '''

    sub_directory_path = os.path.join(self._C.embedding_directory, label_name)
    ensure_directory_exists(sub_directory_path)
    embedding_file_path = self.get_embedding_path(dataset,
                                                  label_name,
                                                  index,
                                                  category
                                                  )

    if embedding_file_path is None:
      return None

    if not os.path.exists(embedding_file_path):
      self.create_embedding_file(embedding_path=embedding_file_path,
                                 dataset=dataset,
                                 label_name=label_name,
                                 index=index,
                                 category=category,
                                 image_date_node=image_data_node,
                                 decoded_image_node=decoded_image_node)

    with open(embedding_file_path, 'r') as embedding_file:
      embedding_string = embedding_file.read()

    did_hit_error = False
    embedding_values = None

    try:
      embedding_values = [float(x) for x in embedding_string.split(',')]
    except ValueError:
      tf.logging.warning('Invalid float found, recreating embedding')
      did_hit_error = True

    if did_hit_error:
      self.create_embedding_file(embedding_path=embedding_file_path,
                                 dataset=dataset,
                                 label_name=label_name,
                                 index=index,
                                 category=category,
                                 image_date_node=image_data_node,
                                 decoded_image_node=decoded_image_node)

      with open(embedding_file_path, 'r') as embedding_file:
        embedding_string = embedding_file.read()
      # Allow exceptions to propagate here, since they shouldn't happen after a
      # fresh creation
      embedding_values = [float(x) for x in embedding_string.split(',')]

    return embedding_values

  def run_embedding_on_image(self,
                             image_data,
                             *,
                             image_data_node,
                             decoded_image_node):
    '''Runs inference on an image to extract the 'embedding' summary layer.

    Args:
      sess: Current active TensorFlow Session.
      image_data: String of raw JPEG data.
      image_data_node: Input data layer in the graph.
      decoded_image_node: Output of initial image resizing and preprocessing.

    Returns:
      Numpy array of embedding values.
    '''
    # First decode the JPEG image, resize it, and rescale the pixel values.

    with tf.get_default_graph().as_default():
      with tf.Session(config=self.tf_config) as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.tables_initializer())

        resized_input_values = sess.run(decoded_image_node,
                                        feed_dict={image_data_node:image_data})

        embedding_values = sess.run(self.embedding_output_node,
                                    feed_dict={self.embedder_input_node:resized_input_values})

    embedding_values = np.squeeze(embedding_values)

    return embedding_values

  def cache_embeddings(self,
                       dataset,
                       *,
                       image_data_node,
                       decoded_image_node,
                       ):
    '''Ensures all the training, testing, and validation embeddings are cached.

    Because we're likely to read the same image multiple times (if there are no
    distortions applied during training) it can speed things up a lot if we
    calculate the embedding layer values once for each image during
    preprocessing, and then just read those cached values repeatedly during
    training. Here we go through all the images we've found, calculate those
    values, and save them off.

    Args:
      sess: The current active TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      image_directory: Root folder string of the subfolders containing the training
      images.
      embedding_directory: Folder string holding cached files of embedding values.
      image_data_node: Input tensor for jpeg data from file.
      decoded_image_node: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The penultimate output layer of the graph.
      embedding_module: The name of the image module being used.

    Returns:
      Nothing.
    '''

    how_many_embeddings = 0
    ensure_directory_exists(self._C.embedding_directory)

    with tf.Session(config=self.tf_config) as sess:
      for label_name, label_lists in dataset.items():
        for category in ['training', 'testing', 'validation']:
          category_list = label_lists[category]

          for index, unused_base_name in enumerate(category_list):
            ret = self.get_or_create_embedding(dataset,
                                               label_name=label_name,
                                               index=index,
                                               category=category,
                                               image_data_node=image_data_node,
                                               decoded_image_node=decoded_image_node)
            if ret is None:
              return None

            how_many_embeddings += 1
            if how_many_embeddings % 100 == 0:
              tf.logging.info(
                  f'{str(how_many_embeddings)} embedding files created.')

  def get_random_cached_embeddings(self,
                                   dataset,
                                   category,
                                   *,
                                   jpeg_data_tensor,
                                   decoded_image_tensor,
                                   batch_size,
                                   **kwargs
                                   ):
    '''Retrieves embedding values for cached images.

    If no distortions are being applied, this function can retrieve the cached
    embedding values directly from disk for images. It picks a random set of
    images from the specified category.

    Args:
      sess: Current TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      batch_size: If positive, a random sample of this size will be chosen.
      If negative, all embeddings will be retrieved.
      category: Name string of which set to pull from - training, testing, or
      validation.
      embedding_directory: Folder string holding cached files of embedding values.
      image_directory: Root folder string of the subfolders containing the training
      images.
      jpeg_data_tensor: The layer to feed jpeg image data into.
      decoded_image_tensor: The output of decoding and resizing the image.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The embedding output layer of the CNN graph.
      embedding_module: The name of the image module being used.

    Returns:
      List of embedding arrays, their corresponding ground truths, and the
      relevant filenames.
    '''
    embeddings = []
    ground_truths = []
    filenames = []
    if batch_size > 0:
      for unused_i in range(batch_size):
        label_index = randrange(dataset.class_count)
        label_name = list(dataset.keys())[label_index]
        image_index = randrange(sys.maxsize + 1)
        image_name = get_image_path(dataset=dataset,
                                    label_name=label_name,
                                    index=image_index,
                                    set=category)

        embedding = self.get_or_create_embedding(
            dataset,
            label_name=label_name,
            index=image_index,
            category=category,
            image_data_node=jpeg_data_tensor,
            decoded_image_node=decoded_image_tensor
            )
        if embedding is None:
          return None

        embeddings.append(embedding)
        ground_truths.append(label_index)
        filenames.append(image_name)
    else:
      for label_index, label_name in enumerate(dataset.keys()):
        for image_index, image_name in enumerate(dataset[label_name][category]):
          image_name = get_image_path(dataset=dataset,
                                      label_name=label_name,
                                      index=image_index,
                                      set=category)
          embedding = self.get_or_create_embedding(
              dataset,
              label_name=label_name,
              index=image_index,
              category=category,
              image_data_node=jpeg_data_tensor,
              decoded_image_node=decoded_image_tensor)
          if embedding is None:
            return None

          embeddings.append(embedding)
          ground_truths.append(label_index)
          filenames.append(image_name)

    return embeddings, ground_truths, filenames

  def get_random_distorted_embeddings_online(self,
                                             dataset,
                                             category,
                                             *,
                                             input_jpeg_tensor,
                                             distorted_image,
                                             batch_size,
                                             **kwargs
                                             ):
    '''
    Retrieves embedding values for training images, after distortions.

    If we're training with distortions like crops, scales, or flips, we have to
    recalculate the full classifier for every image, and so we can't use cached
    embedding values. Instead we find random images for the requested category,
    run them through the distortion graph, and then the full graph to get the
    embedding results for each.

    Args:
      sess: Current TensorFlow Session.
      dataset: OrderedDict of training images for each label.
      how_many: The integer number of embedding values to return.
      category: Name string of which set of images to fetch - training, testing,
      or validation.
      image_directory: Root folder string of the subfolders containing the training
      images.
      input_jpeg_tensor: The input layer we feed the image data to.
      distorted_image: The output node of the distortion graph.
      resized_input_tensor: The input node of the recognition graph.
      embedding_output_node: The embedding output layer of the CNN graph.

    Returns:
      List of embedding arrays and their corresponding ground truths.
      :param sess:
      :param dataset:
      :param category:
      :param input_jpeg_tensor:
      :param distorted_image:
      :param resized_input_tensor:
      :param embedding_output_node:
      :param batch_size:
    '''

    assert batch_size > 0

    embeddings = []
    ground_truths = []
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.allow_soft_placement = True

    with tf.Session(config=config) as sess:
      for unused_i in range(batch_size):
        label_index = random.randrange(dataset.class_count)
        label_name = list(dataset.keys())[label_index]
        image_index = random.randrange(sys.maxsize + 1)
        image_path = get_image_path(dataset=dataset,
                                    label_name=label_name,
                                    index=image_index,
                                    set=category)
        if not tf.gfile.Exists(image_path):
          tf.logging.fatal(f'File does not exist {image_path}')
        jpeg_data = tf.gfile.GFile(image_path, 'rb').read()
        # Note that we materialize the distorted_image_data as a numpy array before
        # sending running inference on the image. This involves 2 memory copies and
        # might be optimized in other implementations.

        distorted_image_data = sess.run(distorted_image,
                                        {input_jpeg_tensor:jpeg_data})
        embedding_values = sess.run(self.embedding_output_node,
                                    feed_dict={self.embedder_input_node:distorted_image_data})
        embedding_values = np.squeeze(embedding_values)
        embeddings.append(embedding_values)
        ground_truths.append(label_index)

    return embeddings, ground_truths

  def get_embedding_path(self,
                         dataset,
                         label_name,
                         index,
                         category):
    '''
    Returns a path to a embedding file for a label at the given index.

    Args:
      dataset: OrderedDict of training images for each label.
      label_name: Label string we want to get an image for.
      index: Integer offset of the image we want. This will be moduloed by the
      available number of images for the label, so it can be arbitrarily large.
      embedding_directory: Folder string holding cached files of embedding values.
      category: Name string of set to pull images from - training, testing, or
      validation.

    Returns:
      File system path string to an image that meets the requested parameters.
    '''
    module_name = (self._C.embedding_module.replace('://', '~')  # URL scheme.
                   .replace('/', '~')  # URL and Unix paths.
                   .replace(':', '~').replace('\\', '~'))  # Windows paths.

    i_path = get_image_path(dataset=dataset,
                            label_name=label_name,
                            index=index,
                            set=category)

    if i_path is None:
      return None

    name = os.path.split(i_path)[1]

    e_path = f'{self._C.embedding_directory}/{label_name}/{name}'

    return e_path + '_' + module_name + '.txt'
