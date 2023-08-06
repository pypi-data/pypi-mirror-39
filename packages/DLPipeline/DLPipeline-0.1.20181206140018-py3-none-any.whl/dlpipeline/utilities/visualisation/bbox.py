#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen

__author__ = 'cnheider'

import cv2
from matplotlib import pyplot as plt
import numpy as np

BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)


def visualize_bbox(img, bbox, class_id, class_idx_to_name, color=BOX_COLOR, thickness=2):
  x_min, y_min, w, h = bbox
  x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
  cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
  class_name = class_idx_to_name[class_id]
  ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
  cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
  cv2.putText(img, class_name, (x_min, y_min - int(0.3 * text_height)), cv2.FONT_HERSHEY_SIMPLEX, 0.35,
              TEXT_COLOR, lineType=cv2.LINE_AA)
  return img


def visualize(annotations, category_id_to_name):
  img = annotations['image'].copy()
  for idx, bbox in enumerate(annotations['bboxes']):
    img = visualize_bbox(img, bbox, annotations['category_id'][idx], category_id_to_name)
  plt.figure(figsize=(12, 12))
  plt.imshow(img)
  plt.show()


def augment_and_show(aug, image):
  r = aug(image=image)
  image = r['image']
  plt.figure(figsize=(10, 10))
  plt.imshow(image)
  plt.show()


def download_image(url):
  data = urlopen(url).read()
  image = decode_image(data)
  return image


def decode_image(data):
  data = np.frombuffer(data, np.uint8)
  image = cv2.imdecode(data, cv2.IMREAD_COLOR)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return image
