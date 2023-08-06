#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import tqdm


class DownloadProgress(tqdm.tqdm):
  last_block = 0

  def hook(self, block_num=1, block_size=1, total_size=None):
    self.total = total_size
    self.update((block_num - self.last_block) * block_size)
    self.last_block = block_num


def example():
  from urllib.request import urlretrieve
  with DownloadProgress(unit='B', unit_scale=True, miniters=1, desc='CIFAR-10 Dataset') as progress_bar:
    urlretrieve(
        'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
        'cifar-10-python.tar.gz',
        progress_bar.hook)
