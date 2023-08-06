#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable

import imgaug as ia
from imgaug import augmenters as A
import matplotlib.image as mpimg
from dlpipeline.visualiser.visualisation.bbox import decode_image, augment_and_show, visualise

from dlpipeline import DLPAugmentor

__author__ = 'cnheider'


class ImgaugAugmentor(DLPAugmentor):
  def _entry_point(self, data_iterator, **kwargs) -> Iterable:
    return self.augment(data_iterator)

  def __init__(self, data_iterator, *, C=None, aug_fn=None, p=.7):
    super().__init__(data_iterator,C=C)

    self._aug_fn = aug_fn
    if not self._aug_fn:
      self._aug_fn = get_aug_pipe(p)

  def augment(self, images):
    if isinstance(images, tuple):
      s = [c for v in images[1].values() for c in v]
      a = []
      for image in s:
        img = mpimg.imread(image)
        a.append(img)
      return a

    return [self._aug_fn.augment_image(images)]


def get_aug_pipe(p=0.5):
  # Sometimes(0.5, ...) applies the given augmenter in 50% of all cases,
  # e.g. Sometimes(0.5, GaussianBlur(0.3)) would blur roughly every second image.
  sometimes = lambda aug:A.Sometimes(p, aug)

  # Define our sequence of augmentation steps that will be applied to every image
  # All augmenters with per_channel=0.5 will sample one value _per image_
  # in 50% of all cases. In all other cases they will sample new values
  # _per channel_.
  s = A.Sequential([A.Fliplr(0.5),  # horizontally flip 50% of all images
                    A.Flipud(0.2),  # vertically flip 20% of all images
                    # crop images by -5% to 10% of their height/width
                    sometimes(A.CropAndPad(percent=(-0.05, 0.1),
                                           pad_mode=ia.ALL,
                                           pad_cval=(0, 255)
                                           )),
                    sometimes(A.Affine(scale={"x":(0.8, 1.2), "y":(0.8, 1.2)},
                                       # scale images to 80-120% of their size, individually per axis
                                       translate_percent={"x":(-0.2, 0.2), "y":(-0.2, 0.2)},
                                       # translate by -20 to +20 percent (per axis)
                                       rotate=(-45, 45),  # rotate by -45 to +45 degrees
                                       shear=(-16, 16),  # shear by -16 to +16 degrees
                                       order=[0, 1],  # use nearest neighbour or bilinear interpolation (fast)
                                       cval=(0, 255),  # if mode is constant, use a cval between 0 and 255
                                       mode=ia.ALL
                                       # use any of scikit-image's warping modes (see 2nd image from the
                                       # top for examples)
                                       )),
                    # execute 0 to 5 of the following (less important) augmenters per image
                    # don't execute all of them, as that would often be way too strong
                    A.SomeOf((0, 5), [sometimes(A.Superpixels(p_replace=(0, 1.0), n_segments=(20, 200))),
                                      # convert images into their superpixel representation
                                      A.OneOf([A.GaussianBlur((0, 3.0)),
                                               # blur images with a sigma between 0 and 3.0
                                               A.AverageBlur(k=(2, 7)),
                                               # blur image using local means with kernel sizes between 2
                                               # and 7
                                               A.MedianBlur(k=(3, 11)),
                                               # blur image using local medians with kernel sizes between 2
                                               # and 7
                                               ]),
                                      A.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),  # sharpen images
                                      A.Emboss(alpha=(0, 1.0), strength=(0, 2.0)),  # emboss images
                                      # search either for all edges or for directed edges,
                                      # blend the result with the original image using a blobby mask
                                      A.SimplexNoiseAlpha(A.OneOf([
                                        A.EdgeDetect(alpha=(0.5, 1.0)),
                                        A.DirectedEdgeDetect(alpha=(0.5, 1.0), direction=(0.0, 1.0)),
                                        ])),
                                      A.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255),
                                                              per_channel=0.5),
                                      # add gaussian noise to images
                                      A.OneOf([A.Dropout((0.01, 0.1), per_channel=0.5),
                                               # randomly remove up to 10% of the pixels
                                               A.CoarseDropout((0.03, 0.15), size_percent=(0.02, 0.05),
                                                               per_channel=0.2),
                                               ]),
                                      A.Invert(0.05, per_channel=True),  # invert color channels
                                      A.Add((-10, 10), per_channel=0.5),
                                      # change brightness of images (by -10 to 10 of original value)
                                      A.AddToHueAndSaturation((-20, 20)),  # change hue and saturation
                                      # either change the brightness of the whole image (sometimes
                                      # per channel) or change the brightness of subareas
                                      A.OneOf([A.Multiply((0.5, 1.5), per_channel=0.5),
                                               A.FrequencyNoiseAlpha(
                                                   exponent=(-4, 0),
                                                   first=A.Multiply((0.5, 1.5), per_channel=True),
                                                   second=A.ContrastNormalization((0.5, 2.0))
                                                   )
                                               ]),
                                      A.ContrastNormalization((0.5, 2.0), per_channel=0.5),
                                      # improve or worsen the contrast
                                      A.Grayscale(alpha=(0.0, 1.0)),
                                      sometimes(A.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)),
                                      # move pixels locally around (with random strengths)
                                      sometimes(A.PiecewiseAffine(scale=(0.01, 0.05))),
                                      # sometimes move parts of the image around
                                      sometimes(A.PerspectiveTransform(scale=(0.01, 0.1)))
                                      ],
                             random_order=True
                             )
                    ],
                   random_order=True
                   )
  return s


def main(images):
  augmentor = ImgaugAugmentor(images)

  for image in augmentor:
    visualise(image[0])


if __name__ == '__main__':
  path__ = '/home/heider/Pictures/Screenshot_2018-12-04_16-50-53.png'

  with open(path__, 'rb') as f:
    image = decode_image(f.read())

  main([image, image, image])
