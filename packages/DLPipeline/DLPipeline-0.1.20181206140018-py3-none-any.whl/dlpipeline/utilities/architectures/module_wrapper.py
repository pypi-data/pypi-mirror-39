#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import tensorflow as tf

from dlpipeline.utilities.architectures import transfer_vgg_net


class TrainableModule(object):
  def __init__(self):
    super().__init__()

  def build(self, input_dim: tuple = (6,), output_dim: tuple = (2,), learning_rate=3e-4):
    self._x = tf.placeholder(tf.float32, shape=(None, *input_dim), name='input_x')
    self._y = tf.placeholder(tf.float32, shape=(None, *output_dim), name='output_y')

    self._logits, self._model = transfer_vgg_net(self._x)

    self._loss = tf.losses.softmax_cross_entropy(self._y, self._logits)
    self._train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self._loss)

    self._correct_pred = tf.equal(tf.argmax(self._model, 1), tf.argmax(self._y, 1))
    self._accuracy = tf.reduce_mean(tf.cast(self._correct_pred, tf.float32), name='accuracy')

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._x

  @property
  def logits(self):
    return self._logits

  @property
  def loss(self):
    return self._loss

  @property
  def train(self):
    return self._train

  @property
  def correct_pred(self):
    return self._correct_pred

  @property
  def accuracy(self):
    return self._accuracy
