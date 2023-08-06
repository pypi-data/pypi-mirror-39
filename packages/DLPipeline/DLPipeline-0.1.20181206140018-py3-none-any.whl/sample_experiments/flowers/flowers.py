#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline import DataLoader, DLPAugmentor
from dlpipeline.classifier.tf_classifier import TFClassifier
from dlpipeline.embedder.tf_hub_embedder import TFHubEmbedder
from dlpipeline.utilities import to_lower_properties, parse_args
from dlpipeline.visualiser.tfvisualiser import TFVisualiser

if __name__ == '__main__':
  from sample_experiments.dog_or_cat import dog_or_cat_config as C

  C = to_lower_properties(C)
  Ca, unparsed = parse_args(C)

  data_loader = DataLoader(C)
  transformer = DLPAugmentor(data_loader)
  embedder = TFHubEmbedder(transformer)

  model = TFClassifier(data_loader, C=C)
  visualiser = TFVisualiser()

  model.learn(data_loader, C)

  model.save('', data_loader, C)
