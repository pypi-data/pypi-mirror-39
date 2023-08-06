#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Augmentor

# https://augmentor.readthedocs.io/en/master/userguide/mainfeatures.html
from dlpipeline import DLPDataIterator

__author__ = 'cnheider'


def create_augmentor_pipeline(path="~/Datasets/mnist_png/training"):
  p = Augmentor.Pipeline(path)
  p.flip_top_bottom(probability=0.1)
  p.rotate(probability=0.3, max_left_rotation=5, max_right_rotation=5)

  print(p.status())

  return p


if __name__ == '__main__':
  import matplotlib.pyplot as plt

  p = create_augmentor_pipeline()
  g = p.keras_generator(batch_size=4)


  def generator_training(g, batch_size=32):
    import tensorflow.keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Flatten
    from tensorflow.keras.layers import Conv2D, MaxPooling2D

    import matplotlib.pyplot as plt

    num_classes = 10
    input_shape = (28, 28, 1)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
                  optimizer=tensorflow.keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    model.fit_generator(g, steps_per_epoch=len(p.augmentor_images) / batch_size, epochs=5, verbose=1)


  def diplay_images(g):
    for images, labels in g:
      image = images[0]
      label = labels[0]
      plt.imshow(image.reshape(28, 28), cmap="Greys")
      plt.show()
      break


class AugmentorAugmentor(DLPDataIterator):
  pass
