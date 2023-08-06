#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.modules import DataLoader, DefaultTransformer, DefaultRetrainModel, Visualiser
from dlpipeline.utilities import to_lower_properties, parse_args

__author__ = 'cnheider'

if __name__ == '__main__':
  from sample_experiments.bee_or_ant import bee_or_ant_config as C

  C = to_lower_properties(C)
  Ca, unparsed = parse_args(C)

  data_loader = DataLoader(C)
  transformer = DefaultTransformer(C)
  model = DefaultRetrainModel(data_loader, transformer, C)
  visualiser = Visualiser(C)

  model.learn(data_loader, C)
  model.test(data_loader, C)

  model.save(data_loader, C)
