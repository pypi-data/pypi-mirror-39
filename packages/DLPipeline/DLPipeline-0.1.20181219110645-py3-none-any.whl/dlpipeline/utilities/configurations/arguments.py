#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

__author__ = 'cnheider'


def parse_args(C):
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--image_directory',
      type=str,
      default=C.image_directory,
      help='Path to folders of labeled images.'
      )
  parser.add_argument(
      '--output_graph',
      type=str,
      default=C.output_graph,
      help='Where to save the trained graph.'
      )
  parser.add_argument(
      '--intermediate_output_graphs_directory',
      type=str,
      default=C.intermediate_output_graphs_directory,
      help='Where to save the intermediate graphs.'
      )
  parser.add_argument(
      '--intermediate_store_frequency',
      type=int,
      default=C.intermediate_store_frequency,
      help='''\
           How many steps to store intermediate graph. If "0" then will not
           store.\
        '''
      )
  parser.add_argument(
      '--output_labels',
      type=str,
      default=C.output_labels_file_name,
      help='Where to save the trained graph\'s labels.'
      )
  parser.add_argument(
      '--summaries_directory',
      type=str,
      default=C.model_directory,
      help='Where to save summary logs for TensorBoard.'
      )
  parser.add_argument(
      '--how_many_training_steps',
      type=int,
      default=C.steps,
      help='How many training steps to run before ending.'
      )
  parser.add_argument(
      '--learning_rate',
      type=float,
      default=C.learning_rate,
      help='How large a learning rate to use when training.'
      )
  parser.add_argument(
      '--testing_percentage',
      type=int,
      default=C.testing_percentage,
      help='What percentage of images to use as a test set.'
      )
  parser.add_argument(
      '--validation_percentage',
      type=int,
      default=C.validation_percentage,
      help='What percentage of images to use as a validation set.'
      )
  parser.add_argument(
      '--eval_step_interval',
      type=int,
      default=C.eval_step_interval,
      help='How often to evaluate the training results.'
      )
  parser.add_argument(
      '--train_batch_size',
      type=int,
      default=C.train_batch_size,
      help='How many images to train on at a time.'
      )
  parser.add_argument(
      '--test_batch_size',
      type=int,
      default=C.test_batch_size,
      help='''\
        How many images to test on. This test set is only used once, to evaluate
        the final accuracy of the classifier after training completes.
        A value of -1 causes the entire test set to be used, which leads to more
        stable results across runs.\
        '''
      )
  parser.add_argument(
      '--validation_batch_size',
      type=int,
      default=C.validation_batch_size,
      help='''\
        How many images to use in an evaluation batch. This validation set is
        used much more often than the test set, and is an early indicator of how
        accurate the classifier is during training.
        A value of -1 causes the entire validation set to be used, which leads to
        more stable results across training iterations, but may be slower on large
        training sets.\
        '''
      )
  parser.add_argument(
      '--print_misclassified_test_images',
      default=C.print_misclassified,
      help='''\
        Whether to print out a list of all misclassified test images.\
        ''',
      action='store_true'
      )
  parser.add_argument(
      '--embedding_directory',
      type=str,
      default=C.embedding_directory,
      help='Path to cache embedding layer values as files.'
      )
  parser.add_argument(
      '--final_node_name',
      type=str,
      default=C.final_node_name,
      help='''\
        The name of the output classification layer in the retrained graph.\
        '''
      )
  parser.add_argument(
      '--flip_left_right',
      default=C.flip_left_right,
      help='''\
        Whether to randomly flip half of the training images horizontally.\
        ''',
      action='store_true'
      )
  parser.add_argument(
      '--random_crop',
      type=int,
      default=C.random_crop,
      help='''\
        A percentage determining how much of a margin to randomly crop off the
        training images.\
        '''
      )
  parser.add_argument(
      '--random_scale',
      type=int,
      default=C.random_scale,
      help='''\
        A percentage determining how much to randomly scale up the size of the
        training images by.\
        '''
      )
  parser.add_argument(
      '--random_brightness',
      type=int,
      default=C.random_brightness,
      help='''\
        A percentage determining how much to randomly multiply the training image
        input pixels up or down by.\
        '''
      )
  parser.add_argument(
      '--tfhub_module',
      type=str,
      default=C.embedding_module
      ,
      help='''\
        Which TensorFlow Hub module to use.
        See https://github.com/tensorflow/hub/blob/master/docs/modules/image.md
        for some publicly available ones.\
        ''')

  parser.add_argument(
      '--saved_model_directory',
      type=str,
      default=C.saved_model_directory,
      help='Where to save the exported graph.')
  FLAGS, unparsed = parser.parse_known_args()

  C.update(FLAGS.__dict__)
  return C
