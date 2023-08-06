#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warg import NamedOrderedDictionary

from dlpipeline import DLPDataLoader
from dlpipeline.classifier.pt_classifier import PTClassifier

from dlpipeline.utilities import to_lower_properties, parse_args
from dlpipeline.visualiser.tfvisualiser import TFVisualiser
import tensorflow as tf

if __name__ == '__main__':
  from sample_experiments.dog_or_cat import dog_or_cat_config as C

  C = to_lower_properties(C)

  tf.reset_default_graph()
  graph = tf.get_default_graph()
  with graph.as_default() as graph:
    with tf.Session(config=C.tf_config, graph=graph) as sess:
      module_specification = hub.load_module_spec(C.embedding_module)
      height, width = hub.get_expected_image_size(module_specification)
      depth = hub.get_num_image_channels(module_specification)

      data_loader = TFDataLoader(C=C,
                                 height=height,
                                 width=width,
                                 depth=depth,
                                 first_level_categories=True)

      augmentor = TFAugmentor(data_loader,
                              C=C,
                              input_height=height,
                              input_width=width,
                              input_depth=depth)

      cache_embeddings = not augmentor.augment_online

      embedder = TFHubEmbedder(augmentor,
                               C=C,
                               cache_embeddings=cache_embeddings)

      model = TFClassifier(embedder,
                           C=C,
                           input_size=embedder.embedding_size)

      # visualiser = Visualiser()

      init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
      sess.run(init_op)

      model.learn(sess,
                  C=C,
                  module_specification=module_specification)

      model.save(data_loader, C, embedder.module_specification)

      model.test(sess, data_loader,
                 C,
                 embedder=embedder,
                 graph_handles=NamedOrderedDictionary(resized_image_node=data_loader.resized_image_node,
                                                      jpeg_placeholder=data_loader.jpeg_placeholder))

      print('Finished')

  print('Finished')
