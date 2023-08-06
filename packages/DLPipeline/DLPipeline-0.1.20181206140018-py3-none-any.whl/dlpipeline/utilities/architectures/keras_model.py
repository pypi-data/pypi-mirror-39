#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from exclude.keras_func import save_model_callback
from exclude.old import save_model_path

__author__ = 'cnheider'

import tensorflow as tf


def create_model():
  '''

  :return: a short sequential classifier
  '''
  _model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

  _model.compile(optimizer=tf.train.AdamOptimizer(),
                 loss=tf.keras.losses.sparse_categorical_crossentropy,
                 metrics=['accuracy'])

  return _model


if __name__ == '__main__':
  import sample_experiments.config.base_config as config
  from dlpipeline.utilities.persistence.load import load_lastest_model

  if not config:
    config = {}

  (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

  train_labels = train_labels[:1000]
  test_labels = test_labels[:1000]

  train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
  test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

  model = create_model()

  model.fit(train_images, train_labels, epochs=10,
            validation_data=(test_images, test_labels),
            callbacks=[save_model_callback])  # pass callback to training

  model = create_model()
  loss, acc = model.evaluate(test_images, test_labels)
  print(f'Trained classifier, accuracy: {100 * acc:5.2f}%')

  latest = load_lastest_model(save_model_path)

  loaded_model = create_model()
  loaded_model.load_weights(latest)
  loss_l, acc_l = loaded_model.evaluate(test_images, test_labels)
  print(f'Restored classifier, accuracy: {100 * acc_l:5.2f}%')
