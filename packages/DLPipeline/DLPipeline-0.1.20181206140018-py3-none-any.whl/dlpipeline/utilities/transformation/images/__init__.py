#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle

import skimage

__author__ = 'cnheider'


def batch_features_labels(features, labels, batch_size):
  '''
  Split features and labels into batches
  '''
  for start in range(0, len(features), batch_size):
    end = min(start + batch_size, len(features))
    yield features[start:end], labels[start:end]


def load_preprocessed_training_batch(batch_id, batch_size):
  '''
  Load the Preprocessed Training data and return them in batches of <batch_size> or less
  '''
  filename = f'preprocess_batch_{batch_id}.p'
  features, labels = pickle.load(open(filename, mode='rb'))

  tmp_features = []

  for feature in features:
    tmpFeature = skimage.transform.resize(feature, (224, 224), mode='constant')
    tmp_features.append(tmpFeature)

  # Return the training data in batches of size <batch_size> or less
  return batch_features_labels(tmp_features, labels, batch_size)


def load_preprocessed_batched(path, batch_size=64):
  '''
  Load the Preprocessed data and return them in batches of <batch_size> or less
  '''

  features, labels = pickle.load(open(path, mode='rb'))

  tmp_features = []

  for feature in features:
    tmpFeature = skimage.transform.resize(feature, (224, 224), mode='constant')
    tmp_features.append(tmpFeature)

  # Return the training data in batches of size <batch_size> or less
  return batch_features_labels(tmp_features, labels, batch_size)


def load_preprocessed_validation_batch(batch_size=64, preprocessed_data_valid_path=''):
  '''
  Load the Preprocessed data and return them in batches of <batch_size> or less
  '''

  return load_preprocessed_batched(preprocessed_data_valid_path)


def load_label_names():
  return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


'''
from dlpipeline.base_config import cifar10_dataset_folder_path
from dlpipeline.transformation.vectors.one_hot_encoding import one_hot_encode

preprocess_and_save_data(cifar10_dataset_folder_path, one_hot_encode)
'''
