#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from keras_preprocessing.image import ImageDataGenerator

from dlpipeline import DLPDataIterator

__author__ = 'cnheider'

datagen = ImageDataGenerator(rotation_range=40,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             shear_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True,
                             fill_mode='nearest')

# RetinaLyze
validationdatagenerator = ImageDataGenerator()
traindatagenerator = ImageDataGenerator(width_shift_range=0.1,
                                        height_shift_range=0.1,
                                        rotation_range=15,
                                        zoom_range=0.1)


class KerasAugmentor(DLPDataIterator):
  pass
