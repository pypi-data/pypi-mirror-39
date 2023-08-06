#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.visualiser.dlp_visualiser import DLPVisualiser

__author__ = 'cnheider'

import tensorflow as tf


class TFVisualiser(DLPVisualiser):

  @staticmethod
  def visualise_variable(variable):
    '''
    Attach summaries to a Tensor (for TensorBoard visualization).
    '''
    with tf.name_scope('summaries'):
      mean = tf.reduce_mean(variable)
      tf.summary.scalar('mean', mean)
      tf.summary.scalar('max', tf.reduce_max(variable))
      tf.summary.scalar('min', tf.reduce_min(variable))
      tf.summary.histogram('histogram', variable)

      with tf.name_scope('stddev'):
        stddev = tf.sqrt(tf.reduce_mean(tf.square(variable - mean)))
      tf.summary.scalar('stddev', stddev)
