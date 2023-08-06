#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import tensorflow as tf
import tensornets as nets


def transfer_vgg_net(x):
  logits = nets.VGG19(x, is_training=True, classes=10)
  model = tf.identity(logits, name='logits')
  return logits, model
