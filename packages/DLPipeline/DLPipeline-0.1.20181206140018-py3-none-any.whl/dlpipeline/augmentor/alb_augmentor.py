#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable

import albumentations as A
import matplotlib.pyplot as plt

from dlpipeline.utilities import DLPDataIterator
from dlpipeline.utilities.visualisation.bbox import visualize, decode_image, augment_and_show

__author__ = 'cnheider'


class AlbumentationsAugmentor(DLPDataIterator):
  def entry_point(self, data_iterator) -> Iterable:
    pass

  def __init__(self, C=None, aug_fn=None, p=.7):
    super().__init__(C)

    self._aug_fn = aug_fn
    if not self._aug_fn:
      self._aug_fn = self.get_strong_aug(p)

  @staticmethod
  def get_strong_aug(p):
    return A.Compose([
      A.Rotate(45, p=p),
      A.Flip(),
      A.Transpose(),
      A.OneOf([
        A.IAAAdditiveGaussianNoise(),
        A.GaussNoise(),
        ], p=0.2),
      A.OneOf([
        A.MotionBlur(p=.2),
        A.MedianBlur(blur_limit=3, p=.1),
        A.Blur(blur_limit=3, p=.1),
        ], p=0.2),
      A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=32, p=0.8),
      A.OneOf([
        A.OpticalDistortion(p=0.3),
        A.GridDistortion(p=.1),
        A.IAAPiecewiseAffine(p=0.3),
        ], p=0.2),
      A.OneOf([
        A.CLAHE(clip_limit=2),
        A.IAASharpen(),
        A.IAAEmboss(),
        A.RandomContrast(),
        A.RandomBrightness(),
        ], p=0.3),
      A.HueSaturationValue(p=0.3),
      ], p=p)

  @staticmethod
  def get_bbox_aug(aug,
                   min_area=0.,
                   min_visibility=0.):
    return A.Compose(aug, bbox_params={'format':        'coco',
                                       'min_area':      min_area,
                                       'min_visibility':min_visibility,
                                       'label_fields':  ['category_id']
                                       })

  def augment(self,
              images):
    if type(images) is iter:
      return [self._aug_fn(image=image) for image in images]

    return [self._aug_fn(image=images)]

  def augment_and_display(self, image, title=''):
    r = self._aug_fn(image=image)
    image = r['image']
    plt.figure(figsize=(10, 10))
    plt.title(title)
    plt.imshow(image)
    plt.show()


def main():
  augmentor = AlbumentationsAugmentor()

  with open('/home/captain/Pictures/cat_and_dog.jpg', 'rb') as f:
    image = decode_image(f.read())

  augment_and_show(augmentor, image)

  annotations = {'image':      image,
                 'bboxes':     [[366.7,
                                 80.84,
                                 132.8,
                                 181.84],
                                [5.66,
                                 138.95,
                                 147.09,
                                 164.88]],
                 'category_id':[18, 17]
                 }
  category_id_to_name = {17:'cat',
                         18:'dog'
                         }

  augmented = augmentor.get_bbox_aug([A.VerticalFlip(p=1.),
                                      A.HorizontalFlip(p=1.)])(**annotations)
  visualize(augmented, category_id_to_name)


if __name__ == '__main__':
  main()
