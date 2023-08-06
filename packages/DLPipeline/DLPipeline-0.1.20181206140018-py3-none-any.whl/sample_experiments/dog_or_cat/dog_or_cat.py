#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dlpipeline.modules import DataLoader, DefaultTransformer, DefaultRetrainModel, Visualiser
from dlpipeline.utilities import to_lower_properties, parse_args

if __name__ == '__main__':
  from sample_experiments.dog_or_cat import dog_or_cat_config as C

  C = to_lower_properties(C)
  Ca, unparsed = parse_args(C)

  data_loader = DataLoader(C)
  transformer = DefaultTransformer()
  model = DefaultRetrainModel(data_loader, transformer, C)
  visualiser = Visualiser()

  model.learn(data_loader, transformer, C)

  model.save('', data_loader, C)
