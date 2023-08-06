#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import matplotlib.pyplot as plt
import numpy as np


def plot_value_array(i, predictions_array, true_label, class_names, show_ticks=True, size=8, rotation=90):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  this_plot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  this_plot[predicted_label].set_color('red')
  this_plot[true_label].set_color('blue')
  if show_ticks:
    _ = plt.xticks(range(len(class_names)), class_names, rotation=rotation, fontsize=size)
    # plt.tick_params(axis='both', which='minor', labelsize=size)
    # plot.tick_params(axis='both', which='major', labelsize=size*1.2)
