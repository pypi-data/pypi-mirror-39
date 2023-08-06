#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

from pathlib import Path

from .deep_label import *
from .first_level_label import *

from .splits import *

if __name__ == '__main__':
  HOME_DIRECTORY = Path.home()
  DATA_HOME = HOME_DIRECTORY / 'Nextcloud/Visual Computing Lab/Projects/IBBD5/Data'
  img_dir = '/home/captain/Nextcloud/Visual Computing Lab/Projects/IBBD5/Data/WorkSystems/images/'
  d = build_deep_level_image_list(img_dir)
  print(d)
