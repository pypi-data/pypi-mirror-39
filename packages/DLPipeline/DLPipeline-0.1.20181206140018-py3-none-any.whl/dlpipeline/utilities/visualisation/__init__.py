#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'cnheider'

import matplotlib.pyplot as plt
import numpy as np
import tqdm
from sklearn.preprocessing import LabelBinarizer


def display_image_predictions(features, labels, predictions):
  from dlpipeline.augmentor.transformation import load_label_names
  n_classes = 10
  label_names = load_label_names()
  label_binariser = LabelBinarizer()
  label_binariser.fit(range(n_classes))
  label_ids = label_binariser.inverse_transform(np.array(labels))

  fig, axs = plt.subplots(10, 2, figsize=(12, 24))

  margin = 0.05
  ind = np.arange(n_classes)
  width = (1. - 2. * margin) / n_classes

  for image_i, (feature, label_id, prediction) in tqdm.tqdm(enumerate(zip(features, label_ids, predictions))):
    correct_name = label_names[label_id]
    pred_name = label_names[np.argmax(prediction)]

    is_match = 'False'

    if np.argmax(prediction) == label_id:
      is_match = 'True'

    predictions_array = []
    prediction_names = []

    for index, pred_value in tqdm.tqdm(enumerate(prediction)):
      tmp_pred_name = label_names[index]
      predictions_array.append({tmp_pred_name:pred_value})
      prediction_names.append(tmp_pred_name)

    print(f'[{image_i}] ground truth: {correct_name}, predicted result: {pred_name} | {is_match}')
    print(f'\t-  {predictions_array}\n')

    #         print('image_i: ', image_i)
    #         print('axs: ', axs, ', axs len: ', len(axs))
    axs[image_i][0].imshow(feature)
    axs[image_i][0].set_title(pred_name)
    axs[image_i][0].set_axis_off()

    axs[image_i][1].barh(ind + margin, prediction, width)
    axs[image_i][1].set_yticks(ind + margin)
    axs[image_i][1].set_yticklabels(prediction_names)

  plt.tight_layout()
